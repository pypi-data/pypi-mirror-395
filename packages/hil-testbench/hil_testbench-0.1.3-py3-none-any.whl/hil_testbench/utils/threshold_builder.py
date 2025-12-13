"""Helpers for building schema thresholds around a nominal value.

Satisfies:
- REQS012 (schema centralizes parameter metadata, including thresholds)
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, cast

from hil_testbench.data_structs.parameters import Threshold
from hil_testbench.data_structs.threshold_utils import build_threshold_from_spec

Number = int | float
ValuePair = tuple[float, float]
ValueResult = float | ValuePair
ValueCallable = Callable[[float, str, str], ValueResult]
ToleranceCallable = Callable[[float, str, str], ValueResult]


def build_nominal_thresholds(
    *,
    nominal: Number,
    levels: Mapping[str, Any],
    default_mode: str = "range",
    default_colors: Mapping[str, str] | None = None,
) -> dict[str, Threshold]:
    """Return Threshold objects derived from a nominal value and tolerance specs."""

    anchor = _coerce_float(nominal, "nominal")
    if not isinstance(levels, Mapping) or not levels:
        raise ValueError("levels must be a non-empty mapping")

    thresholds: dict[str, Threshold] = {}
    for level_name, raw_spec in levels.items():
        if raw_spec is None:
            continue
        thresholds[level_name] = _build_threshold(
            level_name=level_name,
            raw_spec=raw_spec,
            anchor=anchor,
            default_mode=default_mode,
            default_colors=default_colors or {},
        )

    if not thresholds:
        raise ValueError("no thresholds could be resolved from level specifications")
    return thresholds


def _build_threshold(
    *,
    level_name: str,
    raw_spec: Any,
    anchor: float,
    default_mode: str,
    default_colors: Mapping[str, str],
) -> Threshold:
    if isinstance(raw_spec, Threshold):
        return raw_spec

    if not isinstance(raw_spec, Mapping):
        return build_threshold_from_spec(level_name, raw_spec)

    spec = dict(raw_spec)
    mode = (spec.get("mode") or spec.get("operator") or default_mode).lower()
    color = spec.get("color") or default_colors.get(level_name)
    description = spec.get("description", "")

    manual_value = spec.get("value")
    tolerance_spec = spec.get("tolerance")
    calc_callable = spec.get("calc")
    target_anchor = _coerce_float(spec.get("anchor", anchor), f"anchor for '{level_name}'")

    if manual_value is not None and tolerance_spec is None and calc_callable is None:
        value = manual_value
    elif callable(calc_callable):
        value_callable = cast(ValueCallable, calc_callable)
        value = _normalize_value(value_callable, target_anchor, level_name, mode)
    else:
        value = _build_value_from_tolerance(
            tolerance_spec=tolerance_spec,
            mode=mode,
            anchor=target_anchor,
            level_name=level_name,
        )

    resolved_spec: dict[str, Any] = {
        "value": value,
        "operator": mode,
    }
    if color:
        resolved_spec["color"] = color
    if description:
        resolved_spec["description"] = description

    return build_threshold_from_spec(
        level_name,
        resolved_spec,
        default_operator=mode,
        default_color=color,
    )


def _build_value_from_tolerance(
    *,
    tolerance_spec: Any,
    mode: str,
    anchor: float,
    level_name: str,
) -> float | tuple[float, float]:
    if tolerance_spec is None:
        return anchor if mode != "range" else (anchor, anchor)

    if callable(tolerance_spec):
        tolerance_callable = cast(ToleranceCallable, tolerance_spec)
        return _normalize_value(tolerance_callable, anchor, level_name, mode)

    lower_delta, upper_delta, directive = _resolve_tolerance_deltas(
        tolerance_spec, anchor, level_name, mode
    )
    if directive == "below":
        upper_delta = 0.0
    elif directive == "above":
        lower_delta = 0.0

    return _apply_mode(anchor, mode, lower_delta, upper_delta)


def _normalize_value(
    func: ValueCallable | ToleranceCallable,
    anchor: float,
    level_name: str,
    mode: str,
) -> float | tuple[float, float]:
    result = func(anchor, level_name, mode)
    if isinstance(result, (list, tuple)):
        if len(result) != 2:
            raise ValueError(
                f"Callable for '{level_name}' must return scalar or two-value sequence"
            )
        return float(result[0]), float(result[1])
    return float(result)


def _resolve_tolerance_deltas(
    tolerance_spec: Any,
    anchor: float,
    level_name: str,
    mode: str,
) -> tuple[float, float, str | None]:
    if isinstance(tolerance_spec, (int, float)):
        delta = abs(float(tolerance_spec))
        return delta, delta, None

    if isinstance(tolerance_spec, (list, tuple)):
        if len(tolerance_spec) != 2:
            raise ValueError("tolerance tuples must contain exactly two entries")
        return abs(float(tolerance_spec[0])), abs(float(tolerance_spec[1])), None

    if isinstance(tolerance_spec, Mapping):
        return _resolve_mapping_tolerance(tolerance_spec, anchor, level_name, mode)

    raise ValueError("Unsupported tolerance specification type")


def _resolve_mapping_tolerance(
    spec: Mapping[str, Any],
    anchor: float,
    level_name: str,
    mode: str,
) -> tuple[float, float, str | None]:
    direction = _normalize_direction(spec.get("direction"))
    lower_delta = 0.0
    upper_delta = 0.0

    def _update_from_percent(pair_source: Any) -> None:
        nonlocal lower_delta, upper_delta
        lpct, upct = _split_pair(pair_source)
        lower_delta, upper_delta = _update_deltas(
            lower_delta,
            upper_delta,
            _scale_pair((lpct, upct), anchor),
        )

    pct_value = spec.get("pct") or spec.get("percent")
    if pct_value is not None:
        _update_from_percent(pct_value)

    lower_pct = _coerce_optional_float(spec.get("lower_pct"))
    if lower_pct is not None:
        lower_delta = max(lower_delta, abs(anchor * lower_pct))
    upper_pct = _coerce_optional_float(spec.get("upper_pct"))
    if upper_pct is not None:
        upper_delta = max(upper_delta, abs(anchor * upper_pct))

    abs_value = spec.get("abs") or spec.get("absolute")
    if abs_value is not None:
        lower_delta, upper_delta = _update_deltas(
            lower_delta,
            upper_delta,
            _split_pair(abs_value),
        )

    lower_abs = _coerce_optional_float(spec.get("lower_abs"))
    if lower_abs is not None:
        lower_delta = max(lower_delta, abs(lower_abs))
    upper_abs = _coerce_optional_float(spec.get("upper_abs"))
    if upper_abs is not None:
        upper_delta = max(upper_delta, abs(upper_abs))

    calc_candidate = spec.get("calc")
    if callable(calc_candidate):
        calc_callable = cast(ToleranceCallable, calc_candidate)
        lower_val, upper_val = _split_pair(calc_callable(anchor, level_name, mode))
        lower_delta, upper_delta = _update_deltas(
            lower_delta,
            upper_delta,
            (lower_val, upper_val),
        )

    return lower_delta, upper_delta, direction


def _apply_mode(
    anchor: float,
    mode: str,
    lower_delta: float,
    upper_delta: float,
) -> float | tuple[float, float]:
    if mode == "lt":
        return anchor - (lower_delta or upper_delta)
    if mode == "gt":
        return anchor + (upper_delta or lower_delta)
    if mode == "eq":
        return anchor

    lower_bound = anchor - lower_delta
    upper_bound = anchor + upper_delta
    if lower_bound > upper_bound:
        lower_bound, upper_bound = upper_bound, lower_bound
    return lower_bound, upper_bound


def _split_pair(value: Any) -> tuple[float, float]:
    if isinstance(value, (int, float)):
        scalar = float(value)
        return scalar, scalar
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            raise ValueError("pair values must contain exactly two entries")
        return float(value[0]), float(value[1])
    if isinstance(value, Mapping):
        lower_val = _coerce_optional_float(value.get("lower"))
        upper_val = _coerce_optional_float(value.get("upper"))
        return (
            float(lower_val) if lower_val is not None else 0.0,
            float(upper_val) if upper_val is not None else 0.0,
        )
    raise ValueError("Unsupported pair specification")


def _update_deltas(
    current_lower: float,
    current_upper: float,
    candidate: tuple[float, float],
) -> tuple[float, float]:
    proposed_lower, proposed_upper = candidate
    return max(current_lower, abs(proposed_lower)), max(current_upper, abs(proposed_upper))


def _scale_pair(values: tuple[float, float], scale: float) -> tuple[float, float]:
    return values[0] * scale, values[1] * scale


def _normalize_direction(raw: Any) -> str | None:
    if not raw:
        return None
    direction = str(raw).lower()
    if direction in {"below", "lower"}:
        return "below"
    if direction in {"above", "upper"}:
        return "above"
    return None


def _coerce_float(value: Any, context: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{context} must be numeric, got {value!r}") from exc


def _coerce_optional_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    return float(value)


__all__ = ["build_nominal_thresholds"]
