from __future__ import annotations

"""Remote command execution helpers for ExecutionContext."""

import base64
import io
import re
import time
from typing import TYPE_CHECKING, Any

from hil_testbench.run.exceptions import ConfigurationError, ExecutionError
from hil_testbench.run.execution.command_types import CommandInput, stringify_command
from hil_testbench.run.logging.task_logger import LogLevel
from hil_testbench.utils.runtime_deps import get_paramiko

# TODO (EXEC-SSH): Replace any existing wrapper with a universal setsid wrapper:
#   setsid sh -c 'echo $$; trap "kill -- -$$" TERM INT HUP; exec <cmd...>'
#
# Steps for implementation:
# 1. Construct final remote command string using the wrapper above.
# 2. Request a PTY only when CommandSpec.use_pty is explicitly True.
# 3. After channel creation: read the first line of stdout as the PID.
# 4. Add a ProcessStateStore entry via state_store.add_remote(...).
#
# Remove all tool-specific special cases (no iperf version checks, no script -q).
from .command_hash import short_command_hash

SSH_MAX_RETRIES = 3
SSH_RETRY_DELAY_SECONDS = 1.0

PID_MAX_PREFETCH_LINES = 50
PID_MAX_PREFETCH_BYTES = 8192
PID_CONTEXT_PREVIEW_LINES = 5

_ANSI_CSI_PATTERN = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_ANSI_OSC_PATTERN = re.compile(r"\x1B\][^\x07]*(?:\x07|\x1B\\)", re.DOTALL)
_CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x1F\x7F]")
_PID_NUMBER_PATTERN = re.compile(r"(?:__PID__=)?\b(\d{2,})\b")
_LINE_BREAK_PATTERN = re.compile(r"(?:\r\n|\r|\n)")


def _ssh_exception_types(*, strict: bool = False) -> tuple[type[Exception], ...]:
    paramiko = get_paramiko()
    if paramiko is None:
        if strict:
            raise ConfigurationError(
                "Remote execution requires 'paramiko>=3.0.0'.",
                context={
                    "action": "pip install 'paramiko>=3.0.0'",
                },
            )
        return ()
    ssh_exception = getattr(paramiko, "SSHException", None)
    if isinstance(ssh_exception, type) and issubclass(ssh_exception, Exception):
        return (ssh_exception,)
    return ()


if TYPE_CHECKING:
    from .execution_context import ExecutionContext
else:  # pragma: no cover - runtime fallback for type-checking imports
    ExecutionContext = Any


