from __future__ import annotations

import argparse
from typing import Any

from hil_testbench.config.run_config import RunConfig

from .constants import DEFAULT_CONFIG_FILE

LOG_LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def build_parser(
    task_names: list[str],
    task_dir: str = "tasks",
) -> argparse.ArgumentParser:
    """Construct the top-level CLI parser with positional task argument."""
    parser = argparse.ArgumentParser(
        description="TaskRunner CLI - Unified Task Execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run_tasks.py task1 task2 --duration 60 --interval 5\n"
            "  python run_tasks.py task1 --log-level DEBUG --file-log-level INFO\n"
        ),
    )
    _add_core_arguments(parser)
    _add_cleanup_arguments(parser)
    _add_health_arguments(parser)
    _add_logging_arguments(parser)
    _add_utility_arguments(parser, task_dir)
    _add_task_arguments(parser)
    parser.set_defaults(_available_tasks=tuple(task_names))
    return parser


def resolve_logging(args: argparse.Namespace, run_config: RunConfig) -> RunConfig:
    """Apply CLI precedence rules to run_config logging fields."""

    console_level = _resolve_console_level(args, run_config.log_level.upper())
    file_level = _resolve_file_level(args, run_config.log_level_file.upper())

    updated = run_config.with_updates(
        log_level=console_level,
        log_level_file=file_level,
    )
    return _apply_logging_flags(args, updated)


def emit_logging_summary(run_config: Any) -> None:
    print(  # hil: allow-print
        f"Logging: console={run_config.log_level} file={run_config.log_level_file} color={'off' if run_config.no_color else 'on'} json_console={'on' if run_config.json_console else 'off'} quiet_errors_only={'on' if run_config.quiet_errors_only else 'off'} dir={run_config.log_dir}"
    )

    if run_config.loaded_config_path:
        print(f"Config: {run_config.loaded_config_path}")  # hil: allow-print
    else:
        print("Config: [built-in defaults]")  # hil: allow-print


def _add_core_arguments(parser: argparse.ArgumentParser) -> None:
    core = parser.add_argument_group("core")
    core.add_argument("--duration", type=str, help="Test duration (seconds)")
    core.add_argument("--interval", type=str, help="Interval between samples (seconds)")
    core.add_argument("--config", "-c", help="YAML config file for advanced options")
    core.add_argument(
        "--shell-wrapper",
        choices=["auto", "on", "off"],
        help="Control shell wrapper usage for commands (auto=default heuristic)",
    )
    core.add_argument(
        "--force-cleanup",
        action="store_true",
        help="Force forced cleanup after tasks conclude",
    )
    core.add_argument(
        "--pre-cleanup",
        action="store_true",
        help="Run forced cleanup before executing tasks",
    )
    core.add_argument(
        "--force-cleanup-timeout",
        type=float,
        help="Trigger forced cleanup automatically if shutdown exceeds this timeout (seconds)",
    )
    core.add_argument(
        "--force-cleanup-mode",
        choices=["graceful", "strict", "aggressive"],
        help="Select forced cleanup aggressiveness",
    )
    core.add_argument(
        "--max-data-size",
        type=int,
        default=None,
        help="Maximum data size per-task (MB)",
    )


def _add_cleanup_arguments(parser: argparse.ArgumentParser) -> None:
    cleanup = parser.add_argument_group("cleanup")
    cleanup.add_argument(
        "--state-dir",
        metavar="DIR",
        help="Override persistent process state directory",
    )
    cleanup.add_argument(
        "--cleanup-window",
        type=int,
        metavar="SECONDS",
        help="Cleanup window in seconds (default: 86400)",
    )
    toggle = cleanup.add_mutually_exclusive_group()
    toggle.add_argument(
        "--enable-cleanup",
        action="store_true",
        help="Enable orphan cleanup before tasks run",
    )
    toggle.add_argument(
        "--disable-cleanup",
        action="store_true",
        help="Force cleanup to remain disabled",
    )


def _add_health_arguments(parser: argparse.ArgumentParser) -> None:
    health = parser.add_argument_group("health")
    health.add_argument(
        "--disable-health", action="store_true", help="Disable host health monitoring"
    )
    health.add_argument(
        "--health-interval", type=int, default=600, help="Health monitor interval (sec)"
    )


