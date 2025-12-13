"""Dependency-aware execution helpers for TaskOrchestrator.

This module centralizes all logic for executing prepared command entries
with or without dependency constraints so TaskOrchestrator can delegate the
heavy lifting and stay focused on orchestration concerns.

Task entry contract:
* ``task_entries`` is a ``list`` of ``(PreparedEntry, dependencies)`` pairs.
* Dependency names are fully namespaced (e.g. ``task:command``) so they can be
    compared against ``dep_completed`` and ``failed_commands`` sets.

State invariants maintained by this module:
* Every command eventually produces a ``CommandResult`` (success, cancelled, or
    dependency skip).
* ``dep_completed`` and ``completed_commands`` only include successful
    command names; failed commands never unblock downstream work.
* ``failed_commands`` is treated as the single source of truth for
    dependency skips, ensuring dependent commands cannot run once an upstream
    failure (or unresolved dependency) is detected.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from hil_testbench.run.exceptions import ExecutionError, HILTestbenchError
from hil_testbench.run.execution.command_result import (
    CancellationClassification,
    CommandResult,
    CommandStatus,
)
from hil_testbench.run.execution.command_runner import CommandRunner
from hil_testbench.run.execution.command_spec import CommandSpec, PreparedEntry
from hil_testbench.run.logging.task_logger import LogLevel, LogScope


@dataclass(slots=True)
class BatchExecutionResult:
    """Structured response for dependency batch execution."""

    entries: list[PreparedEntry]
    results: list[CommandResult]
    missing_results: list[CommandResult]
    reason: str | None
    cancelled: bool


@dataclass(slots=True)
class DependencyState:
    """Mutable execution state tracked while processing dependencies."""

    results: list[CommandResult]
    dep_completed: set[str]
    remaining_entries: list[tuple[PreparedEntry, list[str] | None]]
    cancellation_requested: bool
    reason: str | None


class ReadinessPlanner:
    """Determines which entries can execute based on dependency state."""

    def __init__(self, *, failed_commands: set[str]):
        self._failed_commands = failed_commands

    def partition_entries(
        self,
        entries: list[tuple[PreparedEntry, list[str] | None]],
        completed: set[str],
    ) -> tuple[
        list[tuple[PreparedEntry, list[str] | None]],
        list[tuple[PreparedEntry, list[str] | None]],
    ]:
        ready: list[tuple[PreparedEntry, list[str] | None]] = []
        blocked: list[tuple[PreparedEntry, list[str] | None]] = []
        for entry, deps in entries:
            dependencies = deps or []
            if any(
                (dep not in completed) or (dep in self._failed_commands) for dep in dependencies
            ):
                blocked.append((entry, dependencies))
            else:
                ready.append((entry, dependencies))
        return ready, blocked


class CancellationHandler:
    """Centralizes building cancellation/skip CommandResults."""

    def __init__(
        self,
        *,
        runner: CommandRunner,
        cancellation_label: str,
        failed_commands: set[str],
        failed_commands_state: set[str] | None,
    ) -> None:
        self._runner = runner
        self._cancellation_label = cancellation_label
        self._failed_commands = failed_commands
        self._failed_commands_state = failed_commands_state

    def handle_remaining(
        self,
        remaining: list[tuple[PreparedEntry, list[str] | None]],
        cancellation_requested: bool,
        reason: str | None,
        dep_completed: set[str],
    ) -> list[CommandResult]:
        if not remaining:
            return []
        if cancellation_requested:
            classification = self._runner.get_cancel_classification()
            return [
                build_cancelled_result_from_entry(
                    entry_tuple,
                    reason or self._cancellation_label,
                    classification=classification,
                )
                for entry_tuple, _ in remaining
            ]
        return self._build_dependency_skip_results(remaining, dep_completed)

    def _build_dependency_skip_results(
        self,
        remaining: list[tuple[PreparedEntry, list[str] | None]],
        dep_completed: set[str],
    ) -> list[CommandResult]:
        task_logger = self._runner.get_task_logger()
        results: list[CommandResult] = []
        for entry_tuple, deps in remaining:
            spec = entry_tuple.spec
            command_name = spec.command_name
            task_name = spec.task_name
            dependencies = deps or []
            failed_deps = [dep for dep in dependencies if dep in self._failed_commands]
            unresolved_deps = [
                dep
                for dep in dependencies
                if dep not in self._failed_commands and dep not in dep_completed
            ]
            if not failed_deps and not unresolved_deps:
                continue
            if failed_deps:
                blocking_deps = failed_deps
                message_prefix = "Skipped due to failed dependencies"
            else:
                blocking_deps = unresolved_deps
                message_prefix = "Skipped because dependencies never completed"
            task_logger.log(
                "dependency_failed_skip",
                LogLevel.WARNING,
                scope=LogScope.COMMAND,
                task=task_name,
                command=command_name,
                failed_dependencies=", ".join(blocking_deps),
            )
            self._failed_commands.add(command_name)
            if self._failed_commands_state is not None:
                self._failed_commands_state.add(command_name)
            results.append(
                _build_dependency_skip_result(
                    command_name,
                    task_name,
                    blocking_deps,
                    message_prefix=message_prefix,
                    spec=spec,
                )
            )
        return results


class DependencyExecutor:
    """Execute prepared command entries with dependency awareness."""

    def __init__(
        self,
        *,
        runner: CommandRunner,
        backend: Any | None,
        command_validators: dict[str, Any],
        failed_commands: set[str],
        validate_results: Callable[..., None],
        completed_commands: set[str] | None,
        failed_commands_state: set[str] | None,
        cancel_reason: str | None,
        cancellation_label: str,
        executor: ThreadPoolExecutor,
    ) -> None:
        self._runner = runner
        self._backend = backend
        self._command_validators = command_validators
        self._failed_commands = failed_commands
        self._validate_results = validate_results
        self._completed_commands = completed_commands
        self._failed_commands_state = failed_commands_state
        self._cancel_reason = cancel_reason
        self._cancellation_label = cancellation_label
        self._executor = executor
        self._readiness_planner = ReadinessPlanner(failed_commands=self._failed_commands)
        self._cancellation_handler = CancellationHandler(
            runner=self._runner,
            cancellation_label=self._cancellation_label,
            failed_commands=self._failed_commands,
            failed_commands_state=self._failed_commands_state,
        )
        self._active_futures: set[Future] = set()
        self._futures_lock = threading.Lock()
        self._cancel_listener_registered = False
        self._cancel_listener = self._cancel_active_futures
        register = getattr(self._runner, "register_cancel_listener", None)
        if callable(register):
            register(self._cancel_listener)
            self._cancel_listener_registered = True

    def shutdown(self) -> None:
        """Release runner hooks and stop any queued futures."""

        try:
            if self._cancel_listener_registered:
                unregister = getattr(self._runner, "unregister_cancel_listener", None)
                if callable(unregister):
                    unregister(self._cancel_listener)
        finally:
            self._cancel_listener_registered = False
            self._cancel_active_futures()

    def execute_with_dependencies(
        self,
        task_entries: list[tuple[PreparedEntry, list[str] | None]],
        *,
        password: str | None,
    ) -> tuple[list[CommandResult], bool, str | None]:
        state = self._initialize_dependency_state(task_entries)

        while state.remaining_entries:
            ready, blocked = self._readiness_planner.partition_entries(
                state.remaining_entries,
                state.dep_completed,
            )
            if not ready:
                state.remaining_entries = blocked
                break

            self._process_ready_entries(
                ready_entries=ready,
                blocked_entries=blocked,
                password=password,
                state=state,
            )

            if state.cancellation_requested:
                break

        if state.remaining_entries:
            state.results.extend(
                self._cancellation_handler.handle_remaining(
                    state.remaining_entries,
                    state.cancellation_requested,
                    state.reason,
                    state.dep_completed,
                )
            )

        return state.results, state.cancellation_requested, state.reason

    def _initialize_dependency_state(
        self, task_entries: list[tuple[PreparedEntry, list[str] | None]]
    ) -> DependencyState:
        return DependencyState(
            results=[],
            dep_completed=set(),
            remaining_entries=task_entries.copy(),
            cancellation_requested=False,
            reason=self._cancel_reason,
        )

    def _process_ready_entries(
        self,
        *,
        ready_entries: list[tuple[PreparedEntry, list[str] | None]],
        blocked_entries: list[tuple[PreparedEntry, list[str] | None]],
        password: str | None,
        state: DependencyState,
    ) -> None:
        batch_result = self._run_dependency_batch(ready_entries, password, state.reason)
        state.results.extend(batch_result.results)
        state.results.extend(batch_result.missing_results)
        state.cancellation_requested = state.cancellation_requested or batch_result.cancelled
        state.reason = batch_result.reason

        successful_commands = {
            result.command_name for result in batch_result.results if result.success
        }
        state.dep_completed.update(successful_commands)
        if self._completed_commands is not None:
            self._completed_commands.update(successful_commands)

        state.remaining_entries = blocked_entries

    def execute_without_dependencies(
        self,
        task_entries: list[tuple[PreparedEntry, list[str] | None]],
        *,
        password: str | None,
    ) -> tuple[list[CommandResult], bool, str | None]:
        cancellation_requested = False
        reason = self._cancel_reason

        entries_only = [entry for entry, _ in task_entries]
        results = self._execute_partitioned_entries(entries_only, password=password)
        missing_results = append_missing_cancellations(
            entries_only,
            results,
            reason,
            classification=self._runner.get_cancel_classification(),
        )
        if missing_results and reason is None:
            reason = self._cancellation_label
        if self._runner.was_cancelled():
            cancellation_requested = True
            reason = reason or self._cancellation_label
        if missing_results:
            cancellation_requested = True
            results.extend(missing_results)

        self._validate_results(
            results,
            command_validators=self._command_validators,
            failed_commands=self._failed_commands,
            runner=self._runner,
            display_backend=self._backend,
            completed_commands=self._completed_commands,
            failed_commands_state=self._failed_commands_state,
        )

        return results, cancellation_requested, reason

    def _run_dependency_batch(
        self,
        ready_entries: list[tuple[PreparedEntry, list[str] | None]],
        password: str | None,
        reason: str | None,
    ) -> BatchExecutionResult:
        batch_entries = [entry for entry, _ in ready_entries]
        batch_results = self._execute_partitioned_entries(batch_entries, password=password)

        self._validate_results(
            batch_results,
            command_validators=self._command_validators,
            failed_commands=self._failed_commands,
            runner=self._runner,
            display_backend=self._backend,
            completed_commands=self._completed_commands,
            failed_commands_state=self._failed_commands_state,
        )

        missing_results = append_missing_cancellations(
            batch_entries,
            batch_results,
            reason,
            classification=self._runner.get_cancel_classification(),
        )

        updated_reason = reason
        if (missing_results or self._runner.was_cancelled()) and updated_reason is None:
            updated_reason = self._cancellation_label

        batch_cancelled = bool(missing_results) or self._runner.was_cancelled()
        return BatchExecutionResult(
            entries=batch_entries,
            results=batch_results,
            missing_results=missing_results,
            reason=updated_reason,
            cancelled=batch_cancelled,
        )

    def _execute_partitioned_entries(
        self,
        entries: list[PreparedEntry],
        *,
        password: str | None,
    ) -> list[CommandResult]:
        if not entries:
            return []
        sequential_entries: list[PreparedEntry] = []
        parallel_entries: list[PreparedEntry] = []
        for entry in entries:
            if self._entry_allows_parallel(entry):
                parallel_entries.append(entry)
            else:
                sequential_entries.append(entry)

        results: list[CommandResult] = []
        if sequential_entries:
            results.extend(
                self._run_commands(
                    sequential_entries,
                    password=password,
                    use_executor=False,
                )
            )
        if parallel_entries:
            results.extend(
                self._run_commands(
                    parallel_entries,
                    password=password,
                    use_executor=True,
                )
            )
        return results

    def _run_commands(
        self,
        entries: list[PreparedEntry],
        *,
        password: str | None,
        use_executor: bool,
    ) -> list[CommandResult]:
        if not entries:
            return []
        runner = self._run_parallel_commands if use_executor else self._run_sequential_commands
        return runner(entries, password)

    def _run_sequential_commands(
        self,
        entries: list[PreparedEntry],
        password: str | None,
    ) -> list[CommandResult]:
        results: list[CommandResult] = []
        for entry in entries:
            if self._runner.was_cancelled():
                break
            try:
                results.append(
                    self._runner.execute_entry(
                        entry,
                        password=password,
                        log_output=True,
                        sample_lines=0,
                    )
                )
            except KeyboardInterrupt:
                self._handle_keyboard_interrupt()
                break
        return results

    def _run_parallel_commands(
        self,
        entries: list[PreparedEntry],
        password: str | None,
    ) -> list[CommandResult]:
        futures: list[Future] = []
        try:
            for entry in entries:
                future = self._executor.submit(
                    self._runner.execute_entry,
                    entry,
                    password=password,
                    log_output=True,
                    sample_lines=0,
                )
                futures.append(future)
                self._track_future(future)
            results: list[CommandResult] = []
            interrupted = False
            for future in futures:
                try:
                    results.append(future.result())
                except CancelledError:
                    continue
                except KeyboardInterrupt:
                    interrupted = True
                    break
                finally:
                    self._untrack_future(future)
            if interrupted:
                self._handle_keyboard_interrupt()
            return results
        except Exception as exc:  # noqa: BLE001
            normalized = self._normalize_runner_exception(
                exc,
                phase="executor",
                commands=[entry.spec.command_name for entry in entries],
            )
            if normalized is exc:
                raise
            raise normalized from exc

    def _normalize_runner_exception(
        self,
        exc: Exception,
        *,
        phase: str,
        commands: list[str],
    ) -> HILTestbenchError:
        context = {
            "phase": phase,
            "commands": ", ".join(commands) if commands else None,
        }
        filtered_context = {k: v for k, v in context.items() if v}
        if isinstance(exc, HILTestbenchError):
            if filtered_context:
                exc.add_context(**filtered_context)
            return exc
        try:
            raise ExecutionError(
                f"Runner failed during {phase} execution",
                context=filtered_context,
            ) from exc
        except ExecutionError as wrapped:
            return wrapped

    @staticmethod
    def _entry_allows_parallel(entry: PreparedEntry) -> bool:
        if entry.spec.exclusive:
            return False
        func = entry.func
        return getattr(func, "_task_concurrent", True)

    def _track_future(self, future: Future) -> None:
        with self._futures_lock:
            self._active_futures.add(future)

    def _untrack_future(self, future: Future) -> None:
        with self._futures_lock:
            self._active_futures.discard(future)

    def _cancel_active_futures(self) -> None:
        with self._futures_lock:
            futures = list(self._active_futures)
            self._active_futures.clear()
        for future in futures:
            future.cancel()

    def _handle_keyboard_interrupt(self) -> None:
        self._cancel_active_futures()


def append_missing_cancellations(
    entries: list[PreparedEntry],
    existing_results: list[CommandResult],
    reason: str | None,
    *,
    classification: CancellationClassification | None = None,
) -> list[CommandResult]:
    """Build CommandResults for entries that were not executed."""
    existing_names = {res.command_name for res in existing_results}
    missing: list[CommandResult] = []
    for entry in entries:
        name = entry.spec.command_name
        if name not in existing_names:
            missing.append(
                build_cancelled_result_from_entry(
                    entry,
                    reason,
                    classification=classification,
                )
            )
    return missing


def build_cancelled_result_from_entry(
    entry: PreparedEntry,
    reason: str | None,
    *,
    classification: CancellationClassification | None = None,
) -> CommandResult:
    now = datetime.now(UTC)
    spec = entry.spec
    command_name = spec.command_name
    task_name = spec.task_name
    stop_due_duration = classification == CancellationClassification.DURATION_LIMIT
    status = CommandStatus.STOPPED if stop_due_duration else CommandStatus.CANCELLED
    if reason:
        message = reason
    elif stop_due_duration:
        message = "Stopped after duration limit"
    else:
        message = "Command cancelled"
    return CommandResult(
        command_name=command_name,
        success=True,
        return_code=-1,
        spec=spec,
        status=status,
        status_message=message,
        task_name=task_name,
        start_time=now,
        end_time=now,
        duration=0.0,
        cancelled=not stop_due_duration,
        cancellation_classification=classification,
    )


def _build_dependency_skip_result(
    command_name: str,
    task_name: str,
    blocking_deps: list[str],
    *,
    message_prefix: str,
    spec: CommandSpec | None = None,
) -> CommandResult:
    now = datetime.now(UTC)
    return CommandResult(
        command_name=command_name,
        success=False,
        return_code=-1,
        spec=spec,
        status=CommandStatus.CANCELLED,
        status_message=f"{message_prefix}: {', '.join(blocking_deps)}",
        task_name=task_name,
        start_time=now,
        end_time=now,
        duration=0.0,
    )
