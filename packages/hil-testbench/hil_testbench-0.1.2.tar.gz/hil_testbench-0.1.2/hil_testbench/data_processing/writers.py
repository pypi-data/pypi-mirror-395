"""Generic writers for CSV and JSONL with rotation support."""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from hil_testbench.data_structs.parameters import ParametersSchema


class BaseWriter:
    """Base writer for event data - no validation or formatting needed."""

    def __init__(self, schema: ParametersSchema | None = None):
        self.schema = schema  # Available for reference, not used for validation

    def write(self, event: dict):
        """Write event directly. Subclasses implement actual writing logic."""
        self._write_event(event)

    def _write_event(self, event: dict):
        """Actual writing logic to be implemented by subclasses."""
        raise NotImplementedError


class CsvWriter(BaseWriter):
    """
    CSV writer with optional header-once functionality and rotation.
    """

    def __init__(
        self,
        path: str,
        fieldnames: Iterable[str],
        write_header_once: bool = True,
        max_bytes: int = 10 * 1024 * 1024,
        max_rotations: int = 3,
        schema: ParametersSchema | None = None,
    ) -> None:
        """
        Args:
            path: File path for the CSV.
            fieldnames: Column names.
            write_header_once: Write header only once if True.
            max_bytes: Maximum file size before rotation (default 10MB).
            max_rotations: Maximum number of rotated files to keep (default 3).
        """
        super().__init__(schema=schema)
        self.path = path
        self.fieldnames = list(fieldnames)
        self.write_header_once = write_header_once
        self.max_bytes = max_bytes
        self.max_rotations = max_rotations
        self._header_written = False
        self._bytes_written = 0

        # Add timestamp field if not present
        if "timestamp" not in self.fieldnames:
            self.fieldnames.insert(0, "timestamp")

        # pre-check for existing header
        if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
            self._header_written = True
            self._bytes_written = os.path.getsize(self.path)

    def _write_event(self, event: dict[str, Any]) -> None:
        """
        Actual writing logic for appending a record to the CSV file with rotation.

        Args:
            record: Data to write.
        """
        if dirname := os.path.dirname(self.path):
            os.makedirs(dirname, exist_ok=True)

        # Check if we need to rotate before writing
        if self._bytes_written >= self.max_bytes:
            self._rotate_file()

        with open(self.path, "a", newline="", encoding="utf-8") as f:
            self._extracted_from__write_event_16(f, event)

    def _extracted_from__write_event_16(self, f, event):
        writer = csv.DictWriter(f, fieldnames=self.fieldnames)
        if self.write_header_once and not self._header_written:
            writer.writeheader()
            self._header_written = True

        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = datetime.now(UTC).isoformat(timespec="milliseconds") + "Z"

        # Write the row
        writer.writerow({k: event.get(k) for k in self.fieldnames})

        # Update byte counter (approximate)
        row_size = sum(len(str(v)) for v in event.values()) + len(self.fieldnames) * 2
        self._bytes_written += row_size

    def _rotate_file(self) -> None:
        """Rotate the CSV file similar to RotatingFileHandler."""
        if not os.path.exists(self.path):
            return

        try:
            # Find the next available rotation number
            for i in range(self.max_rotations - 1, -1, -1):
                rotated_path = f"{self.path}.{i}"
                if os.path.exists(rotated_path):
                    if i + 1 < self.max_rotations:
                        os.rename(rotated_path, f"{self.path}.{i + 1}")
                    else:
                        os.remove(rotated_path)  # Remove oldest rotated file

            # Rotate current file
            os.rename(self.path, f"{self.path}.1")

            # Reset state for new file
            self._header_written = False
            self._bytes_written = 0
        except OSError as e:
            # Rotation failed - log to stderr and continue without rotation
            # This prevents data loss if disk is full or permissions denied
            print(  # hil: allow-print
                f"WARNING: CSV rotation failed for {self.path}: {e}. "
                f"Continuing to append to existing file.",
                file=sys.stderr,
            )
            # Don't reset counters - keep appending to existing file


class JsonlWriter(BaseWriter):
    """
    JSONL writer for appending JSON objects line by line with rotation.
    """

    def __init__(
        self,
        path: str,
        max_bytes: int = 10 * 1024 * 1024,
        max_rotations: int = 3,
        schema: ParametersSchema | None = None,
    ) -> None:
        """
        Args:
            path: File path for the JSONL.
            max_bytes: Maximum file size before rotation.
            max_rotations: Maximum number of rotated files to keep (default 3).
            schema: Optional ParametersSchema for output validation.
        """
        super().__init__(schema=schema)
        self.path = path
        self.max_bytes = max_bytes
        self.max_rotations = max_rotations
        self._bytes_written = 0

        # Check existing file size
        if os.path.exists(self.path):
            self._bytes_written = os.path.getsize(self.path)

        if dirname := os.path.dirname(self.path):
            os.makedirs(dirname, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            os.fsync(f.fileno())

    def _write_event(self, event: dict[str, Any]) -> None:
        """
        Actual writing logic for appending a JSON object to the file with rotation.

        Args:
            event: JSON data to write.
        """
        if dirname := os.path.dirname(self.path):
            os.makedirs(dirname, exist_ok=True)

        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = datetime.now(UTC).isoformat(timespec="milliseconds") + "Z"

        # Check if we need to rotate before writing
        prepared_event = {"timestamp_write": time.time(), **event}
        json_str = json.dumps(prepared_event)
        json_line = json_str + "\n"
        if self._bytes_written + len(json_line.encode("utf-8")) >= self.max_bytes:
            self._rotate_file()

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json_line)
            f.flush()

        # Update byte counter
        self._bytes_written += len(json_line.encode("utf-8"))

    def _rotate_file(self) -> None:
        """Rotate the JSONL file similar to RotatingFileHandler."""
        if not os.path.exists(self.path):
            return

        try:
            # Find the next available rotation number
            for i in range(self.max_rotations - 1, -1, -1):
                rotated_path = f"{self.path}.{i}"
                if os.path.exists(rotated_path):
                    if i + 1 < self.max_rotations:
                        os.rename(rotated_path, f"{self.path}.{i + 1}")
                    else:
                        os.remove(rotated_path)  # Remove oldest rotated file

            # Rotate current file
            os.rename(self.path, f"{self.path}.1")

            # Reset byte counter
            self._bytes_written = 0
        except OSError as e:
            # Rotation failed - log to stderr and continue without rotation
            # This prevents data loss if disk is full or permissions denied
            print(  # hil: allow-print
                f"WARNING: JSONL rotation failed for {self.path}: {e}. "
                f"Continuing to append to existing file.",
                file=sys.stderr,
            )
            # Don't reset counter - keep appending to existing file
