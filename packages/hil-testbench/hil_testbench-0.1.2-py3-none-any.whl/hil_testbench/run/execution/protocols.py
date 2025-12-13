"""Shared structural protocols for execution-layer integrations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

# TODO(long_running): Introduce a protocol describing the forthcoming
# streaming dispatcher interface so transports expose a single `stream` method
# that yields structured events derived from CommandSpec. Legacy stdout/stderr
# iterators should be marked deprecated once this protocol lands.

if TYPE_CHECKING:
    from hil_testbench.data_structs.parameters import ParametersSchema
    from hil_testbench.run.logging.task_logger import TaskLogger


class SSHTransportProtocol(Protocol):
    """Subset of Paramiko Transport interface used by ExecutionContext."""

    def getpeername(self) -> tuple[Any, ...]: ...

    def get_username(self) -> str | None: ...


class SSHClientProtocol(Protocol):
    """Structural typing contract for objects behaving like Paramiko SSHClient."""

    def exec_command(
        self,
        command: str,
        get_pty: bool = False,
    ) -> tuple[Any, Any, Any]: ...

    def get_transport(self) -> SSHTransportProtocol | None: ...


@runtime_checkable
class SupportsRenderFinal(Protocol):
    """Display backend that can render its final view via ``render_final``."""

    def render_final(self) -> None: ...

    def stop(self) -> None: ...


@runtime_checkable
class SupportsRenderableConsole(Protocol):
    """Display backend exposing a console + renderable factory."""

    console: Any

    def _create_renderable(self) -> Any: ...

    def stop(self) -> None: ...


@runtime_checkable
class SupportsTaskStatus(Protocol):
    """Display backend that can update task status information."""

    def update_task_status(
        self,
        task_name: str,
        status: str,
        *,
        start_time: float | None = None,
    ) -> None: ...


@runtime_checkable
class SupportsSchemaUpdates(Protocol):
    """Display backend that accepts schema updates per task."""

    def set_schema(self, task_name: str, schema: ParametersSchema) -> None: ...


@runtime_checkable
class SupportsCommandStatus(Protocol):
    """Display backend that tracks command-level status updates."""

    def update_command_status(
        self,
        task_name: str,
        command_name: str,
        status: str | None = None,
        *,
        lifecycle_status: str | None = None,
    ) -> None: ...


@runtime_checkable
class SupportsPrimaryParameterSummary(Protocol):
    """Display backend that can summarize primary parameter values."""

    def get_primary_parameter_summary(self) -> dict[str, tuple[Any, str | None]]: ...


@runtime_checkable
class SupportsLoggerBinding(Protocol):
    """Display backend capable of binding to a TaskLogger."""

    def bind_logger(self, logger: TaskLogger) -> None: ...


DisplayBackendProtocol = SupportsRenderFinal | SupportsRenderableConsole


__all__ = [
    "SSHTransportProtocol",
    "SSHClientProtocol",
    "SupportsRenderFinal",
    "SupportsRenderableConsole",
    "SupportsTaskStatus",
    "SupportsSchemaUpdates",
    "SupportsCommandStatus",
    "SupportsPrimaryParameterSummary",
    "SupportsLoggerBinding",
    "DisplayBackendProtocol",
]
