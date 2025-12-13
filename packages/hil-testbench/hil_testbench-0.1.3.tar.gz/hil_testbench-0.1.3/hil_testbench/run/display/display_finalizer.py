"""Helpers for rendering final display output safely."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hil_testbench.run.execution.protocols import (
    DisplayBackendProtocol,
    SupportsRenderableConsole,
    SupportsRenderFinal,
)
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger


@dataclass(slots=True)
class DisplayFinalizer:
    """Render a display backend's final view with guarded logging."""

    task_logger: TaskLogger | None = None

    def render(self, backend: DisplayBackendProtocol | None) -> None:
        if backend is None:
            return
        if isinstance(backend, SupportsRenderFinal):
            self._attempt(lambda: backend.render_final(), "render_final")
            return
        if isinstance(backend, SupportsRenderableConsole):
            self._attempt(
                lambda: backend.console.print(backend._create_renderable()),  # noqa: SLF001  # hil: allow-print
                "console_renderable",
            )
            return
        self._log(
            "display_finalizer_unsupported_backend",
            LogLevel.DEBUG,
            details={"backend_type": type(backend).__name__},
        )

    def _attempt(self, callback, mode: str) -> None:
        try:
            callback()
        except Exception as exc:  # noqa: BLE001
            self._log(
                "display_finalizer_failed",
                LogLevel.WARNING,
                details={
                    "mode": mode,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                },
            )

    def _log(self, event: str, level: LogLevel, *, details: dict[str, Any]) -> None:
        if not self.task_logger:
            return
        self.task_logger.log(
            event,
            level,
            scope=LogScope.FRAMEWORK,
            **details,
        )


__all__ = ["DisplayFinalizer"]
