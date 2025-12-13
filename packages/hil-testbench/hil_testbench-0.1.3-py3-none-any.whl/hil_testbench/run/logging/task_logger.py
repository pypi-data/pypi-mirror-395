"""TaskLogger: threadsafe structured logging for tasks and framework.

API:
   logger.log("event_name", level, **data)          # Auto-infers scope
   logger.log("event_name", scope=LogScope.FRAMEWORK, **data)
   logger.exception("error_event", **data)         # Smart exception capture
   logger.log_event_raw("event", scope, level, ...)  # Direct low-level API
"""

from __future__ import annotations

import atexit
import contextlib
import inspect
import json
import logging  # hil: allow-logging-import (logger implementation)
import os
import re
import sys
import threading
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum, IntEnum
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING, Any
from weakref import WeakSet

from hil_testbench.run.exceptions import ExecutionError, ValidationError
from hil_testbench.run.execution.protocols import (
    DisplayBackendProtocol,
    SupportsCommandStatus,
    SupportsLoggerBinding,
)
from hil_testbench.run.logging.console_output import ConsolePrinter
from hil_testbench.run.results.task_outcome import TaskOutcome

MESSAGE_FMT = "%(message)s"
_PLACEHOLDER_PATTERN = re.compile(r"<[^>]+>")


@dataclass(slots=True)
class _BufferedCliMessage:
    event: str
    message: str
    icon: str | None
    level: LogLevel
    scope: LogScope
    stderr: bool


_CLI_MESSAGE_BUFFER: list[_BufferedCliMessage] = []

if TYPE_CHECKING:
    from hil_testbench.config.run_config import RunConfig


class LogLevel(IntEnum):
    """Log level constants - use instead of importing logging module.

    Usage:
        Use `from hil_testbench.run.logging.task_logger import LogLevel` to import
        logger.log_struct("event", LogLevel.INFO, ...)

    Levels:
        TRACE   (numeric < DEBUG): ultra-verbose diagnostic detail; off by default.
                 Use for per-iteration / high-frequency internal state.
        DEBUG   Developer-centric context, lifecycle, and decisions.
        INFO    User-relevant high-level lifecycle and results.
        WARNING Situations that may require attention but execution continues.
        ERROR   Failures that caused an operation to abort or produce invalid results.
        CRITICAL Irrecoverable application state.

    Console behavior:
        Underscore-prefixed fields (e.g. _pid, _duration) appear only when
        console log level is DEBUG or TRACE. TRACE shows everything DEBUG shows.
        Setting run_config.log_level = "TRACE" enables the lower threshold.
    """

    TRACE = (logging.DEBUG) - 10
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogScope(Enum):
    """Semantic scope for a log event.

    FRAMEWORK: Runner/framework level (lifecycle, configuration) → main log only
    TASK: High-level task lifecycle (started/completed) → main log only
    COMMAND: Individual command execution output/events → per-command log
    """

    FRAMEWORK = "framework"
    TASK = "task"
    COMMAND = "command"


