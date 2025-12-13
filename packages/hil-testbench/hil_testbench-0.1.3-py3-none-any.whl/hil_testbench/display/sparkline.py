"""Sparkline rendering helpers with per-sample threshold coloring."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

ThresholdState = Literal["good", "warn", "bad"]

_BLOCKS = "▁▂▃▄▅▆▇█"
_STATE_COLORS: dict[str, str] = {
    "good": "green",
    "warn": "yellow",
    "bad": "red",
}


def _coerce_float_values(values: Sequence[float]) -> list[float]:
    """Return a copy of values as floats, ignoring non-numeric entries."""

    coerced: list[float] = []
    for value in values:
        try:
            coerced.append(float(value))
        except (TypeError, ValueError):
            continue
    return coerced


def _normalize_to_blocks(values: Sequence[float]) -> list[str]:
    """Map numeric values onto sparkline block characters."""

    if not values:
        return []

    v_min = min(values)
    v_max = max(values)
    if v_min == v_max:
        return [_BLOCKS[0]] * len(values)

    span = v_max - v_min
    blocks: list[str] = []
    for value in values:
        ratio = (value - v_min) / span
        idx = min(len(_BLOCKS) - 1, max(0, int(ratio * (len(_BLOCKS) - 1))))
        blocks.append(_BLOCKS[idx])
    return blocks


def render_colored_sparkline(
    values: Sequence[float],
    states: Sequence[ThresholdState | None],
    *,
    max_width: int | None = None,
    enable_color: bool = True,
) -> tuple[str, bool]:
    """Render a sparkline string with optional per-sample coloring.

    Args:
        values: Numeric history, newest sample last.
        states: Threshold classification history aligned with ``values``.
        max_width: Optional maximum number of samples to display (ellipsis added by caller).
        enable_color: Toggle for colored output.

    Returns:
        Tuple of (sparkline_string, truncated_flag).
    """

    if not values:
        return "", False

    trimmed_values = list(values)
    trimmed_states = list(states)
    truncated = False

    if max_width is not None and max_width > 0 and len(trimmed_values) > max_width:
        keep = max_width
        trimmed_values = trimmed_values[-keep:]
        trimmed_states = trimmed_states[-keep:]
        truncated = True

    if len(trimmed_states) != len(trimmed_values):
        keep = min(len(trimmed_states), len(trimmed_values))
        trimmed_values = trimmed_values[-keep:]
        trimmed_states = trimmed_states[-keep:]

    if not trimmed_values:
        return "", truncated

    blocks = _normalize_to_blocks(trimmed_values)

    if not enable_color:
        return "".join(blocks), truncated

    parts: list[str] = []
    for block, state in zip(blocks, trimmed_states, strict=False):
        color = _STATE_COLORS.get(state or "")
        if color:
            parts.append(f"[{color}]{block}[/{color}]")
        else:
            parts.append(block)
    return "".join(parts), truncated


def colorize_trend_arrow(
    arrow: str,
    states: Sequence[ThresholdState | None],
    *,
    enable_color: bool = True,
) -> str:
    """Wrap the trend arrow in threshold-color markup if enabled."""

    if not enable_color or not states:
        return arrow

    latest_state = states[-1]
    color = _STATE_COLORS.get(latest_state or "")
    if not color:
        return arrow
    return f"[{color}]{arrow}[/{color}]"
