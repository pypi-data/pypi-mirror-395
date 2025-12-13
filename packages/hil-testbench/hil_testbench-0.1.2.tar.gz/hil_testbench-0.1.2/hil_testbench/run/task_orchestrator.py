"""TaskOrchestrator - converts task objects to execution graphs.

Tasks never see orchestration internals. This module handles:
- Building CommandRunner from config
- Converting task declarations to TaskDefinition
- Orchestrating multi-task execution via ExecutionSession
- Display backend lifecycle management
- Result aggregation and reporting
"""

from __future__ import annotations

import os
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Any

from rich.console import Console

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.display.display_lifecycle import DisplayLifecycle
from hil_testbench.run.exceptions import ConfigurationError, ExecutionError, HILTestbenchError
from hil_testbench.run.execution.command_preparer import (
    CommandPreparer,
    PreparedCommands,
)
from hil_testbench.run.execution.command_result import CommandResult
from hil_testbench.run.execution.command_runner import CommandRunner
from hil_testbench.run.execution.dependency_executor import (
    DependencyExecutor,
    build_cancelled_result_from_entry,
)
from hil_testbench.run.execution.execution_session import ExecutionSession
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.orchestration.dag_builder import DAGBuilder
from hil_testbench.run.orchestration.multi_task_planner import (
    MultiTaskPlan,
    MultiTaskPlanner,
)
from hil_testbench.run.orchestration.result_aggregator import ResultAggregator
from hil_testbench.run.orchestration.runtime_context import RuntimeContextBuilder
from hil_testbench.run.results.task_outcome import MultiTaskOutcome
from hil_testbench.run.session.forced_cleanup import ForcedCleanupPlanEntry, OrphanDetector
from hil_testbench.task.specs import CommandDefinition, TaskDefinition

EXECUTION_CANCELLED = "Execution cancelled"


