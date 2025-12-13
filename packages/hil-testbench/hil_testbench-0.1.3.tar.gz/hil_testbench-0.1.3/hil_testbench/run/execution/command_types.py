from __future__ import annotations

"""Shared typing helpers for execution strategies."""

import shlex
from collections.abc import Sequence

from hil_testbench.run.exceptions import ConfigurationError

# TODO(long_running): Move these helpers under CommandSpec so command quoting
# and environment metadata live beside the spec instead of loose module
# functions. Future helpers should emit structured command descriptors rather
# than plain strings.

CommandInput = str | Sequence[str]


def stringify_command(command: CommandInput) -> str:
    """Convert command input into a shell-friendly string representation."""

    if isinstance(command, str):
        return command

    sequence = list(command)
    if not sequence:
        raise ConfigurationError(
            "Command sequence cannot be empty",
            context={"input_type": type(command).__name__},
        )
    return shlex.join(sequence)
