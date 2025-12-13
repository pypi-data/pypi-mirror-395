"""Parameter schema and threshold definitions for framework-wide use."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from typing import Any, Literal


@dataclass
class ExtractionRule:
    """Defines how to extract parameter value from tool output.

    Supports three extraction methods:
    - regex: Extract using regex pattern with capture group
    - json: Extract using JSON path notation
    - csv: Extract from CSV column by index (int) or name (str)
    """

    method: str  # "regex", "json", "csv"
    pattern: str | None = None  # regex pattern
    group: int = 1  # regex capture group number
    path: str | None = None  # JSON path (e.g., "intervals[-1].sum.bits_per_second")
    column: int | str | None = None  # CSV column index (0-based) or name
    transform: Callable[[str], Any] | None = None  # Optional value transformer


@dataclass(frozen=True, slots=True)
class Threshold:
    """Definition of a threshold for parameter monitoring."""

    value: float | tuple[float, float] | str
    mode: str  # "lt", "gt", "eq", "range", or formula-based variants
    color: str | int = ""
    description: str = ""

    @property
    def is_formula(self) -> bool:
        """Return True when this threshold is a formula-based definition."""

        return self.mode.startswith("formula_")

    @property
    def min(self) -> float:
        """Get minimum bound for range checking."""
        if self.is_formula:
            return float("-inf")
        if self.mode == "range" and isinstance(self.value, tuple):
            return float(self.value[0])
        if self.mode == "gt":
            return self._value_as_float(index=0)
        if self.mode == "eq":
            return self._value_as_float(index=0)
        return float("-inf")

    @property
    def max(self) -> float:
        """Get maximum bound for range checking."""
        if self.is_formula:
            return float("inf")
        if self.mode == "range" and isinstance(self.value, tuple):
            return float(self.value[1])
        if self.mode == "lt":
            return self._value_as_float(index=1 if isinstance(self.value, tuple) else 0)
        if self.mode == "eq":
            return self._value_as_float(index=0)
        return float("inf")

    def _value_as_float(self, index: int = 0) -> float:
        """Return numeric threshold value, handling tuple-based definitions."""

        if isinstance(self.value, tuple):
            try:
                return float(self.value[index])
            except (TypeError, ValueError):
                return 0.0
        try:
            return float(self.value)
        except (TypeError, ValueError):
            return 0.0


def _empty_thresholds() -> Mapping[str, Threshold]:
    return MappingProxyType({})


def _freeze_thresholds(
    thresholds: Mapping[str, Threshold] | dict[str, Threshold] | None,
) -> Mapping[str, Threshold]:
    if not thresholds:
        return MappingProxyType({})
    if isinstance(thresholds, MappingProxyType):
        return thresholds
    return MappingProxyType(dict(thresholds))


def _empty_calculated_params() -> Mapping[str, CalculatedParameter]:
    return MappingProxyType({})


def _freeze_calculated_params(
    calculated: Mapping[str, CalculatedParameter] | dict[str, CalculatedParameter] | None,
) -> Mapping[str, CalculatedParameter]:
    if not calculated:
        return MappingProxyType({})
    if isinstance(calculated, MappingProxyType):
        return calculated
    return MappingProxyType(dict(calculated))


@dataclass(frozen=True, slots=True)
class ParameterField:
    """Definition of a single parameter field in the schema."""

    name: str
    type: type
    goal: float | tuple[float, float] | None = None
    aggregation_window_seconds: float | None = None
    direction: str = ""
    group: str = ""
    derived_from: DerivedSpec | None = None
    unit: str = ""
    description: str = ""
    is_summary: bool = False
    is_primary: bool = False
    thresholds: Mapping[str, Threshold] = field(default_factory=_empty_thresholds)

    # Visualization settings (YAML-overridable)
    display_enabled: bool = True
    trendline_length: int = 30
    trendline_window_sec: float = 60.0
    display_order: int = 0
    display_group: str = ""
    precision: int = 2  # Decimal places for value display
    scale_strategy: str = "raw"  # "raw" | "auto" - unit scaling behavior
    normalize_range: tuple[float, float] | None = None
    display_annotation: str = ""  # Optional secondary label appended in UI

    # Layout hints
    group_title: str | None = None
    group_caption: str | None = None
    group_order: int = 0
    section_category: str | None = None
    sparkline_style: str | None = None
    layout_hint: str | None = None

    # Extraction settings (schema-driven parsing)
    extract: ExtractionRule | None = None  # How to extract this parameter from tool output

    # Derived parameter settings
    formula: str | None = None
    dependencies: Sequence[str] = field(default_factory=tuple)
    task: str | None = None  # Optional virtual task grouping
    display_format: dict[Any, str] | str | None = None
    formula_version: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "thresholds", _freeze_thresholds(self.thresholds))
        object.__setattr__(self, "dependencies", tuple(self.dependencies))

    def replace(self, **changes: Any) -> ParameterField:
        """Return a new field with provided overrides applied."""

        if not changes:
            return self
        updated = replace(self, **changes)
        object.__setattr__(updated, "thresholds", _freeze_thresholds(updated.thresholds))
        return updated

    def with_threshold(self, level: str, threshold: Threshold | None) -> ParameterField:
        """Return copy with threshold level added, updated, or removed."""

        current = dict(self.thresholds)
        if threshold is None:
            current.pop(level, None)
        else:
            current[level] = threshold
        return self.replace(thresholds=current)

    @property
    def source_type(self) -> Literal["derived", "extracted"]:
        """Classify whether the field is derived or extracted."""

        return "derived" if self.formula else "extracted"


@dataclass(frozen=True, slots=True)
class CalculatedParameter:
    """Runtime definition for schema-driven calculated parameters."""

    name: str
    fn: Callable[[Mapping[str, Any]], Any]
    field: ParameterField


@dataclass(frozen=True, slots=True)
class DerivedSpec:
    """Declarative description for derived parameters."""

    type: str
    numerator: str | None = None
    denominator: str | None = None
    source: str | None = None
    sources: tuple[str, ...] = field(default_factory=tuple)
    window_seconds: float | None = None
    rule: str | None = None
    multiplier: float | None = None


class ParameterStatus(str, Enum):
    """Unified data-flow status for a parameter."""

    WAITING = "waiting"  # No data received yet, task still running
    STREAMING = "streaming"  # Receiving fresh values within threshold
    COMPLETE = "complete"  # Task finished and stream stopped cleanly
    STALE = "stale"  # Missing data beyond threshold or task ended without data
    FAILED = "failed"  # Task failed before parameter produced data
    CANCELLED = "cancelled"  # Task cancelled before producing definitive data


@dataclass(frozen=True, slots=True)
class ParametersSchema:
    """Schema defining expected parameters and their properties."""

    fields: Sequence[ParameterField] = field(default_factory=tuple)
    staleness_threshold_seconds: float = 30.0  # Unified threshold for stale detection
    calculated_params: Mapping[str, CalculatedParameter] = field(
        default_factory=_empty_calculated_params
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "fields", tuple(self.fields))
        object.__setattr__(
            self,
            "calculated_params",
            _freeze_calculated_params(self.calculated_params),
        )

    def replace(self, **changes: Any) -> ParametersSchema:
        if not changes:
            return self
        updated = replace(self, **changes)
        object.__setattr__(updated, "fields", tuple(updated.fields))
        object.__setattr__(
            updated,
            "calculated_params",
            _freeze_calculated_params(updated.calculated_params),
        )
        return updated

    def with_fields(self, fields: Iterable[ParameterField]) -> ParametersSchema:
        return self.replace(fields=tuple(fields))

    def upsert_field(self, field: ParameterField) -> tuple[ParametersSchema, bool]:
        """Insert or replace a field, returning updated schema and creation flag."""

        replaced = False
        updated_fields: list[ParameterField] = []
        for existing in self.fields:
            if existing.name == field.name:
                updated_fields.append(field)
                replaced = True
            else:
                updated_fields.append(existing)
        if not replaced:
            updated_fields.append(field)
        return self.with_fields(updated_fields), not replaced

    def extend_with_fields(self, fields: Iterable[ParameterField]) -> ParametersSchema:
        schema = self
        for param_field in fields:
            schema, _ = schema.upsert_field(param_field)
        return schema
