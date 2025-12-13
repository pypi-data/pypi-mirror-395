"""Generic schema-driven parser for extracting data from command output.

Applies extraction rules defined in ParametersSchema to tool output,
eliminating need for task-specific parser implementations.
"""

from collections.abc import Callable
from typing import Any, cast

from hil_testbench.data_processing.extractors import (
    CsvExtractor,
    JsonPathExtractor,
    RegexExtractor,
)
from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.task.specs import Parser


class SchemaParser(Parser):
    """Generic parser driven by schema extraction rules.

    Applies schema-defined extraction rules to each line of tool output.
    Supports regex, JSON path, and CSV column extraction methods.

    For tasks with dynamic parameter naming (e.g., a task generating
    throughput_eth0 from server_eth0 context), supports context-aware
    parameter name resolution.
    """

    def __init__(
        self,
        schema: ParametersSchema,
        param_name_from_context: Callable[[dict[str, Any]], str] | str | None = None,
    ) -> None:
        """Initialize parser with schema containing extraction rules.

        Args:
            schema: ParametersSchema with ExtractionRule for each parameter
            param_name_from_context: Optional parameter name resolver:
                - Callable: Function that takes context dict and returns param_name
                - str: Fixed parameter name to use for all extractions
                - None: Use parameter names from schema (default)
        """
        self.schema = schema
        self.param_name_from_context = param_name_from_context
        self._extractors: dict[str, RegexExtractor | JsonPathExtractor | CsvExtractor] = (
            self._build_extractors(schema)
        )

    def _build_extractors(
        self, schema: ParametersSchema
    ) -> dict[str, RegexExtractor | JsonPathExtractor | CsvExtractor]:
        """Compile extraction rules into efficient extractors.

        Args:
            schema: ParametersSchema containing fields with extraction rules

        Returns:
            Dict mapping parameter names to extractor instances

        Raises:
            ValueError: If extraction rule method is unknown
        """
        extractors: dict[str, RegexExtractor | JsonPathExtractor | CsvExtractor] = {}

        for field in schema.fields:
            if not field.extract:
                continue

            method = field.extract.method
            if method == "regex":
                extractors[field.name] = RegexExtractor(field.extract, field.type)
            elif method == "json":
                extractors[field.name] = JsonPathExtractor(field.extract, field.type)
            elif method == "csv":
                extractors[field.name] = CsvExtractor(field.extract, field.type)
            else:
                raise ValueError(f"Unknown extraction method: {method}")

        return extractors

    def feed(
        self, line: str, is_error: bool, context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Apply extraction rules and emit events for matched parameters.

        Args:
            line: Output line from command
            is_error: Whether line came from stderr (ignored)
            context: Optional context dict (used for dynamic param naming)

        Returns:
            List of event dicts with param_name and value fields
        """
        if is_error:
            return []
        if self.param_name_from_context is not None:
            return self._extract_with_context_routing(line, context)
        return self._extract_with_schema_routing(line)

    def _extract_with_context_routing(
        self, line: str, context: dict[str, Any] | None
    ) -> list[dict[str, Any]]:
        param_name = self._resolve_context_param_name(context)
        value = self._first_successful_extract(line)
        if value is None:
            return []

        events = [{"param_name": param_name, "value": value}]
        calculated_events = self._evaluate_calculated({param_name: value})
        if calculated_events:
            events.extend(calculated_events)
        return events

    def _resolve_context_param_name(self, context: dict[str, Any] | None) -> str:
        if callable(self.param_name_from_context):
            return self.param_name_from_context(context or {})
        return cast(str, self.param_name_from_context)

    def _first_successful_extract(self, line: str) -> Any | None:
        for extractor in self._extractors.values():
            value = self._safe_extract(extractor, line)
            if value is not None:
                return value
        return None

    def _extract_with_schema_routing(self, line: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        row: dict[str, Any] = {}
        for param_name, extractor in self._extractors.items():
            value = self._safe_extract(extractor, line)
            if value is not None:
                events.append({"param_name": param_name, "value": value})
                row[param_name] = value
        if row:
            calculated_events = self._evaluate_calculated(row)
            if calculated_events:
                events.extend(calculated_events)
        return events

    @staticmethod
    def _safe_extract(
        extractor: RegexExtractor | JsonPathExtractor | CsvExtractor, line: str
    ) -> Any | None:
        try:
            return extractor.extract(line)
        except Exception:
            # Extraction failure - log and continue
            # Don't crash on malformed input
            return None

    def _evaluate_calculated(self, row: dict[str, Any]) -> list[dict[str, Any]]:
        if not getattr(self.schema, "calculated_params", None):
            return []

        calculated_events: list[dict[str, Any]] = []
        values = dict(row)

        for name, calc in self.schema.calculated_params.items():
            try:
                value = calc.fn(values)
            except Exception:
                continue
            if value is None:
                continue
            try:
                typed_value = calc.field.type(value)
            except Exception:
                continue
            calculated_events.append({"param_name": name, "value": typed_value})
            values[name] = typed_value

        return calculated_events
