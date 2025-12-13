"""Supplementary utilities exposed on the public task API surface.

This module re-exports a curated set of helpers that plugin authors relied on
from internal packages prior to the API surface being stabilized. Importing
from here keeps task modules within the `hil_testbench.api` namespace while the
underlying implementations continue to live in their original locations.
"""

from __future__ import annotations

from hil_testbench.data_processing.schema_parser import SchemaParser
from hil_testbench.data_structs.parameters import Threshold
from hil_testbench.data_structs.threshold_utils import build_threshold_from_spec
from hil_testbench.task.cleanup_spec import CleanupSpec
from hil_testbench.utils.exec_detection import (
    is_binary_available,
    probe_version_output,
    supports_flags,
)
from hil_testbench.utils.intervals import format_interval_arg, normalize_interval
from hil_testbench.utils.json_stream import JsonEventAccumulator
from hil_testbench.utils.net import detect_version
from hil_testbench.utils.threshold_builder import build_nominal_thresholds

__all__ = [
    "CleanupSpec",
    "JsonEventAccumulator",
    "SchemaParser",
    "Threshold",
    "build_nominal_thresholds",
    "build_threshold_from_spec",
    "detect_version",
    "format_interval_arg",
    "is_binary_available",
    "normalize_interval",
    "probe_version_output",
    "supports_flags",
]
