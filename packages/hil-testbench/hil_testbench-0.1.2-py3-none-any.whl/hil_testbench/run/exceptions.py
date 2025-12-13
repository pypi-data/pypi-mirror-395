"""Domain-specific exception hierarchy for the run subsystem."""

from __future__ import annotations

from collections.abc import Mapping

__all__ = [
    "HILTestbenchError",
    "ExecutionError",
    "ValidationError",
    "ConfigurationError",
]


class HILTestbenchError(RuntimeError):
    """Base class for errors surfaced to task orchestrators and CLI."""

    def __init__(self, message: str, *, context: Mapping[str, object] | None = None):
        super().__init__(message)
        if context:
            self.add_context(**context)

    def add_context(self, **context: object) -> None:
        """Attach structured context via exception notes."""

        if not context:
            return
        formatted = ", ".join(f"{key}={value!r}" for key, value in context.items())
        self.add_note(formatted)


class ExecutionError(HILTestbenchError):
    """Failures during command execution (local or remote)."""


class ValidationError(HILTestbenchError):
    """Raised when validators or result checks detect invalid output."""


class ConfigurationError(HILTestbenchError):
    """Raised when user-facing configuration is invalid or incomplete."""
