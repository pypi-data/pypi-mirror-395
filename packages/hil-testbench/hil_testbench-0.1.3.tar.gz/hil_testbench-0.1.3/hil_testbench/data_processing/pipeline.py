"""Centralized sinks and event pipeline for task definitions.

This module wires parser events to JSONL/CSV writers and to the live
metrics display using MetricsManager. Tasks do not construct writers
directly; they only provide a parser and optional metrics config.
"""

from __future__ import annotations

import contextlib
import fnmatch
import os
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from hil_testbench.data_processing.derived_metrics import DerivedMetricsEngine

# DisplayBackend imported via TYPE_CHECKING to avoid circular dependency
from hil_testbench.data_processing.events import CommandOutputEvent
from hil_testbench.data_processing.status_evaluator import evaluate_param_status
from hil_testbench.data_processing.writers import CsvWriter, JsonlWriter
from hil_testbench.data_structs.parameters import ParameterField, ParametersSchema
from hil_testbench.data_structs.threshold_utils import build_threshold_from_spec
from hil_testbench.run.logging.message_helpers import (
    build_display_placeholder_warning,
    build_display_unknown_parameters_warning,
)
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

# Constants
_RANGE_TUPLE_SIZE = 2
_LOG_LINE_PREVIEW_LENGTH = 100
_SCHEMA_LEVEL_KEYS = {"staleness_threshold_seconds"}

# Track display-config warnings to avoid repeating the same console message for every
# command in a task. Protected by lock for concurrent task execution.
_DISPLAY_WARNING_CACHE: set[tuple[str | None, str | None, str]] = set()
_DISPLAY_WARNING_LOCK = threading.Lock()


def _reset_display_warning_cache() -> None:
    """Reset display warning dedupe cache (test helper)."""
    with _DISPLAY_WARNING_LOCK:
        _DISPLAY_WARNING_CACHE.clear()


@dataclass(slots=True)
class PipelineContext:
    """Context data shared across pipeline callbacks."""

    task_name: str
    command_name: str
    exec_dir: str
    file_base: str
    enable_csv: bool
    parameters_schema: ParametersSchema | None
    merged_schema: ParametersSchema | None
    display_backend: Any | None
    task_logger: TaskLogger | None
    dynamic_field_cap: int = 500
    session: Any | None = None
    _field_cache: dict[str, Any] | None = None  # Cache for O(1) field lookups
    _warned_params: set[str] = field(
        default_factory=set
    )  # Track warned parameters (dedupe warnings)


@dataclass(slots=True)
class PipelineFactoryArgs:
    """Arguments for building a pipeline callback factory (single parameter to reduce signature complexity).

    Unified adaptive pipeline design:
    - Dynamic schema extension
    - Buffered writes with size/age heuristics
    - Overrides supplied via run_config when present
    """

    task_name: str
    command_name: str
    parser_factory: Callable[[], Any] | None
    display_backend: Any | None
    enable_jsonl: bool
    enable_csv: bool
    custom_file_base: str | None = None
    task_logger: TaskLogger | None = None
    parameters_schema: ParametersSchema | None = None
    display_config: dict | None = None
    max_bytes: int | None = None
    max_rotations: int | None = None
    # Adaptive pipeline overrides (optional overrides)
    event_buffer_max: int = 50  # Flush when buffered events reach this count
    event_max_age_ms: int = 500  # Flush if oldest buffered event exceeds this age
    dynamic_field_cap: int = 500  # Maximum dynamically added parameters per task
    session: Any | None = None


@dataclass(slots=True)
class EventSinks:
    """Holds the event sinks used in the pipeline callback."""

    jsonl: JsonlWriter | None
    csv: CsvWriter | None
    max_bytes: int
    max_rotations: int


def _make_sinks(
    exec_dir: str,
    file_base: str,
    enable_jsonl: bool,
    enable_csv: bool,
    schema: ParametersSchema | None = None,
    max_bytes: int | None = None,
    max_rotations: int | None = None,
) -> EventSinks:
    jsonl_writer: JsonlWriter | None = None
    csv_writer: CsvWriter | None = None
    max_bytes_val = max_bytes or 10 * 1024 * 1024
    max_rotations_val = max_rotations or 3

    if enable_jsonl:
        jsonl_path = os.path.join(exec_dir, f"{file_base}.jsonl")
        jsonl_writer = JsonlWriter(
            jsonl_path,
            schema=schema,
            max_bytes=max_bytes_val,
            max_rotations=max_rotations_val,
        )

    if enable_csv:
        # CSV fieldnames are determined lazily from first event
        # We create the writer on first write when we know the keys
        csv_writer = None

    return EventSinks(jsonl_writer, csv_writer, max_bytes_val, max_rotations_val)


def _find_param_config(field_name: str, yaml_config: dict) -> dict | None:
    """Find parameter config by exact match or wildcard pattern.

    Args:
        field_name: Parameter field name to match
        yaml_config: YAML display config dictionary

    Returns:
        Matching config dict or None
    """
    # Try exact match first
    if param_config := yaml_config.get(field_name):
        return param_config

    # Fall back to wildcard pattern matching
    return next(
        (config for pattern, config in yaml_config.items() if fnmatch.fnmatch(field_name, pattern)),
        None,
    )


