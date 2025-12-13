from __future__ import annotations

import importlib
import os
import pathlib
import sys
from collections.abc import Callable
from typing import Any

import yaml

from .constants import DEFAULT_CONFIG_FILE
from .task_loader import resolve_task_class
from .utils import safe_symbol

ReportBuilder = Callable[[], dict[str, Any]]


def generate_config(
    task_names: list[str],
    task_dir: str = "tasks",
    output_path: str = DEFAULT_CONFIG_FILE,
    *,
    force: bool = False,
    report_builder: ReportBuilder | None = None,
) -> None:
    output_path = output_path or DEFAULT_CONFIG_FILE
    if os.path.exists(output_path) and not force:
        print(  # hil: allow-print
            f"Warning: {output_path} already exists. Aborting generation."
        )
        print(  # hil: allow-print
            "Delete or rename the existing file, or re-run with --generate-config-force."
        )
        sys.exit(1)

    report = report_builder() if report_builder else None

    config, task_metadata = build_config_template(task_names, task_dir, report)
    resolved_path = write_config_template(config, task_metadata, output_path)
    print_config_generation_summary(resolved_path)


def build_config_template(
    task_names: list[str],
    task_dir: str,
    report: dict | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    task_module_prefix = _task_module_prefix(task_dir)
    config = _base_config()
    task_metadata: dict[str, Any] = {}

    for tname in sorted(task_names):
        task_parts = _build_task_entry(tname, task_module_prefix, report)
        if task_parts is None:
            continue
        task_config, metadata = task_parts
        config["tasks"][tname] = task_config
        task_metadata[tname] = metadata

    return config, task_metadata


def _task_module_prefix(task_dir: str) -> str:
    return task_dir.replace("/", ".").replace("\\", ".")


def _base_config() -> dict[str, Any]:
    return {
        "defaults": {
            "duration": None,  # None = indefinite (runs until CTRL+C or shutdown signal)
            "interval": 5,
            "log_level": "INFO",
            "log_level_file": "DEBUG",
        },
        "hosts": {
            "example_host": {
                "host": "<hostname or IP4 address>",
                "user": "<username>",
                "port": 22,
                "password": "<password_or_leave_empty_for_key>",
            },
            "localhost": {"host": "localhost", "user": "<username>", "port": 22},
        },
        "tasks": {},
    }


def _build_task_entry(
    task_name: str,
    module_prefix: str,
    report: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    module_path = f"{module_prefix}.{task_name}"
    try:
        task_module = importlib.import_module(module_path)
        task_cls = resolve_task_class(task_module)
        task_instance = task_cls()
    except (AttributeError, ImportError):
        return None

    task_config: dict[str, Any] = {"module": task_name}
    if report:
        _populate_report_keys(task_config, task_name, report)

    has_schema = _has_schema(task_instance)
    if has_schema:
        task_config["display"] = _display_template()

    metadata = {
        "description": _task_description(task_module),
        "has_schema": has_schema,
    }
    return task_config, metadata


def _task_description(task_module: Any) -> str | None:
    doc = (task_module.__doc__ or "").strip().splitlines()
    return doc[0] if doc else None


def _has_schema(task_instance: Any) -> bool:
    schema_attr = getattr(task_instance, "schema", None)
    return callable(schema_attr)


def _populate_report_keys(
    task_config: dict[str, Any],
    task_name: str,
    report: dict[str, Any],
) -> None:
    task_info = report.get("tasks", {}).get(task_name, {})
    task_params = task_info.get("task_params_keys", [])
    nested_keys = task_info.get("nested_keys", [])
    for param in task_params:
        if param == "hosts":
            task_config["hosts"] = ["<host_name>"]
        elif param == "links":
            if links_template := _build_links_example(nested_keys):
                task_config["links"] = links_template
        else:
            task_config[param] = f"<{param}>"


def _build_links_example(nested_keys: list[str]) -> list[dict[str, str]] | None:
    example_link: dict[str, str] = {}
    for nested in sorted(nested_keys):
        if nested.startswith("link."):
            key = nested.split(".", 1)[1]
            example_link[key] = f"<{key}>"
    return [example_link] if example_link else None


def _display_template() -> dict[str, Any]:
    return {
        "parameters": {
            "<parameter_name>": {
                "thresholds": {
                    "good": {
                        "value": "<value>",
                        "operator": "gt",
                        "color": "green",
                    },
                    "warn": {
                        "value": ["<min>", "<max>"],
                        "operator": "range",
                        "color": "yellow",
                    },
                    "bad": {
                        "value": "<value>",
                        "operator": "lt",
                        "color": "red",
                    },
                }
            }
        }
    }


def write_config_template(
    config: dict[str, Any],
    task_metadata: dict[str, Any],
    output_path: str,
) -> pathlib.Path:
    output_file = pathlib.Path(output_path)
    with output_file.open("w", encoding="utf-8") as handle:
        handle.write("# Generated tasks.yaml configuration template\n")
        handle.write("#\n")
        handle.write("# ⚠️  WARNING: This is a TEMPLATE with placeholder values.\n")
        handle.write("# You MUST edit this file and replace ALL <placeholder> values before use!\n")
        handle.write("#\n")
        handle.write("# Each task shows:\n")
        handle.write("#  • Required YAML parameters (from static code analysis)\n")
        handle.write("#  • Display parameters structure (for monitoring thresholds)\n")
        handle.write("#\n")
        handle.write("# To use this config:\n")
        handle.write("#  1. Replace ALL <placeholder> values with real data\n")
        handle.write("#  2. Fill in host connection details (user, password/key)\n")
        handle.write("#  3. Remove unused tasks\n")
        handle.write("#  4. Configure display thresholds for monitoring\n\n")

        yaml.dump(
            {"defaults": config["defaults"], "hosts": config["hosts"]},
            handle,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )

        handle.write("\ntasks:\n")
        for tname in sorted(config["tasks"].keys()):
            task_config = config["tasks"][tname]
            metadata = task_metadata.get(tname, {})
            handle.write(f"\n  # Task: {tname}\n")
            if metadata.get("description"):
                handle.write(f"  # {metadata['description']}\n")
            if metadata.get("has_schema"):
                handle.write(
                    "  # Note: Configure display.parameters with actual parameter names from task.schema()\n"
                )

            task_yaml = yaml.dump(
                {tname: task_config},
                default_flow_style=False,
                sort_keys=False,
                width=116,
            )
            for line in task_yaml.splitlines():
                if line and not line.startswith("#"):
                    handle.write(f"  {line}\n")

    return output_file.resolve()


def print_config_generation_summary(output_path: str | pathlib.Path) -> None:
    abs_path = pathlib.Path(output_path).resolve()
    print(  # hil: allow-print
        f"{safe_symbol('✅')} Generated configuration: {abs_path}"
    )
    print(  # hil: allow-print
        "\n⚠️  This is a TEMPLATE - all placeholders must be replaced before use!"
    )
    print("\nTemplate includes:")  # hil: allow-print
    print("  • Task YAML parameters (from static code analysis)")  # hil: allow-print
    print("  • Task CLI options (from argument parsers)")  # hil: allow-print
    print(  # hil: allow-print
        "  • Display parameter structure (for threshold configuration)"
    )
    print("\nNext actions:")  # hil: allow-print
    print(  # hil: allow-print
        f"  1. Edit {output_path} - replace ALL <placeholder> values with real data"
    )
    print(  # hil: allow-print
        "  2. Fill in host credentials and task-specific configuration"
    )
    print(  # hil: allow-print
        f"  3. Run: python -m run_tasks --config {output_path} <task_name>"
    )
