from __future__ import annotations

import argparse
import os
import sys

from hil_testbench.cli.commands import daemon_detach
from hil_testbench.cli.config_loader import load_config_from_args
from hil_testbench.cli.config_template import generate_config
from hil_testbench.cli.constants import DEFAULT_CONFIG_FILE
from hil_testbench.cli.describe import describe_options as emit_cli_description
from hil_testbench.cli.executor import execute_tasks
from hil_testbench.cli.monitor import handle_monitor
from hil_testbench.cli.parser import build_parser, emit_logging_summary, resolve_logging
from hil_testbench.cli.prune_logs import handle_prune_logs
from hil_testbench.cli.shutdown import handle_shutdown
from hil_testbench.cli.task_listing import print_task_list
from hil_testbench.cli.task_loader import discover_tasks
from hil_testbench.cli.task_utils import (
    build_invalid_task_messages,
    has_requested_tasks,
    select_tasks,
)
from hil_testbench.cli.utils import emit_cli_message
from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.logging.task_logger import LogLevel, LogScope
from hil_testbench.tools.yaml_options_report import build_report
from hil_testbench.utils.console_encoding import configure_console_encoding

configure_console_encoding()


def _describe(parser: argparse.ArgumentParser, fmt: str) -> None:
    emit_cli_description(parser, fmt, build_report=build_report)
    sys.exit(0)


def _run_cli(
    parser: argparse.ArgumentParser, args: argparse.Namespace, task_names: list[str]
) -> None:
    # --------------------------- Early CLI handlers ---------------------------
    handle_monitor(args)
    handle_shutdown(args)

    if args.describe:
        _describe(parser, args.describe_format)

    if args.list:
        print_task_list(task_names, args.task_dir)
        sys.exit(0)

    if args.generate_config:
        output_file = (
            args.generate_config if isinstance(args.generate_config, str) else DEFAULT_CONFIG_FILE
        )
        generate_config(
            task_names,
            args.task_dir,
            output_file,
            force=args.generate_config_force,
            report_builder=build_report,
        )
        sys.exit(0)

    # prune-logs runs without tasks
    if args.prune_logs is not None:
        _, run_config, _ = load_config_from_args(args)
        run_config = resolve_logging(args, run_config)
        handle_prune_logs(args, run_config)
        # prune_logs exits internally

    # require tasks
    if not has_requested_tasks(args.tasks):
        parser.print_help()
        sys.exit(1)

    # --------------------------- Task Selection ---------------------------
    selection = select_tasks(args.tasks, task_names)

    if selection.invalid:
        error_line, available_line = build_invalid_task_messages(selection.invalid, task_names)
        raise ConfigurationError(
            f"{error_line}\n{available_line}",
            context={
                "invalid_tasks": tuple(selection.invalid),
                "task_dir": args.task_dir,
            },
        )

    unique_tasks = selection.unique

    if args.daemon:
        daemon_detach()

    yaml_data, run_config, yaml_tasks = load_config_from_args(args)
    run_config = resolve_logging(args, run_config)

    # update with flags that may not exist in all configs
    run_config = run_config.with_updates(
        cleanup_required=bool(getattr(args, "cleanup_required", False)),
    )

    emit_logging_summary(run_config)

    exit_code = execute_tasks(unique_tasks, args, yaml_data, run_config, yaml_tasks)
    sys.exit(exit_code)


def main() -> None:
    """
    Insert task-dir into sys.path BEFORE discover_tasks()
    This is required so tests can import dynamic task modules correctly.
    """

    # -------------------- First parse to get task_dir early --------------------
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--task-dir", default="tasks")
    pre_args, _ = pre_parser.parse_known_args()

    # -------------------- inject task-dir BEFORE discovery ----------------
    task_dir_path = os.path.abspath(pre_args.task_dir)
    if task_dir_path not in sys.path:
        sys.path.insert(0, task_dir_path)

    task_names = discover_tasks(pre_args.task_dir)

    # Second parse with full task knowledge
    parser = build_parser(task_names, pre_args.task_dir)
    args = parser.parse_args()

    try:
        _run_cli(parser, args, task_names)
    except ConfigurationError as exc:
        emit_cli_message(
            event="cli_configuration_error",
            message=str(exc),
            level=LogLevel.ERROR,
            scope=LogScope.FRAMEWORK,
            stderr=False,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
