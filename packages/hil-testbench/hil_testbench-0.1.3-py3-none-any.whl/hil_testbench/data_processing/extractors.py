"""Schema-driven data extraction from tool output.

Provides generic extractors that apply schema-defined rules to extract parameter
values from command output (regex, JSON, CSV).
"""

import csv
import io
import re
from typing import Any

from hil_testbench.data_processing.parsers import JsonAccumulator
from hil_testbench.data_structs.parameters import ExtractionRule


class RegexExtractor:
    """Extract value using regex pattern with capture group."""

    def __init__(self, rule: ExtractionRule, value_type: type) -> None:
        if not rule.pattern:
            raise ValueError("RegexExtractor requires pattern")

        self.pattern = re.compile(rule.pattern)
        self.group = rule.group
        self.value_type = value_type
        self.transform = rule.transform

    def extract(self, line: str) -> Any | None:
        """Extract value from line using regex pattern.

        Args:
            line: Input line from command output

        Returns:
            Extracted value converted to target type, or None if no match
        """
        match = self.pattern.search(line)
        if not match:
            return None

        raw_value = match.group(self.group)
        raw_value = self.transform(raw_value) if self.transform else raw_value
        return _safe_convert(raw_value, self.value_type)


class JsonPathExtractor:
    """Extract value using JSON path notation."""

    def __init__(self, rule: ExtractionRule, value_type: type) -> None:
        if not rule.path:
            raise ValueError("JsonPathExtractor requires path")

        self.path = rule.path
        self.value_type = value_type
        self.transform = rule.transform
        self._accumulator = JsonAccumulator(ndjson=False)

    def extract(self, line: str) -> Any | None:
        """Extract value from JSON line using path notation.

        Args:
            line: Input line containing JSON data

        Returns:
            Extracted value at JSON path, or None if not found
        """
        for obj in self._accumulator.feed(line):
            value = self._navigate_path(obj, self.path)
            if value is None:
                continue
            value = self.transform(value) if self.transform else value
            return _safe_convert(value, self.value_type)
        return None

    def _navigate_path(self, obj: dict | list, path: str) -> Any:
        """Navigate JSON path like 'intervals[-1].sum.bits_per_second'.

        Args:
            obj: JSON object to navigate
            path: Dot-separated path with optional array indices

        Returns:
            Value at path, or None if path doesn't exist
        """
        current: Any = obj
        for part in filter(None, path.split(".")):
            current = self._resolve_segment(current, part)
            if current is None:
                return None
        return current

    def _resolve_segment(self, current: Any, part: str) -> Any:
        if "[" not in part:
            return current.get(part) if isinstance(current, dict) else None

        key, index_str = part.split("[", 1)
        index_str = index_str.rstrip("]")
        current = self._resolve_key(current, key)
        if current is None:
            return None
        return self._resolve_list_index(current, index_str)

    @staticmethod
    def _resolve_key(current: Any, key: str) -> Any:
        if not key:
            return current
        if isinstance(current, dict):
            return current.get(key)
        return None

    @staticmethod
    def _resolve_list_index(current: Any, index_str: str) -> Any:
        if not isinstance(current, list):
            return None
        try:
            return current[int(index_str)]
        except (ValueError, IndexError):
            return None


class CsvExtractor:
    """Extract value from CSV column by index or name."""

    def __init__(self, rule: ExtractionRule, value_type: type) -> None:
        if rule.column is None:
            raise ValueError("CsvExtractor requires column")

        self.column: int | str = rule.column  # Can be int (index) or str (name)
        self.value_type = value_type
        self.transform = rule.transform
        self._header_row: list[str] | None = None
        self._use_index = isinstance(rule.column, int)

    def extract(self, line: str) -> Any | None:
        """Extract value from CSV line by column index or name.

        Args:
            line: CSV-formatted input line

        Returns:
            Value from specified column, or None if not found
        """
        if not line.strip():
            return None

        # Parse CSV line
        reader = csv.reader(io.StringIO(line))
        try:
            row = next(reader)
        except (StopIteration, csv.Error):
            return None

        raw_value = self._extract_by_index(row) if self._use_index else self._extract_by_name(row)

        if raw_value is None:
            return None

        raw_value = self.transform(raw_value) if self.transform else raw_value
        return _safe_convert(raw_value, self.value_type)

    def _extract_by_index(self, row: list[str]) -> str | None:
        assert isinstance(self.column, int)
        col_index = self.column
        if col_index >= len(row):
            return None
        return row[col_index].strip() or None

    def _extract_by_name(self, row: list[str]) -> str | None:
        assert isinstance(self.column, str)
        if self._header_row is None:
            if self.column in row:
                self._header_row = row
            return None
        try:
            col_index = self._header_row.index(self.column)
        except ValueError:
            return None
        if col_index >= len(row):
            return None
        return row[col_index].strip() or None


_NUMERIC_PREFIX = re.compile(r"^[\s]*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)")


def _safe_convert(value: Any, target_type: type) -> Any | None:
    try:
        return target_type(value)
    except (ValueError, TypeError):
        if (
            isinstance(value, str)
            and target_type in (int, float)
            and (match := _NUMERIC_PREFIX.match(value))
        ):
            try:
                return target_type(match.group(1))
            except (ValueError, TypeError):
                return None
        return None
