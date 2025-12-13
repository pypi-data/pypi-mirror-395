from __future__ import annotations

"""Command preparation utilities extracted from TaskOrchestrator."""

import os
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.data_processing.pipeline import (
    PipelineFactoryArgs,
    make_pipeline_callback_factory,
)
from hil_testbench.data_structs.hosts import HostDefinition
from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.run.display.display_lifecycle import DisplayLifecycle
from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.execution.command_runner import CommandRunner
from hil_testbench.run.execution.command_spec import CommandSpec, PreparedEntry
from hil_testbench.run.execution.shell_wrapper import resolve_shell_wrapper_mode
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.task.specs import (
    CommandDefinition,
    SinkDefinition,
    TaskDefinition,
)


@dataclass
class PreparedCommands:
    """Container for prepared command execution artifacts."""

    entries: list[tuple[PreparedEntry, list[str] | None]]
    command_validators: dict[str, Any]
    failed_commands: set[str]
    backend: Any | None
    cancellation_requested: bool
    cancel_reason: str | None


@dataclass
class CommandPreparationState:
    """Mutable preparation state while building PreparedEntry list."""

    task_entries: list[tuple[PreparedEntry, list[str] | None]]
    command_validators: dict[str, Any]
    failed_commands: set[str]
    cancellation_requested: bool = False
    cancel_reason: str | None = None


