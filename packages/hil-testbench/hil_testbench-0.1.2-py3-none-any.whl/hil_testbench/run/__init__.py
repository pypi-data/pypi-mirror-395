"""Core execution pipeline for task orchestration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .graph_executor import GraphExecutor as _GraphExecutor
    from .task_orchestrator import TaskOrchestrator as _TaskOrchestrator

    GraphExecutor = _GraphExecutor
    TaskOrchestrator = _TaskOrchestrator

__all__ = ["GraphExecutor", "TaskOrchestrator"]


def __getattr__(name: str) -> Any:
    if name == "GraphExecutor":
        from .graph_executor import GraphExecutor as _GraphExecutor  # hil: allow-lazy

        return _GraphExecutor
    if name == "TaskOrchestrator":
        from .task_orchestrator import (  # hil: allow-lazy
            TaskOrchestrator as _TaskOrchestrator,
        )

        return _TaskOrchestrator
    raise AttributeError(name)


def __dir__() -> list[str]:
    return sorted(__all__ + list(globals().keys()))
