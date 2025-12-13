"""CLI-aware configuration helpers."""

from __future__ import annotations

import os
import sys
from typing import Any

from hil_testbench.cli.constants import DEFAULT_CONFIG_FILE
from hil_testbench.config.config_loader import load_project_config


def load_config_from_args(args) -> tuple[dict, Any, dict[str, Any]]:
    """Load YAML + run config based on parsed CLI arguments."""

    config_path = args.config or DEFAULT_CONFIG_FILE
    abs_path = os.path.abspath(config_path)

    if args.config and not os.path.exists(config_path):
        print(  # hil: allow-print
            f"Warning: configuration file '{config_path}' not found. Using built-in defaults.",
            file=sys.stderr,
        )
    yaml_data, run_config, yaml_tasks = load_project_config(config_path, cli_args=args)

    updates = {
        "loaded_config_path": abs_path if os.path.exists(config_path) else None,
    }
    if args.daemon:
        updates["daemon_mode"] = True
    return yaml_data, run_config.with_updates(**updates), yaml_tasks
