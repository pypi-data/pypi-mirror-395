"""Output streaming handler for real-time task output processing."""

import sys
import threading
import time
from io import StringIO
from typing import TYPE_CHECKING, Any

from hil_testbench.data_processing.events import CommandOutputCallback, CommandOutputEvent
from hil_testbench.run.logging.task_logger import LogLevel, TaskLogger

if TYPE_CHECKING:  # pragma: no cover - import for type hints only
    from hil_testbench.run.execution.command_spec import CommandSpec

# TODO(long_running): Split this class into a lightweight dispatcher that forwards
# decoded stream events into the data pipeline and a background sampler that
# handles buffering for diagnostics. The dispatcher should emit structured
# events that include stream type, timestamp, and parser metadata, and it must
# run parser callbacks provided by `CommandSpec.parser_factory` without assuming
# iperf- or paramiko-specific payloads. No command-specific branching should live
# here; use registry-driven parser hooks instead.


class OutputStreamer:
    """Handles real-time output streaming with callbacks and logging."""

    def __init__(
        self,
        task_name: str,
        callback: CommandOutputCallback | None = None,
        logger: TaskLogger | None = None,
        log_output: bool | None = None,
        sample_lines: int = 0,
    ):
        self.task_name = task_name
        self.callback = callback
        self.logger = logger
        self.stdout_buffer = StringIO()
        self.stderr_buffer = StringIO()
        self._stop_event = threading.Event()
        # Logging policy: None => auto (don't log raw if callback present)
        self._log_output = log_output
        self._sample_lines = max(0, sample_lines)
        self._lines_logged = 0
        # Stats
        self.total_lines = 0
        self.total_stderr_lines = 0
        self.total_bytes = 0
        self.callback_calls = 0
        self._callback_condition = threading.Condition()
        self._pending_callbacks = 0
        self._stats_lock = threading.Lock()
        # First data tracking for debug
        self._first_data_received = False
        self._command_spec = None
        self._spec_identity: dict[str, Any] | None = None

    def _buffer_line(self, line: str, is_error: bool) -> None:
        if is_error:
            self.stderr_buffer.write(line + "\n")
        else:
            self.stdout_buffer.write(line + "\n")

    def _update_stats(self, line: str, is_error: bool) -> None:
        self.total_lines += 1
        if is_error:
            self.total_stderr_lines += 1
        self.total_bytes += len(line) + 1  # include newline

    def _compute_logging_flag(self) -> bool:
        if self._log_output is True:
            return True
        return False if self._log_output is False else self.callback is None

    def _should_log_sample(self) -> bool:
        return bool(self._sample_lines and self._lines_logged < self._sample_lines)

    def _invoke_callback(self, event: CommandOutputEvent) -> None:
        callback = self.callback
        if callback is None:
            return
        try:
            callback(event)
            self.callback_calls += 1
        except Exception as e:
            if self.logger:
                self.logger.log(
                    "callback_error",
                    level=LogLevel.ERROR,
                    task=self.task_name,
                    error=str(e),
                )
            else:
                sys.stderr.write(f"Callback error [{self.task_name}]: {e}\n")

    def set_command_spec(self, spec: "CommandSpec | None") -> None:
        """Attach the command specification to enrich emitted events."""

        self._command_spec = spec
        if spec is None:
            self._spec_identity = None
            return
        try:
            self._spec_identity = spec.identity()
        except Exception:  # noqa: BLE001 - defensive guard around repr conversion
            self._spec_identity = None

    def process_line(self, line: str, is_error: bool = False, *, stream: str | None = None) -> None:
        """Process a single line of output."""
        if not line:
            return
        event = CommandOutputEvent(
            raw_line=line,
            is_error=is_error,
            stream=stream or ("stderr" if is_error else "stdout"),
        )
        self.process_event(event)

    def process_event(self, event: CommandOutputEvent) -> None:
        """Process a structured command output event."""
        stream = event.stream or ("stderr" if event.is_error else "stdout")
        sequence: int | None = None
        raw_line = event.raw_line
        if raw_line:
            with self._stats_lock:
                if not self._first_data_received:
                    self._first_data_received = True
                    if self.logger:
                        self.logger.log(
                            "first_data_received",
                            level=LogLevel.DEBUG,
                            task=self.task_name,
                            stream=stream,
                        )
                self._buffer_line(raw_line, event.is_error)
                self._update_stats(raw_line, event.is_error)
                sequence = self.total_lines
        elif event.records:
            with self._stats_lock:
                if not self._first_data_received:
                    self._first_data_received = True
                    if self.logger:
                        self.logger.log(
                            "first_data_received",
                            level=LogLevel.DEBUG,
                            task=self.task_name,
                            stream=stream,
                        )
                sequence = self.total_lines

        self._attach_metadata(event, stream, sequence)

        if self.callback:
            self._increase_pending_callbacks()
            try:
                self._invoke_callback(event)
            finally:
                self._decrease_pending_callbacks()

    def _attach_metadata(
        self,
        event: CommandOutputEvent,
        stream: str,
        sequence: int | None,
    ) -> None:
        metadata = dict(event.metadata or {})
        metadata.setdefault("task_name", self.task_name)
        metadata.setdefault("stream", stream)
        metadata.setdefault("timestamp", time.time())
        metadata.setdefault("lifecycle_status", "running")
        if sequence is not None:
            metadata.setdefault("sequence", sequence)
        spec = self._command_spec
        if spec is not None:
            metadata.setdefault("command_name", spec.command_name)
            metadata.setdefault("command_task", spec.task_name)
        if self._spec_identity is not None:
            metadata.setdefault("command_spec_identity", self._spec_identity)
        event.metadata = metadata

    def get_stdout(self) -> str:
        """Get accumulated stdout."""
        with self._stats_lock:
            return self.stdout_buffer.getvalue()

    def get_stderr(self) -> str:
        """Get accumulated stderr."""
        with self._stats_lock:
            return self.stderr_buffer.getvalue()

    def get_event_count(self) -> int:
        """Get number of events produced by parser (if callback has tracking)."""
        if self.callback:
            counter = getattr(self.callback, "get_event_count", None)
            if callable(counter):
                result = counter()
                if isinstance(result, int):
                    return result
        return 0

    def is_data_expected(self) -> bool:
        """Check if data output was expected (parser + schema configured)."""
        if self.callback:
            expected = getattr(self.callback, "data_expected", None)
            if isinstance(expected, bool):
                return expected
        return False

    def snapshot_parser_state(self) -> dict[str, Any]:
        """Return a threadsafe snapshot of parser-facing stats."""
        with self._stats_lock:
            stdout_lines = self.total_lines - self.total_stderr_lines
            stderr_lines = self.total_stderr_lines
            total_bytes = self.total_bytes
        return {
            "stdout_lines": stdout_lines,
            "stderr_lines": stderr_lines,
            "total_bytes": total_bytes,
            "event_count": self.get_event_count(),
            "data_expected": self.is_data_expected(),
        }

    def stop(self):
        """Signal to stop streaming."""
        self._stop_event.set()

    def should_stop(self) -> bool:
        """Check if streaming should stop."""
        return self._stop_event.is_set()

    def wait_for_completion(self, timeout: float | None = None) -> bool:
        """Block until all pending callback work completes."""
        with self._callback_condition:
            if self._pending_callbacks == 0:
                return True

            deadline = None if timeout is None else time.monotonic() + timeout
            while self._pending_callbacks > 0:
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    return False
                self._callback_condition.wait(timeout=remaining)
            return True

    def flush_callbacks(self) -> None:
        """Force-flush buffered pipeline callbacks when supported."""
        if not self.callback:
            return
        flush = getattr(self.callback, "flush", None)
        if not callable(flush):
            return
        flush()

    def _increase_pending_callbacks(self) -> None:
        with self._callback_condition:
            self._pending_callbacks += 1

    def _decrease_pending_callbacks(self) -> None:
        with self._callback_condition:
            self._pending_callbacks -= 1
            if self._pending_callbacks == 0:
                self._callback_condition.notify_all()
