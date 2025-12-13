"""Declarative command builders for task authors."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from .schema import SchemaDeclaration

__all__ = [
    "CommandDeclaration",
    "command",
]


@dataclass(frozen=True)
class CommandDeclaration:
    """Declarative description of a task command."""

    name: str
    host: Any = None
    run: Callable[[Any], Any] | None = None
    argv: tuple[str, ...] | None = None
    shell: str | None = None
    long_running: bool = False
    delay: float = 0.0
    tags: tuple[str, ...] = tuple()
    env: Mapping[str, str] = field(default_factory=dict)
    cwd: str | None = None
    depends_on: tuple[str, ...] = tuple()
    immediate: bool = False
    validator: Callable[..., tuple[bool, str | None]] | None = None
    retry: int = 0
    use_pty: bool | None = None
    use_shell_wrapper: str | bool | None = None
    exclusive: bool = False
    owned_parameters: tuple[str, ...] | None = None
    parameters_schema: SchemaDeclaration | Mapping[str, Any] | None = None


def _normalize_tags(tags: Sequence[str] | None) -> tuple[str, ...]:
    if not tags:
        return tuple()
    return tuple(str(tag) for tag in tags)


def _normalize_sequence(values: Sequence[str] | None) -> tuple[str, ...]:
    if not values:
        return tuple()
    return tuple(str(value) for value in values)


def command(
    name: str,
    *,
    host: Any = None,
    args: Sequence[str] | str | None = None,
    run: Callable[[Any], Any] | None = None,
    long_running: bool = False,
    delay: float = 0.0,
    tags: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | None = None,
    depends_on: Sequence[str] | None = None,
    immediate: bool = False,
    retry: int = 0,
    use_pty: bool | None = None,
    use_shell_wrapper: str | bool | None = None,
    exclusive: bool = False,
    owned_parameters: Sequence[str] | None = None,
    validator: Callable[..., tuple[bool, str | None]] | None = None,
    parameters_schema: SchemaDeclaration | Mapping[str, Any] | None = None,
) -> CommandDeclaration:
    """Create a declarative command description."""

    if run is None and args is None:
        raise ValueError("command() requires either args or run")
    if run is not None and args is not None:
        raise ValueError("command() cannot accept both args and run")

    argv: tuple[str, ...] | None = None
    shell: str | None = None
    if isinstance(args, str):
        shell = args
    elif args is not None:
        argv = tuple(str(part) for part in args)

    env_mapping: Mapping[str, str] = dict(env) if env else {}
    owned = tuple(owned_parameters) if owned_parameters else None

    return CommandDeclaration(
        name=name,
        host=host,
        run=run,
        argv=argv,
        shell=shell,
        long_running=long_running,
        delay=float(delay),
        tags=_normalize_tags(tags),
        env=env_mapping,
        cwd=cwd,
        depends_on=_normalize_sequence(depends_on),
        immediate=immediate,
        retry=int(retry),
        use_pty=use_pty,
        use_shell_wrapper=use_shell_wrapper,
        exclusive=exclusive,
        owned_parameters=owned,
        validator=validator,
        parameters_schema=parameters_schema,
    )
