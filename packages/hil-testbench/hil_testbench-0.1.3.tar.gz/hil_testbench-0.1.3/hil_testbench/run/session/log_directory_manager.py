"""Log directory management: automatic pruning of old execution directories.

This module provides cleanup of execution log directories to prevent
disk space exhaustion during development. Directories are pruned based on:
- Maximum count: keep only the N most recent directories (default: 50)
- Maximum age: delete directories older than N days (default: 30)

By default, automatic pruning is DISABLED. The system will only suggest
cleanup when limits are exceeded. Use --prune-logs to manually clean up,
or set auto_prune=true in config to enable automatic cleanup.

Safety features:
- Never deletes the current execution directory
- Protects the 'latest-run' pointer file
- Logs all pruning actions for auditability
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from hil_testbench.run.logging.task_logger import LogLevel, LogScope

if TYPE_CHECKING:
    from hil_testbench.config.run_config import RunConfig
    from hil_testbench.run.logging.task_logger import TaskLogger


@dataclass(slots=True)
class PruneStats:
    """Statistics from a log directory pruning operation."""

    total_dirs: int = 0
    pruned_count: int = 0
    protected_count: int = 0
    failed_count: int = 0
    bytes_freed: int = 0
    candidates_count: int = 0  # Number of directories that could be pruned


_LOG_CLEANUP_TRACKED: set[str] = set()


def _normalize_dir(path: str) -> str:
    return os.path.normpath(os.path.abspath(path))


def should_run_log_cleanup(log_dir: str) -> bool:
    """Return True when log cleanup checks have not yet run for the directory."""

    return _normalize_dir(log_dir) not in _LOG_CLEANUP_TRACKED


def mark_log_cleanup_checked(log_dir: str) -> None:
    """Mark that cleanup checks have already executed for the directory."""

    _LOG_CLEANUP_TRACKED.add(_normalize_dir(log_dir))


class LogDirectoryManager:
    """Manages automatic cleanup of execution log directories."""

    def __init__(self, logger: TaskLogger):
        self._logger = logger

    @staticmethod
    def describe_prune_behavior(run_config: RunConfig) -> str:
        """Generate description of what --prune-logs will do based on current config.

        Args:
            run_config: Configuration containing pruning settings.

        Returns:
            Human-readable description of pruning behavior.
        """
        criteria = []
        if run_config.max_log_dirs > 0:
            criteria.append(f"keeping {run_config.max_log_dirs} most recent directories")
        if run_config.max_log_age_days > 0:
            criteria.append(f"deleting directories older than {run_config.max_log_age_days} days")

        if not criteria:
            return "--prune-logs (no limits configured)"

        return f"--prune-logs ({', '.join(criteria)})"

    def check_and_suggest_cleanup(self, run_config: RunConfig) -> PruneStats:
        """Check if cleanup is needed and log a suggestion if so.

        This method does NOT delete anything. It only checks the current state
        and logs a message suggesting the user run --prune-logs if cleanup is needed.

        Args:
            run_config: Configuration containing pruning settings.

        Returns:
            Statistics about potential cleanup (nothing deleted).
        """
        if run_config.max_log_dirs <= 0 and run_config.max_log_age_days <= 0:
            return PruneStats()

        log_dir = self._logger.log_dir
        if not os.path.exists(log_dir):
            return PruneStats()

        stats = PruneStats()
        current_exec_dir = os.path.normpath(self._logger.execution_dir)

        # Get all execution directories
        dirs_with_time = list(self._list_execution_dirs(log_dir, current_exec_dir))
        stats.total_dirs = len(dirs_with_time)

        if stats.total_dirs == 0:
            return stats

        # Determine which directories could be pruned
        dirs_to_prune = self._select_dirs_to_prune(dirs_with_time, run_config)
        stats.candidates_count = len(dirs_to_prune)

        # Count protected directories
        for dir_path in dirs_to_prune:
            if self._is_protected(dir_path):
                stats.protected_count += 1

        # If there are directories that could be cleaned, suggest it
        prunable_count = stats.candidates_count - stats.protected_count
        if prunable_count > 0:
            prune_desc = self.describe_prune_behavior(run_config)
            self._logger.log(
                "log_cleanup_suggested",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                message=(
                    f"Log directory cleanup recommended: {prunable_count} directories exceed configured limits."
                    f"\n  Run with {prune_desc} to clean up."
                ),
                show_fields_with_message=True,
                total_dirs=stats.total_dirs,
                prunable=prunable_count,
                protected=stats.protected_count,
                max_dirs=run_config.max_log_dirs,
                max_age_days=run_config.max_log_age_days,
            )

        return stats

    def prune_old_directories(self, run_config: RunConfig) -> PruneStats:
        """Prune old execution directories based on configuration.

        Args:
            run_config: Configuration containing pruning settings.

        Returns:
            Statistics about the pruning operation.
        """
        if not run_config.auto_prune:
            self._logger.log(
                "log_prune_skipped",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                reason="disabled",
                message="Automatic log directory pruning disabled (auto_prune=false)",
            )
            return PruneStats()

        if run_config.max_log_dirs <= 0 and run_config.max_log_age_days <= 0:
            self._logger.log(
                "log_prune_skipped",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                reason="no_limits",
                message="No log pruning limits configured",
            )
            return PruneStats()

        log_dir = self._logger.log_dir
        if not os.path.exists(log_dir):
            return PruneStats()

        stats = PruneStats()
        current_exec_dir = os.path.normpath(self._logger.execution_dir)

        # Get all execution directories sorted by creation time (newest first)
        dirs_with_time = list(self._list_execution_dirs(log_dir, current_exec_dir))
        stats.total_dirs = len(dirs_with_time)

        if stats.total_dirs == 0:
            return stats

        # Determine which directories to prune
        dirs_to_prune = self._select_dirs_to_prune(dirs_with_time, run_config)

        for dir_path in dirs_to_prune:
            if self._is_protected(dir_path):
                stats.protected_count += 1
                self._logger.log(
                    "log_prune_protected",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    dir_path=dir_path,
                    reason="active_processes",
                )
                continue

            dir_size = self._get_dir_size(dir_path)
            if self._safe_delete_directory(dir_path):
                stats.pruned_count += 1
                stats.bytes_freed += dir_size
            else:
                stats.failed_count += 1

        self._emit_prune_summary(stats, run_config)
        return stats

    def _list_execution_dirs(
        self, log_dir: str, current_exec_dir: str
    ) -> Iterator[tuple[str, float]]:
        """Yield (dir_path, modification_time) for execution directories.

        Uses modification time (st_mtime) for consistent cross-platform behavior
        and testability (os.utime can set mtime but not ctime on most systems).

        Excludes:
        - The current execution directory
        - Non-directory entries
        - Special files (latest-run pointer, etc.)
        """
        try:
            entries = os.listdir(log_dir)
        except OSError:
            return

        for entry in entries:
            if entry in ("latest-run", "latest-run.tmp"):
                continue

            dir_path = os.path.join(log_dir, entry)
            if not os.path.isdir(dir_path):
                continue

            if os.path.normpath(dir_path) == current_exec_dir:
                continue

            try:
                mtime = os.path.getmtime(dir_path)
                yield dir_path, mtime
            except OSError:
                continue

    def _select_dirs_to_prune(
        self,
        dirs_with_time: list[tuple[str, float]],
        run_config: RunConfig,
    ) -> list[str]:
        """Select directories to prune based on count and age limits."""
        # Sort by modification time (newest first)
        sorted_dirs = sorted(dirs_with_time, key=lambda x: x[1], reverse=True)

        dirs_to_prune: set[str] = set()

        # Apply count-based pruning
        if run_config.max_log_dirs > 0 and len(sorted_dirs) > run_config.max_log_dirs:
            excess_dirs = sorted_dirs[run_config.max_log_dirs :]
            dirs_to_prune.update(d[0] for d in excess_dirs)

        # Apply age-based pruning
        if run_config.max_log_age_days > 0:
            cutoff_time = (datetime.now() - timedelta(days=run_config.max_log_age_days)).timestamp()
            for dir_path, ctime in sorted_dirs:
                if ctime < cutoff_time:
                    dirs_to_prune.add(dir_path)

        return list(dirs_to_prune)

    def _is_protected(self, dir_path: str) -> bool:
        """Check if directory should be protected from pruning."""
        return False

    def _get_dir_size(self, dir_path: str) -> int:
        """Calculate total size of directory in bytes."""
        total = 0
        try:
            for dirpath, _dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total += os.path.getsize(filepath)
                    except OSError:
                        pass
        except OSError:
            pass
        return total

    def _safe_delete_directory(self, dir_path: str) -> bool:
        """Safely delete a directory and its contents.

        Returns True if deletion succeeded, False otherwise.
        """
        try:
            shutil.rmtree(dir_path)
            self._logger.log(
                "log_dir_pruned",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                dir_path=dir_path,
            )
            return True
        except OSError as exc:
            self._logger.log(
                "log_prune_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                dir_path=dir_path,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            return False

    def _emit_prune_summary(self, stats: PruneStats, run_config: RunConfig) -> None:
        """Log summary of pruning operation."""
        if stats.pruned_count > 0 or stats.protected_count > 0:
            bytes_mb = stats.bytes_freed / (1024 * 1024)
            self._logger.log(
                "log_prune_summary",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                message=f"Log cleanup: {stats.pruned_count} directories removed, "
                f"{bytes_mb:.1f} MB freed",
                show_fields_with_message=True,
                pruned=stats.pruned_count,
                protected=stats.protected_count,
                failed=stats.failed_count,
                total=stats.total_dirs,
                bytes_freed=stats.bytes_freed,
                max_dirs=run_config.max_log_dirs,
                max_age_days=run_config.max_log_age_days,
            )


__all__ = [
    "LogDirectoryManager",
    "PruneStats",
    "mark_log_cleanup_checked",
    "should_run_log_cleanup",
]
