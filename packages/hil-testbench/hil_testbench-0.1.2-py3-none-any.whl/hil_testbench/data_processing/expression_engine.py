"""Safe expression compilation and evaluation for derived parameters.

Uses ``simpleeval`` with a restricted function namespace and basic AST validation to
prevent unsafe constructs (attribute access, imports, lambdas). Time-windowed
functions are injected when a registry is bound via ``bind_windowed_stats``.
"""

from __future__ import annotations

import ast
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

try:
    from simpleeval import EvalWithCompoundTypes, FunctionNotDefined, NameNotDefined, simple_eval
except ModuleNotFoundError:
    EvalWithCompoundTypes = None  # type: ignore[assignment]
    FunctionNotDefined = None  # type: ignore[assignment]
    NameNotDefined = None  # type: ignore[assignment]
    simple_eval = None  # type: ignore[assignment]

if TYPE_CHECKING:  # pragma: no cover - import for typing only
    from hil_testbench.run.session.time_windowed_stats import TimeWindowedStatsRegistry


@dataclass(frozen=True, slots=True)
class CompiledExpression:
    """Opaque handle to a compiled expression AST."""

    ast: Any
    formula: str


class ExpressionEngine:
    """Compile and evaluate parameter formulas with a constrained sandbox."""

    _BASE_FUNCTIONS: dict[str, Any] = {
        "abs": abs,
        "min": min,
        "max": max,
        "round": round,
        "len": len,
        "sum": sum,
        "sqrt": math.sqrt,
        "pow": pow,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    def __init__(self) -> None:
        self._functions: dict[str, Any] = dict(self._BASE_FUNCTIONS)
        self._windowed_stats: TimeWindowedStatsRegistry | None = None

    def bind_windowed_stats(self, registry: TimeWindowedStatsRegistry) -> None:
        """Inject time-windowed stats registry for aggregation helpers."""

        self._windowed_stats = registry
        self._functions.update(
            {
                "avg_1min": lambda param: self._get_windowed_stat(param, "avg_1min"),
                "avg_5min": lambda param: self._get_windowed_stat(param, "avg_5min"),
                "avg_1hour": lambda param: self._get_windowed_stat(param, "avg_1hour"),
                "max_1hour": lambda param: self._get_windowed_stat(param, "max_1hour"),
                "min_1hour": lambda param: self._get_windowed_stat(param, "min_1hour"),
            }
        )

    def compile(self, formula: str) -> CompiledExpression:
        """Compile a formula string into a safe AST."""

        evaluator = self._load_evaluator()
        try:
            parsed = evaluator.parse(formula)
        except SyntaxError as exc:  # pragma: no cover - simpleeval formatting
            raise ValueError(f"Formula syntax error: {exc}") from exc
        self._validate_ast(parsed)
        return CompiledExpression(ast=parsed, formula=formula)

    def evaluate(self, compiled: CompiledExpression, namespace: Mapping[str, Any]) -> Any:
        """Evaluate a compiled expression with the provided namespace."""

        evaluator = self._load_eval_function()
        try:
            return evaluator(compiled.formula, names=namespace, functions=self._functions)
        except NameNotDefined as exc:  # type: ignore[unreachable]
            raise ValueError(f"Undefined variable: {exc}") from exc
        except FunctionNotDefined as exc:  # type: ignore[unreachable]
            raise ValueError(str(exc)) from exc
        except ZeroDivisionError:
            return None

    def _load_evaluator(self):
        evaluator_cls = EvalWithCompoundTypes
        if evaluator_cls is None:
            raise RuntimeError(
                "Derived parameter formulas require the 'simpleeval' package; install it in your environment."
            )
        return evaluator_cls(functions=self._functions)

    def _load_eval_function(self):
        evaluator_fn = simple_eval
        if evaluator_fn is None:
            raise RuntimeError(
                "Derived parameter formulas require the 'simpleeval' package; install it in your environment."
            )
        return evaluator_fn
    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_windowed_stat(self, param_key: str, method_name: str) -> Any:
        if not self._windowed_stats:
            return None
        stats = self._windowed_stats.get(str(param_key))
        method = getattr(stats, method_name, None)
        if callable(method):
            return method()
        return None

    def _validate_ast(self, parsed: Any) -> None:
        """Reject unsafe AST nodes before evaluation."""

        unsafe_nodes = (
            ast.Attribute,
            ast.Lambda,
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.Import,
            ast.ImportFrom,
            ast.Global,
            ast.Nonlocal,
            ast.ClassDef,
        )
        for node in ast.walk(parsed):
            if isinstance(node, unsafe_nodes):
                raise ValueError(f"Unsafe expression node: {type(node).__name__}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                raise ValueError("Attribute access in function calls is not allowed")


__all__ = ["ExpressionEngine", "CompiledExpression"]
