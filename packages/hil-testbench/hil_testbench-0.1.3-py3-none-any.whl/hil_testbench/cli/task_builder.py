from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from hil_testbench.config.run_config import RunConfig
from hil_testbench.config.task_config import TaskConfig

from .task_loader import resolve_task_class

PACKAGE_INIT = "__init__.py"


def _build_top_defaults(yaml_data: dict[str, Any]) -> dict[str, Any]:
    """Merge YAML defaults with project-level display configuration."""
    defaults = dict(yaml_data.get("defaults", {}) or {})
    global_display = yaml_data.get("display")
    if isinstance(global_display, Mapping):
        existing_display = defaults.get("display")
        if isinstance(existing_display, Mapping):
            merged_display = dict(existing_display)
            merged_display.update(global_display)
        else:
            merged_display = dict(global_display)
        defaults["display"] = merged_display
    return defaults


def build_task_instances(
    task_list: list[str],
    args: argparse.Namespace,
    yaml_data: dict,
    run_config: Any,
    yaml_tasks: dict[str, Any],
) -> tuple[list[Any], dict[str, TaskConfig]]:
    """Materialize task objects and TaskConfig instances for execution."""
    task_dir_raw = args.task_dir
    task_module_prefix = task_dir_raw.replace("/", ".").replace("\\", ".")
    task_dir_path = Path(task_dir_raw).expanduser().resolve()
    use_package_import = _is_package_like_path(task_dir_raw)
    top_defaults = _build_top_defaults(yaml_data)
    configs: dict[str, TaskConfig] = {}
    instances: list[Any] = []

    for task_name in task_list:
        task_args = argparse.Namespace(**vars(args))
        task_args.task = task_name
        yaml_task_cfg = yaml_tasks.get(task_name, {})
        try:
            if use_package_import:
                task_module = importlib.import_module(f"{task_module_prefix}.{task_name}")
            else:
                task_module = _load_task_module_from_path(task_dir_path, task_name)
            task_cls = resolve_task_class(task_module)
        except (ModuleNotFoundError, AttributeError) as err:
            raise RuntimeError(
                f"Could not find task '{task_name}' in {args.task_dir} folder: {err}"
            ) from err
        config = TaskConfig.from_args(
            args=task_args,
            top_defaults=top_defaults,
            task_defaults=yaml_task_cfg,
            run_config=run_config,
        )
        instances.append(task_cls(config))
        configs[task_name] = config

    return instances, configs


def ensure_adaptive_pipeline_defaults(run_config: RunConfig) -> RunConfig:
    """Populate adaptive pipeline caps when config omits them."""

    updates: dict[str, Any] = {}
    if not hasattr(run_config, "event_buffer_max"):
        updates["event_buffer_max"] = 50
    if not hasattr(run_config, "event_max_age_ms"):
        updates["event_max_age_ms"] = 500
    if not hasattr(run_config, "event_dynamic_field_cap"):
        updates["event_dynamic_field_cap"] = 500
    return run_config.with_updates(**updates) if updates else run_config


def _is_package_like_path(task_dir: str) -> bool:
    # dotted reference like "mytasks" or "foo.bar"
    if "." in task_dir and not any(sep in task_dir for sep in (os.sep, os.altsep or "")):
        return True

    path = Path(task_dir).expanduser().resolve()
    return (path / PACKAGE_INIT).is_file()


def _load_task_module_from_path(task_dir: Path, task_name: str):
    module_file = _resolve_module_file(task_dir, task_name)

    unique_name = f"_hil_task_{task_name}_{abs(hash(module_file.as_posix())) & 0xFFFFFFFF}"
    public_name = task_name

    # Remove stale modules
    sys.modules.pop(public_name, None)
    sys.modules.pop(unique_name, None)

    # Determine package name
    package_name = task_dir.name if (task_dir / PACKAGE_INIT).is_file() else None

    # Load under PUBLIC NAME (important!)
    spec = importlib.util.spec_from_file_location(public_name, module_file)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(f"Cannot import '{task_name}'")

    module = importlib.util.module_from_spec(spec)

    module.__package__ = package_name

    # Register under public name BEFORE exec so relative imports work
    sys.modules[public_name] = module

    # Execute module
    spec.loader.exec_module(module)

    # Also register unique alias (optional but harmless)
    sys.modules[unique_name] = module

    return module


def _resolve_module_file(task_dir: Path, task_name: str) -> Path:
    candidate = task_dir / f"{task_name}.py"
    if candidate.is_file():
        return candidate
    package_init = task_dir / task_name / PACKAGE_INIT
    if package_init.is_file():
        return package_init
    raise ModuleNotFoundError(f"Task module '{task_name}' not found under {task_dir}")
