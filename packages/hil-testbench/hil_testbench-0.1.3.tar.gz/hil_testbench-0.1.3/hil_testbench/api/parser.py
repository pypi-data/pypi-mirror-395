"""Declarative parser helpers for task authors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .schema import SchemaDeclaration

__all__ = [
    "ParserDeclaration",
    "custom",
    "custom_with_schema",
    "json_stream",
    "schema_parser",
    "text",
]


@dataclass(frozen=True)
class ParserDeclaration:
    """Declarative parser description."""

    kind: str
    options: dict[str, Any] = field(default_factory=dict)


def json_stream(get_param_name: Callable[[dict[str, Any]], str]) -> ParserDeclaration:
    """Declare a JSON stream parser with dynamic parameter selection."""

    return ParserDeclaration("json_stream", {"get_param_name": get_param_name})


def text(get_param_name: Callable[[dict[str, Any]], str]) -> ParserDeclaration:
    """Declare a text parser that maps command context to parameter names."""

    return ParserDeclaration("text", {"get_param_name": get_param_name})


def schema_parser(schema: SchemaDeclaration) -> ParserDeclaration:
    """Declare a parser driven by a schema declaration."""

    return ParserDeclaration("schema", {"schema": schema})


def custom(factory: Callable[[], Any]) -> ParserDeclaration:
    """Declare a parser using a caller-provided factory."""

    return ParserDeclaration("custom", {"factory": factory})


def custom_with_schema(
    factory: Callable[[Any], Any], schema_decl: SchemaDeclaration
) -> ParserDeclaration:
    """Declare a parser factory that requires a schema declaration."""

    return ParserDeclaration("custom_schema", {"factory": factory, "schema": schema_decl})
