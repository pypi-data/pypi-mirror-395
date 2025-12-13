"""Command specification declarations for the execution layer."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, cast

from hil_testbench.data_processing.events import CommandOutputCallbackFactory

_EMPTY_MAPPING: Mapping[str, str] = MappingProxyType({})


def _freeze_env(env: Mapping[str, str] | None) -> Mapping[str, str]:
    if not env:
        return _EMPTY_MAPPING
    if isinstance(env, MappingProxyType):
        return env
    return MappingProxyType(dict(env))


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Immutable command specification consumed by the execution layer."""

    command_name: str
    task_name: str
    long_running: bool = False
    streaming_format: str | None = None
    parser_factory: Callable[[], Any] | None = None
    shell_wrapper_mode: str | None = None
    use_pty: bool | None = None
    immediate: bool = False
    host: Any | None = None
    env: Mapping[str, str] = field(default_factory=lambda: _EMPTY_MAPPING)
    cwd: str | None = None
    tags: tuple[str, ...] = ()
    retry: int = 0
    exclusive: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "env", _freeze_env(self.env))
        object.__setattr__(self, "tags", tuple(self.tags))

    def with_updates(self, **updates: Any) -> CommandSpec:
        if not updates:
            return self
        normalized = updates.copy()
        if "env" in normalized:
            normalized["env"] = _freeze_env(normalized.get("env"))
        if "tags" in normalized and normalized["tags"] is not None:
            normalized["tags"] = tuple(normalized["tags"])
        return cast(CommandSpec, replace(self, **normalized))

    def identity(self) -> dict[str, Any]:
        """Return a serializable identity snapshot for auditing."""

        host_value = self.host
        if host_value is not None and not isinstance(host_value, (str, int, float, bool)):
            host_value = repr(host_value)

        return {
            "command_name": self.command_name,
            "task_name": self.task_name,
            "long_running": self.long_running,
            "streaming_format": self.streaming_format,
            "shell_wrapper_mode": self.shell_wrapper_mode,
            "use_pty": self.use_pty,
            "immediate": self.immediate,
            "host": host_value,
            "env": dict(self.env),
            "cwd": self.cwd,
            "tags": list(self.tags),
            "retry": self.retry,
            "exclusive": self.exclusive,
        }


@dataclass(frozen=True, slots=True)
class PreparedEntry:
    """Prepared command execution entry produced by CommandPreparer."""

    func: Callable[..., Any]
    spec: CommandSpec
    callback_factory: CommandOutputCallbackFactory | None = None


__all__ = ["CommandSpec", "PreparedEntry"]
