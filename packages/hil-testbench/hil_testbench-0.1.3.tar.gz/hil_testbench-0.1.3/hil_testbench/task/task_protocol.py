"""Task authoring protocol (static guidance for tasks).

Provides a Protocol to document and type-check the
interface the framework expects for task implementations.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.task.specs import ParserDefinition


@runtime_checkable
class TaskLike(Protocol):
    """Minimal interface a task should implement.

    Required:
    - commands(config): returns a list of CommandDefinition objects

    Optional:
    - parser(config): returns ParserDefinition or None
    - schema: dict or ParametersSchema (attribute)
    - task_name: str (attribute); defaults to class name if missing
    - concurrent: bool (attribute); defaults to False
    - depends_on: list[str] (attribute); task names that must complete first
    """

    def commands(self, config: TaskConfig) -> list[Any]: ...

    def parser(self, config: TaskConfig) -> ParserDefinition | None: ...
