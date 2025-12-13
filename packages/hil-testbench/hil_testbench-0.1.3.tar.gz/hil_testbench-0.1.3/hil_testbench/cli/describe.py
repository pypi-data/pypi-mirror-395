"""Helpers for describing CLI/YAML surfaces."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from typing import Any


def describe_options(
    parser: argparse.ArgumentParser,
    fmt: str,
    *,
    build_report: Callable[[], dict[str, Any]],
) -> None:
    """Emit a description of CLI + YAML override surface."""

    report = build_report()
    data = _build_description(parser, report)
    if fmt == "json":
        print(json.dumps(_clean(data), indent=2))  # hil: allow-print
        return
    _emit_pretty(data)


def _build_description(
    parser: argparse.ArgumentParser,
    report: dict[str, Any],
) -> dict[str, Any]:
    program_block = {
        "cli_options": _collect_actions(parser),
        "yaml_keys": {
            "root_sections": list(report.get("root_sections", [])),
            "defaults": list(report.get("task_defaults_keys", [])),
            "run_config_keys": list(report.get("run_config_yaml_keys", [])),
            "reserved_task_keys": list(report.get("task_reserved_keys", [])),
            "cli_override_keys": list(report.get("cli_override_keys", [])),
        },
    }
    tasks_block = {
        name: {
            "cli_options": [],
            "yaml_keys": report.get("tasks", {}).get(name, {}),
        }
        for name in report.get("tasks", {})
    }
    return {"program": program_block, "tasks": tasks_block}


def _collect_actions(parser: argparse.ArgumentParser) -> list[dict[str, Any]]:
    return [
        _serialize_action(action)
        for action in parser._actions  # pylint: disable=protected-access
        if _is_user_action(action)
    ]


def _is_user_action(action: argparse.Action) -> bool:
    return action.dest not in ("help", argparse.SUPPRESS)


def _serialize_action(action: argparse.Action) -> dict[str, Any]:
    flags = list(action.option_strings) if action.option_strings else [action.dest]
    default_val = None if action.default is argparse.SUPPRESS else action.default
    choices_val = _normalize_choices(action.choices)
    type_name = getattr(action.type, "__name__", None) if action.type else None
    return {
        "flags": flags,
        "dest": action.dest,
        "help": action.help,
        "default": default_val,
        "type": type_name,
        "choices": choices_val,
    }


def _normalize_choices(choices: Any) -> Any:
    if isinstance(choices, (list | tuple | set)):
        return list(choices)
    return choices


def _emit_pretty(data: dict[str, Any]) -> None:
    _emit_program_cli(data["program"]["cli_options"])
    _emit_yaml_keys(data["program"]["yaml_keys"])
    _emit_task_sections(data["tasks"])


def _emit_program_cli(opts: list[dict[str, Any]]) -> None:
    print("Program CLI options:")  # hil: allow-print
    for opt in opts:
        flags = ", ".join(opt["flags"])
        default = (
            f" (default: {opt['default']})"
            if opt["default"] not in (None, argparse.SUPPRESS)
            else ""
        )
        print(f"  {flags}{default} - {opt['help'] or ''}")  # hil: allow-print


def _emit_yaml_keys(block: dict[str, Any]) -> None:
    print("\nYAML keys (program-level):")  # hil: allow-print
    _emit_key_line("defaults", block["defaults"])
    _emit_key_line("run_config", block["run_config_keys"])
    _emit_key_line("reserved_task_keys", block["reserved_task_keys"])
    _emit_key_line("cli_override_keys", block["cli_override_keys"])


def _emit_key_line(label: str, values: list[str]) -> None:
    print(f"  {label}:", ", ".join(values))  # hil: allow-print


def _emit_task_sections(tasks: dict[str, Any]) -> None:
    for tname, tdata in tasks.items():
        print(f"\nTask: {tname}")  # hil: allow-print
        _emit_cli_options(tdata["cli_options"])
        _emit_task_yaml_keys(tdata["yaml_keys"])


def _emit_cli_options(cli_opts: list[dict[str, Any]]) -> None:
    if not cli_opts:
        return
    print("  CLI options:")  # hil: allow-print
    for opt in cli_opts:
        flags = ", ".join(opt["flags"])
        default = _format_default(opt["default"])
        print(f"    {flags}{default} - {opt['help'] or ''}")  # hil: allow-print


def _emit_task_yaml_keys(keys: dict[str, Any]) -> None:
    _emit_optional_key_line("YAML task_params keys", keys.get("task_params_keys"))
    _emit_optional_key_line("YAML host_param keys", keys.get("host_param_keys"))
    _emit_optional_key_line("YAML nested keys", keys.get("nested_keys"))


def _emit_optional_key_line(label: str, values: list[str] | None) -> None:
    if values:
        print(f"  {label}:", ", ".join(values))  # hil: allow-print


def _format_default(value: Any) -> str:
    return "" if value in (None, argparse.SUPPRESS) else f" (default: {value})"


def _clean(obj: Any):
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list | tuple | set)):
        return [_clean(v) for v in obj]
    return obj if isinstance(obj, (str | int | float)) or obj is None else str(obj)
