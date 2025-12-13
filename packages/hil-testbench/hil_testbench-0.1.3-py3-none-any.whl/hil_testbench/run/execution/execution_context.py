"""Execution context for task functions."""

from __future__ import annotations

import contextlib
import os
import shlex
import signal
import subprocess
import threading
import time
from collections.abc import Mapping
from enum import Enum
from typing import Literal

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.exceptions import ExecutionError
from hil_testbench.run.execution.command_spec import CommandSpec
from hil_testbench.run.execution.command_types import CommandInput, stringify_command
from hil_testbench.run.execution.local import LocalExecutionStrategy
from hil_testbench.run.execution.output_streamer import OutputStreamer
from hil_testbench.run.execution.protocols import SSHClientProtocol
from hil_testbench.run.execution.remote import RemoteExecutionStrategy
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.session.process_tracker import ProcessTracker
from hil_testbench.utils.shell import needs_unbuffered_execution

STREAMER_FLUSH_TIMEOUT = 10.0


class ExecutionState(str, Enum):
    """Lifecycle states for command execution."""

    IDLE = "idle"
    RUNNING_LOCAL = "running_local"
    RUNNING_REMOTE = "running_remote"
    TERMINATING = "terminating"


# TODO(long_running): Rework this context to be spec-driven—accept a
# `CommandSpec` instance so transports can read long_running, streaming_format,
# and parser hints without reaching back into task definitions. Strip out the
# PTY auto-detect heuristics once the spec declares PTY intent explicitly.
class ExecutionContext:
    """
    Context object passed to task functions with run() method.
    """

    def __init__(
        self,
        logger: TaskLogger,
        ssh_client: SSHClientProtocol | None,
        streamer: OutputStreamer | None,
        cancel_event: threading.Event | None,
        execution_dir: str,
        task_name: str,
        config: TaskConfig,
        process_tracker: ProcessTracker,
        use_pty: bool = False,
        remote_os: Literal["unix", "windows"] = "unix",
        shell_wrapper_mode: str = "auto",
        command_spec: CommandSpec | None = None,
    ):
        self.ssh_client: SSHClientProtocol | None = ssh_client
        self.streamer: OutputStreamer | None = streamer
        self.cancel_event: threading.Event | None = cancel_event
        self.execution_dir: str = execution_dir
        self.use_pty: bool = use_pty
        self.is_remote: bool = ssh_client is not None
        self.remote_os: Literal["unix", "windows"] = remote_os
        self._process = None
        self._channel = None  # Track SSH channel for remote execution
        self._remote_pid: int | None = None  # Track remote process PID
        self._pty_proc = None  # Track winpty process
        self._logger: TaskLogger = logger
        self.task_name: str = task_name
        self.config = config
        self._process_tracker = process_tracker
        self._state: ExecutionState = ExecutionState.IDLE
        self._local_execution: LocalExecutionStrategy | None = None
        self._remote_execution: RemoteExecutionStrategy | None = None
        self._local_process_group_id: int | None = None
        self._remote_process_group_leader: int | None = None
        self.shell_wrapper_mode = shell_wrapper_mode
        self.command_spec = command_spec
        self._spec_env: dict[str, str] = (
            dict(command_spec.env) if command_spec and command_spec.env else {}
        )
        self._spec_cwd: str | None = command_spec.cwd if command_spec else None
        self._pending_env: dict[str, str] | None = None
        self._pending_cwd: str | None = None

        if command_spec is not None:
            if command_spec.use_pty is not None:
                self.use_pty = bool(command_spec.use_pty)
            if command_spec.shell_wrapper_mode:
                self.shell_wrapper_mode = command_spec.shell_wrapper_mode

    @property
    def has_active_process(self) -> bool:
        """Check if there is an active process running."""
        return (
            self._process is not None
            or self._channel is not None
            or self._remote_pid is not None
            or self._pty_proc is not None
        )

    @property
    def state(self) -> ExecutionState:
        """Expose current execution state."""
        return self._state

    def __enter__(self) -> ExecutionContext:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: D401 - context manager cleanup
        self.cleanup()
        if self._state is not ExecutionState.TERMINATING:
            self._set_state(ExecutionState.IDLE)

    def run(
        self,
        command: CommandInput,
        capture: bool | None = None,
        *,
        env: Mapping[str, str] | None = None,
        cwd: str | None = None,
        **_unused,
    ) -> int:
        """
        Execute a command locally or remotely.

        Args:
            command: The command to execute
            capture: If True, capture output without streaming (immediate mode)
                    If None, use streamer if available

        Returns:
            Exit code of the command
        """
        if self.cancel_event and self.cancel_event.is_set():
            raise KeyboardInterrupt("Task cancelled")

        self._validate_command(command)

        resolved_env = self._resolve_environment(env)
        resolved_cwd = self._resolve_cwd(cwd)
        self._pending_env = resolved_env
        self._pending_cwd = resolved_cwd

        # Auto-detect and apply execution strategy
        command = self._apply_execution_strategy(command, env=resolved_env, cwd=resolved_cwd)

        # Apply wrapper if configured
        command = self._apply_shell_wrapper(command)

        # Determine if we should use immediate mode
        if capture is not None:
            immediate_mode = capture
        elif self.command_spec and self.command_spec.immediate:
            immediate_mode = True
        else:
            immediate_mode = self.streamer is None

        target_state = (
            ExecutionState.RUNNING_REMOTE if self.is_remote else ExecutionState.RUNNING_LOCAL
        )
        self._set_state(target_state)

        try:
            if self.is_remote:
                return self._remote_strategy().run(command, immediate_mode=immediate_mode)
            return self._local_strategy().run(command, immediate_mode=immediate_mode)
        finally:
            self._finalize_execution()
            self._pending_env = None
            self._pending_cwd = None

    def _resolve_environment(self, runtime_env: Mapping[str, str] | None) -> dict[str, str] | None:
        merged: dict[str, str] = {}
        if self._spec_env:
            merged.update(self._spec_env)
        if runtime_env:
            merged.update({str(k): str(v) for k, v in runtime_env.items()})
        return merged or None

    def _resolve_cwd(self, runtime_cwd: str | None) -> str | None:
        return runtime_cwd or self._spec_cwd

    def _apply_execution_strategy(
        self,
        command: CommandInput,
        *,
        env: Mapping[str, str] | None,
        cwd: str | None,
    ) -> str:
        """Auto-detect and apply PTY/script wrapper based on command structure."""
        command_str = stringify_command(command)

        if self.is_remote:
            return self._inject_remote_environment(command_str, env=env, cwd=cwd)
        return command_str

    def _inject_remote_environment(
        self,
        command: str,
        *,
        env: Mapping[str, str] | None,
        cwd: str | None,
    ) -> str:
        prefix_parts: list[str] = []
        if env:
            exports = [f"export {key}={shlex.quote(value)}" for key, value in env.items()]
            if exports:
                prefix_parts.append("; ".join(exports))
        if cwd:
            prefix_parts.append(f"cd {shlex.quote(cwd)}")
        if not prefix_parts:
            return command
        prefix_parts.append(command)
        return " && ".join(prefix_parts)

    def _apply_shell_wrapper(self, command: str) -> str:
        """Apply shell wrapper if configured."""
        wrapper_on = self.shell_wrapper_mode == "on"
        transport = "remote" if self.is_remote else "local"

        if wrapper_on:
            self._logger.log(
                "command_wrapper_applied",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=self.task_name,
                wrapper_mode=self.shell_wrapper_mode,
                transport=transport,
            )
        elif self.is_remote:
            self._logger.log(
                "command_wrapper_disabled",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=self.task_name,
                wrapper_mode=self.shell_wrapper_mode,
                transport=transport,
            )

        if wrapper_on and not self.is_remote:
            return self._wrap_local_command(command)

        return command

    def _wrap_local_command(self, command: CommandInput) -> str:
        """Wrap a local command in a shell for tools needing shell semantics."""
        # If we already have a sequence (argv-style), avoid wrapping in an extra
        # shell; shlex.join() preserves quoting and the subprocess strategy will
        # execute directly. Wrapping would double-quote embedded scripts (e.g.,
        # python -c payloads) and can yield SyntaxError from mangled strings.
        if not isinstance(command, str):
            return stringify_command(command)

        cmd_str = command
        if needs_unbuffered_execution(cmd_str):
            return f"sh -c '{cmd_str}'"
        return f"sh -c 'exec {cmd_str}'"

    def _wait_for_stream_callbacks(self, mode: str) -> None:
        """Ensure streaming callbacks finish before validation runs."""
        if not self.streamer:
            return
        timeout = self._get_streamer_flush_timeout()
        if self.streamer.wait_for_completion(timeout=timeout):
            return
        self._logger.log(
            "streamer_flush_timeout",
            LogLevel.WARNING,
            task=self.task_name,
            message="Streaming callbacks did not flush before timeout",
            _mode=mode,
            _timeout=timeout,
        )

    def _flush_stream_callbacks(self, mode: str) -> None:
        """Flush buffered pipeline callbacks if supported."""
        if not self.streamer:
            return
        try:
            self.streamer.flush_callbacks()
        except Exception as exc:  # pylint: disable=broad-except
            self._logger.log(
                "streamer_flush_error",
                LogLevel.WARNING,
                task=self.task_name,
                message="Failed to flush pipeline callbacks",
                error=str(exc),
                _mode=mode,
            )

    def _get_streamer_flush_timeout(self) -> float:
        run_config = getattr(self.config, "run_config", None)
        configured_timeout = (
            getattr(run_config, "streamer_flush_timeout", None) if run_config is not None else None
        )
        if isinstance(configured_timeout, int | float) and configured_timeout > 0:
            return float(configured_timeout)
        return STREAMER_FLUSH_TIMEOUT

    def cleanup(self) -> None:
        """Release execution resources."""
        local_strategy = self._local_execution
        if local_strategy:
            local_strategy.cleanup()
        self._close_channel()
        self._close_process_streams()
        self._reset_process_handles()

    def _finalize_execution(self) -> None:
        if self._state is not ExecutionState.TERMINATING:
            self._set_state(ExecutionState.IDLE)
        self.cleanup()

    def _set_state(self, state: ExecutionState) -> None:
        if self._state is state:
            return
        self._logger.log(
            "execution_state_changed",
            LogLevel.DEBUG,
            task=self.task_name,
            _old_state=self._state.value,
            _new_state=state.value,
        )
        self._state = state

    def _close_channel(self) -> None:
        if self._channel is None:
            return
        with contextlib.suppress(Exception):
            self._channel.close()
        self._channel = None

    def _local_strategy(self) -> LocalExecutionStrategy:
        if self._local_execution is None:
            self._local_execution = LocalExecutionStrategy(self)
        return self._local_execution

    def _remote_strategy(self) -> RemoteExecutionStrategy:
        if self._remote_execution is None:
            self._remote_execution = RemoteExecutionStrategy(self)
        return self._remote_execution

    def _close_process_streams(self) -> None:
        if not self._process:
            return
        for stream_name in ("stdout", "stderr", "stdin"):
            stream = getattr(self._process, stream_name, None)
            if stream is None:
                continue
            close = getattr(stream, "close", None)
            if callable(close):
                with contextlib.suppress(Exception):
                    close()

    def _reset_process_handles(self) -> None:
        self._process = None
        self._remote_pid = None
        self._local_process_group_id = None
        self._remote_process_group_leader = None

    def _validate_command(self, command: CommandInput) -> None:
        try:
            stringify_command(command)
        except (ValueError, TypeError) as exc:
            raise ExecutionError(
                "Commands must be non-empty strings or sequences of strings",
                context={"task": self.task_name},
            ) from exc

    def kill(self):
        """Kill the running process/command."""
        self._set_state(ExecutionState.TERMINATING)
        self._logger.log(
            "kill_request",
            LogLevel.DEBUG,
            task=self.task_name,
            message="Terminating process",
        )
        self._terminate_local_process_group(signal.SIGTERM)

        if self._process:
            try:
                self._process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._logger.log(
                    "kill_local_timeout",
                    LogLevel.WARNING,
                    task=self.task_name,
                    message="Process did not terminate gracefully, forcing kill",
                    _pid=self._process.pid,
                )
                self._terminate_local_process_group(signal.SIGKILL)
                try:
                    self._process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    self._logger.log(
                        "kill_local_failed",
                        LogLevel.WARNING,
                        task=self.task_name,
                        message="Process stuck, unable to kill",
                        _pid=self._process.pid,
                    )

        self._terminate_remote_process_group("TERM")
        time.sleep(0.3)
        self._terminate_remote_process_group("KILL")

        # Close remote SSH channel
        if self._channel:
            with contextlib.suppress(Exception):
                self._channel.close()

    def force_kill(self) -> None:
        """Forcefully kill the running process group (used after repeat interrupts)."""
        self._set_state(ExecutionState.TERMINATING)
        self._logger.log(
            "force_kill_request",
            LogLevel.WARNING,
            task=self.task_name,
            message="Force-killing process group",
        )
        self._terminate_local_process_group(signal.SIGKILL)
        self._terminate_remote_process_group("KILL")

    def _register_local_process_group(self, pid: int) -> None:
        if os.name == "nt":
            self._local_process_group_id = pid
            return
        try:
            self._local_process_group_id = os.getpgid(pid)
        except OSError:
            self._local_process_group_id = None

    def _register_remote_process_group(self, pid: int) -> None:
        self._remote_process_group_leader = pid

    def _validate_signal_safety(self, sig: int, target_pgid: int | None) -> bool:
        """
        Validate signal and PGID for safe process group signaling.

        SEC-1: Implements python:S4828 compliance checks.

        Returns:
            True if safe to proceed, False otherwise.
        """
        # Validate signal parameter - only allow controlled signals
        if sig not in (signal.SIGTERM, signal.SIGKILL):
            self._logger.log(
                "signal_validation_failed",
                LogLevel.ERROR,
                task=self.task_name,
                message="Attempted to send invalid signal to process group",
                _signal=sig,
                _allowed_signals=[signal.SIGTERM, signal.SIGKILL],
            )
            return False

        # Validate PGID - never signal special or system process groups
        # pgid <= 0: special meaning (0 = current, -1 = all processes with permission)
        # pgid == 1: init process
        if target_pgid is None or target_pgid <= 1:
            if target_pgid is not None and target_pgid <= 0:
                self._logger.log(
                    "pgid_safety_violation",
                    LogLevel.ERROR,
                    task=self.task_name,
                    message="Prevented dangerous signal to special process group",
                    _pgid=target_pgid,
                    _signal=sig,
                )
            return False

        # Warn about low-numbered process groups (typically system processes)
        if target_pgid < 100:
            self._logger.log(
                "pgid_low_value_warning",
                LogLevel.WARNING,
                task=self.task_name,
                message="Sending signal to low-numbered process group (potential system process)",
                _pgid=target_pgid,
                _signal=sig,
            )

        return True

    def _terminate_local_process_group(self, sig: int) -> None:
        if not self._process:
            return
        if os.name == "nt":
            try:
                if sig == signal.SIGKILL:
                    self._process.kill()
                else:
                    self._process.terminate()
            except Exception:  # noqa: BLE001 - best-effort cleanup
                pass
            return

        target_pgid = self._local_process_group_id
        if target_pgid is None:
            try:
                target_pgid = os.getpgid(self._process.pid)
            except OSError:
                return

        # SEC-1: Safety validation (python:S4828 compliance)
        if not self._validate_signal_safety(sig, target_pgid):
            return

        # SEC-3: Log termination attempt (never silently kill processes)
        try:
            os.killpg(target_pgid, sig)
            self._logger.log(
                "process_group_signal_sent",
                LogLevel.DEBUG,
                task=self.task_name,
                message="Process group signal sent",
                _pgid=target_pgid,
                _signal=sig,
            )
        except ProcessLookupError:
            # Process already terminated - this is expected and not an error
            self._logger.log(
                "process_group_already_terminated",
                LogLevel.DEBUG,
                task=self.task_name,
                message="Process group already terminated",
                _pgid=target_pgid,
                _signal=sig,
            )
        except PermissionError as exc:
            # Permission denied - this should not happen for our own processes
            self._logger.log(
                "process_group_signal_permission_denied",
                LogLevel.ERROR,
                task=self.task_name,
                message="Permission denied when signaling process group",
                _pgid=target_pgid,
                _signal=sig,
                error=str(exc),
            )
        except OSError as exc:
            # Other OS errors
            self._logger.log(
                "process_group_signal_failed",
                LogLevel.WARNING,
                task=self.task_name,
                message="Failed to signal process group",
                _pgid=target_pgid,
                _signal=sig,
                error=str(exc),
            )

    def _terminate_remote_process_group(self, signal_name: str) -> None:
        if not (self.ssh_client and self._remote_process_group_leader):
            return
        target = self._remote_process_group_leader
        if target is None or target <= 1:
            return
        try:
            self.ssh_client.exec_command(f"kill -{signal_name} -- -{target} 2>/dev/null || true")
            self._logger.log(
                "kill_remote_sent",
                LogLevel.DEBUG,
                task=self.task_name,
                message="Remote process group termination signal sent",
                _pid=target,
                _signal=signal_name,
            )
        except Exception:
            self._logger.log(
                "kill_remote_exception",
                LogLevel.WARNING,
                task=self.task_name,
                message="Error sending remote kill signal",
                _pid=target,
                _signal=signal_name,
            )
