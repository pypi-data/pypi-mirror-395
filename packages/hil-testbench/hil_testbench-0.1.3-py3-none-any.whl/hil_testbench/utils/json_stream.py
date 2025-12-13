"""Utilities for streaming JSON output."""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from typing import Any


class JsonEventAccumulator:
    """Accumulate JSON events from streaming output."""

    def __init__(self) -> None:
        self._buffer = ""

    def feed(self, line: str) -> Iterator[dict[str, Any]]:
        self._buffer += line
        while self._buffer:
            obj, remaining = self._extract_json_object(self._buffer)
            if obj is None:
                break
            self._buffer = remaining
            yield obj

    def _extract_json_object(self, text: str) -> tuple[dict[str, Any] | None, str]:
        # Try NDJSON (line-delimited)
        if "\n" in text:
            head, tail = text.split("\n", 1)
            try:
                return json.loads(head), tail
            except json.JSONDecodeError:
                pass

        # Try brace-balanced extraction
        depth = 0
        start = None
        for idx, char in enumerate(text):
            if char == "{":
                if depth == 0:
                    start = idx
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0 and start is not None:
                    candidate = text[start : idx + 1]
                    try:
                        obj = json.loads(candidate)
                        return obj, text[idx + 1 :]
                    except json.JSONDecodeError:
                        continue
        return None, text


def add_interval_metadata(
    event: dict[str, Any],
    interval_index: int,
    timestamp: float | None = None,
) -> dict[str, Any]:
    """Add interval metadata (index + timestamp) to event."""

    if timestamp is None:
        timestamp = time.time()
    event["interval_index"] = interval_index
    event["timestamp"] = timestamp
    return event
