"""
Generic JSON stream accumulator for line-oriented process output.
Task-agnostic: decodes either brace-balanced JSON objects spanning lines
or newline-delimited JSON (NDJSON).

Usage:
    acc = JsonAccumulator(ndjson=False)
    for line in lines:
        for obj in acc.feed(line):
            handle(obj)
"""

from __future__ import annotations

import json
import sys
from typing import Any

from hil_testbench.data_structs.parameters import ParametersSchema
from hil_testbench.run.logging.task_logger import LogLevel, LogScope

# Maximum number of parse errors to log before silencing
_MAX_PARSE_ERRORS_TO_LOG = 3


class JsonAccumulator:
    """Accumulates streaming JSON objects, validates against schema if provided."""

    def __init__(self, ndjson: bool = False, schema: ParametersSchema | None = None) -> None:
        self.ndjson = ndjson
        self.schema = schema
        self._schema_fields = {field.name for field in schema.fields} if schema else None
        self._buffer: list[str] = []
        self._brace_balance = 0
        self._in_string = False
        self._escape_next = False
        self._parse_error_count = 0

    def reset(self) -> None:
        """Reset the internal buffer and brace counter."""
        self._buffer.clear()
        self._brace_balance = 0
        self._in_string = False
        self._escape_next = False

    def _parse_ndjson_line(self, line: str) -> list[dict[str, Any]]:
        """Parse a single NDJSON line and return parsed objects.

        Args:
            line: JSON line to parse

        Returns:
            List containing parsed dict, or empty list on error
        """
        line = line.strip()
        if not line:
            return []

        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                return [obj]
        except json.JSONDecodeError as e:
            self._log_parse_error(line, e)

        return []

    def _log_parse_error(self, line: str, error: json.JSONDecodeError) -> None:
        """Log JSON parse errors for debugging (first few occurrences only).

        Args:
            line: Line that failed to parse
            error: JSONDecodeError exception
        """
        if not hasattr(self, "_parse_error_count"):
            self._parse_error_count = 0
        self._parse_error_count += 1

        if self._parse_error_count <= _MAX_PARSE_ERRORS_TO_LOG and (
            logger := getattr(
                sys.modules.get("hil_testbench.run.logging.task_logger"),
                "get_global_logger",
                lambda: None,
            )()
        ):
            logger.log(
                "json_parse_failed",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                _line_preview=line[:100],
                _error=str(error),
                _parse_error_count=self._parse_error_count,
            )

    def _parse_brace_balanced(self, line: str) -> list[dict[str, Any]]:
        """Parse brace-balanced multi-line JSON objects.

        Args:
            line: Line to add to buffer

        Returns:
            List containing parsed dict if object is complete, else empty list
        """
        self._buffer.append(line.rstrip("\n"))
        self._update_brace_balance(line)

        if self._brace_balance != 0 or self._in_string:
            return []  # Object not complete yet

        # Complete object in buffer - parse it
        raw = "\n".join(self._buffer)
        self.reset()

        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            self._log_parse_error(raw, e)
            return []

        if isinstance(obj, dict):
            return [obj]
        return []

    def _update_brace_balance(self, line: str) -> None:
        """Track brace balance while ignoring braces inside JSON strings."""
        for char in line:
            if self._escape_next:
                self._escape_next = False
                continue

            if char == "\\":
                self._escape_next = True
                continue

            if char == '"':
                self._in_string = not self._in_string
                continue

            if self._in_string:
                continue

            if char == "{":
                self._brace_balance += 1
            elif char == "}" and self._brace_balance > 0:
                self._brace_balance -= 1

    def feed(self, line: str) -> list[dict[str, Any]]:
        """Feed one line of text; return zero or more parsed JSON objects.

        This method is resilient to malformed input: if decoding fails,
        the offending chunk is discarded and parsing continues.
        """
        if not line:
            return []

        if self.ndjson:
            return self._parse_ndjson_line(line)

        return self._parse_brace_balanced(line)

    def feed_with_validation(self, line: str) -> list[dict[str, Any]]:
        """Feed a line of JSON or NDJSON, return only valid objects that match schema.

        Objects with unknown fields are silently filtered out when schema validation is enabled.
        """
        objs = self.feed(line)
        if not self._schema_fields:
            return objs

        validated: list[dict[str, Any]] = []
        for obj in objs:
            if not isinstance(obj, dict):
                continue
            if unknown_field := next(
                (field for field in obj if field not in self._schema_fields), None
            ):
                raise ValueError(f"Unknown field '{unknown_field}' in JSON payload")
            validated.append(obj)
        return validated