class CommandPreparer:
    """Translates TaskDefinitions into PreparedEntry execution records."""

    def __init__(self, display_lifecycle: DisplayLifecycle) -> None:
        self._display_lifecycle = display_lifecycle

    def prepare(
        self,
        runner: CommandRunner,
        task_definitions: Iterable[TaskDefinition],
        *,
        task_logger: TaskLogger,
        task_def_map: dict[str, TaskDefinition],
        failed_commands: set[str],
        config: TaskConfig | None,
        config_by_task: dict[str, TaskConfig] | None = None,
        duration: str | None,
        wrap_command: Callable[..., Callable],
        dependency_resolver: Callable[[list[CommandDefinition]], list[CommandDefinition]],
    ) -> PreparedCommands:
        backend = self._display_lifecycle.get_display_backend(task_logger)
        state = CommandPreparationState(
            task_entries=[],
            command_validators={},
            failed_commands=failed_commands,
        )

        for task_def in task_definitions:
            if state.cancellation_requested:
                break
            self._prepare_single_task(
                runner,
                task_def,
                task_logger,
                backend,
                state,
                task_def_map=task_def_map,
                config=config,
                config_by_task=config_by_task,
                duration=duration,
                wrap_command=wrap_command,
                dependency_resolver=dependency_resolver,
            )

        return PreparedCommands(
            entries=state.task_entries,
            command_validators=state.command_validators,
            failed_commands=state.failed_commands,
            backend=backend,
            cancellation_requested=state.cancellation_requested,
            cancel_reason=state.cancel_reason,
        )

    def _prepare_single_task(
        self,
        runner: CommandRunner,
        task_def: TaskDefinition,
        task_logger: TaskLogger,
        backend: Any | None,
        state: CommandPreparationState,
        *,
        task_def_map: dict[str, TaskDefinition],
        config: TaskConfig | None,
        config_by_task: dict[str, TaskConfig] | None,
        duration: str | None,
        wrap_command: Callable[..., Callable],
        dependency_resolver: Callable[[list[CommandDefinition]], list[CommandDefinition]],
    ) -> None:
        task_display_name = self._task_display_name(task_def)
        self._log_task_start(task_logger, task_display_name, duration)
        sorted_commands = self._resolve_task_commands_safe(
            task_def,
            task_display_name,
            dependency_resolver,
            task_logger,
        )

        base_parser_factory = task_def.parser.factory if task_def.parser else None
        base_schema = task_def.parameters_schema if hasattr(task_def, "parameters_schema") else None
        base_sinks = task_def.sinks

        for command in sorted_commands:
            if self._shutdown_requested(runner, task_logger):
                state.cancellation_requested = True
                state.cancel_reason = state.cancel_reason or "Shutdown signal requested by user"
                runner.cancel_all()
            if self._should_skip_command(
                command, state.failed_commands, task_logger, task_display_name
            ):
                continue

            parser_factory, schema, sinks = self._resolve_command_io(
                task_def_map,
                base_parser_factory,
                base_schema,
                base_sinks,
                command.name,
            )
            if command.parameters_schema:
                schema = command.parameters_schema

            self._prepare_single_command(
                runner,
                command,
                task_display_name,
                task_logger,
                backend,
                parser_factory,
                schema,
                sinks,
                config,
                config_by_task,
                state,
                wrap_command=wrap_command,
                task_allows_parallel=self._command_allows_parallel(
                    command.name,
                    task_def,
                    task_def_map,
                ),
            )

    @staticmethod
    def _task_display_name(task_def: TaskDefinition) -> str:
        if task_def.name != "__multi_task__" or not task_def.commands:
            return task_def.name
        task_names = {cmd.name.split(":", 1)[0] for cmd in task_def.commands if ":" in cmd.name}
        return ", ".join(sorted(task_names)) if task_names else task_def.name

    @staticmethod
    def _log_task_start(
        task_logger: TaskLogger,
        task_display_name: str,
        duration: str | None,
    ) -> None:
        duration_text = "indefinite" if not duration or duration is None else f"{duration}s"
        task_logger.log(
            "task_start",
            LogLevel.INFO,
            scope=LogScope.TASK,
            task=task_display_name,
            icon="▶️",
            message=f"Starting {task_display_name} (duration: {duration_text})",
            duration=duration,
        )

    @staticmethod
    def _resolve_task_commands_safe(
        task_def: TaskDefinition,
        task_display_name: str,
        dependency_resolver: Callable[[list[CommandDefinition]], list[CommandDefinition]],
        task_logger: TaskLogger | None,
    ) -> list[CommandDefinition]:
        try:
            return dependency_resolver(task_def.commands)
        except ConfigurationError as error:
            error.add_context(task=task_display_name)
            raise
        except Exception as error:  # noqa: BLE001
            if task_logger:
                task_logger.log(
                    "dependency_resolution_failed",
                    LogLevel.ERROR,
                    scope=LogScope.FRAMEWORK,
                    message="Dependency resolver raised unexpected error",
                    task=task_display_name,
                    error=str(error),
                    error_type=type(error).__name__,
                    remediation=(
                        "Inspect task dependency declarations for cycles or missing"
                        " prerequisites. Remove dynamic dependency mutation before execution."
                    ),
                )
            raise ConfigurationError(
                "Dependency resolution failed",
                context={
                    "task": task_display_name,
                    "details": str(error),
                    "remediation": (
                        "Review task commands and depends_on fields for cycles or typos."
                        " Ensure MultiTaskPlanner namespaces commands prior to execution."
                    ),
                },
            ) from error

    @staticmethod
    def _shutdown_requested(runner: CommandRunner, task_logger: TaskLogger) -> bool:
        shutdown_file = os.path.join(runner.get_execution_dir(), "shutdown.signal")
        if not os.path.exists(shutdown_file):
            return False
        task_logger.log_shutdown_signal(shutdown_file=shutdown_file)
        return True

    @staticmethod
    def _should_skip_command(
        command: CommandDefinition,
        failed_commands: set[str],
        task_logger: TaskLogger,
        display_task_name: str,
    ) -> bool:
        if not command.depends_on:
            return False
        failed_deps = [dep for dep in command.depends_on if dep in failed_commands]
        if not failed_deps:
            return False
        task_logger.log(
            "dependency_failed_skip",
            LogLevel.WARNING,
            scope=LogScope.COMMAND,
            task=display_task_name,
            command=command.name,
            failed_dependencies=", ".join(failed_deps),
        )
        failed_commands.add(command.name)
        return True

    @staticmethod
    def _resolve_command_io(
        task_def_map: dict[str, TaskDefinition],
        base_parser,
        base_schema,
        base_sinks,
        command_name: str,
    ) -> tuple[Any | None, ParametersSchema | None, SinkDefinition | None]:
        if task_def_map and ":" in command_name:
            cmd_task_name = command_name.split(":", 1)[0]
            if original_def := task_def_map.get(cmd_task_name):
                parser_factory = original_def.parser.factory if original_def.parser else None
                schema = (
                    original_def.parameters_schema
                    if hasattr(original_def, "parameters_schema")
                    else None
                )
                sinks = original_def.sinks
                return parser_factory, schema, sinks
        return base_parser, base_schema, base_sinks

    def _prepare_single_command(
        self,
        runner: CommandRunner,
        command: CommandDefinition,
        display_task_name: str,
        task_logger: TaskLogger,
        backend: Any | None,
        parser_factory: Any | None,
        command_schema: ParametersSchema | None,
        command_sinks: SinkDefinition | None,
        config: TaskConfig | None,
        config_by_task: dict[str, TaskConfig] | None,
        state: CommandPreparationState,
        *,
        wrap_command: Callable[..., Callable],
        task_allows_parallel: bool,
    ) -> None:
        host = self._command_host(command)
        display_backend = backend or self._display_lifecycle.get_display_backend(task_logger)
        self._register_validator(command, display_task_name, task_logger, display_backend, state)
        self._register_command_with_backend(
            display_backend,
            display_task_name,
            command.name,
            task_logger,
            owned_parameters=command.owned_parameters,
        )
        command_config = self._select_command_config(command.name, config, config_by_task)
        display_config = self._extract_display_config(command_config)
        run_cfg = getattr(command_config, "run_config", None)
        if run_cfg is None:
            raise ConfigurationError(
                "TaskConfig.run_config missing",
                context={
                    "task": display_task_name,
                    "command": command.name,
                },
            )

        pipeline_args = self._build_pipeline_args(
            display_task_name,
            command,
            parser_factory,
            display_backend,
            command_schema,
            command_sinks,
            display_config,
            command_config,
            run_cfg,
            task_logger,
            runner.state if hasattr(runner, "state") else None,
        )
        cb_factory = make_pipeline_callback_factory(pipeline_args)
        is_remote = bool(host) and not (isinstance(host, HostDefinition) and host.local)
        wrapper_mode = resolve_shell_wrapper_mode(
            command.use_shell_wrapper,
            getattr(run_cfg, "shell_wrapper_mode", "auto"),
            is_remote=is_remote,
        )
        logged_command_func = wrap_command(
            command.run,
            display_task_name,
            command.name,
            runner,
            concurrent=task_allows_parallel,
        )
        logged_command_func = self._apply_startup_delay(logged_command_func, command, task_logger)

        streaming_format = "structured" if parser_factory is not None else "text"
        spec = CommandSpec(
            command_name=command.name,
            task_name=display_task_name,
            long_running=bool(command.long_running),
            streaming_format=streaming_format,
            parser_factory=parser_factory,
            shell_wrapper_mode=wrapper_mode,
            use_pty=command.use_pty,
            immediate=bool(command.immediate),
            host=host,
            env=command.env,
            cwd=command.cwd,
            tags=tuple(command.tags),
            retry=int(command.retry or 0),
            exclusive=bool(getattr(command, "exclusive", False)) or not task_allows_parallel,
        )
        logged_command_func._command_spec = spec  # type: ignore[attr-defined]

        entry = PreparedEntry(
            func=logged_command_func,
            spec=spec,
            callback_factory=cb_factory,
        )
        state.task_entries.append((entry, command.depends_on or []))

    @staticmethod
    def _select_command_config(
        command_name: str,
        default_config: TaskConfig | None,
        config_by_task: dict[str, TaskConfig] | None,
    ) -> TaskConfig | None:
        if config_by_task and ":" in command_name:
            task_prefix = command_name.split(":", 1)[0]
            if task_prefix in config_by_task:
                return config_by_task[task_prefix]
        return default_config

    @staticmethod
    def _command_allows_parallel(
        command_name: str,
        task_def: TaskDefinition,
        task_def_map: dict[str, TaskDefinition],
    ) -> bool:
        if ":" in command_name and task_def_map:
            task_prefix = command_name.split(":", 1)[0]
            if task_prefix in task_def_map:
                return getattr(task_def_map[task_prefix], "concurrent", True)
        return getattr(task_def, "concurrent", True)

    def _register_validator(
        self,
        command: CommandDefinition,
        display_task_name: str,
        task_logger: TaskLogger,
        backend: Any | None,
        state: CommandPreparationState,
    ) -> None:
        if command.validator:
            task_logger.log(
                "validator_registered",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                command_name=command.name,
                message=(
                    f"Registered validator for command '{command.name}' in task "
                    f"'{display_task_name}'"
                ),
                task_name=display_task_name,
                validator_type=type(command.validator).__name__,
            )
            state.command_validators[command.name] = (command.validator, backend)
            return
        task_logger.log(
            "no_validator",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            command_name=command.name,
            task_name=display_task_name,
        )

    @staticmethod
    def _register_command_with_backend(
        backend: Any | None,
        task_name: str,
        command_name: str,
        task_logger: TaskLogger,
        *,
        owned_parameters: list[str] | None = None,
    ) -> None:
        if backend and hasattr(backend, "register_command"):
            try:
                backend.register_command(task_name, command_name, owned_parameters)
            except Exception as exc:  # noqa: BLE001
                task_logger.log(
                    "display_register_command_failed",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    task_name=task_name,
                    command_name=command_name,
                    backend_type=type(backend).__name__,
                    error=str(exc),
                )

    @staticmethod
    def _extract_display_config(config: TaskConfig | None) -> dict[str, Any] | None:
        if config and hasattr(config, "display") and isinstance(config.display, dict):
            return config.display.get("parameters", {})
        return None

    @staticmethod
    def _build_pipeline_args(
        task_name: str,
        command: CommandDefinition,
        parser_factory: Any | None,
        backend: Any | None,
        command_schema: ParametersSchema | None,
        command_sinks: SinkDefinition | None,
        display_config: dict[str, Any] | None,
        config: TaskConfig | None,
        run_cfg: Any,
        task_logger: TaskLogger,
        session: Any | None,
    ) -> PipelineFactoryArgs:
        # Extract individual task name from command name in multi-task scenarios
        # Command names are formatted as "task:command" in multi-task mode
        individual_task_name = command.name.split(":", 1)[0] if ":" in command.name else task_name

        enable_jsonl = True if command_sinks is None else command_sinks.enable_jsonl
        enable_csv = True if command_sinks is None else command_sinks.enable_csv
        max_bytes = config.max_data_size_mb * 1024 * 1024 if config else 100 * 1024 * 1024
        max_rotations = config.max_log_file_count_task if config else 10

        # Detect streaming behavior: If task has a parser, assume it needs live streaming
        # Per streaming-execution-architecture.md: Framework decides streaming behavior, not YAML/tasks
        # Tasks with parsers produce structured events that should be flushed immediately
        has_parser = parser_factory is not None

        if has_parser:
            # Force aggressive flush for tasks with parsers (live event streaming)
            event_buffer_max = 1  # Flush after every single event
            event_max_age_ms = 50  # Flush if event older than 50ms
        else:
            # Use configured values or defaults for raw output tasks
            event_buffer_max = getattr(run_cfg, "event_buffer_max", 50)
            event_max_age_ms = getattr(run_cfg, "event_max_age_ms", 500)

        return PipelineFactoryArgs(
            task_name=individual_task_name,
            command_name=command.name,
            parser_factory=parser_factory,
            display_backend=backend,
            enable_jsonl=enable_jsonl,
            enable_csv=enable_csv,
            custom_file_base=(command_sinks.file_base if command_sinks else None),
            task_logger=task_logger,
            parameters_schema=command_schema,
            display_config=display_config,
            max_bytes=max_bytes,
            max_rotations=max_rotations,
            event_buffer_max=event_buffer_max,
            event_max_age_ms=event_max_age_ms,
            dynamic_field_cap=getattr(run_cfg, "event_dynamic_field_cap", 500),
            session=session,
        )

    @staticmethod
    def _apply_startup_delay(
        func: Callable,
        command: CommandDefinition,
        task_logger: TaskLogger,
    ) -> Callable:
        if command.startup_delay <= 0:
            return func

        def delayed_func(ctx: Any) -> Any:
            task_logger.log(
                "startup_delay",
                LogLevel.DEBUG,
                message="Delaying startup",
                scope=LogScope.COMMAND,
                task=command.name,
                show_fields_with_message=True,
                delay_seconds=command.startup_delay,
            )
            time.sleep(command.startup_delay)
            return func(ctx)

        delayed_func._task_name = getattr(func, "_task_name", None)  # type: ignore[attr-defined]
        delayed_func._command_name = getattr(  # type: ignore[attr-defined]
            func, "_command_name", None
        )
        return delayed_func

    @staticmethod
    def _command_host(command: CommandDefinition) -> HostDefinition | str | None:
        host = command.host
        if host is None:
            return None
        if isinstance(host, HostDefinition):
            return host
        if hasattr(host, "as_string"):
            return host.as_string()
        return host if isinstance(host, str) else str(host)