def _validate_threshold_config(
    param_name: str,
    level: str,
    threshold_data: dict[str, Any] | Any,
    logger: TaskLogger | None,
) -> bool:
    """Validate threshold configuration from YAML."""
    if not isinstance(threshold_data, dict):
        return True

    operator = threshold_data.get("operator", "range")
    if not _is_supported_operator(operator, param_name, level, logger):
        return False

    value = threshold_data.get("value")
    if not _validate_threshold_value(operator, value, param_name, level, logger):
        return False

    color = threshold_data.get("color")
    return _validate_threshold_color(color, param_name, level, logger)


def _is_supported_operator(
    operator: str, param_name: str, level: str, logger: TaskLogger | None
) -> bool:
    valid_operators = {"gt", "lt", "eq", "range"}
    if operator in valid_operators:
        return True
    if logger:
        logger.log(
            "threshold_validation_invalid_operator",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message=(
                f"Invalid operator '{operator}' for {param_name}.{level}. "
                f"Must be one of: {', '.join(valid_operators)}"
            ),
            _parameter=param_name,
            _level=level,
            _operator=operator,
        )
    return False


def _validate_threshold_value(
    operator: str,
    value: Any,
    param_name: str,
    level: str,
    logger: TaskLogger | None,
) -> bool:
    if value is None:
        return True

    is_range_value = isinstance(value, (list | tuple)) and len(value) == _RANGE_TUPLE_SIZE
    is_scalar_value = isinstance(value, (int | float))

    if operator == "range" and not is_range_value:
        _log_threshold_warning(
            logger,
            "threshold_validation_range_needs_tuple",
            param_name,
            level,
            f"Operator 'range' requires tuple/list value, got: {type(value).__name__}",
        )
        return False

    if operator in {"gt", "lt", "eq"} and not is_scalar_value:
        _log_threshold_warning(
            logger,
            "threshold_validation_scalar_needs_number",
            param_name,
            level,
            f"Operator '{operator}' requires numeric value, got: {type(value).__name__}",
        )
        return False

    return True


def _validate_threshold_color(
    color: Any, param_name: str, level: str, logger: TaskLogger | None
) -> bool:
    if color is None or isinstance(color, str):
        return True
    _log_threshold_warning(
        logger,
        "threshold_validation_invalid_color",
        param_name,
        level,
        (
            f"Color must be string (Rich color name or hex), got: {type(color).__name__}. "
            "RGB tuples not supported."
        ),
        extra={"_color_type": type(color).__name__},
    )
    return False


def _log_threshold_warning(
    logger: TaskLogger | None,
    event: str,
    param_name: str,
    level: str,
    message: str,
    extra: dict | None = None,
) -> None:
    if not logger:
        return
    payload: dict[str, Any] = {
        "_parameter": param_name,
        "_level": level,
    }
    if extra:
        payload.update(extra)
    logger.log(
        event,
        LogLevel.WARNING,
        scope=LogScope.FRAMEWORK,
        message=message,
        **payload,
    )


def _merge_thresholds(
    field: ParameterField,
    yaml_thresholds: Any,
    logger: TaskLogger | None = None,
) -> ParameterField:
    """Merge YAML threshold config into field thresholds."""

    if not isinstance(yaml_thresholds, dict):
        return field

    updated_field = field
    for level, threshold_data in yaml_thresholds.items():
        if not isinstance(threshold_data, dict):
            continue

        if not _validate_threshold_config(field.name, level, threshold_data, logger):
            continue

        existing = updated_field.thresholds.get(level)
        threshold = build_threshold_from_spec(
            level,
            threshold_data,
            default_color="",
            fallback=existing,
        )
        updated_field = updated_field.with_threshold(level, threshold)
    return updated_field


def _apply_simple_field_overrides(field: ParameterField, param_config: dict) -> ParameterField:
    """Apply simple field overrides from YAML config."""

    field_mappings = {
        "display_enabled": ("display_enabled", bool),
        "trendline_length": ("trendline_length", int),
        "trendline_window_sec": ("trendline_window_sec", float),
        "display_order": ("display_order", int),
        "display_group": ("display_group", str),
        "display_annotation": ("display_annotation", str),
        "precision": ("precision", int),
        "scale_strategy": ("scale_strategy", str),
    }

    updates: dict[str, Any] = {}
    for config_key, (field_name, converter) in field_mappings.items():
        if config_key in param_config:
            updates[field_name] = converter(param_config[config_key])

    if "normalize_range" in param_config:
        nr = param_config["normalize_range"]
        if isinstance(nr, (list | tuple)) and len(nr) == _RANGE_TUPLE_SIZE:
            updates["normalize_range"] = (float(nr[0]), float(nr[1]))

    if not updates:
        return field
    return field.replace(**updates)


