"""ThresholdEvaluator - Unified threshold evaluation logic.

Eliminates code duplication between threshold color retrieval and threshold
color application in LiveDisplayManager.
"""

from __future__ import annotations

from typing import Any

from hil_testbench.data_processing.expression_engine import CompiledExpression, ExpressionEngine
from hil_testbench.data_structs.parameters import ParameterField, Threshold
from hil_testbench.data_structs.threshold_utils import is_threshold_triggered

_EXPRESSION_ENGINE = ExpressionEngine()
_THRESHOLD_CACHE: dict[int, CompiledExpression] = {}


class ThresholdEvaluator:
    """Evaluate thresholds for parameter values."""

    # Priority order for threshold evaluation (highest to lowest)
    THRESHOLD_PRIORITY = ["critical", "bad", "error", "warn", "warning", "good"]

    @staticmethod
    def evaluate(
        value: Any,
        param_field: ParameterField,
        *,
        stats: Any | None = None,
        context: dict[str, Any] | None = None,
    ) -> Threshold | None:
        """Find triggered threshold for given value (highest priority).

        Args:
            value: Raw parameter value
            param_field: Parameter field with threshold definitions
            stats: Optional statistics object (e.g., ParameterStats) for formula thresholds
            context: Optional cross-parameter context mapping for formula thresholds

        Returns:
            Triggered Threshold object or None if no threshold triggered
        """
        if not param_field.thresholds or value is None:
            return None

        # Convert to numeric
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return None

        # Check thresholds in priority order
        for priority_name in ThresholdEvaluator.THRESHOLD_PRIORITY:
            if priority_name not in param_field.thresholds:
                continue

            threshold = param_field.thresholds[priority_name]
            if not threshold.color:
                continue

            if ThresholdEvaluator._is_triggered(numeric_value, threshold, stats, context):
                return threshold

        return None

    @staticmethod
    def _is_triggered(
        numeric_value: float,
        threshold: Threshold,
        stats: Any | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """Check if threshold condition is triggered."""

        if threshold.is_formula:
            return ThresholdEvaluator._is_formula_triggered(
                threshold, numeric_value, stats, context
            )
        return is_threshold_triggered(numeric_value, threshold)

    @staticmethod
    def _is_formula_triggered(
        threshold: Threshold,
        numeric_value: float,
        stats: Any | None,
        context: dict[str, Any] | None,
    ) -> bool:
        expression = threshold.value if isinstance(threshold.value, str) else None
        if not expression:
            return False

        compiled = _THRESHOLD_CACHE.get(id(threshold))
        if compiled is None:
            try:
                compiled = _EXPRESSION_ENGINE.compile(expression)
                _THRESHOLD_CACHE[id(threshold)] = compiled
            except ValueError:
                return False

        namespace = ThresholdEvaluator._build_formula_namespace(numeric_value, stats, context)
        try:
            result = _EXPRESSION_ENGINE.evaluate(compiled, namespace)
        except Exception:  # noqa: BLE001
            return False
        return bool(result)

    @staticmethod
    def _build_formula_namespace(
        numeric_value: float, stats: Any | None, context: dict[str, Any] | None
    ) -> dict[str, Any]:
        history_values = []
        if stats and getattr(stats, "history", None) is not None:
            try:
                history_values = list(stats.history)
            except Exception:  # pragma: no cover - defensive
                history_values = []

        return {
            "value": numeric_value,
            "avg": getattr(stats, "average", None) if stats else None,
            "min": getattr(stats, "min", None) if stats else None,
            "max": getattr(stats, "max", None) if stats else None,
            "count": getattr(stats, "count", None) if stats else None,
            "history": history_values,
            "ctx": context or {},
        }

    @staticmethod
    def get_color(
        value: Any,
        param_field: ParameterField,
        *,
        stats: Any | None = None,
        context: dict[str, Any] | None = None,
    ) -> str | None:
        """Get threshold color for a value (convenience method).

        Args:
            value: Raw parameter value
            param_field: Parameter field with threshold definitions

        Returns:
            Color string if threshold triggered, None otherwise
        """
        threshold = ThresholdEvaluator.evaluate(value, param_field, stats=stats, context=context)
        return str(threshold.color) if threshold and threshold.color else None

    @staticmethod
    def apply_color(
        formatted_value: str,
        raw_value: Any,
        param_field: ParameterField,
        *,
        stats: Any | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Apply threshold-based color styling to formatted value.

        Args:
            formatted_value: Already formatted value string
            raw_value: Raw numeric value for threshold checking
            param_field: Parameter field with threshold definitions

        Returns:
            Formatted value with Rich color markup applied (if threshold triggered)
        """
        threshold = ThresholdEvaluator.evaluate(
            raw_value, param_field, stats=stats, context=context
        )
        if threshold and threshold.color:
            return f"[{threshold.color}]{formatted_value}[/{threshold.color}]"
        return formatted_value
