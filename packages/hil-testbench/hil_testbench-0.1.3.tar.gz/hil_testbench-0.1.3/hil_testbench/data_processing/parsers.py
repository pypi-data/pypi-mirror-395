"""Built-in parser primitives for task command output parsing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hil_testbench.data_processing.accumulators import JsonAccumulator
from hil_testbench.task.specs import Parser


@dataclass
class JsonStreamParser(Parser):
    """Parses one JSON object per (possibly multi-line) chunk.

    Works for tools that emit brace-balanced objects or ndjson when
    configured accordingly.
    """

    ndjson: bool = False

    def __post_init__(self) -> None:
        self._acc = JsonAccumulator(ndjson=self.ndjson)

    def feed(
        self, line: str, is_error: bool, context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        return [] if is_error else self._acc.feed(line)


@dataclass
class DelimitedParser(Parser):
    """Simple CSV/TSV parser mapping fields by index or header.

    If headers are provided, map by name; otherwise use provided fieldnames.
    """

    delimiter: str = ","
    fieldnames: list[str] | None = None
    has_header: bool = False

    def __post_init__(self) -> None:
        self._header: list[str] | None = None

    def feed(
        self, line: str, is_error: bool, context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if self._should_skip_line(line, is_error):
            return []

        parts = self._split_line(line)
        if not parts:
            return []

        if self._maybe_set_header(parts):
            return []

        keys = self._determine_keys(len(parts))
        return [self._build_record(keys, parts)]

    def _should_skip_line(self, line: str, is_error: bool) -> bool:
        return is_error or not line.strip()

    def _split_line(self, line: str) -> list[str]:
        return line.strip().split(self.delimiter)

    def _maybe_set_header(self, parts: list[str]) -> bool:
        if self.has_header and self._header is None:
            self._header = [p.strip() for p in parts]
            return True
        return False

    def _determine_keys(self, part_count: int) -> list[str]:
        if self._header is not None:
            return self._header
        if self.fieldnames is not None:
            return self.fieldnames
        return [f"col{i}" for i in range(part_count)]

    def _build_record(self, keys: list[str], parts: list[str]) -> dict[str, Any]:
        return {k: parts[i] if i < len(parts) else None for i, k in enumerate(keys)}