class RemoteExecutionStrategy:
    """Execute commands over SSH with PID tracking and streaming output."""

    _CONTEXT_ATTRS = {"_channel", "_remote_pid"}
    _remote_pid: int | None

    def __init__(self, ctx: ExecutionContext) -> None:
        object.__setattr__(self, "_ctx", ctx)
        self._remote_pty_active = False

    def __getattr__(self, item: str) -> Any:
        return getattr(self._ctx, item)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._CONTEXT_ATTRS:
            setattr(self._ctx, name, value)
        else:
            object.__setattr__(self, name, value)

    def run(self, command: CommandInput, immediate_mode: bool = False, **_kwargs) -> int:
        return self._run_remote(command, immediate_mode=immediate_mode, **_kwargs)

    def _run_remote(self, command: CommandInput, immediate_mode: bool = False, **_kwargs) -> int:
        command_repr = self._stringify_command(command)
        host_info = self._current_host_info()
        self._logger.log(
            "shell_command_started",
            LogLevel.DEBUG,
            message=f"Executing remote command: {command_repr}",
            task=self.task_name,
            show_fields_with_message=False,
            host=host_info,
            command=command_repr,
        )

        self._remote_pty_active = False
        handled_exceptions: tuple[type[BaseException], ...] = (OSError,) + _ssh_exception_types(
            strict=True
        )
        try:
            stdout, stderr, start_time, pid_line, pid_context, prefetched_stderr = (
                self._start_remote_command(command_repr)
            )
            self._replay_prefetched_stderr(prefetched_stderr)
            self._record_remote_pid(pid_line, command_repr, start_time, pid_context)
            if immediate_mode:
                return self._run_remote_immediate(stdout, stderr, start_time)
            return self._run_remote_streaming(stdout, stderr, start_time)
        except handled_exceptions as exc:
            if self.streamer:
                self.streamer.process_line(
                    f"Error executing command: {exc}",
                    True,
                    stream="stderr",
                )
            raise ExecutionError(
                (
                    f"Task '{self.task_name}' command '{command_repr}' on host {host_info} failed to start remotely: {exc}. "
                    "Verify SSH connectivity and credentials, then rerun the command."
                ),
                context={
                    "task": self.task_name,
                    "command": command_repr,
                    "host": host_info,
                    "remote": True,
                },
            ) from exc

    def _stringify_command(self, command: CommandInput) -> str:
        try:
            return stringify_command(command)
        except ValueError as exc:  # pragma: no cover - validated upstream
            raise ExecutionError(
                "Command sequences cannot be empty",
                context={"task": self.task_name},
            ) from exc

    def _run_remote_immediate(
        self,
        stdout: Any,
        stderr: Any,
        start_time: float,
    ) -> int:
        stdout_data = _decode_stream_data(stdout.read())
        stderr_data = _decode_stream_data(stderr.read())

        if self.streamer:
            for line in stdout_data.splitlines():
                self.streamer.stdout_buffer.write(line + "\n")
            for line in stderr_data.splitlines():
                self.streamer.stderr_buffer.write(line + "\n")

        exit_code = stdout.channel.recv_exit_status()
        duration = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.DEBUG,
            message="Finished",
            task=self.task_name,
            show_fields_with_message=True,
            exit_code=exit_code,
            duration=f"{duration:.2f}s",
            _remote=True,
            _pid=self._remote_pid,
            _immediate=True,
        )
        self._maybe_track_remote_end()
        return exit_code

    def _run_remote_streaming(
        self,
        stdout: Any,
        stderr: Any,
        start_time: float,
    ) -> int:
        self._stream_remote_channel(stdout, stderr)
        self._settle_remote_stream_callbacks()
        exit_code = stdout.channel.recv_exit_status()
        self._logger.log(
            "remote_process_terminated",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=self._remote_pid,
            _exit_code=exit_code,
        )

        duration = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.DEBUG,
            message="Finished",
            task=self.task_name,
            show_fields_with_message=True,
            exit_code=exit_code,
            duration=f"{duration:.2f}s",
            _remote=True,
            _pid=self._remote_pid,
        )
        self._maybe_track_remote_end()
        return exit_code

    def _exec_remote_command(self, command: str, *, get_pty: bool) -> tuple[Any, Any, Any]:
        if self.ssh_client is None:
            raise ConfigurationError(
                "SSH client not initialized",
                context={"task": self.task_name, "command": command},
            )

        last_error: BaseException | None = None
        host_info = self._current_host_info()
        handled_exceptions: tuple[type[BaseException], ...] = (OSError,) + _ssh_exception_types(
            strict=True
        )

        for attempt in range(1, SSH_MAX_RETRIES + 1):
            try:
                stdin, stdout, stderr = self.ssh_client.exec_command(command, get_pty=get_pty)
                if get_pty:
                    # Combine stderr into stdout when using PTY for single-channel streaming
                    channel = stdout.channel
                    channel.set_combine_stderr(True)
                    stderr = stdout
                    self._logger.log(
                        "pty_allocated",
                        LogLevel.DEBUG,
                        task=self.task_name,
                        message="PTY allocated for remote command",
                    )
                return stdin, stdout, stderr
            except handled_exceptions as exc:
                last_error = exc
                self._logger.log(
                    "ssh_exec_retry",
                    LogLevel.WARNING,
                    task=self.task_name,
                    message=(
                        f"Task '{self.task_name}' command '{command}' on host {host_info} "
                        f"failed to start over SSH (attempt {attempt}/{SSH_MAX_RETRIES}). "
                        "Verify network access, SSH credentials, and remote shell availability before rerunning."
                    ),
                    _attempt=attempt,
                    _max_attempts=SSH_MAX_RETRIES,
                    error=str(last_error),
                    host=host_info,
                    command=command,
                    error_type=type(last_error).__name__ if last_error else None,
                )
                if attempt == SSH_MAX_RETRIES:
                    break
                time.sleep(SSH_RETRY_DELAY_SECONDS)
                continue

        assert last_error is not None
        raise last_error

    def _start_remote_command(
        self, command: str
    ) -> tuple[Any, Any, float, str, list[str], list[str]]:
        use_wrapper = getattr(self, "shell_wrapper_mode", "on") == "on"

        # Always wrap remote commands to emit PID per IPERF-REQ-002
        # When shell_wrapper_mode="off", use minimal wrapper (just PID, no trap/exec)
        # When shell_wrapper_mode="on", use full setsid wrapper with trap/exec
        if not use_wrapper:
            # Minimal wrapper: emit PID, then run command as-is (command may have script wrapper)
            wrapped_command = self._wrap_minimal_pid(command)
        else:
            wrapped_command = self._wrap_remote_command(command)

        start_time = time.time()
        use_pty = bool(getattr(self, "use_pty", False))
        _, stdout, stderr = self._exec_remote_command(wrapped_command, get_pty=use_pty)
        self._channel = stdout.channel
        self._remote_pty_active = use_pty
        self._logger.log(
            "remote_channel_created",
            LogLevel.DEBUG,
            task=self.task_name,
            _command=command[:100],
        )
        # Prefer STDERR for PID preamble when not using a PTY; fall back to STDOUT once.
        pid_context: list[str] = []
        prefetched_stderr: list[str] = []
        pid_text = ""
        if not use_pty:
            # Attempt to extract the PID line from stderr first (our wrapper prints there).
            pid_text, stderr, pid_context, prefetched_stderr = self._extract_pid_line(stderr)
            if not pid_text:
                # Without PTY: use buffered readline (safe since we'll read from stderr anyway)
                pid_raw = stdout.readline()
                pid_text, _ = _normalize_pid_line(pid_raw)
        # When PTY is enabled, DON'T read PID here - let it come through the streaming loop
        # This avoids triggering ChannelFile buffering which blocks live streaming
        # PID will be extracted from the first line in _stream_remote_channel
        return stdout, stderr, start_time, pid_text, pid_context, prefetched_stderr

    def _record_remote_pid(
        self,
        pid_line: str,
        command: str,
        start_time: float,
        pid_context: list[str] | None = None,
    ) -> None:
        try:
            parsed_pid = _parse_pid_number(pid_line)
            self._remote_pid = parsed_pid
        except (ValueError, TypeError):
            self._remote_pid = None
            # Only warn if not using PTY (PTY mode extracts PID from stream lazily)
            if not self._remote_pty_active:
                preview = " | ".join(pid_context or [])
                host_info = self._current_host_info()
                self._logger.log(
                    "remote_pid_missing",
                    LogLevel.WARNING,
                    task=self.task_name,
                    message=(
                        f"Task '{self.task_name}' command '{command}' on host {host_info} did not report a PID. "
                        "Ensure the remote shell echoes PID on stderr before command output (setsid shim)."
                    ),
                    _raw_line=pid_line,
                    _prefetch_preview=preview,
                    host=host_info,
                    command=command,
                )
            return

        if self._remote_pid is None:
            # Only warn if not using PTY
            if not self._remote_pty_active:
                preview = " | ".join(pid_context or [])
                host_info = self._current_host_info()
                self._logger.log(
                    "remote_pid_missing",
                    LogLevel.WARNING,
                    task=self.task_name,
                    message=(
                        f"Task '{self.task_name}' command '{command}' on host {host_info} did not report a PID. "
                        "Ensure the remote shell echoes PID on stderr before command output (setsid shim)."
                    ),
                    _raw_line=pid_line,
                    _prefetch_preview=preview,
                    host=host_info,
                    command=command,
                )
            return

        self._logger.log(
            "remote_pid_captured",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=self._remote_pid,
        )
        self._register_remote_process_group(self._remote_pid)

        host_info, username, port = self._transport_metadata()
        command_hash = short_command_hash(command)
        spec_identity = None
        if self.command_spec:
            try:
                spec_identity = self.command_spec.identity()
            except Exception:  # noqa: BLE001 - defensive guard around repr conversion
                spec_identity = None
        self._process_tracker.track_start(
            command_name=self.task_name,
            pid=self._remote_pid,
            create_time=start_time,
            command_hash=command_hash,
            host=host_info,
            port=port or 22,
            username=username,
            spec_identity=spec_identity,
        )

    def _require_ssh_client(self):
        if self.ssh_client is None:
            raise ConfigurationError(
                "SSH client is not initialized for remote execution",
                context={"task": self.task_name},
            )
        return self.ssh_client

    def _read_first_line_from_channel(self, channel: Any, timeout: float = 5.0) -> bytes:
        """Read first line from SSH channel without using buffered ChannelFile.

        This prevents readline() from buffering excess data and blocking live streaming.
        Reads byte-by-byte from the channel until newline, with timeout.
        """
        line = b""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if channel.recv_ready():
                byte = channel.recv(1)
                if not byte:
                    break
                line += byte
                if byte in (b"\n", b"\r"):
                    # Read one more byte if it's \r\n
                    if byte == b"\r" and channel.recv_ready():
                        next_byte = channel.recv(1)
                        if next_byte == b"\n":
                            line += next_byte
                    break
            else:
                time.sleep(0.01)  # Small sleep to avoid busy-waiting
        return line

    def _get_remote_os(self) -> str:
        """Get the remote OS type from the execution context."""
        return getattr(self._ctx, "remote_os", "unix")

    def _wrap_minimal_pid(self, command: str) -> str:
        """Minimal wrapper that only emits PID, then runs command as-is.

        Used when shell_wrapper_mode="off" (e.g., with script wrapper).
        The command is assumed to already have any necessary wrappers (script, etc.).
        """
        escaped_command = command.replace("'", "'\"'\"'")
        # Emit PID on stdout, then run the command directly (no setsid, trap, or exec)
        return f"sh -c 'echo $$; {escaped_command}'"

    def _wrap_remote_command(self, command: str) -> str:
        """Wrap command with PID capture for remote execution."""
        remote_os = self._get_remote_os()

        if remote_os == "windows":
            return self._wrap_windows_command(command)

        return self._wrap_unix_command(command)

    def _wrap_unix_command(self, command: str) -> str:
        """Wrap command for Unix/Linux sh-based systems with PID capture."""
        # Emit PID on stdout first, set trap to forward signals to the group, then exec/run the command.
        # Escape any embedded single quotes so the user command survives the single-quoted sh -c wrapper.
        escaped_command = command.replace("'", "'\"'\"'")

        # For compound commands (containing ;, |, &, etc.), don't use exec - just run directly
        # because exec can only exec a single command, not a shell script
        if any(char in command for char in [";", "|", "&", "&&", "||", "\n"]):
            return f"setsid sh -c 'echo $$; trap \"kill -- -$$\" TERM INT HUP; {escaped_command}'"

        # For simple commands, use exec to replace the shell (cleaner process tree)
        return f"setsid sh -c 'echo $$; trap \"kill -- -$$\" TERM INT HUP; exec {escaped_command}'"

    def _wrap_windows_command(self, command: str) -> str:
        """Wrap command for Windows PowerShell with PID capture.

        Uses Base64-encoded command (-EncodedCommand) for safe execution,
        avoiding complex escaping issues with special characters.
        """
        # Build PowerShell script that outputs PID to stderr then runs command
        # [Console]::Error.WriteLine writes directly to stderr stream
        ps_script = f"[Console]::Error.WriteLine($PID); {command}"

        # PowerShell -EncodedCommand expects UTF-16LE Base64
        encoded = base64.b64encode(ps_script.encode("utf-16-le")).decode("ascii")

        return f"powershell -NoProfile -EncodedCommand {encoded}"

    def _current_host_info(self) -> str:
        host, _, _ = self._transport_metadata()
        return host or "unknown"

    def _transport_metadata(self) -> tuple[str | None, str | None, int | None]:
        if self.ssh_client is None:
            return None, None, None
        transport = self.ssh_client.get_transport()
        if not transport:
            return None, None, None
        host = None
        username = None
        port = None
        try:
            peer = transport.getpeername()
            host = peer[0] if peer else None
            if peer and len(peer) > 1:
                port = peer[1]
        except Exception:  # noqa: BLE001
            host = None
        try:
            username = transport.get_username()
        except Exception:  # noqa: BLE001
            username = None
        return host, username, port

    def _stream_remote_channel(self, stdout: Any, stderr: Any) -> None:
        # stdout/stderr may be the same channel when set_combine_stderr(True)
        channel = stdout.channel if hasattr(stdout, "channel") else stdout
        combined = stdout is stderr
        stdout_buffer = ""
        stderr_buffer = ""

        while not channel.exit_status_ready() and not self._remote_cancel_requested():
            ready = channel.recv_ready()
            if ready:
                stdout_buffer = self._drain_remote_buffer(
                    channel.recv_ready,
                    lambda: channel.recv(4096),
                    stdout_buffer,
                    is_error=False,
                )
            if (
                not combined
                and hasattr(channel, "recv_stderr_ready")
                and channel.recv_stderr_ready()
            ):
                stderr_buffer = self._drain_remote_buffer(
                    channel.recv_stderr_ready,
                    lambda: channel.recv_stderr(4096),
                    stderr_buffer,
                    is_error=True,
                )
            if not ready and not getattr(channel, "recv_stderr_ready", lambda: False)():
                time.sleep(0.05)

        self._flush_remote_buffer(stdout_buffer, is_error=False)
        self._flush_remote_buffer(stderr_buffer, is_error=True)
        self._drain_remaining_stream(stdout, is_error=False)
        if not combined and stdout is not stderr:
            self._drain_remaining_stream(stderr, is_error=True)

    def _drain_remote_buffer(
        self,
        ready_fn,
        read_fn,
        buffer: str,
        *,
        is_error: bool,
    ) -> str:
        if ready_fn():
            data = _decode_stream_data(read_fn())
            buffer += data
            buffer = self._emit_stream_lines(buffer, is_error)
        return buffer

    def _emit_stream_lines(self, buffer: str, is_error: bool) -> str:
        parts = _LINE_BREAK_PATTERN.split(buffer)
        for line in parts[:-1]:
            self._process_remote_line(line, is_error)
        return parts[-1]

    def _process_remote_line(self, line: str, is_error: bool) -> None:
        # When PTY is active and PID not yet captured, first line is the PID from wrapper
        if self._remote_pty_active and self._remote_pid is None and not is_error and line:
            maybe_pid = _parse_pid_number(line)
            if maybe_pid is not None:
                self._remote_pid = maybe_pid
                self._logger.log(
                    "remote_pid_captured",
                    LogLevel.DEBUG,
                    task=self.task_name,
                    message=f"Remote process PID: {self._remote_pid}",
                    _pid=self._remote_pid,
                )
                return  # Don't pass PID line to streamer/parser

        if self.streamer and line:
            stream_name = "stderr" if is_error else "stdout"
            self.streamer.process_line(line, is_error, stream=stream_name)

    def _flush_remote_buffer(self, buffer: str, *, is_error: bool) -> None:
        if not buffer:
            return
        for line in buffer.splitlines():
            self._process_remote_line(line, is_error)

    def _drain_remaining_stream(self, stream: Any, *, is_error: bool) -> None:
        remaining = _decode_stream_data(stream.read())
        for line in remaining.splitlines():
            self._process_remote_line(line, is_error)

    def _remote_cancel_requested(self) -> bool:
        return bool(self.cancel_event and self.cancel_event.is_set())

    def _settle_remote_stream_callbacks(self) -> None:
        self._wait_for_stream_callbacks("remote_streaming")
        self._flush_stream_callbacks("remote_streaming")

    def _maybe_track_remote_end(self) -> None:
        if self._remote_pid is None:
            return
        self._enforce_remote_exit()
        self._process_tracker.track_end(self.task_name)

    def _enforce_remote_exit(self) -> None:
        if self._remote_pid is None or self.ssh_client is None:
            return
        pid = self._remote_pid
        if not self._remote_probe(pid):
            return
        self._logger.log(
            "remote_process_still_running",
            LogLevel.WARNING,
            task=self.task_name,
            _pid=pid,
        )
        self._remote_signal(pid, "TERM")
        time.sleep(0.5)
        if not self._remote_probe(pid):
            self._logger.log(
                "remote_process_killed",
                LogLevel.DEBUG,
                task=self.task_name,
                _pid=pid,
                _signal="TERM",
            )
            return
        self._remote_signal(pid, "KILL")
        time.sleep(0.2)
        if not self._remote_probe(pid):
            self._logger.log(
                "remote_process_killed",
                LogLevel.DEBUG,
                task=self.task_name,
                _pid=pid,
                _signal="KILL",
            )
        else:
            self._logger.log(
                "remote_process_kill_failed",
                LogLevel.WARNING,
                task=self.task_name,
                _pid=pid,
            )

    def _remote_probe(self, pid: int) -> bool:
        try:
            _, stdout, _ = self.ssh_client.exec_command(f"kill -0 -- -{pid} 2>/dev/null || exit 1")
            exit_code = stdout.channel.recv_exit_status()
            return exit_code == 0
        except Exception:  # noqa: BLE001
            return False

    def _remote_signal(self, pid: int, signal_name: str) -> None:
        try:
            self.ssh_client.exec_command(f"kill -{signal_name} -- -{pid} 2>/dev/null || true")
        except Exception:  # noqa: BLE001
            self._logger.log(
                "remote_signal_failed",
                LogLevel.WARNING,
                task=self.task_name,
                _pid=pid,
                _signal=signal_name,
            )

    def _extract_pid_line(self, stderr: Any) -> tuple[str, Any, list[str], list[str]]:
        if getattr(self, "_remote_pty_active", False):
            return "", stderr, [], []
        prefetched: list[bytes] = []
        prefetched_lines: list[str] = []
        context_preview: list[str] = []
        pid_text = ""
        consumed_bytes = 0

        for _ in range(PID_MAX_PREFETCH_LINES):
            raw_line = stderr.readline()
            if not raw_line:
                break

            decoded, normalized = _normalize_pid_line(raw_line)
            consumed_bytes += len(normalized)
            cleaned = _clean_pid_candidate(decoded)
            maybe_pid = _parse_pid_number(cleaned)

            if maybe_pid is not None:
                pid_text = str(maybe_pid)
                break

            prefetched.append(normalized)
            if decoded:
                prefetched_lines.append(decoded)
            if len(context_preview) < PID_CONTEXT_PREVIEW_LINES:
                context_preview.append(decoded[:120])

            if consumed_bytes >= PID_MAX_PREFETCH_BYTES:
                break

        wrapped_stderr = _PrefetchedChannelFile(prefetched, stderr) if prefetched else stderr
        return pid_text, wrapped_stderr, context_preview, prefetched_lines

    def _replay_prefetched_stderr(self, prefetched_lines: list[str]) -> None:
        if not prefetched_lines:
            return
        for line in prefetched_lines:
            self._process_remote_line(line, True)


