from __future__ import annotations

"""Local command execution helpers for ExecutionContext."""

import codecs
import contextlib
import importlib
import os
import shlex
import signal
import subprocess
import sys
import time
from functools import lru_cache
from typing import TYPE_CHECKING, Any, cast

import psutil

from hil_testbench.run.exceptions import ConfigurationError, ExecutionError
from hil_testbench.run.execution.command_types import CommandInput, stringify_command
from hil_testbench.run.logging.task_logger import LogLevel

# TODO (EXEC-LOCAL): Modify Popen calls:
# - Add start_new_session=True to spawn processes in their own session/process group.
# - Use bufsize=1 and text=True for minimal buffering.
# - stdout=PIPE, stderr=PIPE must always be set.
#
# After Popen:
# - Immediately add a ProcessStateStore entry via state_store.add_local(...)
#   including pid, create_time, cmd_preview, and session_id.
#
# Long-running logic:
# - Do NOT add tool-specific wrappers (script, stdbuf, iperf detection, etc.).
# - Do NOT change behavior based on argv content.
# Behavior is based ONLY on spec.long_running and run_config flags.
from .command_hash import short_command_hash
from .stream_worker import StreamWorker

# Detect ConPTY environment early (VS Code with ConPTY enabled)
CONPTY_DETECTED = (
    os.environ.get("WT_SESSION") is not None or os.environ.get("TERM_PROGRAM") == "vscode"
)

winpty: Any | None = None
pty: Any | None = None
select: Any | None = None
PTY_AVAILABLE = False
PTY_MODE: str | None = None
EMPTY_COMMAND_MESSAGE = "Command sequences cannot be empty"


@lru_cache(maxsize=1)
def _load_pty_support() -> tuple[bool, str | None]:
    """Import PTY helpers lazily and cache the result."""

    global winpty, pty, select, PTY_AVAILABLE, PTY_MODE  # noqa: PLW0603 - module state cache

    if PTY_MODE is not None or PTY_AVAILABLE:
        return PTY_AVAILABLE, PTY_MODE

    winpty_module = _load_winpty_module()
    unix_pty_module, unix_select_module = _load_unix_modules()

    winpty = winpty_module
    pty = unix_pty_module
    select = unix_select_module

    PTY_AVAILABLE, PTY_MODE = _determine_pty_state(winpty_module, unix_pty_module)
    return PTY_AVAILABLE, PTY_MODE


def _load_winpty_module() -> Any | None:
    try:
        module = importlib.import_module("winpty")  # hil: allow-lazy
    except ImportError:
        return None

    return None if CONPTY_DETECTED else module


def _load_unix_modules() -> tuple[Any | None, Any | None]:
    if sys.platform == "win32":
        return None, None

    unix_pty_module: Any | None
    unix_select_module: Any | None
    try:
        import pty as unix_pty_module  # hil: allow-lazy
    except ImportError:
        unix_pty_module = None

    try:
        import select as unix_select_module  # hil: allow-lazy
    except ImportError:
        unix_select_module = None

    return unix_pty_module, unix_select_module


def _determine_pty_state(
    winpty_module: Any | None,
    unix_pty_module: Any | None,
) -> tuple[bool, str | None]:
    if winpty_module:
        return True, "winpty"
    if unix_pty_module:
        return True, "unix"
    return False, None


def _require_winpty_module() -> Any:
    if winpty is None:
        raise ConfigurationError("winpty module not available")
    return winpty


def _require_select_module() -> Any:
    if select is None:
        raise ConfigurationError("select module not available")
    return select


if TYPE_CHECKING:
    from .execution_context import ExecutionContext
else:  # pragma: no cover - runtime fallback for type checking only import
    ExecutionContext = Any


