"""Time-windowed aggregation helpers for derived parameters."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TimeWindowedStats:
    """Maintain rolling windows for common aggregation periods."""

    window_1min: deque[tuple[float, Any]] = field(default_factory=lambda: deque(maxlen=60))
    window_5min: deque[tuple[float, Any]] = field(default_factory=lambda: deque(maxlen=300))
    window_1hour: deque[tuple[float, Any]] = field(default_factory=lambda: deque(maxlen=3600))

    def append(self, timestamp: float, value: Any) -> None:
        entry = (timestamp, value)
        self.window_1min.append(entry)
        self.window_5min.append(entry)
        self.window_1hour.append(entry)

    def avg_1min(self) -> float | None:
        return self._avg(self.window_1min)

    def avg_5min(self) -> float | None:
        return self._avg(self.window_5min)

    def avg_1hour(self) -> float | None:
        return self._avg(self.window_1hour)

    def max_1hour(self) -> float | None:
        values = [v for _, v in self.window_1hour if isinstance(v, (int, float))]
        return max(values) if values else None

    def min_1hour(self) -> float | None:
        values = [v for _, v in self.window_1hour if isinstance(v, (int, float))]
        return min(values) if values else None

    def _avg(self, window: deque[tuple[float, Any]]) -> float | None:
        values = [v for _, v in window if isinstance(v, (int, float))]
        return sum(values) / len(values) if values else None


class TimeWindowedStatsRegistry:
    """Registry of windowed stats per parameter name."""

    def __init__(self) -> None:
        self._stats: dict[str, TimeWindowedStats] = {}

    def get(self, key: str) -> TimeWindowedStats:
        if key not in self._stats:
            self._stats[key] = TimeWindowedStats()
        return self._stats[key]

    def clear(self) -> None:
        self._stats.clear()


__all__ = ["TimeWindowedStats", "TimeWindowedStatsRegistry"]
