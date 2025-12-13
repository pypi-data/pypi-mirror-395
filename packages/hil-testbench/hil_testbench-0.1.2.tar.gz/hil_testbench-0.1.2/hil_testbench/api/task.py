"""Public task base class thin wrapper over internal BaseTask."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any, Protocol, TypeAlias, cast

from hil_testbench.task.base_task import BaseTask

from .command import CommandDeclaration
from .parser import ParserDeclaration
from .schema import SchemaDeclaration

try:  # Lazy import to avoid circular dependency during type checking
    from hil_testbench.internal import plugin_adapter
except Exception:  # pragma: no cover - defensive import barrier
    plugin_adapter = None  # type: ignore

__all__ = ["Task", "TaskConfigProtocol", "TaskConfig"]


class TaskConfigProtocol(Protocol):
    """Lightweight configuration surface exposed to task plugins."""

    @property
    def duration(self) -> Any: ...

    @property
    def interval(self) -> Any: ...

    @property
    def task_params(self) -> Mapping[str, Any]: ...

    @property
    def display(self) -> Mapping[str, Any]: ...

    @property
    def run_config(self) -> Any: ...

    def get_host(self, host_id: str) -> Any: ...

    def get_host_param(self, param_name: str) -> Any: ...

    def with_task_params_updates(
        self,
        *,
        updates: Mapping[str, Any] | None = None,
        removals: Iterable[str] | None = None,
    ) -> TaskConfigProtocol: ...


# Public-friendly alias so task authors can import TaskConfig without worrying about Protocol naming.
TaskConfig: TypeAlias = TaskConfigProtocol


class Task(BaseTask):
    """Public-facing task base class exposing declarative helpers."""

    def __init__(self, config: TaskConfigProtocol | None = None) -> None:
        super().__init__(cast(Any, config))
        self._command_factory: (
            Callable[[TaskConfigProtocol], Iterable[CommandDeclaration]] | None
        ) = None
        self._schema_factory: (
            Callable[[TaskConfigProtocol], SchemaDeclaration | Mapping[str, Any]] | None
        ) = None
        self._parser_factory: Callable[[TaskConfigProtocol], ParserDeclaration | None] | None = None

    def define_commands(
        self,
        factory: Callable[[TaskConfigProtocol], Iterable[CommandDeclaration]]
        | Callable[[TaskConfigProtocol], CommandDeclaration],
    ) -> None:
        """Register a factory returning command declarations."""

        def _iter_commands(cfg: TaskConfigProtocol) -> Iterable[CommandDeclaration]:
            result = factory(cfg)
            if isinstance(result, CommandDeclaration):
                return (result,)
            return tuple(result or ())

        self._command_factory = _iter_commands

    def define_schema(
        self, factory: Callable[[TaskConfigProtocol], SchemaDeclaration | Mapping[str, Any]]
    ) -> None:
        """Register a schema declaration factory."""
        self._schema_factory = factory

    def define_parser(
        self, factory: Callable[[TaskConfigProtocol], ParserDeclaration | None]
    ) -> None:
        """Register a parser declaration factory."""
        self._parser_factory = factory

    def schema(self, config: TaskConfigProtocol | None = None) -> Mapping[str, Any]:
        """Return schema declaration materialized as a mapping."""

        if self._schema_factory is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} must call define_schema() to declare a schema"
            )
        cfg = self._resolve_config(config, caller="schema")
        declaration = self._schema_factory(cfg)
        adapter = _get_plugin_adapter()
        return adapter.schema_to_dict(declaration)

    def parser(self, config: TaskConfigProtocol | None = None) -> ParserDefinition | None:
        """Return parser definition for the task if one is declared."""

        if self._parser_factory is None:
            return None
        cfg = self._resolve_config(config, caller="parser")
        declaration = self._parser_factory(cfg)
        adapter = _get_plugin_adapter()

        schema_provider: Callable[[], Mapping[str, Any]] | None = None
        if self._schema_factory is not None:

            def _schema_provider() -> Mapping[str, Any]:
                return self.schema(cfg)

            schema_provider = _schema_provider

        return adapter.build_parser(declaration, config=cfg, schema_provider=schema_provider)

    # BaseTask.commands() calls build_commands(); override to emit internal definitions.
    def build_commands(self, config: TaskConfigProtocol) -> list[Any]:
        adapter = _get_plugin_adapter()
        if self._command_factory is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} must call define_commands() to declare task commands"
            )
        declarations = list(self._command_factory(config))
        return adapter.build_commands(declarations, config=config)

    def _resolve_config(
        self, config: TaskConfigProtocol | None, *, caller: str
    ) -> TaskConfigProtocol:
        if config is not None:
            return config
        if self.config is None:
            raise ValueError(
                f"{caller}() requires a TaskConfig when task was constructed without one"
            )
        return cast(TaskConfigProtocol, self.config)


def _get_plugin_adapter():
    global plugin_adapter  # noqa: PLW0603 - cached module reference for performance
    if plugin_adapter is None:
        from hil_testbench.internal import plugin_adapter as _adapter

        plugin_adapter = _adapter
    return plugin_adapter
