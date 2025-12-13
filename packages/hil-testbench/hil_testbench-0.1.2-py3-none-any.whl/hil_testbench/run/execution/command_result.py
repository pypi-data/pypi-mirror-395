from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from hil_testbench.run.execution.command_spec import CommandSpec

# Keywords indicating error messages in command output
_ERROR_KEYWORDS = (
    "error",
    "failed",
    "timeout",
    "refused",
    "denied",
    "unreachable",
    "exception",
    "not found",
)


class CommandStatus(Enum):
    """Command execution status lifecycle."""

    PENDING = "pending"  # Not yet started
    WAITING_DEPENDENCY = "waiting_dependency"  # Waiting for dependencies
    DELAYED_START = "delayed_start"  # In startup_delay period
    RUNNING = "running"  # Currently executing
    COMPLETED = "completed"  # Finished successfully
    FAILED = "failed"  # Execution or validation failed
    CANCELLED = "cancelled"  # Cancelled due to dependency failure
    STOPPED = "stopped"  # Stopped intentionally by framework (e.g., duration limit)


class CancellationClassification(Enum):
    """Different cancellation types to improve user messaging."""

    NONE = "none"
    USER = "user"
    DURATION_LIMIT = "duration_limit"


@dataclass
class CommandResult:
    """Result of a command execution."""

    command_name: str
    success: bool
    return_code: int
    spec: CommandSpec | None = None
    stdout: str = ""
    stderr: str = ""
    error: Exception | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration: float | None = None
    event_count: int = 0  # Number of parser events produced
    data_expected: bool = False  # Whether data output was expected
    status: CommandStatus = CommandStatus.PENDING  # Execution status
    status_message: str | None = None  # Additional status information
    task_name: str | None = None  # Task name this command belongs to
    cancelled: bool = False  # True when command terminated due to cancellation
    cancellation_classification: CancellationClassification | None = None
    long_running: bool | None = None  # Whether the originating spec marked this command persistent
    streaming_format: str | None = None  # Streaming format identifier from CommandSpec
    parser_id: str | None = None  # Optional parser factory identifier for diagnostics
    spec_identity: dict[str, Any] | None = None  # Serialized spec snapshot for downstream use
    exclusive: bool | None = None  # Whether command required exclusive scheduling per spec
    lifecycle_status: str | None = None  # String copy of CommandStatus for downstream consumers

    # The optional spec back-reference lets downstream components access the
    # declarative intent (streaming format, parser hints, etc.) without
    # recomputing metadata from command names or runtime heuristics.

    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"CommandResult(command='{self.command_name}', status={status}, code={self.return_code})"

    def __post_init__(self) -> None:
        if self.lifecycle_status is None and isinstance(self.status, CommandStatus):
            self.lifecycle_status = self.status.value

    def get_error_detail(self) -> str:
        """Extract the most actionable error detail from this command result.

        Searches in order:
        1. status_message (if set)
        2. error exception message
        3. stderr/stdout for lines containing error keywords
        4. First line of stderr/stdout
        5. Fallback message

        Returns:
            String describing what went wrong (max 200 chars)
        """
        if self.status_message:
            return self.status_message.strip()
        if self.error:
            return str(self.error).strip()[:200]

        for source in (self.stderr, self.stdout):
            text = (source or "").strip()
            if not text:
                continue
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if not lines:
                continue
            # Look for lines with error keywords first
            for line in lines:
                lowered = line.lower()
                if any(keyword in lowered for keyword in _ERROR_KEYWORDS):
                    return line[:200]
            # Fallback to first line
            return lines[0][:200]

        return "No error output captured"
