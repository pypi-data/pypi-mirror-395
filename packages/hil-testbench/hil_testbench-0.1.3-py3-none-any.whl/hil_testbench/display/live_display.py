"""Live parameter display using Rich Live for in-place updates."""

import itertools
import os
import threading
from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from hil_testbench.data_processing.status_evaluator import evaluate_param_status
from hil_testbench.data_structs.parameters import (
    ParameterField,
    ParametersSchema,
    ParameterStatus,
)
from hil_testbench.display.sections import SectionRow, render_group_section
from hil_testbench.display.sparkline import (
    _STATE_COLORS,
    ThresholdState,
    _normalize_to_blocks,
    colorize_trend_arrow,
    render_colored_sparkline,
)
from hil_testbench.display.threshold_evaluator import ThresholdEvaluator
from hil_testbench.run.logging.shutdown_summary import ShutdownSummaryBuffer
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.utils.registry import PintValueFormatter

_PINT_UNIT_ALIASES = {
    "%": "percent",
    "percent": "percent",
    "celsius": "degC",
    "°C": "degC",
    "fahrenheit": "degF",
    "°F": "degF",
    "ms": "millisecond",
    "millisecond": "millisecond",
    "GiB": "gibibyte",
    "gibibyte": "gibibyte",
    "MiB": "mebibyte",
    "mebibyte": "mebibyte",
    "KiB": "kibibyte",
    "kibibyte": "kibibyte",
    "TiB": "tebibyte",
    "tebibyte": "tebibyte",
}

_RAW_ONLY_UNITS = {
    "degC",
    "degF",
    "percent",
    "millisecond",
    "gibibyte",
    "mebibyte",
    "kibibyte",
    "tebibyte",
}

_DISPLAY_UNIT_LABELS = {
    "%": "%",
    "percent": "%",
    "degC": "°C",
    "°C": "°C",
    "celsius": "°C",
    "degF": "°F",
    "°F": "°F",
    "fahrenheit": "°F",
    "millisecond": "ms",
    "ms": "ms",
    "GiB": "GiB",
    "gibibyte": "GiB",
    "MiB": "MiB",
    "mebibyte": "MiB",
    "KiB": "KiB",
    "kibibyte": "KiB",
    "TiB": "TiB",
    "tebibyte": "TiB",
}

_CONNECTION_STATUS_ICONS = {
    "pending": "⚫",
    "connecting": "🟡",
    "connected": "🟢",
    "closed": "🔵",
    "failed": "🔴",
}

_KNOWN_CONNECTION_STATES = set(_CONNECTION_STATUS_ICONS)

_LIFECYCLE_STATUS_ICONS = {
    "pending": "⚪",
    "running": "🟠",
    "completed": "🟢",
    "failed": "🔴",
    "cancelled": "⏹️",
    "stopped": "⏹️",
}

_KNOWN_LIFECYCLE_STATES = set(_LIFECYCLE_STATUS_ICONS)

_STATE_ICONS = {
    "good": "🟢",
    "warn": "🟡",
    "bad": "🔴",
    "unknown": "⚪",
}

_STRING_STATE_ALIASES = {
    "ok": "good",
    "pass": "good",
    "passed": "good",
    "good": "good",
    "success": "good",
    "warn": "warn",
    "warning": "warn",
    "caution": "warn",
    "attention": "warn",
    "bad": "bad",
    "fail": "bad",
    "failed": "bad",
    "error": "bad",
    "critical": "bad",
}


@dataclass(frozen=True)
class DisplayGroup:
    order: int
    key: str
    title: str
    caption: str | None
    layout_hint: str | None
    sparkline_style: str | None
    fields: list[ParameterField]


@dataclass
class ParameterStats:
    """Track statistics for a parameter."""

    name: str
    current: Any = None
    min: float | None = None
    max: float | None = None
    sum: float = 0.0
    count: int = 0
    history: deque = field(default_factory=lambda: deque(maxlen=50))
    threshold_states: deque = field(init=False)
    last_update: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    staleness_threshold_seconds: float = 30.0
    status: ParameterStatus = ParameterStatus.WAITING
    last_error: str | None = None
    dependencies: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.threshold_states = deque(maxlen=self.history.maxlen or 50)

    @property
    def average(self) -> float | None:
        """Calculate average value."""
        return self.sum / self.count if self.count > 0 else None

    def update(self, value: Any, threshold_state: ThresholdState | None = None) -> None:
        """Update statistics with new value and mark as streaming."""
        self.current = value
        self.last_update = datetime.now()
        self.status = ParameterStatus.STREAMING
        self.last_error = None

        # Try to track numeric stats
        try:
            numeric_value = float(value)
            self.history.append(numeric_value)
            self.sum += numeric_value
            self.count += 1

            if self.min is None or numeric_value < self.min:
                self.min = numeric_value
            if self.max is None or numeric_value > self.max:
                self.max = numeric_value
            self.threshold_states.append(threshold_state)
        except (TypeError, ValueError):
            # Non-numeric value, just track current
            pass

    def set_threshold(self, seconds: float) -> None:
        """Update staleness threshold for this parameter."""
        self.staleness_threshold_seconds = max(0.0, seconds)

    def seconds_since_last_update(self, now: datetime) -> float | None:
        """Return seconds since last update, if any."""
        return (now - self.last_update).total_seconds() if self.last_update else None

    def seconds_since_created(self, now: datetime) -> float:
        """Return seconds since parameter stats were created."""
        return (now - self.created_at).total_seconds()

    def evaluate_status(
        self,
        now: datetime,
        task_status: str,
        dependencies: dict[str, "ParameterStats"] | None = None,
    ) -> tuple[ParameterStatus, ParameterStatus]:
        """Update status based on staleness rules.

        Returns:
            Tuple of (previous_status, current_status).
        """

        previous = self.status

        if self.last_error:
            self.status = ParameterStatus.FAILED
            return previous, self.status

        dep_status = self._evaluate_dependency_health(now, task_status, dependencies)
        if dep_status is not None:
            self.status = dep_status
            return previous, self.status

        if task_status == "cancelled":
            self.status = ParameterStatus.CANCELLED
        elif self.count == 0:
            self.status = self._evaluate_status_without_data(now, task_status)
        else:
            self.status = self._evaluate_status_with_data(now, task_status)
        return previous, self.status

    def _evaluate_dependency_health(
        self,
        now: datetime,
        task_status: str,
        dependencies: dict[str, "ParameterStats"] | None,
    ) -> ParameterStatus | None:
        if not dependencies:
            return None

        dep_stats = [dependencies.get(dep) for dep in self.dependencies]
        dep_stats = [s for s in dep_stats if s is not None]
        if not dep_stats:
            return None

        # If any dependency has an error, mark failed.
        if any(ds.last_error for ds in dep_stats):
            return ParameterStatus.FAILED

        # If any dependency has not produced data, treat as waiting unless task completed.
        missing = [ds for ds in dep_stats if ds.count == 0]
        if missing:
            if task_status == "completed":
                return ParameterStatus.STALE
            return ParameterStatus.WAITING

        # If any dependency is stale, propagate stale.
        stale = [
            ds
            for ds in dep_stats
            if (ds.seconds_since_last_update(now) or 0.0) >= ds.staleness_threshold_seconds
        ]
        if stale:
            return ParameterStatus.STALE if task_status != "completed" else ParameterStatus.COMPLETE

        return None

    def _evaluate_status_without_data(self, now: datetime, task_status: str) -> ParameterStatus:
        """Determine status when parameter has not produced data yet."""

        if task_status == "completed":
            return ParameterStatus.STALE
        if task_status == "failed":
            return ParameterStatus.FAILED
        waited = self.seconds_since_created(now)
        if waited >= self.staleness_threshold_seconds:
            return ParameterStatus.STALE
        return ParameterStatus.WAITING

    def _evaluate_status_with_data(self, now: datetime, task_status: str) -> ParameterStatus:
        """Determine status when at least one value has been received."""

        age = self.seconds_since_last_update(now)
        if age is not None and age >= self.staleness_threshold_seconds:
            if task_status == "completed":
                return ParameterStatus.COMPLETE
            return ParameterStatus.STALE
        if task_status == "completed":
            return ParameterStatus.COMPLETE
        return ParameterStatus.STREAMING


