"""Centralized process state store.

Maintains a single process_state.json with atomic updates and basic
corruption handling. This store is the source of truth for cleanup
and orphan detection across runs.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from threading import Lock
from typing import Any

from hil_testbench.run.logging.task_logger import LogLevel

STATE_VERSION = 1


def _default_state_dir() -> str:
    """Return default state directory path (~/.hil_testbench/state)."""
    env_override = os.getenv("HIL_STATE_DIR")
    if env_override:
        return os.path.abspath(env_override)
    xdg = os.getenv("XDG_STATE_HOME")
    if xdg:
        return os.path.join(os.path.abspath(xdg), "hil_testbench")
    home = os.path.expanduser("~")
    return os.path.join(home, ".hil_testbench", "state")


@dataclass(slots=True)
class ProcessEntry:
    pid: int
    create_time: float
    command_hash: str
    command_name: str
    task: str | None = None
    session_id: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    started_at: float | None = None
    cmd_preview: str | None = None
    platform: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    spec_identity: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProcessEntry:
        """Create ProcessEntry from dict, ignoring unknown fields."""
        known = {field.name for field in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered: dict[str, Any] = {}
        extras: dict[str, Any] = {}
        for key, value in data.items():
            if key in known:
                filtered[key] = value
            else:
                extras[key] = value
        filtered.setdefault("extra", extras)
        return cls(**filtered)


class ProcessStateStore:
    """Thread-safe, atomic process state persistence."""

    def __init__(self, path: str | None = None, *, logger: Any | None = None) -> None:
        self._path = path or os.path.join(_default_state_dir(), "process_state.json")
        self._lock = Lock()
        self._logger = logger
        self._state: dict[str, Any] = {
            "version": STATE_VERSION,
            "updated_at": "",
            "entries": [],
        }
        self._ensure_dir()
        self._load()

    # Public API
    def add(self, entry: ProcessEntry) -> None:
        with self._lock:
            entries = self._state.get("entries", [])
            entries = [e for e in entries if not self._same_identity_dict(e, entry)]
            entries.append(asdict(entry))
            self._state["entries"] = entries
            self._state["version"] = STATE_VERSION
            self._state["updated_at"] = self._now_iso()
            self._persist_locked()

    def remove_by_pid(self, pid: int) -> None:
        with self._lock:
            entries = self._state.get("entries", [])
            new_entries = [e for e in entries if int(e.get("pid", -1)) != int(pid)]
            if len(new_entries) == len(entries):
                return
            self._state["entries"] = new_entries
            self._state["updated_at"] = self._now_iso()
            self._persist_locked()

    def list_entries(self) -> list[ProcessEntry]:
        with self._lock:
            raw_entries = list(self._state.get("entries", []))
        entries: list[ProcessEntry] = []
        for raw in raw_entries:
            if not isinstance(raw, dict):
                continue
            try:
                entries.append(ProcessEntry.from_dict(raw))
            except Exception:
                continue
        return entries

    def find_by_predicate(self, predicate: Callable[[ProcessEntry], bool]) -> list[ProcessEntry]:
        """Return entries matching the predicate; ignores predicate failures."""

        matches: list[ProcessEntry] = []
        for entry in self.list_entries():
            try:
                if predicate(entry):
                    matches.append(entry)
            except Exception:
                continue
        return matches

    # Internal helpers
    def _ensure_dir(self) -> None:
        try:
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
        except Exception as exc:  # pragma: no cover - defensive
            self._log_warning("state_dir_create_failed", error=str(exc))

    def _load(self) -> None:
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path, encoding="utf-8") as handle:
                raw = json.load(handle)
            if isinstance(raw, dict) and "entries" in raw:
                self._state = raw
        except Exception as exc:  # pragma: no cover - defensive
            self._backup_corrupt_file(exc)
            self._state = {"version": STATE_VERSION, "updated_at": "", "entries": []}

    def _persist_locked(self) -> None:
        data = self._state
        directory = os.path.dirname(self._path)
        try:
            fd, tmp_path = tempfile.mkstemp(prefix=".process_state.", dir=directory)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, self._path)
            try:
                dir_fd = os.open(directory, os.O_DIRECTORY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
            except Exception:
                pass
        except Exception as exc:  # pragma: no cover - defensive
            self._log_warning("state_persist_failed", error=str(exc))

    def _backup_corrupt_file(self, exc: Exception) -> None:
        try:
            ts = int(time.time())
            backup_path = f"{self._path}.corrupt.{ts}"
            os.replace(self._path, backup_path)
            self._log_warning(
                "state_file_corrupt",
                error=str(exc),
                backup=backup_path,
            )
        except Exception:
            self._log_warning("state_backup_failed", error=str(exc))

    def _log_warning(self, event: str, **fields: Any) -> None:
        logger = self._logger
        if not logger:
            return
        try:
            logger.log(event, LogLevel.WARNING, **fields)
        except Exception:
            # Best-effort logging; never raise.
            pass

    @staticmethod
    def _now_iso() -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @staticmethod
    def _same_identity_dict(existing: dict[str, Any], entry: ProcessEntry) -> bool:
        try:
            pid_match = int(existing.get("pid", -1)) == entry.pid
            create = float(existing.get("create_time", -1.0))
            time_match = abs(create - entry.create_time) <= 0.001
            return pid_match and time_match
        except Exception:
            return False


__all__ = ["ProcessEntry", "ProcessStateStore"]
