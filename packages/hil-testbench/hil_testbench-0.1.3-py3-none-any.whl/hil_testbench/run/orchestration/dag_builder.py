"""DAGBuilder - Constructs unified dependency graphs from multiple tasks.

Responsibilities:
- Namespace command names to prevent collisions (task:command format)
- Merge multiple TaskDefinitions into single unified DAG
- Resolve dependencies across task boundaries
- Detect circular dependencies
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.task.dependency import (
    DependencyError as TaskDependencyError,
)
from hil_testbench.task.dependency import (
    build_dependency_graph,
    topological_sort,
)
from hil_testbench.task.specs import CommandDefinition, TaskDefinition


class DAGBuilder:
    """Build unified dependency DAG from multiple task definitions."""

    @staticmethod
    def build_global_dag(
        task_definitions: list[TaskDefinition],
        *,
        task_logger: TaskLogger | None = None,
    ) -> tuple[TaskDefinition, dict[str, TaskDefinition]]:
        """Build merged DAG with namespaced commands.

        Args:
            task_definitions: List of TaskDefinition objects

        Returns:
            Tuple of (merged_definition, task_def_map)
            - merged_definition: Single TaskDefinition with all namespaced commands
            - task_def_map: Mapping of task_name -> original TaskDefinition

        """
        if not task_definitions:
            DAGBuilder._log_dag_error(
                task_logger,
                "dag_build_failed",
                message="No task definitions provided",
            )
            raise ConfigurationError(
                "No task definitions provided",
            )

        try:
            namespaced_defs = DAGBuilder._namespace_commands(task_definitions)
            merged_def = DAGBuilder._merge_definitions(namespaced_defs)
            task_def_map = {td.name: td for td in namespaced_defs}
        except TaskDependencyError as error:
            DAGBuilder._log_dag_error(
                task_logger,
                "dag_build_failed",
                message="Dependency validation failed",
                error=str(error),
            )
            raise ConfigurationError(
                "Dependency validation failed",
                context={
                    "details": str(error),
                },
            ) from error

        return merged_def, task_def_map

    @staticmethod
    def _namespace_commands(
        task_definitions: list[TaskDefinition],
    ) -> list[TaskDefinition]:
        """Apply namespacing to all commands across multiple tasks.

        Transforms:
        - Command names: "cmd1" -> "taskA:cmd1"
        - Internal dependencies: "cmd2" -> "taskA:cmd2"
        - Cross-task dependencies: Already in format "taskB:cmd1" (preserved)

        Args:
            task_definitions: List of TaskDefinition objects

        Returns:
            List of TaskDefinition with namespaced command names and dependencies
        """
        namespaced_defs: list[TaskDefinition] = []

        for task_def in task_definitions:
            namespaced_commands = [
                DAGBuilder._namespace_single_command(task_def.name, cmd)
                for cmd in task_def.commands
            ]

            # Create new TaskDefinition with namespaced commands
            namespaced_def = TaskDefinition(
                name=task_def.name,
                commands=namespaced_commands,
                parser=task_def.parser,
                sinks=task_def.sinks,
                parameters_schema=task_def.parameters_schema,
                concurrent=task_def.concurrent,
            )
            namespaced_defs.append(namespaced_def)

        return namespaced_defs

    @staticmethod
    def _namespace_single_command(task_name: str, command: CommandDefinition) -> CommandDefinition:
        new_depends_on = (
            [dep if ":" in dep else f"{task_name}:{dep}" for dep in command.depends_on]
            if command.depends_on
            else None
        )
        return replace(
            command,
            name=f"{task_name}:{command.name}",
            depends_on=new_depends_on,
        )

    @staticmethod
    def _merge_definitions(
        task_definitions: list[TaskDefinition],
    ) -> TaskDefinition:
        """Merge multiple task definitions into a single flattened definition.

        This enables cross-task dependency resolution by combining all commands
        into one task definition. The merged task uses a synthetic name and
        aggregates commands from all input tasks.

        Note: Parsers and schemas are NOT merged here - they remain task-specific
        and are resolved per-command during execution based on command namespace.

        Args:
            task_definitions: List of (namespaced) TaskDefinition objects

        Returns:
            Single TaskDefinition containing all commands from all tasks
        """
        # Collect all commands from all tasks
        all_commands: list[CommandDefinition] = []
        for task_def in task_definitions:
            all_commands.extend(task_def.commands)

        # Create a merged task definition with synthetic name
        # Parser/schema are None for merged task - resolved per-command in execution
        return TaskDefinition(
            name="__multi_task__",  # Synthetic name for merged execution
            commands=all_commands,
            parser=None,  # Will be resolved per-command based on namespace
            sinks=task_definitions[0].sinks if task_definitions else None,
            parameters_schema=None,  # Will be resolved per-command based on namespace
            concurrent=True,
        )

    @staticmethod
    def resolve_dependencies(
        commands: list[CommandDefinition],
        *,
        task_logger: TaskLogger | None = None,
    ) -> list[CommandDefinition]:
        """Resolve and sort commands by dependencies (topological sort).

        Args:
            commands: List of CommandDefinition objects with dependencies

        Returns:
            Topologically sorted list of commands

        Raises:
            ConfigurationError: If dependency graph invalid or cyclic
        """
        command_map = {cmd.name: cmd for cmd in commands}
        try:
            graph = build_dependency_graph(command_map)
            sorted_names = topological_sort(graph)
        except TaskDependencyError as error:
            DAGBuilder._log_dag_error(
                task_logger,
                "dependency_resolution_failed",
                message="Dependency resolution failed",
                error=str(error),
            )
            raise ConfigurationError(
                "Dependency resolution failed",
                context={
                    "details": str(error),
                },
            ) from error

        return [command_map[name] for name in sorted_names]

    @staticmethod
    def _log_dag_error(
        task_logger: TaskLogger | None,
        event: str,
        *,
        message: str,
        **fields: Any,
    ) -> None:
        if not task_logger:
            return
        task_logger.log(
            event,
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            message=message,
            **fields,
        )