def _merge_field_config(
    field: ParameterField, param_config: dict, logger: TaskLogger | None
) -> ParameterField:
    """Merge YAML config into a single parameter field."""

    updated_field = field
    try:
        updated_field = _apply_simple_field_overrides(updated_field, param_config)

        if "thresholds" in param_config:
            updated_field = _merge_thresholds(updated_field, param_config["thresholds"], logger)

    except (ValueError, TypeError) as e:
        if logger:
            logger.log(
                "display_config_validation_failed",
                LogLevel.WARNING,
                scope=LogScope.COMMAND,
                message=(
                    f"Invalid display override for parameter '{field.name}' in tasks.yaml: {e}. "
                    "Fix the YAML value or remove the override to use schema defaults."
                ),
                _parameter=field.name,
                _error=str(e),
                error_type=type(e).__name__,
                show_fields_with_message=True,
            )
        return field

    return updated_field


def _deep_merge_display_config(
    schema: ParametersSchema | None,
    yaml_config: dict | None,
    logger: TaskLogger | None = None,
    task_name: str | None = None,
    command_name: str | None = None,
) -> ParametersSchema | None:
    """Deep merge schema ParameterField with YAML display config."""
    if not schema or not yaml_config:
        return schema

    merged = _clone_schema_with_overrides(schema, yaml_config)
    merged, matched_yaml_params = _merge_parameter_configs(merged, yaml_config, logger)
    _warn_unknown_display_params(
        schema, yaml_config, matched_yaml_params, logger, task_name, command_name
    )
    return merged


def _clone_schema_with_overrides(schema: ParametersSchema, yaml_config: dict) -> ParametersSchema:
    merged = schema
    if "staleness_threshold_seconds" in yaml_config:
        merged = merged.replace(
            staleness_threshold_seconds=float(yaml_config["staleness_threshold_seconds"])
        )
    return merged


def _merge_parameter_configs(
    merged: ParametersSchema,
    yaml_config: dict,
    logger: TaskLogger | None,
) -> tuple[ParametersSchema, set[str]]:
    matched_yaml_params: set[str] = set()
    updated_fields: list[ParameterField] = []
    for param_field in merged.fields:
        param_config = _find_param_config(param_field.name, yaml_config)
        if not param_config:
            updated_fields.append(param_field)
            continue
        updated_field = _merge_field_config(param_field, param_config, logger)
        updated_fields.append(updated_field)
        matched_yaml_params.update(_matching_yaml_keys(param_field.name, yaml_config))
    merged = merged.with_fields(updated_fields)
    matched_yaml_params.update(_SCHEMA_LEVEL_KEYS & yaml_config.keys())
    return merged, matched_yaml_params


def _matching_yaml_keys(param_name: str, yaml_config: dict) -> set[str]:
    return {key for key in yaml_config if key == param_name or fnmatch.fnmatch(param_name, key)}


def _warn_unknown_display_params(
    schema: ParametersSchema,
    yaml_config: dict,
    matched_yaml_params: set[str],
    logger: TaskLogger | None,
    task_name: str | None = None,
    command_name: str | None = None,
) -> None:
    if not logger:
        return
    unmatched = set(yaml_config.keys()) - matched_yaml_params
    if not unmatched:
        return
    schema_names = [f.name for f in schema.fields]

    # Detect template placeholders
    template_placeholders = {p for p in unmatched if p.startswith("<") and p.endswith(">")}
    actual_unknown = unmatched - template_placeholders

    def _should_emit(event: str) -> bool:
        cache_key = (task_name, command_name, event)
        with _DISPLAY_WARNING_LOCK:
            if cache_key in _DISPLAY_WARNING_CACHE:
                return False
            _DISPLAY_WARNING_CACHE.add(cache_key)
            return True

    if template_placeholders and _should_emit("display_config_template_placeholders"):
        logger.log(
            "display_config_template_placeholders",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message=build_display_placeholder_warning(
                task_name,
                command_name,
                template_placeholders,
            ),
            _unmatched_params=sorted(template_placeholders),
            _template_placeholders=sorted(template_placeholders),
            _known_params=schema_names,
            _task=task_name,
            _command=command_name,
            show_fields_with_message=True,
            _concise_console=True,
        )

    if actual_unknown and _should_emit("display_config_unknown_parameters"):
        logger.log(
            "display_config_unknown_parameters",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message=build_display_unknown_parameters_warning(
                task_name,
                command_name,
                actual_unknown,
            ),
            _unknown_params=sorted(actual_unknown),
            _known_params=schema_names,
            _task=task_name,
            _command=command_name,
            show_fields_with_message=True,
            _concise_console=True,
        )


def _serialize_thresholds(field: Any) -> dict[str, dict[str, Any]] | None:
    """Convert field.thresholds mapping to a serializable dict form."""
    if not (thresholds := getattr(field, "thresholds", None)):
        return None
    return {
        level: {
            "value": thr.value,
            "operator": thr.mode,
            "color": thr.color,
        }
        for level, thr in thresholds.items()
    }


def _ensure_csv_writer(
    sinks: EventSinks,
    exec_dir: str,
    file_base: str,
    event: dict[str, Any],
    schema: ParametersSchema | None = None,
) -> None:
    if sinks.csv is not None:
        return

    # Use schema to get all possible fieldnames, not just fields from first event
    if schema:
        fieldnames = ["timestamp"] + [field.name for field in schema.fields]
    else:
        fieldnames = list(event.keys())

    csv_path = os.path.join(exec_dir, f"{file_base}.csv")
    sinks.csv = CsvWriter(
        csv_path,
        fieldnames,
        schema=schema,
        max_bytes=sinks.max_bytes,
        max_rotations=sinks.max_rotations,
    )


