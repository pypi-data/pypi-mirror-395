"""Schema builder - converts dict schemas to ParametersSchema.

Supports minimal forms (int, float) and full specifications.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from hil_testbench.data_structs.parameters import (
    CalculatedParameter,
    DerivedSpec,
    ExtractionRule,
    ParameterField,
    ParametersSchema,
)
from hil_testbench.data_structs.threshold_utils import build_threshold_from_spec

RESERVED_KEYS = {"staleness_threshold_seconds"}


def _coerce_float(value: Any, default: float, context: str) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise ValueError(f"{context} must be numeric, got {value!r}") from exc


def _coerce_int(value: Any, default: int, context: str) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise ValueError(f"{context} must be an integer, got {value!r}") from exc


def _build_thresholds(field_name: str, thresholds_spec: Any | None) -> dict[str, Any]:
    if thresholds_spec is None:
        return {}
    if not isinstance(thresholds_spec, dict):
        raise ValueError(
            f"Schema field '{field_name}' thresholds must be dict, got {type(thresholds_spec)}"
        )

    return {
        threshold_name: build_threshold_from_spec(
            threshold_name,
            threshold_spec,
        )
        for threshold_name, threshold_spec in thresholds_spec.items()
    }


def _build_extraction_rule(field_name: str, extract_spec: Any | None) -> ExtractionRule | None:
    if extract_spec is None:
        return None
    if not isinstance(extract_spec, dict):
        raise ValueError(
            f"Schema field '{field_name}' extract must be dict, got {type(extract_spec)}"
        )

    method = extract_spec.get("method")
    if not method:
        raise ValueError(f"Schema field '{field_name}' extract must have 'method'")

    group_index = _coerce_int(
        extract_spec.get("group", 1),
        default=1,
        context=f"Schema field '{field_name}' extract group",
    )

    return ExtractionRule(
        method=method,
        pattern=extract_spec.get("pattern"),
        group=group_index,
        path=extract_spec.get("path"),
        column=extract_spec.get("column"),
        transform=extract_spec.get("transform"),
    )


def _normalize_dependencies(field_name: str, deps: Any | None) -> tuple[str, ...]:
    if deps is None:
        return ()
    if isinstance(deps, str):
        return (deps,)
    if isinstance(deps, (list, tuple, set)):
        normalized: list[str] = []
        for dep in deps:
            if not isinstance(dep, str) or not dep:
                raise ValueError(
                    f"Schema field '{field_name}' dependencies must be non-empty strings"
                )
            normalized.append(dep)
        return tuple(normalized)
    raise ValueError(f"Schema field '{field_name}' dependencies must be a string or sequence")


def _build_calc_callable(
    field_name: str, spec: Mapping[str, Any]
) -> tuple[Callable[[Mapping[str, Any]], Any] | None, str | None]:
    calc_fn = spec.get("calc")
    expr = spec.get("expr")

    if calc_fn is not None and not callable(calc_fn):
        raise ValueError(f"Schema field '{field_name}' calc must be callable, got {type(calc_fn)}")
    if expr is not None and not isinstance(expr, str):
        raise ValueError(f"Schema field '{field_name}' expr must be a string, got {type(expr)}")
    if calc_fn is not None and expr is not None:
        raise ValueError(f"Schema field '{field_name}' cannot define both 'calc' and 'expr'")

    if expr is not None:
        expr_source = expr
        compiled = compile(expr_source, f"<calc:{field_name}>", "eval")

        def _expr_calc(values: Mapping[str, Any]) -> Any:
            return eval(compiled, {"__builtins__": {}}, dict(values))

        return _expr_calc, expr_source

    return calc_fn, None


def _normalize_sources(field_name: str, sources: Any | None) -> tuple[str, ...]:
    if sources is None:
        return ()
    if isinstance(sources, str):
        return (sources,)
    if isinstance(sources, (list, tuple, set)):
        normalized: list[str] = []
        for src in sources:
            if not isinstance(src, str) or not src:
                raise ValueError(f"Schema field '{field_name}' derived_from sources must be strings")
            normalized.append(src)
        return tuple(normalized)
    raise ValueError(f"Schema field '{field_name}' derived_from sources must be string or sequence")


def _build_derived_spec(field_name: str, spec: Any | None) -> DerivedSpec | None:
    if spec is None:
        return None
    if not isinstance(spec, Mapping):
        raise ValueError(
            f"Schema field '{field_name}' derived_from must be a mapping if provided, got {type(spec)}"
        )

    dtype = spec.get("type")
    if not dtype or not isinstance(dtype, str):
        raise ValueError(f"Schema field '{field_name}' derived_from.type must be a non-empty string")

    sources = _normalize_sources(field_name, spec.get("sources"))
    numerator = spec.get("numerator")
    denominator = spec.get("denominator")
    source = spec.get("source")
    window = spec.get("window_seconds")
    rule = spec.get("rule")
    multiplier = spec.get("multiplier")

    if window is not None:
        window = _coerce_float(window, default=0.0, context=f"Schema field '{field_name}' window_seconds")

    return DerivedSpec(
        type=dtype,
        numerator=numerator,
        denominator=denominator,
        source=source,
        sources=sources,
        window_seconds=window,
        rule=rule,
        multiplier=multiplier if multiplier is None else float(multiplier),
    )


def _build_field(
    name: str, spec: Any
) -> tuple[ParameterField, Callable[[Mapping[str, Any]], Any] | None]:
    if isinstance(spec, type):
        return ParameterField(name=name, type=spec), None

    if not isinstance(spec, dict):
        raise ValueError(f"Schema field '{name}' must be a type or dict, got {type(spec)}")

    calc_callable, calc_expr = _build_calc_callable(name, spec)
    field_type = spec.get("type")
    if not field_type:
        raise ValueError(f"Schema field '{name}' must have 'type' property")

    formula = spec.get("formula")
    if formula is not None and not isinstance(formula, str):
        raise ValueError(f"Schema field '{name}' formula must be a string if provided")

    if calc_callable is not None and spec.get("extract") is not None:
        raise ValueError(f"Schema field '{name}' cannot define both 'calc' and 'extract'")

    if calc_callable is not None:
        if formula:
            raise ValueError(f"Schema field '{name}' cannot define both 'formula' and 'calc'")
        formula = calc_expr or "<calc>"

    dependencies = _normalize_dependencies(name, spec.get("dependencies"))

    agg_window = spec.get("aggregation_window_seconds")
    if agg_window is not None:
        agg_window = _coerce_float(
            agg_window,
            default=float(agg_window) if isinstance(agg_window, (int, float)) else 0.0,
            context=f"Schema field '{name}' aggregation_window_seconds",
        )

    field = ParameterField(
        name=name,
        type=field_type,
        goal=spec.get("goal"),
        aggregation_window_seconds=agg_window,
        direction=spec.get("direction", ""),
        group=spec.get("group", spec.get("display_group", "")),
        group_title=spec.get("group_title"),
        group_caption=spec.get("group_caption"),
        group_order=_coerce_int(
            spec.get("group_order", 0),
            default=0,
            context=f"Schema field '{name}' group_order",
        ),
        section_category=spec.get("section_category"),
        sparkline_style=spec.get("sparkline_style"),
        layout_hint=spec.get("layout_hint"),
        derived_from=_build_derived_spec(name, spec.get("derived_from")),
        unit=spec.get("unit", ""),
        description=spec.get("description", ""),
        thresholds=_build_thresholds(name, spec.get("thresholds")),
        precision=_coerce_int(
            spec.get("precision", 2),
            default=2,
            context=f"Schema field '{name}' precision",
        ),
        scale_strategy=spec.get("scale_strategy", "raw"),
        display_enabled=spec.get("display_enabled", True),
        display_annotation=spec.get("display_annotation", ""),
        display_format=spec.get("display_format"),
        trendline_length=_coerce_int(
            spec.get("trendline_length", 30),
            default=30,
            context=f"Schema field '{name}' trendline_length",
        ),
        trendline_window_sec=_coerce_float(
            spec.get("trendline_window_sec", 60.0),
            default=60.0,
            context=f"Schema field '{name}' trendline_window_sec",
        ),
        display_order=_coerce_int(
            spec.get("display_order", 0),
            default=0,
            context=f"Schema field '{name}' display_order",
        ),
        display_group=spec.get("display_group", ""),
        normalize_range=spec.get("normalize_range"),
        extract=_build_extraction_rule(name, spec.get("extract")),
        formula=formula,
        dependencies=dependencies,
        task=spec.get("task"),
        formula_version=spec.get("formula_version"),
    )

    return field, calc_callable


def _validate_schema(fields: list[ParameterField]) -> None:
    name_to_field = {f.name: f for f in fields}
    for field in fields:
        if field.formula and field.extract is not None:
            raise ValueError(
                f"Schema field '{field.name}' cannot define both 'formula' and 'extract'"
            )

        if not field.dependencies:
            continue

        for dep in field.dependencies:
            if "." in dep:
                continue  # allow cross-task references
            if dep not in name_to_field:
                raise ValueError(
                    f"Schema field '{field.name}' dependency '{dep}' not found in schema"
                )

    _detect_dependency_cycles({f.name: tuple(f.dependencies or ()) for f in fields if f.formula})


def _detect_dependency_cycles(graph: dict[str, tuple[str, ...]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def _dfs(node: str, path: list[str]) -> None:
        if node in visited:
            return
        if node in visiting:
            cycle = path[path.index(node) :] + [node]
            raise ValueError(
                "Circular dependency detected in derived parameters: " + " -> ".join(cycle)
            )
        visiting.add(node)
        deps = graph.get(node, ())
        for dep in deps:
            if "." in dep:
                continue  # cross-task dependency allowed
            if dep in graph:
                _dfs(dep, path + [dep])
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        _dfs(node, [node])


def build_schema(schema_dict: dict[str, Any]) -> ParametersSchema:
    """Build ParametersSchema from dictionary specification.

    Supports two forms:

    Minimal form (just type):
        {"count": int, "temp": float}

    Full form (with metadata):
        {
            "cpu_temp": {
                "type": float,
                "unit": "°C",
                "description": "CPU temperature",
                "thresholds": {"good": (0, 65), "warn": (65, 80), "bad": (80, 100)},
            }
        }

    Args:
        schema_dict: Dictionary mapping field names to type or spec dict

    Returns:
        ParametersSchema instance
    """
    fields: list[ParameterField] = []
    calculated: dict[str, CalculatedParameter] = {}

    for name, spec in schema_dict.items():
        if name in RESERVED_KEYS:
            continue
        field, calc_callable = _build_field(name, spec)
        fields.append(field)
        if calc_callable is not None:
            calculated[name] = CalculatedParameter(name=name, fn=calc_callable, field=field)

    # Extract schema-level settings (not field-specific)
    staleness_threshold_seconds = _coerce_float(
        schema_dict.get("staleness_threshold_seconds", 30.0),
        default=30.0,
        context="Schema staleness_threshold_seconds",
    )

    _validate_schema(fields)

    return ParametersSchema(
        fields=tuple(fields),
        staleness_threshold_seconds=staleness_threshold_seconds,
        calculated_params=calculated,
    )
