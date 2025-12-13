"""Execution session implementation for runtime state and duration guards."""

from __future__ import annotations

import contextlib
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from hil_testbench.data_processing.derived_processor import DerivedParameterProcessor
from hil_testbench.data_processing.expression_engine import ExpressionEngine
from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.run.execution.command_result import CancellationClassification
from hil_testbench.run.execution.command_spec import CommandSpec
from hil_testbench.run.logging.task_logger import LogLevel, LogScope
from hil_testbench.run.session.parameter_context import ParameterContext
from hil_testbench.run.session.time_windowed_stats import TimeWindowedStatsRegistry

_DURATION_GUARD_GRACE_SECONDS = 5.0


@dataclass
# ExecutionSession deliberately manages only in-run state. Command specs are
# not persisted across executions; callers rebuild fresh specs for each new
# run. The session surfaces streaming helpers and guards for the current
# lifecycle.
class ExecutionSession:
    task_logger: Any
    runner: Any
    process_tracker: Any
    duration_seconds: float | None

    completed_commands: set[str] = field(default_factory=set)
    failed_commands: set[str] = field(default_factory=set)
    parameter_context: ParameterContext = field(default_factory=ParameterContext)
    time_windowed_stats: TimeWindowedStatsRegistry = field(
        default_factory=TimeWindowedStatsRegistry
    )
    derived_processor: DerivedParameterProcessor | None = None
    expression_engine: ExpressionEngine = field(default_factory=ExpressionEngine)
    _streamers: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _contexts: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _specs: dict[str, CommandSpec] = field(default_factory=dict, init=False, repr=False)
    _parameter_metadata: dict[str, dict[str, Any]] = field(
        default_factory=dict, init=False, repr=False
    )
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _derived_schema: ParametersSchema | None = field(default=None, init=False, repr=False)

    _cancel_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _duration_guard_thread: threading.Thread | None = field(default=None, init=False, repr=False)
    _duration_guard_stop_event: threading.Event | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        getter = getattr(self.runner, "get_cancel_event", None)
        if callable(getter):
            event = getter()
            if isinstance(event, threading.Event):
                self._cancel_event = event

    # ------------------------------------------------------------------
    # Streamer + context helpers
    # ------------------------------------------------------------------
    def iter_contexts(self) -> list[tuple[str, Any]]:
        with self._lock:
            return list(self._contexts.items())

    def iter_command_specs(self) -> list[tuple[str, CommandSpec]]:
        with self._lock:
            return list(self._specs.items())

    def active_command_count(self) -> int:
        with self._lock:
            return len(self._contexts)

    def register_streamer(self, command_name: str, streamer: Any) -> None:
        with self._lock:
            self._streamers[command_name] = streamer

    def remove_streamer(self, command_name: str) -> None:
        with self._lock:
            self._streamers.pop(command_name, None)

    def stop_all_streamers(self) -> None:
        with self._lock:
            streamers = list(self._streamers.values())
            self._streamers.clear()
        for streamer in streamers:
            stopper = getattr(streamer, "stop", None)
            if callable(stopper):
                with contextlib.suppress(Exception):
                    stopper()
            waiter = getattr(streamer, "wait_for_completion", None)
            if callable(waiter):
                with contextlib.suppress(Exception):
                    waiter(1.0)
            flusher = getattr(streamer, "flush_callbacks", None)
            if callable(flusher):
                with contextlib.suppress(Exception):
                    flusher()

    def register_context(self, command_name: str, context: Any) -> None:
        with self._lock:
            self._contexts[command_name] = context

    def remove_context(self, command_name: str) -> None:
        with self._lock:
            self._contexts.pop(command_name, None)

    def register_command_spec(self, command_name: str, spec: CommandSpec | None) -> None:
        if spec is None:
            return
        with self._lock:
            self._specs[command_name] = spec

    def remove_command_spec(self, command_name: str) -> None:
        with self._lock:
            self._specs.pop(command_name, None)

    def get_command_spec(self, command_name: str) -> CommandSpec | None:
        with self._lock:
            return self._specs.get(command_name)

    def shutdown_summary(self) -> tuple[int, int]:
        with self._lock:
            return len(self._contexts), len(self._streamers)

    # ------------------------------------------------------------------
    # Derived parameter helpers
    # ------------------------------------------------------------------
    def register_schema(self, schema: ParametersSchema | None) -> None:
        """Merge schema into derived processor state and initialize if needed."""

        if schema is None:
            return
        with self._lock:
            if self._derived_schema is None:
                self._derived_schema = schema
            else:
                self._derived_schema = self._derived_schema.extend_with_fields(schema.fields)
            self._rebuild_derived_processor_locked()

    def record_parameter_event(
        self,
        task_name: str,
        param_name: str,
        value: Any,
        timestamp: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> set[str]:
        """Record a parameter update into shared context and mark derived dirty."""

        ts = float(timestamp) if timestamp is not None else time.time()
        qualified = f"{task_name}.{param_name}" if task_name else param_name
        self.parameter_context.set(qualified, value, ts)
        self.parameter_context.set(param_name, value, ts)
        self.time_windowed_stats.get(qualified).append(ts, value)
        self.time_windowed_stats.get(param_name).append(ts, value)

        if metadata:
            metadata_copy = dict(metadata)
            with self._lock:
                self._parameter_metadata[qualified] = metadata_copy
                self._parameter_metadata[param_name] = metadata_copy

        updated = {qualified, param_name}
        if self.derived_processor:
            self.derived_processor.mark_dirty(updated)
        return updated

    def get_parameter_metadata(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            stored = self._parameter_metadata.get(key)
            return dict(stored) if stored is not None else None

    # ------------------------------------------------------------------
    # Duration guard lifecycle
    # ------------------------------------------------------------------
    def start_duration_guard(self) -> None:
        if self.duration_seconds is None or self.duration_seconds <= 0:
            return
        if self._duration_guard_thread:
            return
        stop_event = threading.Event()
        delay = self.duration_seconds + _DURATION_GUARD_GRACE_SECONDS
        thread = self._create_duration_guard_thread(delay, stop_event)
        thread.daemon = True
        thread.start()
        self._duration_guard_thread = thread
        self._duration_guard_stop_event = stop_event
        self.task_logger.log(
            "duration_guard_scheduled",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            duration_seconds=self.duration_seconds,
            guard_delay_seconds=delay,
            grace_seconds=_DURATION_GUARD_GRACE_SECONDS,
        )

    def cancel_duration_guard(self) -> None:
        if not self._duration_guard_thread or not self._duration_guard_stop_event:
            return
        self._duration_guard_stop_event.set()
        self._duration_guard_thread.join(timeout=1.0)
        self._duration_guard_thread = None
        self._duration_guard_stop_event = None

    def _create_duration_guard_thread(
        self, delay: float, stop_event: threading.Event
    ) -> threading.Thread:
        return threading.Thread(target=self._duration_guard_loop, args=(delay, stop_event))

    def _duration_guard_loop(self, delay: float, stop_event: threading.Event) -> None:
        if stop_event.wait(delay):
            return
        self._enforce_duration_guard()
        self._duration_guard_thread = None
        self._duration_guard_stop_event = None

    def _enforce_duration_guard(self) -> None:
        duration = self.duration_seconds or 0.0
        reason = f"Duration limit reached ({duration:.1f}s)"
        self.task_logger.log(
            "duration_guard_triggered",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            message="Requested duration elapsed; canceling in-flight commands",
            duration_seconds=duration,
        )
        cancel_all = getattr(self.runner, "cancel_all", None)
        if callable(cancel_all):
            cancel_all(
                reason=reason,
                classification=CancellationClassification.DURATION_LIMIT,
            )

    # ------------------------------------------------------------------
    # Shutdown + cancellation helpers
    # ------------------------------------------------------------------
    def get_cancel_event(self) -> threading.Event:
        return self._cancel_event

    def was_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    def shutdown(self) -> None:
        self.cancel_duration_guard()
        self.stop_all_streamers()
        with self._lock:
            self._specs.clear()
        if self.derived_processor:
            with contextlib.suppress(Exception):
                self.derived_processor.shutdown()
            self.derived_processor = None
        self.parameter_context.clear()
        self.time_windowed_stats.clear()
        backend = self._safe_task_logger_call("get_display_backend")
        if backend:
            shutdown = getattr(backend, "shutdown", None)
            if callable(shutdown):
                with contextlib.suppress(Exception):
                    shutdown()
        runner_shutdown = getattr(self.runner, "shutdown", None)
        if callable(runner_shutdown):
            with contextlib.suppress(Exception):
                runner_shutdown()

    def log_event(self, event: str, **kwargs: Any) -> None:
        self.task_logger.log(event, LogLevel.DEBUG, scope=LogScope.FRAMEWORK, **kwargs)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _safe_task_logger_call(self, method: str) -> Any:
        func = getattr(self.task_logger, method, None)
        if callable(func):
            try:
                return func()
            except Exception:  # pragma: no cover - defensive
                return None
        return None

    def _rebuild_derived_processor_locked(self) -> None:
        if self._derived_schema is None:
            return
        if self.derived_processor:
            with contextlib.suppress(Exception):
                self.derived_processor.shutdown()
        self.expression_engine.bind_windowed_stats(self.time_windowed_stats)
        self.derived_processor = DerivedParameterProcessor(
            schema=self._derived_schema,
            expression_engine=self.expression_engine,
            parameter_context=self.parameter_context,
            windowed_stats=self.time_windowed_stats,
            logger=self.task_logger,
        )


__all__ = ["ExecutionSession"]
