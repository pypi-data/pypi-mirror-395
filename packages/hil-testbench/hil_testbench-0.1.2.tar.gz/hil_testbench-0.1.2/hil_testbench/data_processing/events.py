"""Event definitions for data processing pipelines."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

CommandOutputCallback = Callable[["CommandOutputEvent"], None]
CommandOutputCallbackFactory = Callable[[str], CommandOutputCallback]


@dataclass(slots=True)
class CommandOutputEvent:
    """Structured event emitted from the execution layer.

    The streaming dispatcher converts raw command output into CommandOutputEvent
    instances. Each event may contain a batch of parsed records ready for the
    data pipeline to write to sinks and update the display layer. The legacy
    line-based callbacks are still supported by converting lines into these
    events at the pipeline boundary until the dispatcher is fully deployed.
    """

    records: list[dict[str, Any]] = field(default_factory=list)
    raw_line: str | None = None
    is_error: bool = False
    stream: str = "stdout"
    metadata: dict[str, Any] | None = None

    def has_records(self) -> bool:
        return bool(self.records)
