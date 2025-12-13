"""Visualization utilities for task dependency graphs.

Optional helpers for debugging dependency issues. Requires matplotlib.
"""

from __future__ import annotations

import contextlib
import importlib
from collections import defaultdict
from typing import Any

from hil_testbench.task.dependency import build_dependency_graph

plt: Any | None = None
nx: Any | None = None
VISUALIZATION_AVAILABLE = False

with contextlib.suppress(ImportError):
    plt = importlib.import_module("matplotlib.pyplot")
    nx = importlib.import_module("networkx")
    VISUALIZATION_AVAILABLE = True


def visualize_task_dependencies(
    tasks: dict[str, Any], output_file: str | None = None, show: bool = True
) -> None:
    """Visualize task dependency graph.

    Args:
        tasks: Map of task_name -> task_object
        output_file: Optional path to save image (e.g., "deps.png")
        show: Whether to display interactive plot

    Raises:
        ImportError: If matplotlib is not installed
    """
    if not VISUALIZATION_AVAILABLE:
        raise ImportError("Visualization requires matplotlib. Install with: pip install matplotlib")

    # Build graph
    graph = build_dependency_graph(tasks)
    assert nx is not None  # for type checkers
    assert plt is not None
    G = nx.DiGraph()

    for node in graph:
        G.add_node(node)

    for task, dependencies in graph.items():
        for dep in dependencies:
            G.add_edge(dep, task)

    # Layout and draw
    pos = nx.spring_layout(G, k=1, iterations=50)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=3000,
        font_size=10,
        font_weight="bold",
        arrowsize=20,
        edge_color="gray",
        width=2,
    )

    plt.title("Task Dependency Graph", fontsize=16)
    plt.axis("off")

    if output_file:
        plt.savefig(output_file, bbox_inches="tight", dpi=150)
        print(f"Graph saved to {output_file}")  # hil: allow-print

    if show:
        plt.show()


def print_execution_order(tasks: dict[str, Any]) -> None:
    """Print task execution order by phase.

    Args:
        tasks: Map of task_name -> task_object
    """
    sorted_phases = _group_by_phase_and_sort(tasks)

    print("\n=== Task Execution Order ===\n")  # hil: allow-print

    for phase in ["initialization", "main", "teardown"]:
        task_list = sorted_phases.get(phase, [])
        if not task_list:
            continue

        print(f"{phase.upper()} Phase:")  # hil: allow-print
        for i, task_name in enumerate(task_list, 1):
            task_obj = tasks[task_name]
            deps = getattr(task_obj, "depends_on", [])
            dep_str = f" (depends on: {', '.join(deps)})" if deps else ""
            print(f"  {i}. {task_name}{dep_str}")  # hil: allow-print
            print()  # hil: allow-print


def _group_by_phase_and_sort(tasks: dict[str, Any]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for name, task in tasks.items():
        phase = getattr(task, "phase", "main") or "main"
        grouped[phase].append(name)
    for names in grouped.values():
        names.sort()
    return grouped
