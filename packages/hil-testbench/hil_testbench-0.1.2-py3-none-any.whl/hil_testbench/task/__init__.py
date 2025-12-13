"""Task authoring components.

This package provides the core interfaces and base classes for task authoring:
- TaskLike: Protocol defining the task interface
- BaseTask: Optional base class with common patterns (bin override, etc.)
- CommandDefinition: Command specification class
- ParserDefinition, SinkDefinition: Data processing specifications
"""

from hil_testbench.task.base_task import BaseTask
from hil_testbench.task.specs import (
    CommandDefinition,
    ParserDefinition,
    SinkDefinition,
    TaskDefinition,
)
from hil_testbench.task.task_protocol import TaskLike

__all__ = [
    "BaseTask",
    "CommandDefinition",
    "ParserDefinition",
    "SinkDefinition",
    "TaskDefinition",
    "TaskLike",
]
