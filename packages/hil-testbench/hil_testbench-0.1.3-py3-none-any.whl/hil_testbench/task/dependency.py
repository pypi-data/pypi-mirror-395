"""Dependency graph builder and topological sorter for task execution.

Provides dependency resolution with cycle detection to determine valid
execution order for tasks with inter-dependencies.

Uses NetworkX for battle-tested graph algorithms (topological sort, cycle detection).
"""

from __future__ import annotations

import contextlib
from typing import Any

import networkx as nx


class DependencyError(Exception):
    """Raised when dependency graph has cycles or missing dependencies."""


def build_dependency_graph(tasks: dict[str, Any]) -> dict[str, set[str]]:
    """Build adjacency list from task dependencies.

    Args:
        tasks: Map of task_name -> task_object

    Returns:
        Map of task_name -> set of task names it depends on

    Raises:
        DependencyError: If a task depends on non-existent task
    """
    graph: dict[str, set[str]] = {}

    for task_name, task_obj in tasks.items():
        depends = getattr(task_obj, "depends_on", None) or []
        if not isinstance(depends, list):
            depends = [depends]

        # Validate all dependencies exist
        for dep in depends:
            if dep not in tasks:
                raise DependencyError(f"Task '{task_name}' depends on unknown task '{dep}'")

        graph[task_name] = set(depends)

    return graph


def topological_sort(graph: dict[str, set[str]]) -> list[str]:
    """Sort tasks by dependencies using NetworkX topological sort.

    Args:
        graph: Adjacency list (task -> dependencies it requires)

    Returns:
        Ordered list of task names (dependencies first)

    Raises:
        DependencyError: If graph contains cycles
    """
    # Build directed graph: edges point from dependency to dependent
    # (if task A depends on B, edge goes B -> A)
    dependency_graph: nx.DiGraph[str] = nx.DiGraph()

    # Add all nodes first
    for node in graph:
        dependency_graph.add_node(node)

    # Add edges: dependency -> task
    for task, dependencies in graph.items():
        for dep in dependencies:
            dependency_graph.add_edge(dep, task)

    # Check for cycles
    with contextlib.suppress(nx.NetworkXNoCycle):
        if cycles := list(nx.simple_cycles(dependency_graph)):
            # Format cycle for error message
            cycle_str = " -> ".join(cycles[0]) + f" -> {cycles[0][0]}"
            raise DependencyError(f"Circular dependency detected: {cycle_str}")
    # Perform topological sort
    try:
        return list(nx.topological_sort(dependency_graph))
    except nx.NetworkXError as e:
        raise DependencyError(f"Failed to sort dependencies: {e}") from e
