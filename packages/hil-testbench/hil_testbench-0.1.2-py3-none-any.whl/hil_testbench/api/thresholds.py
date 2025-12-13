"""Threshold helpers for task schema declarations."""

from __future__ import annotations

from typing import Any

__all__ = [
    "spec",
    "good",
    "warn",
    "bad",
    "range_spec",
]


def spec(
    value: Any,
    *,
    operator: str | None = None,
    color: str | None = None,
    description: str = "",
) -> dict[str, Any]:
    """Create a threshold specification mapping."""

    payload: dict[str, Any] = {"value": value}
    if operator is not None:
        payload["operator"] = operator
    if color is not None:
        payload["color"] = color
    if description:
        payload["description"] = description
    return payload


def good(
    value: Any,
    *,
    operator: str = "lt",
    color: str = "green",
    description: str = "",
) -> dict[str, Any]:
    """Return a 'good' threshold specification."""

    return spec(value, operator=operator, color=color, description=description)


def warn(
    value: Any,
    *,
    operator: str = "range",
    color: str = "yellow",
    description: str = "",
) -> dict[str, Any]:
    """Return a 'warn' threshold specification."""

    return spec(value, operator=operator, color=color, description=description)


def bad(
    value: Any,
    *,
    operator: str = "gt",
    color: str = "red",
    description: str = "",
) -> dict[str, Any]:
    """Return a 'bad' threshold specification."""

    return spec(value, operator=operator, color=color, description=description)


def range_spec(
    lower: Any,
    upper: Any,
    *,
    color: str | None = None,
    description: str = "",
) -> dict[str, Any]:
    """Return a range threshold specification."""

    return spec((lower, upper), operator="range", color=color, description=description)
