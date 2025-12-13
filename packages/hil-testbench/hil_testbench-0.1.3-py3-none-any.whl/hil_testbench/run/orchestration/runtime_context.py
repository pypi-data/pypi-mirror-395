"""Runtime context builder for command execution."""

from __future__ import annotations

import os
from dataclasses import dataclass

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.execution.command_runner import (
    CommandRunner,
    CommandRunnerSettings,
)
from hil_testbench.run.logging.task_logger import TaskLogger
from hil_testbench.run.logging.task_logger_factory import TaskLoggerFactory
from hil_testbench.run.session.log_directory_manager import (
    LogDirectoryManager,
    mark_log_cleanup_checked,
    should_run_log_cleanup,
)
from hil_testbench.run.session.process_state_store import ProcessStateStore
from hil_testbench.run.session.process_tracker import ProcessTracker


@dataclass(slots=True)
class RuntimeContext:
    """Aggregates runtime components needed for task execution."""

    runner: CommandRunner
    process_tracker: ProcessTracker
    task_logger: TaskLogger


class RuntimeContextBuilder:
    """Constructs runtime components for the TaskOrchestrator."""

    def __init__(self, logger_factory: TaskLoggerFactory | None = None) -> None:
        self._logger_factory = logger_factory or TaskLoggerFactory()

    def build(self, config: TaskConfig) -> RuntimeContext:
        log_dir = config.run_config.log_dir or "logs"
        task_logger = self._logger_factory.create(
            run_config=config.run_config,
            log_dir=log_dir,
        )
        # Check log directory state and either prune (if enabled) or suggest cleanup
        self._handle_log_directories(task_logger, config)

        state_dir_override = getattr(config.run_config, "state_dir", None)
        state_path: str | None = None
        if state_dir_override:
            expanded_dir = os.path.abspath(os.path.expanduser(state_dir_override))
            state_path = os.path.join(expanded_dir, "process_state.json")
        state_store = ProcessStateStore(path=state_path, logger=task_logger)
        process_tracker = ProcessTracker(task_logger, state_store=state_store)
        runner = self._build_runner(
            config, process_tracker, task_logger, log_dir, state_store=state_store
        )
        return RuntimeContext(
            runner=runner,
            process_tracker=process_tracker,
            task_logger=task_logger,
        )

    def _handle_log_directories(self, task_logger: TaskLogger, config: TaskConfig) -> None:
        """Handle log directory management based on configuration.

        If auto_prune is enabled, automatically prune old directories.
        Otherwise, just check and suggest cleanup if limits are exceeded.
        """
        run_config = config.run_config
        log_manager = LogDirectoryManager(task_logger)
        log_dir = task_logger.log_dir
        if not should_run_log_cleanup(log_dir):
            return
        if run_config.auto_prune:
            log_manager.prune_old_directories(run_config)
        else:
            log_manager.check_and_suggest_cleanup(run_config)
        mark_log_cleanup_checked(log_dir)

    def _build_runner(
        self,
        config: TaskConfig,
        process_tracker: ProcessTracker,
        task_logger: TaskLogger,
        log_dir: str,
        *,
        state_store: ProcessStateStore,
    ) -> CommandRunner:
        settings = CommandRunnerSettings(
            verbose=True,
            log_dir=log_dir,
            max_bytes_main=config.max_log_size_main_mb * 1024 * 1024,
            max_bytes_task=config.max_log_size_task_mb * 1024 * 1024,
            max_log_file_count_main=config.run_config.max_log_file_count_main,
            max_log_file_count_task=config.max_log_file_count_task,
            enable_health_logging=config.enable_runner_health,
            health_interval=config.runner_health_interval,
            health_cpu_threshold=config.run_config.health_cpu_threshold,
            health_memory_threshold=config.run_config.health_memory_threshold,
            health_disk_threshold_gb=config.run_config.health_disk_threshold_gb,
            signal_force_grace_seconds=config.run_config.signal_force_grace_seconds,
            ssh_max_retries=config.run_config.ssh_connection_max_retries,
            ssh_retry_delay=config.run_config.ssh_connection_retry_delay,
            shell_wrapper_mode=getattr(config.run_config, "shell_wrapper_mode", "auto"),
            forced_cleanup_timeout=getattr(config.run_config, "force_cleanup_timeout", 5.0),
        )
        return CommandRunner(
            settings=settings,
            config=config,
            process_tracker=process_tracker,
            task_logger=task_logger,
            state_store=state_store,
        )
