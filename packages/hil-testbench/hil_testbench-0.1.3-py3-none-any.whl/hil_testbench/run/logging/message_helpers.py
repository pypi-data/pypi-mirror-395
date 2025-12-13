"""Helpers for constructing consistent TaskLogger message strings."""

from __future__ import annotations

from collections.abc import Iterable


def describe_task_command(task_name: str | None, command_name: str | None) -> str:
    """Return human-readable context label for task/command combinations."""
    if task_name and command_name:
        return f"task '{task_name}' command '{command_name}'"
    if task_name:
        return f"task '{task_name}'"
    if command_name:
        return f"command '{command_name}'"
    return "this task"


def _format_list(values: Iterable[str]) -> str:
    ordered = [val for val in values if val]
    return ", ".join(ordered)


def build_display_placeholder_warning(
    task_name: str | None,
    command_name: str | None,
    placeholders: Iterable[str],
) -> str:
    """Create actionable warning for template placeholders in display config."""
    context = describe_task_command(task_name, command_name)
    placeholder_text = _format_list(sorted(placeholders))
    return (
        f"Display config for {context} contains template placeholders: {placeholder_text}. "
        "Edit tasks.yaml to replace each placeholder with a parameter emitted by the parser."
    )


def build_display_unknown_parameters_warning(
    task_name: str | None,
    command_name: str | None,
    unknown_params: Iterable[str],
) -> str:
    """Create actionable warning for unknown parameter overrides."""
    context = describe_task_command(task_name, command_name)
    unknown_text = _format_list(sorted(unknown_params))
    return (
        f"Display config for {context} references unknown parameters: {unknown_text}. "
        "Remove or rename them in tasks.yaml to match your parser schema."
    )
