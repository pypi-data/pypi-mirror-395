"""Shell helpers for streaming-safe command execution."""

from __future__ import annotations

BUFFERING_OPERATORS = [
    "|",
    "||",
    "&&",
    ";",
    ">",
    ">>",
    "<",
    "2>",
    "2>>",
    "2>&1",
]


def needs_unbuffered_execution(command: str) -> bool:
    """Return True if command contains shell operators that buffer output."""

    return any(op in command for op in BUFFERING_OPERATORS)


def wrap_with_script(command: str, quote_escape: bool = True) -> str:
    """Wrap a command with ``script`` to force PTY-backed execution."""

    if quote_escape:
        command = command.replace('"', '\\"')
    return f'script -q -c "{command}" /dev/null'


def build_streaming_command(
    *,
    base_command: str,
    pre_commands: list[str] | None = None,
    use_script: bool = False,
    use_stdbuf: bool = False,
    combine_stderr: bool = False,
    quote_escape: bool = True,
) -> str:
    """Construct a streaming-safe command with optional pre-commands.

    Args:
        base_command: Main command to execute.
        pre_commands: Commands to run before the main command (e.g., kill_port).
        use_script: Wrap the command with ``script`` to force PTY-backed stdio.
        use_stdbuf: Prefix with ``stdbuf -oL`` to force line buffering.
        combine_stderr: Append ``2>&1`` to merge stderr into stdout.
        quote_escape: Escape quotes when wrapping with script.
    """

    cmd = base_command
    if use_stdbuf:
        cmd = f"stdbuf -oL {cmd}"
    if combine_stderr:
        cmd = f"{cmd} 2>&1"
    if use_script:
        cmd = wrap_with_script(cmd, quote_escape=quote_escape)

    parts = list(pre_commands or [])
    parts.append(cmd)
    return "; ".join(parts)