def _handle_no_parser_event(line: str, sinks: EventSinks, ctx: PipelineContext) -> None:
    """Handle line when no parser is configured (raw text mode)."""
    event = {"message": line}

    if sinks.jsonl:
        with contextlib.suppress(Exception):
            sinks.jsonl.write(event)

    if ctx.enable_csv:
        with contextlib.suppress(Exception):
            _ensure_csv_writer(
                sinks, ctx.exec_dir, ctx.file_base, event, schema=ctx.parameters_schema
            )
            assert sinks.csv is not None
            sinks.csv.write(event)

    if ctx.display_backend:
        with contextlib.suppress(Exception):
            timestamp = time.time()
            ctx.display_backend.update_parameter(
                ctx.task_name, event.get("message", "raw"), event, timestamp
            )


def _write_to_sinks(ev: dict[str, Any], sinks: EventSinks, ctx: PipelineContext) -> None:
    """Write a single event to all configured sinks with lazy CSV initialization.

    Errors writing to sinks are logged (Option B policy) without failing the command.
    """
    # JSONL sink
    if sinks.jsonl:
        try:
            sinks.jsonl.write(ev)
        except Exception as e:  # noqa: S110
            if ctx.task_logger:
                jsonl_path = getattr(
                    sinks.jsonl,
                    "path",
                    os.path.join(ctx.exec_dir, f"{ctx.file_base}.jsonl"),
                )
                ctx.task_logger.log(
                    "jsonl_write_error",
                    LogLevel.ERROR,
                    scope=LogScope.COMMAND,
                    task=ctx.task_name,
                    message=(
                        f"Failed to append JSONL event for task '{ctx.task_name}' command '{ctx.command_name}' to {jsonl_path}: {e}. "
                        "Verify disk space and file permissions, then rerun or rotate logs."
                    ),
                    error=str(e),
                    command=ctx.command_name,
                    path=jsonl_path,
                    error_type=type(e).__name__,
                    show_fields_with_message=True,
                )

    # CSV sink (lazy create on first write)
    if ctx.enable_csv:
        try:
            _ensure_csv_writer(
                sinks,
                ctx.exec_dir,
                ctx.file_base,
                ev,
                schema=ctx.parameters_schema,
            )
            if sinks.csv:
                sinks.csv.write(ev)
        except Exception as e:  # noqa: S110
            if ctx.task_logger:
                csv_path = os.path.join(ctx.exec_dir, f"{ctx.file_base}.csv")
                ctx.task_logger.log(
                    "csv_write_error",
                    LogLevel.ERROR,
                    scope=LogScope.COMMAND,
                    task=ctx.task_name,
                    message=(
                        f"Failed to write CSV event for task '{ctx.task_name}' command '{ctx.command_name}' to {csv_path}: {e}. "
                        "Check disk space/permissions or disable CSV output before rerunning."
                    ),
                    error=str(e),
                    command=ctx.command_name,
                    path=csv_path,
                    error_type=type(e).__name__,
                    show_fields_with_message=True,
                )


def _init_display_backend_schema(
    display_backend: Any | None, merged_schema: ParametersSchema | None, task_name: str
) -> None:
    """Initialize display backend with merged schema if supported."""
    if not display_backend or not merged_schema:
        return
    with contextlib.suppress(Exception):
        if hasattr(display_backend, "set_schema"):
            display_backend.set_schema(task_name, merged_schema)


def _enrich_event_with_schema(ev: dict, field: Any) -> dict:
    """Enrich event with schema metadata (unit, thresholds, formatting)."""
    enriched_ev = ev.copy()
    # Keep the existing value from the event (don't try to extract by field name)
    # The event already has 'value' key from the parser

    # Validate that event has a value field - common parser bug
    if "value" not in ev:
        raise ValueError(
            f"Event for parameter '{field.name}' missing required 'value' field. "
            f"Parser must emit events with 'value' key. Event keys: {list(ev.keys())}"
        )

    enriched_ev["unit"] = field.unit
    enriched_ev["precision"] = field.precision
    enriched_ev["scale"] = field.scale_strategy
    enriched_ev["description"] = field.description or field.name

    if field.display_annotation:
        enriched_ev["annotation"] = field.display_annotation

    if serialized := _serialize_thresholds(field):
        enriched_ev["thresholds"] = serialized

    return enriched_ev


