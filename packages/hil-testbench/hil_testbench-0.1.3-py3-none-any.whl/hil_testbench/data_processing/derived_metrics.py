"""Derived metrics engine for synthesized parameters (ratios, rolling averages, logical)."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Any

from hil_testbench.data_structs.parameters import DerivedSpec, ParameterField, ParametersSchema


class DerivedMetricsEngine:
    """Compute derived parameters from incoming parameter events."""

    def __init__(self, schema: ParametersSchema | None) -> None:
        self._schema = schema
        self._fields: dict[str, ParameterField] = {}
        self._derived_fields: dict[str, ParameterField] = {}
        self._deps: dict[str, list[str]] = defaultdict(list)
        self._history: dict[str, deque[tuple[float, Any]]] = defaultdict(lambda: deque(maxlen=256))
        self._max_windows: dict[str, float] = {}

        if not schema:
            return

        for field in schema.fields:
            self._fields[field.name] = field
            if field.derived_from:
                self._derived_fields[field.name] = field

        for name, field in self._derived_fields.items():
            spec = field.derived_from
            if spec is None:
                continue
            for source in self._sources_for_spec(spec):
                self._deps[source].append(name)
                window = spec.window_seconds or field.aggregation_window_seconds or 0.0
                if window:
                    self._max_windows[source] = max(self._max_windows.get(source, 0.0), window)

    def ingest(self, event: dict[str, Any]) -> list[dict[str, Any]]:
        """Ingest a base event and return any derived events generated."""

        param = event.get("param_name")
        if not param:
            return []

        timestamp = float(event.get("timestamp") or time.time())
        value = event.get("value")
        self._history[param].append((timestamp, value))
        self._prune_history(param, timestamp)

        derived: list[dict[str, Any]] = []
        for derived_name in self._deps.get(param, ()):
            computed = self._compute_derived(derived_name, timestamp)
            if computed is None:
                continue
            derived.append(computed)
        return derived

    def _compute_derived(self, name: str, timestamp: float) -> dict[str, Any] | None:
        field = self._derived_fields.get(name)
        spec = field.derived_from if field else None
        if not field or not spec:
            return None

        dtype = spec.type.lower()
        if dtype == "ratio":
            value = self._compute_ratio(spec, field)
        elif dtype == "rolling_avg":
            value = self._compute_rolling_avg(spec, field)
        elif dtype == "logical_all_pass":
            value = self._compute_logical(spec, require_all=True)
        elif dtype == "logical_any_fail":
            value = self._compute_logical(spec, require_all=False)
        else:
            return None

        if value is None:
            return None

        return {
            "param_name": name,
            "value": value,
            "timestamp": timestamp,
            "metadata": {"derived": True, "sources": self._sources_for_spec(spec)},
        }

    def _compute_ratio(self, spec: DerivedSpec, field: ParameterField) -> float | None:
        num = self._latest_value(spec.numerator)
        denom = self._latest_value(spec.denominator)
        try:
            if num is None or denom in (None, 0, 0.0):
                return None
            ratio = float(num) / float(denom)
            if spec.multiplier is not None:
                ratio *= float(spec.multiplier)
            elif field.unit == "%":
                ratio *= 100.0
            return ratio
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    def _compute_rolling_avg(self, spec: DerivedSpec, field: ParameterField) -> float | None:
        source = spec.source or (spec.sources[0] if spec.sources else None)
        if not source:
            return None
        window = spec.window_seconds or field.aggregation_window_seconds
        if not window:
            return None
        cutoff = time.time() - float(window)
        samples = [
            float(v)
            for ts, v in self._history.get(source, ())
            if ts >= cutoff and _is_numeric(v)
        ]
        if not samples:
            return None
        return sum(samples) / len(samples)

    def _compute_logical(self, spec: DerivedSpec, *, require_all: bool) -> str | None:
        sources = self._sources_for_spec(spec)
        if not sources:
            return None

        values = [self._latest_value(src) for src in sources]
        normalized = [_normalize_status_value(v) for v in values if v is not None]
        if not normalized:
            return None

        if require_all:
            if any(val == "bad" for val in normalized):
                return "bad"
            if any(val == "warn" for val in normalized):
                return "warn"
            return "good"
        if any(val == "bad" for val in normalized):
            return "bad"
        if any(val == "warn" for val in normalized):
            return "warn"
        return "good"

    def _latest_value(self, name: str | None) -> Any | None:
        if not name:
            return None
        hist = self._history.get(name)
        if not hist:
            return None
        return hist[-1][1]

    def _prune_history(self, param: str, now: float) -> None:
        window = self._max_windows.get(param)
        if not window:
            return
        cutoff = now - window
        hist = self._history.get(param)
        if not hist:
            return
        while hist and hist[0][0] < cutoff:
            hist.popleft()

    @staticmethod
    def _sources_for_spec(spec: DerivedSpec) -> tuple[str, ...]:
        if spec.sources:
            return spec.sources
        candidates: list[str] = []
        for attr in (spec.numerator, spec.denominator, spec.source):
            if attr:
                candidates.append(attr)
        return tuple(candidates)


def _normalize_status_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, str):
        upper = value.strip().upper()
        if "FAIL" in upper or "BAD" in upper or upper in {"0", "FALSE"}:
            return "bad"
        if "WARN" in upper or upper == "WARN":
            return "warn"
        if upper in {"PASS", "GOOD", "TRUE", "1"}:
            return "good"
    try:
        numeric = float(value)
        if numeric < 0:
            return "bad"
        return "good"
    except (TypeError, ValueError):
        return "unknown"


def _is_numeric(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False