class LocalExecutionStrategy:
    """Execute commands locally with PTY fallback based on terminal support."""

    _CONTEXT_ATTRS = {"_process", "_pty_proc"}

    def __init__(self, ctx: ExecutionContext) -> None:
        object.__setattr__(self, "_ctx", ctx)
        self._local_strategies = self._build_local_strategies()

    def __getattr__(self, item: str) -> Any:
        return getattr(self._ctx, item)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._CONTEXT_ATTRS:
            setattr(self._ctx, name, value)
        else:
            object.__setattr__(self, name, value)

    def run(
        self,
        command: CommandInput,
        immediate_mode: bool = False,
        **_kwargs,
    ) -> int:
        return self._run_local(command, immediate_mode=immediate_mode)

    def cleanup(self) -> None:
        self._cleanup_winpty_process()

    def _build_local_strategies(self) -> list[_BaseLocalStrategy]:
        return [
            _WinPTYStrategy(self),
            _UnixPTYStrategy(self),
            _SubprocessStrategy(self),
        ]

    def _run_local(
        self,
        command: CommandInput,
        immediate_mode: bool = False,
    ) -> int:
        command_repr = self._stringify_command(command)
        self._logger.log(
            "shell_command_started",
            LogLevel.DEBUG,
            message=f"Executing local command: {command_repr}",
            task=self.task_name,
            show_fields_with_message=False,
            command=command_repr,
        )

        disable_pty = self.config.run_config.disable_pty if self.config else False

        _load_pty_support()

        last_error: Exception | None = None
        for strategy in self._local_strategies:
            if not strategy.supports(
                disable_pty=disable_pty,
                env=self._ctx._pending_env,
                cwd=self._ctx._pending_cwd,
            ):
                continue
            try:
                return strategy.run(command, immediate_mode)
            except ExecutionError:
                raise
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                error = ExecutionError(
                    "Local command execution failed",
                    context={
                        "task": self.task_name,
                        "command": command_repr,
                        "strategy": type(strategy).__name__,
                    },
                )
                raise error from exc

        error = ExecutionError(
            "No suitable local execution strategy available",
            context={"task": self.task_name, "command": command_repr},
        )
        if last_error is not None:
            raise error from last_error
        raise error

    def _stringify_command(self, command: CommandInput) -> str:
        try:
            return stringify_command(command)
        except ValueError as exc:
            raise ExecutionError(
                EMPTY_COMMAND_MESSAGE,
                context={"task": self.task_name},
            ) from exc

    def _normalize_command(self, command: str) -> str:
        # Windows cmd.exe requires double-quoted tokens; re-quote POSIX strings.
        if sys.platform != "win32" or not command:
            return command

        if "'" not in command:
            return command

        try:
            tokens = shlex.split(command, posix=True)
        except ValueError:
            return command

        return subprocess.list2cmdline(tokens) if tokens else command

    def _prepare_command_invocation(self, command: CommandInput) -> tuple[str | list[str], bool]:
        if isinstance(command, str):
            args = self._build_subprocess_args(command)
            if args is not None:
                return args, False
            return self._normalize_command(command), True

        sequence = list(command)
        if not sequence:
            raise ExecutionError(
                EMPTY_COMMAND_MESSAGE,
                context={"task": self.task_name},
            )
        return sequence, False

    def _build_subprocess_args(self, command: str) -> list[str] | None:
        if sys.platform != "win32" or not command:
            return None

        if "'" not in command and "\n" not in command:
            return None

        if any(meta in command for meta in ("|", "&", ">", "<")):
            return None

        try:
            tokens = shlex.split(command, posix=True)
        except ValueError:
            return None

        return tokens or None

    def _run_local_subprocess(self, command: CommandInput, immediate_mode: bool = False) -> int:
        command_repr = self._stringify_command(command)
        try:
            return self._execute_local_subprocess(command, command_repr, immediate_mode)
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            if self.streamer:
                self.streamer.process_line(
                    f"Error executing command: {e}",
                    True,
                    stream="stderr",
                )
            raise ExecutionError(
                (
                    f"Task '{self.task_name}' command '{command_repr}' failed to start locally: {e}. "
                    "Confirm the binary exists on this host and that your shell quoting is valid, then rerun."
                ),
                context={
                    "task": self.task_name,
                    "command": command_repr,
                    "strategy": "local_subprocess",
                    "remote": False,
                },
            ) from e

    def _execute_local_subprocess(
        self, command: CommandInput, command_repr: str, immediate_mode: bool
    ) -> int:
        start_time: float = time.time()
        env = self._build_subprocess_env()
        self._process = self._spawn_subprocess(command, env)
        self._log_subprocess_spawn(command_repr)
        create_time = self._get_process_create_time()
        self._track_subprocess_start(command_repr, create_time)

        if immediate_mode:
            return self._run_immediate_subprocess()

        stdout_worker, stderr_worker = self._start_subprocess_stream_workers()
        return_code = self._wait_for_subprocess_completion()
        self._finalize_subprocess_run(return_code, start_time, stdout_worker, stderr_worker)
        return return_code

    def _build_subprocess_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        custom_env = self._ctx._pending_env
        if custom_env:
            env.update(custom_env)
        return env

    def _spawn_subprocess(
        self, command: CommandInput, env: dict[str, str]
    ) -> subprocess.Popen[Any]:
        cmd, use_shell = self._prepare_command_invocation(command)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        popen_kwargs: dict[str, Any] = {}
        if sys.platform != "win32":
            popen_kwargs["start_new_session"] = True
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=use_shell,
            text=True,
            bufsize=1,
            env=env,
            creationflags=creationflags,
            cwd=self._ctx._pending_cwd,
            **popen_kwargs,
        )
        self._ctx._register_local_process_group(process.pid)
        return process

    def _log_subprocess_spawn(self, command: str) -> None:
        self._logger.log(
            "process_spawned",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=self._process.pid,
            _command=command[:100],
            _mode="local_subprocess",
        )

    def _get_process_create_time(self) -> float:
        try:
            proc = psutil.Process(self._process.pid)
            return proc.create_time()
        except Exception:  # pylint: disable=broad-except
            return time.time()

    def _track_subprocess_start(self, command: str, create_time: float) -> None:
        command_hash = short_command_hash(command)
        spec_identity = None
        if self.command_spec:
            try:
                spec_identity = self.command_spec.identity()
            except Exception:  # noqa: BLE001 - defensive guard around repr conversion
                spec_identity = None
        self._process_tracker.track_start(
            command_name=self.task_name,
            pid=self._process.pid,
            create_time=create_time,
            command_hash=command_hash,
            host=None,
            spec_identity=spec_identity,
        )

    def _run_immediate_subprocess(self) -> int:
        stdout_raw, stderr_raw = self._process.communicate()
        stdout_data = cast(str, stdout_raw)
        stderr_data = cast(str, stderr_raw)
        if self.streamer:
            for line in stdout_data.splitlines():
                self.streamer.stdout_buffer.write(f"{line}\n")
            for line in stderr_data.splitlines():
                self.streamer.stderr_buffer.write(f"{line}\n")
        return self._process.returncode

    def _start_subprocess_stream_workers(self) -> tuple[StreamWorker, StreamWorker]:
        assert self._process.stdout is not None
        assert self._process.stderr is not None

        stdout_worker = self._create_stream_worker(
            pipe=self._process.stdout,
            suffix="stdout",
            purpose="stdout streaming",
            is_error=False,
        )
        stderr_worker = self._create_stream_worker(
            pipe=self._process.stderr,
            suffix="stderr",
            purpose="stderr streaming",
            is_error=True,
        )
        return stdout_worker, stderr_worker

    def _create_stream_worker(
        self,
        *,
        pipe: Any,
        suffix: str,
        purpose: str,
        is_error: bool,
    ) -> StreamWorker:
        def _strip_line(line: str) -> str:
            return line.rstrip()

        iterator_factory = self._build_pipe_iterator(pipe)

        return StreamWorker(
            name=f"{self.task_name}_{suffix}",
            line_iterator_factory=iterator_factory,
            streamer=self.streamer,
            logger=self._logger,
            task_name=self.task_name,
            mode="local_subprocess",
            purpose=purpose,
            is_error=is_error,
            transform=_strip_line,
            stop_event=self.cancel_event,
        ).start()

    def _build_pipe_iterator(self, pipe: Any):
        buffer = getattr(pipe, "buffer", None)
        raw = getattr(buffer, "raw", None)
        reader = raw or buffer or pipe
        encoding = getattr(pipe, "encoding", "utf-8") or "utf-8"
        fd = self._safe_fileno(reader)
        if fd is not None:
            self._set_nonblocking_fd(fd)

        def _read_chunk() -> bytes | str | None:
            read1 = getattr(reader, "read1", None)
            if callable(read1):
                return cast(bytes | str | None, read1(4096))
            read_method = getattr(reader, "read", None)
            if callable(read_method):
                return cast(bytes | str | None, read_method(4096))
            return None

        def _iterator(cancel_event=None, poll_interval: float = 0.1):
            decoder = None
            text_buffer = ""
            while True:
                if cancel_event and cancel_event.is_set():
                    break
                try:
                    chunk = _read_chunk()
                except BlockingIOError:
                    if self._wait_for_cancel(cancel_event, poll_interval):
                        break
                    continue
                except OSError:
                    break

                if chunk is None:
                    if self._wait_for_cancel(cancel_event, poll_interval):
                        break
                    continue

                if chunk in {b"", ""}:
                    if self._process_finished():
                        break
                    if self._wait_for_cancel(cancel_event, poll_interval):
                        break
                    continue

                if isinstance(chunk, bytes):
                    if decoder is None:
                        decoder = codecs.getincrementaldecoder(encoding)(errors="replace")
                    text_buffer += decoder.decode(chunk)
                else:
                    text_buffer += chunk

                while "\n" in text_buffer:
                    line, text_buffer = text_buffer.split("\n", 1)
                    yield line

            if decoder is not None:
                remainder = decoder.decode(b"", final=True)
                if remainder:
                    text_buffer += remainder
            if text_buffer:
                yield text_buffer

        return _iterator

    @staticmethod
    def _safe_fileno(stream: Any) -> int | None:
        fileno = getattr(stream, "fileno", None)
        if not callable(fileno):
            return None
        try:
            return cast(int, fileno())
        except (OSError, ValueError):
            return None

    @staticmethod
    def _set_nonblocking_fd(fd: int) -> None:
        try:
            os.set_blocking(fd, False)
        except (AttributeError, OSError, ValueError):
            pass

    @staticmethod
    def _wait_for_cancel(cancel_event, timeout: float) -> bool:
        if cancel_event:
            return bool(cancel_event.wait(timeout))
        time.sleep(timeout)
        return False

    def _wait_for_subprocess_completion(self) -> int:
        while True:
            try:
                return self._process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                if self._shutdown_requested():
                    self._handle_shutdown_signal()

    def _shutdown_requested(self) -> bool:
        shutdown_file = os.path.join(self.execution_dir, "shutdown.signal")
        return os.path.exists(shutdown_file)

    def _handle_shutdown_signal(self) -> None:
        shutdown_file = os.path.join(self.execution_dir, "shutdown.signal")
        self._logger.log_shutdown_signal(
            shutdown_file=shutdown_file,
            task=self.task_name,
            pid=self._process.pid,
        )
        self._terminate_subprocess()
        raise KeyboardInterrupt("Shutdown signal received during command execution") from None

    def _terminate_subprocess(self) -> None:
        if not self._process:
            return
        self._ctx._terminate_local_process_group(signal.SIGTERM)
        try:
            self._process.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            self._ctx._terminate_local_process_group(signal.SIGKILL)
            self._process.wait()

    def _finalize_subprocess_run(
        self,
        return_code: int,
        start_time: float,
        stdout_worker: StreamWorker,
        stderr_worker: StreamWorker,
    ) -> None:
        self._join_stream_workers([stdout_worker, stderr_worker], "local_subprocess")
        process = getattr(self, "_process", None)
        pid = process.pid if process else "unknown"
        self._logger.log(
            "process_terminated",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=pid,
            _exit_code=return_code,
        )
        duration: float = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.DEBUG,
            message="Finished",
            task=self.task_name,
            show_fields_with_message=True,
            exit_code=return_code,
            duration=f"{duration:.2f}s",
            _remote=False,
        )
        if return_code != 0:
            self._logger.log(
                "shell_command_exit_nonzero",
                LogLevel.DEBUG,
                task=self.task_name,
                _exit_code=return_code,
            )
        self._process_tracker.track_end(self.task_name)

    def _run_local_pty_windows(self, command: CommandInput, immediate_mode: bool = False) -> int:
        command_repr = self._stringify_command(command)
        _load_pty_support()
        if winpty is None:
            raise ConfigurationError(
                "winpty not available on this system",
                context={"task": self.task_name, "command": command_repr},
            )

        assert winpty is not None

        try:
            env = self._build_subprocess_env()
            cwd = self._ctx._pending_cwd
            self._spawn_winpty_process(
                self._format_command_for_winpty(command),
                command_repr,
                env,
                cwd,
            )
            pty_proc = getattr(self, "_pty_proc", None)
            if pty_proc and hasattr(pty_proc, "pid"):
                self._register_local_process_group(pty_proc.pid)
            if immediate_mode:
                return self._run_winpty_immediate()
            return self._run_winpty_streaming()

        except Exception as e:  # pylint: disable=broad-except
            if self.streamer:
                self.streamer.process_line(
                    f"Error executing command with PTY: {e}",
                    True,
                    stream="stderr",
                )
            raise ExecutionError(
                (
                    f"Task '{self.task_name}' command '{command_repr}' failed while running via Windows PTY: {e}. "
                    "Verify winpty is installed and the command runs in a local terminal before retrying."
                ),
                context={
                    "task": self.task_name,
                    "command": command_repr,
                    "remote": False,
                    "pty": True,
                    "pty_mode": "windows",
                },
            ) from e

    def _format_command_for_winpty(self, command: CommandInput) -> str:
        if isinstance(command, str):
            return command
        sequence = list(command)
        if not sequence:
            raise ExecutionError(
                EMPTY_COMMAND_MESSAGE,
                context={"task": self.task_name},
            )
        return subprocess.list2cmdline(sequence)

    def _spawn_winpty_process(
        self,
        command: str,
        command_repr: str,
        env: dict[str, str] | None,
        cwd: str | None,
    ) -> None:
        winpty_module = _require_winpty_module()
        spawn_kwargs: dict[str, Any] = {}
        if env:
            spawn_kwargs["env"] = env
        if cwd:
            spawn_kwargs["cwd"] = cwd
        self._pty_proc = winpty_module.PtyProcess.spawn(command, **spawn_kwargs)
        if self._pty_proc is None:
            raise ExecutionError(
                "Failed to create PTY process",
                context={"task": self.task_name, "command": command_repr},
            )
        self._logger.log(
            "process_spawned",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=getattr(self._pty_proc, "pid", "unknown"),
            _command=command_repr[:100],
            _mode="local_pty_windows",
        )

    def _run_winpty_immediate(self) -> int:
        assert self._pty_proc is not None
        start_time: float = time.time()
        output = []
        while self._pty_proc.isalive():
            try:
                if line := self._pty_proc.readline():
                    output.append(line.rstrip("\r\n"))
            except EOFError:
                break

        if self.streamer:
            for line in output:
                self.streamer.stdout_buffer.write(line + "\n")

        self._pty_proc.wait()
        exit_code = self._pty_proc.exitstatus or 0
        duration: float = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.INFO,
            task=self.task_name,
            message=f"PTY command finished (exit {exit_code}) in {duration:.2f}s",
            exit_code=exit_code,
            _duration=f"{duration:.2f}",
            _remote=False,
            _pty=True,
        )
        return exit_code

    def _run_winpty_streaming(self) -> int:
        assert self._pty_proc is not None

        def winpty_line_iterator(cancel_event=None, poll_interval: float = 0.1):
            while self._pty_proc and self._pty_proc.isalive():
                if cancel_event and cancel_event.is_set():
                    break
                try:
                    line = self._pty_proc.readline()
                except EOFError:
                    break
                if not line:
                    if self._wait_for_cancel(cancel_event, poll_interval):
                        break
                    continue
                yield line

        output_worker = StreamWorker(
            name=f"{self.task_name}_pty_output",
            line_iterator_factory=winpty_line_iterator,
            streamer=self.streamer,
            logger=self._logger,
            task_name=self.task_name,
            mode="local_pty_windows_streaming",
            purpose="PTY output streaming",
            transform=lambda line: line.rstrip("\r\n"),
            stop_event=self.cancel_event,
        ).start()

        start_time = time.time()
        self._pty_proc.wait()

        self._join_stream_workers([output_worker], "local_pty_windows")
        exit_code = self._pty_proc.exitstatus or 0
        self._logger.log(
            "process_terminated",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=getattr(self._pty_proc, "pid", "unknown"),
            _exit_code=exit_code,
        )
        duration = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.INFO,
            task=self.task_name,
            message=f"PTY command finished (exit {exit_code}) in {duration:.2f}s",
            exit_code=exit_code,
            _duration=f"{duration:.2f}",
            _remote=False,
            _pty=True,
        )
        return exit_code

    def _run_local_pty_unix(self, command: CommandInput, immediate_mode: bool = False) -> int:
        command_repr = self._stringify_command(command)
        _load_pty_support()
        if pty is None:
            return self._run_local_subprocess(command, immediate_mode)

        if select is None:
            return self._run_local_subprocess(command, immediate_mode)

        assert pty is not None
        assert select is not None

        master_fd: int | None = None
        slave_fd: int | None = None

        try:
            master_fd, slave_fd = pty.openpty()
            self._spawn_unix_pty_process(command, command_repr, slave_fd)
            slave_fd = None

            if immediate_mode:
                return self._run_unix_pty_immediate(master_fd)
            return self._run_unix_pty_streaming(master_fd)

        except (OSError, ValueError) as e:
            if self.streamer:
                self.streamer.process_line(
                    f"Error executing command with Unix PTY: {e}",
                    True,
                    stream="stderr",
                )
            raise ExecutionError(
                (
                    f"Task '{self.task_name}' command '{command_repr}' failed while running via Unix PTY: {e}. "
                    "Check shell permissions/TTY settings and rerun without --disable-pty if needed."
                ),
                context={
                    "task": self.task_name,
                    "command": command_repr,
                    "remote": False,
                    "pty": True,
                    "pty_mode": "unix",
                },
            ) from e
        finally:
            self._close_fd(slave_fd)
            self._close_fd(master_fd)

    def _spawn_unix_pty_process(
        self, command: CommandInput, command_repr: str, slave_fd: int | None
    ) -> None:
        args, use_shell = self._prepare_command_invocation(command)
        env = self._build_subprocess_env()
        self._process = subprocess.Popen(
            args,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            shell=use_shell,
            text=False,
            close_fds=True,
            start_new_session=True,
            cwd=self._ctx._pending_cwd,
            env=env,
        )
        self._ctx._register_local_process_group(self._process.pid)
        self._logger.log(
            "process_spawned",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=self._process.pid,
            _command=command_repr[:100],
            _mode="local_pty_unix",
        )

    def _run_unix_pty_immediate(self, master_fd: int | None) -> int:
        assert master_fd is not None
        start_time = time.time()
        output = self._collect_unix_pty_output(master_fd)
        if self.streamer:
            for line in output:
                self.streamer.stdout_buffer.write(line + "\n")
        self._close_fd(master_fd)
        return_code = self._process.wait()
        duration = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.INFO,
            task=self.task_name,
            message=f"PTY command finished (exit {return_code}) in {duration:.2f}s",
            exit_code=return_code,
            _duration=f"{duration:.2f}",
            _remote=False,
            _pty=True,
        )
        return return_code

    def _collect_unix_pty_output(self, master_fd: int) -> list[str]:
        select_module = _require_select_module()
        output: list[str] = []
        while True:
            try:
                ready, _, _ = select_module.select([master_fd], [], [], 0.1)
                if ready:
                    chunk = self._read_fd_chunk(master_fd)
                    if chunk is None:
                        break
                    output.extend(chunk.splitlines())
                elif self._process_finished():
                    with contextlib.suppress(OSError):
                        if chunk := self._read_fd_chunk(master_fd):
                            output.extend(chunk.splitlines())
                    break
            except OSError:
                break
        return output

    def _run_unix_pty_streaming(self, master_fd: int | None) -> int:
        assert master_fd is not None
        output_worker = StreamWorker(
            name=f"{self.task_name}_pty_unix",
            line_iterator_factory=lambda cancel_event=None,
            poll_interval=0.1: self._unix_pty_line_generator(
                master_fd, cancel_event=cancel_event, poll_interval=poll_interval
            ),
            streamer=self.streamer,
            logger=self._logger,
            task_name=self.task_name,
            mode="local_pty_unix",
            purpose="PTY output streaming (Unix)",
            transform=lambda line: line.rstrip("\r"),
            stop_event=self.cancel_event,
        ).start()

        start_time = time.time()
        return_code = self._process.wait()

        self._join_stream_workers([output_worker], "local_pty_unix")
        self._logger.log(
            "process_terminated",
            LogLevel.DEBUG,
            task=self.task_name,
            _pid=self._process.pid,
            _exit_code=return_code,
        )
        duration = time.time() - start_time
        self._logger.log(
            "shell_command_ended",
            LogLevel.INFO,
            task=self.task_name,
            message=f"PTY command finished (exit {return_code}) in {duration:.2f}s",
            exit_code=return_code,
            _duration=f"{duration:.2f}",
            _remote=False,
            _pty=True,
        )
        self._close_fd(master_fd)
        return return_code

    def _unix_pty_line_generator(self, fd: int, cancel_event=None, poll_interval: float = 0.1):
        buffer = ""
        try:
            while True:
                if cancel_event and cancel_event.is_set():
                    break
                ready = self._unix_select_ready(fd)
                if ready is None:
                    break
                if ready:
                    result = self._read_and_split_lines(fd, buffer)
                    if result is None:
                        break
                    buffer, lines = result
                    yield from lines
                elif self._process_finished():
                    buffer, lines = self._drain_unix_buffer_once(fd, buffer)
                    yield from lines
                    break
                elif self._wait_for_cancel(cancel_event, poll_interval):
                    break
        finally:
            if buffer:
                yield from buffer.splitlines()

    @staticmethod
    def _close_fd(fd: int | None) -> None:
        if fd is None:
            return
        with contextlib.suppress(OSError):
            os.close(fd)

    def _read_fd_chunk(self, fd: int) -> str | None:
        data = os.read(fd, 4096)
        return data.decode("utf-8", errors="replace") if data else None

    def _split_buffer_lines(self, buffer: str, chunk: str) -> tuple[list[str], str]:
        buffer_local = buffer + chunk
        lines: list[str] = []
        while "\n" in buffer_local:
            line, buffer_local = buffer_local.split("\n", 1)
            lines.append(line)
        return lines, buffer_local

    def _read_and_split_lines(self, fd: int, buffer: str) -> tuple[str, list[str]] | None:
        if (chunk := self._read_fd_chunk(fd)) is None:
            return None
        lines, new_buffer = self._split_buffer_lines(buffer, chunk)
        return new_buffer, lines

    def _drain_unix_buffer_once(self, fd: int, buffer: str) -> tuple[str, list[str]]:
        with contextlib.suppress(OSError):
            if result := self._read_and_split_lines(fd, buffer):
                return result
        return buffer, []

    def _unix_select_ready(self, fd: int) -> bool | None:
        select_module = _require_select_module()
        try:
            ready, _, _ = select_module.select([fd], [], [], 0.1)
        except OSError:
            return None
        return bool(ready)

    def _process_finished(self) -> bool:
        return self._process is not None and self._process.poll() is not None

    def _settle_stream_callbacks(self, mode: str) -> None:
        self._wait_for_stream_callbacks(mode)
        self._flush_stream_callbacks(mode)

    def _join_stream_workers(self, workers: list[StreamWorker], mode: str) -> None:
        for worker in workers:
            worker.join(timeout=5.0)
        self._settle_stream_callbacks(mode)

    def _cleanup_winpty_process(self) -> None:
        if self._pty_proc is None:
            return
        close_method = getattr(self._pty_proc, "close", None)
        if callable(close_method):
            try:
                close_method()
            except Exception as exc:  # pylint: disable=broad-except
                self._logger.log(
                    "pty_cleanup_failed",
                    LogLevel.WARNING,
                    task=self.task_name,
                    message="Failed to clean up PTY process",
                    error=str(exc),
                    _mode="local_pty_windows",
                )
        self._pty_proc = None


