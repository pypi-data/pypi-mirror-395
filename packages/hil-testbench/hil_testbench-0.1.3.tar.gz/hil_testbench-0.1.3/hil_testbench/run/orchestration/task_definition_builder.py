"""TaskDefinitionBuilder - Converts task objects to TaskDefinitions.

Responsibilities:
- Extract commands (static or dynamic via build_commands hook)
- Extract parser definitions
- Extract schema definitions
- Extract sink configurations
- Validate and normalize all components
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.task.cleanup_spec import CleanupSpec
from hil_testbench.task.specs import (
    CommandDefinition,
    ParserDefinition,
    SinkDefinition,
    TaskDefinition,
)
from hil_testbench.utils.schema_builder import build_schema


class TaskDefinitionBuilder:
    """Build TaskDefinitions from task objects and configuration."""

    def __init__(self, task_logger: TaskLogger | None = None):
        """Initialize builder.

        Args:
            task_logger: Optional TaskLogger for observability logging
        """
        self._task_logger = task_logger

    def build(self, task: Any, config: TaskConfig) -> list[TaskDefinition]:
        """Build TaskDefinition from task object.

        Supports both static commands() and dynamic build_commands(config) hooks.

        Args:
            task: Task object implementing TaskLike protocol
            config: Task-specific configuration

        Returns:
            List containing single TaskDefinition (list for consistency)

        Raises:
            ConfigurationError: If task definition extraction fails
        """
        commands = self._extract_commands(task, config)
        task_name = self._resolve_task_name(task)
        parser_def = self._extract_parser(task, config)
        schema = self._extract_schema(task, config)
        sinks = self._extract_sinks(task, config)
        cleanup_spec = self._extract_cleanup_spec(task, config)

        schema = self._merge_command_schemas(commands, schema)
        self._enforce_parameter_ownership(task_name, commands, schema)

        task_def = TaskDefinition(
            name=task_name,
            commands=commands,
            parser=parser_def,
            sinks=sinks,
            parameters_schema=schema,
            concurrent=bool(getattr(task, "concurrent", True)),
            cleanup_spec=cleanup_spec,
            display_config=dict(config.display) if config.display else None,
        )

        return [task_def]

    def _extract_commands(self, task: Any, config: TaskConfig) -> list[CommandDefinition]:
        """Extract commands from task using dynamic or static hook.

        Resolution order:
        1. If task has build_commands(config): use its result (dynamic generation)
        2. Else fallback to commands(config)

        All returned items must already be CommandDefinition instances.

        Args:
            task: Task object
            config: Task configuration

        Returns:
            List of CommandDefinition instances

        Raises:
            ConfigurationError: If dynamic command generation or validation fails
        """
        # Try dynamic build_commands hook first
        used_dynamic_generation = False
        raw_commands: list[Any]

        build_commands_fn: Callable[[TaskConfig], Any] | None = getattr(
            task, "build_commands", None
        )
        if callable(build_commands_fn):
            try:
                raw_commands = build_commands_fn(config)
                used_dynamic_generation = True
            except Exception as error:  # noqa: BLE001
                task_name = self._resolve_task_name(task)
                self._log_builder_error(
                    "task_definition_error",
                    message="Dynamic command generation failed",
                    task_name=task_name,
                    error=str(error),
                )
                raise ConfigurationError(
                    "Dynamic command generation failed",
                    context={
                        "task": task_name,
                    },
                ) from error
        else:
            commands_fn: Callable[[TaskConfig], Any] = task.commands
            raw_commands = commands_fn(config)

        commands = list(raw_commands)

        # Validate all are CommandDefinition instances
        for c in commands:
            if not isinstance(c, CommandDefinition):
                task_name = self._resolve_task_name(task)
                self._log_builder_error(
                    "task_definition_error",
                    message="commands() must return CommandDefinition instances",
                    task_name=task_name,
                    invalid_type=type(c).__name__,
                )
                raise ConfigurationError(
                    "commands() must return CommandDefinition instances",
                    context={
                        "task": task_name,
                        "invalid_type": type(c).__name__,
                    },
                )

        # Log dynamic command generation for observability
        if used_dynamic_generation and self._task_logger:
            task_name = self._resolve_task_name(task)
            command_names = [c.name for c in commands]
            self._task_logger.log(
                "dynamic_commands_generated",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                task=task_name,
                message=f"Generated {len(commands)} commands dynamically",
                command_count=len(commands),
                command_names=command_names,
                generation_method="build_commands",
            )

        return commands

    def _extract_parser(self, task: Any, config: TaskConfig) -> ParserDefinition | None:
        """Extract parser definition from task.

        Args:
            task: Task object
            config: Task configuration

        Returns:
            ParserDefinition if task has parser() method, None otherwise

        Raises:
            TypeError: If parser() returns invalid type
        """
        if hasattr(task, "parser") and callable(task.parser):
            parser_result = task.parser(config)
            if parser_result is not None and not isinstance(parser_result, ParserDefinition):
                task_name = self._resolve_task_name(task)
                self._log_builder_error(
                    "task_definition_error",
                    message="parser() must return ParserDefinition or None",
                    task_name=task_name,
                    invalid_type=type(parser_result).__name__,
                )
                raise ConfigurationError(
                    "parser() must return ParserDefinition or None",
                    context={
                        "task": task_name,
                        "invalid_type": type(parser_result).__name__,
                    },
                )
            return parser_result
        return None

    def _extract_schema(
        self, task: Any, config: TaskConfig | None = None
    ) -> ParametersSchema | None:
        """Extract schema definition from task.

        Args:
            task: Task object
            config: Task configuration (required if schema() method exists)

        Returns:
            ParametersSchema if task has schema() method, None otherwise

        Raises:
            ValueError: If schema() method exists but no config provided
            TypeError: If schema() returns non-dict
        """
        if hasattr(task, "schema") and callable(task.schema):
            if config is None:
                task_name = self._resolve_task_name(task)
                self._log_builder_error(
                    "task_definition_error",
                    message="schema() requires config",
                    task_name=task_name,
                )
                raise ConfigurationError(
                    "schema() requires TaskConfig",
                    context={
                        "task": task_name,
                    },
                )
            schema_result = task.schema(config)
            if isinstance(schema_result, dict):
                return build_schema(schema_result)
            task_name = self._resolve_task_name(task)
            self._log_builder_error(
                "task_definition_error",
                message="schema() must return dict",
                task_name=task_name,
                invalid_type=type(schema_result).__name__,
            )
            raise ConfigurationError(
                "schema() must return dict",
                context={
                    "task": task_name,
                    "invalid_type": type(schema_result).__name__,
                },
            )
        return None

    def _extract_cleanup_spec(self, task: Any, config: TaskConfig | None) -> CleanupSpec | None:
        """Extract cleanup specification from task if provided."""

        if not hasattr(task, "cleanup_spec"):
            return None

        cleanup_value = task.cleanup_spec
        if callable(cleanup_value):
            cleanup_value = cleanup_value(config) if config is not None else cleanup_value()

        if cleanup_value is None:
            return None

        if not isinstance(cleanup_value, CleanupSpec):
            task_name = self._resolve_task_name(task)
            self._log_builder_error(
                "task_definition_error",
                message="cleanup_spec must be CleanupSpec or None",
                task_name=task_name,
                invalid_type=type(cleanup_value).__name__,
            )
            raise ConfigurationError(
                "cleanup_spec must be CleanupSpec or None",
                context={"task": task_name, "invalid_type": type(cleanup_value).__name__},
            )

        return cleanup_value

    def _extract_sinks(self, _task: Any, config: TaskConfig) -> SinkDefinition | None:
        """Extract sink configuration from config.task_params.

        Args:
            task: Task object (unused, for future extension)
            config: Task configuration

        Returns:
            SinkDefinition if sinks configured, None otherwise
        """
        sinks_params = config.task_params.get("sinks", {})
        if sinks_params:
            return SinkDefinition(
                enable_jsonl=sinks_params.get("enable_jsonl", True),
                enable_csv=sinks_params.get("enable_csv", True),
                file_base=sinks_params.get("file_base"),
            )
        return None

    def _resolve_task_name(self, task: Any) -> str:
        """Resolve task name from task object.

        Args:
            task: Task object

        Returns:
            Task name (from task_name attribute or class name)
        """
        raw_name = getattr(task, "task_name", None)
        if isinstance(raw_name, str) and raw_name.strip():
            return raw_name.strip()
        return task.__class__.__name__

    def _merge_command_schemas(
        self,
        commands: list[CommandDefinition],
        schema: ParametersSchema | None,
    ) -> ParametersSchema | None:
        merged = schema
        for command in commands:
            if not command.parameters_schema:
                continue
            if merged is None:
                merged = command.parameters_schema
            else:
                merged = merged.extend_with_fields(command.parameters_schema.fields)
        return merged

    def _enforce_parameter_ownership(
        self,
        task_name: str,
        commands: list[CommandDefinition],
        schema: ParametersSchema | None,
    ) -> None:
        if not schema or not schema.fields or not commands:
            return

        field_names = self._extract_field_names(schema)
        if not field_names:
            return

        if len(commands) == 1:
            self._assign_single_command(commands[0], field_names, task_name)
            return

        ownership_map = self._build_ownership_map(
            commands,
            set(field_names),
            task_name,
        )
        self._ensure_all_fields_owned(field_names, ownership_map, task_name)

    def _extract_field_names(self, schema: ParametersSchema) -> tuple[str, ...]:
        return tuple(field.name for field in schema.fields if field.name)

    def _assign_single_command(
        self,
        command: CommandDefinition,
        field_names: tuple[str, ...],
        task_name: str,
    ) -> None:
        owned = self._resolve_command_owned_parameters(command, task_name)
        if not owned:
            command.owned_parameters = list(field_names)

    def _build_ownership_map(
        self,
        commands: list[CommandDefinition],
        field_name_set: set[str],
        task_name: str,
    ) -> dict[str, str]:
        ownership_map: dict[str, str] = {}
        for command in commands:
            owned = self._resolve_command_owned_parameters(command, task_name)
            if not owned:
                continue
            for param in owned:
                self._validate_param_known(param, field_name_set, command, task_name)
                existing_owner = ownership_map.get(param)
                if existing_owner and existing_owner != command.name:
                    raise ConfigurationError(
                        (
                            f"Parameter '{param}' is declared by both "
                            f"'{existing_owner}' and '{command.name}'"
                        ),
                        context={
                            "task": task_name,
                            "parameter": param,
                            "first_owner": existing_owner,
                            "second_owner": command.name,
                        },
                    )
                ownership_map[param] = command.name
        return ownership_map

    def _validate_param_known(
        self,
        param: str,
        field_name_set: set[str],
        command: CommandDefinition,
        task_name: str,
    ) -> None:
        if param in field_name_set:
            return
        raise ConfigurationError(
            (
                f"Command '{command.name}' in task '{task_name}' references "
                f"unknown parameter '{param}'"
            ),
            context={
                "task": task_name,
                "command": command.name,
                "parameter": param,
            },
        )

    def _ensure_all_fields_owned(
        self,
        field_names: tuple[str, ...],
        ownership_map: dict[str, str],
        task_name: str,
    ) -> None:
        missing = [param for param in field_names if param not in ownership_map]
        if not missing:
            return
        raise ConfigurationError(
            (
                f"Task '{task_name}' defines parameters without an owning command: "
                f"{', '.join(missing)}"
            ),
            context={
                "task": task_name,
                "parameters": missing,
            },
        )

    def _resolve_command_owned_parameters(
        self,
        command: CommandDefinition,
        task_name: str,
    ) -> list[str]:
        if command.parameters_schema and command.owned_parameters:
            raise ConfigurationError(
                (
                    f"Command '{command.name}' in task '{task_name}' cannot define "
                    "both parameters_schema and owned_parameters"
                ),
                context={
                    "task": task_name,
                    "command": command.name,
                },
            )

        raw: list[str] = []
        if command.parameters_schema:
            raw.extend(field.name for field in command.parameters_schema.fields if field.name)
        elif command.owned_parameters:
            raw.extend(command.owned_parameters)

        if not raw:
            return []

        seen: set[str] = set()
        deduped: list[str] = []
        for name in raw:
            if name in seen:
                continue
            seen.add(name)
            deduped.append(name)

        command.owned_parameters = deduped
        return deduped

    def _log_builder_error(
        self,
        event: str,
        *,
        message: str,
        task_name: str,
        **fields: Any,
    ) -> None:
        if not self._task_logger:
            return
        self._task_logger.log(
            event,
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message=message,
            task=task_name,
            **fields,
        )