class TaskLogger:
    """
    Threadsafe logger for task-specific and program-wide logs.
    """

    _instances: WeakSet[TaskLogger] = WeakSet()

    def __init__(
        self,
        run_config: RunConfig,
        log_dir: str = "logs",
        correlation_id: str | None = None,
    ):
        """
        Initialize TaskLogger with RunConfig.

        Args:
            run_config: RunConfig object with logging settings
            log_dir: Directory for log files (default: "logs")
            correlation_id: Unique ID for tracking multi-run sessions (auto-generated if None)
        """
        if getattr(self, "_initialized", False):
            return

        # Extract settings from RunConfig
        max_bytes_main = run_config.max_log_size_main_mb * 1024 * 1024
        max_log_file_count_main = run_config.max_log_file_count_main
        max_bytes_task = run_config.max_log_size_task_mb * 1024 * 1024
        max_log_file_count_task = run_config.max_log_file_count_task
        log_level_console = run_config.log_level
        log_level_file = run_config.log_level_file
        daemon_mode = run_config.daemon_mode
        enable_console = not daemon_mode

        log_dir_abs = os.path.abspath(log_dir)
        # New configuration flags
        self.no_color = run_config.no_color
        self.json_console = run_config.json_console
        self.quiet_errors_only = run_config.quiet_errors_only

        # Allow overriding directory via run_config.log_dir ONLY when caller did not
        # explicitly supply a custom log_dir (i.e. left default 'logs'). This prevents
        # tests that inject a temporary directory via the log_dir parameter from being
        # silently redirected back to the default from run_config.
        if run_config.log_dir and run_config.log_dir != log_dir and log_dir == "logs":
            log_dir_abs = os.path.abspath(run_config.log_dir)

        self.log_dir = log_dir_abs
        self.max_bytes_main = max_bytes_main
        self.max_bytes_task = max_bytes_task
        self.max_log_file_count_main = max_log_file_count_main
        self.max_log_file_count_task = max_log_file_count_task
        self.enable_console = enable_console
        self.daemon_mode = daemon_mode
        self.correlation_id = correlation_id or uuid.uuid4().hex[:12]
        self._console_printer = ConsolePrinter(
            daemon_mode=daemon_mode,
            quiet_errors_only=self.quiet_errors_only,
            json_console=self.json_console,
            no_color=self.no_color,
            correlation_id=self.correlation_id,
        )
        self._display_backend: DisplayBackendProtocol | None = None
        self._last_display_backend: DisplayBackendProtocol | None = None
        # Register custom TRACE level if not already present in logging module
        if not hasattr(logging, "TRACE"):
            logging.TRACE = LogLevel.TRACE  # type: ignore[attr-defined]
            logging.addLevelName(LogLevel.TRACE, "TRACE")

        requested_console_level = log_level_console.upper()
        self.log_level_console = getattr(logging, requested_console_level, logging.INFO)
        self.log_level_file = getattr(logging, log_level_file.upper(), logging.DEBUG)
        self._lock = threading.Lock()
        self._dynamic_fields_lock = threading.Lock()
        self._loggers: dict[str, logging.Logger] = {}
        self._files: dict[str, str] = {}
        self._task_counts: dict[str, int] = {}
        self._dynamic_fields: dict[str, dict[str, str]] = {}
        self._shutdown_signal_logged = False
        self._shutdown_in_progress = False
        self._closed = False
        self._message_quality_warnings: set[str] = set()

        # Create root logs directory
        os.makedirs(log_dir_abs, exist_ok=True)

        # Create per-execution directory with human-readable timestamp unless reusing
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]  # YYYY-MM-DD_HH-MM-SS_mmm
        exec_dir = os.path.join(self.log_dir, ts)
        os.makedirs(exec_dir, exist_ok=True)
        self.execution_dir = exec_dir
        self._latest_pointer_path = os.path.join(self.log_dir, "latest-run")
        self._update_latest_pointer()

        # Create main program logger
        self._setup_main_logger()
        self._initialized = True
        TaskLogger._instances.add(self)
        flush_cli_messages(self)

    def _setup_main_logger(self):
        """Set up the main program logger."""
        log_file = os.path.join(self.execution_dir, "runner.log")
        self._main_log_file = log_file

        self._main_logger = logging.getLogger("taskrunner_main")
        self._main_logger.setLevel(self.log_level_file)
        self._main_logger.handlers.clear()

        self._add_file_handler(log_file)

    def _add_file_handler(self, log_file: str) -> None:
        """Add rotating file handler to main logger."""
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes_main,
            backupCount=self.max_log_file_count_main,
            encoding="utf-8",
        )
        file_handler.setLevel(self.log_level_file)
        formatter = logging.Formatter(MESSAGE_FMT)
        file_handler.setFormatter(formatter)
        self._main_logger.addHandler(file_handler)

    # Dynamic field registry API
    def register_dynamic_field(self, name: str, type_name: str) -> None:
        """Register a dynamically added parameter field for resume.

        Args:
            name: Parameter name
            type_name: Inferred type name
        """
        if not name:
            return
        with self._dynamic_fields_lock:
            if name not in self._dynamic_fields:
                self._dynamic_fields[name] = {"type": type_name}

    def snapshot_dynamic_fields(self) -> dict[str, dict[str, str]]:
        """Return a shallow copy of dynamic field registry."""
        with self._dynamic_fields_lock:
            return dict(self._dynamic_fields)

    def _add_console_handler(self) -> None:
        """Add console handler to main logger if not already present."""
        has_console = any(
            isinstance(h, logging.StreamHandler)
            and not isinstance(h, RotatingFileHandler | logging.FileHandler)
            for h in self._main_logger.handlers
        )
        if has_console:
            return

        console_handler = self._create_console_handler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(MESSAGE_FMT))
        self._main_logger.addHandler(console_handler)

    def _create_console_handler(self) -> logging.StreamHandler:
        """Create console handler for JSONL logging output.

        NOTE: Console handler is DISABLED when display backend is present.
        All console output goes through _console_print() using Rich Console directly.
        """

        # Custom handler that only emits the message without timestamp/level/module
        class ConsoleHandler(logging.StreamHandler):
            """StreamHandler that suppresses empty formatted messages."""

            def emit(self, record: logging.LogRecord) -> None:
                try:
                    msg = self.format(record)
                    if not msg or not str(msg).strip():
                        return
                    stream = self.stream
                    try:
                        stream.write(msg + self.terminator)
                    except UnicodeEncodeError:
                        enc = getattr(stream, "encoding", None) or "utf-8"
                        safe = msg.encode(enc, errors="ignore").decode(enc, errors="ignore")
                        stream.write(safe + self.terminator)
                    self.flush()
                except Exception:  # pylint: disable=broad-except
                    self.handleError(record)

        return ConsoleHandler(sys.stdout)

    # Removed complex console formatter: no lifecycle/icon formatting retained.

    # Core logging API: log_event_raw() and convenience methods

    def log(
        self,
        event: str,
        level: int | LogLevel = LogLevel.INFO,
        scope: LogScope | None = None,
        task: str | None = None,
        icon: str | None = None,
        message: str | None = None,
        show_fields_with_message: bool = False,
        **data,
    ) -> None:
        """Log a structured event with automatic scope inference.

        Args:
            event: Semantic event name (e.g., "task_started", "validation_failed").
            level: Log level (DEBUG, INFO, WARNING, ERROR).
            scope: Explicit scope (FRAMEWORK, TASK, COMMAND). If None, inferred from event/task.
            task: Task name for routing (creates separate log file for COMMAND scope).
            icon: Optional emoji/icon to display in console output (e.g., "▶️", "✅", "❌").
            message: Optional explicit console message (auto-generated from event+data if omitted).
            show_fields_with_message: If True, append key=value fields even when message is provided.
            **data: Additional key-value pairs for structured logging.
                   - Fields with _ prefix: Only shown at DEBUG console level
                   - All fields are logged to JSONL regardless of prefix

        Examples:
            # Auto-generated message from event name and fields
            logger.log("process_started", pid=1234, command="example_cmd")
            # Console: "Process Started | pid=1234 | command=example_cmd"

            # Debug-only fields (prefix with _)
            logger.log("process_started", pid=1234, _host="localhost", _cwd="/tmp")
            # Console at INFO:  "Process Started | pid=1234"
            # Console at DEBUG: "Process Started | pid=1234 | host=localhost | cwd=/tmp"

            # Explicit message with fields appended
            logger.log("cleanup_incomplete", LogLevel.WARNING, message="Cleanup incomplete",
                       orphaned=10, cleaned=5, show_fields_with_message=True)
            # Console: "Cleanup incomplete | orphaned=10 | cleaned=5"
        """
        scope = scope or self._infer_scope(event, task)
        payload = self._build_log_payload(
            message=self._enforce_message_quality(event, level, message),
            show_fields_with_message=show_fields_with_message,
            data=data,
        )
        self._ensure_main_logger_ready(scope)
        self.log_event_raw(event, scope, level, task, exception=False, icon=icon, **payload)

    def _update_latest_pointer(self) -> None:
        """Write the latest-run marker for fast session lookup."""

        tmp_path = f"{self._latest_pointer_path}.tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as handle:
                handle.write(f"{self.execution_dir}\n")
            os.replace(tmp_path, self._latest_pointer_path)
        except OSError:
            # Best-effort hint; skip failures to avoid blocking task start
            pass

    @staticmethod
    def get_latest_execution_dir(log_dir: str) -> str | None:
        """Return the newest execution directory recorded in log_dir."""

        pointer_path = os.path.join(os.path.abspath(log_dir), "latest-run")
        try:
            with open(pointer_path, encoding="utf-8") as handle:
                target = handle.read().strip()
        except OSError:
            return None
        if not target:
            return None
        return target if os.path.isdir(target) else None

    def log_shutdown_signal(
        self,
        *,
        shutdown_file: str,
        task: str | None = None,
        pid: int | None = None,
    ) -> bool:
        """Emit shutdown detection once per execution."""

        with self._lock:
            if self._shutdown_signal_logged:
                return False
            self._shutdown_signal_logged = True

        extra_fields: dict[str, Any] = {"shutdown_file": shutdown_file}
        if task:
            extra_fields["task"] = task
        if pid is not None:
            extra_fields["_pid"] = pid

        self.log(
            "shutdown_signal_received",
            LogLevel.INFO,
            scope=LogScope.FRAMEWORK,
            message="Shutdown signal detected, stopping execution",
            **extra_fields,
        )
        return True

    def exception(self, event: str, task: str | None = None, **data) -> None:
        """Log an exception with automatic traceback capture.

        Caller just passes the event name and data - logger automatically:
        - Captures current exception and traceback via exc_info=True
        - Logs full traceback to JSONL always
        - Shows traceback on console only if debug mode or not daemon

        Args:
            event: Semantic event name (e.g., "connection_failed", "validation_error").
            task: Optional task name for routing.
            **data: Additional context (error message, etc.).

        Example:
            try:
                connect_to_server()
            except Exception as e:
                logger.exception("connection_failed", error=str(e))
        """
        scope = self._infer_scope(event, task)
        self.log_event_raw(event, scope, LogLevel.ERROR, task, exception=True, **data)

    def log_task_summary(self, outcome: TaskOutcome) -> None:
        """Emit a structured task_summary event for the provided outcome."""

        if not isinstance(outcome, TaskOutcome):  # Defensive type check
            raise TypeError("outcome must be TaskOutcome")

        self.log(
            "task_summary",
            level=LogLevel.INFO,
            scope=LogScope.TASK,
            task=outcome.task_name,
            message=outcome.format_summary(),
            total_commands=outcome.total_commands,
            failed_commands=outcome.failed_commands,
            duration_seconds=outcome.duration_seconds,
            success=outcome.success,
            show_fields_with_message=True,
            _plain_console=True,
        )

    def _get_logger(self, task_name: str) -> logging.Logger:
        """Get or create a logger for a specific task within the execution folder.

        If the same task runs multiple times, files will be suffixed with
        an incrementing counter: task.log, task_2.log, task_3.log, ...
        """
        with self._lock:
            if task_name not in self._loggers:
                # Determine unique filename for this task in this execution
                count = self._task_counts.get(task_name, 0) + 1
                self._task_counts[task_name] = count
                # Sanitize task_name for Windows filenames (replace colons)
                sanitized_name = task_name.replace(":", "__")
                base_name = (
                    f"{sanitized_name}.log" if count == 1 else f"{sanitized_name}_{count}.log"
                )
                log_file = os.path.join(self.execution_dir, base_name)
                self._files[task_name] = log_file

                # Create logger
                logger = logging.getLogger(f"task_{task_name}")
                logger.setLevel(logging.DEBUG)

                # Remove any existing handlers
                logger.handlers.clear()

                # Create file handler with rotation (5MB max, keep 10 rotated files per task)
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=self.max_bytes_task,
                    backupCount=self.max_log_file_count_task,
                    encoding="utf-8",
                )
                file_handler.setLevel(self.log_level_file)

                # JSONL format - just the raw JSON object per line, no timestamp prefix
                formatter = logging.Formatter(MESSAGE_FMT)
                file_handler.setFormatter(formatter)

                # Add handler to logger
                logger.addHandler(file_handler)

                self._loggers[task_name] = logger

            return self._loggers[task_name]

    def get_log_file(self, task_name: str) -> str | None:
        """Get the log file path for a task."""
        with self._lock:
            return self._files.get(task_name)

    def close_task_logger(self, task_name: str):
        """Close and cleanup logger for a specific task."""
        with self._lock:
            self._close_task_logger_unlocked(task_name)

    def _close_task_logger_unlocked(self, task_name: str):
        """Internal: close task logger without acquiring lock (caller must hold lock)."""
        if task_name in self._loggers:
            logger = self._loggers[task_name]
            # Close and remove all handlers
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
            # Keep logger in dict to prevent creating duplicate files
            # when subsequent logs (like command_result) are written after command completes

    def close_all(self):
        """Close all loggers and display backends."""

        if getattr(self, "_closed", False):
            return
        self._closed = True

        with self._lock:
            for task_name in self._loggers:
                self._close_task_logger_unlocked(task_name)

            # Close main logger
            if hasattr(self, "_main_logger"):
                for handler in self._main_logger.handlers:
                    handler.close()

        backend = self._display_backend
        if backend is not None:
            self._last_display_backend = backend
        if backend:
            shutdown = getattr(backend, "shutdown", None)
            stop = getattr(backend, "stop", None)
            with contextlib.suppress(Exception):
                if callable(shutdown):
                    shutdown()
                elif callable(stop):
                    stop()
        self._display_backend = None

        # Allow fresh initialization for the next execution
        self._initialized = False
        TaskLogger._instances.discard(self)

    @classmethod
    def shutdown_all(cls) -> None:
        """Close all known TaskLogger instances (primarily for tests)."""

        for logger in cls._instances.copy():
            with contextlib.suppress(Exception):
                logger.close_all()

    def get_main_log_file(self) -> str:
        """Get the main program log file path."""
        if not hasattr(self, "_main_log_file"):
            msg = "TaskLogger is not initialized; main log file unavailable"
            raise ExecutionError(
                msg,
                context={"logger_initialized": False},
            )
        return self._main_log_file

    def get_execution_dir(self) -> str:
        """Get the per-execution log directory path."""
        return self.execution_dir

    def get_correlation_id(self) -> str:
        """Return correlation id for this execution."""
        return self.correlation_id

    def set_display_backend(self, backend: DisplayBackendProtocol | None) -> None:
        """Set the display backend for event routing and console output.

        When backend has a console attribute, _console_print() will use it directly
        instead of creating a separate Rich Console instance.

        Also removes console handler from logger since all console output
        now goes through _console_print() → Rich Console (not via logging handler).
        """
        self._display_backend = backend
        self._last_display_backend = backend
        if backend and isinstance(backend, SupportsLoggerBinding):
            backend.bind_logger(self)

        # Remove console handler from logger - display will handle all console output
        if backend and hasattr(backend, "console"):
            # Remove StreamHandler (but keep file handlers)
            self._main_logger.handlers = [
                h
                for h in self._main_logger.handlers
                if not isinstance(h, logging.StreamHandler)
                or isinstance(h, RotatingFileHandler | logging.FileHandler)
            ]
        self._console_printer.set_backend(backend)

    def get_display_backend(self) -> DisplayBackendProtocol | None:
        """Return the currently bound display backend, if any."""

        return self._display_backend or self._last_display_backend

    def notify_display_command_status(
        self,
        task_name: str | None,
        command_name: str,
        status: str | None = None,
        backend: DisplayBackendProtocol | None = None,
        *,
        lifecycle_status: str | None = None,
    ) -> None:
        """Propagate command status updates to the live display backend if available."""

        target = backend or self.get_display_backend()
        if not target or not isinstance(target, SupportsCommandStatus):
            return

        resolved_task = task_name or command_name.split(":", 1)[0]

        try:
            target.update_command_status(
                resolved_task,
                command_name,
                status,
                lifecycle_status=lifecycle_status,
            )
        except Exception as exc:  # noqa: BLE001
            self.log(
                "display_command_status_failed",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                task_name=resolved_task,
                command_name=command_name,
                status=status,
                lifecycle_status=lifecycle_status,
                error=str(exc),
            )

    def _derive_context_label(self, scope: LogScope | None, task: str | None) -> str | None:
        if task:
            return task.upper()
        if scope:
            return scope.value.upper()
        return None

    # Structured logging API
    def log_struct(  # hil: allow-log-struct (internal implementation)
        self,
        event: str,
        level: int | LogLevel = LogLevel.INFO,
        scope: LogScope | None = None,
        task: str | None = None,
        exception: bool = False,
        **data,
    ) -> None:
        """Emit a structured JSON log line."""
        # Simplified: require explicit scope or infer minimally, no display routing.
        scope = scope or self._infer_scope(event, task)
        self.log_event_raw(
            event=event,
            scope=scope,
            level=level,
            task=task,
            exception=exception,
            **data,
        )

    def log_event_raw(
        self,
        event: str,
        scope: LogScope,
        level: int | LogLevel = LogLevel.INFO,
        task: str | None = None,
        exception: bool = False,
        icon: str | None = None,
        **data,
    ) -> None:
        """Minimal logging funnel.

        Accepts explicit scope and writes a single JSON object without any
        additional formatting, scope inference, or display routing. This is the
        lean API for future callers wanting a pure "event -> writers" path.

        Args:
            event: Semantic event name.
            scope: Explicit log scope (no inference performed).
            level: Numeric or LogLevel enum value.
            task: Optional task/command routing key (only used for COMMAND scope).
            exception: Whether to attach exception info for underlying logger.
            icon: Optional emoji/icon to display in console output.
            **data: Arbitrary serializable key/value pairs for the event.
        """
        payload = self._build_payload(event, level, scope, task, data)
        message = json.dumps(payload, ensure_ascii=False)
        logger = self._route_logger(scope, task)
        safe_level = self._resolve_safe_level(level)
        with contextlib.suppress(Exception):
            logger.log(safe_level, message, exc_info=exception)

        # Print human-readable console output (icon optional)
        self._print_console_message(icon, level, data, event, scope, task)

    @property
    def shutdown_in_progress(self) -> bool:
        """Return True when the runner is handling a shutdown signal."""

        return self._shutdown_in_progress

    def mark_shutdown_in_progress(self) -> None:
        """Record that shutdown handling has begun."""

        self._shutdown_in_progress = True

    def clear_shutdown_flag(self) -> None:
        """Clear shutdown flag for reuse in long-lived logger instances."""

        self._shutdown_in_progress = False

    def _print_console_message(
        self,
        icon: str | None,
        level: int | LogLevel,
        data: dict,
        event: str = "",
        scope: LogScope | None = None,
        task: str | None = None,
    ) -> None:
        """Print console message - auto-generates from event data if no message field.

        Ensures console and file logs have same visibility at same log level.
        """
        if not self.enable_console:
            return
        if level < self.log_level_console:
            return

        message_text = data.get("message")
        if not message_text or not isinstance(message_text, str) or not message_text.strip():
            return

        formatted_msg = message_text
        level_str = logging.getLevelName(level) if isinstance(level, int) else str(level)
        caller_module = (
            self._resolve_caller_module() if self.log_level_console <= logging.DEBUG else None
        )
        context_label = self._derive_context_label(scope, task)
        self._console_print(
            formatted_msg,
            level=level_str,
            context_label=context_label,
            module_label=caller_module,
            force_inline=bool(data.get("_concise_console")),
            plain=bool(data.get("_plain_console")),
            icon_override=icon,
        )

    def _resolve_caller_module(self) -> str | None:
        frame = inspect.currentframe()
        try:
            current_frame = frame
            while current_frame:
                frame_info = inspect.getframeinfo(current_frame)
                filename = frame_info.filename or ""
                if filename and "task_logger.py" not in filename:
                    if "hil_testbench" in filename:
                        parts = filename.replace("\\", "/").split("hil_testbench/")
                        if len(parts) > 1:
                            return parts[1].replace("/", ".").replace(".py", "")
                    return os.path.basename(filename).replace(".py", "")
                current_frame = current_frame.f_back
        finally:
            del frame
        return None

    def _build_log_payload(
        self,
        *,
        message: str | None,
        show_fields_with_message: bool,
        data: dict,
    ) -> dict:
        payload = dict(data)
        if message is not None:
            payload["message"] = message
        if show_fields_with_message:
            payload["_show_fields"] = True
        return payload

    def _ensure_main_logger_ready(self, scope: LogScope) -> None:
        if scope == LogScope.COMMAND:
            return
        try:
            target_logger = self._main_logger
        except AttributeError:
            return
        for handler in target_logger.handlers:
            stream = getattr(handler, "stream", None)
            if stream is None or not getattr(stream, "closed", False):
                continue
            if stream is sys.stdout:
                target_logger.removeHandler(handler)
                target_logger.addHandler(self._create_console_handler())
                continue
            with contextlib.suppress(Exception):
                if log_path := getattr(self, "_main_log_file", None):
                    target_logger.removeHandler(handler)
                    new_file = RotatingFileHandler(
                        log_path,
                        maxBytes=self.max_bytes_main,
                        backupCount=self.max_log_file_count_main,
                        encoding="utf-8",
                    )
                    new_file.setLevel(self.log_level_file)
                    new_file.setFormatter(logging.Formatter(MESSAGE_FMT))
                    target_logger.addHandler(new_file)

    def _infer_scope(self, event: str, task: str | None) -> LogScope:
        if task is None:
            return LogScope.TASK if event.startswith("task_") else LogScope.FRAMEWORK
        return LogScope.TASK if event.startswith("task_") else LogScope.COMMAND

    def _build_payload(
        self,
        event: str,
        level: int | LogLevel,
        scope: LogScope,
        task: str | None,
        data: dict,
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "cid": self.correlation_id,
            "level": logging.getLevelName(level),
            "event": event,
            "scope": scope.value,
        }
        if task:
            payload["task"] = task
        if data:
            safe_data: dict[str, object] = {}
            for k, original in data.items():
                if isinstance(original, str):
                    safe_data[k] = original.replace("\\", "/") if "\\" in original else original
                elif isinstance(original, int | float | bool) or original is None:
                    safe_data[k] = original
                else:
                    safe_data[k] = repr(original)
            payload["data"] = safe_data
        return payload

    def _route_logger(self, scope: LogScope, task: str | None) -> logging.Logger:
        if scope == LogScope.COMMAND and task:
            return self._get_logger(task)
        return self._main_logger

    def _resolve_safe_level(self, level: int | LogLevel) -> int:
        if not isinstance(level, int):  # pragma: no cover
            return logging.INFO
        if level <= logging.DEBUG:
            return logging.DEBUG
        if level <= logging.INFO:
            return logging.INFO
        if level <= logging.WARNING:
            return logging.WARNING
        return logging.ERROR if level <= logging.ERROR else logging.CRITICAL

    def _enforce_message_quality(
        self,
        event: str,
        level: int | LogLevel,
        message: str | None,
    ) -> str | None:
        # Skip enforcement for internal quality violation events to prevent recursion
        if (
            event == "message_quality_violation"
            or event.startswith("message_quality_")
            or event == "display_config_template_placeholders"
        ):
            return message
        if not message:
            return message
        if isinstance(level, LogLevel):
            numeric_level = int(level)
        elif isinstance(level, int):
            numeric_level = level
        else:
            try:
                self.log(
                    "message_quality_enforcement_invalid_level",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    message=(
                        f"Message quality enforcement skipped for event '{event}': "
                        f"received invalid level type {type(level).__name__}."
                    ),
                    _violating_event=event,
                    _invalid_level_type=type(level).__name__,
                )
            except Exception:
                pass
            return message
        if numeric_level < LogLevel.WARNING:
            return message
        if not _PLACEHOLDER_PATTERN.search(message):
            return message

        note = (
            f"Log event '{event}' attempted to emit WARNING/ERROR message with template placeholders. "
            "Replace <placeholder> tokens with real entities per .github/copilot/message_quality.md."
        )

        if os.getenv("HIL_TESTBENCH_STRICT_LOG_MESSAGES") == "1":
            raise ValidationError(
                note,
                context={
                    "event": event,
                    "log_level": numeric_level,
                },
            )

        self._report_message_quality_violation(event, note)
        return _PLACEHOLDER_PATTERN.sub("[placeholder]", message)

    def _report_message_quality_violation(self, event: str, note: str) -> None:
        if event in self._message_quality_warnings:
            return
        self._message_quality_warnings.add(event)
        try:
            self.log(
                "message_quality_violation",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message=note,
                _violating_event=event,
            )
        except Exception:
            pass

    # Removed display backend smart routing: logger no longer formats lifecycle/error events.

    # Removed error formatting helpers.

    def get_all_task_log_files(self) -> dict[str, str]:
        """Return a copy of the mapping of task_name -> latest log file path."""
        with self._lock:
            return dict(self._files)

    @dataclass(slots=True)
    class _TaskSummaryBundle:
        console_block: str
        console_summary: list[dict[str, object]]
        detailed_summary: list[dict[str, object]]
        success_count: int
        failure_count: int

    def print_task_status_summary(self, results: list):
        """Emit task status summary as structured log event."""
        summary = self._build_task_summary_bundle(results)
        self.log(
            "task_status_summary",
            level=LogLevel.INFO,
            message=summary.console_block,
            summary=summary.console_summary,
        )
        self._log_task_summary_totals(summary)

    def _build_task_summary_bundle(self, results: list) -> _TaskSummaryBundle:
        lines = ["\nTask Status Summary:", "-" * 60]
        console_summary: list[dict[str, object]] = []
        detailed_summary: list[dict[str, object]] = []
        success_count = 0
        failure_count = 0

        for result in results:
            icon = "✅" if result.success else "❌"
            status = "SUCCESS" if result.success else "FAILED"
            duration = f"{result.duration:.2f}s" if result.duration else "N/A"
            reason = self._format_failure_reason(result)
            lines.append(
                f"{icon} {result.task_name:20} {status:7} [Exit: {result.return_code}] [Duration: {duration}] {reason}"
            )

            console_summary.append(
                {
                    "task": result.task_name,
                    "success": result.success,
                    "return_code": result.return_code,
                    "duration": result.duration,
                }
            )
            detailed_summary.append(
                {
                    **console_summary[-1],
                    "error": self._extract_error_field(result),
                }
            )

            if result.success:
                success_count += 1
            else:
                failure_count += 1

        lines.append("-" * 60)
        block = "\n".join(lines)
        return self._TaskSummaryBundle(
            console_block=block,
            console_summary=console_summary,
            detailed_summary=detailed_summary,
            success_count=success_count,
            failure_count=failure_count,
        )

    def _log_task_summary_totals(self, summary: _TaskSummaryBundle) -> None:
        summary_text = f"{summary.success_count} succeeded, {summary.failure_count} failed"
        self.log(
            "task_status_summary",
            LogLevel.INFO,
            scope=LogScope.FRAMEWORK,
            message=f"Task execution complete: {summary_text}",
            summary=summary.detailed_summary,
        )

    def _format_failure_reason(self, result) -> str:
        if result.success:
            return ""
        if result.status_message:
            return f"Reason: {result.status_message}"
        if result.error:
            return f"Reason: {str(result.error)}"
        return f"Reason: {result.stderr.strip()[:100]}" if result.stderr else ""

    def _extract_error_field(self, result):
        if result.error:
            return str(result.error)
        return result.stderr.strip() if result.stderr else None

    def print_execution_summary(self, outcome, schema=None) -> None:
        """Print final execution summary to console."""

        self._print_summary_header(outcome)
        self._print_failed_commands(outcome)
        self._print_successful_commands(outcome)
        self._print_captured_parameters(schema)
        self._print_log_location(outcome)
        print("=" * 70 + "\n")  # hil: allow-print (CLI summary output)

    def _print_summary_header(self, outcome) -> None:
        print("\n" + "=" * 70)  # hil: allow-print (CLI summary output)
        print("EXECUTION SUMMARY")  # hil: allow-print (CLI summary output)
        print("=" * 70)  # hil: allow-print (CLI summary output)
        status_symbol = "✅" if outcome.success else "❌"
        task_display = outcome.task_name or "Task"
        print(f"\nTask: {task_display}")  # hil: allow-print (CLI summary output)
        result_text = "SUCCESS" if outcome.success else "FAILED"
        print(f"Status: {status_symbol} {result_text}")  # hil: allow-print (CLI summary output)
        print(f"Duration: {outcome.duration_seconds:.2f}s")  # hil: allow-print
        print(  # hil: allow-print (CLI summary output)
            f"Commands: {outcome.total_commands} total, {outcome.failed_commands} failed"
        )

    def _print_failed_commands(self, outcome) -> None:
        if outcome.failed_commands <= 0:
            return
        print("\nFailed Commands:")  # hil: allow-print (CLI summary output)
        for result in outcome.commands_by_status(success=False):
            event_info = f" (events={result.event_count})" if result.event_count > 0 else ""
            print(
                f"  ❌ {result.command_name}{event_info}"
            )  # hil: allow-print (CLI summary output)
            if result.status_message:
                print(  # hil: allow-print (CLI summary output)
                    f"     Reason: {result.status_message}"
                )

    def _print_successful_commands(self, outcome) -> None:
        successful = outcome.commands_by_status(success=True)
        if not successful:
            return
        print("\nCompleted Commands:")  # hil: allow-print (CLI summary output)
        for result in successful:
            event_info = f" (events={result.event_count})" if result.event_count > 0 else ""
            print(
                f"  ✅ {result.command_name}{event_info}"
            )  # hil: allow-print (CLI summary output)

    def _print_captured_parameters(self, schema) -> None:
        if not schema or not getattr(schema, "fields", None):
            return
        print("\nCaptured Parameters:")  # hil: allow-print (CLI summary output)
        for field in schema.fields:
            unit_str = f" ({field.unit})" if field.unit else ""
            desc_str = f" - {field.description}" if field.description else ""
            primary_str = " [PRIMARY]" if field.is_primary else ""
            print(
                f"  • {field.name}{unit_str}{primary_str}{desc_str}"
            )  # hil: allow-print (CLI summary output)

    def _print_log_location(self, outcome) -> None:
        if outcome.log_directory:
            print(f"\nLogs: {outcome.log_directory}")  # hil: allow-print
        elif hasattr(self, "execution_dir"):
            print(f"\nLogs: {self.execution_dir}")  # hil: allow-print

    @property
    def _rich_console(self):  # pragma: no cover - compatibility proxy
        return self._console_printer.rich_console

    def _console_print(
        self,
        message: str,
        *,
        level: str = "INFO",
        context_label: str | None = None,
        module_label: str | None = None,
        force_inline: bool = False,
        plain: bool = False,
        icon_override: str | None = None,
    ) -> None:
        """Legacy console hook retained for tests and tooling.

        All console output flows through ConsolePrinter to ensure consistent
        routing (backend console sharing, quiet-errors mode, JSON console, etc.).
        Tests patch this hook directly, so keep it as the single call site.
        """

        if not message:
            return

        normalized = message.replace("\r", "")
        self._console_printer.emit(
            normalized,
            level,
            context_label=context_label,
            module_label=module_label,
            force_inline=force_inline,
            plain=plain,
            icon_override=icon_override,
        )