class TaskOrchestrator:
    """Orchestrates task-to-command transformation and execution."""

    def __init__(
        self,
        *,
        dependencies: TaskOrchestratorDependencies | None = None,
        console: Console | None = None,
    ) -> None:
        """Initialize TaskOrchestrator with explicit dependencies."""

        if dependencies is None:
            dependencies = TaskOrchestratorDependencies.build(console=console)
        elif console is not None:
            raise ConfigurationError(
                "TaskOrchestrator received both explicit dependencies and console",
                context={
                    "console_provided": True,
                },
            )

        self._deps = dependencies
        self._task_logger: TaskLogger | None = None
        self._display_lifecycle = dependencies.display_lifecycle
        self._command_preparer = dependencies.command_preparer
        self._multi_task_planner = dependencies.multi_task_planner
        self._runtime_builder = dependencies.runtime_builder
        self._result_aggregator = dependencies.result_aggregator
        self._command_runner: CommandRunner | None = None
        self._cancel_event: threading.Event | None = None
        self._local_cancelled = False

    def get_task_logger(self):
        """Get the task logger created during execution.

        Returns:
            TaskLogger instance or None if execution hasn't started
        """
        return self._task_logger

    def execute_multiple(self, tasks: list[Any], configs: list[TaskConfig]) -> MultiTaskOutcome:
        """Execute multiple tasks concurrently with cross-task dependencies."""

        self._validate_task_lists(tasks, configs)
        if not configs:
            raise ConfigurationError(
                "At least one task/config pair is required",
            )

        primary_config = configs[0]
        runtime_context = self._runtime_builder.build(primary_config)
        runner = runtime_context.runner
        self._command_runner = runner
        self._local_cancelled = False
        self._cancel_event = self._resolve_cancel_event(runner)
        task_logger = runtime_context.task_logger
        self._task_logger = task_logger
        try:
            plan = self._build_multi_task_plan(
                tasks,
                configs,
                task_logger=task_logger,
            )
        except HILTestbenchError as error:
            self._log_plan_failure(task_logger, error, task_count=len(tasks))
            self._safe_runner_shutdown(runner)
            raise
        except Exception as error:  # noqa: BLE001
            self._log_plan_failure(task_logger, error, task_count=len(tasks))
            self._safe_runner_shutdown(runner)
            raise ConfigurationError(
                "Failed to build multi-task plan",
                context={
                    "task_count": len(tasks),
                    "error_type": type(error).__name__,
                },
            ) from error
        dependency_resolver = plan.create_dependency_resolver(task_logger)
        cleanup_plan = self._build_forced_cleanup_plan(plan.all_task_defs)
        self._detect_orphans(
            runner,
            cleanup_plan,
            pre_cleanup=getattr(primary_config.run_config, "pre_cleanup", False),
        )
        runner.configure_forced_cleanup(
            cleanup_plan,
            pre_cleanup=getattr(primary_config.run_config, "pre_cleanup", False),
            force_cleanup=getattr(primary_config.run_config, "force_cleanup", False),
        )

        duration_opt = plan.primary_config.duration
        duration = duration_opt if duration_opt is not None else ""
        session = self._start_execution_session(
            runner=runner,
            process_tracker=runtime_context.process_tracker,
            task_logger=task_logger,
            duration=duration,
            task_count=len(plan.all_task_defs),
        )
        self._display_lifecycle.initialize_task_displays(
            plan.namespaced_task_defs,
            task_logger,
            session,
            duration,
        )

        all_results = self._run_task_definitions(
            runner,
            [plan.merged_task_def],
            namespaced_task_defs=plan.namespaced_task_defs,
            password=plan.primary_config.password,
            config=plan.primary_config,
            config_by_task=plan.config_by_task,
            completed_commands=session.completed_commands,
            failed_commands_state=session.failed_commands,
            duration=duration,
            dependency_resolver=dependency_resolver,
        )
        task_outcomes = self._result_aggregator.aggregate(
            all_results, plan.all_task_defs, runner, task_logger
        )

        try:
            return MultiTaskOutcome(tasks=task_outcomes)
        finally:
            session.shutdown()

    def _start_execution_session(
        self,
        *,
        runner: CommandRunner,
        process_tracker: Any,
        task_logger: TaskLogger,
        duration: str | None,
        task_count: int,
    ) -> ExecutionSession:
        duration_seconds = self._parse_duration_seconds(duration, task_logger)
        session = ExecutionSession(task_logger, runner, process_tracker, duration_seconds)
        runner.attach_session(session)
        session.start_duration_guard()
        duration_text = "indefinite" if duration_seconds is None else f"{duration_seconds:.0f}s"
        task_logger.log(
            "session_start",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            message=f"Session start | tasks={task_count} | duration={duration_text}",
            task_count=task_count,
            duration=duration,
            duration_seconds=duration_seconds,
            parallel=True,
        )
        return session

    @staticmethod
    def _parse_duration_seconds(duration: str | None, task_logger: TaskLogger) -> float | None:
        if duration is None:
            return None
        try:
            seconds = float(duration)
        except (TypeError, ValueError):
            task_logger.log(
                "invalid_session_duration",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="Duration must be numeric; defaulting to indefinite",
                provided_value=duration,
            )
            return None
        if seconds <= 0:
            task_logger.log(
                "invalid_session_duration",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="Duration must be > 0 seconds; defaulting to indefinite",
                provided_value=duration,
            )
            return None
        return seconds

    def was_cancelled(self) -> bool:
        """Return True when the active command runner has been cancelled."""
        event = self._cancel_event
        if event and event.is_set():
            return True
        if self._local_cancelled:
            return True
        if self._command_runner is None:
            return False
        return self._command_runner.was_cancelled()

    def consume_interrupt_flag(self) -> bool:
        """Return True if an external interrupt was observed for the run."""
        if self._command_runner is None:
            return False
        consumer = getattr(self._command_runner, "consume_interrupt_flag", None)
        return bool(consumer() if callable(consumer) else False)

    def _validate_task_lists(self, tasks: list[Any], configs: list[TaskConfig]) -> None:
        if len(tasks) != len(configs):
            raise ConfigurationError(
                "Task/config count mismatch",
                context={
                    "tasks": len(tasks),
                    "configs": len(configs),
                },
            )
        for task in tasks:
            self._validate_task_interface(task)

    def _validate_task_interface(self, task: Any) -> None:
        """Early validation of the task interface to guide authors.

        Requirements:
        - commands attribute must exist and be callable
        """
        if not hasattr(task, "commands") or not callable(task.commands):
            raise ConfigurationError(
                "Task must define a callable commands(config) method",
                context={
                    "task": task.__class__.__name__,
                    "requirement": "REQ-TASK-001",
                },
            )

    def _make_logged_command_wrapper(
        self,
        command_func: Callable,
        task_name: str,
        command_name: str,
        runner: CommandRunner,
        *,
        concurrent: bool,
    ) -> Callable:
        """Wrap command function with start/finish/error logging for display."""

        @wraps(command_func)
        def wrapper(ctx: Any) -> Any:
            logger = runner.get_task_logger()
            backend = self._display_lifecycle.get_display_backend(logger)
            start_time = datetime.now()
            self._display_lifecycle.handle_command_start(
                logger,
                backend,
                task_name,
                command_name,
            )
            try:
                result = command_func(ctx)
                self._display_lifecycle.handle_command_completion(
                    logger,
                    backend,
                    task_name,
                    command_name,
                    result,
                )
                return result
            except Exception as exc:  # pylint: disable=broad-except
                normalized = self._normalize_orchestrator_exception(
                    exc,
                    message="Command wrapper raised unexpected exception",
                    context={"task": task_name, "command": command_name},
                )
                self._display_lifecycle.handle_command_exception(
                    logger,
                    backend,
                    task_name,
                    command_name,
                    start_time,
                    normalized,
                )
                if normalized is exc:
                    raise
                raise normalized from exc

        wrapper._task_name = task_name  # type: ignore[attr-defined]
        wrapper._command_name = command_name  # type: ignore[attr-defined]
        wrapper._task_concurrent = concurrent  # type: ignore[attr-defined]
        return wrapper

    def _run_task_definitions(
        self,
        runner: CommandRunner,
        task_definitions: Iterable[TaskDefinition],
        *,
        namespaced_task_defs: list[TaskDefinition] | None = None,
        password: str | None = None,
        config: TaskConfig | None = None,
        config_by_task: dict[str, TaskConfig] | None = None,
        completed_commands: set[str] | None = None,
        failed_commands_state: set[str] | None = None,
        duration: str | None = None,
        dependency_resolver: Callable[[list[CommandDefinition]], list[CommandDefinition]],
    ) -> list[CommandResult]:
        """Execute task definitions by translating them to TaskEntry objects."""

        if dependency_resolver is None:
            raise ConfigurationError(
                "Dependency resolver must be provided (single DAG per run)",
                context={
                    "remediation": (
                        "Call MultiTaskPlanner.build_plan() before execution so the"
                        " shared DAG resolver can be attached to command preparation."
                    ),
                },
            )

        task_defs = list(task_definitions)
        task_names = [task_def.name for task_def in task_defs]
        task_logger = runner.get_task_logger()
        task_def_map = self._build_task_definition_map(namespaced_task_defs)
        failed_commands: set[str] = set()
        try:
            prepared = self._command_preparer.prepare(
                runner,
                task_defs,
                task_logger=task_logger,
                task_def_map=task_def_map,
                failed_commands=failed_commands,
                config=config,
                config_by_task=config_by_task,
                duration=duration,
                wrap_command=self._make_logged_command_wrapper,
                dependency_resolver=dependency_resolver,
            )
        except Exception as exc:  # noqa: BLE001
            normalized = self._normalize_orchestrator_exception(
                exc,
                message="Failed to prepare command entries",
                context={"tasks": task_names or None},
            )
            if normalized is exc:
                raise
            raise normalized from exc

        if not (task_entries := prepared.entries):
            return []

        if prepared.cancellation_requested:
            return self._handle_preparation_cancellation(
                runner, task_entries, prepared.cancel_reason
            )

        try:
            return self._execute_prepared_entries(
                runner,
                prepared,
                password,
                completed_commands,
                failed_commands_state,
            )
        except Exception as exc:  # noqa: BLE001
            normalized = self._normalize_orchestrator_exception(
                exc,
                message="Failed to execute prepared command entries",
                context={
                    "tasks": task_names or None,
                    "entry_count": len(prepared.entries),
                },
            )
            if normalized is exc:
                raise
            raise normalized from exc

    # Legacy summary helper removed: GraphExecutor provides unified aggregation.

    def _build_multi_task_plan(
        self,
        tasks: list[Any],
        configs: list[TaskConfig],
        *,
        task_logger: TaskLogger | None = None,
    ) -> MultiTaskPlan:
        return self._multi_task_planner.build_plan(tasks, configs, task_logger=task_logger)

    def _handle_preparation_cancellation(
        self,
        runner: CommandRunner,
        task_entries: list[tuple],
        reason: str | None,
    ) -> list[CommandResult]:
        cancel_reason = reason or EXECUTION_CANCELLED
        self._record_execution_cancellation(runner, True, cancel_reason)
        logger = runner.get_task_logger()
        logger.log(
            "preparation_cancelled",
            LogLevel.INFO,
            scope=LogScope.FRAMEWORK,
            message="Execution skipped due to cancellation before run",
            reason=cancel_reason,
        )
        classification = runner.get_cancel_classification()
        return [
            build_cancelled_result_from_entry(
                entry,
                cancel_reason,
                classification=classification,
            )
            for entry, _ in task_entries
        ]

    def _execute_prepared_entries(
        self,
        runner: CommandRunner,
        prepared: PreparedCommands,
        password: str | None,
        completed_commands: set[str] | None,
        failed_commands_state: set[str] | None,
    ) -> list[CommandResult]:
        with self._create_executor() as executor_pool:
            dependency_executor = DependencyExecutor(
                runner=runner,
                backend=prepared.backend,
                command_validators=prepared.command_validators,
                failed_commands=prepared.failed_commands,
                validate_results=self._result_aggregator.validate_results,
                completed_commands=completed_commands,
                failed_commands_state=failed_commands_state,
                cancel_reason=prepared.cancel_reason,
                cancellation_label=EXECUTION_CANCELLED,
                executor=executor_pool,
            )
            try:
                if self._has_dependencies(prepared.entries):
                    results, cancelled, reason = dependency_executor.execute_with_dependencies(
                        prepared.entries,
                        password=password,
                    )
                    self._record_execution_cancellation(runner, cancelled, reason)
                    return results

                results, cancelled, reason = dependency_executor.execute_without_dependencies(
                    prepared.entries,
                    password=password,
                )
                self._record_execution_cancellation(runner, cancelled, reason)
                return results
            finally:
                dependency_executor.shutdown()

    @staticmethod
    def _create_executor() -> ThreadPoolExecutor:
        workers = min(32, (os.cpu_count() or 1) + 4)
        return ThreadPoolExecutor(max_workers=workers, thread_name_prefix="task-orchestrator")

    @staticmethod
    def _has_dependencies(task_entries: list[tuple]) -> bool:
        return any(deps for _, deps in task_entries if deps)

    @staticmethod
    def _build_forced_cleanup_plan(
        task_definitions: list[TaskDefinition] | None,
    ) -> dict[str, ForcedCleanupPlanEntry]:
        plan: dict[str, ForcedCleanupPlanEntry] = {}
        if not task_definitions:
            return plan

        for task_def in task_definitions:
            spec = getattr(task_def, "cleanup_spec", None)
            if spec is None or getattr(spec, "is_empty", lambda: True)():
                continue

            hosts = TaskOrchestrator._collect_hosts(task_def.commands)
            plan[task_def.name] = ForcedCleanupPlanEntry(
                task_name=task_def.name,
                spec=spec,
                hosts=tuple(hosts),
            )
        return plan

    @staticmethod
    def _collect_hosts(commands: list[CommandDefinition]) -> list[Any | None]:
        hosts: list[Any | None] = []
        seen: set[str] = set()
        for command in commands:
            host = getattr(command, "host", None)
            if host is None or getattr(host, "local", False):
                key = "local"
            else:
                describe = getattr(host, "as_string", None)
                key = describe() if callable(describe) else str(host)
            key = str(key)
            if key in seen:
                continue
            seen.add(key)
            hosts.append(None if key == "local" else host)
        return hosts

    @staticmethod
    def _build_task_definition_map(
        namespaced_task_defs: list[TaskDefinition] | None,
    ) -> dict[str, TaskDefinition]:
        if not namespaced_task_defs:
            return {}
        return {task_def.name: task_def for task_def in namespaced_task_defs}

    def _detect_orphans(
        self,
        runner: CommandRunner,
        cleanup_plan: dict[str, ForcedCleanupPlanEntry],
        *,
        pre_cleanup: bool,
    ) -> None:
        """Scan for orphan processes before execution and warn/remediate."""

        if not cleanup_plan:
            return
        task_logger = self._task_logger or runner.get_task_logger()
        if task_logger is None:
            return
        detector = OrphanDetector(
            logger=task_logger,
            ssh_manager=getattr(runner, "_ssh_manager", None),
        )
        findings = detector.detect(cleanup_plan)
        if not findings:
            return

        for match in findings:
            task_logger.log(
                "orphan_process_detected",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=match.task_name,
                host=match.host,
                pids=list(match.pids),
                patterns=list(match.patterns),
                ports=list(match.ports),
                message=(
                    "Orphan processes detected before execution. Enable pre_cleanup=true and ensure CleanupSpec covers these targets."
                ),
            )

        if pre_cleanup:
            task_logger.log(
                "orphan_process_pre_cleanup",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="Pre-cleanup enabled; attempting to clear orphan processes before tasks start",
            )
        else:
            task_logger.log(
                "orphan_process_pre_cleanup_disabled",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="Pre-cleanup disabled; proceeding despite detected orphans. Results may be skewed.",
            )

    def _normalize_orchestrator_exception(
        self,
        exc: Exception,
        *,
        message: str,
        context: dict[str, object | None] | None = None,
    ) -> HILTestbenchError:
        filtered_context = {
            key: value for key, value in (context or {}).items() if value is not None
        }
        if isinstance(exc, HILTestbenchError):
            if filtered_context:
                exc.add_context(**filtered_context)
            return exc
        try:
            raise ExecutionError(message, context=filtered_context) from exc
        except ExecutionError as wrapped:
            return wrapped

    @staticmethod
    def _safe_runner_shutdown(runner: CommandRunner) -> None:
        with suppress(Exception):
            runner.shutdown()

    def _log_plan_failure(
        self,
        task_logger: TaskLogger | None,
        error: Exception,
        *,
        task_count: int,
    ) -> None:
        if not task_logger:
            return
        task_logger.log(
            "multi_task_plan_failed",
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message="Failed to build multi-task plan",
            error=str(error),
            error_type=type(error).__name__,
            task_count=task_count,
            remediation=(
                "Validate task definitions and dependency declarations; remove cycles or"
                " missing depends_on references before running again."
            ),
        )

    def _record_execution_cancellation(
        self,
        runner: CommandRunner,
        cancelled: bool,
        reason: str | None,
    ) -> None:
        if not cancelled:
            return
        resolved_reason = reason or EXECUTION_CANCELLED
        if self._cancel_event is None:
            self._local_cancelled = True
        if runner.was_cancelled():
            return
        try:
            runner.cancel_all(reason=resolved_reason)
        except Exception as exc:  # noqa: BLE001
            task_logger = runner.get_task_logger()
            if task_logger:
                task_logger.log(
                    "runner_cancel_sync_failed",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    message="Failed to propagate cancellation to runner",
                    error=str(exc),
                    error_type=type(exc).__name__,
                )

    @staticmethod
    def _resolve_cancel_event(runner: CommandRunner | None) -> threading.Event | None:
        if runner is None:
            return None
        getter = getattr(runner, "get_cancel_event", None)
        if not callable(getter):
            return None
        event = getter()
        return event if isinstance(event, threading.Event) else None


@dataclass(slots=True)
class TaskOrchestratorDependencies:
    """Bundled dependencies for :class:`TaskOrchestrator`."""

    display_lifecycle: DisplayLifecycle
    command_preparer: CommandPreparer
    multi_task_planner: MultiTaskPlanner
    runtime_builder: RuntimeContextBuilder
    result_aggregator: ResultAggregator

    @classmethod
    def build(cls, *, console: Console | None = None) -> TaskOrchestratorDependencies:
        display_lifecycle = DisplayLifecycle(console)
        command_preparer = CommandPreparer(display_lifecycle)
        dag_builder = DAGBuilder()
        multi_task_planner = MultiTaskPlanner(dag_builder)
        runtime_builder = RuntimeContextBuilder()
        result_aggregator = ResultAggregator(display_lifecycle)
        return cls(
            display_lifecycle=display_lifecycle,
            command_preparer=command_preparer,
            multi_task_planner=multi_task_planner,
            runtime_builder=runtime_builder,
            result_aggregator=result_aggregator,
        )


__all__ = ["TaskOrchestrator", "TaskOrchestratorDependencies"]