def _update_display_backend(ev: dict, ctx: PipelineContext) -> None:
    """Update display backend with event data.

    Events must contain one of these routing keys: param_name, sensor_name, or name.
    The value of this key determines which schema parameter receives the event.
    """
    if not ctx.display_backend or not ctx.merged_schema:
        return

    param_name = ev.get("param_name") or ev.get("sensor_name") or ev.get("name")
    if not param_name or not isinstance(param_name, str):
        if ctx.task_logger:
            ctx.task_logger.log(
                "event_missing_routing_key",
                LogLevel.WARNING,
                scope=LogScope.COMMAND,
                task=ctx.task_name,
                message=(
                    f"Parser for task '{ctx.task_name}' command '{ctx.command_name}' "
                    "emitted an event without param_name/sensor_name/name. Update the parser "
                    "to set one of these fields so the display backend can route the metric."
                ),
                event_keys=list(ev.keys()),
                command=ctx.command_name,
                show_fields_with_message=True,
            )
        return
    _update_display_backend_with_param(param_name, ev, ctx)


def _prepare_event_for_outputs(ev: dict[str, Any], ctx: PipelineContext) -> dict[str, Any]:
    """Enrich event with schema metadata for sinks and display if available."""

    if not ctx.merged_schema:
        return ev

    param_name = ev.get("param_name") or ev.get("sensor_name") or ev.get("name")
    if not param_name or not isinstance(param_name, str):
        return ev

    field = _resolve_parameter_field(param_name, ev, ctx)
    if not field:
        return ev

    try:
        return _enrich_event_with_schema(ev, field)
    except ValueError as e:
        _log_missing_value(param_name, ctx, ev, e)
        return ev


