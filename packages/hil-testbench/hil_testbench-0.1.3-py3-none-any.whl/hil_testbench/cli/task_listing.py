from __future__ import annotations

import importlib


def print_task_list(task_names: list[str], task_dir: str = "tasks") -> None:
    print("Available tasks:")  # hil: allow-print
    task_module_prefix = task_dir.replace("/", ".").replace("\\", ".")
    for name in sorted(task_names):
        try:
            tmod = importlib.import_module(f"{task_module_prefix}.{name}")
            short = (tmod.__doc__ or "").splitlines()[0].strip()
        except Exception:
            short = "(failed to import description)"

        print(f"  {name}: {short}")  # hil: allow-print
    print("\nUsage: python run_tasks.py [OPTIONS] TASK [TASK ...]")  # hil: allow-print
    print("Example: python run_tasks.py task1 task2 --duration 100")  # hil: allow-print
