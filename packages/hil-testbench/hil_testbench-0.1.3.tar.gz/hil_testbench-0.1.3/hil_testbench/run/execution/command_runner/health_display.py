"""Background health display updates for CommandRunner."""

from __future__ import annotations

import os
import threading
import time
from typing import Any

import psutil

from hil_testbench.run.logging.task_logger import LogLevel, TaskLogger

_SYSTEM_HEALTH_SECTION = "System Health"


class HealthDisplayService:
    """Best-effort health metric sampler feeding the display backend."""

    def __init__(
        self,
        task_logger: TaskLogger,
        cancel_event: threading.Event,
        *,
        psutil_module: Any | None = None,
    ) -> None:
        self._task_logger = task_logger
        self._cancel_event = cancel_event
        self._psutil = psutil if psutil_module is None else psutil_module
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the background sampler if a display backend is available."""
        backend = self._get_backend()
        if not backend or self._thread:
            return
        self._stop_event.clear()
        process = self._init_psutil_process()
        thread = threading.Thread(
            target=self._loop,
            args=(backend, process),
            name="HealthDisplayUpdater",
            daemon=True,
        )
        thread.start()
        self._thread = thread

    def update_once(self) -> None:
        """Run a single sampling cycle (useful for deterministic tests)."""
        backend = self._get_backend()
        if not backend:
            return
        process = self._init_psutil_process()
        self._safe_update_metrics(backend, self._psutil, process)

    def stop(self) -> None:
        """Request the background thread to stop and wait briefly."""
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join(timeout=1)
        self._thread = None
        self._stop_event.clear()

    def _loop(self, backend: Any, process: psutil.Process | None) -> None:
        while not self._cancel_event.is_set() and not self._stop_event.is_set():
            self._safe_update_metrics(backend, self._psutil, process)
            time.sleep(10)

    def _init_psutil_process(self) -> psutil.Process | None:
        if not self._psutil:
            return None
        try:
            return self._psutil.Process(os.getpid())
        except Exception:  # pragma: no cover - psutil may fail in restricted envs
            return None

    def _safe_update_metrics(self, backend: Any, psutil_mod: Any, process: Any) -> None:
        try:
            timestamp = time.time()
            if not psutil_mod:
                self._update_thread_count_only(backend, timestamp)
                return
            cpu_sys = psutil_mod.cpu_percent(interval=0.2)
            mem = psutil_mod.virtual_memory()
            disk = psutil_mod.disk_usage(self._task_logger.get_execution_dir())
            backend.update_parameter(
                _SYSTEM_HEALTH_SECTION,
                "CPU System%",
                {"value": cpu_sys, "unit": "%"},
                timestamp,
            )
            backend.update_parameter(
                _SYSTEM_HEALTH_SECTION,
                "Memory%",
                {"value": mem.percent, "unit": "%"},
                timestamp,
            )
            backend.update_parameter(
                _SYSTEM_HEALTH_SECTION,
                "Memory Used GB",
                {"value": round(mem.used / (1024**3), 2), "unit": "GB"},
                timestamp,
            )
            backend.update_parameter(
                _SYSTEM_HEALTH_SECTION,
                "Disk Free GB",
                {"value": round(disk.free / (1024**3), 2), "unit": "GB"},
                timestamp,
            )
            if process:
                cpu_proc = process.cpu_percent(interval=None)
                backend.update_parameter(
                    _SYSTEM_HEALTH_SECTION,
                    "CPU Proc%",
                    {"value": cpu_proc, "unit": "%"},
                    timestamp,
                )
        except Exception as exc:  # pylint: disable=broad-except
            self._task_logger.log(
                "health_display_update_error",
                LogLevel.DEBUG,
                _error=str(exc),
            )

    def _update_thread_count_only(self, backend: Any, timestamp: float) -> None:
        backend.update_parameter(
            _SYSTEM_HEALTH_SECTION,
            "Thread Count",
            {"value": threading.active_count(), "unit": "threads"},
            timestamp,
        )

    def _get_backend(self) -> Any | None:
        getter = getattr(self._task_logger, "get_display_backend", None)
        if callable(getter):
            return getter()
        return None


__all__ = ["HealthDisplayService"]
