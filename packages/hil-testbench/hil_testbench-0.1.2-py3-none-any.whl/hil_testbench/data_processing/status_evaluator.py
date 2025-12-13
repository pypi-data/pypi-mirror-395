"""Centralized parameter status evaluation."""

from __future__ import annotations

from typing import Any

from hil_testbench.data_structs.parameters import ParameterField
from hil_testbench.data_structs.threshold_utils import is_threshold_triggered


def evaluate_param_status(field: ParameterField, value: Any) -> str:
    """Return health classification for a parameter value."""

    if value is None:
        return "unknown"

    numeric = _coerce_float(value)
    if numeric is None:
        return "unknown"

    severity = _evaluate_thresholds(field, numeric)
    if severity != "unknown":
        return severity

    goal = field.goal
    direction = (field.direction or "").lower()

    if goal is None:
        return "unknown"

    goal_numeric = _coerce_float(goal, numeric)
    if goal_numeric is None:
        return "unknown"

    if direction == "higher_better":
        return "good" if numeric >= goal_numeric else "bad"
    if direction == "lower_better":
        return "good" if numeric <= goal_numeric else "bad"
    if direction == "equal_target":
        return "good" if numeric == goal_numeric else "bad"
    if direction == "in_range":
        if isinstance(goal, tuple) and len(goal) == 2:
            return "good" if goal[0] <= numeric <= goal[1] else "bad"
    return "unknown"


def _evaluate_thresholds(field: ParameterField, numeric: float) -> str:
    if not field.thresholds:
        return "unknown"

    best = "good"
    for level, threshold in field.thresholds.items():
        if not is_threshold_triggered(numeric, threshold):
            continue
        severity = _severity_from_level(level, threshold.color)
        if severity == "bad":
            return "bad"
        if severity == "warn":
            best = "warn"
    return best if best != "good" else "good"


def _severity_from_level(level: str, color: str | int | None) -> str:
    key = (level or "").lower()
    if "bad" in key or "error" in key or str(color).lower() in {"red"}:
        return "bad"
    if "warn" in key or str(color).lower() in {"yellow"}:
        return "warn"
    return "good"


def _coerce_float(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
