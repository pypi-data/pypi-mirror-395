"""Derived parameter evaluation orchestrator."""

from __future__ import annotations

from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
from datetime import datetime
from threading import Event
from typing import TYPE_CHECKING, Any

from hil_testbench.data_processing.expression_engine import CompiledExpression, ExpressionEngine
from hil_testbench.data_structs.parameters import ParameterField, ParametersSchema
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

if TYPE_CHECKING:  # pragma: no cover - used for typing only
    from hil_testbench.run.session.parameter_context import ParameterContext
    from hil_testbench.run.session.time_windowed_stats import TimeWindowedStatsRegistry


@dataclass(frozen=True)
class DependencyGraph:
    """Topologically ordered derived parameters."""

    levels: list[list[str]]
    params: Mapping[str, ParameterField]


class DerivedParameterProcessor:
    """Evaluate derived parameters in dependency order."""

    _MAX_WORKERS = 4
    _EVAL_TIMEOUT_SECONDS = 0.01

    def __init__(
        self,
        schema: ParametersSchema,
        expression_engine: ExpressionEngine,
        parameter_context: ParameterContext,
        windowed_stats: TimeWindowedStatsRegistry,
        logger: TaskLogger | None = None,
    ) -> None:
        self._schema = schema
        self._expression_engine = expression_engine
        self._parameter_context = parameter_context
        self._windowed_stats = windowed_stats
        self._logger = logger
        self._executor = ThreadPoolExecutor(max_workers=self._MAX_WORKERS)

        self._graph = self._build_dependency_graph(schema)
        self._compiled: dict[str, CompiledExpression] = {}
        self._compile_all()

        self._dirty: set[str] = set(self._graph.params.keys())
        self._logged_errors: set[str] = set()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def mark_dirty(self, updated_params: set[str]) -> None:
        """Mark derived params dirty when dependencies change."""

        if not updated_params:
            return
        updated_short = {name.split(".", 1)[-1] for name in updated_params}
        for name, field in self._graph.params.items():
            deps = set(getattr(field, "dependencies", ()) or ())
            if deps & updated_params or deps & updated_short:
                self._dirty.add(name)

    def evaluate_all(self, task_name: str) -> list[dict[str, Any]]:
        """Evaluate all dirty derived parameters and return emitted events."""

        events: list[dict[str, Any]] = []
        if not self._dirty:
            return events

        evaluated: set[str] = set()
        for level in self._graph.levels:
            to_eval = [name for name in level if name in self._dirty]
            if not to_eval:
                continue

            futures = self._schedule_level(task_name, to_eval)
            self._consume_futures(task_name, futures, evaluated, events)
        self._dirty.difference_update(evaluated)
        return events

    def _schedule_level(self, task_name: str, params: list[str]) -> list[tuple[str, Any, Event]]:
        futures: list[tuple[str, Any, Event]] = []
        for name in params:
            stop_event = Event()
            fut = self._executor.submit(self._evaluate_one, task_name, name, stop_event)
            futures.append((name, fut, stop_event))
        return futures

    def _consume_futures(
        self,
        task_name: str,
        futures: list[tuple[str, Any, Event]],
        evaluated: set[str],
        events: list[dict[str, Any]],
    ) -> None:
        for name, fut, stop_event in futures:
            evaluated.add(name)
            try:
                event = fut.result(timeout=self._EVAL_TIMEOUT_SECONDS)
            except TimeoutError:
                stop_event.set()
                event = self._handle_timeout(task_name, name)
            except Exception as exc:  # noqa: BLE001
                event = self._handle_exception(task_name, name, exc)
            if event is not None:
                events.append(event)

    def shutdown(self) -> None:
        """Placeholder for future resource cleanup."""

        self._executor.shutdown(wait=False, cancel_futures=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_dependency_graph(self, schema: ParametersSchema) -> DependencyGraph:
        derived, dependencies, dependents = self._collect_dependencies(schema)
        in_degree = self._compute_in_degree(derived, dependencies)
        levels = self._topological_levels(in_degree, dependents)
        return DependencyGraph(levels=levels, params=derived)

    def _collect_dependencies(
        self, schema: ParametersSchema
    ) -> tuple[dict[str, ParameterField], dict[str, set[str]], dict[str, set[str]]]:
        derived = {f.name: f for f in schema.fields if getattr(f, "formula", None)}
        dependencies: dict[str, set[str]] = {}
        dependents: dict[str, set[str]] = {name: set() for name in derived}
        for name, field in derived.items():
            deps = {str(dep) for dep in (getattr(field, "dependencies", ()) or ())}
            dependencies[name] = deps
            for dep in deps:
                if dep in dependents:
                    dependents[dep].add(name)
        return derived, dependencies, dependents

    def _compute_in_degree(
        self, derived: dict[str, ParameterField], dependencies: dict[str, set[str]]
    ) -> dict[str, int]:
        in_degree: dict[str, int] = {}
        for name, deps in dependencies.items():
            derived_deps = {dep for dep in deps if dep in derived}
            in_degree[name] = len(derived_deps)
        return in_degree

    def _topological_levels(
        self, in_degree: dict[str, int], dependents: dict[str, set[str]]
    ) -> list[list[str]]:
        levels: list[list[str]] = []
        while True:
            zero_deg = [name for name, degree in in_degree.items() if degree == 0]
            if not zero_deg:
                break
            levels.append(zero_deg)
            for name in zero_deg:
                in_degree[name] = -1
                for dep in dependents.get(name, ()):
                    if dep in in_degree:
                        in_degree[dep] -= 1

        if any(deg >= 0 for deg in in_degree.values()):
            raise ValueError(
                "Circular dependency detected in derived parameters",
            ) from None
        return levels

    def _compile_all(self) -> None:
        for name, field in self._graph.params.items():
            formula = getattr(field, "formula", None)
            if not formula:
                continue
            self._compiled[name] = self._expression_engine.compile(formula)

    def _evaluate_one(
        self,
        task_name: str,
        param_name: str,
        stop_event: Event | None = None,
    ) -> dict[str, Any] | None:
        field = self._graph.params.get(param_name)
        if field is None:
            return None
        compiled = self._compiled.get(param_name)
        if compiled is None:
            return None

        if stop_event and stop_event.is_set():
            return None

        namespace = self._build_namespace(field)
        value: Any
        error: str | None = None
        try:
            value = self._expression_engine.evaluate(compiled, namespace)
        except Exception as exc:  # noqa: BLE001
            value = None
            error = str(exc)
            if param_name not in self._logged_errors and self._logger:
                self._logger.log(
                    "derived_parameter_evaluation_failed",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    task=task_name,
                    parameter=param_name,
                    formula=getattr(field, "formula", ""),
                    error=error,
                )
                self._logged_errors.add(param_name)

        if stop_event and stop_event.is_set():
            return None

        owner_task = getattr(field, "task", None) or task_name
        timestamp = datetime.now().timestamp()
        return self._persist_result(field, param_name, owner_task, value, timestamp, error)

    def _handle_timeout(self, task_name: str, param_name: str) -> dict[str, Any] | None:
        field = self._graph.params.get(param_name)
        if field is None:
            return None
        error = f"evaluation timeout (>{self._EVAL_TIMEOUT_SECONDS:.3f}s)"
        if param_name not in self._logged_errors and self._logger:
            self._logger.log(
                "derived_parameter_evaluation_timeout",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=task_name,
                parameter=param_name,
                formula=getattr(field, "formula", ""),
                timeout_seconds=self._EVAL_TIMEOUT_SECONDS,
                error=error,
            )
            self._logged_errors.add(param_name)
        owner_task = getattr(field, "task", None) or task_name
        timestamp = datetime.now().timestamp()
        return self._persist_result(field, param_name, owner_task, None, timestamp, error)

    def _handle_exception(
        self, task_name: str, param_name: str, exc: Exception
    ) -> dict[str, Any] | None:
        field = self._graph.params.get(param_name)
        if field is None:
            return None
        error = str(exc)
        if param_name not in self._logged_errors and self._logger:
            self._logger.log(
                "derived_parameter_evaluation_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=task_name,
                parameter=param_name,
                formula=getattr(field, "formula", ""),
                error=error,
            )
            self._logged_errors.add(param_name)
        owner_task = getattr(field, "task", None) or task_name
        timestamp = datetime.now().timestamp()
        return self._persist_result(field, param_name, owner_task, None, timestamp, error)

    def _persist_result(
        self,
        field: ParameterField,
        param_name: str,
        owner_task: str,
        value: Any,
        timestamp: float,
        error: str | None,
    ) -> dict[str, Any]:
        self._parameter_context.set(f"{owner_task}.{param_name}", value, timestamp)
        self._parameter_context.set(param_name, value, timestamp)
        self._windowed_stats.get(f"{owner_task}.{param_name}").append(timestamp, value)
        self._windowed_stats.get(param_name).append(timestamp, value)

        return {
            "param_name": param_name,
            "value": value,
            "unit": getattr(field, "unit", ""),
            "timestamp": timestamp,
            "task": owner_task,
            "derived": True,
            "formula": getattr(field, "formula", None),
            "formula_version": getattr(field, "formula_version", None),
            "dependencies": list(getattr(field, "dependencies", ()) or ()),
            "error": error,
        }

    def _build_namespace(self, field: ParameterField) -> dict[str, Any]:
        namespace: dict[str, Any] = {}
        deps = getattr(field, "dependencies", ()) or ()
        for dep in deps:
            value = self._parameter_context.get(dep)
            namespace[dep] = value
            if "." in dep:
                namespace[dep.split(".", 1)[-1]] = value
        namespace["ctx"] = self._parameter_context.as_dict()
        return namespace


__all__ = ["DerivedParameterProcessor", "DependencyGraph"]
