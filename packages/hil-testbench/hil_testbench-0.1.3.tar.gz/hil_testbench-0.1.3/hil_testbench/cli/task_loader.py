from __future__ import annotations

import pkgutil
from pathlib import Path
from typing import Any

from hil_testbench.api.task import Task as ApiTask


def discover_tasks(task_dir: str = "tasks") -> list[str]:
    """Discover tasks from a directory.

    Supports BOTH:
    - tasks packaged as directories with __init__.py
    - loose .py task modules (used in tests)
    """

    path = Path(task_dir)
    if not path.exists():
        return []

    discovered: set[str] = set()

    # 1. Discover packages and modules via pkgutil (only finds packages)
    for m in pkgutil.iter_modules([task_dir]):
        if m.name != "__init__":
            discovered.add(m.name)

    # 2. Discover loose .py files (missed by pkgutil)
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix == ".py":
            name = entry.stem
            if name not in ("__init__",):
                discovered.add(name)

    return sorted(discovered)


def resolve_task_class(module: Any) -> type:
    # Explicit preferred
    explicit = getattr(module, "Task", None)
    if isinstance(explicit, type):
        # Skip the framework base class so module-level imports like
        # `from hil_testbench.api import Task` don't short-circuit discovery.
        if explicit is not ApiTask:
            return explicit

    # Any class with suffix "Task", but prefer classes defined in this module
    # First pass: look for classes defined IN this module (not imported)
    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and name.lower().endswith("task")
            and obj.__module__ == module.__name__
        ):
            return obj

    # Second pass: fall back to any imported class ending in "Task"
    # (for backward compatibility with tasks that might re-export)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and name.lower().endswith("task"):
            return obj

    raise AttributeError(f"No Task class found in module {module.__name__}")
