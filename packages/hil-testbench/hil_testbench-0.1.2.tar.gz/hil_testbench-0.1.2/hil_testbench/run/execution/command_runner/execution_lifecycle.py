"""Execution lifecycle helpers for :mod:`command_runner`."""

from __future__ import annotations

import threading
import traceback
from collections.abc import Callable
from typing import Any

from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

from .health_lifecycle import HealthLifecycle
from .signal_controller import SignalController
from .types import CommandRunnerSettings


class ExecutionLifecycle:
    """Coordinates health monitoring, signal handling, and thread hooks."""

    def __init__(
        self,
        *,
        logger: TaskLogger,
        cancel_event: threading.Event,
        shutdown_callback: Callable[[], None],
        force_shutdown_callback: Callable[[], None] | None = None,
        running_tasks_supplier: Callable[[], int],
        interrupt_callback: Callable[[], None] | None = None,
        signal_grace_seconds: float = 10.0,
    ) -> None:
        self._logger = logger
        self._cancel_event = cancel_event
        self._health = HealthLifecycle(
            task_logger=logger,
            cancel_event=cancel_event,
            running_tasks_supplier=running_tasks_supplier,
        )
        self._signal_controller = SignalController(
            logger=logger,
            cancel_event=cancel_event,
            shutdown_callback=shutdown_callback,
            force_shutdown_callback=force_shutdown_callback,
            interrupt_callback=interrupt_callback,
            force_grace_seconds=signal_grace_seconds,
        )
        self._thread_hook_installed = False

    def start(self, settings: CommandRunnerSettings) -> None:
        """Start health monitoring and register signal handlers."""
        self._health.start(settings)
        self._signal_controller.register()
        self._install_thread_exception_hook()

    def stop(self) -> None:
        """Stop health monitoring and unregister signal handlers."""
        self._signal_controller.unregister()
        self._health.stop()

    def _install_thread_exception_hook(self) -> None:
        if self._thread_hook_installed or not hasattr(threading, "excepthook"):
            return

        def _threading_excepthook(args: Any) -> None:
            exc_type = getattr(args, "exc_type", None)
            exc_value = getattr(args, "exc_value", None)
            exc_tb = getattr(args, "exc_traceback", None)
            thr = getattr(args, "thread", None)
            tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            self._logger.log(
                "thread_exception",
                LogLevel.ERROR,
                scope=LogScope.FRAMEWORK,
                message="Uncaught exception in thread",
                thread_name=getattr(thr, "name", "unknown"),
                error_type=getattr(exc_type, "__name__", str(exc_type)),
                error=str(exc_value),
                _traceback=tb_str,
            )

        threading.excepthook = _threading_excepthook
        self._thread_hook_installed = True


__all__ = ["ExecutionLifecycle"]
