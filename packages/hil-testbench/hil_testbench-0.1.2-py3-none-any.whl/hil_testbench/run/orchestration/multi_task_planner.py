"""Pure planning logic for multi-task execution."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.orchestration.dag_builder import DAGBuilder
from hil_testbench.run.orchestration.task_definition_builder import (
    TaskDefinitionBuilder,
)
from hil_testbench.task.specs import CommandDefinition, TaskDefinition


class TaskDefinitionBuilderLike(Protocol):
    def build(self, task: Any, config: TaskConfig) -> list[TaskDefinition]: ...


TaskDefinitionBuilderFactory = Callable[[TaskLogger | None], TaskDefinitionBuilderLike]


class DAGBuilderLike(Protocol):
    def build_global_dag(
        self,
        task_definitions: list[TaskDefinition],
        *,
        task_logger: TaskLogger | None = None,
    ) -> tuple[TaskDefinition, dict[str, TaskDefinition]]: ...

    def resolve_dependencies(
        self,
        commands: list[CommandDefinition],
        *,
        task_logger: TaskLogger | None = None,
    ) -> list[CommandDefinition]: ...


DependencyResolver = Callable[[list[CommandDefinition]], list[CommandDefinition]]
DependencyResolverFactory = Callable[[TaskLogger | None], DependencyResolver]


@dataclass
class MultiTaskPlan:
    """Describes merged multi-task execution plan."""

    all_task_defs: list[TaskDefinition]
    merged_task_def: TaskDefinition
    namespaced_task_defs: list[TaskDefinition]
    primary_config: TaskConfig
    config_by_task: dict[str, TaskConfig]
    dependency_resolver_factory: DependencyResolverFactory

    def create_dependency_resolver(
        self, task_logger: TaskLogger | None = None
    ) -> DependencyResolver:
        return self.dependency_resolver_factory(task_logger)


class MultiTaskPlanner:
    """Builds execution plans without touching runtime state."""

    def __init__(
        self,
        dag_builder: DAGBuilderLike | None = None,
        task_def_builder_factory: TaskDefinitionBuilderFactory | None = None,
    ) -> None:
        self._dag_builder = dag_builder or DAGBuilder()
        self._task_def_builder_factory = task_def_builder_factory or (
            lambda logger=None: TaskDefinitionBuilder(task_logger=logger)
        )

    def build_plan(
        self,
        tasks: Sequence[Any],
        configs: Sequence[TaskConfig],
        *,
        task_logger: TaskLogger | None = None,
    ) -> MultiTaskPlan:
        if len(tasks) != len(configs):
            self._log_planner_error(
                task_logger,
                "plan_validation_failed",
                "Task/config count mismatch",
                task_count=len(tasks),
                config_count=len(configs),
            )
            raise ConfigurationError(
                "Task/config count mismatch",
                context={
                    "tasks": len(tasks),
                    "configs": len(configs),
                },
            )
        if not tasks:
            self._log_planner_error(
                task_logger,
                "plan_validation_failed",
                "At least one task must be provided",
            )
            raise ConfigurationError(
                "No tasks provided for execution",
            )

        builder = self._task_def_builder_factory(task_logger)
        task_definitions, config_by_task = self._build_all_task_definitions(tasks, configs, builder)
        merged_task_def, task_def_map = self._dag_builder.build_global_dag(
            task_definitions,
            task_logger=task_logger,
        )
        namespaced_task_defs = list(task_def_map.values())

        dependency_resolver_factory = self._make_dependency_resolver_factory()

        return MultiTaskPlan(
            all_task_defs=task_definitions,
            merged_task_def=merged_task_def,
            namespaced_task_defs=namespaced_task_defs,
            primary_config=configs[0],
            config_by_task=config_by_task,
            dependency_resolver_factory=dependency_resolver_factory,
        )

    @staticmethod
    def _build_all_task_definitions(
        tasks: Sequence[Any],
        configs: Sequence[TaskConfig],
        builder: TaskDefinitionBuilderLike,
    ) -> tuple[list[TaskDefinition], dict[str, TaskConfig]]:
        task_defs: list[TaskDefinition] = []
        config_map: dict[str, TaskConfig] = {}
        for index, task in enumerate(tasks):
            built_defs = builder.build(task, configs[index])
            task_defs.extend(built_defs)
            for task_def in built_defs:
                config_map[task_def.name] = configs[index]
        return task_defs, config_map

    @staticmethod
    def _log_planner_error(
        task_logger: TaskLogger | None,
        event: str,
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

    def _make_dependency_resolver_factory(self) -> DependencyResolverFactory:
        def factory(task_logger: TaskLogger | None = None) -> DependencyResolver:
            def resolver(commands: list[CommandDefinition]) -> list[CommandDefinition]:
                return self._dag_builder.resolve_dependencies(
                    commands,
                    task_logger=task_logger,
                )

            return resolver

        return factory
