"""Shared helpers for working with Threshold specifications."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, SupportsFloat, SupportsIndex, cast

from hil_testbench.data_structs.parameters import Threshold

_RANGE_TUPLE_SIZE = 2

_DEFAULT_THRESHOLD_COLORS = {
    "good": "green",
    "warn": "yellow",
    "warning": "yellow",
    "bad": "red",
    "error": "red",
    "critical": "red",
}


def get_default_threshold_color(name: str) -> str:
    """Return fallback color for a threshold level name."""

    return _DEFAULT_THRESHOLD_COLORS.get(name.lower(), "white")


def parse_threshold_value(raw_value: Any) -> float | tuple[float, float]:
    """Convert YAML/raw threshold values into a typed representation."""

    candidate = raw_value.value if isinstance(raw_value, Threshold) else raw_value
    if isinstance(candidate, (list | tuple)) and len(candidate) == _RANGE_TUPLE_SIZE:
        try:
            return float(candidate[0]), float(candidate[1])
        except (TypeError, ValueError):
            return 0.0, 0.0
    try:
        scalar_candidate = cast(str | SupportsFloat | SupportsIndex, candidate)
        return float(scalar_candidate)
    except (TypeError, ValueError):
        return 0.0


def build_threshold_from_spec(
    threshold_name: str,
    spec: Any,
    *,
    default_operator: str | None = None,
    default_color: str | None = None,
    fallback: Threshold | None = None,
) -> Threshold:
    """Create a Threshold instance from schema/YAML specifications."""

    if isinstance(spec, Threshold):
        return _clone_threshold(spec)

    raw_value, operator, color, description = _extract_spec_parts(spec)
    mode = _resolve_mode(operator, raw_value, fallback, default_operator)

    parsed_value = raw_value if mode.startswith("formula") else parse_threshold_value(raw_value)
    resolved_color = _resolve_color(color, threshold_name, fallback, default_color)
    resolved_description = _resolve_description(description, fallback)

    return Threshold(
        value=parsed_value,
        mode=mode,
        color=resolved_color,
        description=resolved_description,
    )


def _clone_threshold(spec: Threshold) -> Threshold:
    return Threshold(
        value=parse_threshold_value(spec.value),
        mode=spec.mode,
        color=spec.color,
        description=spec.description,
    )


def _extract_spec_parts(spec: Any) -> tuple[Any, str | None, str | None, str]:
    if isinstance(spec, Mapping):
        return (
            spec.get("value"),
            spec.get("operator"),
            spec.get("color"),
            spec.get("description", ""),
        )
    return spec, None, None, ""


def _resolve_mode(
    operator: str | None,
    value_candidate: Any,
    fallback: Threshold | None,
    default_operator: str | None,
) -> str:
    inferred_operator = "range" if isinstance(value_candidate, tuple) else "gt"
    return (
        operator or (fallback.mode if fallback else None) or default_operator or inferred_operator
    )


def _resolve_color(
    color: str | None,
    threshold_name: str,
    fallback: Threshold | None,
    default_color: str | None,
) -> str:
    if color is not None:
        return color
    if fallback is not None and fallback.color is not None:
        return str(fallback.color)
    if default_color is not None:
        return default_color
    return get_default_threshold_color(threshold_name)


def _resolve_description(description: str, fallback: Threshold | None) -> str:
    if description:
        return description
    return fallback.description if fallback is not None else ""


def is_threshold_triggered(numeric_value: float, threshold: Threshold) -> bool:
    """Return True when the numeric value violates the threshold definition."""

    lower = threshold.min
    upper = threshold.max

    if threshold.mode == "gt":
        return numeric_value > lower
    if threshold.mode == "lt":
        return numeric_value < upper
    if threshold.mode in {"range", "eq"}:
        return lower <= numeric_value <= upper
    return False


__all__ = [
    "build_threshold_from_spec",
    "get_default_threshold_color",
    "is_threshold_triggered",
    "parse_threshold_value",
]
