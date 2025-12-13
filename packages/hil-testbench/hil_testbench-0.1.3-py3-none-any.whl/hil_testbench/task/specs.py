"""Declarative task definitions.

Defines dataclasses for declarative task execution. This layer avoids
positional tuples and implicit callback detection by expressing tasks
explicitly as definitions composed of command, parser, metrics, and sink
specifications.
"""

from __future__ import annotations

from _collections_abc import Callable
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol

from hil_testbench.data_structs.hosts import HostDefinition
from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.task.cleanup_spec import CleanupSpec


class Parser(Protocol):
    """Protocol for parsers converting lines to structured events.

    Implementations should be lightweight and stateless where possible.
    """

    def feed(
        self, line: str, is_error: bool, context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Accept a single line and optional context, return zero or more parsed event dicts.

        Args:
            line: Output line from command
            is_error: Whether line came from stderr
            context: Optional dict with command_name, task_name, etc.
        """
        raise NotImplementedError


class CommandValidator(Protocol):
    """Protocol for validating command execution results.

    Allows tasks to define success criteria beyond exit code.
    """

    def validate(
        self,
        exit_code: int,
        stdout: str,
        stderr: str,
        duration: float,
        parameter_count: int = 0,
    ) -> tuple[bool, str | None]:
        """Validate command execution.

        Args:
            exit_code: OS exit code
            stdout: Complete stdout output
            stderr: Complete stderr output
            duration: Execution duration in seconds
            parameter_count: Number of parameter events produced

        Returns:
            (success: bool, error_message: str | None)
            - (True, None) if validation passed
            - (False, "error message") if validation failed
        """
        raise NotImplementedError


@dataclass
class CommandDefinition:
    """Single executable unit that will be invoked by the runner."""

    name: str
    run: Callable[[Any], Any]  # (ExecutionContext) -> Any
    host: HostDefinition | None = None
    use_pty: bool | None = None  # None = auto-detect from command
    use_shell_wrapper: str | bool | None = (
        None  # auto/on/off (bool maps to on/off), None = auto-detect
    )
    immediate: bool = False
    long_running: bool = False
    retry: int = 0
    env: dict[str, str] = field(default_factory=dict)
    cwd: str | None = None
    validator: CommandValidator | None = None  # Optional validation hook
    startup_delay: float = 0.0  # Delay before starting command (seconds)
    depends_on: list[str] | None = None  # List of command names this depends on
    tags: list[str] = field(
        default_factory=list
    )  # Classification tags (e.g. ['server', 'monitoring'])
    parameters_schema: ParametersSchema | None = None  # Optional per-command schema
    owned_parameters: list[str] | None = None  # Explicit parameter ownership (names)
    exclusive: bool = False  # True when command must run alone regardless of DAG


@dataclass
class ParserDefinition:
    """Definition for building a parser instance for a task command."""

    # Factory returning a parser instance implementing Parser.feed()
    factory: Callable[[], Parser]


@dataclass
class SinkDefinition:
    """Output sinks configuration for a task command."""

    enable_jsonl: bool = True
    enable_csv: bool = True
    file_base: str | None = None  # Defaults to <task>_<command> when None


@dataclass
class TaskDefinition:
    """Top-level definition describing a task composed of commands."""

    name: str
    commands: list[CommandDefinition]
    parser: ParserDefinition | None = None
    sinks: SinkDefinition | None = None
    parameters_schema: ParametersSchema | None = None
    concurrent: bool = True
    cleanup_spec: CleanupSpec | None = None
    display_config: Mapping[str, Any] | None = None
