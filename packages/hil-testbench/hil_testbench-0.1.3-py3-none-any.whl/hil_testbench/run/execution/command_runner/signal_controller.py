"""Dedicated interrupt controller for :mod:`command_runner`."""

from __future__ import annotations

import contextlib
import signal
import sys
import threading
import time
from collections.abc import Callable
from typing import cast

from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger


class SignalController:
    """Registers SIGINT/SIGTERM handlers and coordinates graceful shutdown."""

    def __init__(
        self,
        *,
        logger: TaskLogger,
        cancel_event: threading.Event,
        shutdown_callback: Callable[[], None],
        force_shutdown_callback: Callable[[], None] | None = None,
        interrupt_callback: Callable[[], None] | None = None,
        force_grace_seconds: float = 10.0,
    ) -> None:
        self._logger = logger
        self._cancel_event = cancel_event
        self._shutdown_callback = shutdown_callback
        self._force_shutdown_callback = force_shutdown_callback
        self._interrupt_callback = interrupt_callback
        self._original_handlers: dict[int, signal.Handlers] = {}
        self._interrupt_count = 0
        self._force_grace_seconds = max(0.0, float(force_grace_seconds))
        self._first_interrupt_time: float | None = None

    def register(self) -> None:
        """Register handlers when running on the main thread."""
        if threading.current_thread() is not threading.main_thread():
            self._logger.log(
                "skip_signal_handlers",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                message="Skipping signal handler registration (not in main thread)",
                thread=threading.current_thread().name,
            )
            return

        for sig in (signal.SIGINT, signal.SIGTERM):
            handler = signal.getsignal(sig)
            self._original_handlers[sig] = cast(signal.Handlers, handler)
            signal.signal(sig, self._handle_signal)

    def unregister(self) -> None:
        """Restore original signal handlers."""
        for sig, handler in self._original_handlers.items():
            with contextlib.suppress(Exception):
                signal.signal(sig, handler)
        self._original_handlers.clear()

    def _handle_signal(self, _signum, _frame) -> None:
        """SIGINT/SIGTERM callback supporting escalation on repeat interrupts."""
        self._interrupt_count += 1
        if self._interrupt_count == 1:
            self._first_interrupt_time = time.monotonic()
            self._handle_initial_interrupt()
            return
        if not self._should_escalate_interrupt():
            self._log_grace_window_event()
            return
        self._handle_escalated_interrupt()

    def _handle_initial_interrupt(self) -> None:
        self._logger.log(
            "interrupt_received",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message="User interrupt (Ctrl+C) received - cancelling tasks and shutting down",
        )

        self._mark_shutdown_mode()

        self._flush_stdio()
        self._cancel_event.set()
        if self._interrupt_callback:
            with contextlib.suppress(Exception):
                self._interrupt_callback()
        self._shutdown_callback()
        self._logger.log(
            "runner_exiting",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            message="Runner exiting after interrupt",
        )
        raise KeyboardInterrupt()

    def _should_escalate_interrupt(self) -> bool:
        if self._force_grace_seconds <= 0:
            return True
        if self._first_interrupt_time is None:
            return True
        elapsed = time.monotonic() - self._first_interrupt_time
        return elapsed >= self._force_grace_seconds

    def _log_grace_window_event(self) -> None:
        remaining = None
        if self._first_interrupt_time is not None and self._force_grace_seconds > 0:
            elapsed = time.monotonic() - self._first_interrupt_time
            remaining = max(0.0, self._force_grace_seconds - elapsed)
        self._logger.log(
            "interrupt_grace_window_active",
            LogLevel.INFO,
            scope=LogScope.FRAMEWORK,
            message=(
                "Ignoring additional interrupt while graceful shutdown grace window is active"
            ),
            grace_seconds=self._force_grace_seconds,
            remaining_seconds=round(remaining, 2) if remaining is not None else None,
        )

    def _handle_escalated_interrupt(self) -> None:
        self._logger.log(
            "interrupt_force_shutdown",
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message="Grace period elapsed; forcing immediate shutdown after repeated interrupt",
            remediation="Allow the framework to exit cleanly or investigate stuck commands before retrying",
        )

        self._mark_shutdown_mode()

        self._flush_stdio()
        self._cancel_event.set()
        if self._interrupt_callback:
            with contextlib.suppress(Exception):
                self._interrupt_callback()

        if self._force_shutdown_callback:
            try:
                self._force_shutdown_callback()
            except Exception as exc:  # noqa: BLE001 - best-effort emergency path
                self._logger.log(
                    "force_shutdown_callback_failed",
                    LogLevel.ERROR,
                    scope=LogScope.FRAMEWORK,
                    message="Force shutdown callback raised exception",
                    error=str(exc),
                    error_type=type(exc).__name__,
                )
        self._shutdown_callback()
        self._logger.log(
            "runner_force_exit",
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message="Runner exiting after forced interrupt",
        )
        raise KeyboardInterrupt()

    def _flush_stdio(self) -> None:
        """Flush task logger handlers and stdio for immediate feedback."""
        main_logger = getattr(self._logger, "_main_logger", None)
        if main_logger and hasattr(main_logger, "handlers"):
            for handler in main_logger.handlers:
                with contextlib.suppress(Exception):
                    handler.flush()
        sys.stdout.flush()
        sys.stderr.flush()

    def _mark_shutdown_mode(self) -> None:
        marker = getattr(self._logger, "mark_shutdown_in_progress", None)
        if callable(marker):
            marker()


__all__ = ["SignalController"]
