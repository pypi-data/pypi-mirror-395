"""Run configuration for the task executor."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, cast


def _empty_mapping() -> Mapping[str, Any]:
    return MappingProxyType({})


def _freeze_hosts(hosts: Mapping[str, Mapping[str, Any]] | None) -> Mapping[str, Mapping[str, Any]]:
    if not hosts:
        return MappingProxyType({})
    if isinstance(hosts, MappingProxyType):
        return hosts
    frozen: dict[str, Mapping[str, Any]] = {}
    for name, host_cfg in hosts.items():
        if isinstance(host_cfg, MappingProxyType):
            frozen[name] = host_cfg
        else:
            frozen[name] = MappingProxyType(dict(host_cfg))
    return MappingProxyType(frozen)


@dataclass(frozen=True, slots=True)
class RunConfig:
    """Global runner configuration (applies to all tasks in a run)."""

    # Logging configuration (global/main only)
    # When a log file reaches max size, it rotates (creates .1, .2, etc for long-running programs)
    max_log_size_main_mb: int = 10  # Triggers rotation when main log hits this size
    max_log_file_count_main: int = 10  # Keep this many rotated main log files
    max_log_size_task_mb: int = 5  # Triggers rotation when per-task log hits this size
    max_log_file_count_task: int = 10  # Keep this many rotated per-task log files
    log_level: str = "INFO"  # Console output level: DEBUG, INFO, WARNING, ERROR
    log_level_file: str = "DEBUG"  # File logging level
    log_dir: str = "logs"  # Root log directory override
    no_color: bool = False  # Disable colored console output
    json_console: bool = False  # Emit structured JSON to console
    quiet_errors_only: bool = False  # Console prints only ERROR/CRITICAL

    # Local host health monitoring (TaskRunner machine only)
    # Tracks CPU, memory, disk space, thread count for the local process host.
    # Remote SSH hosts are NOT monitored.
    enable_runner_health: bool = True
    runner_health_interval: int = 600
    health_cpu_threshold: float = 80.0
    health_memory_threshold: float = 85.0
    health_disk_threshold_gb: float = 10.0

    # PTY settings
    disable_pty: bool = False  # Set True to force subprocess mode (useful with VS Code ConPTY)

    # Signal handling / shutdown tuning
    signal_force_grace_seconds: float = 10.0

    # SSH retry policy (connection establishment only)
    ssh_connection_max_retries: int = 3
    ssh_connection_retry_delay: float = 1.0

    # Cleanup settings
    no_cleanup: bool = False  # Skip process cleanup entirely (not recommended)
    state_dir: str | None = None  # Persistent state directory override
    cleanup_window_seconds: int = 24 * 3600  # Default 24h cleanup window
    shell_wrapper_mode: str = "auto"  # auto|on|off wrapper default
    force_cleanup: bool = False  # Force forced-cleanup pass after shutdown
    pre_cleanup: bool = False  # Run forced cleanup before tasks start
    force_cleanup_timeout: float = 5.0  # Trigger forced cleanup if shutdown exceeds this timeout
    force_cleanup_mode: str = "strict"  # graceful|strict|aggressive hint for forced cleanup

    # Log directory management
    # By default, pruning is disabled - only a suggestion is shown when limits are exceeded
    # Enable auto_prune to automatically delete old directories on startup
    max_log_dirs: int = 50  # Keep N most recent execution directories (0 = unlimited)
    max_log_age_days: int = 30  # Delete directories older than N days (0 = unlimited)
    auto_prune: bool = False  # Enable automatic log directory pruning (default: disabled)
    # Cleanup gating
    cleanup_required: bool = False  # Fail fast if cleanup cannot clear leftovers

    # Infrastructure: all configured hosts
    # Format: {"server1": {"host": "110.212.30.100", "user": "my_user", ...}, ...}
    hosts: Mapping[str, Mapping[str, Any]] = field(default_factory=_empty_mapping)

    # Adaptive pipeline buffering (affects event flush timing for live display)
    event_buffer_max: int = 50  # Flush when buffered events reach this count
    event_max_age_ms: int = 500  # Flush if oldest buffered event exceeds this age (ms)
    event_dynamic_field_cap: int = 500  # Limit dynamically discovered parameters

    # Daemon mode: run in background with minimal output
    daemon_mode: bool = False

    # Path to loaded config file (for logging/debugging)
    loaded_config_path: str | None = None

    # Internal flag to avoid duplicate log directory suggestions within a run

    def __post_init__(self) -> None:
        object.__setattr__(self, "hosts", _freeze_hosts(self.hosts))

    def with_updates(self, **updates: Any) -> RunConfig:
        if not updates:
            return self
        normalized = updates.copy()
        if "hosts" in normalized:
            normalized["hosts"] = _freeze_hosts(normalized["hosts"])
        return cast(RunConfig, replace(self, **normalized))

    @classmethod
    def from_yaml(cls, yaml_data: dict[str, Any]) -> RunConfig:
        """Create RunConfig from YAML configuration dict.

        Example YAML structure:
            defaults:
              max_log_size_main_mb: 20
              max_log_file_count_main: 10
              log_level: "INFO"
            hosts:
              server1:
                host: 110.212.30.100
                user: my_user
                port: 22

        Args:
            yaml_data: Loaded YAML dict (typically from yaml.safe_load())

        Returns:
            RunConfig with values from YAML defaults section and hosts
        """
        defaults = yaml_data.get("defaults", {})
        hosts_section = yaml_data.get("hosts")
        hosts = hosts_section if hosts_section else {"localhost": {"host": "localhost"}}

        return cls(
            hosts=hosts,
            max_log_size_main_mb=defaults.get("max_log_size_main_mb", 10),
            max_log_file_count_main=defaults.get("max_log_file_count_main", 10),
            log_level=defaults.get("log_level", "INFO").upper(),
            log_level_file=str(defaults.get("log_level_file", "DEBUG")).upper(),
            log_dir=defaults.get("log_dir", "logs"),
            no_color=defaults.get("no_color", False),
            json_console=defaults.get("json_console", False),
            quiet_errors_only=defaults.get("quiet_errors_only", False),
            enable_runner_health=defaults.get("enable_runner_health", True),
            runner_health_interval=defaults.get("runner_health_interval", 600),
            health_cpu_threshold=float(defaults.get("health_cpu_threshold", 80.0)),
            health_memory_threshold=float(defaults.get("health_memory_threshold", 85.0)),
            health_disk_threshold_gb=float(defaults.get("health_disk_threshold_gb", 10.0)),
            disable_pty=defaults.get("disable_pty", False),
            signal_force_grace_seconds=float(defaults.get("signal_force_grace_seconds", 10.0)),
            ssh_connection_max_retries=int(defaults.get("ssh_connection_max_retries", 3)),
            ssh_connection_retry_delay=float(defaults.get("ssh_connection_retry_delay", 1.0)),
            no_cleanup=defaults.get("no_cleanup", False),
            state_dir=defaults.get("state_dir"),
            cleanup_window_seconds=int(
                defaults.get("cleanup_window_seconds", 24 * 3600)
                if defaults.get("cleanup_window_seconds") is not None
                else 24 * 3600
            ),
            shell_wrapper_mode=str(defaults.get("shell_wrapper_mode", "auto")).lower(),
            force_cleanup=defaults.get("force_cleanup", False),
            pre_cleanup=defaults.get("pre_cleanup", False),
            force_cleanup_timeout=float(defaults.get("force_cleanup_timeout", 5.0)),
            force_cleanup_mode=str(defaults.get("force_cleanup_mode", "strict")),
            cleanup_required=defaults.get("cleanup_required", False),
            max_log_dirs=defaults.get("max_log_dirs", 50),
            max_log_age_days=defaults.get("max_log_age_days", 30),
            auto_prune=defaults.get("auto_prune", False),
            event_buffer_max=defaults.get("event_buffer_max", 50),
            event_max_age_ms=defaults.get("event_max_age_ms", 500),
            daemon_mode=defaults.get("daemon_mode", False),
            event_dynamic_field_cap=defaults.get("event_dynamic_field_cap", 500),
        )