def _add_logging_arguments(parser: argparse.ArgumentParser) -> None:
    logging_grp = parser.add_argument_group("logging")
    logging_grp.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase console verbosity (stackable)",
    )
    logging_grp.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="Decrease console verbosity (stackable)",
    )
    logging_grp.add_argument(
        "--log-level",
        choices=list(LOG_LEVELS),
        help="Explicit console log level",
    )
    logging_grp.add_argument(
        "--file-log-level",
        choices=list(LOG_LEVELS),
        help="Explicit file log level",
    )
    logging_grp.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Shortcut for DEBUG console (and file if not set)",
    )
    logging_grp.add_argument(
        "--quiet-errors-only",
        action="store_true",
        help="Console shows only ERROR/CRITICAL events",
    )
    logging_grp.add_argument(
        "--no-color", action="store_true", help="Disable colored console output"
    )
    logging_grp.add_argument(
        "--json-console",
        action="store_true",
        help="Emit structured JSON objects to console",
    )
    logging_grp.add_argument("--log-dir", help="Override root log directory (default: logs)")
    logging_grp.add_argument(
        "--max-log-size-main", type=int, default=10, help="Main log rotation size MB"
    )
    logging_grp.add_argument(
        "--max-log-size-task", type=int, default=5, help="Task log rotation size MB"
    )
    logging_grp.add_argument(
        "--max-log-file-count-main",
        type=int,
        default=10,
        help="Max rotated main log files",
    )
    logging_grp.add_argument(
        "--max-log-file-count-task",
        type=int,
        default=10,
        help="Max rotated task log files",
    )
    logging_grp.add_argument(
        "--max-log-dirs",
        type=int,
        help="Max execution directories to keep (default: 50, 0=unlimited)",
    )
    logging_grp.add_argument(
        "--max-log-age-days",
        type=int,
        help="Max age in days for log directories (default: 30, 0=unlimited)",
    )
    logging_grp.add_argument(
        "--auto-prune",
        action="store_true",
        help="Enable automatic log directory cleanup on startup",
    )


def _add_utility_arguments(parser: argparse.ArgumentParser, task_dir: str) -> None:
    util = parser.add_argument_group("utility")
    util.add_argument("--daemon", action="store_true", help="Run in background (daemon mode)")
    util.add_argument(
        "--monitor",
        "-m",
        action="store_true",
        help="Launch status monitor for latest session",
    )
    util.add_argument(
        "--shutdown",
        "-s",
        metavar="SESSION_DIR",
        help="Shutdown a daemon session by log directory path",
    )
    util.add_argument(
        "--prune-logs",
        nargs="?",
        const="auto",
        metavar="MODE",
        help="Prune old log directories (auto|dry-run|force)",
    )
    util.add_argument("--describe", action="store_true", help="Describe CLI + YAML options")
    util.add_argument(
        "--describe-format",
        choices=["text", "json"],
        default="text",
        help="Describe output format",
    )
    util.add_argument("--list", action="store_true", help="List available tasks")
    util.add_argument(
        "--generate-config",
        nargs="?",
        const=DEFAULT_CONFIG_FILE,
        metavar="FILENAME",
        help=f"Generate sample config YAML (default: {DEFAULT_CONFIG_FILE})",
    )
    util.add_argument(
        "--generate-config-force",
        action="store_true",
        help="Allow overwriting files when generating config templates",
    )
    util.add_argument(
        "--task-dir",
        default=task_dir,
        help=f"Directory to discover tasks from (default: {task_dir})",
    )
    util.add_argument(
        "--cleanup-required",
        action="store_true",
        help="Fail if pre-run cleanup cannot clear leftover processes",
    )


def _add_task_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "tasks",
        nargs="*",
        metavar="TASK",
        help="One or more task names to execute (e.g., task1 task2 task3)",
    )


def _resolve_console_level(args: argparse.Namespace, base_level: str) -> str:
    if args.log_level:
        return args.log_level.upper()
    level = _apply_stackable_offsets(base_level, args.verbose, args.quiet)
    if args.debug:
        level = "DEBUG"
    if args.quiet_errors_only:
        level = "ERROR"
    return level


def _resolve_file_level(args: argparse.Namespace, base_level: str) -> str:
    if args.file_log_level:
        return args.file_log_level.upper()
    if args.debug:
        return "DEBUG"
    return base_level


def _apply_logging_flags(args: argparse.Namespace, run_config: RunConfig) -> RunConfig:
    updates: dict[str, Any] = {
        "no_color": args.no_color or run_config.no_color,
        "json_console": args.json_console or run_config.json_console,
        "quiet_errors_only": args.quiet_errors_only or run_config.quiet_errors_only,
    }
    if args.log_dir:
        updates["log_dir"] = args.log_dir
    if args.max_log_dirs is not None:
        updates["max_log_dirs"] = args.max_log_dirs
    if args.max_log_age_days is not None:
        updates["max_log_age_days"] = args.max_log_age_days
    if args.auto_prune:
        updates["auto_prune"] = True
    return run_config.with_updates(**updates)


def _apply_stackable_offsets(base_level: str, verbose: int, quiet: int) -> str:
    idx = LOG_LEVELS.index(base_level) if base_level in LOG_LEVELS else 1
    idx = max(0, min(idx - verbose + quiet, len(LOG_LEVELS) - 1))
    return LOG_LEVELS[idx]
