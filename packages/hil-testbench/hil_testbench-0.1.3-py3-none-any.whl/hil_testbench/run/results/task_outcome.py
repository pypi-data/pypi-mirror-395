"""TaskOutcome dataclass aggregating command results for a task.

Provides a structured summary separate from individual CommandResult objects
without reintroducing legacy TaskResult naming. Users can opt into this
via TaskRunner.execute_with_summary() while existing execute() return type
remains a list of CommandResult for backward compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from hil_testbench.run.execution.command_result import (
    CancellationClassification,
    CommandResult,
    CommandStatus,
)


@dataclass(slots=True)
class ParameterDataSummary:
    """Track which parameters produced data vs. remained silent."""

    with_data: list[str]
    without_data: list[str]


@dataclass(slots=True)
class TaskOutcome:
    """Aggregate outcome for a single task execution.

    Attributes:
        task_name: Logical task name.
        command_results: List of per-command results.
        success: True if all commands succeeded.
        total_commands: Count of commands executed.
        failed_commands: Count of commands failed.
        cancelled: True if task ended due to cancellation request.
        cancelled_commands: Count of commands marked as cancelled.
        start_time: Wall-clock start timestamp.
        end_time: Wall-clock end timestamp.
        duration_seconds: Elapsed time in seconds.
        correlation_id: Runner correlation ID for tracing.
        log_directory: Directory containing JSONL/CSV/log files.
    """

    task_name: str
    command_results: list[CommandResult]
    success: bool
    total_commands: int
    failed_commands: int
    cancelled: bool
    cancelled_commands: int
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    correlation_id: str | None
    log_directory: str | None
    parameter_data_summary: ParameterDataSummary | None = None
    cancellation_classification: CancellationClassification = CancellationClassification.NONE

    def failed(self) -> bool:
        """Return True if any command failed."""
        return not self.success

    def commands_by_status(self, success: bool = True) -> list[CommandResult]:
        """Filter command results by success state."""
        return [r for r in self.command_results if r.success is success]

    def format_summary(self) -> str:
        """Return a human-readable summary for console/log outputs."""

        treat_user_cancel_as_success = self._treat_user_cancellation_as_success()
        missing_parameters = self._missing_parameters()
        warning_due_to_missing_data = bool(missing_parameters)

        if warning_due_to_missing_data:
            status_symbol = "⚠️"
        elif treat_user_cancel_as_success:
            status_symbol = "🟢"
        elif self.cancelled:
            status_symbol = "⏹️"
        elif self.success:
            status_symbol = "🟢"
        else:
            status_symbol = "🔴"
        passed = max(self.total_commands - self.failed_commands - self.cancelled_commands, 0)
        duration = f"{self.duration_seconds:.1f}s" if self.duration_seconds else "N/A"
        stats: list[str] = [
            duration,
            f"{passed} passed",
            f"{self.failed_commands} failed",
        ]
        if self.cancelled_commands and not treat_user_cancel_as_success:
            stats.append(f"{self.cancelled_commands} cancelled")
        if missing_parameters:
            stats.append(f"{len(missing_parameters)} missing data")
        header = f"{status_symbol} {self.task_name} ({', '.join(stats)})"

        lines = [header]

        self._append_parameter_summary(lines)

        cancelled_results = self._cancelled_results()
        failed_results = [
            r for r in self.command_results if (not r.success) and r not in cancelled_results
        ]
        if failed_results:
            lines.append("  Failed commands:")
            for result in failed_results:
                reason = result.get_error_detail()
                lines.append(f"    └─ {result.command_name}: exit {result.return_code} - {reason}")

        if cancelled_results and not treat_user_cancel_as_success:
            lines.append("  Cancelled commands:")
            for result in cancelled_results:
                reason = result.status_message or "Cancelled by request"
                lines.append(f"    └─ {result.command_name}: {reason}")

        return "\n".join(lines)

    def _cancelled_results(self) -> list[CommandResult]:
        """Return command results marked as cancelled."""

        cancelled_results: list[CommandResult] = []
        for result in self.command_results:
            if getattr(result, "cancelled", False):
                cancelled_results.append(result)
                continue
            status = getattr(result, "status", None)
            if status == CommandStatus.CANCELLED:
                cancelled_results.append(result)
        return cancelled_results

    def _treat_user_cancellation_as_success(self) -> bool:
        return (
            self.cancelled
            and self.failed_commands == 0
            and self.cancellation_classification == CancellationClassification.USER
        )

    def _parameter_data_lists(self) -> tuple[list[str], list[str]]:
        if not self.parameter_data_summary:
            return [], []
        return (
            list(self.parameter_data_summary.with_data),
            list(self.parameter_data_summary.without_data),
        )

    def _missing_parameters(self) -> list[str]:
        if not self.parameter_data_summary:
            return []
        return list(self.parameter_data_summary.without_data)

    def _append_parameter_summary(self, lines: list[str]) -> None:
        collected, missing = self._parameter_data_lists()
        if collected:
            lines.append(f"  ✓ Data collected: {', '.join(collected[:5])}")
            if len(collected) > 5:
                lines.append(f"    ... and {len(collected) - 5} more")
        if missing:
            lines.append(f"  ⚠️ No data before shutdown: {', '.join(missing[:5])}")
            if len(missing) > 5:
                lines.append(f"    ... and {len(missing) - 5} more")


@dataclass(slots=True)
class MultiTaskOutcome:
    """Aggregate outcome for multi-task execution.

    Attributes:
        tasks: Map of task_name to TaskOutcome for each executed task.
    """

    tasks: dict[str, TaskOutcome]

    @property
    def overall_success(self) -> bool:
        """True if all tasks succeeded."""
        return all(outcome.success for outcome in self.tasks.values())

    @property
    def any_cancelled(self) -> bool:
        """True if any task ended due to cancellation."""
        return any(outcome.cancelled for outcome in self.tasks.values())

    @property
    def total_commands(self) -> int:
        """Total commands across all tasks."""
        return sum(outcome.total_commands for outcome in self.tasks.values())

    @property
    def failed_commands(self) -> int:
        """Total failed commands across all tasks."""
        return sum(outcome.failed_commands for outcome in self.tasks.values())

    @property
    def cancelled_commands(self) -> int:
        """Total cancelled commands across all tasks."""
        return sum(outcome.cancelled_commands for outcome in self.tasks.values())

    @property
    def cancelled_tasks(self) -> int:
        """Count of tasks impacted by cancellation."""
        return sum(bool(outcome.cancelled) for outcome in self.tasks.values())

    def failed(self) -> bool:
        """Return True if any task failed."""
        return not self.overall_success

    def get_task(self, task_name: str) -> TaskOutcome | None:
        """Get outcome for specific task."""
        return self.tasks.get(task_name)
