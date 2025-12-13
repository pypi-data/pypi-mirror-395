"""Aggregates command results, performs validation, and finalizes outcomes."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any, Protocol, cast, runtime_checkable

from hil_testbench.run.display.display_lifecycle import DisplayLifecycle
from hil_testbench.run.exceptions import ValidationError
from hil_testbench.run.execution.command_result import CommandResult, CommandStatus
from hil_testbench.run.execution.command_runner import CommandRunner
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.results.task_outcome import (
    ParameterDataSummary,
    TaskOutcome,
)
from hil_testbench.task.specs import TaskDefinition


class ValidatorProtocol(Protocol):
    """Structural interface for command result validators."""

    def validate(
        self,
        exit_code: int,
        stdout: str,
        stderr: str,
        duration: float,
        parameter_count: int,
    ) -> tuple[bool, str | None]:
        """Validate command result and return (success, error_message)."""
        ...


class CommandDisplayBackendProtocol(Protocol):
    """Structural interface for display backends."""

    def update_command_status(
        self,
        task_name: str,
        command_name: str,
        status: str | None = None,
        *,
        lifecycle_status: str | None = None,
    ) -> None:
        """Update display status for a command."""
        ...

    def report_command_error(self, task_name: str, command_name: str, error: str) -> None:
        """Report a command failure to the display."""
        ...

    def add_event(self, message: str, level: str) -> None:
        """Record an event entry."""
        ...


@runtime_checkable
class SupportsErrorCountingBackend(Protocol):
    """Display backend that can report pipeline error counts."""

    def get_error_count(self, task_name: str) -> int: ...


@runtime_checkable
class SupportsTaskEntry(Protocol):
    """Display task entry that tracks aggregate error counts."""

    error_count: int


@runtime_checkable
class SupportsTaskRegistry(Protocol):
    """Display backend exposing an internal task registry."""

    _tasks: Mapping[str, SupportsTaskEntry]


@dataclass(slots=True)
class _ValidationContext:
    """Aggregates mutable validation state for a validation pass."""

    command_validators: dict[str, tuple[ValidatorProtocol, CommandDisplayBackendProtocol | None]]
    failed_commands: set[str]
    display_backend: CommandDisplayBackendProtocol | None
    completed_commands: set[str] | None
    failed_commands_state: set[str] | None
    task_logger: TaskLogger

    def mark_failed(self, command_name: str) -> None:
        self.failed_commands.add(command_name)
        if self.failed_commands_state is not None:
            self.failed_commands_state.add(command_name)


@dataclass(slots=True)
class _CommandAggregates:
    total: int
    failed: int
    cancelled: int
    success: bool


@dataclass(slots=True)
class _TimingWindow:
    start: datetime
    end: datetime
    duration_seconds: float


class ResultAggregator:
    """Group namespaced command results back into TaskOutcome objects."""

    def __init__(self, display_lifecycle: DisplayLifecycle):
        self._display_lifecycle = display_lifecycle

    def aggregate(
        self,
        all_results: list[CommandResult],
        original_task_defs: list[TaskDefinition],
        runner: CommandRunner,
        task_logger: TaskLogger,
    ) -> dict[str, TaskOutcome]:
        grouped_results = self._group_results_by_task(all_results, original_task_defs, task_logger)
        task_outcomes = {
            task_def.name: self._build_task_outcome(
                task_def.name,
                grouped_results.get(task_def.name, []),
                runner,
                task_logger,
            )
            for task_def in original_task_defs
        }
        self._finalize_task_outcomes(task_outcomes, task_logger)
        return task_outcomes

    def validate_results(
        self,
        results: list[CommandResult],
        *,
        command_validators: dict[
            str, tuple[ValidatorProtocol, CommandDisplayBackendProtocol | None]
        ],
        failed_commands: set[str],
        runner: CommandRunner,
        display_backend: CommandDisplayBackendProtocol | None = None,
        completed_commands: set[str] | None = None,
        failed_commands_state: set[str] | None = None,
    ) -> None:
        """Validate command results and update bookkeeping state."""

        context = _ValidationContext(
            command_validators=command_validators,
            failed_commands=failed_commands,
            display_backend=display_backend,
            completed_commands=completed_commands,
            failed_commands_state=failed_commands_state,
            task_logger=runner.get_task_logger(),
        )

        for result in results:
            self._process_validation_result(result, context)

        self._update_display_backend(results, display_backend, context)

    def _group_results_by_task(
        self,
        all_results: list[CommandResult],
        original_task_defs: list[TaskDefinition],
        task_logger: TaskLogger,
    ) -> dict[str, list[CommandResult]]:
        task_results: dict[str, list[CommandResult]] = {
            task_def.name: [] for task_def in original_task_defs
        }
        for result in all_results:
            task_name, command_label = self._resolve_task_and_command(result)
            if task_name and task_name in task_results:
                denamespaced_result = replace(result)
                denamespaced_result.command_name = command_label
                denamespaced_result.task_name = task_name
                task_results[task_name].append(denamespaced_result)
                continue
            if task_name is None:
                task_logger.log(
                    "unnamespaced_result_warning",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    command_name=result.command_name,
                    message="Command result missing namespace",
                )
        return task_results

    def _resolve_task_and_command(self, result: CommandResult) -> tuple[str | None, str]:
        """Determine target task name and denamespaced command label."""

        spec = result.spec
        task_name = spec.task_name if spec else result.task_name

        command_source = None
        if spec and spec.command_name:
            command_source = spec.command_name
        if (not command_source or ":" not in command_source) and ":" in result.command_name:
            command_source = result.command_name
        if command_source is None:
            command_source = result.command_name

        command_label = command_source
        if ":" in command_source:
            prefix, suffix = command_source.split(":", 1)
            command_label = suffix
            if not task_name:
                task_name = prefix

        if not task_name:
            task_name = result.task_name

        return task_name, command_label

    def _build_task_outcome(
        self,
        task_name: str,
        results: list[CommandResult],
        runner: CommandRunner,
        task_logger: TaskLogger,
    ) -> TaskOutcome:
        aggregates = self._summarize_command_results(results)
        timing = self._derive_timing_window(results)

        backend = self._display_lifecycle.get_display_backend(task_logger)
        status_backend = cast(CommandDisplayBackendProtocol | None, backend)
        pipeline_errors = self._fetch_pipeline_errors(task_name, status_backend)

        overall_success = aggregates.success and (pipeline_errors == 0)
        task_cancelled = aggregates.cancelled > 0
        cancellation_classification = runner.get_cancel_classification()

        parameter_summary = self._capture_parameter_data_summary(status_backend)

        return TaskOutcome(
            task_name=task_name,
            command_results=results,
            success=overall_success,
            total_commands=aggregates.total,
            failed_commands=aggregates.failed,
            cancelled=task_cancelled,
            cancelled_commands=aggregates.cancelled,
            start_time=timing.start,
            end_time=timing.end,
            duration_seconds=timing.duration_seconds,
            correlation_id=runner.get_correlation_id(),
            log_directory=runner.get_execution_dir(),
            parameter_data_summary=parameter_summary,
            cancellation_classification=cancellation_classification,
        )

    def _summarize_command_results(self, results: list[CommandResult]) -> _CommandAggregates:
        total = len(results)
        failed = sum(not r.success for r in results)
        cancelled = sum(
            bool(
                getattr(r, "cancelled", False)
                or getattr(r, "status", None) == CommandStatus.CANCELLED
            )
            for r in results
        )
        return _CommandAggregates(
            total=total,
            failed=failed,
            cancelled=cancelled,
            success=failed == 0,
        )

    def _derive_timing_window(self, results: list[CommandResult]) -> _TimingWindow:
        command_starts = [
            r.start_time.replace(tzinfo=UTC)
            if (r.start_time and r.start_time.tzinfo is None)
            else r.start_time
            for r in results
            if r.start_time
        ]
        command_ends = [
            r.end_time.replace(tzinfo=UTC)
            if (r.end_time and r.end_time.tzinfo is None)
            else r.end_time
            for r in results
            if r.end_time
        ]

        now = datetime.now(UTC)
        start_time = min(command_starts) if command_starts else now
        end_time = max(command_ends, default=start_time)
        duration = max((end_time - start_time).total_seconds(), 0.0)
        return _TimingWindow(start=start_time, end=end_time, duration_seconds=duration)

    @staticmethod
    def _fetch_pipeline_errors(
        task_name: str, backend: CommandDisplayBackendProtocol | None
    ) -> int:
        if backend is None:
            return 0
        if isinstance(backend, SupportsErrorCountingBackend):
            try:
                return int(backend.get_error_count(task_name))
            except Exception:  # noqa: BLE001 - best-effort
                return 0
        if isinstance(backend, SupportsTaskRegistry):
            task_entry = backend._tasks.get(task_name)
            if task_entry is not None:
                return int(task_entry.error_count)
        return 0

    def _finalize_task_outcomes(
        self,
        task_outcomes: dict[str, TaskOutcome],
        task_logger: TaskLogger,
    ) -> None:
        backend = self._display_lifecycle.get_display_backend(task_logger)
        for task_name, outcome in task_outcomes.items():
            self._log_task_completion(task_logger, task_name, outcome)
            self._display_lifecycle.update_final_task_status(
                task_logger,
                backend,
                task_name,
                outcome,
            )

    @staticmethod
    def _log_task_completion(
        task_logger: TaskLogger,
        task_name: str,
        outcome: TaskOutcome,
    ) -> None:
        log_level = LogLevel.INFO if outcome.success else LogLevel.ERROR
        task_logger.log(
            "task_complete",
            log_level,
            scope=LogScope.TASK,
            task=task_name,
            success=outcome.success,
            total_commands=outcome.total_commands,
            failed_commands=outcome.failed_commands,
        )
        task_logger.log_task_summary(outcome)

    def _process_validation_result(
        self,
        result: CommandResult,
        context: _ValidationContext,
    ) -> None:
        if context.completed_commands is not None and getattr(result, "success", False):
            context.completed_commands.add(result.command_name)

        if self._handle_data_expected_failure(result, context):
            return

        validator_entry = context.command_validators.get(result.command_name)
        if validator_entry is None:
            self._handle_missing_validator(result, context)
            return

        validator, backend = validator_entry
        success, error_msg = self._run_command_validator(result, validator, context)
        if backend is None:
            backend = context.display_backend
        if success:
            return

        self._handle_validator_failure(result, backend, error_msg, context)

    def _handle_data_expected_failure(
        self,
        result: CommandResult,
        context: _ValidationContext,
    ) -> bool:
        if result.cancelled or result.status is CommandStatus.CANCELLED:
            return False

        if not self._data_expected_failure(result, context.command_validators):
            return False

        result.success = False
        context.mark_failed(result.command_name)
        error_msg = self._build_no_data_error(result)
        self._set_validation_error(result, error_msg)
        context.task_logger.log(
            "auto_failed_no_data",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=result.task_name,
            command=result.command_name,
            reason=error_msg,
            remediation=(
                "Ensure the parser produces parameter data or clear the data_expected"
                " flag if empty output is acceptable."
            ),
        )
        return True

    def _handle_missing_validator(
        self,
        result: CommandResult,
        context: _ValidationContext,
    ) -> None:
        if result.success:
            return

        result.success = False
        context.mark_failed(result.command_name)
        error_msg = self._build_execution_error(result)
        self._report_backend_error(
            result,
            context,
            error_msg,
        )
        failure_reason = error_msg or "Command failed without an assigned validator"
        context.task_logger.log(
            "missing_command_validator",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=result.task_name,
            command=result.command_name,
            reason=failure_reason,
            remediation=(
                "Attach a validator for this command or disable data_expected when"
                " validation is not required."
            ),
        )

    def _run_command_validator(
        self,
        result: CommandResult,
        validator: ValidatorProtocol,
        context: _ValidationContext,
    ) -> tuple[bool, str | None]:
        context.task_logger.log(
            "running_validator",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=result.task_name,
            message=f"Running validator for command '{result.command_name}'",
            command=result.command_name,
            validator_type=type(validator).__name__,
        )

        try:
            success, error_msg = validator.validate(
                exit_code=result.return_code,
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                duration=result.duration or 0.0,
                parameter_count=result.event_count or 0,
            )

            context.task_logger.log(
                "validator_result",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=result.task_name,
                command=result.command_name,
                success=success,
                error_msg=error_msg,
            )
            return success, error_msg
        except Exception as exc:  # noqa: BLE001
            context.task_logger.log(
                "validator_exception",
                LogLevel.ERROR,
                scope=LogScope.COMMAND,
                task=result.task_name,
                command=result.command_name,
                error=str(exc),
                validator_type=type(validator).__name__,
                remediation=(
                    "Update the validator to handle this output without raising or"
                    " adjust validation configuration before rerunning."
                ),
            )
            self._set_validation_error(result, str(exc), cause=exc)
            return False, str(exc)

    def _handle_validator_failure(
        self,
        result: CommandResult,
        backend: CommandDisplayBackendProtocol | None,
        error_msg: str | None,
        context: _ValidationContext,
    ) -> None:
        result.success = False
        context.mark_failed(result.command_name)
        failure_reason = error_msg or "Validation failed"
        if isinstance(result.error, ValidationError):
            if failure_reason:
                result.error.add_context(reason=failure_reason)
        else:
            self._set_validation_error(result, failure_reason)
        self._report_command_failure(
            backend,
            result,
            failure_reason,
        )

        context.task_logger.log(
            "command_validation_failed",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=result.task_name,
            command=result.command_name,
            reason=failure_reason,
            remediation=(
                "Inspect validator output and command results, then adjust command"
                " parameters or validator rules before retrying."
            ),
        )

    def _update_display_backend(
        self,
        results: list[CommandResult],
        backend: CommandDisplayBackendProtocol | None,
        context: _ValidationContext,
    ) -> None:
        if not backend:
            return

        for result in results:
            if result.task_name and hasattr(backend, "update_command_status"):
                status = self._display_lifecycle.result_status(result)
                try:
                    backend.update_command_status(
                        result.task_name,
                        result.command_name,
                        lifecycle_status=status,
                    )
                except Exception as exc:  # noqa: BLE001
                    context.task_logger.log(
                        "display_command_status_failed",
                        LogLevel.DEBUG,
                        scope=LogScope.FRAMEWORK,
                        task=result.task_name,
                        command=result.command_name,
                        status=status,
                        backend_type=type(backend).__name__,
                        error=str(exc),
                    )
                    context.mark_failed(result.command_name)
                    self._set_validation_error(
                        result,
                        f"Display backend failed updating status '{status}'",
                        cause=exc,
                    )

    def _set_validation_error(
        self,
        result: CommandResult,
        reason: str,
        *,
        cause: Exception | None = None,
    ) -> ValidationError:
        context = {
            "task": result.task_name,
            "command": result.command_name,
            "return_code": result.return_code,
        }
        filtered_context = {k: v for k, v in context.items() if v is not None}
        error = ValidationError(reason, context=filtered_context)
        if cause is not None:
            error.add_context(
                cause_type=type(cause).__name__,
                cause_message=str(cause),
            )
        result.error = error
        result.success = False
        result.status = CommandStatus.FAILED
        return error

    def _capture_parameter_data_summary(
        self,
        backend: CommandDisplayBackendProtocol | None,
    ) -> ParameterDataSummary | None:
        if not backend:
            return None
        summary_getter = getattr(backend, "get_parameter_data_summary", None)
        if not callable(summary_getter):
            return None
        try:
            summary_payload = summary_getter()
        except Exception:  # noqa: BLE001 - display summary is best-effort
            return None

        if isinstance(summary_payload, ParameterDataSummary):
            return summary_payload

        summary_mapping = cast(Mapping[str, Any], summary_payload)
        with_data = list(summary_mapping.get("with_data", []))
        without_data = list(summary_mapping.get("without_data", []))
        return ParameterDataSummary(with_data=with_data, without_data=without_data)

    @staticmethod
    def _data_expected_failure(
        result: CommandResult,
        command_validators: dict[
            str, tuple[ValidatorProtocol, CommandDisplayBackendProtocol | None]
        ],
    ) -> bool:
        return (
            getattr(result, "data_expected", False)
            and getattr(result, "event_count", None) == 0
            and result.success
            and result.command_name not in command_validators
        )

    @staticmethod
    def _build_no_data_error(res: CommandResult) -> str:
        stdout_hint = ResultAggregator._stdout_error_hint(getattr(res, "stdout", None))
        if stdout_hint:
            return f"No data output: {stdout_hint}"

        stderr_hint = ResultAggregator._stderr_error_hint(getattr(res, "stderr", None))
        if stderr_hint:
            return f"No data output: {stderr_hint}"

        return "No data output: parser produced zero events"

    @staticmethod
    def _stdout_error_hint(stdout: str | None) -> str | None:
        if not stdout:
            return None

        cleaned = stdout.strip()
        if not cleaned:
            return None

        json_hint = ResultAggregator._json_error_hint(cleaned)
        if json_hint:
            return json_hint

        return ResultAggregator._plaintext_error_hint(cleaned)

    @staticmethod
    def _json_error_hint(stdout: str) -> str | None:
        try:
            data = json.loads(stdout)
        except ValueError:
            return None

        if isinstance(data, dict) and "error" in data:
            return str(data["error"])[:200]
        return None

    @staticmethod
    def _plaintext_error_hint(stdout: str) -> str | None:
        for line in stdout.split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("{"):
                continue
            if "error" in stripped.lower():
                return stripped[:200]
        return None

    @staticmethod
    def _stderr_error_hint(stderr: str | None) -> str | None:
        if not stderr:
            return None
        for line in stderr.strip().split("\n"):
            stripped = line.strip()
            if stripped:
                return stripped[:200]
        return None

    @staticmethod
    def _build_execution_error(res: CommandResult) -> str | None:
        if getattr(res, "error", None):
            return f"{type(res.error).__name__}: {res.error}"
        if getattr(res, "stderr", None):
            return res.stderr.strip()[:200]
        if getattr(res, "return_code", 0) != 0:
            return f"Command exited with code {res.return_code}"
        return None

    def _report_backend_error(
        self,
        result: CommandResult,
        context: _ValidationContext,
        error_msg: str | None,
    ) -> None:
        backend = context.display_backend
        task_name = result.task_name
        if backend and error_msg and task_name and hasattr(backend, "report_command_error"):
            try:
                backend.report_command_error(task_name, result.command_name, error_msg)
            except Exception as exc:  # noqa: BLE001
                context.task_logger.log(
                    "display_report_error_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task=task_name,
                    command=result.command_name,
                    error=str(exc),
                )
                context.mark_failed(result.command_name)
                self._set_validation_error(
                    result,
                    "Display backend failed to report validation error",
                    cause=exc,
                )
        if backend and task_name and hasattr(backend, "update_command_status"):
            try:
                backend.update_command_status(
                    task_name,
                    result.command_name,
                    lifecycle_status="failed",
                )
            except Exception as exc:  # noqa: BLE001
                context.task_logger.log(
                    "display_update_command_status_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task=task_name,
                    command=result.command_name,
                    status="failed",
                    error=str(exc),
                )
                context.mark_failed(result.command_name)
                self._set_validation_error(
                    result,
                    "Display backend failed to update failed status",
                    cause=exc,
                )

    def _report_command_failure(
        self,
        backend: CommandDisplayBackendProtocol | None,
        result: CommandResult,
        failure_reason: str,
    ) -> None:
        task_name = result.task_name
        if not (backend and task_name):
            return

        self._safe_backend_call(
            backend,
            "update_command_status",
            result,
            "Display backend failed to update failed status",
            task_name,
            result.command_name,
            lifecycle_status="failed",
        )

        if failure_reason:
            self._safe_backend_call(
                backend,
                "report_command_error",
                result,
                "Display backend failed to report validation failure",
                task_name,
                result.command_name,
                failure_reason,
            )

        self._safe_backend_call(
            backend,
            "add_event",
            result,
            "Display backend failed to emit validation event",
            f"❌ {result.command_name}: {failure_reason}",
            "ERROR",
        )

    def _safe_backend_call(
        self,
        backend: CommandDisplayBackendProtocol,
        method_name: str,
        result: CommandResult,
        error_message: str,
        *args: object,
        **kwargs: object,
    ) -> None:
        method = getattr(backend, method_name, None)
        if not callable(method):
            return
        try:
            method(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            self._set_validation_error(result, error_message, cause=exc)
