"""Command runner responsible for process execution only."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.data_processing.events import (
    CommandOutputCallback,
    CommandOutputCallbackFactory,
)
from hil_testbench.data_structs.hosts import HostDefinition
from hil_testbench.run.exceptions import ConfigurationError, ExecutionError, HILTestbenchError
from hil_testbench.run.execution.command_result import (
    CancellationClassification,
    CommandResult,
)
from hil_testbench.run.execution.command_spec import CommandSpec, PreparedEntry
from hil_testbench.run.execution.execution_context import ExecutionContext
from hil_testbench.run.execution.shell_wrapper import resolve_shell_wrapper_mode
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.session.forced_cleanup import (
    ForcedCleanupExecutor,
    ForcedCleanupPlanEntry,
)
from hil_testbench.run.session.process_cleanup import ProcessCleanup
from hil_testbench.run.session.process_state_store import ProcessStateStore

from .cleanup_coordinator import CleanupCoordinator
from .execution_lifecycle import ExecutionLifecycle
from .result_builder import CommandResultBuilder
from .ssh_client_manager import SSHClientManager
from .transport_adapters import TransportAdapters
from .types import CommandRunnerSettings, ExecutionParams

if TYPE_CHECKING:  # pragma: no cover - import cycle guard
    from hil_testbench.run.execution.execution_session import ExecutionSession


class CommandRunner:
    """
    Executes commands with support for:
    - Concurrent or sequential execution of multiple commands
    - Mixed local and remote (SSH) command execution
    - Live output streaming with callbacks
    - Command cancellation
    - Graceful shutdown

    Usage:
        runner = CommandRunner(settings=CommandRunnerSettings(max_workers=5))

        # Define commands
        def build(c):
            c.run("npm install")
            c.run("npm run build")

        def deploy(c):
            c.run("rsync -av dist/ server:/var/www/")

        # Run tasks (single or multiple)
        results = runner.run([
            (build, None),
            (deploy, "user@server.com"),
        ])

        # Run with output callback
        from hil_testbench.data_processing.events import CommandOutputEvent

        def log_output(event: CommandOutputEvent):
            pass

        results = runner.run([
            (deploy, "user@server.com", log_output),
        ])
    """

    def __init__(
        self,
        settings: CommandRunnerSettings,
        config: TaskConfig,
        process_tracker: Any,
        *,
        task_logger: TaskLogger | None = None,
        state_store: ProcessStateStore | None = None,
    ):
        if settings is None:
            settings = CommandRunnerSettings()
        self._settings = settings
        self.max_workers = settings.max_workers
        self.verbose = settings.verbose
        self.log_dir = settings.log_dir
        self.max_bytes_main = settings.max_bytes_main
        self.max_bytes_task = settings.max_bytes_task
        self.max_log_file_count_main = settings.max_log_file_count_main
        self.max_log_file_count_task = settings.max_log_file_count_task
        self._cancel_event = threading.Event()
        self._external_interrupt = False
        self._force_shutdown_triggered = False
        self._cancel_classification = CancellationClassification.NONE
        self._cancel_reason: str | None = None
        self._cancel_listeners: set[Callable[[], None]] = set()
        self._cancel_listener_lock = threading.Lock()
        self._session: ExecutionSession | None = None
        self._config = config
        self._process_tracker = process_tracker
        run_config = config.run_config

        if task_logger is None:
            self._task_logger = TaskLogger(
                run_config=run_config,
                log_dir=settings.log_dir,
            )
        else:
            self._task_logger = task_logger

        self._state_store = state_store or ProcessStateStore(logger=self._task_logger)
        self._ssh_manager = SSHClientManager(
            self._task_logger,
            self.verbose,
            cancel_event=self._cancel_event,
            max_retries=settings.ssh_max_retries,
            retry_delay=settings.ssh_retry_delay,
        )
        self._transport = TransportAdapters(
            logger=self._task_logger,
            cancel_event=self._cancel_event,
            config=self._config,
            process_tracker=self._process_tracker,
            ssh_manager=self._ssh_manager,
            process_cleanup=None,  # set after creation
        )
        self._result_builder = CommandResultBuilder(
            self._task_logger,
            self._cancel_event,
            cancel_state_supplier=self._get_cancel_state,
        )
        self._cleanup = CleanupCoordinator(
            logger=self._task_logger,
            ssh_manager=self._ssh_manager,
            normalize_shutdown_error=self._normalize_shutdown_exception,
        )
        self._lifecycle = ExecutionLifecycle(
            logger=self._task_logger,
            cancel_event=self._cancel_event,
            shutdown_callback=self.shutdown,
            force_shutdown_callback=self.force_shutdown,
            running_tasks_supplier=self._active_command_count,
            interrupt_callback=self._register_external_interrupt,
            signal_grace_seconds=settings.signal_force_grace_seconds,
        )
        self._lifecycle.start(settings)
        self._task_logger.log(
            "command_runner_initialized",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            message="CommandRunner initialized",
            max_workers=self.max_workers,
        )
        self._process_cleanup = ProcessCleanup(
            logger=self._task_logger,
            state_store=self._state_store,
            cleanup_required=bool(run_config.cleanup_required),
            cleanup_window_seconds=getattr(run_config, "cleanup_window_seconds", None),
        )
        self._transport.set_process_cleanup(self._process_cleanup)
        self._forced_cleanup_executor = ForcedCleanupExecutor(
            logger=self._task_logger,
            ssh_manager=self._ssh_manager,
            timeout_seconds=settings.forced_cleanup_timeout,
        )
        self._forced_cleanup_plan: dict[str, ForcedCleanupPlanEntry] = {}
        self._force_cleanup_requested = bool(getattr(run_config, "force_cleanup", False))
        self._pre_cleanup_requested = bool(getattr(run_config, "pre_cleanup", False))
        self._forced_cleanup_timeout = float(getattr(settings, "forced_cleanup_timeout", 5.0))
        if config and not config.run_config.no_cleanup:
            self._process_cleanup.sweep_local()

    # Public accessors for correlation id and execution directory
    def get_correlation_id(self) -> str:
        """Return the correlation ID for the current execution."""
        return self._task_logger.get_correlation_id()

    def get_execution_dir(self) -> str:
        """Return the per-execution log directory path."""
        return self._task_logger.get_execution_dir()

    def attach_session(self, session: ExecutionSession) -> None:
        """Provide the live ExecutionSession so runtime state flows through it."""
        self._session = session
        self._cleanup.attach_session(session)

    def configure_forced_cleanup(
        self,
        plan: dict[str, ForcedCleanupPlanEntry] | None,
        *,
        pre_cleanup: bool | None = None,
        force_cleanup: bool | None = None,
    ) -> None:
        """Attach forced-cleanup plan and user-driven flags."""

        if plan:
            self._forced_cleanup_plan = plan
        if pre_cleanup is not None:
            self._pre_cleanup_requested = bool(pre_cleanup)
        if force_cleanup is not None:
            self._force_cleanup_requested = bool(force_cleanup)
        if self._pre_cleanup_requested:
            self._run_forced_cleanup(reason="pre_cleanup")

    def _require_session(self) -> ExecutionSession:
        if self._session is None:
            raise ExecutionError(
                "ExecutionSession has not been attached to CommandRunner",
                context={"runner_initialized": hasattr(self, "_lifecycle")},
            )
        return self._session

    def _active_command_count(self) -> int:
        session = self._session
        return session.active_command_count() if session else 0

    def _session_safe_call(self, method_name: str, *args, **kwargs) -> None:
        session = self._session
        if not session:
            return
        method = getattr(session, method_name, None)
        if callable(method):
            method(*args, **kwargs)

    @property
    def state(self) -> ExecutionSession:
        """Expose ExecutionSession for legacy collaborators (tests/integration)."""
        return self._require_session()

    def was_cancelled(self) -> bool:
        """Return True if a cancellation request has been issued."""
        return self._cancel_event.is_set()

    def consume_interrupt_flag(self) -> bool:
        """Return True if an external interrupt occurred and reset the flag."""
        interrupted = self._external_interrupt
        self._external_interrupt = False
        return interrupted

    def _register_external_interrupt(self) -> None:
        """Mark that an external interrupt (SIGINT/SIGTERM) was received."""
        self._external_interrupt = True

    def shutdown(self):
        """Gracefully shut down all running tasks, resources, and logging."""
        # Prevent duplicate shutdown work
        if getattr(self, "_shutdown_started", False):
            return
        self._shutdown_started = True
        cleanup_duration: float | None = None
        local_stats = None
        remote_stats = None
        try:
            start = time.monotonic()
            self._cleanup.terminate_running_processes(verbose=self.verbose)
            cleanup_duration = time.monotonic() - start
            try:
                local_stats = self._process_cleanup.sweep_local()
                remote_stats = self._process_cleanup.sweep_clients(self._ssh_manager.iter_clients())
            except Exception as exc:  # noqa: BLE001 - shutdown path
                self._task_logger.log(
                    "runner_cleanup_failed",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    message="Cleanup during shutdown encountered errors",
                    error=str(exc),
                )
            self._maybe_run_forced_cleanup(cleanup_duration, local_stats, remote_stats)
            self.close_transports()
            issues = self._cleanup.summarize_shutdown()
            self._cleanup.log_process_exit_diagnostics_safe()
            session = self._session
            self._task_logger.log(
                "runner_shutdown_completed",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                message="Shutdown complete",
                total_tasks_executed=getattr(session, "tasks_started", 0) if session else 0,
                _had_issues=issues,
            )
            self._task_logger.close_all()
        finally:
            self._lifecycle.stop()

    def force_shutdown(self) -> None:
        """Escalate shutdown by force-killing active processes."""
        if self._force_shutdown_triggered:
            return
        self._force_shutdown_triggered = True
        self._task_logger.log(
            "runner_force_shutdown",
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message="Force shutdown requested - terminating remaining processes",
        )
        self._cleanup.force_terminate_processes(verbose=self.verbose)
        self.close_transports()

    def _run_forced_cleanup(self, *, reason: str) -> None:
        if not self._forced_cleanup_plan:
            return
        self._task_logger.log(
            "forced_cleanup_start",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message="Starting forced cleanup",
            reason=reason,
        )
        self._forced_cleanup_executor.execute(self._forced_cleanup_plan, reason=reason)

    def _maybe_run_forced_cleanup(
        self,
        cleanup_duration: float | None,
        local_stats: Any | None,
        remote_stats: Any | None,
    ) -> None:
        if not self._forced_cleanup_plan:
            return

        unresolved_local = getattr(local_stats, "unresolved", 0) if local_stats else 0
        unresolved_remote = getattr(remote_stats, "unresolved", 0) if remote_stats else 0
        unresolved = (unresolved_local + unresolved_remote) > 0
        timeout_triggered = (
            cleanup_duration is not None and cleanup_duration > self._forced_cleanup_timeout
        )
        no_pids_tracked = not bool(self._state_store.list_entries())

        if self._force_cleanup_requested:
            reason = "user_requested"
        elif unresolved:
            reason = "pid_cleanup_failed"
        elif timeout_triggered:
            reason = "shutdown_timeout"
        elif no_pids_tracked:
            reason = "pid_tracking_unavailable"
        else:
            return

        self._run_forced_cleanup(reason=reason)

    @dataclass(slots=True)
    class TaskCallbacks:
        output_callback: CommandOutputCallback | CommandOutputCallbackFactory | None = None
        error_callback: Callable[[Exception], None] | None = None
        completion_callback: Callable[[int], None] | None = None

    def _execute_task(
        self,
        command_func: Callable,
        command_name: str,
        execution: ExecutionParams,
        callbacks: CommandRunner.TaskCallbacks | None = None,
        **task_kwargs,
    ) -> CommandResult:
        """Execute a single task function."""

        callbacks = callbacks or self.TaskCallbacks()
        start_time = datetime.now()
        self._log_command_start(command_name, execution)
        actual_callback = self._transport.resolve_output_callback(
            command_name, callbacks.output_callback
        )
        streamer = self._transport.create_streamer(command_name, actual_callback, execution)
        self._require_session()
        self._session_safe_call("register_streamer", command_name, streamer)

        context = None
        try:
            context = self._transport.create_execution_context(command_name, execution, streamer)
            self._session_safe_call("register_context", command_name, context)
            self._session_safe_call("register_command_spec", command_name, execution.spec)

            exit_code = self._invoke_command_func(command_func, context, task_kwargs)
            end_time = datetime.now()
            result = self._result_builder.build_command_result(
                command_name,
                execution,
                streamer,
                (start_time, end_time),
                exit_code,
            )
            self._safe_invoke_callback(
                callbacks.completion_callback, exit_code, command_name, "completion"
            )
            return result

        except KeyboardInterrupt:
            self._log_cancellation(command_name, start_time)
            raise

        except Exception as exc:  # pylint: disable=broad-except
            end_time = datetime.now()
            normalized = self._normalize_command_exception(exc, command_name, execution)
            self._log_command_failure(command_name, execution, normalized)
            self._safe_invoke_callback(callbacks.error_callback, normalized, command_name, "error")
            return self._result_builder.build_failure_result(
                command_name,
                execution,
                streamer,
                (start_time, end_time),
                normalized,
            )
        finally:
            self._session_safe_call("remove_streamer", command_name)
            self._session_safe_call("remove_context", command_name)
            self._session_safe_call("remove_command_spec", command_name)
            self._task_logger.close_task_logger(command_name)
            if context is not None:
                self._transport.notify_connection_closed(execution.task_name, command_name)

    def _log_command_start(self, command_name: str, execution: ExecutionParams) -> None:
        execution_type = "remote" if execution.host else "local"
        self._task_logger.log(
            "command_started",
            LogLevel.DEBUG,
            message="Starting command",
            scope=LogScope.COMMAND,
            task=command_name,
            show_fields_with_message=True,
            execution_type=execution_type,
            _host=execution.host,
        )

    @staticmethod
    def _resolve_command_name(command_func: Callable[..., Any]) -> str:
        override = getattr(command_func, "_command_name", None)
        if override:
            return override
        if isinstance(command_func, partial):
            return command_func.func.__name__
        return getattr(command_func, "__name__", "command")

    def _build_execution_params(
        self,
        host_value: Any | None,
        *,
        password: str | None,
        log_output: bool | None,
        sample_lines: int,
        use_pty: bool,
        task_name: str | None,
        shell_wrapper_mode: str | None,
        spec: CommandSpec | None,
    ) -> ExecutionParams:
        resolved_host: str | None = None
        port = 22
        remote_os: str = "unix"
        resolved_password = password
        allow_agent = False
        look_for_keys = True

        if isinstance(host_value, HostDefinition):
            if not host_value.local:
                resolved_host = host_value.as_string()
                port = host_value.port
                remote_os = host_value.remote_os
                if not resolved_password and host_value.password:
                    resolved_password = host_value.password
                allow_agent = host_value.allow_agent
                look_for_keys = host_value.look_for_keys
            else:
                resolved_host = None
        elif host_value is None:
            resolved_host = None
        else:
            resolved_host = str(host_value)

        is_remote = resolved_host is not None
        resolved_wrapper_mode = resolve_shell_wrapper_mode(
            shell_wrapper_mode,
            getattr(self._settings, "shell_wrapper_mode", "auto"),
            is_remote=is_remote,
        )
        if spec is None:
            raise ExecutionError(
                "Command specification missing for execution",
                context={"task": task_name or "unknown"},
            )

        spec_overrides: dict[str, Any] = {
            "host": resolved_host,
            "use_pty": use_pty,
            "shell_wrapper_mode": resolved_wrapper_mode,
        }
        spec_with_overrides = spec.with_updates(**spec_overrides)

        return ExecutionParams(
            spec=spec_with_overrides,
            password=resolved_password,
            allow_agent=allow_agent,
            look_for_keys=look_for_keys,
            log_output=log_output,
            sample_lines=sample_lines,
            task_name=task_name,
            remote_os=remote_os,
            host=resolved_host,
            port=port,
            use_pty=use_pty,
            shell_wrapper_mode=resolved_wrapper_mode,
        )

    def _invoke_command_func(
        self,
        command_func: Callable,
        context: ExecutionContext,
        task_kwargs: dict[str, Any],
    ) -> int:
        result = command_func(context, **task_kwargs)
        if not isinstance(result, int):
            raise ExecutionError(
                "Command function must return an integer exit code",
                context={
                    "command": context.task_name,
                    "actual_type": type(result).__name__,
                },
            )
        return result

    def _safe_invoke_callback(
        self,
        callback: Callable | None,
        payload: Any,
        command_name: str,
        callback_type: str,
    ) -> None:
        if not callback:
            return
        try:
            callback(payload)
        except Exception as exc:  # pylint: disable=broad-except
            self._task_logger.log(
                "callback_error",
                LogLevel.ERROR,
                scope=LogScope.COMMAND,
                task=command_name,
                message=f"Callback {callback_type} failed",
                error=str(exc),
                _callback_type=callback_type,
            )

    def _log_cancellation(self, command_name: str, start_time: datetime) -> None:
        duration = (datetime.now() - start_time).total_seconds()
        self._task_logger.log(
            "execution_cancelled",
            LogLevel.INFO,
            scope=LogScope.COMMAND,
            task=command_name,
            message="Command cancelled",
            _duration=f"{duration:.2f}",
        )

    def execute_entry(
        self,
        entry: PreparedEntry,
        *,
        password: str | None,
        log_output: bool | None = None,
        sample_lines: int = 0,
        use_pty: bool = False,
    ) -> CommandResult:
        """Execute a prepared command entry synchronously."""

        if not isinstance(entry, PreparedEntry):
            raise ConfigurationError(
                "Command entry must be a PreparedEntry",
                context={"entry_type": type(entry).__name__},
            )

        return self._execute_prepared_entry(
            entry,
            password=password,
            log_output=log_output,
            sample_lines=sample_lines,
            default_use_pty=use_pty,
        )

    def _execute_prepared_entry(
        self,
        entry: PreparedEntry,
        *,
        password: str | None,
        log_output: bool | None,
        sample_lines: int,
        default_use_pty: bool,
    ) -> CommandResult:
        command_func = entry.func
        spec = entry.spec
        callback_factory = entry.callback_factory

        command_name = spec.command_name or self._resolve_command_name(command_func)
        task_name = spec.task_name or getattr(command_func, "_task_name", None)

        effective_use_pty = default_use_pty
        if spec.use_pty is not None:
            effective_use_pty = bool(spec.use_pty)

        execution = self._build_execution_params(
            spec.host,
            password=password,
            log_output=log_output,
            sample_lines=sample_lines,
            use_pty=effective_use_pty,
            task_name=task_name,
            shell_wrapper_mode=spec.shell_wrapper_mode,
            spec=spec,
        )

        callbacks = self.TaskCallbacks(output_callback=callback_factory)
        return self._execute_task(command_func, command_name, execution, callbacks)

    def cancel_all(
        self,
        *,
        reason: str | None = None,
        classification: CancellationClassification | None = None,
    ) -> None:
        """Cancel all running tasks with optional user-facing reason."""

        resolved_classification = classification or CancellationClassification.USER
        self._cancel_classification = resolved_classification
        if reason:
            self._cancel_reason = reason
        elif self._cancel_reason is None:
            default_reason = (
                "User cancellation"
                if resolved_classification == CancellationClassification.USER
                else None
            )
            self._cancel_reason = default_reason

        self._cancel_event.set()
        self._notify_cancel_listeners()

        session = self._session
        pending = session.active_command_count() if session else 0
        if session:
            self._session_safe_call("stop_all_streamers")

        if self.verbose and pending:
            self._task_logger.log(
                "all_tasks_cancelled",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message=f"Cancelling {pending} running tasks",
                _count=pending,
            )

        # Close connections
        self.close_transports()

    def get_cancel_reason(self, default: str | None = None) -> str | None:
        """Return the last cancellation reason if available."""

        return self._cancel_reason or default

    def get_cancel_classification(self) -> CancellationClassification:
        return self._cancel_classification

    def get_cancel_event(self) -> threading.Event:
        """Return the shared cancellation event."""

        return self._cancel_event

    def get_cancel_state(self) -> tuple[CancellationClassification, str | None]:
        """Return the current cancellation classification and reason."""

        return self._get_cancel_state()

    def _get_cancel_state(self) -> tuple[CancellationClassification, str | None]:
        return self._cancel_classification, self._cancel_reason

    def register_cancel_listener(self, listener: Callable[[], None]) -> None:
        """Register a callable that will be invoked when cancellation occurs."""

        if not callable(listener):
            raise ConfigurationError(
                "Cancellation listener must be callable",
                context={"listener_type": type(listener).__name__},
            )
        with self._cancel_listener_lock:
            self._cancel_listeners.add(listener)
        if self.was_cancelled():
            try:
                listener()
            except Exception as exc:  # noqa: BLE001
                self._task_logger.log(
                    "cancel_listener_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    message="Cancellation listener raised",
                    error=str(exc),
                    listener_type=type(listener).__name__,
                )

    def unregister_cancel_listener(self, listener: Callable[[], None]) -> None:
        """Remove a previously registered cancellation listener."""

        with self._cancel_listener_lock:
            self._cancel_listeners.discard(listener)

    def _notify_cancel_listeners(self) -> None:
        with self._cancel_listener_lock:
            listeners = list(self._cancel_listeners)
        for listener in listeners:
            try:
                listener()
            except Exception as exc:  # noqa: BLE001
                self._task_logger.log(
                    "cancel_listener_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    message="Cancellation listener raised",
                    error=str(exc),
                    listener_type=type(listener).__name__,
                )

    def close_transports(self) -> None:
        """Close all cached SSH connections."""
        self._cleanup.close_transports()

    def _normalize_command_exception(
        self,
        exc: Exception,
        command_name: str,
        execution: ExecutionParams,
    ) -> Exception:
        context = {
            "command": command_name,
            "task": execution.task_name,
            "host": execution.host,
        }
        if isinstance(exc, HILTestbenchError):
            exc.add_context(**{k: v for k, v in context.items() if v})
            return exc
        try:
            raise ExecutionError(
                f"Command '{command_name}' raised unexpected exception",
                context={k: v for k, v in context.items() if v},
            ) from exc
        except ExecutionError as wrapped:
            return wrapped

    def _log_command_failure(
        self, command_name: str, execution: ExecutionParams, error: Exception
    ) -> None:
        # Extract the root cause error message if available
        root_cause = error.__cause__ if error.__cause__ else error
        error_detail = str(root_cause)
        error_type = type(root_cause).__name__

        # Build comprehensive error message with context-aware remediation
        parts = [f"Command '{command_name}' failed"]
        if execution.host:
            parts.append(f"on {execution.host}")
        parts.append(f": {error_detail}")

        friendly_hint = self._result_builder.friendly_hint_for_error(
            command_name,
            error_detail,
            host=execution.host,
        )
        if friendly_hint:
            parts.append(f"({friendly_hint})")

        remediation = self._result_builder.remediation_for_error(
            error_detail,
            host=execution.host,
            port=execution.port if execution.host else None,
            is_ssh=execution.host is not None,
        )

        self._task_logger.log(
            "command_execution_failed",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=command_name,
            message=" ".join(parts),
            error_type=error_type,
            error=str(root_cause),
            host=execution.host,
            remediation=remediation,
            friendly_hint=friendly_hint,
        )

    def _normalize_shutdown_exception(self, exc: Exception, command_name: str) -> Exception:
        message = f"Failed to terminate task '{command_name}'"
        if isinstance(exc, HILTestbenchError):
            exc.add_context(command=command_name)
            return exc
        try:
            raise ExecutionError(message, context={"command": command_name}) from exc
        except ExecutionError as wrapped:
            return wrapped

    def get_running_tasks(self) -> list[str]:
        """Get list of currently running task names."""
        session = self._session
        if not session:
            return []
        return [name for name, _ in session.iter_contexts()]

    def get_task_log_file(self, command_name: str) -> str | None:
        """
        Get the log file path for a specific task.

        Args:
            command_name: Name of the task

        Returns:
            Path to the log file, or None if task hasn't been run
        """
        return self._task_logger.get_log_file(command_name)

    def get_all_log_files(self) -> dict[str, str]:
        """
        Get all log file paths for completed tasks.

        Returns:
            Dictionary mapping task names to log file paths
        """
        return self._task_logger.get_all_task_log_files()

    def get_main_log_file(self) -> str | None:
        """
        Get the main program log file path.

        Returns:
            Path to the main log file
        """
        return self._task_logger.get_main_log_file()

    def get_task_logger(self) -> TaskLogger:
        """Return the TaskLogger instance for structured logging factories."""
        return self._task_logger

    def _print_health_summary(self):
        """Print health monitoring summary at shutdown (suppressed for user output)."""
        # Suppressed: No console output for health summary
        pass
