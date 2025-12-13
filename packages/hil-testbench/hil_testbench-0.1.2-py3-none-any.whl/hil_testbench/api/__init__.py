"""Public task plugin API surface for task authors.

This package exposes the stable, task-facing abstractions required to
implement declarative tasks without importing internal framework modules.
"""

from . import command, extras, parser, schema, thresholds
from .task import Task, TaskConfig, TaskConfigProtocol

__all__ = [
    "Task",
    "TaskConfig",
    "TaskConfigProtocol",
    "command",
    "extras",
    "parser",
    "schema",
    "thresholds",
]
