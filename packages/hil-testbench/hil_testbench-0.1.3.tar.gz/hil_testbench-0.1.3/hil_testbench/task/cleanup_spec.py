"""Cleanup specification for forced cleanup fallback paths.

Defines a constrained structure so tasks can declare how to identify
and terminate lingering processes even when PID tracking is unavailable.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass


def _tuple_str(values: Iterable[str] | None) -> tuple[str, ...]:
    if not values:
        return tuple()
    return tuple(str(v).strip() for v in values if str(v).strip())


def _tuple_int(values: Iterable[int] | None) -> tuple[int, ...]:
    if not values:
        return tuple()
    return tuple(int(v) for v in values if int(v) > 0)


@dataclass(frozen=True, slots=True)
class CleanupSpec:
    """Declarative forced-cleanup targets for a task.

    Attributes:
        patterns: Substring/regex-like patterns to match against process
            command lines. Intended for pkill/psutil filtering.
        ports: TCP ports whose listeners/owners should be terminated.
        commands: Explicit cleanup commands to execute as a last resort
            (e.g., tool-specific teardown). Executed in order.
        mode: Optional hint for graded cleanup (graceful/strict/aggressive).
    """

    patterns: tuple[str, ...] = tuple()
    ports: tuple[int, ...] = tuple()
    commands: tuple[str, ...] = tuple()
    mode: str | None = None

    def __init__(
        self,
        *,
        patterns: Sequence[str] | None = None,
        ports: Sequence[int] | None = None,
        commands: Sequence[str] | None = None,
        mode: str | None = None,
    ) -> None:
        object.__setattr__(self, "patterns", _tuple_str(patterns))
        object.__setattr__(self, "ports", _tuple_int(ports))
        object.__setattr__(self, "commands", _tuple_str(commands))
        object.__setattr__(self, "mode", mode.strip() if mode else None)
        self._validate()

    def is_empty(self) -> bool:
        """Return True when no cleanup targets are declared."""

        return not (self.patterns or self.ports or self.commands)

    def _validate(self) -> None:
        errors: list[str] = []

        for pattern in self.patterns:
            if not pattern or pattern in {"*", ".*"}:
                errors.append("Unsafe or empty pattern is not allowed")
            if len(pattern) < 3:
                errors.append(f"Pattern '{pattern}' is too short for safe matching")

        for port in self.ports:
            if port <= 0 or port > 65535:
                errors.append(f"Port {port} is outside the valid range 1-65535")

        for command in self.commands:
            if not command or command in {":", "true", "false"}:
                errors.append("Cleanup command must be non-empty and meaningful")

        if errors:
            raise ValueError("; ".join(errors))


__all__ = ["CleanupSpec"]
