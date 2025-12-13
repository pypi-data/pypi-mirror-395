"""Health monitoring utilities for the unified execution framework.
Collected metrics describe host/process health while GraphExecutor + CommandRunner
execute the global DAG. Internal-only; never exposed as a user-facing task.
"""

# Question: should this just be a task? or its own thing?
from __future__ import annotations

import contextlib
import os
import shutil
import sys
import threading
import time
from collections.abc import Callable
from typing import Any

from hil_testbench.data_structs.parameters import Threshold
from hil_testbench.data_structs.threshold_utils import (
    build_threshold_from_spec,
    is_threshold_triggered,
)
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

psutil: Any | None
try:
    import psutil as _psutil  # hil: allow-lazy - optional dependency
except ImportError:  # pragma: no cover - fallback if psutil missing
    psutil = None
else:
    psutil = _psutil


class HealthMonitor:
    """Background thread that periodically logs health metrics.

    Metrics (if psutil available):
        - process_cpu_percent
        - system_cpu_percent
        - process_memory_rss_bytes
        - process_memory_percent
        - thread_count
        - open_fds (Unix only / if available)
        - disk_free_gb (log directory)
        - running_tasks (callback provided)

    Thresholds:
        - cpu_threshold: CPU % to trigger warning (default 80)
        - memory_threshold: Memory % to trigger warning (default 85)
        - disk_threshold_gb: Free disk space in GB to trigger warning (default 10)

    Fallback (no psutil):
        - thread_count (approx)
        - running_tasks
    """

    def __init__(
        self,
        logger: TaskLogger,
        interval: int = 600,
        running_tasks_supplier: Callable[[], int] | None = None,
        stop_event: threading.Event | None = None,
        log_directory: str | None = None,
        cpu_threshold: float = 80.0,
        memory_threshold: float = 85.0,
        disk_threshold_gb: float = 10.0,
    ):
        self._logger = logger
        self._interval = max(5, interval)  # safeguard minimal interval
        self._running_tasks_supplier = running_tasks_supplier or (lambda: -1)
        self._stop_event = stop_event or threading.Event()
        self._thread: threading.Thread | None = None
        self._started = False
        self._pid = os.getpid()
        if psutil is not None:
            self._proc = psutil.Process(self._pid)
        else:
            self._proc = None
        self._log_directory = log_directory
        self._cpu_threshold = cpu_threshold
        self._memory_threshold = memory_threshold
        self._disk_threshold_gb = disk_threshold_gb
        self._cpu_threshold_def = build_threshold_from_spec(
            "cpu",
            {"value": cpu_threshold, "operator": "gt", "color": "red"},
        )
        self._memory_threshold_def = build_threshold_from_spec(
            "memory",
            {"value": memory_threshold, "operator": "gt", "color": "red"},
        )
        self._disk_threshold_def = build_threshold_from_spec(
            "disk",
            {"value": disk_threshold_gb, "operator": "lt", "color": "yellow"},
        )
        self._active_warnings: set[str] = set()
        self._process_registry: dict[int, str] = {}  # pid -> description
        self._thread_registry: dict[int, str] = {}  # thread_id -> description

    def start(self):
        """Start health monitoring thread."""
        if self._started:
            return
        self._started = True
        self._thread = threading.Thread(target=self._run, name="HealthMonitor", daemon=True)
        # Log thread creation
        self._logger.log(
            "thread_created",
            LogLevel.DEBUG,
            thread_name="HealthMonitor",
            daemon=True,
            purpose="system health monitoring",
        )
        self._thread.start()
        self._logger.log(
            "health_monitor_started",
            LogLevel.DEBUG,
            interval_seconds=self._interval,
        )

    def stop(self):
        """Stop health monitoring thread."""
        if not self._started:
            return
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
            # Log thread termination
            self._logger.log(
                "thread_terminated",
                LogLevel.DEBUG,
                thread_name="HealthMonitor",
                alive=self._thread.is_alive(),
            )

        # Check for leaked processes/threads
        if self._process_registry or self._thread_registry:
            leaked_data: dict[str, Any] = {}
            if self._process_registry:
                leaked_data["leaked_processes"] = list(self._process_registry.values())
            if self._thread_registry:
                leaked_data["leaked_threads"] = list(self._thread_registry.values())
            self._logger.log(
                "resource_leak_detected",
                level=LogLevel.WARNING,
                **leaked_data,
            )

        self._logger.log("health_monitor_stopped", LogLevel.DEBUG)
        self._started = False

    def register_process(self, pid: int, description: str):
        """Register a process for leak tracking."""
        self._process_registry[pid] = description

    def unregister_process(self, pid: int):
        """Unregister a process (normal cleanup)."""
        self._process_registry.pop(pid, None)

    def register_thread(self, thread_id: int, description: str):
        """Register a thread for leak tracking."""
        self._thread_registry[thread_id] = description

    def unregister_thread(self, thread_id: int):
        """Unregister a thread (normal cleanup)."""
        self._thread_registry.pop(thread_id, None)

    def get_active_warnings(self) -> list[dict[str, Any]]:
        """Get list of active warnings for display."""
        warnings: list[dict[str, Any]] = []
        warnings.extend({"type": warning, "active": True} for warning in self._active_warnings)
        return warnings

    def get_thresholds(self) -> dict[str, float]:
        """Get configured threshold values."""
        return {
            "cpu": self._cpu_threshold,
            "memory": self._memory_threshold,
            "disk_gb": self._disk_threshold_gb,
        }

    def get_final_summary(self) -> dict[str, Any] | None:
        """Get final health metrics snapshot for shutdown display."""
        if not self._started:
            return None
        try:
            return self._collect_metrics()
        except Exception:  # pylint: disable=broad-except
            return None

    def _collect_metrics(self) -> dict[str, Any]:
        data: dict[str, Any] = {"running_tasks": self._running_tasks_supplier()}
        # Disk space check
        if self._log_directory:
            with contextlib.suppress(OSError, RuntimeError):
                disk_usage = shutil.disk_usage(self._log_directory)
                disk_free_gb = disk_usage.free / (1024**3)
                rounded_disk = round(disk_free_gb, 2)
                data["disk_free_gb"] = rounded_disk
                self._handle_threshold_event(
                    warning_key="disk_low",
                    current_value=rounded_disk,
                    threshold=self._disk_threshold_def,
                    log_payload={
                        "threshold_type": "disk_space",
                        "free_gb": rounded_disk,
                        "threshold_gb": self._disk_threshold_gb,
                    },
                )
        if psutil and self._proc:
            try:
                self._extracted_from__collect_metrics_26(data)
            except Exception as ex:  # pylint: disable=broad-except
                # Best-effort metrics; do not let psutil glitches break shutdown
                self._logger.log(
                    "health_monitor_sampling_error",
                    LogLevel.WARNING,
                    error=str(ex),
                )
                # Provide minimal fallback
                try:
                    data.setdefault("thread_count", self._proc.num_threads())
                except Exception as e:
                    self._logger.log(
                        "health_thread_count_fallback_failed",
                        LogLevel.DEBUG,
                        scope=LogScope.FRAMEWORK,
                        error=str(e),
                    )

            # Check CPU threshold (only if successfully sampled)
            self._handle_threshold_event(
                warning_key="cpu_high",
                current_value=data.get("process_cpu_percent"),
                threshold=self._cpu_threshold_def,
                log_payload={
                    "threshold_type": "cpu",
                    "cpu_percent": data.get("process_cpu_percent"),
                    "threshold": self._cpu_threshold,
                },
            )

            # Check memory threshold (only if successfully sampled)
            self._handle_threshold_event(
                warning_key="memory_high",
                current_value=data.get("process_memory_percent"),
                threshold=self._memory_threshold_def,
                log_payload={
                    "threshold_type": "memory",
                    "memory_percent": data.get("process_memory_percent"),
                    "threshold": self._memory_threshold,
                },
            )

            # open file descriptors (Unix)
            # Open file descriptors (Unix only)
            with contextlib.suppress(OSError, RuntimeError):
                if sys.platform != "win32" and hasattr(self._proc, "open_files"):
                    # Approximate via count of open files list
                    data["open_fds"] = len(self._proc.open_files())
        else:
            # Fallback minimal stats
            data["thread_count"] = threading.active_count()
        return data

    def _handle_threshold_event(
        self,
        warning_key: str,
        current_value: float | None,
        threshold: Threshold,
        log_payload: dict[str, Any],
    ) -> None:
        """Update warning state and emit logs when thresholds trip."""

        if current_value is None:
            self._active_warnings.discard(warning_key)
            return

        try:
            numeric_value = float(current_value)
        except (TypeError, ValueError):
            self._active_warnings.discard(warning_key)
            return

        if is_threshold_triggered(numeric_value, threshold):
            if warning_key not in self._active_warnings:
                self._active_warnings.add(warning_key)
                self._logger.log(
                    "threshold_exceeded",
                    LogLevel.WARNING,
                    **log_payload,
                )
        else:
            self._active_warnings.discard(warning_key)

    def _extracted_from__collect_metrics_26(self, data):
        # CPU percent: first call returns 0.0, subsequent gives actual. Call once ahead?
        if not self._proc or not psutil:
            return
        cpu_proc = self._proc.cpu_percent(interval=None)  # percentage since last call
        cpu_sys = psutil.cpu_percent(interval=None)  # system-wide

        # Some psutil builds use a per-process cache set by oneshot(); ensure presence
        if not hasattr(self._proc, "_cache"):
            try:
                # best-effort guard - cache will be initialized on first access
                pass
            except Exception as e:
                self._logger.log(
                    "health_psutil_cache_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    error=str(e),
                )

        try:
            mem_info = self._proc.memory_info()
        except AttributeError:
            # Recreate Process handle and retry once
            self._proc = psutil.Process(self._pid)
            mem_info = self._proc.memory_info()

        try:
            mem_percent = self._proc.memory_percent()
        except (RuntimeError, OSError, AttributeError):  # pragma: no cover
            mem_percent = None

        data.update(
            {
                "process_cpu_percent": round(cpu_proc, 2),
                "system_cpu_percent": round(cpu_sys, 2),
                "process_memory_rss_bytes": getattr(mem_info, "rss", 0),
                "process_memory_rss_mb": round(getattr(mem_info, "rss", 0) / (1024**2), 2),
                "process_memory_percent": (round(mem_percent, 2) if mem_percent else None),
                "thread_count": self._proc.num_threads(),
            }
        )

    def _run(self):
        # Prime psutil CPU percent for meaningful next sample
        if psutil and self._proc:
            self._proc.cpu_percent(interval=None)
            psutil.cpu_percent(interval=None)
        next_time = time.time() + self._interval
        while not self._stop_event.is_set():
            now = time.time()
            if now >= next_time:
                metrics = self._collect_metrics()
                # Log structured health snapshot
                self._logger.log(
                    "health_snapshot",
                    LogLevel.INFO,
                    **metrics,
                )
                next_time = now + self._interval
            time.sleep(1)


__all__ = ["HealthMonitor"]