class LiveDisplayManager:
    """Live parameter display using Rich Live for in-place updates.

    Displays real-time table of parameter statistics during task execution:
    - Current value, average, min/max
    - Sparkline trend visualization
    - Updates in-place without scrolling
    - Transient mode: disappears on completion, leaving clean console logs
    """

    _DEFAULT_PROJECT_TITLE = "HIL TESTBENCH"
    _DEFAULT_PROJECT_DESCRIPTION = "System Characterization"

    def __init__(
        self,
        schema: ParametersSchema,
        refresh_rate: int = 4,
        duration: str | None = None,
        console: Console | None = None,
        display_config: Mapping[str, Any] | None = None,
    ):
        """Initialize display.

        Args:
            schema: Parameter schema defining what to display
            refresh_rate: Ignored (kept for compatibility)
            duration: Task duration in seconds (None = indefinite)
        """
        self.schema = schema
        self.duration = duration

        self._staleness_threshold_seconds = schema.staleness_threshold_seconds
        self.display_config = dict(display_config) if display_config else {}

        # Track parameter statistics
        self.stats: dict[str, ParameterStats] = {}
        self._field_map: dict[str, ParameterField] = {}
        for param_field in schema.fields:
            self.stats[param_field.name] = ParameterStats(
                name=param_field.name,
                staleness_threshold_seconds=self._staleness_threshold_seconds,
            )
            self._field_map[param_field.name] = param_field
        self._schema_field_names = {field.name for field in schema.fields}
        self._summary_parameter_names: set[str] = set()
        self._refresh_summary_parameter_filter()

        # Rich console for final output only (allow injection for tests)
        if console is not None:
            self.console = console
        else:
            self.console = Console(soft_wrap=True)

        self.live: Live | None = None
        self.task_logger: TaskLogger | None = None

        # Task status
        self.task_name = ""
        self.task_status = "initializing"
        self.update_count = 0
        self.start_time = datetime.now()

        # Cache pint formatters per parameter name for reuse
        self._value_formatters: dict[str, PintValueFormatter] = {}
        self._formatter_config: dict[str, tuple[str, int, str]] = {}

        # Refresh thread for periodic updates (even when no data)
        self._refresh_thread: threading.Thread | None = None
        self._refresh_stop_event = threading.Event()
        self._update_lock = threading.RLock()
        self._parameter_task_map: dict[str, str] = {}
        self._parameter_command_map: dict[str, str] = {}
        self._parameter_metadata: dict[str, dict[str, Any]] = {}
        self._command_connection_status: dict[str, str] = {}
        self._command_lifecycle_status: dict[str, str] = {}
        self._shutdown_summaries: dict[str, ShutdownSummaryBuffer] = {}
        self._latest_shutdown_summary_messages: list[str] = []

        # Calculate max rows that fit in terminal (height - overhead for borders/header/footer)
        # Overhead: title(1) + top_border(1) + header(1) + separator(1) + bottom_border(1) + caption(1) + margin(2) = 8
        try:
            terminal_height = os.get_terminal_size().lines
            self.max_rows = max(1, terminal_height - 8)
        except OSError:
            self.max_rows = 20  # Default fallback if terminal size unavailable

    def set_schema(self, task_name: str, schema: ParametersSchema) -> None:
        """Update schema after YAML merge (called per-command).

        Args:
            task_name: Logical task name owning the schema
            schema: Merged schema with YAML overrides applied
        """
        # Merge new schema fields instead of replacing existing ones to
        # maintain a consolidated display across tasks.
        if not schema:
            return

        for param_field in schema.fields:
            self._update_parameter_field(param_field, schema, task_name)
        self._refresh_summary_parameter_filter()

    def _update_parameter_field(
        self,
        param_field: ParameterField,
        schema: ParametersSchema,
        task_name: str,
    ) -> None:
        if param_field.name not in self.stats:
            self.stats[param_field.name] = ParameterStats(
                name=param_field.name,
                staleness_threshold_seconds=schema.staleness_threshold_seconds,
            )
        self.schema, is_new = self.schema.upsert_field(param_field)
        if is_new:
            self._schema_field_names.add(param_field.name)
        self._field_map[param_field.name] = param_field
        self.stats[param_field.name].set_threshold(schema.staleness_threshold_seconds)
        owner = self._normalize_task_name(task_name)
        if owner:
            with self._update_lock:
                self._parameter_task_map[param_field.name] = owner

    def _refresh_summary_parameter_filter(self) -> None:
        """Cache names of parameters that should appear in summaries."""

        self._summary_parameter_names = {
            field.name for field in self.schema.fields if getattr(field, "is_primary", False)
        }

    def _get_param_field_by_name(self, param_name: str) -> ParameterField | None:
        """Return the ParameterField for a given name if known."""

        return self._field_map.get(param_name)

    def register_command(
        self,
        task_name: str,
        command_name: str,
        parameters: Sequence[str] | None = None,
    ) -> None:
        """Record ownership metadata for commands prior to data flow."""

        if not parameters:
            return

        owner = self._normalize_task_name(task_name)
        command_label = command_name or ""
        if not command_label:
            self._log_missing_command_name(task_name)

        with self._update_lock:
            for param_name in parameters:
                if not param_name or param_name not in self._schema_field_names:
                    continue
                if owner and param_name not in self._parameter_task_map:
                    self._parameter_task_map[param_name] = owner
                if command_label:
                    self._parameter_command_map.setdefault(param_name, command_label)
            if command_label and command_label not in self._command_connection_status:
                # Pending indicates the command has not begun execution/connection yet.
                self._command_connection_status[command_label] = "pending"
                if command_label and command_label not in self._command_lifecycle_status:
                    self._command_lifecycle_status[command_label] = "pending"

    def start(self, task_name: str) -> None:
        """Start live display with Rich Live context.

        Args:
            task_name: Name of task being executed
        """
        self.task_name = task_name
        self.task_status = "running"
        self.start_time = datetime.now()
        self._latest_shutdown_summary_messages = []
        for summary in self._shutdown_summaries.values():
            summary.clear()

        self.live = Live(
            self._create_renderable(),
            console=self.console,
            refresh_per_second=2,
            auto_refresh=False,
            transient=True,
            vertical_overflow="visible",
        )
        self.live.start()

        # Start refresh thread for periodic updates (elapsed time, etc.)
        self._refresh_stop_event.clear()
        self._refresh_thread = threading.Thread(
            target=self._refresh_loop, daemon=True, name="LiveDisplayRefresh"
        )
        self._refresh_thread.start()

    def update_task_status(self, _: str, status: str) -> None:
        """Update task status.

        Args:
            task_name: Name of the task (ignored, single-task display)
            status: Task status ("running", "completed", "failed")
        """
        previous_status = self.task_status
        self.task_status = status
        self._evaluate_parameter_states()

        if self.live and status != previous_status:
            with self._update_lock:
                self.live.update(self._create_renderable(), refresh=True)

    def bind_logger(self, logger: TaskLogger) -> None:
        """Attach TaskLogger for status transition logging."""
        self.task_logger = logger
        for summary in self._shutdown_summaries.values():
            summary.bind_logger(logger)

    def stop(self) -> None:
        """Stop live display and refresh thread.

        Display will disappear (transient=True). The calling code (run_tasks.py)
        is responsible for showing final display state if needed.
        """
        # Stop refresh thread first
        if self._refresh_thread and self._refresh_thread.is_alive():
            self._refresh_stop_event.set()
            self._refresh_thread.join(timeout=1.0)
        # Ensure thread reference cleared for lifecycle tests
        self._refresh_thread = None

        if self.live:
            self.live.stop()
            self.live = None

        self._emit_shutdown_stale_summary()

    def _refresh_loop(self) -> None:
        """Background thread to refresh display periodically.

        Updates elapsed time and keeps display visible even when no data flows.
        Runs every 2 seconds to update elapsed time without flickering.
        """
        while not self._refresh_stop_event.is_set():
            self._evaluate_parameter_states()
            if self.live:
                try:
                    with self._update_lock:
                        self.live.update(self._create_renderable(), refresh=True)
                except Exception:  # pylint: disable=broad-except
                    # Suppress any rendering errors (e.g., terminal resize)
                    pass
            # Sleep with check for stop event (2 seconds for smooth updates without flicker)
            self._refresh_stop_event.wait(timeout=2.0)

    def _evaluate_parameter_states(self) -> None:
        """Evaluate parameter statuses and log transitions."""

        now = datetime.now()
        dep_lookup = self.stats
        for stat in self.stats.values():
            dependencies = {
                name: dep for name in stat.dependencies if (dep := dep_lookup.get(name)) is not None
            }
            previous, current = stat.evaluate_status(
                now, self.task_status, dependencies=dependencies or None
            )
            if previous != current:
                self._log_status_transition(stat, previous, now)

    def _log_status_transition(
        self, stat: ParameterStats, previous: ParameterStatus, now: datetime
    ) -> None:
        """Log high-signal transitions (stale/failed)."""

        if not self.task_logger:
            return

        if stat.status == ParameterStatus.STALE:
            if stat.count == 0:
                seconds_without_data = stat.seconds_since_created(now)
                reason = "never_received"
            else:
                seconds_without_data = stat.seconds_since_last_update(now) or 0.0
                reason = "stalled_stream"

            if self._record_shutdown_summary_item(stat.name):
                return

            self.task_logger.log(
                "parameter_data_stale",
                LogLevel.WARNING,
                scope=LogScope.COMMAND,
                task=self.task_name,
                parameter=stat.name,
                previous_status=previous.value,
                status=stat.status.value,
                reason=reason,
                seconds_without_data=round(seconds_without_data, 3),
            )

    def shutdown(self) -> None:
        """Shutdown display (alias for stop)."""
        self.stop()

    def _record_shutdown_summary_item(self, parameter_name: str) -> bool:
        if not self.task_logger or not self.task_logger.shutdown_in_progress:
            return False
        with self._update_lock:
            owner = self._parameter_task_map.get(parameter_name)
        task_name = self._resolved_task_name(owner)
        summary = self._get_shutdown_summary(task_name)
        return summary.add(parameter_name)

    def _resolved_task_name(self, task_name: str | None) -> str:
        normalized = self._normalize_task_name(task_name)
        if normalized:
            return normalized
        fallback = self._normalize_task_name(self.task_name)
        return fallback or "task"

    def _normalize_task_name(self, task_name: str | None) -> str:
        if not task_name:
            return ""
        return task_name.split(":", 1)[0]

    def _log_missing_command_name(self, task_name: str | None) -> None:
        if not self.task_logger:
            return
        resolved = self._normalize_task_name(task_name) or self.task_name or "task"
        self.task_logger.log(
            "display_register_command_missing_name",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            task=resolved,
            message="register_command invoked without command name",
        )

    def _get_shutdown_summary(self, task_name: str) -> ShutdownSummaryBuffer:
        summary = self._shutdown_summaries.get(task_name)
        if summary is None:
            summary = ShutdownSummaryBuffer(
                event_type="parameter_data_stale_summary",
                level=LogLevel.WARNING,
                scope=LogScope.COMMAND,
                list_field="suppressed_parameters",
                message_builder=self._build_stale_summary_message,
            )
            summary.bind_logger(self.task_logger)
            self._shutdown_summaries[task_name] = summary
        return summary

    def render_final(self) -> None:
        """Render the final state of the live display to its console."""

        if not hasattr(self, "console") or self.console is None:
            return
        renderable = self._create_renderable()
        self.console.print(renderable)  # hil: allow-print (final display snapshot)

    def _emit_shutdown_stale_summary(self) -> None:
        """Emit aggregated stale warning during shutdown to avoid console spam."""
        messages: list[str] = []
        for task_name in sorted(self._shutdown_summaries):
            summary = self._shutdown_summaries[task_name].emit(task=task_name)
            if summary and summary.get("message"):
                messages.append(f"{task_name}: {summary['message']}")
        self._latest_shutdown_summary_messages = messages
        for summary in self._shutdown_summaries.values():
            summary.clear()

    def get_primary_parameter_summary(self) -> dict[str, tuple[Any, str | None]]:
        """Get final values for primary parameters that received data.

        Returns:
            Dict mapping parameter_name -> (final_value, unit)
            Limited to first 10 primary parameters, sorted by display_order
            Only includes parameters with is_primary=True and count > 0
        """
        tracked = self._summary_parameter_names
        if not tracked:
            return {}

        # Collect primary parameters with data
        primary_params = []
        for schema_field in self.schema.fields:
            if schema_field.name not in tracked:
                continue
            stat = self.stats.get(schema_field.name)
            if stat and stat.count > 0 and stat.current is not None:
                primary_params.append((schema_field, stat))

        # Sort by display_order
        primary_params.sort(key=lambda x: getattr(x[0], "display_order", 0))

        # Build summary dict (limit to 10)
        summary = {}
        for param_field, stat in primary_params[:10]:
            unit = getattr(param_field, "unit", None) or None
            summary[param_field.name] = (stat.current, unit)

        return summary

    def get_parameter_data_summary(self) -> dict[str, list[str]]:
        """Return parameter names grouped by whether data was received."""

        tracked = set(self._summary_parameter_names)
        if not tracked:
            return {"with_data": [], "without_data": []}

        with_data: list[str] = []
        without_data: list[str] = []

        with self._update_lock:
            stats_snapshot = [(name, stat) for name, stat in self.stats.items() if name in tracked]

        for name, stat in stats_snapshot:
            if stat.count > 0:
                with_data.append(name)
            else:
                without_data.append(name)

        return {"with_data": with_data, "without_data": without_data}

    def update_parameter(
        self,
        task_name: str | None,
        param_name: str,
        event: dict[str, Any],
        timestamp: float,
        command_name: str | None = None,
    ) -> None:
        """Record parameter stats and track ownership metadata.

        Args:
            task_name: Task name emitting the parameter update
            param_name: Parameter name in the schema
            event: Event dict containing 'value' key
            timestamp: Event timestamp
            command_name: Command name emitting the event (used for connection status lookup)
        """
        owner = self._normalize_task_name(task_name)
        with self._update_lock:
            if owner and param_name not in self._parameter_task_map:
                self._parameter_task_map[param_name] = owner

            if command_name:
                self._parameter_command_map.setdefault(param_name, command_name)

        value = event.get("value")
        error = event.get("error")
        dependencies = event.get("dependencies") or ()
        metadata = event.get("command_metadata")
        param_field = self._field_map.get(param_name)

        if param_name in self.stats and dependencies:
            self.stats[param_name].dependencies = tuple(dependencies)
        if param_name in self.stats and error:
            self.stats[param_name].last_error = str(error)
        if isinstance(metadata, dict):
            with self._update_lock:
                self._parameter_metadata[param_name] = dict(metadata)

        stat = self.stats.get(param_name)
        if stat is not None and value is not None:
            previous_len = len(stat.history)
            stat.update(value)

            if len(stat.history) > previous_len and stat.threshold_states:
                classification = self._classify_threshold_state(param_name, value, param_field)
                stat.threshold_states[-1] = classification

            self.update_count += 1

            # Update live display (with lock to prevent concurrent updates)
            if self.live:
                with self._update_lock:
                    self.live.update(self._create_renderable(), refresh=True)

    def get_summary(self) -> dict[str, dict[str, Any]]:
        """Get final statistics summary.

        Returns:
            Dictionary of parameter statistics
        """
        return {
            name: {
                "current": stat.current,
                "average": stat.average,
                "min": stat.min,
                "max": stat.max,
                "count": stat.count,
            }
            for name, stat in self.stats.items()
            if stat.count > 0
        }

    def update_parameters(self, params: dict[str, Any]) -> None:
        """Batch update multiple parameters.

        Args:
            params: Mapping of parameter name to new value.
        """
        if not params:
            return
        for name, value in params.items():
            stat = self.stats.get(name)
            if stat is None or value is None:
                continue

            previous_len = len(stat.history)
            stat.update(value)

            if len(stat.history) > previous_len and stat.threshold_states:
                param_field = self._field_map.get(name)
                classification = self._classify_threshold_state(name, value, param_field)
                stat.threshold_states[-1] = classification

            self.update_count += 1
        if self.live:
            with self._update_lock:
                self.live.update(self._create_renderable(), refresh=True)

    def update_command_status(
        self,
        _task_name: str,
        command_name: str,
        status: str | None = None,
        *,
        lifecycle_status: str | None = None,
    ) -> None:
        """Record command-level lifecycle and connection status updates."""

        refresh_display = False

        if status:
            normalized = status.lower().strip()
            if normalized in _KNOWN_CONNECTION_STATES:
                with self._update_lock:
                    previous = self._command_connection_status.get(command_name)
                    if previous != normalized:
                        self._command_connection_status[command_name] = normalized
                        refresh_display = self.live is not None or refresh_display

        if lifecycle_status:
            normalized_lifecycle = lifecycle_status.lower().strip()
            if normalized_lifecycle in _KNOWN_LIFECYCLE_STATES:
                with self._update_lock:
                    previous_lifecycle = self._command_lifecycle_status.get(command_name)
                    if previous_lifecycle != normalized_lifecycle:
                        self._command_lifecycle_status[command_name] = normalized_lifecycle
                        refresh_display = self.live is not None or refresh_display

        if refresh_display and self.live:
            with self._update_lock:
                if self.live:
                    self.live.update(self._create_renderable(), refresh=True)

    def _create_renderable(self) -> Group:
        """Create the new section-driven display layout."""

        visible_fields = self._get_visible_fields()
        total_params = len(visible_fields)
        display_limit = min(total_params, self.max_rows)
        groups = self._build_group_models(visible_fields[:display_limit])
        group_states = self._aggregate_group_states()

        renderables: list[Any] = []
        if header := self._render_header_block():
            renderables.append(header)
        if summary := self._render_system_summary(group_states, groups):
            renderables.append(Text(summary, style="bold"))
        renderables.append(Rule())

        for group in groups:
            metrics = self._collect_group_metrics(
                group.fields, sparkline_style=group.sparkline_style
            )
            if not metrics:
                continue
            if block := self._render_group_block(group, metrics):
                renderables.append(block)
                renderables.append(Rule())

        if alert := self._render_alert_banner():
            renderables.append(self._render_alert_panel(alert))

        if subsystem := self._render_subsystem_summary(group_states, groups):
            renderables.append(Text(subsystem, style="bold"))

        hidden_count = total_params - display_limit
        if hidden_count > 0:
            renderables.append(Text(f"+{hidden_count} more parameters", style="dim"))

        return Group(*renderables)

    def _merge_captions(self, base: str | None, group: str | None) -> str | None:
        if not base:
            return group
        if not group:
            return base
        return f"{group}\n{base}"

    def _build_group_models(self, fields: list[ParameterField]) -> list[DisplayGroup]:
        grouped: dict[str, list[ParameterField]] = {}
        for param_field in fields:
            group = (
                param_field.group
                or param_field.display_group
                or self._get_task_label(param_field.name)
            )
            if group not in grouped:
                grouped[group] = []
            grouped[group].append(param_field)

        group_items: list[
            tuple[int, str, list[ParameterField], str, str | None, str | None, str | None]
        ] = []
        for group_name, members in grouped.items():
            order_val = min((getattr(member, "group_order", 0) or 0) for member in members)
            title = next(
                (f.group_title for f in members if f.group_title), group_name or "Ungrouped"
            )
            caption = next((f.group_caption for f in members if f.group_caption), None)
            layout_hint = next((f.layout_hint for f in members if f.layout_hint), None)
            sparkline_style = next((f.sparkline_style for f in members if f.sparkline_style), None)
            group_items.append(
                (order_val, group_name, members, title, caption, layout_hint, sparkline_style)
            )

        group_items.sort(key=lambda item: item[0])
        groups: list[DisplayGroup] = []
        for (
            order_val,
            group_name,
            members,
            title,
            caption,
            layout_hint,
            sparkline_style,
        ) in group_items:
            groups.append(
                DisplayGroup(
                    key=group_name,
                    title=title,
                    caption=caption,
                    order=order_val,
                    layout_hint=layout_hint,
                    sparkline_style=sparkline_style,
                    fields=members,
                )
            )
        return groups

    def _render_header_block(self) -> Panel:
        """Render the top-level header panel."""

        header_config = self._build_header_config()
        title = self._header_value(
            header_config,
            keys=("project_title", "project", "title"),
            fallback=self._DEFAULT_PROJECT_TITLE,
        )
        subtitle = self._header_value(
            header_config,
            keys=("description", "subtitle", "project_description", "desc"),
            fallback=self._DEFAULT_PROJECT_DESCRIPTION,
        )
        project_gradient = self._normalize_color_sequence(
            header_config.get("project_gradient_colors")
        ) or self._normalize_color_sequence(header_config.get("gradient_colors"))
        description_gradient = self._normalize_color_sequence(
            header_config.get("description_gradient_colors")
        ) or self._normalize_color_sequence(header_config.get("gradient_colors"))

        title_line = Text()
        title_line.append(self._gradient_text(title, project_gradient))
        if title and subtitle:
            title_line.append(" — ")
        title_line.append(self._gradient_text(subtitle, description_gradient))

        timestamp = self.start_time.strftime("%Y-%m-%d  %I:%M %p")
        elapsed_text = self._format_duration((datetime.now() - self.start_time).total_seconds())
        target_text = ""
        if self.duration:
            try:
                duration_val = float(self.duration)
                target_text = f" / {self._format_duration(duration_val)}"
            except (TypeError, ValueError):
                target_text = f" / {self.duration}"
        duration_line = f"Elapsed {elapsed_text}{target_text}"

        header_text = Text()
        header_text.append(title_line)
        header_text.append("\n")
        header_text.append(Text(f"{timestamp}   |   {duration_line}", style="bold"))

        return Panel(
            header_text,
            border_style="cyan",
            padding=(1, 2),
            expand=True,
        )

    def _build_header_config(self) -> dict[str, Any]:
        """Build a flat header config dict combining display settings."""

        config: dict[str, Any] = {}
        display_cfg = self.display_config or {}
        if isinstance(display_cfg, Mapping):
            config.update(display_cfg)
        header_section = display_cfg.get("header")
        if isinstance(header_section, Mapping):
            config.update(header_section)
        return config

    @staticmethod
    def _header_value(
        header_config: dict[str, Any], *, keys: tuple[str, ...], fallback: str
    ) -> str:
        """Extract the first available header value from config keys."""

        for key in keys:
            value = header_config.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return fallback

    @staticmethod
    def _normalize_color_sequence(raw: Any | None) -> list[str] | None:
        """Normalize color inputs to an ordered list."""

        if not raw:
            return None
        if isinstance(raw, str):
            lines = [line.strip() for line in raw.splitlines() if line.strip()]
            return lines or [raw.strip()]
        if isinstance(raw, Sequence):
            colors = [str(item).strip() for item in raw if str(item).strip()]
            return colors or None
        return None

    @staticmethod
    def _gradient_text(text: str, colors: list[str] | None) -> Text:
        """Return text styled with cycling gradient colors."""

        if not text:
            return Text()
        if not colors:
            return Text(text, style="bold")
        gradient = Text()
        palette = itertools.cycle(colors)
        for char in text:
            if char.isspace():
                gradient.append(char)
                continue
            gradient.append(char, style=next(palette))
        return gradient

    def _render_group_block(self, group: DisplayGroup, rows: list[SectionRow]) -> Table | None:
        """Render a generic group section using layout hints."""

        if not rows:
            return None
        display_title = group.title or group.key or "Metrics"
        return render_group_section(
            title=display_title,
            caption=group.caption,
            rows=rows,
            layout_hint=group.layout_hint,
            sparkline_style=group.sparkline_style,
        )

    def _render_alert_panel(self, alert_text: str) -> Panel:
        """Wrap alert text inside a bordered panel."""

        return Panel(
            Text(alert_text, style="yellow"),
            title="Alerts / Info",
            border_style="yellow",
            padding=(0, 1),
            expand=True,
        )

    def _render_subsystem_summary(
        self, group_states: dict[str, str], groups: list[DisplayGroup]
    ) -> str | None:
        """Generate the subsystem summary line based on aggregated states."""

        if not group_states:
            return None
        ordered: list[str] = []
        for group in groups:
            if group.key in group_states and group.key not in ordered:
                ordered.append(group.key)

        summary_parts: list[str] = []
        seen: set[str] = set()
        for name in ordered:
            state = group_states.get(name)
            if not state:
                continue
            label = next(
                (group.title for group in groups if group.key == name and group.title), name
            )
            summary_parts.append(f"{label} {self._state_icon(state)}")
            seen.add(name)

        for name, state in sorted(group_states.items()):
            if name in seen:
                continue
            summary_parts.append(f"{name} {self._state_icon(state)}")

        return "SUBSYSTEM SUMMARY → " + " | ".join(summary_parts)

    def _should_display_task_column(self) -> bool:
        """Task column is always rendered (REQS055 regression fix)."""

        return True

    def _get_visible_fields(self) -> list[ParameterField]:
        """Return schema fields marked as display-enabled."""

        return [
            schema_field
            for schema_field in self.schema.fields
            if getattr(schema_field, "display_enabled", True) is not False
        ]

    def _color_output_enabled(self) -> bool:
        """Return True when console output supports color/markup."""

        if not hasattr(self, "console") or self.console is None:
            return False
        if getattr(self.console, "no_color", False):
            return False
        return bool(getattr(self.console, "is_terminal", False))

    def _prepare_history_for_display(
        self,
        values: list[float],
        states: list[ThresholdState | None],
        *,
        max_width: int,
    ) -> tuple[list[float], list[ThresholdState | None], bool]:
        """Align and truncate value/state histories for sparkline rendering."""

        if not values or not states:
            if not values:
                return [], [], False
            states = [None] * len(values)

        if len(states) != len(values):
            keep = min(len(states), len(values))
            values = values[-keep:]
            states = states[-keep:]

        truncated = False
        if max_width > 0 and len(values) > max_width:
            values = values[-max_width:]
            states = states[-max_width:]
            truncated = True

        return values, states, truncated

    def _render_alert_banner(self) -> str | None:
        """Render a concise alert banner highlighting degraded parameters."""

        def build_segment(names: list[str], icon: str, label: str, color: str) -> str | None:
            if not names:
                return None
            preview = ", ".join(names[:3])
            suffix = "…" if len(names) > 3 else ""
            detail = f": {preview}{suffix}" if preview else ""
            return f"[{color}]{icon} {label} ({len(names)}){detail}[/{color}]"

        stale = sorted(
            name for name, stat in self.stats.items() if stat.status == ParameterStatus.STALE
        )
        failed = sorted(
            name for name, stat in self.stats.items() if stat.status == ParameterStatus.FAILED
        )
        cancelled = sorted(
            name for name, stat in self.stats.items() if stat.status == ParameterStatus.CANCELLED
        )

        segments: list[str] = []
        for names, icon, label, color in (
            (stale, "⚠️", "Stale", "yellow"),
            (failed, "❌", "Failed", "red"),
            (cancelled, "⏹️", "Cancelled", "magenta"),
        ):
            if segment := build_segment(names, icon, label, color):
                segments.append(segment)

        lines: list[str] = []
        if segments:
            lines.extend(segments)
        for message in self._latest_shutdown_summary_messages:
            lines.append(f"[bold yellow]{message}[/bold yellow]")

        if not lines:
            return None
        return "\n".join(lines)

    def _render_system_summary(
        self,
        group_states: dict[str, str] | None = None,
        groups: list[DisplayGroup] | None = None,
    ) -> str | None:
        """Render a compact system summary line based on grouped parameter health."""

        if group_states is None:
            group_states = self._aggregate_group_states()
        if not group_states:
            return None

        overall_state = self._reduce_states(group_states.values())
        label_map = {"good": "PASS", "warn": "WARN", "bad": "FAIL"}
        overall_label = label_map.get(overall_state, "UNKNOWN")

        summary_parts = [f"SYSTEM: {self._state_icon(overall_state)} {overall_label}"]
        seen: set[str] = set()
        if groups:
            for group in groups:
                state = group_states.get(group.key)
                if not state:
                    continue
                summary_parts.append(f"{group.title or group.key} {self._state_icon(state)}")
                seen.add(group.key)

        for name, state in sorted(group_states.items()):
            if name in seen:
                continue
            summary_parts.append(f"{name} {self._state_icon(state)}")

        if len(summary_parts) == 1:
            return summary_parts[0]
        return "  |  ".join(summary_parts)

    def _classify_threshold_state(
        self,
        param_name: str,
        value: Any,
        param_field: ParameterField | None,
    ) -> ThresholdState | None:
        """Map a parameter sample to a coarse threshold state."""

        if param_field is None or not param_field.thresholds:
            return None

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return None

        stat = self.stats.get(param_name)
        threshold = ThresholdEvaluator.evaluate(
            numeric_value,
            param_field,
            stats=stat,
            context=self._build_context_snapshot(),
        )
        if threshold is None:
            return None

        for level, candidate in param_field.thresholds.items():
            if candidate is threshold:
                if normalized := self._normalize_threshold_state_key(level):
                    return normalized

        return self._state_from_color(str(threshold.color))

    @staticmethod
    def _normalize_threshold_state_key(level: str) -> ThresholdState | None:
        lookup = level.lower().strip()
        if lookup in {"good", "success", "ok", "pass"}:
            return "good"
        if lookup in {"warn", "warning", "caution", "attention"}:
            return "warn"
        if lookup in {"bad", "critical", "error", "fail", "failure"}:
            return "bad"
        return None

    @staticmethod
    def _state_from_color(color: str) -> ThresholdState | None:
        lookup = color.lower().strip()
        if lookup in {"green", "bright_green"}:
            return "good"
        if lookup in {"yellow", "gold", "amber", "orange"}:
            return "warn"
        if lookup in {"red", "bright_red", "magenta"}:
            return "bad"
        return None

    def add_event(self, message: str, level: str = "INFO") -> None:
        """Add event message (required by display backend protocol).

        Args:
            message: Event message
            level: Log level (unused in this simple display)
        """
        # No-op: this display focuses on parameters only
        pass

    def _render_header_text(self) -> str:
        """Render header as plain text for table title."""
        status_icons = {
            "initializing": "⏳",
            "running": "▶️ ",
            "completed": "✅",
            "failed": "❌",
            "cancelled": "⏹️",
        }
        status_icon = status_icons.get(self.task_status, "❓")
        now = datetime.now()
        elapsed = (now - self.start_time).total_seconds()

        # Format duration display using HH:MM:SS format
        if self.duration is None or self.duration == "0":
            duration_text = f"{self._format_duration(elapsed)} (indefinite)"
        else:
            try:
                duration_val = float(self.duration)
                duration_text = (
                    f"{self._format_duration(elapsed)} / {self._format_duration(duration_val)}"
                )
            except (ValueError, TypeError):
                duration_text = f"Elapsed: {elapsed:.1f}s"

        hour_24 = now.hour
        hour_12 = hour_24 % 12 or 12
        meridiem = "am" if hour_24 < 12 else "pm"
        time_text = f"{hour_12}:{now.minute:02d}{meridiem}"
        date_text = f"{now.month}/{now.day}/{now.year % 100:02d}"
        timestamp_text = f"{time_text} {date_text}"

        return f"{status_icon} {self.task_name.upper()}  •  {timestamp_text}  •  {duration_text}"

    def _render_footer_text(self) -> str:
        """Render footer as plain text for table caption."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.update_count / elapsed if elapsed > 0 else 0.0
        active_count = len([s for s in self.stats.values() if s.count > 0])
        total_count = len(self.schema.fields)
        return f"Updates: {self.update_count}  •  Rate: {rate:.1f}/s  •  Parameters: {active_count}/{total_count}  •  [dim]CTRL+C to stop[/]"

    def _render_table_caption(self) -> str:
        """Combine footer details, alerts, and shutdown summaries for the table caption."""

        lines = [self._render_footer_text()]
        if alert_banner := self._render_alert_banner():
            lines.append(alert_banner)
        for message in self._latest_shutdown_summary_messages:
            lines.append(f"[bold yellow]{message}[/bold yellow]")
        return "\n".join(lines)

    def _aggregate_group_states(self) -> dict[str, str]:
        """Collapse per-parameter health into group-level states."""

        groups: dict[str, list[str]] = {}
        for param_field in self.schema.fields:
            stat = self.stats.get(param_field.name)
            if stat is None:
                continue
            state = self._resolve_param_state(param_field, stat)
            if not state or state == "unknown":
                continue
            group = (
                param_field.group
                or param_field.display_group
                or self._get_task_label(param_field.name)
            )
            groups.setdefault(group, []).append(state)

        collapsed: dict[str, str] = {}
        for group, states in groups.items():
            collapsed[group] = self._reduce_states(states)
        return collapsed

    @staticmethod
    def _reduce_states(states: Iterable[str]) -> str:
        states_list = list(states)
        if any(s == "bad" for s in states_list):
            return "bad"
        if any(s == "warn" for s in states_list):
            return "warn"
        if any(s == "good" for s in states_list):
            return "good"
        return "unknown"

    def _resolve_param_state(self, field: ParameterField, stat: ParameterStats) -> str:
        """Resolve per-parameter health using threshold history or current value."""

        if stat.threshold_states:
            last = stat.threshold_states[-1]
            if last:
                return last

        if normalized := self._normalize_string_state(stat.current):
            return normalized

        if stat.current is not None:
            state = evaluate_param_status(field, stat.current)
            if state != "unknown":
                return state

        if stat.status == ParameterStatus.FAILED:
            return "bad"
        if stat.status in {ParameterStatus.STALE, ParameterStatus.CANCELLED}:
            return "warn"
        if stat.status in {ParameterStatus.STREAMING, ParameterStatus.COMPLETE}:
            return "good"
        return "unknown"

    @staticmethod
    def _normalize_string_state(value: Any) -> str | None:
        if not isinstance(value, str) or not value:
            return None
        return _STRING_STATE_ALIASES.get(value.strip().lower())

    def _collect_group_metrics(
        self, fields: list[ParameterField], *, sparkline_style: str | None = None
    ) -> list[SectionRow]:
        rows: list[SectionRow] = []
        for param_field in fields:
            stat = self.stats.get(param_field.name)
            if stat is None:
                continue
            label = param_field.display_annotation or param_field.name
            detail = self._build_metric_detail(param_field, stat, sparkline_style=sparkline_style)
            rows.append(SectionRow(label=label, detail=detail))
        return rows

    def _build_metric_detail(
        self,
        field: ParameterField,
        stat: ParameterStats,
        *,
        sparkline_style: str | None = None,
    ) -> str:
        history_vals = list(stat.history)
        history_states = list(stat.threshold_states)
        max_width = self._sparkline_style_config(sparkline_style)
        trimmed_values, trimmed_states, truncated = self._prepare_history_for_display(
            history_vals, history_states, max_width=max_width
        )
        sparkline, _ = self._render_sparkline(
            trimmed_values,
            trimmed_states,
            style=sparkline_style,
            enable_color=self._color_output_enabled(),
        )
        trend_arrow_raw = self._calculate_trend(trimmed_values)
        trend_arrow = colorize_trend_arrow(
            trend_arrow_raw,
            trimmed_states,
            enable_color=self._color_output_enabled(),
        )
        if truncated and sparkline:
            sparkline = f"…{sparkline}"

        value_text = self._format_value(stat.current, field)
        goal_text = self._format_goal(field, stat.current)
        state_icon = self._state_icon(self._resolve_param_state(field, stat))
        parts = [state_icon, sparkline, trend_arrow, value_text, goal_text]
        return "  ".join(part for part in parts if part)

    def _sparkline_style_config(self, style: str | None) -> int:
        if style == "dense":
            return 40
        if style in {"compact", "thick"}:
            return 18
        return 25

    def _render_sparkline(
        self,
        values: list[float],
        states: list[ThresholdState | None],
        *,
        style: str | None,
        enable_color: bool,
    ) -> tuple[str, bool]:
        if style == "thin":
            return self._render_thin_sparkline(values, states, enable_color=enable_color)
        return render_colored_sparkline(
            values,
            states,
            enable_color=enable_color,
        )

    def _render_thin_sparkline(
        self,
        values: list[float],
        states: list[ThresholdState | None],
        *,
        enable_color: bool,
    ) -> tuple[str, bool]:
        if not values:
            return "", False

        blocks = _normalize_to_blocks(values)
        colored_segments: list[str] = []
        for idx, block in enumerate(blocks):
            state = states[idx] if idx < len(states) else None
            color = _STATE_COLORS.get(state or "")
            colored_block = f"[{color}]{block}[/{color}]" if color and enable_color else block
            prefix = "─" if idx == 0 else "──"
            colored_segments.append(f"{prefix}{colored_block}")

        return "".join(colored_segments), False

    def _format_goal(self, field: ParameterField, current: Any) -> str:
        goal = field.goal
        if goal is None:
            return ""
        if isinstance(goal, (list, tuple)) and len(goal) == 2:
            goal_desc = f"goal {goal[0]}–{goal[1]}"
        else:
            goal_desc = f"goal {goal}"

        delta = ""
        try:
            if current is not None:
                numeric = float(current)
                target = float(goal[0]) if isinstance(goal, (list, tuple)) else float(goal)
                diff = numeric - target
                if diff != 0:
                    sign = "+" if diff > 0 else ""
                    delta = f"Δ {sign}{diff:.2f}"
        except (TypeError, ValueError):
            pass

        parts = [goal_desc]
        if delta:
            parts.append(delta)
        return f"({'  '.join(parts)})" if parts else ""

    def _icon_for_group(self, group: str) -> str:
        state = self._aggregate_group_states().get(group, "unknown")
        return self._state_icon(state)

    def _state_icon(self, state: str | None) -> str:
        if not state:
            return _STATE_ICONS["unknown"]
        return _STATE_ICONS.get(state, _STATE_ICONS["unknown"])

    def _get_threshold_color_for_value(self, value: Any, param_field: ParameterField) -> str | None:
        """Get threshold color for a value using unified threshold logic.

        Args:
            value: Raw numeric value
            param_field: Parameter field with threshold definitions

        Returns:
            Color string if threshold triggered, None otherwise
        """
        stat = self.stats.get(param_field.name)
        return ThresholdEvaluator.get_color(
            value,
            param_field,
            stats=stat,
            context=self._build_context_snapshot(),
        )

    def _apply_threshold_color(
        self, formatted_value: str, raw_value: Any, param_field: ParameterField
    ) -> str:
        """Apply threshold-based color styling to a formatted value.

        Args:
            formatted_value: Already formatted value string
            raw_value: Raw numeric value for threshold checking
            param_field: Parameter field with threshold definitions

        Returns:
            Formatted value with Rich color markup applied
        """
        stat = self.stats.get(param_field.name)
        return ThresholdEvaluator.apply_color(
            formatted_value,
            raw_value,
            param_field,
            stats=stat,
            context=self._build_context_snapshot(),
        )

    def _format_value(
        self, value: Any, param_field: ParameterField, include_unit: bool = True
    ) -> str:
        """Format value according to field metadata.

        Args:
            value: The value to format
            param_field: Parameter metadata
            include_unit: Whether to include unit suffix (default: True)

        Returns:
            Formatted string
        """
        if value is None:
            return "—"  # Em dash (U+2014) for missing values

        display_format = getattr(param_field, "display_format", None)
        if display_format:
            if isinstance(display_format, dict):
                formatted = display_format.get(value)
                if formatted is None and isinstance(value, (int, float)):
                    int_key = int(value)
                    if int_key == value and int_key in display_format:
                        formatted = display_format[int_key]
                if formatted is None:
                    formatted = display_format.get(str(value))
                if formatted is not None:
                    return formatted
            elif isinstance(display_format, str):
                try:
                    return display_format.format(value=value)
                except Exception:  # pragma: no cover - fallback
                    pass

        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return str(value)[:20]

        precision = param_field.precision if param_field.precision is not None else 2
        unit_label = (getattr(param_field, "unit", "") or "").strip()

        formatted_via_pint = self._format_with_pint(numeric, param_field, include_unit)
        if formatted_via_pint is not None:
            return formatted_via_pint

        # Default numeric formatting fallback when pint is unavailable/unsupported
        if abs(numeric) >= 1000:
            fallback = f"{numeric:,.0f}"
        elif abs(numeric) >= 1:
            fallback = f"{numeric:.{precision}f}"
        else:
            fallback = f"{numeric:.4f}"

        if include_unit and unit_label:
            display_unit = self._format_unit_label(unit_label)
            return f"{fallback} {display_unit}".strip()
        return fallback

    def _format_parameter_row(
        self,
        field: ParameterField,
        stat: ParameterStats,
        *,
        show_task_column: bool,
    ) -> list[str]:
        """Return the legacy row representation used by table-based tests."""

        sparkline_style = getattr(field, "sparkline_style", None)
        history_vals = list(stat.history)
        history_states = list(stat.threshold_states)
        max_width = self._sparkline_style_config(sparkline_style)
        trimmed_values, trimmed_states, truncated = self._prepare_history_for_display(
            history_vals,
            history_states,
            max_width=max_width,
        )

        enable_color = self._color_output_enabled()
        sparkline, _ = self._render_sparkline(
            trimmed_values,
            trimmed_states,
            style=sparkline_style,
            enable_color=enable_color,
        )
        trend_arrow_raw = self._calculate_trend(trimmed_values)
        trend_arrow = colorize_trend_arrow(
            trend_arrow_raw,
            trimmed_states,
            enable_color=enable_color,
        )
        if truncated and sparkline:
            sparkline = f"…{sparkline}"
        trend_cell = "  ".join(part for part in (sparkline, trend_arrow) if part).strip() or "—"

        value_text = self._apply_threshold_color(
            self._format_value(stat.current, field),
            stat.current,
            field,
        )
        average_text = self._format_value(stat.average, field) if stat.average is not None else "—"
        goal_text = self._format_goal(field, stat.current) or ""
        state_icon = self._state_icon(self._resolve_param_state(field, stat))
        status_indicator = self._get_status_indicator(stat)
        connection_icon = self._get_connection_indicator(field.name, stat)
        lifecycle_icon = self._get_lifecycle_indicator(field.name, stat)
        task_label = self._get_task_label(field.name)

        row: list[str] = [
            field.display_annotation or field.name,
            value_text,
            average_text,
            goal_text if goal_text else "—",
            trend_cell,
            state_icon,
            status_indicator,
            connection_icon,
            lifecycle_icon,
        ]
        if show_task_column:
            row.insert(0, task_label)
        return row

    def _format_with_pint(
        self, numeric_value: float, param_field: ParameterField, include_unit: bool
    ) -> str | None:
        """Format using PintValueFormatter when a schema unit is defined."""

        unit_label = (getattr(param_field, "unit", "") or "").strip()
        unit_expr = self._normalize_unit_for_pint(unit_label)
        if not unit_expr or unit_expr in _RAW_ONLY_UNITS:
            return None

        precision = param_field.precision if param_field.precision is not None else 2
        strategy = self._determine_initial_strategy(param_field.name, unit_expr, precision)

        return self._format_with_pint_strategy(
            param_field.name,
            unit_expr,
            precision,
            include_unit,
            numeric_value,
            strategy,
        )

    def _determine_initial_strategy(self, name: str, unit: str, precision: int) -> str:
        """Reuse raw formatting if auto scaling previously failed."""

        if unit in _RAW_ONLY_UNITS:
            return "raw"

        cached = self._formatter_config.get(name)
        if cached and cached == (unit, precision, "raw"):
            return "raw"
        return "auto"

    def _format_with_pint_strategy(
        self,
        name: str,
        unit: str,
        precision: int,
        include_unit: bool,
        numeric_value: float,
        strategy: str,
    ) -> str | None:
        formatter = self._get_value_formatter(name, unit, precision, strategy)
        try:
            if include_unit:
                return formatter.format(numeric_value)
            return formatter.format_magnitude_only(numeric_value)
        except Exception:  # noqa: BLE001
            self._invalidate_formatter(name)
            if strategy == "auto":
                return self._format_with_pint_strategy(
                    name,
                    unit,
                    precision,
                    include_unit,
                    numeric_value,
                    "raw",
                )
            return None

    @staticmethod
    def _normalize_unit_for_pint(unit: str) -> str | None:
        """Map human-friendly unit labels to pint expressions."""

        cleaned = unit.strip()
        if not cleaned:
            return None
        return _PINT_UNIT_ALIASES.get(cleaned, cleaned)

    @staticmethod
    def _format_unit_label(unit: str) -> str:
        cleaned = unit.strip()
        return _DISPLAY_UNIT_LABELS.get(cleaned, cleaned)

    def _invalidate_formatter(self, name: str) -> None:
        """Drop cached formatter so strategy/unit can be rebuilt."""

        self._value_formatters.pop(name, None)
        self._formatter_config.pop(name, None)

    def _get_value_formatter(
        self, name: str, unit: str, precision: int, strategy: str
    ) -> PintValueFormatter:
        """Return cached PintValueFormatter configured for the parameter."""

        desired_config = (unit, precision, strategy)
        cached = self._value_formatters.get(name)

        if cached is not None and self._formatter_config.get(name) == desired_config:
            return cached

        formatter = PintValueFormatter(unit=unit, precision=precision, strategy=strategy)
        self._value_formatters[name] = formatter
        self._formatter_config[name] = desired_config
        return formatter

    def _calculate_trend(self, values: list[float]) -> str:
        """Calculate trend arrow from recent values.

        Args:
            values: Numeric values (minimum 10 required for trend calculation)

        Returns:
            Trend arrow: → (flat), ↗ (up), ↘ (down), ⇈ (steep up), ⇊ (steep down)
        """
        if len(values) < 10:
            return "→"

        # Compare average of first half vs second half of last 20 values for smoother trend
        window = values[-20:] if len(values) >= 20 else values
        mid = len(window) // 2
        first_half_avg = sum(window[:mid]) / mid
        second_half_avg = sum(window[mid:]) / (len(window) - mid)

        # Handle zero division
        if first_half_avg == 0:
            return "→"

        # Calculate percentage change between halves
        change_pct = abs((second_half_avg - first_half_avg) / first_half_avg)

        # Determine trend
        if change_pct < 0.05:  # Less than 5% change
            return "→"
        elif second_half_avg > first_half_avg:
            return "⇈" if change_pct > 0.2 else "↗"  # Steep up (>20%) or gradual
        else:
            return "⇊" if change_pct > 0.2 else "↘"  # Steep down (>20%) or gradual

    def _get_status_indicator(self, stat: ParameterStats) -> str:
        """Get status indicator for parameter data flow.

        Args:
            stat: Parameter statistics

        Returns:
            Status indicator: "⏳" (waiting), "🟢" (streaming), "⚠️" (stale/missing), "❌" (failed)
        """

        stat.evaluate_status(datetime.now(), self.task_status)
        icon_map = {
            ParameterStatus.WAITING: "⏳",
            ParameterStatus.STREAMING: "🟢",
            ParameterStatus.STALE: "⚠️",
            ParameterStatus.FAILED: "❌",
            ParameterStatus.CANCELLED: "⏹️",
            ParameterStatus.COMPLETE: "🔵",
        }
        return icon_map.get(stat.status, "⏳")

    def _get_task_label(self, param_name: str) -> str:
        """Return the normalized task name that owns a parameter."""

        with self._update_lock:
            owner = self._parameter_task_map.get(param_name)
        return owner or "—"

    def _build_context_snapshot(self) -> dict[str, Any]:
        """Build a lightweight context mapping for threshold formulas."""

        context: dict[str, Any] = {}
        with self._update_lock:
            for name, stat in self.stats.items():
                if stat.current is None:
                    continue
                context[name] = stat.current
                owner = self._parameter_task_map.get(name)
                if owner:
                    context[f"{owner}.{name}"] = stat.current
        return context

    def _get_connection_indicator(self, param_name: str, stat: ParameterStats | None) -> str:
        """Return connection state icon for the command feeding this parameter.

        Derived parameters aggregate dependency link states to surface upstream health.
        """

        field = self._get_param_field_by_name(param_name)
        if field and getattr(field, "formula", None):
            dependencies = stat.dependencies if stat else getattr(field, "dependencies", ())
            return self._aggregate_dependency_links(dependencies)

        with self._update_lock:
            command_name = self._parameter_command_map.get(param_name)
            status = self._command_connection_status.get(command_name) if command_name else None
        if not command_name or not status:
            return "—"
        return _CONNECTION_STATUS_ICONS.get(status, "—")

    def _get_lifecycle_indicator(self, param_name: str, stat: ParameterStats | None) -> str:
        """Return lifecycle state icon for the command feeding this parameter."""

        field = self._get_param_field_by_name(param_name)
        if field and getattr(field, "formula", None):
            dependencies = stat.dependencies if stat else getattr(field, "dependencies", ())
            return self._aggregate_dependency_lifecycle(dependencies)

        with self._update_lock:
            command_name = self._parameter_command_map.get(param_name)
            lifecycle = self._command_lifecycle_status.get(command_name) if command_name else None
        if not command_name or not lifecycle:
            return "—"
        return _LIFECYCLE_STATUS_ICONS.get(lifecycle, "—")

    def _aggregate_dependency_links(self, dependencies: tuple[str, ...] | list[str] | None) -> str:
        statuses = self._collect_dependency_statuses(dependencies)
        if not statuses:
            return "—"
        if "failed" in statuses:
            return "🔴"
        if "connecting" in statuses:
            return "🟡"
        if "pending" in statuses:
            return "⚫"
        if all(s == "closed" for s in statuses):
            return "🔵"
        if all(s == "connected" for s in statuses):
            return "🟢"
        return "🟢"

    def _collect_dependency_statuses(
        self, dependencies: tuple[str, ...] | list[str] | None
    ) -> list[str]:
        if not dependencies:
            return []

        dep_statuses: list[str] = []
        with self._update_lock:
            for dep in dependencies:
                dep_name = dep.split(".", 1)[-1] if isinstance(dep, str) else None
                if not dep_name:
                    continue
                command_name = self._parameter_command_map.get(dep_name)
                if not command_name:
                    continue
                status = self._command_connection_status.get(command_name)
                if status:
                    dep_statuses.append(status)

        return dep_statuses

    def _aggregate_dependency_lifecycle(
        self, dependencies: tuple[str, ...] | list[str] | None
    ) -> str:
        statuses = self._collect_dependency_lifecycle_statuses(dependencies)
        if not statuses:
            return "—"
        priority = ["failed", "cancelled", "stopped", "running", "completed", "pending"]
        for state in priority:
            if state in statuses:
                return _LIFECYCLE_STATUS_ICONS.get(state, "—")
        return "—"

    def _collect_dependency_lifecycle_statuses(
        self, dependencies: tuple[str, ...] | list[str] | None
    ) -> list[str]:
        if not dependencies:
            return []

        lifecycle_statuses: list[str] = []
        with self._update_lock:
            for dep in dependencies:
                dep_name = dep.split(".", 1)[-1] if isinstance(dep, str) else None
                if not dep_name:
                    continue
                command_name = self._parameter_command_map.get(dep_name)
                if not command_name:
                    continue
                lifecycle = self._command_lifecycle_status.get(command_name)
                if lifecycle:
                    lifecycle_statuses.append(lifecycle)

        return lifecycle_statuses

    def _build_stale_summary_message(self, parameters: Sequence[str]) -> str:
        count = len(parameters)
        noun = "parameter" if count == 1 else "parameters"
        preview = ", ".join(parameters[:5])
        suffix = "…" if len(parameters) > 5 else ""
        if preview:
            return f"{count} {noun} never produced data before shutdown: {preview}{suffix}"
        return f"{count} {noun} never produced data before shutdown."

    def _format_duration(self, seconds: float | timedelta) -> str:
        """Format durations as HH:MM:SS when >=1 hour else MM:SS."""
        if isinstance(seconds, timedelta):
            total_seconds = int(seconds.total_seconds())
        else:
            try:
                total_seconds = int(float(seconds))
            except (TypeError, ValueError):
                total_seconds = 0
        hours, remainder = divmod(total_seconds, 3600)
        minutes, secs = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