def _clean_pid_candidate(text: str) -> str:
    """Remove ANSI/OSC sequences and control chars before PID detection."""

    without_osc = _ANSI_OSC_PATTERN.sub("", text)
    without_csi = _ANSI_CSI_PATTERN.sub("", without_osc)
    without_control = _CONTROL_CHAR_PATTERN.sub("", without_csi)
    cleaned = without_control.strip()
    if cleaned.startswith("__PID__="):
        return cleaned.split("=", 1)[-1].strip()
    return cleaned


def _parse_pid_number(text: str | bytes | None) -> int | None:
    """Extract the first numeric PID from text, handling __PID__= hints."""

    if text is None:
        return None
    decoded = (
        text.decode("utf-8", errors="replace")
        if isinstance(text, (bytes, bytearray))
        else str(text)
    )
    match = _PID_NUMBER_PATTERN.search(decoded)
    if not match:
        return None
    value = int(match.group(1))
    if value <= 1:
        return None
    return value


def _normalize_pid_line(raw_line: Any) -> tuple[str, bytes]:
    normalized_bytes = _ensure_bytes(raw_line)
    decoded = normalized_bytes.decode("utf-8", errors="replace").rstrip("\r\n")
    return decoded, normalized_bytes


class _PrefetchedChannelFile:
    """Wrap Paramiko channel file to replay prefetched bytes before live reads."""

    def __init__(self, prefetched: list[bytes], stream: Any) -> None:
        self._buffer = io.BytesIO(b"".join(prefetched))
        self._stream = stream

    def read(self, size: int | None = None) -> bytes:
        prefetched = self._buffer.read(size) or b""
        if size is None or (isinstance(size, int) and size < 0):
            return prefetched + _ensure_bytes(self._stream.read())
        if len(prefetched) >= size:
            return prefetched[:size]
        remainder = _ensure_bytes(self._stream.read(size - len(prefetched)))
        return prefetched + remainder

    def readline(self, size: int | None = None) -> bytes:
        data = self._buffer.readline(size)
        if data:
            return data
        return _ensure_bytes(self._stream.readline(size))

    def __getattr__(self, item: str) -> Any:
        return getattr(self._stream, item)


def _ensure_bytes(data: Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if data is None:
        return b""
    if isinstance(data, str):
        return data.encode("utf-8", errors="replace")
    return str(data).encode("utf-8", errors="replace")


def _decode_stream_data(data: Any) -> str:
    return _ensure_bytes(data).decode("utf-8", errors="replace")
