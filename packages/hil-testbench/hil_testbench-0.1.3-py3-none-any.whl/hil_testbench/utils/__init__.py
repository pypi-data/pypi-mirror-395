"""Utility modules for task execution framework."""

from hil_testbench.utils.exec_detection import (
    is_binary_available,
    probe_version_output,
    supports_flags,
)
from hil_testbench.utils.intervals import format_interval_arg, normalize_interval
from hil_testbench.utils.json_stream import JsonEventAccumulator, add_interval_metadata
from hil_testbench.utils.net import (
    bits_to_human,
    detect_version,
    is_port_open,
    kill_port,
    wait_for_port_state,
)
from hil_testbench.utils.pty_plan import PTYPlan, choose
from hil_testbench.utils.schema_builder import build_schema
from hil_testbench.utils.shell import (
    BUFFERING_OPERATORS,
    build_streaming_command,
    needs_unbuffered_execution,
    wrap_with_script,
)

__all__ = [
    "JsonEventAccumulator",
    "add_interval_metadata",
    "bits_to_human",
    "detect_version",
    "kill_port",
    "is_port_open",
    "wait_for_port_state",
    "is_binary_available",
    "supports_flags",
    "probe_version_output",
    "format_interval_arg",
    "normalize_interval",
    "build_streaming_command",
    "PTYPlan",
    "choose",
    "build_schema",
    "BUFFERING_OPERATORS",
    "needs_unbuffered_execution",
    "wrap_with_script",
]
