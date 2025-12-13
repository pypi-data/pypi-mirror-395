"""Small helper utilities shared between CLI components."""

from __future__ import annotations

import sys

from hil_testbench.run.logging.task_logger import (
    LogLevel,
    LogScope,
    queue_cli_message,
)


def safe_symbol(symbol: str) -> str:
    """Return printable symbol, falling back when the console lacks support."""
    if sys.platform == "win32":
        return "*"

    try:
        symbol.encode(sys.stdout.encoding or "utf-8")
        return symbol
    except (UnicodeEncodeError, AttributeError):
        return "*"


def emit_cli_message(
    *,
    event: str,
    message: str,
    icon: str | None = None,
    level: LogLevel = LogLevel.INFO,
    scope: LogScope = LogScope.FRAMEWORK,
    stderr: bool = False,
) -> None:
    """Emit a CLI-facing message via TaskLogger when available."""
    queue_cli_message(
        event=event,
        message=message,
        icon=icon,
        level=level,
        scope=scope,
        stderr=stderr,
    )
