"""Task execution framework package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hil_testbench.run.logging.task_logger import LogLevel as _LogLevel

    LogLevel = _LogLevel

__all__ = ["LogLevel"]


def __getattr__(name: str) -> Any:
    """Lazily expose selected submodules to keep import graph lightweight."""

    if name == "LogLevel":
        from hil_testbench.run.logging.task_logger import (  # hil: allow-lazy
            LogLevel as _LogLevel,
        )

        return _LogLevel
    raise AttributeError(name)


def __dir__() -> list[str]:
    return sorted(__all__ + list(globals().keys()))
