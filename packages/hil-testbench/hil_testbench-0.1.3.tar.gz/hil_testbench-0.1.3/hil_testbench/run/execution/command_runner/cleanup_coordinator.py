"""Cleanup helpers for the command runner shutdown path."""

from __future__ import annotations

import contextlib
import os
import sys
import threading
import traceback
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import psutil

from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

if TYPE_CHECKING:  # pragma: no cover - import cycle guard
    from hil_testbench.run.execution.execution_session import ExecutionSession
from .ssh_client_manager import SSHClientManager


# TODO(long_running): Consume the upcoming ExecutionSession command registry so
# cleanup decisions (kill vs resume) use CommandSpec metadata like
# `long_running` instead of inspecting context objects directly.
class CleanupCoordinator:
    """Handles process termination, SSH teardown, and diagnostics."""

    def __init__(
        self,
        *,
        logger: TaskLogger,
        ssh_manager: SSHClientManager,
        normalize_shutdown_error: Callable[[Exception, str], Exception],
        session: ExecutionSession | None = None,
    ) -> None:
        self._logger = logger
        self._ssh_manager = ssh_manager
        self._normalize_shutdown_error = normalize_shutdown_error
        self._session = session

    def attach_session(self, session: ExecutionSession) -> None:
        self._session = session

    def terminate_running_processes(self, *, verbose: bool) -> None:
        """Terminate any still-running subprocesses before shutdown."""
        for command_name, ctx in self._iter_contexts():
            if ctx.has_active_process:
                try:
                    if verbose:
                        self._logger.log(
                            "shutdown_task_kill",
                            LogLevel.DEBUG,
                            scope=LogScope.FRAMEWORK,
                            message="Terminating running task",
                            task=command_name,
                        )
                    ctx.kill()
                except Exception as exc:  # pylint: disable=broad-except
                    normalized = self._normalize_shutdown_error(exc, command_name)
                    self._logger.log(
                        "task_kill_error",
                        LogLevel.ERROR,
                        scope=LogScope.FRAMEWORK,
                        message="Failed to terminate task",
                        task=command_name,
                        error=str(normalized),
                        error_type=type(normalized).__name__,
                    )
            elif verbose:
                self._logger.log(
                    "task_already_completed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    _task=command_name,
                    _reason="shutdown_skip",
                )

    def force_terminate_processes(self, *, verbose: bool) -> None:
        """Force kill remaining subprocesses during escalated shutdown."""
        for command_name, ctx in self._iter_contexts():
            if not ctx.has_active_process:
                continue
            try:
                if verbose:
                    self._logger.log(
                        "force_shutdown_task_kill",
                        LogLevel.WARNING,
                        scope=LogScope.FRAMEWORK,
                        message="Force-killing stuck task",
                        task=command_name,
                    )
                ctx.force_kill()
            except Exception as exc:  # pylint: disable=broad-except
                normalized = self._normalize_shutdown_error(exc, command_name)
                self._logger.log(
                    "task_force_kill_error",
                    LogLevel.ERROR,
                    scope=LogScope.FRAMEWORK,
                    message="Failed to force-kill task",
                    task=command_name,
                    error=str(normalized),
                    error_type=type(normalized).__name__,
                )

    def close_transports(self) -> None:
        """Close all cached SSH clients."""
        self._ssh_manager.close_all()

    def summarize_shutdown(self) -> bool:
        """Return True if any resources were still active at shutdown."""
        session = self._session
        if session:
            remaining_tasks, remaining_streamers = session.shutdown_summary()
        else:
            remaining_tasks = remaining_streamers = 0
        remaining_ssh = self._ssh_manager.active_client_count()
        return remaining_tasks > 0 or remaining_streamers > 0 or remaining_ssh > 0

    def log_process_exit_diagnostics(self) -> None:
        """Emit best-effort process diagnostics for debugging."""
        pid = os.getpid()
        thread_details = [
            {
                "name": t.name,
                "ident": t.ident,
                "daemon": t.daemon,
                "alive": t.is_alive(),
            }
            for t in threading.enumerate()
        ]
        children: list[int] = []
        if psutil:
            with contextlib.suppress(Exception):
                proc = psutil.Process(pid)
                children = [c.pid for c in proc.children(recursive=True)]
        stack_dump: list[dict[str, Any]] = []
        if hasattr(sys, "_current_frames"):
            frames = sys._current_frames()
            stack_dump.extend(
                {
                    "thread_id": thread_id,
                    "stack": traceback.format_stack(frame)[-10:],
                }
                for thread_id, frame in frames.items()
                if thread_id != threading.current_thread().ident
            )
        self._logger.log(
            "process_exit_diagnostics",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            _pid=pid,
            _thread_count=len(thread_details),
            _threads=repr(thread_details[:15]),
            _child_pids=repr(children),
            _sampled_stack_threads=len(stack_dump),
        )

    def _iter_contexts(self) -> list[tuple[str, Any]]:
        session = self._session
        if not session:
            return []
        return session.iter_contexts()

    def log_process_exit_diagnostics_safe(self) -> None:
        """Log diagnostics while ignoring unexpected failures."""
        with contextlib.suppress(Exception):
            self.log_process_exit_diagnostics()


__all__ = ["CleanupCoordinator"]
