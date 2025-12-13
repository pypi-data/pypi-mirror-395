"""Centralized YAML loader for the TaskRunner project.

Responsibilities:
- Load YAML from a path (default `tasks.yaml`)
- Return RunConfig with YAML + CLI args merged
- Avoid side effects like modifying global state

Design notes:
- Keeps file I/O separate from dataclass constructors for clean architecture
- Handles both YAML defaults and CLI overrides in one place
- Returns ready-to-use RunConfig and task definitions
"""

from __future__ import annotations

import os
from typing import Any

import yaml

from hil_testbench.config.run_config import RunConfig


def load_project_config(
    yaml_path: str = "tasks.yaml",
    cli_args: object | None = None,
) -> tuple[dict[str, Any], RunConfig, dict[str, Any]]:
    """Load project YAML and merge with CLI args to create RunConfig.

    Args:
        yaml_path: Path to YAML config file
        cli_args: Argparse namespace with CLI overrides (optional)

    Returns:
        yaml_data: the raw YAML dictionary (or {})
        run_config: RunConfig with YAML + CLI args merged
        tasks_map: yaml_data.get("tasks", {})
    """
    yaml_data: dict[str, Any] = {}
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            # Surface malformed YAML instead of silently continuing so callers/tests fail fast.
            raise ValueError(f"Error parsing YAML config file '{yaml_path}': {e}") from e
        run_config = RunConfig.from_yaml(yaml_data)
    else:
        run_config = RunConfig(hosts={"localhost": {"host": "localhost"}})

    if cli_args is not None:
        run_config = _apply_cli_overrides(run_config, cli_args)

    tasks_map = yaml_data.get("tasks", {})
    return yaml_data, run_config, tasks_map


def _apply_cli_overrides(run_config: RunConfig, cli_args: object) -> RunConfig:
    def _attr(name: str, default: Any) -> Any:
        return getattr(cli_args, name, default)

    disable_health = getattr(cli_args, "disable_health", None)
    enable_health = (
        run_config.enable_runner_health if disable_health is None else not bool(disable_health)
    )

    force_timeout = getattr(cli_args, "force_cleanup_timeout", None)
    cleanup_mode = getattr(cli_args, "force_cleanup_mode", None)
    cleanup_window = getattr(cli_args, "cleanup_window", None)
    state_dir = getattr(cli_args, "state_dir", None)

    overrides = {
        "max_log_size_main_mb": _attr("max_log_size_main", run_config.max_log_size_main_mb),
        "max_log_file_count_main": _attr(
            "max_log_file_count_main", run_config.max_log_file_count_main
        ),
        "enable_runner_health": enable_health,
        "runner_health_interval": _attr("health_interval", run_config.runner_health_interval),
        "shell_wrapper_mode": getattr(cli_args, "shell_wrapper", None)
        or run_config.shell_wrapper_mode,
        "force_cleanup": _attr("force_cleanup", run_config.force_cleanup),
        "pre_cleanup": _attr("pre_cleanup", run_config.pre_cleanup),
        "force_cleanup_timeout": run_config.force_cleanup_timeout
        if force_timeout is None
        else force_timeout,
        "force_cleanup_mode": cleanup_mode or run_config.force_cleanup_mode,
    }

    if state_dir:
        overrides["state_dir"] = os.path.abspath(os.path.expanduser(state_dir))
    if cleanup_window is not None:
        overrides["cleanup_window_seconds"] = max(int(cleanup_window), 0)
    if getattr(cli_args, "enable_cleanup", False):
        overrides["no_cleanup"] = False
    if getattr(cli_args, "disable_cleanup", False):
        overrides["no_cleanup"] = True

    return run_config.with_updates(**overrides)