class _BaseLocalStrategy:
    """Base class for local execution strategies."""

    def __init__(self, ctx) -> None:
        self._ctx = ctx

    def supports(  # pragma: no cover - interface
        self,
        *,
        disable_pty: bool,
        env: dict[str, str] | None,
        cwd: str | None,
    ) -> bool:
        raise NotImplementedError

    def run(  # pragma: no cover
        self,
        command: CommandInput,
        immediate_mode: bool,
    ) -> int:
        raise NotImplementedError

    def _get_pty_state(self) -> tuple[bool, str | None]:
        return _load_pty_support()


class _WinPTYStrategy(_BaseLocalStrategy):
    def supports(
        self,
        *,
        disable_pty: bool,
        env: dict[str, str] | None,
        cwd: str | None,
    ) -> bool:
        available, mode = self._get_pty_state()
        return self._ctx.use_pty and available and mode == "winpty" and not disable_pty

    def run(self, command: CommandInput, immediate_mode: bool) -> int:
        return self._ctx._run_local_pty_windows(command, immediate_mode)


class _UnixPTYStrategy(_BaseLocalStrategy):
    def supports(
        self,
        *,
        disable_pty: bool,
        env: dict[str, str] | None,
        cwd: str | None,
    ) -> bool:
        available, mode = self._get_pty_state()
        return self._ctx.use_pty and available and mode == "unix" and not disable_pty

    def run(self, command: CommandInput, immediate_mode: bool) -> int:
        return self._ctx._run_local_pty_unix(command, immediate_mode)


class _SubprocessStrategy(_BaseLocalStrategy):
    def supports(
        self,
        *,
        disable_pty: bool,
        env: dict[str, str] | None,
        cwd: str | None,
    ) -> bool:  # pylint: disable=unused-argument
        return True

    def run(self, command: CommandInput, immediate_mode: bool) -> int:
        return self._ctx._run_local_subprocess(command, immediate_mode)
