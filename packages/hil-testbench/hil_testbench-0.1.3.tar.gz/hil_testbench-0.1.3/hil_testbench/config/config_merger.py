"""Configuration merging utilities for TaskRunner.

Centralizes the logic for merging CLI args, YAML defaults,
and program defaults into a single, testable function with clear precedence rules.

Precedence (most specific to least):
1. Top-level CLI args (e.g., --duration, --interval)
2. Task-level YAML defaults (tasks.<task_name>.*)
3. Top-level YAML defaults (defaults.*)
4. Program defaults (dataclass field defaults)

"""

from __future__ import annotations

from typing import Any


def merge_config_sources(
    args: object,
    top_defaults: dict[str, Any],
    task_defaults: dict[str, Any],
    program_defaults: dict[str, Any],
) -> dict[str, Any]:
    """Merge configuration sources according to precedence rules.

    Args:
        args: Top-level CLI argparse namespace (program-level flags)
        top_defaults: Top-level YAML defaults (yaml_data["defaults"])
        task_defaults: Task-specific YAML defaults (yaml_data["tasks"][task_name])
        program_defaults: Dataclass field defaults (e.g., TaskConfig.duration)

    Returns:
        Merged dict with all config values resolved according to precedence.
    """
    merged = program_defaults | top_defaults
    merged = _merge_task_defaults(merged, task_defaults)
    merged = _apply_namespace(merged, args)
    return merged


def _merge_task_defaults(merged: dict[str, Any], task_defaults: dict[str, Any]) -> dict[str, Any]:
    for key, value in task_defaults.items():
        if _should_deep_merge_display(key, value, merged):
            merged["display"] = _deep_merge_dicts(merged["display"], value)
        else:
            merged[key] = value
    return merged


def _apply_namespace(merged: dict[str, Any], namespace: object | None) -> dict[str, Any]:
    if namespace is None:
        return merged
    for key, val in vars(namespace).items():
        if val is not None:
            merged[key] = val
    return merged


def _should_deep_merge_display(key: str, value: Any, merged: dict[str, Any]) -> bool:
    return key == "display" and isinstance(value, dict) and isinstance(merged.get("display"), dict)


def _deep_merge_dicts(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overrides.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(value, dict):
            merged[key] = _deep_merge_dicts(base_value, value)
        else:
            merged[key] = value
    return merged
