"""Helpers for declaring task parameter schemas.

Task authors describe parameters using `SchemaDeclaration` objects composed
of `SchemaField` entries. The framework converts these declarative
representations into runtime schemas internally.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "SchemaDeclaration",
    "SchemaField",
    "build",
    "combine",
    "from_dict",
    "param",
    "regex",
    "json_path",
    "csv_column",
    "extract",
]


@dataclass(frozen=True)
class SchemaField:
    """Declarative description for a single parameter field."""

    name: str
    spec: Mapping[str, Any]

    def to_mapping(self) -> Mapping[str, Any]:
        return self.spec


@dataclass(frozen=True)
class SchemaDeclaration:
    """Declarative schema composed of parameter fields."""

    fields: tuple[SchemaField, ...] = field(default_factory=tuple)
    options: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a mutable dictionary representation for internal adapters."""

        schema: dict[str, Any] = {field.name: dict(field.to_mapping()) for field in self.fields}
        schema.update(self.options)
        return schema

    def merge(self, *fields: SchemaField, **options: Any) -> SchemaDeclaration:
        """Return new schema with additional fields or options."""

        merged_fields = self.fields + tuple(fields)
        merged_options = dict(self.options)
        merged_options.update(options)
        return SchemaDeclaration(fields=merged_fields, options=merged_options)


def build(*fields: SchemaField, **options: Any) -> SchemaDeclaration:
    """Create a schema from fields and optional schema-level options."""

    return SchemaDeclaration(fields=tuple(fields), options=options)


def from_dict(schema_dict: Mapping[str, Any]) -> SchemaDeclaration:
    """Create a schema declaration directly from a mapping."""

    fields: list[SchemaField] = []
    options: dict[str, Any] = {}
    for key, value in schema_dict.items():
        if key == "staleness_threshold_seconds":
            options[key] = value
            continue
        if isinstance(value, Mapping):
            fields.append(SchemaField(name=key, spec=dict(value)))
        else:
            fields.append(SchemaField(name=key, spec={"type": value}))
    return SchemaDeclaration(fields=tuple(fields), options=options)


def param(
    name: str,
    type_: type,
    *,
    unit: str | None = None,
    description: str | None = None,
    extract: Mapping[str, Any] | None = None,
    thresholds: Mapping[str, Any] | None = None,
    dependencies: Sequence[str] | None = None,
    calc: Callable[[Mapping[str, Any]], Any] | None = None,
    expr: str | None = None,
    **metadata: Any,
) -> SchemaField:
    """Create a schema field with the provided metadata."""

    specification: dict[str, Any] = {"type": type_}
    if unit is not None:
        specification["unit"] = unit
    if description is not None:
        specification["description"] = description
    if extract is not None:
        specification["extract"] = dict(extract)
    if thresholds is not None:
        specification["thresholds"] = dict(thresholds)
    if dependencies is not None:
        specification["dependencies"] = list(dependencies)
    if calc is not None:
        specification["calc"] = calc
    if expr is not None:
        specification["expr"] = expr
    specification.update(metadata)
    return SchemaField(name=name, spec=specification)


def extract(method: str, **options: Any) -> Mapping[str, Any]:
    """Generic extractor helper."""

    return {"method": method, **options}


def regex(
    pattern: str, *, group: int = 1, transform: Callable[[str], Any] | None = None
) -> Mapping[str, Any]:
    """Regex extraction helper."""

    payload: dict[str, Any] = {"method": "regex", "pattern": pattern, "group": group}
    if transform is not None:
        payload["transform"] = transform
    return payload


def json_path(path: str) -> Mapping[str, Any]:
    """JSON path extraction helper."""

    return {"method": "json", "path": path}


def csv_column(column: int | str) -> Mapping[str, Any]:
    """CSV column extraction helper."""

    return {"method": "csv", "column": column}


def combine(fields: Iterable[SchemaField], **options: Any) -> SchemaDeclaration:
    """Combine iterable of fields into a schema declaration."""

    return SchemaDeclaration(fields=tuple(fields), options=options)
