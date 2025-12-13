"""Helper utilities for resolving shell wrapper modes."""

from __future__ import annotations

from typing import Any

# TODO(long_running): Drop wrapper mode heuristics once CommandSpec explicitly
# sets shell wrapping intent; execution contexts should stop guessing based on
# locality and defer to the spec-provided value.

WrapperMode = str  # "on" | "off" | "auto"


def _normalize_wrapper_mode(value: Any) -> WrapperMode:
    if value is None:
        return "auto"
    if isinstance(value, bool):
        return "on" if value else "off"
    text = str(value).strip().lower()
    if text in {"on", "true", "yes", "1"}:
        return "on"
    if text in {"off", "false", "no", "0"}:
        return "off"
    return "auto"


def resolve_shell_wrapper_mode(
    command_hint: Any,
    global_default: Any,
    *,
    is_remote: bool,
) -> WrapperMode:
    """Resolve the effective wrapper mode for a command.

    Resolution order:
    1. Command-level hint (if not auto)
    2. Global default (if not auto)
    3. Auto fallback: on for remote commands, off for local commands
    """

    cmd_mode = _normalize_wrapper_mode(command_hint)
    if cmd_mode != "auto":
        return cmd_mode
    global_mode = _normalize_wrapper_mode(global_default)
    if global_mode != "auto":
        return global_mode
    return "on" if is_remote else "off"


__all__ = ["resolve_shell_wrapper_mode"]
