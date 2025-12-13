"""Generate a YAML option report for CI.

The script statically inspects the config/data classes and task modules to list
which YAML keys are recognized at the program level and which task-level keys
are referenced. It is intentionally conservative (no execution of tasks).
"""

from __future__ import annotations

import argparse
import ast
import json
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_ast(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"))


def _is_dict_assignment_to_var(node: ast.Assign, var_name: str) -> bool:
    """Check if assignment is a dict literal to the given variable."""
    return any(isinstance(t, ast.Name) and t.id == var_name for t in node.targets) and isinstance(
        node.value, ast.Dict
    )


def _extract_string_keys_from_dict(dict_node: ast.Dict) -> set[str]:
    """Extract string constant keys from a dict AST node."""
    keys: set[str] = set()
    for k in dict_node.keys:
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            keys.add(k.value)
    return keys


def _dict_literal_keys(tree: ast.AST, var_name: str) -> list[str]:
    keys: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and _is_dict_assignment_to_var(node, var_name):
            if isinstance(node.value, ast.Dict):
                keys.update(_extract_string_keys_from_dict(node.value))
    return sorted(keys)


def _is_set_assignment_to_var(node: ast.Assign, var_name: str) -> bool:
    """Check if assignment is a set literal to the given variable."""
    return any(isinstance(t, ast.Name) and t.id == var_name for t in node.targets) and isinstance(
        node.value, ast.Set
    )


def _extract_string_elements_from_set(set_node: ast.Set) -> set[str]:
    """Extract string constant elements from a set AST node."""
    values: set[str] = set()
    for elt in set_node.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
            values.add(elt.value)
    return values


def _set_literal_strings(tree: ast.AST, var_name: str) -> list[str]:
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and _is_set_assignment_to_var(node, var_name):
            if isinstance(node.value, ast.Set):
                values.update(_extract_string_elements_from_set(node.value))
    return sorted(values)


def _is_get_call_on_source(node: ast.Call, source_name: str) -> bool:
    """Check if call is source.get(string_literal)."""
    if not isinstance(node.func, ast.Attribute):
        return False
    if node.func.attr != "get":
        return False
    if not isinstance(node.func.value, ast.Name):
        return False
    if node.func.value.id != source_name:
        return False
    if not node.args:
        return False
    if not isinstance(node.args[0], ast.Constant):
        return False
    return isinstance(node.args[0].value, str)


def _yaml_get_keys(tree: ast.AST, source_name: str) -> list[str]:
    keys: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            if _is_get_call_on_source(node, source_name):
                arg = node.args[0]
                if isinstance(arg, ast.Constant):
                    keys.add(arg.value)  # type: ignore[arg-type]
            self.generic_visit(node)

    Visitor().visit(tree)
    return sorted(keys)


def _list_literal_values(tree: ast.AST, inside_function: str | None = None) -> list[str]:
    values: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if inside_function is None or node.name == inside_function:
                self.generic_visit(node)

        def visit_List(self, node: ast.List) -> None:
            for elt in node.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    values.add(elt.value)
            self.generic_visit(node)

    Visitor().visit(tree)
    return sorted(values)


def _attr_chain_matches(node: ast.AST, chain: Iterable[str]) -> bool:
    parts = list(chain)
    if not parts:
        return False
    current: ast.AST | None = node
    for expected in reversed(parts):
        if isinstance(current, ast.Attribute) and current.attr == expected:
            current = current.value
        elif isinstance(current, ast.Name) and current.id == expected and len(parts) == 1:
            current = None
        else:
            return False
    return True


def _process_get_call(
    node: ast.Call,
    task_param_keys: set[str],
    nested_keys: set[str],
) -> None:
    """Process .get() method calls to extract task parameter keys."""
    if not (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "get"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ):
        return

    key = node.args[0].value
    target = node.func.value
    if isinstance(target, ast.Attribute) and target.attr == "task_params":
        task_param_keys.add(key)
    if isinstance(target, ast.Name) and target.id == "link":
        nested_keys.add(f"link.{key}")


def _process_get_host_param_call(node: ast.Call, host_param_keys: set[str]) -> None:
    """Process .get_host_param() method calls."""
    if (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "get_host_param"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ):
        host_param_keys.add(node.args[0].value)


def _process_subscript(
    node: ast.Subscript, task_param_keys: set[str], nested_keys: set[str]
) -> None:
    """Process subscript operations to extract task parameter keys."""
    if not (isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str)):
        return

    key = node.slice.value
    if _attr_chain_matches(node.value, ["config", "task_params"]):
        task_param_keys.add(key)
    if isinstance(node.value, ast.Name) and node.value.id == "link":
        nested_keys.add(f"link.{key}")


def _task_keys_from_ast(tree: ast.AST) -> dict[str, list[str]]:
    task_param_keys: set[str] = set()
    host_param_keys: set[str] = set()
    nested_keys: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            _process_get_call(node, task_param_keys, nested_keys)
            _process_get_host_param_call(node, host_param_keys)
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            _process_subscript(node, task_param_keys, nested_keys)
            self.generic_visit(node)

    Visitor().visit(tree)
    return {
        "task_params_keys": sorted(task_param_keys),
        "host_param_keys": sorted(host_param_keys),
        "nested_keys": sorted(nested_keys),
    }


def build_report() -> dict:
    run_cfg_tree = _load_ast(ROOT / "hil_testbench" / "config" / "run_config.py")
    task_cfg_tree = _load_ast(ROOT / "hil_testbench" / "config" / "task_config.py")
    merger_tree = _load_ast(ROOT / "hil_testbench" / "config" / "config_merger.py")

    tasks_dir = ROOT / "tasks"
    task_reports = {}
    for path in sorted(tasks_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        task_tree = _load_ast(path)
        task_reports[path.stem] = _task_keys_from_ast(task_tree)

    report = {
        "root_sections": ["defaults", "hosts", "tasks"],
        "run_config_yaml_keys": _yaml_get_keys(run_cfg_tree, "yaml_data"),
        "task_defaults_keys": _dict_literal_keys(task_cfg_tree, "program_defaults"),
        "task_reserved_keys": _set_literal_strings(task_cfg_tree, "RESERVED_KEYS"),
        "cli_override_keys": _list_literal_values(
            merger_tree, inside_function="merge_config_sources"
        ),
        "tasks": task_reports,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect YAML option usage and output a report.")
    parser.add_argument(
        "--format",
        choices=["json", "pretty"],
        default="pretty",
        help="Output format (pretty prints JSON with indentation).",
    )
    parser.add_argument("--output", type=Path, help="Optional file to write.")
    args = parser.parse_args()

    report = build_report()

    if args.format == "json":
        text = json.dumps(report)
    else:
        text = json.dumps(report, indent=2, sort_keys=True)

    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
