from __future__ import annotations

from contextlib import suppress
from typing import Any

from hil_testbench.run.execution.protocols import SupportsPrimaryParameterSummary
from hil_testbench.run.graph_executor import GraphExecutor
from hil_testbench.run.logging.task_logger import (
    LogLevel,
    LogScope,
    flush_cli_messages,
)

from .task_utils import join_task_names, task_word
from .utils import emit_cli_message, safe_symbol


def print_execution_summary(
    executor: GraphExecutor,
    exit_code: int,
    task_list: list[str],
    outcomes: dict[str, Any],
) -> None:
    """Emit human-friendly execution summaries and display fallback info."""
    log_directory = executor.get_log_directory()
    get_logger = getattr(executor, "get_task_logger", lambda: None)
    task_logger = get_logger()
    if exit_code == 0:
        _print_success_summary(task_list, executor, log_directory)
    else:
        _print_failure_summary(outcomes)

    _print_log_directory(log_directory)

    backend = executor.get_display_backend()
    if backend is not None:
        # Insert a raw newline so the static display snapshot does not
        # collide with the preceding CLI summary text; using emit_cli_message
        # would create an extra structured log event we do not want.
        print()  # hil: allow-print
    executor.render_final_display()
    flush_cli_messages(task_logger)


def _print_success_summary(
    task_list: list[str],
    executor: GraphExecutor,
    log_directory: str | None,
) -> None:
    emit_cli_message(
        event="execution_success_summary",
        icon=safe_symbol("✅"),
        message=f"All {len(task_list)} {task_word(task_list)} completed successfully",
    )
    _emit_primary_parameters(executor, log_directory)


def _print_failure_summary(outcomes: dict[str, Any]) -> None:
    failed = [name for name, outcome in outcomes.items() if not outcome.success]
    if not failed:
        return
    emit_cli_message(
        event="execution_failure_summary",
        icon=safe_symbol("❌"),
        message=f"Failed {task_word(failed)}: {join_task_names(failed)}",
        level=LogLevel.ERROR,
        stderr=True,
    )


def _print_log_directory(log_directory: str | None) -> None:
    if log_directory:
        emit_cli_message(
            event="log_directory_hint",
            icon=safe_symbol("📁"),
            message=f"\nLogs: {log_directory}",
        )
        return
    emit_cli_message(
        event="log_directory_unavailable",
        icon=safe_symbol("⚠️"),
        message="\nWarning: Log directory unavailable (unexpected state)",
        level=LogLevel.WARNING,
        scope=LogScope.FRAMEWORK,
        stderr=True,
    )


def _emit_primary_parameters(executor: GraphExecutor, log_directory: str | None) -> None:
    backend = executor.get_display_backend()
    if not backend or not isinstance(backend, SupportsPrimaryParameterSummary):
        return
    summary = None
    with suppress(Exception):
        summary = backend.get_primary_parameter_summary()
    if not summary:
        return
    emit_cli_message(
        event="primary_parameters_header",
        icon=safe_symbol("📊"),
        message="\nPrimary Parameters:",
    )
    for param_name, (value, unit) in summary.items():
        emit_cli_message(
            event="primary_parameter",
            message=f"  {param_name}: {_format_value(value)}{_format_unit(unit)}",
        )
    if log_directory:
        emit_cli_message(
            event="primary_parameters_hint",
            message="  (See logs for complete data)",
        )


def _format_value(value: Any) -> str:
    return f"{value:.2f}" if isinstance(value, float) else str(value)


def _format_unit(unit: str | None) -> str:
    return f" {unit}" if unit else ""
