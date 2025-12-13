from __future__ import annotations

import argparse
import traceback
from typing import Any

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.run.exceptions import HILTestbenchError
from hil_testbench.run.graph_executor import GraphExecutor
from hil_testbench.run.logging.task_logger import (
    LogLevel,
    LogScope,
    TaskLogger,
    flush_cli_messages,
)
from hil_testbench.run.logging.task_logger_factory import TaskLoggerFactory
from hil_testbench.run.orchestration.runtime_context import RuntimeContextBuilder
from hil_testbench.run.session.log_directory_manager import (
    LogDirectoryManager,
    mark_log_cleanup_checked,
    should_run_log_cleanup,
)
from hil_testbench.run.task_orchestrator import (
    TaskOrchestrator,
    TaskOrchestratorDependencies,
)

from .constants import LOG_HINT
from .run_summary import print_execution_summary
from .task_builder import build_task_instances, ensure_adaptive_pipeline_defaults
from .task_utils import join_task_names, task_word
from .utils import emit_cli_message, safe_symbol


def execute_tasks(
    task_list: list[str],
    args: argparse.Namespace,
    yaml_data: dict,
    run_config: Any,
    yaml_tasks: dict[str, Any],
) -> int:
    joined = join_task_names(task_list)
    try:
        instances, configs = build_task_instances(
            task_list, args, yaml_data, run_config, yaml_tasks
        )
    except RuntimeError as exc:
        emit_cli_message(
            event="cli_runtime_error",
            message=f"Error: {exc}",
            icon="❌",
            level=LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            stderr=True,
        )
        flush_cli_messages()
        return 1

    run_config = ensure_adaptive_pipeline_defaults(run_config)

    preconfigured_logger = _prepare_preconfigured_logger(configs)
    executor = _build_graph_executor(preconfigured_logger)
    _log_task_banner(preconfigured_logger, task_list, joined)

    try:
        exit_code, outcomes = executor.execute(instances, configs)
    except HILTestbenchError as exc:
        return _handle_testbench_error(exc, executor)
    except Exception as exc:  # noqa: BLE001
        return _handle_unexpected_error(exc, executor)

    interrupted = False
    consume_interrupt = getattr(executor, "consume_interrupt_flag", None)
    if callable(consume_interrupt):
        interrupted = consume_interrupt()
        if interrupted:
            exit_code = 130

    print_execution_summary(executor, exit_code, task_list, outcomes)
    flush_cli_messages(getattr(executor, "get_task_logger", lambda: None)())
    return 130 if interrupted else exit_code


def _handle_testbench_error(exc: HILTestbenchError, executor: GraphExecutor) -> int:
    """Handle HILTestbenchError with structured logging."""
    logger = getattr(executor, "get_task_logger", lambda: None)()
    cause_text = str(exc.__cause__) if exc.__cause__ else None
    message = f"Task Execution Error ({type(exc).__name__}): {exc}"
    if cause_text:
        message = f"{message} (Caused by: {cause_text})"
    if logger:
        logger.log(
            "execution_error",
            LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            icon="❌",
            message=message,
            error_type=type(exc).__name__,
            error=str(exc),
            caused_by=cause_text,
        )
    emit_cli_message(
        event="cli_execution_error",
        message=message,
        icon="❌",
        level=LogLevel.ERROR,
        scope=LogScope.FRAMEWORK,
        stderr=True,
    )
    emit_cli_message(
        event="cli_log_hint",
        message=LOG_HINT,
        icon="📁",
        level=LogLevel.INFO,
        scope=LogScope.FRAMEWORK,
        stderr=True,
    )
    flush_cli_messages(logger)
    return 1


def _handle_unexpected_error(exc: Exception, executor: GraphExecutor) -> int:
    """Handle unexpected exceptions with structured logging."""
    logger = getattr(executor, "get_task_logger", lambda: None)()
    cli_message = f"Execution Error: {exc}"
    trace_details = None
    if logger:
        logger.exception(
            "unexpected_execution_error",
            icon="❌",
            message=cli_message,
            error_type=type(exc).__name__,
            error=str(exc),
        )
    else:
        trace_details = traceback.format_exc()
    emit_cli_message(
        event="cli_unexpected_execution_error",
        message=cli_message,
        icon="❌",
        level=LogLevel.ERROR,
        scope=LogScope.FRAMEWORK,
        stderr=True,
    )
    if trace_details:
        emit_cli_message(
            event="cli_unexpected_execution_error_trace",
            message=f"Traceback (most recent call last):\n{trace_details}",
            icon="🧵",
            level=LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            stderr=True,
        )
    emit_cli_message(
        event="cli_log_hint",
        message=LOG_HINT,
        icon="📁",
        level=LogLevel.INFO,
        scope=LogScope.FRAMEWORK,
        stderr=True,
    )
    flush_cli_messages(logger)
    return 1


def _prepare_preconfigured_logger(configs: dict[str, TaskConfig]) -> TaskLogger | None:
    if not configs:
        return None

    try:
        primary_config = next(iter(configs.values()))
    except StopIteration:
        return None

    run_config = primary_config.run_config
    factory = TaskLoggerFactory()
    log_dir = run_config.log_dir or "logs"
    if not should_run_log_cleanup(log_dir):
        return None
    logger = factory.create(run_config=run_config, log_dir=log_dir)
    log_manager = LogDirectoryManager(logger)
    if run_config.auto_prune:
        log_manager.prune_old_directories(run_config)
    else:
        log_manager.check_and_suggest_cleanup(run_config)
    mark_log_cleanup_checked(log_dir)
    return logger


def _build_graph_executor(preconfigured_logger: TaskLogger | None) -> GraphExecutor:
    if preconfigured_logger is None:
        return GraphExecutor()

    logger_factory = TaskLoggerFactory(preconfigured_logger=preconfigured_logger)
    dependencies = TaskOrchestratorDependencies.build()
    dependencies.runtime_builder = RuntimeContextBuilder(logger_factory=logger_factory)
    orchestrator = TaskOrchestrator(dependencies=dependencies)
    return GraphExecutor(orchestrator=orchestrator)


def _log_task_banner(logger: TaskLogger | None, task_list: list[str], joined_names: str) -> None:
    emit_cli_message(
        event="task_execution_start",
        icon=safe_symbol("🚀"),
        message=f"Running {len(task_list)} {task_word(task_list)}: {joined_names}",
        level=LogLevel.INFO,
    )
