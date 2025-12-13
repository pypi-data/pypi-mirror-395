"""CommandResult assembly helpers."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from hil_testbench.run.exceptions import ExecutionError
from hil_testbench.run.execution.command_result import (
    CancellationClassification,
    CommandResult,
    CommandStatus,
)
from hil_testbench.run.execution.command_runner.types import ExecutionParams
from hil_testbench.run.execution.command_spec import CommandSpec
from hil_testbench.run.execution.output_streamer import OutputStreamer
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.utils.formatting import format_duration


class CommandResultBuilder:
    """Encapsulates command result bookkeeping and logging."""

    def __init__(
        self,
        task_logger: TaskLogger,
        cancel_event: Any,
        *,
        cancel_state_supplier: Callable[[], tuple[CancellationClassification, str | None]]
        | None = None,
    ) -> None:
        self._task_logger = task_logger
        self._cancel_event = cancel_event
        self._cancel_state_supplier = cancel_state_supplier

    @staticmethod
    def _describe_parser(factory: Callable[[], Any] | None) -> str | None:
        if factory is None:
            return None
        name = getattr(factory, "__qualname__", None) or getattr(factory, "__name__", None)
        module = getattr(factory, "__module__", None)
        if name and module and module not in {"__main__", None}:
            return f"{module}.{name}"
        if name:
            return name
        return repr(factory)

    def _build_spec_metadata(self, spec: CommandSpec | None) -> dict[str, Any]:
        if not spec:
            return {
                "long_running": None,
                "streaming_format": None,
                "parser_id": None,
                "spec_identity": None,
                "exclusive": None,
            }
        identity = None
        try:
            identity = spec.identity()
        except Exception:  # pragma: no cover - defensive snapshot guard
            identity = None
        return {
            "long_running": bool(spec.long_running),
            "streaming_format": spec.streaming_format,
            "parser_id": self._describe_parser(spec.parser_factory),
            "spec_identity": identity,
            "exclusive": bool(spec.exclusive),
        }

    def build_command_result(
        self,
        command_name: str,
        execution: ExecutionParams,
        streamer: OutputStreamer,
        timing: tuple[datetime, datetime],
        exit_code: int,
    ) -> CommandResult:
        start_time, end_time = timing
        duration = (end_time - start_time).total_seconds()
        duration_str = format_duration(duration)
        stdout_text = streamer.get_stdout()
        stderr_text = streamer.get_stderr()
        success = exit_code == 0
        event_count = streamer.get_event_count()
        data_expected = streamer.is_data_expected()

        cancel_state = self._current_cancel_state()

        spec_metadata = self._build_spec_metadata(execution.spec)

        if success:
            self._log_success(
                command_name,
                exit_code,
                duration,
                duration_str,
                event_count,
                data_expected,
                spec=execution.spec,
            )
            status = CommandStatus.COMPLETED
            error = None
            status_message = None
            classification = None
        else:
            (
                status,
                error,
                status_message,
                classification,
            ) = self._handle_nonzero_exit(
                command_name,
                exit_code,
                duration,
                duration_str,
                stdout_text,
                stderr_text,
                event_count,
                data_expected,
                cancel_state,
            )

        success = success or status in (
            CommandStatus.CANCELLED,
            CommandStatus.STOPPED,
        )

        return CommandResult(
            command_name=command_name,
            success=success,
            return_code=exit_code,
            spec=execution.spec,
            stdout=stdout_text,
            stderr=stderr_text,
            error=error,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            event_count=event_count,
            data_expected=data_expected,
            task_name=execution.task_name,
            status=status,
            status_message=status_message,
            cancelled=bool(status == CommandStatus.CANCELLED),
            cancellation_classification=classification,
            **spec_metadata,
        )

    def build_failure_result(
        self,
        command_name: str,
        execution: ExecutionParams,
        streamer: OutputStreamer,
        timing: tuple[datetime, datetime],
        error: Exception,
    ) -> CommandResult:
        start_time, end_time = timing
        duration = (end_time - start_time).total_seconds()
        event_count = streamer.get_event_count()
        data_expected = streamer.is_data_expected()
        if data_expected and event_count > 0:
            self._task_logger.log(
                "command_exception_with_data",
                LogLevel.WARNING,
                scope=LogScope.COMMAND,
                task=command_name,
                message=(f"Command failed with exception but produced {event_count} events"),
                _event_count=event_count,
                _error_type=type(error).__name__,
            )
        spec_metadata = self._build_spec_metadata(execution.spec)

        return CommandResult(
            command_name=command_name,
            success=False,
            return_code=-1,
            spec=execution.spec,
            stdout=streamer.get_stdout(),
            stderr=streamer.get_stderr(),
            error=error,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            event_count=event_count,
            data_expected=data_expected,
            task_name=execution.task_name,
            status=CommandStatus.FAILED,
            **spec_metadata,
        )

    def build_cancelled_result(
        self,
        command_name: str,
        task_name: str | None,
        reason: str | None = None,
        classification: CancellationClassification | None = None,
        *,
        spec: CommandSpec | None = None,
    ) -> CommandResult:
        now = datetime.now()
        stop_due_duration = classification == CancellationClassification.DURATION_LIMIT
        status = CommandStatus.STOPPED if stop_due_duration else CommandStatus.CANCELLED
        if reason:
            message = reason
        elif stop_due_duration:
            message = "Stopped after duration limit"
        else:
            message = "Command cancelled"
        spec_metadata = self._build_spec_metadata(spec)
        resolved_task_name = (
            task_name if task_name is not None else (spec.task_name if spec else None)
        )
        return CommandResult(
            command_name=command_name,
            success=True,
            return_code=-1,
            spec=spec,
            status=status,
            status_message=message,
            start_time=now,
            end_time=now,
            duration=0.0,
            task_name=resolved_task_name,
            cancelled=not stop_due_duration,
            cancellation_classification=classification,
            **spec_metadata,
        )

    def _log_success(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        event_count: int,
        data_expected: bool,
        *,
        spec: CommandSpec | None,
    ) -> None:
        long_running = bool(spec.long_running) if spec else False
        streaming_format = spec.streaming_format if spec else None
        if long_running:
            message = "Long-running command exited cleanly"
            log_level = LogLevel.INFO
        elif data_expected and event_count > 0:
            message = f"Completed successfully | events={event_count}"
            log_level = LogLevel.INFO
        else:
            message = "Completed successfully"
            log_level = LogLevel.DEBUG
        self._task_logger.log(
            "command_succeeded",
            log_level,
            message=message,
            scope=LogScope.COMMAND,
            task=command_name,
            show_fields_with_message=True,
            duration=duration_human,
            _duration_seconds=f"{duration:.2f}",
            _exit_code=exit_code,
            _event_count=event_count if data_expected else None,
            _long_running=long_running or None,
            _streaming_format=streaming_format,
        )
        self._task_logger.log(
            "command_complete",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=command_name,
            _success=True,
            _exit_code=exit_code,
            _duration_seconds=f"{duration:.2f}",
            _event_count=event_count if data_expected else None,
            _long_running=long_running or None,
            _streaming_format=streaming_format,
        )

    def _handle_nonzero_exit(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        stdout_text: str,
        stderr_text: str,
        event_count: int,
        data_expected: bool,
        cancel_state: tuple[CancellationClassification, str | None],
    ) -> tuple[CommandStatus, ExecutionError, str | None, CancellationClassification | None]:
        stderr_preview = self._preview(stderr_text)
        stdout_preview = "" if stderr_preview else self._preview(stdout_text)
        was_cancelled = bool(self._cancel_event and self._cancel_event.is_set())

        status, reason, status_message, classification = self._determine_failure_status(
            was_cancelled, cancel_state, stderr_preview, stdout_preview
        )
        error_obj = self._build_execution_error(
            exit_code, stderr_preview, stdout_preview, command_name, was_cancelled
        )

        self._log_command_failure(
            command_name,
            exit_code,
            duration,
            duration_human,
            reason,
            stderr_preview,
            stdout_preview,
            event_count,
            data_expected,
            was_cancelled,
            status,
        )

        return status, error_obj, status_message, classification

    def _determine_failure_status(
        self,
        was_cancelled: bool,
        cancel_state: tuple[CancellationClassification, str | None],
        stderr_preview: str,
        stdout_preview: str,
    ) -> tuple[CommandStatus, str, str | None, CancellationClassification | None]:
        """Determine status, reason, and message based on cancellation state."""
        classification, provided_reason = cancel_state
        if was_cancelled and classification == CancellationClassification.DURATION_LIMIT:
            message = provided_reason or "Task Duration Reached"
            return (
                CommandStatus.STOPPED,
                message,
                message,
                classification,
            )
        if was_cancelled:
            message = provided_reason or "Command cancelled"
            return (
                CommandStatus.CANCELLED,
                provided_reason or "shutdown",
                message,
                classification or CancellationClassification.USER,
            )
        return (
            CommandStatus.FAILED,
            stderr_preview or stdout_preview or "Unknown error",
            None,
            None,
        )

    def _build_execution_error(
        self,
        exit_code: int,
        stderr_preview: str,
        stdout_preview: str,
        command_name: str,
        was_cancelled: bool,
    ) -> ExecutionError:
        """Build ExecutionError with appropriate context."""
        preview = stderr_preview or stdout_preview
        context = {
            "command": command_name,
            "exit_code": exit_code,
            "cancelled": was_cancelled,
        }
        if stderr_preview:
            context["stderr_preview"] = stderr_preview
        if stdout_preview:
            context["stdout_preview"] = stdout_preview

        return ExecutionError(
            f"Non-zero exit code {exit_code}{f' | {preview}' if preview else ''}",
            context=context,
        )

    def _log_command_failure(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        reason: str,
        stderr_preview: str,
        stdout_preview: str,
        event_count: int,
        data_expected: bool,
        was_cancelled: bool,
        status: CommandStatus,
    ) -> None:
        """Log command failure with appropriate level and formatting."""
        if status is CommandStatus.STOPPED:
            self._log_stopped_command(
                command_name,
                exit_code,
                duration,
                duration_human,
                reason,
                event_count,
                data_expected,
            )
        elif was_cancelled:
            self._log_cancelled_command(
                command_name,
                exit_code,
                duration,
                duration_human,
                reason,
                stderr_preview,
                stdout_preview,
                event_count,
                data_expected,
            )
        else:
            self._log_failed_command(
                command_name,
                exit_code,
                duration,
                duration_human,
                reason,
                stderr_preview,
                stdout_preview,
                event_count,
                data_expected,
            )

        # Always log debug entries
        success_flag = was_cancelled or status is CommandStatus.STOPPED

        self._task_logger.log(
            "command_exit_nonzero",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=command_name,
            _exit_code=exit_code,
            _stderr_preview=stderr_preview,
        )
        self._task_logger.log(
            "command_complete",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=command_name,
            _success=success_flag,
            _exit_code=exit_code,
            _duration_seconds=f"{duration:.2f}",
            _event_count=event_count if data_expected else None,
        )

    def _log_cancelled_command(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        reason: str,
        stderr_preview: str,
        stdout_preview: str,
        event_count: int,
        data_expected: bool,
    ) -> None:
        """Log user-initiated shutdown as DEBUG."""
        summary_line = (
            f"{command_name} terminated during shutdown (exit code {exit_code}, {duration_human})"
        )
        detail_line = f"└─ {reason}"
        formatted_message = f"{summary_line}\n  {detail_line}"
        self._task_logger.log(
            "command_cancelled",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=command_name,
            message=formatted_message,
            _exit_code=exit_code,
            duration=duration_human,
            reason=reason,
            show_fields_with_message=False,
            stderr_preview=stderr_preview,
            stdout_preview=stdout_preview,
            duration_seconds=f"{duration:.2f}",
            cancelled=True,
            event_count=event_count if data_expected else None,
        )

    def _log_stopped_command(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        message: str,
        event_count: int,
        data_expected: bool,
    ) -> None:
        """Log framework-initiated stops (duration guard)."""

        summary_line = f"{command_name} stopped ({duration_human})"
        formatted_message = f"{summary_line}\n  └─ {message}"
        self._task_logger.log(
            "command_stopped",
            LogLevel.INFO,
            scope=LogScope.COMMAND,
            task=command_name,
            message=formatted_message,
            _exit_code=exit_code,
            duration=duration_human,
            reason=message,
            show_fields_with_message=False,
            duration_seconds=f"{duration:.2f}",
            cancelled=False,
            event_count=event_count if data_expected else None,
        )

    def _current_cancel_state(
        self,
    ) -> tuple[CancellationClassification, str | None]:
        if not self._cancel_state_supplier:
            return (CancellationClassification.NONE, None)
        return self._cancel_state_supplier()

    def _log_failed_command(
        self,
        command_name: str,
        exit_code: int,
        duration: float,
        duration_human: str,
        reason: str,
        stderr_preview: str,
        stdout_preview: str,
        event_count: int,
        data_expected: bool,
    ) -> None:
        """Log actual failure as ERROR."""
        summary_line = f"{command_name} FAILED (exit code {exit_code}, {duration_human})"
        detail_line = f"└─ {reason}"
        formatted_message = f"{summary_line}\n  {detail_line}"

        remediation = self.remediation_for_error(reason, host=None, is_ssh=False)

        self._task_logger.log(
            "command_failed_exit_code",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=command_name,
            message=formatted_message,
            _exit_code=exit_code,
            duration=duration_human,
            reason=reason,
            show_fields_with_message=False,
            stderr_preview=stderr_preview,
            stdout_preview=stdout_preview,
            duration_seconds=f"{duration:.2f}",
            cancelled=False,
            event_count=event_count if data_expected else None,
            remediation=remediation,
        )

    def _preview(self, text: str | None) -> str:
        if not text:
            return ""
        lines = text.strip().splitlines()
        if not lines:
            return ""
        return "\n".join(lines[:5])[:1000]

    def remediation_for_error(
        self,
        error_text: str,
        *,
        host: str | None,
        port: int | None = None,
        is_ssh: bool,
    ) -> str:
        """Build human-readable remediation guidance."""

        primary, secondary, general = self._shape_remediation(
            error_text or "",
            host=host,
            port=port,
            is_ssh=is_ssh,
        )
        return " ".join(part for part in (primary, secondary, general) if part)

    def friendly_hint_for_error(
        self,
        command_name: str,
        error_text: str,
        *,
        host: str | None,
    ) -> str | None:
        """Return short, user-friendly hint for common failure patterns."""

        lower_detail = (error_text or "").lower()

        if host and "authentication failed" in lower_detail:
            return f"SSH authentication to {host} was rejected"

        if host and ("unable to connect" in lower_detail or "connection refused" in lower_detail):
            return f"SSH socket to {host} was refused or blocked"

        if command_name.startswith("iperf:client") and "iperf3" in lower_detail:
            return "iperf3 client could not reach the iperf server"

        return None

    @staticmethod
    def _shape_remediation(
        error_text: str,
        *,
        host: str | None,
        port: int | None,
        is_ssh: bool,
    ) -> tuple[str, str | None, str | None]:
        lower_text = error_text.lower()

        if "connection refused" in lower_text or "connect failed" in lower_text:
            if is_ssh:
                target = host or "target host"
                port_hint = f" port {port}" if port else ""
                primary = (
                    f"Verify the SSH server is running on {target}{port_hint} "
                    "(e.g., check 'systemctl status sshd' or docker-compose status)."
                )
            else:
                primary = (
                    "Verify the service is running locally and listening on the expected port."
                )
            secondary = "Check network connectivity and firewall rules."
            general = "Confirm the service is configured to accept connections."
            return primary, secondary, general

        if "permission denied" in lower_text or "auth" in lower_text:
            if is_ssh:
                target = host or "target host"
                primary = f"Verify SSH credentials for {target}."
                secondary = (
                    "Check SSH key permissions (chmod 600) and authorized_keys configuration."
                )
            else:
                primary = "Check file permissions and user access rights for the command."
                secondary = None
            general = "Ensure the user has appropriate access permissions."
            return primary, secondary, general

        if "not found" in lower_text or "no such file" in lower_text:
            primary = "Ensure the command is installed and available in PATH on the target system."
            secondary = "Verify the command name and path are correct."
            return primary, secondary, None

        if "timeout" in lower_text or "timed out" in lower_text:
            primary = "Check network connectivity and latency to the target."
            secondary = (
                "Verify the SSH server is responsive and not overloaded."
                if is_ssh
                else "Verify the target service is responsive and not overloaded."
            )
            general = "Consider increasing timeout values if this is expected."
            return primary, secondary, general

        primary = "Review the error details above for root cause information."
        secondary = "Verify command parameters in the task definition."
        general = "Retry the operation after addressing potential issues."
        return primary, secondary, general


__all__ = ["CommandResultBuilder"]
