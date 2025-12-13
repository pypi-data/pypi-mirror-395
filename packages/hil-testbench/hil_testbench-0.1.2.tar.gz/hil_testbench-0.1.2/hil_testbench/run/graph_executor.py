"""Global GraphExecutor orchestrates command-level DAG execution across tasks.

Responsibilities:
- Build ordered ``TaskConfig`` list for each task (REQ-EXEC-001)
- Delegate to :class:`TaskOrchestrator` for flattened DAG execution
- Provide simple success/failure aggregation and exit code mapping

GraphExecutor is the public facade for CLI flows; TaskOrchestrator owns
execution per ``architecture.md`` Section 2.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, cast

from rich.console import Console

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.display.display_finalizer import DisplayFinalizer
from hil_testbench.run.exceptions import ConfigurationError, ExecutionError, HILTestbenchError
from hil_testbench.run.execution.protocols import DisplayBackendProtocol
from hil_testbench.run.logging.task_logger import LogLevel, LogScope
from hil_testbench.run.task_orchestrator import (
    TaskOrchestrator,
    TaskOrchestratorDependencies,
)


class GraphExecutor:
    """Unified global executor for one or multiple tasks.

    Always uses the multi-task path for consistency (single task treated as list of one).
    """

    def __init__(
        self,
        console: Console | None = None,
        *,
        orchestrator: TaskOrchestrator | None = None,
        dependencies: TaskOrchestratorDependencies | None = None,
    ) -> None:
        if orchestrator is not None and dependencies is not None:
            raise ConfigurationError(
                "GraphExecutor requires either orchestrator or dependencies, not both",
                context={
                    "orchestrator_type": type(orchestrator).__name__,
                    "dependencies_type": type(dependencies).__name__,
                },
            )

        if orchestrator is not None:
            self._runner = orchestrator
            return

        if dependencies is None:
            dependencies = TaskOrchestratorDependencies.build(console=console)

        self._runner = TaskOrchestrator(dependencies=dependencies)

    def execute(
        self, tasks: Iterable[Any], configs: dict[str, TaskConfig]
    ) -> tuple[int, dict[str, Any]]:
        """Execute all tasks via unified DAG.

        Args:
            tasks: Iterable of instantiated task objects
            configs: Mapping task_name -> TaskConfig (keys are CLI task names from run_tasks.py)

        Returns:
            (exit_code, outcomes_dict) where:
            - exit_code: 0 for success, 1 for failure
            - outcomes_dict: maps task name to TaskOutcome
        """
        task_list = list(tasks)
        if not task_list:
            return 1, {}

        # Match tasks to configs - run_tasks.py creates them in same order
        # configs keys are task names from CLI (e.g., 'task1', 'task2')
        config_keys = list(configs.keys())
        if len(task_list) != len(config_keys):
            raise ConfigurationError(
                "Task/config count mismatch",
                context={
                    "tasks": len(task_list),
                    "configs": len(config_keys),
                },
            )

        # Build ordered list: (task_name, task_instance, config)
        config_objects = []
        for idx, task in enumerate(task_list):
            name = config_keys[idx]
            cfg = configs[name]
            config_objects.append((name, task, cfg))

        # Use TaskOrchestrator multi-task execution for flattened DAG
        runner = self._runner

        # Extract task instances and configs in order
        task_instances = [task for _, task, _ in config_objects]
        task_configs = [cfg for _, _, cfg in config_objects]

        try:
            outcome = runner.execute_multiple(task_instances, task_configs)
        except Exception as exc:  # noqa: BLE001
            normalized = self._normalize_graph_exception(
                exc,
                task_names=config_keys,
            )
            if normalized is exc:
                raise
            raise normalized from exc

        # outcome.success per task accessible via outcome.tasks dict
        failed = [name for name, t_out in outcome.tasks.items() if not t_out.success]
        exit_code = 1 if failed else 0

        return exit_code, outcome.tasks

    def get_task_logger(self):  # Expose underlying logger for CLI summary
        return self._runner.get_task_logger()

    def was_cancelled(self) -> bool:
        """Expose cancellation status from the underlying orchestrator."""
        checker = getattr(self._runner, "was_cancelled", None)
        return bool(checker() if callable(checker) else False)

    def consume_interrupt_flag(self) -> bool:
        """Return True if an external interrupt occurred during execution."""
        consumer = getattr(self._runner, "consume_interrupt_flag", None)
        return bool(consumer() if callable(consumer) else False)

    def get_log_directory(self) -> str | None:
        """Get execution log directory path.

        Returns:
            Absolute path to log directory, or None if unavailable.
        """
        if task_logger := self.get_task_logger():
            try:
                return task_logger.get_execution_dir()
            except Exception as exc:  # noqa: S110
                task_logger.log(
                    "log_directory_lookup_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    error=str(exc),
                    error_type=type(exc).__name__,
                )
        return None

    def get_display_backend(self) -> DisplayBackendProtocol | None:
        """Get display backend for final rendering.

        Returns:
            Display backend instance, or None if unavailable.
        """
        task_logger = self.get_task_logger()
        getter = getattr(task_logger, "get_display_backend", None) if task_logger else None
        backend = getter() if callable(getter) else None
        return cast(DisplayBackendProtocol | None, backend)

    def render_final_display(self) -> None:
        """Render final display state for failed runs.

        Call this after execute() completes to show final metrics.
        Only renders if task failed and display backend exists.
        """
        backend = self.get_display_backend()
        if backend is None:
            return

        task_logger = self.get_task_logger()
        if task_logger is None:
            return

        DisplayFinalizer(task_logger=task_logger).render(backend)

    def _normalize_graph_exception(
        self, exc: Exception, *, task_names: list[str]
    ) -> HILTestbenchError:
        context = {"tasks": ", ".join(task_names)} if task_names else {}
        if isinstance(exc, HILTestbenchError):
            if context:
                exc.add_context(**context)
            return exc
        try:
            raise ExecutionError(
                "Task orchestration failed",
                context=context,
            ) from exc
        except ExecutionError as wrapped:
            return wrapped
