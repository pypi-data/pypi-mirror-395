"""Helpers for aggregating shutdown-time warning summaries."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

SummaryMessageBuilder = Callable[[Sequence[str]], str | None]


def _default_message_builder(items: Sequence[str]) -> str:
    count = len(items)
    preview = ", ".join(items[:5])
    suffix = "…" if count > 5 else ""
    noun = "item" if count == 1 else "items"
    if preview:
        return f"Suppressed {count} {noun}: {preview}{suffix}"
    return f"Suppressed {count} {noun}."


@dataclass
class ShutdownSummaryBuffer:
    """Collect repeated signals while shutdown is in progress and emit one summary."""

    event_type: str
    level: LogLevel
    scope: LogScope = LogScope.COMMAND
    list_field: str = "suppressed_items"
    static_fields: dict[str, Any] = field(default_factory=dict)
    message_builder: SummaryMessageBuilder | None = None

    def __post_init__(self) -> None:
        self._items: set[str] = set()
        self._logger: TaskLogger | None = None

    def bind_logger(self, logger: TaskLogger | None) -> None:
        self._logger = logger

    def add(self, value: str | None) -> bool:
        """Record a suppressed value if shutdown aggregation is active."""

        if not value:
            return False
        logger = self._logger
        if not logger or not logger.shutdown_in_progress:
            return False
        self._items.add(value)
        return True

    def emit(self, *, task: str | None = None, **fields: Any) -> dict[str, Any] | None:
        """Emit the summary event if aggregation captured any values."""

        if not self._items:
            return None
        logger = self._logger
        if not logger or not logger.shutdown_in_progress:
            self._items.clear()
            return None

        ordered = sorted(self._items)
        payload: dict[str, Any] = {**self.static_fields, **fields}
        payload[self.list_field] = ordered
        payload["suppressed_count"] = len(ordered)
        builder = self.message_builder or _default_message_builder
        message = builder(ordered)
        if message:
            payload.setdefault("message", message)
        logger.log(
            self.event_type,
            self.level,
            scope=self.scope,
            task=task,
            **payload,
        )
        self._items.clear()
        return payload

    def clear(self) -> None:
        self._items.clear()
