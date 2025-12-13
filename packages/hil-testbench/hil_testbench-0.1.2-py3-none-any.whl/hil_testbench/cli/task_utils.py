"""CLI task selection helpers for run_tasks.

These helpers keep the task validation logic centralized so tests can
exercise it without launching subprocesses. They directly support the
Multi-Task CLI requirement **R2 (Task Validation)** defined in
``docs-internal/features/multi-task-cli-requirements.md`` and
**REQ-CLI-002** (deterministic remediation messaging).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class TaskSelection:
    """Structured result of CLI task normalization."""

    unique: list[str]
    invalid: list[str]


def has_requested_tasks(tasks: Sequence[str] | None) -> bool:
    """Return True when at least one CLI task argument was supplied."""

    return bool(tasks)


def select_tasks(
    requested: Sequence[str] | None,
    available: Iterable[str],
) -> TaskSelection:
    """Normalize CLI task arguments and detect invalid entries.

    - Deduplicates the requested tasks while preserving user order.
    - Flags any deduplicated task that does not exist in ``available``.
    - Returns ``TaskSelection`` so callers can render remediation text.
    """

    unique = _deduplicate(requested or [])
    invalid = _find_invalid(unique, available)
    return TaskSelection(unique=unique, invalid=invalid)


def _deduplicate(tasks: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for task in tasks:
        if task in seen:
            continue
        ordered.append(task)
        seen.add(task)
    return ordered


def _find_invalid(tasks: Sequence[str], available: Iterable[str]) -> list[str]:
    available_set = set(available)
    return [task for task in tasks if task not in available_set]


def task_word(tasks_or_count: Sequence[Any] | int) -> str:
    """Return singular/plural label for tasks."""

    count = tasks_or_count if isinstance(tasks_or_count, int) else len(tasks_or_count)
    return "task" if count == 1 else "tasks"


def join_task_names(
    task_names: Iterable[str],
    *,
    sort_output: bool = False,
) -> str:
    """Return a comma-separated list of task names.

    Defaults to preserving input order; set ``sort_output`` to ``True`` when the
    CLI must render deterministic listings (REQ-CLI-002).
    """

    names = list(task_names)
    if sort_output:
        names = sorted(names)
    return ", ".join(names)


def build_invalid_task_messages(
    invalid_tasks: Sequence[str],
    available_tasks: Iterable[str],
) -> tuple[str, str]:
    """Create deterministic error/remediation lines for invalid CLI tasks."""

    invalid_line = f"Error: Invalid {task_word(invalid_tasks)}: {', '.join(invalid_tasks)}"
    available_line = "Available tasks: " + join_task_names(available_tasks, sort_output=True)
    return invalid_line, available_line
