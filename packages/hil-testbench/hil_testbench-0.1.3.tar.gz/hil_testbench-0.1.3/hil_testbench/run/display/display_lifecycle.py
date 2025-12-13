"""Display backend lifecycle helpers for task execution."""

from __future__ import annotations

import importlib
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from rich.console import Console

from hil_testbench.run.execution.protocols import (
    DisplayBackendProtocol,
    SupportsCommandStatus,
    SupportsSchemaUpdates,
    SupportsTaskStatus,
)
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.run.results.task_outcome import TaskOutcome
from hil_testbench.task.specs import TaskDefinition

if TYPE_CHECKING:
    from hil_testbench.run.execution.execution_session import ExecutionSession


_CUSTOM_BACKEND_ENV = "HIL_TESTBENCH_DISPLAY_BACKEND"


class DisplayLifecycle:
    """Encapsulates display backend initialization and status updates."""

    def __init__(self, console: Console | None = None):
        self._console = console

    def initialize_task_displays(
        self,
        task_definitions: list[TaskDefinition],
        task_logger: TaskLogger,
        session: ExecutionSession,
        duration: str,
    ) -> None:
        _ = session  # Reserved for future display lifecycle hooks
        # Extract original task names (before namespacing) for display
        task_names = [
            td.name.split(":")[0] if ":" in td.name else td.name for td in task_definitions
        ]
        combined_task_name = ", ".join(sorted(set(task_names)))

        for task_def in task_definitions:
            backend = self.ensure_display_backend(
                task_def, task_logger, duration, combined_task_name
            )
            self.update_task_status(task_logger, backend, task_def.name, "running")
            self.set_display_schema(task_logger, backend, task_def)

    def ensure_display_backend(
        self,
        task_def: TaskDefinition,
        task_logger: TaskLogger,
        duration: str,
        display_name: str | None = None,
    ) -> DisplayBackendProtocol | None:
        backend = self.get_display_backend(task_logger)
        if backend or not task_def.parameters_schema:
            return backend
        try:
            backend = self._create_display_backend(task_def, duration, task_logger)
            if backend is None:
                return None
            task_logger.set_display_backend(backend)
            backend.start(display_name or task_def.name)
            return backend
        except Exception as exc:  # noqa: BLE001
            task_logger.log(
                "display_backend_init_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task_name=task_def.name,
                error=str(exc),
            )
            return None

    @staticmethod
    def get_display_backend(task_logger: TaskLogger) -> DisplayBackendProtocol | None:
        getter = getattr(task_logger, "get_display_backend", None)
        if callable(getter):
            backend = getter()
            return cast(DisplayBackendProtocol | None, backend)
        return None

    def update_task_status(
        self,
        task_logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        status: str,
    ) -> None:
        if backend and isinstance(backend, SupportsTaskStatus):
            try:
                backend.update_task_status(task_name, status)
            except Exception as exc:  # noqa: BLE001
                task_logger.log(
                    "display_update_task_status_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task_name=task_name,
                    status=status,
                    error=str(exc),
                )

    def set_display_schema(
        self,
        task_logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_def: TaskDefinition,
    ) -> None:
        if task_def.parameters_schema and backend and isinstance(backend, SupportsSchemaUpdates):
            try:
                backend.set_schema(task_def.name, task_def.parameters_schema)
            except Exception as exc:  # noqa: BLE001
                task_logger.log(
                    "display_set_schema_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task_name=task_def.name,
                    error=str(exc),
                )

    def update_final_task_status(
        self,
        task_logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        outcome: TaskOutcome | bool,
    ) -> None:
        if backend and isinstance(backend, SupportsTaskStatus):
            status = "completed" if self._outcome_success(outcome) else "failed"
            try:
                backend.update_task_status(task_name, status)
            except Exception as exc:  # noqa: BLE001
                task_logger.log(
                    "display_update_task_status_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task_name=task_name,
                    status=status,
                    error=str(exc),
                )

    @staticmethod
    def _outcome_success(outcome: TaskOutcome | bool) -> bool:
        """Return True when the provided outcome indicates task success."""

        if isinstance(outcome, TaskOutcome):
            return outcome.success
        return bool(outcome)

    def handle_command_start(
        self,
        logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        command_name: str,
    ) -> None:
        self.safe_update_command_status(
            logger,
            backend,
            task_name,
            command_name,
            lifecycle_status="running",
        )
        # Emit "connected" after any startup delay so the live link turns green only
        # while the command body is executing.
        self.safe_update_command_status(
            logger,
            backend,
            task_name,
            command_name,
            "connected",
        )

    def handle_command_completion(
        self,
        logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        command_name: str,
        result: Any,
    ) -> None:
        status = self.result_status(result)
        self.safe_update_command_status(
            logger,
            backend,
            task_name,
            command_name,
            lifecycle_status=status,
        )

    def handle_command_exception(
        self,
        logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        command_name: str,
        start_time: datetime,
        exc: Exception,
    ) -> None:
        self.safe_update_command_status(
            logger,
            backend,
            task_name,
            command_name,
            lifecycle_status="failed",
        )
        self.safe_update_command_status(
            logger,
            backend,
            task_name,
            command_name,
            "failed",
        )
        duration = (datetime.now() - start_time).total_seconds()
        logger.log(
            "command_failed",
            LogLevel.ERROR,
            scope=LogScope.COMMAND,
            task=task_name,
            command=command_name,
            message="Command execution raised an exception",
            duration_seconds=f"{duration:.2f}",
            error=str(exc),
            error_type=type(exc).__name__,
        )

    def _create_display_backend(
        self,
        task_def: TaskDefinition,
        duration: str,
        task_logger: TaskLogger,
    ):
        """Return a backend instance: env override → default LiveDisplay."""
        schema = task_def.parameters_schema
        if not schema:
            return None

        backend_cls = self._load_backend_from_env(task_logger, task_def.name)

        if backend_cls is not None:
            try:
                return backend_cls(schema, duration=duration, console=self._console)
            except Exception as exc:
                task_logger.log(
                    "Custom display backend failed to initialize",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    backend_spec=os.getenv(_CUSTOM_BACKEND_ENV),
                    error=str(exc),
                    task=task_def.name,
                )

        # fallback to the standard live display
        from hil_testbench.display.live_display import LiveDisplayManager

        display_config = getattr(task_def, "display_config", None)
        return LiveDisplayManager(
            schema,
            duration=duration,
            console=self._console,
            display_config=display_config,
        )

    @staticmethod
    def result_status(result: Any) -> str:
        if isinstance(result, int):
            return "completed" if result == 0 else "failed"
        if hasattr(result, "success"):
            return "completed" if result.success else "failed"
        return "completed"

    @staticmethod
    def safe_update_command_status(
        logger: TaskLogger,
        backend: DisplayBackendProtocol | None,
        task_name: str,
        command_name: str,
        status: str | None = None,
        *,
        lifecycle_status: str | None = None,
    ) -> None:
        if backend and isinstance(backend, SupportsCommandStatus):
            logger.notify_display_command_status(
                task_name,
                command_name,
                status,
                backend,
                lifecycle_status=lifecycle_status,
            )

    @staticmethod
    def _load_backend_from_env(task_logger: TaskLogger, task_name: str):
        """Load a display backend specified as 'module:Class'. Returns a class or None."""
        spec = os.getenv(_CUSTOM_BACKEND_ENV)
        if not spec:
            return None

        if ":" not in spec:
            task_logger.log(
                "display_backend_invalid_spec",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                task=task_name,
                backend_spec=spec,
            )
            return None

        module_name, class_name = spec.split(":", 1)
        try:
            module = importlib.import_module(module_name)
            backend_cls = getattr(module, class_name)
            return backend_cls
        except Exception as exc:
            task_logger.log(
                "Failed to load custom display backend",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                backend_spec=spec,
                error=str(exc),
                task=task_name,
            )
            return None