def queue_cli_message(
    *,
    event: str,
    message: str,
    icon: str | None = None,
    level: LogLevel = LogLevel.INFO,
    scope: LogScope = LogScope.FRAMEWORK,
    stderr: bool = False,
) -> None:
    """Queue a CLI message for the next available TaskLogger."""

    logger = _active_logger()
    entry = _BufferedCliMessage(event, message, icon, level, scope, stderr)
    if logger is not None:
        _log_buffered_entry(logger, entry)
        return
    _CLI_MESSAGE_BUFFER.append(entry)


def flush_cli_messages(logger: TaskLogger | None = None) -> None:
    if not _CLI_MESSAGE_BUFFER:
        return

    target = logger or _active_logger()
    if target is not None:
        entries = list(_CLI_MESSAGE_BUFFER)
        _CLI_MESSAGE_BUFFER.clear()
        for entry in entries:
            _log_buffered_entry(target, entry)
        return

    _print_buffered_entries()


def _log_buffered_entry(logger: TaskLogger, entry: _BufferedCliMessage) -> None:
    logger.log(
        entry.event,
        entry.level,
        scope=entry.scope,
        icon=entry.icon,
        message=entry.message,
    )


def _print_buffered_entries() -> None:
    if not _CLI_MESSAGE_BUFFER:
        return
    entries = list(_CLI_MESSAGE_BUFFER)
    _CLI_MESSAGE_BUFFER.clear()
    for entry in entries:
        stream = sys.stderr if entry.stderr else sys.stdout
        prefix = f"{entry.icon} " if entry.icon else ""
        print(f"{prefix}{entry.message}", file=stream)  # hil: allow-print


def _active_logger() -> TaskLogger | None:
    for logger in TaskLogger._instances.copy():
        if getattr(logger, "_closed", False):
            continue
        return logger
    return None


atexit.register(flush_cli_messages)
