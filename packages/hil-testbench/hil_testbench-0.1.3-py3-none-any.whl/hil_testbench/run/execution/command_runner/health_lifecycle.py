"""Health monitor orchestration for :mod:`command_runner`."""

from __future__ import annotations

import contextlib
import threading
from collections.abc import Callable

from hil_testbench.health_monitor import HealthMonitor
from hil_testbench.run.logging.task_logger import TaskLogger

from .health_display import HealthDisplayService
from .types import CommandRunnerSettings


class HealthLifecycle:
    """Starts/stops health-related background services."""

    def __init__(
        self,
        *,
        task_logger: TaskLogger,
        cancel_event: threading.Event,
        running_tasks_supplier: Callable[[], int],
    ) -> None:
        self._task_logger = task_logger
        self._cancel_event = cancel_event
        self._running_tasks_supplier = running_tasks_supplier
        self._monitor: HealthMonitor | None = None
        self._display: HealthDisplayService | None = None

    def start(self, settings: CommandRunnerSettings) -> None:
        if not settings.enable_health_logging:
            return
        self._display = HealthDisplayService(self._task_logger, self._cancel_event)
        self._monitor = HealthMonitor(
            logger=self._task_logger,
            interval=settings.health_interval,
            running_tasks_supplier=self._running_tasks_supplier,
            stop_event=self._cancel_event,
            log_directory=self._task_logger.get_execution_dir(),
            cpu_threshold=settings.health_cpu_threshold,
            memory_threshold=settings.health_memory_threshold,
            disk_threshold_gb=settings.health_disk_threshold_gb,
        )
        self._monitor.start()
        self._display.start()

    def stop(self) -> None:
        if self._monitor:
            with contextlib.suppress(Exception):
                self._monitor.stop()
            self._monitor = None
        if self._display:
            self._display.stop()
            self._display = None


__all__ = ["HealthLifecycle"]
