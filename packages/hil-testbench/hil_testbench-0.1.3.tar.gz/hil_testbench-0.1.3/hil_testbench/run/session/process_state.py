"""Process tracking data structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ProcessInfo:
    """Information about an active process for cleanup/verification.
    All fields are required for integrity checks during orphan cleanup.
    """

    pid: int
    command_name: str
    create_time: float  # Process creation time (epoch seconds)
    command_hash: str  # Hash of command string for verification
    host: str | None = None  # SSH host for remote processes
    port: int | None = None  # SSH port
    username: str | None = None  # SSH username (no password stored)
    spec_identity: dict[str, Any] | None = None  # Serializable CommandSpec snapshot
