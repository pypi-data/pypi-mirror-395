"""Execution planning for streaming commands (PTY, script, wrapper)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from hil_testbench.utils.shell import needs_unbuffered_execution

StreamingMode = Literal["native", "pty", "script", "none"]
ShellWrapperMode = Literal["on", "off", "auto"]


@dataclass(frozen=True)
class PTYPlan:
    """Execution plan for streaming commands."""

    use_pty: bool
    use_script: bool
    shell_wrapper_mode: ShellWrapperMode
    streaming_mode: StreamingMode
    wrap_with_stdbuf: bool
    combine_stderr: bool


def choose(
    is_remote: bool,
    command: str,
) -> PTYPlan:
    """Select execution plan based on command characteristics.

    Analyzes the command string to determine optimal execution strategy:
    - Local execution: PTY if command has buffering operators, otherwise native
    - Remote execution: PTY allocation for pseudo-terminal behavior
    - Commands with buffering operators (;, |, &&, etc.): script wrapper to force line buffering
    """

    needs_unbuffering = needs_unbuffered_execution(command)

    if not is_remote:
        # Local commands with shell operators need PTY for unbuffered output
        if needs_unbuffering:
            return PTYPlan(
                use_pty=True,
                use_script=False,
                shell_wrapper_mode="off",
                streaming_mode="pty",
                wrap_with_stdbuf=False,
                combine_stderr=False,
            )
        return PTYPlan(
            use_pty=False,
            use_script=False,
            shell_wrapper_mode="off",
            streaming_mode="native",
            wrap_with_stdbuf=False,
            combine_stderr=False,
        )

    if needs_unbuffering:
        return PTYPlan(
            use_pty=True,
            use_script=True,
            shell_wrapper_mode="off",
            streaming_mode="script",
            wrap_with_stdbuf=False,
            combine_stderr=False,
        )

    return PTYPlan(
        use_pty=True,
        use_script=False,
        shell_wrapper_mode="on",
        streaming_mode="pty",
        wrap_with_stdbuf=False,
        combine_stderr=False,
    )
