"""Interval helpers for streaming and scheduling."""

from __future__ import annotations


def normalize_interval(value: float | int | str | None, default: float = 1.0) -> float:
    """Normalize an interval value to a positive float.

    Empty/None -> default. Negative or zero -> default. Strings are parsed as float.
    """

    if value in (None, ""):
        return float(default)

    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return float(default)

    if parsed <= 0:
        return float(default)
    return parsed


def format_interval_arg(value: float | int | str | None, default: float = 1.0) -> str:
    """Return a CLI-friendly interval argument from a value."""

    normalized = normalize_interval(value, default=default)
    # iperf accepts fractional seconds; keep as compact as possible
    if normalized.is_integer():
        return str(int(normalized))
    return str(normalized)
