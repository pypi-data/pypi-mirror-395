"""Base task class providing common patterns for task authoring.

Clean-sheet minimal design:
- Automatic bin override from `config.task_params.bin`
- Automatic `task_name` derived from class name (CamelCase → snake_case, acronym aware)
- `concurrent` defaults to True if not explicitly set by subclass
- Fallback `commands()` that delegates to `build_commands()` when present
- Accepts any iterable (list or generator) from `build_commands`
- Lightweight `__repr__` for debugging (internal only)
- Convenience `_cmd()` helper to construct `Command` objects (optional use)

Tasks can inherit from `BaseTask` or implement the TaskLike protocol directly. Inheritance
is optional convenience—protocol/duck typing remains the core contract.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from typing import Any

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.task.specs import CommandDefinition

# TODO (EXEC/TASKS-GENERAL): Ensure all tasks explicitly set long_running on each
# CommandSpec based on the task's semantic needs.


class BaseTask:
    """Optional base class providing common task patterns.

    Subclasses may define:
    - `task_name`: explicit string (else auto-generated)
    - `bin`: default binary path (auto-overridden via config)
    - `concurrent`: bool (defaults True if absent)
    - `build_commands(config)`: dynamic command generation hook
    - `schema(config)`, `parser(config)` if needed
    """

    # Subclasses can override these class attributes
    task_name: str = ""  # Auto-filled if empty
    concurrent: bool = True  # Default parallel behavior
    bin: str = ""  # Optional default binary path

    def __init__(self, config: TaskConfig | None = None) -> None:
        self.config = config

        # Auto-generate task_name if not explicitly set
        if not self.task_name:
            self.task_name = self._auto_name()

        # Ensure concurrent defaults to True if not overridden by subclass
        if not hasattr(self, "concurrent"):
            self.concurrent = True

        # Apply bin override if provided in config
        if config and self.bin:
            override = config.task_params.get("bin")
            if override is not None:
                self.bin = override

    # Fallback commands() using dynamic build_commands if present. Supports list or generator.
    def commands(self, config: TaskConfig) -> list[Any]:
        build_commands_fn: Callable[[TaskConfig], Any] | None = getattr(
            self, "build_commands", None
        )
        if build_commands_fn is not None:
            result = build_commands_fn(config)
            # If already a list return directly; if any other iterable (e.g. generator) materialize.
            if isinstance(result, list):
                return result
            if isinstance(result, Iterable):
                return list(result)
            raise TypeError("build_commands() must return an iterable of Command objects.")
        raise NotImplementedError("Task must implement commands() or build_commands().")

    def _cmd(self, *, name: str, run, host, **kwargs) -> CommandDefinition:
        """Convenience factory returning a `CommandDefinition` directly."""
        return CommandDefinition(name=name, run=run, host=host, **kwargs)

    def _auto_name(self) -> str:
        cls = self.__class__.__name__
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def __repr__(self) -> str:  # Debug-only representation
        return f"{self.__class__.__name__}(task_name={self.task_name!r}, bin={self.bin!r})"