# TODO(long_running): Once the streaming dispatcher emits `CommandOutputEvent`
# objects exclusively, drop the legacy line-based path in this class so it no
# longer needs to invoke parser callbacks directly.
class PipelineCallback:
    """Callable pipeline callback with adaptive buffering and dynamic schema.

    The callback inspects command output line-by-line, feeding stdout into the
    parser and logging early warnings when expected parseable data never
    appears. Only stdout lines contribute to the "no parseable data" warning
    threshold because structured parsers consume stdout, while stderr carries
    diagnostic/error messages that should not be mistaken for missing data.
    """

    def __init__(
        self,
        parser: Any | None,
        sinks: EventSinks,
        ctx: PipelineContext,
        event_buffer_max: int,
        event_max_age_ms: int,
    ) -> None:
        self._parser = parser
        self._sinks = sinks
        self._ctx = ctx
        self._session = ctx.session
        self._derived_engine = (
            DerivedMetricsEngine(ctx.parameters_schema) if ctx.parameters_schema else None
        )
        self._event_count: int = 0
        self._first_event_logged: bool = False
        self._buffer: list[dict[str, Any]] = []
        self._buffer_timestamps: list[float] = []
        self._buffer_max = max(1, event_buffer_max)
        self._max_age_ms = max(50, event_max_age_ms)
        self._last_flush_time = time.time()
        self._flush_count = 0
        self._since_last_stats = 0

    def __del__(self) -> None:
        """Flush remaining events when callback is destroyed."""
        try:
            self.flush()
        except Exception:  # noqa: S110
            pass  # Silently ignore errors during cleanup

    def __call__(self, event: CommandOutputEvent) -> None:
        """Handle structured output events emitted from the streamer."""

        if not isinstance(event, CommandOutputEvent):
            raise TypeError("PipelineCallback expects CommandOutputEvent inputs")

        self._handle_output_event(event)

    def _handle_output_event(self, event: CommandOutputEvent) -> None:
        if event.has_records():
            self._process_events(event.records, event.metadata)
            return

        raw_line = event.raw_line
        if not raw_line:
            return

        if self._parser is None:
            self._handle_line_without_parser(raw_line, event.is_error)
            return

        events = self._parse_line(raw_line, event.is_error)
        if not events:
            return

        self._process_events(events, event.metadata)

    def _handle_line_without_parser(self, line: str, is_error: bool) -> None:
        if is_error:
            return
        _handle_no_parser_event(line, self._sinks, self._ctx)

    def _parse_line(self, line: str, is_error: bool) -> list[dict[str, Any]] | None:
        parser = self._parser
        if parser is None:
            return None
        try:
            context = {
                "command_name": self._ctx.command_name,
                "task_name": self._ctx.task_name,
            }
            return parser.feed(line, is_error, context=context)
        except Exception as e:  # noqa: S110
            _handle_parser_error(e, line, self._ctx)
            return None

    def _process_events(
        self,
        events: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        for ev in events:
            self._ingest_event(ev, metadata)
            if self._derived_engine:
                derived_events = self._derived_engine.ingest(
                    {
                        "param_name": ev.get("param_name"),
                        "value": ev.get("value"),
                        "timestamp": ev.get("timestamp"),
                    }
                )
                for derived in derived_events:
                    self._ingest_event(derived, metadata)

    def _ingest_event(
        self, event_payload: dict[str, Any], metadata: dict[str, Any] | None = None
    ) -> None:
        payload = dict(event_payload)
        payload.setdefault("timestamp", time.time())
        payload["command_metadata"] = self._resolve_event_metadata(payload, metadata)
        if field := self._lookup_field(payload.get("param_name")):
            payload.setdefault("status", evaluate_param_status(field, payload.get("value")))
        self._event_count += 1
        self._log_first_event_if_needed()
        self._record_in_session(payload)
        self._buffer.append(payload)
        self._buffer_timestamps.append(time.time())
        self._maybe_flush()

    def _resolve_event_metadata(
        self,
        event_payload: dict[str, Any],
        metadata: dict[str, Any] | None,
    ) -> dict[str, Any]:
        baseline = self._default_command_metadata()
        if metadata and isinstance(metadata, dict):
            merged = dict(baseline)
            merged.update(metadata)
            return merged
        candidate = event_payload.get("command_metadata")
        if isinstance(candidate, dict):
            merged = dict(baseline)
            merged.update(candidate)
            return merged
        return baseline

    def _lookup_field(self, param_name: str | None) -> ParameterField | None:
        if not param_name or not self._ctx.parameters_schema:
            return None
        cache = self._ctx._field_cache
        if cache is None:
            cache = {}
            self._ctx._field_cache = cache
        if param_name in cache:
            return cache[param_name]
        for param_field in self._ctx.parameters_schema.fields:
            cache[param_field.name] = param_field
            if param_field.name == param_name:
                return param_field
        return None

    def _default_command_metadata(self) -> dict[str, Any]:
        metadata = {
            "task_name": self._ctx.task_name,
            "command_name": self._ctx.command_name,
            "source": "pipeline_callback",
            "timestamp": time.time(),
            "lifecycle_status": "running",
        }
        session = self._session
        if session is not None and hasattr(session, "get_command_spec"):
            try:
                spec = session.get_command_spec(self._ctx.command_name)
            except Exception:  # noqa: BLE001 - defensive guard around spec lookup
                spec = None
            if spec is not None:
                try:
                    identity = spec.identity()
                except Exception:  # noqa: BLE001 - defensive guard around repr conversion
                    identity = None
                if identity:
                    metadata["command_spec_identity"] = identity
        return metadata

    def _log_first_event_if_needed(self) -> None:
        task_logger = self._ctx.task_logger
        if self._first_event_logged or task_logger is None:
            return

        self._first_event_logged = True
        ctx = self._ctx
        display_task = self._display_task_name()
        task_logger.log(
            "data_stream_started",
            LogLevel.DEBUG,
            scope=LogScope.COMMAND,
            task=display_task,  # Use actual task name for log prefix
            message=f"{display_task}/{ctx.command_name} received first data event",
            command=ctx.command_name,
            show_fields_with_message=True,
        )

    def _record_in_session(self, ev: dict[str, Any]) -> None:
        """Record raw events into ExecutionSession shared context."""

        if not self._session:
            return
        param_name = ev.get("param_name") or ev.get("sensor_name") or ev.get("name")
        if not param_name:
            return
        value = ev.get("value")
        timestamp = ev.get("timestamp")
        try:
            ts = float(timestamp) if timestamp is not None else time.time()
        except (TypeError, ValueError):
            ts = time.time()
        metadata = ev.get("command_metadata")
        self._session.record_parameter_event(
            self._ctx.task_name,
            param_name,
            value,
            ts,
            metadata=metadata if isinstance(metadata, dict) else None,
        )

    def _record_derived_in_session(self, ev: dict[str, Any]) -> None:
        """Record derived events so downstream evaluations see latest values."""

        if not self._session:
            return
        param_name = ev.get("param_name")
        if not param_name:
            return
        value = ev.get("value")
        timestamp = ev.get("timestamp")
        try:
            ts = float(timestamp) if timestamp is not None else time.time()
        except (TypeError, ValueError):
            ts = time.time()
        task_name = ev.get("task") or self._ctx.task_name
        metadata = ev.get("command_metadata")
        self._session.record_parameter_event(
            task_name,
            param_name,
            value,
            ts,
            metadata=metadata if isinstance(metadata, dict) else None,
        )

    def _display_task_name(self) -> str:
        """Derive user-facing task name from namespaced command.

        When commands are merged (e.g., multi-task execution), the orchestrator
        namespaces command names using the ``task:command`` pattern. This helper
        extracts the original task name so warnings and informational logs never
        expose internal identifiers like ``__multi_task__``.
        """

        command_name = self._ctx.command_name
        if ":" in command_name:
            return command_name.split(":", 1)[0]
        return self._ctx.task_name

    def get_event_count(self) -> int:
        return self._event_count

    @property
    def data_expected(self) -> bool:
        return self._parser is not None and self._ctx.parameters_schema is not None

    def flush(self) -> None:
        if not self._buffer:
            return
        events_to_flush = list(self._buffer)
        if self._session and self._session.derived_processor:
            derived_events = self._session.derived_processor.evaluate_all(self._ctx.task_name)
            for dev in derived_events:
                dev.setdefault("command_metadata", self._default_command_metadata())
                self._record_derived_in_session(dev)
            events_to_flush.extend(derived_events)

        for ev in events_to_flush:
            enriched = _prepare_event_for_outputs(ev, self._ctx)
            _write_to_sinks(enriched, self._sinks, self._ctx)
            _update_display_backend(enriched, self._ctx)

        self._buffer.clear()
        self._buffer_timestamps.clear()
        self._last_flush_time = time.time()
        self._flush_count += 1
        self._since_last_stats += 1
        if self._since_last_stats >= 20 and self._ctx.task_logger:
            self._ctx.task_logger.log(
                "pipeline_flush_stats",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=self._ctx.task_name,
                command=self._ctx.command_name,
                flush_count=self._flush_count,
                buffer_max=self._buffer_max,
                max_age_ms=self._max_age_ms,
            )
            self._since_last_stats = 0

    def _maybe_flush(self) -> None:
        if len(self._buffer) >= self._buffer_max:
            self.flush()
            return
        if self._buffer_timestamps:
            oldest_age_ms = (time.time() - self._buffer_timestamps[0]) * 1000.0
            if oldest_age_ms >= self._max_age_ms:
                self.flush()


def _handle_parser_error(e: Exception, line: str, ctx: PipelineContext) -> None:
    """Log parser errors and notify display backend if available."""
    if not ctx.task_logger:
        return
    preview = line[:_LOG_LINE_PREVIEW_LENGTH] if len(line) > _LOG_LINE_PREVIEW_LENGTH else line
    ctx.task_logger.log(
        "parser_feed_error",
        LogLevel.ERROR,
        scope=LogScope.COMMAND,
        message=(
            f"Parser for task '{ctx.task_name}' command '{ctx.command_name}' raised {type(e).__name__}: {e}. "
            "Fix the parser's feed() implementation to handle this line and emit valid events."
        ),
        task=ctx.task_name,
        error=str(e),
        _error_type=type(e).__name__,
        _line_preview=preview,
        command=ctx.command_name,
    )
    backend_getter = getattr(ctx.task_logger, "get_display_backend", None)
    backend = backend_getter() if callable(backend_getter) else None
    with contextlib.suppress(Exception):
        if backend and hasattr(backend, "report_task_error"):
            backend.report_task_error(  # type: ignore[attr-defined]
                ctx.task_name, f"Parser error: {type(e).__name__}: {str(e)}"
            )


def _update_display_backend_with_param(param_name: str, ev: dict, ctx: PipelineContext) -> bool:
    """Update display backend for a named parameter."""
    if not ctx.display_backend or not ctx.merged_schema:
        return False

    field = _resolve_parameter_field(param_name, ev, ctx)
    if not field or not field.display_enabled:
        return False

    try:
        enriched_ev = _enrich_event_with_schema(ev, field)
    except ValueError as e:
        _log_missing_value(param_name, ctx, ev, e)
        return False

    return _send_to_display_backend(ctx, param_name, enriched_ev)


def _resolve_parameter_field(param_name: str, ev: dict, ctx: PipelineContext) -> Any | None:
    _ensure_field_cache(ctx)
    if ctx._field_cache is None:
        return None
    field = ctx._field_cache.get(param_name)
    if field:
        return field
    return _maybe_add_dynamic_field(param_name, ev, ctx)


def _ensure_field_cache(ctx: PipelineContext) -> None:
    if ctx._field_cache is not None:
        return
    if ctx.merged_schema:
        ctx._field_cache = {f.name: f for f in ctx.merged_schema.fields}
    else:
        ctx._field_cache = {}


def _maybe_add_dynamic_field(param_name: str, ev: dict, ctx: PipelineContext) -> Any | None:
    if not (ctx.task_logger and param_name and param_name not in ctx._warned_params):
        return None
    if ctx._field_cache is None or ctx.merged_schema is None:
        return None
    if len(ctx._field_cache) >= ctx.dynamic_field_cap:
        ctx.task_logger.log(
            "dynamic_field_cap_reached",
            LogLevel.WARNING,
            scope=LogScope.COMMAND,
            task=ctx.task_name,
            message=(
                f"Task '{ctx.task_name}' command '{ctx.command_name}' hit the dynamic parameter cap "
                f"({ctx.dynamic_field_cap}). Reduce the number of unique parameters emitted or increase "
                "run_config.dynamic_field_cap before rerunning."
            ),
            param_name=param_name,
            cap=ctx.dynamic_field_cap,
            command=ctx.command_name,
        )
        return None

    raw_val = ev.get("value")
    inferred_type = type(raw_val) if raw_val is not None else float
    try:
        new_field = _create_dynamic_field(param_name, inferred_type)
    except Exception as e:  # noqa: S110
        ctx.task_logger.log(
            "dynamic_parameter_add_failed",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=ctx.task_name,
            message=(
                f"Failed adding dynamic parameter '{param_name}' for task '{ctx.task_name}': {e}. "
                "Ensure the parser emits a supported value type or adjust the schema to accept it."
            ),
            param_name=param_name,
            error=str(e),
            command=ctx.command_name,
            error_type=type(e).__name__,
        )
        return None

    ctx.merged_schema, added = ctx.merged_schema.upsert_field(new_field)
    if not added:
        return ctx._field_cache.get(param_name)
    ctx._field_cache[param_name] = new_field
    ctx._warned_params.add(param_name)
    ctx.task_logger.log(
        "dynamic_parameter_added",
        LogLevel.INFO,
        scope=LogScope.COMMAND,
        task=ctx.task_name,
        message=f"Added dynamic parameter '{param_name}' to schema",
        param_name=param_name,
        inferred_type=inferred_type.__name__,
    )
    _persist_dynamic_field(ctx, param_name, inferred_type)
    return new_field


def _create_dynamic_field(param_name: str, inferred_type: type) -> Any:
    return ParameterField(
        name=param_name,
        type=inferred_type,
        description=f"Dynamically added parameter '{param_name}'",
    )


def _persist_dynamic_field(ctx: PipelineContext, param_name: str, inferred_type: type) -> None:
    with contextlib.suppress(Exception):
        if ctx.task_logger and hasattr(ctx.task_logger, "register_dynamic_field"):
            ctx.task_logger.register_dynamic_field(param_name, inferred_type.__name__)
    with contextlib.suppress(Exception):
        if ctx.display_backend and hasattr(ctx.display_backend, "set_schema"):
            ctx.display_backend.set_schema(ctx.task_name, ctx.merged_schema)


def _log_missing_value(param_name: str, ctx: PipelineContext, ev: dict, error: Exception) -> None:
    if not ctx.task_logger:
        return
    ctx.task_logger.log(
        "parser_event_missing_value",
        LogLevel.ERROR,
        scope=LogScope.COMMAND,
        task=ctx.task_name,
        message=(
            f"Parser for task '{ctx.task_name}' command '{ctx.command_name}' emitted parameter '{param_name}' "
            "without a 'value'. Update the parser to include a numeric/text 'value' key in each event."
        ),
        param_name=param_name,
        event_keys=list(ev.keys()),
        command=ctx.command_name,
        error=str(error),
        error_type=type(error).__name__,
        show_fields_with_message=True,
    )


def _send_to_display_backend(ctx: PipelineContext, param_name: str, enriched_ev: dict) -> bool:
    if not ctx.display_backend:
        return False
    timestamp = time.time()
    try:
        ctx.display_backend.update_parameter(
            ctx.task_name,
            param_name,
            enriched_ev,
            timestamp,
            ctx.command_name,
        )
    except Exception as e:  # noqa: S110
        if ctx.task_logger:
            ctx.task_logger.log(
                "display_backend_update_error",
                LogLevel.ERROR,
                scope=LogScope.COMMAND,
                task=ctx.task_name,
                message=(
                    f"Failed to update display for task '{ctx.task_name}' command '{ctx.command_name}' parameter '{param_name}': {e}. "
                    "Verify the display backend is running and accepts parameter updates, then rerun."
                ),
                param_name=param_name,
                error=str(e),
                error_type=type(e).__name__,
                command=ctx.command_name,
                show_fields_with_message=True,
            )
        return False
    return True


def _log_pipeline_config(ctx: PipelineContext, parser: Any | None, sinks: EventSinks) -> None:
    """Log pipeline configuration to task logger."""
    if not ctx.task_logger:
        return

    parser_type = type(parser).__name__ if parser else None
    ctx.task_logger.log(
        "pipeline_configured",
        LogLevel.DEBUG,
        scope=LogScope.COMMAND,
        task=ctx.task_name,
        command=ctx.command_name,
        metrics_enabled=bool(
            ctx.display_backend
        ),  # True when display backend is present for real-time visualization
        _parser=parser_type,
        _jsonl_path=sinks.jsonl.path if sinks.jsonl else None,
        _csv_path=sinks.csv.path if sinks.csv else None,
    )


def make_pipeline_callback_factory(
    args: PipelineFactoryArgs,
) -> Callable[[str], PipelineCallback]:
    """Create a callback factory wiring parser -> sinks -> display backend.

    Returns a factory used by the unified GraphExecutor -> CommandRunner path:
    factory(exec_dir) -> callback(event).
    """

    def factory(exec_dir: str) -> PipelineCallback:
        file_base = args.custom_file_base or f"{args.task_name}_{args.command_name}"
        # Sanitize file_base for Windows compatibility (colons invalid in filenames)
        file_base = file_base.replace(":", "__")
        sinks = _make_sinks(
            exec_dir,
            file_base,
            args.enable_jsonl,
            args.enable_csv,
            schema=args.parameters_schema,
            max_bytes=args.max_bytes,
            max_rotations=args.max_rotations,
        )

        # Deep merge schema with YAML display config
        merged_schema = _deep_merge_display_config(
            args.parameters_schema,
            args.display_config,
            args.task_logger,
            args.task_name,
            args.command_name,
        )

        if args.session:
            args.session.register_schema(merged_schema)

        # Create pipeline context
        ctx = PipelineContext(
            task_name=args.task_name,
            command_name=args.command_name,
            exec_dir=exec_dir,
            file_base=file_base,
            enable_csv=args.enable_csv,
            parameters_schema=merged_schema,  # Use merged schema with YAML overrides
            merged_schema=merged_schema,
            display_backend=args.display_backend,
            task_logger=args.task_logger,
            session=args.session,
        )

        _init_display_backend_schema(args.display_backend, merged_schema, args.task_name)

        parser = args.parser_factory() if args.parser_factory else None

        _log_pipeline_config(ctx, parser, sinks)

        return PipelineCallback(
            parser,
            sinks,
            ctx,
            event_buffer_max=args.event_buffer_max,
            event_max_age_ms=args.event_max_age_ms,
        )

    return factory
