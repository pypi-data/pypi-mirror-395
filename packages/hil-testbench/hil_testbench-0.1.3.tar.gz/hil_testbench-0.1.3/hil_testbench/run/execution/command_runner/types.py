"""Dataclasses and shared types for the command runner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from hil_testbench.run.execution.command_spec import CommandSpec


@dataclass(slots=True)
class CommandRunnerSettings:
    """Settings bundle for CommandRunner to keep __init__ signature small."""

    max_workers: int = 10
    verbose: bool = True
    log_dir: str = "logs"
    max_bytes_main: int = 10 * 1024 * 1024
    max_bytes_task: int = 5 * 1024 * 1024
    max_log_file_count_main: int = 10
    max_log_file_count_task: int = 10
    enable_health_logging: bool = True
    health_interval: int = 600
    health_cpu_threshold: float = 80.0
    health_memory_threshold: float = 85.0
    health_disk_threshold_gb: float = 10.0
    signal_force_grace_seconds: float = 10.0
    ssh_max_retries: int = 3
    ssh_retry_delay: float = 1.0
    shell_wrapper_mode: str = "auto"
    forced_cleanup_timeout: float = 5.0


@dataclass(slots=True)
class ExecutionParams:
    """Per-task execution settings for _execute_task."""

    spec: CommandSpec
    password: str | None = None
    allow_agent: bool = False
    look_for_keys: bool = True
    log_output: bool | None = None
    sample_lines: int = 0
    task_name: str | None = None
    remote_os: Literal["unix", "windows"] = "unix"
    host: str | None = None
    port: int = 22
    use_pty: bool | None = None
    shell_wrapper_mode: str | None = None

    def __post_init__(self) -> None:
        if self.host is None:
            host_value = self.spec.host
            if host_value is None:
                resolved_host = None
            elif isinstance(host_value, str):
                resolved_host = host_value
            else:
                resolved_host = str(host_value)
            object.__setattr__(self, "host", resolved_host)
        if self.shell_wrapper_mode is None:
            wrapper = self.spec.shell_wrapper_mode or "auto"
            object.__setattr__(self, "shell_wrapper_mode", wrapper)
        if self.use_pty is None:
            spec_use_pty = self.spec.use_pty
            resolved = bool(spec_use_pty) if spec_use_pty is not None else False
            object.__setattr__(self, "use_pty", resolved)


__all__ = [
    "CommandRunnerSettings",
    "ExecutionParams",
]
