"""Thread-safe shared parameter context for derived calculations."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from threading import RLock
from typing import Any


@dataclass
class ParameterContext:
    """Holds latest parameter values with timestamps (LRU bounded)."""

    _data: OrderedDict[str, tuple[Any, float]] = field(default_factory=OrderedDict)
    _lock: RLock = field(default_factory=RLock)
    _max_params: int = 10000
    _staleness_threshold_seconds: float = 30.0

    def set(self, key: str, value: Any, timestamp: float) -> None:
        """Store parameter value with timestamp (LRU eviction)."""

        with self._lock:
            if key in self._data:
                del self._data[key]
            self._data[key] = (value, float(timestamp))
            if len(self._data) > self._max_params:
                self._data.popitem(last=False)

    def get(self, key: str) -> Any | None:
        """Return latest value for key, or None if absent."""

        with self._lock:
            entry = self._data.get(key)
            return entry[0] if entry else None

    def has(self, key: str) -> bool:
        """Return True if key is present."""

        with self._lock:
            return key in self._data

    def is_stale(self, key: str, now: datetime) -> bool:
        """Return True if key is missing or older than staleness threshold."""

        with self._lock:
            entry = self._data.get(key)
            if not entry:
                return True
            _, timestamp = entry
            age = now.timestamp() - timestamp
            return age >= self._staleness_threshold_seconds

    def as_dict(self) -> dict[str, Any]:
        """Return snapshot of current values (value only)."""

        with self._lock:
            return {k: v for k, (v, _) in self._data.items()}

    def clear(self) -> None:
        """Clear all stored values."""

        with self._lock:
            self._data.clear()


__all__ = ["ParameterContext"]
