"""Task configuration dataclass for structured task parameters."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import MISSING, dataclass, field, replace
from types import MappingProxyType
from typing import Any, cast

from hil_testbench.config.config_merger import merge_config_sources
from hil_testbench.config.run_config import RunConfig
from hil_testbench.data_structs.hosts import HostDefinition

_EMPTY_MAPPING: Mapping[str, Any] = MappingProxyType({})


def _deep_freeze_value(value: Any) -> Any:
    """Recursively convert mappings/sequences to immutable equivalents."""

    if isinstance(value, Mapping):
        # Reconstruct dict so nested dicts from callers are not shared.
        frozen = {key: _deep_freeze_value(inner) for key, inner in value.items()}
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze_value(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_deep_freeze_value(item) for item in value)
    return value


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if not data:
        return _EMPTY_MAPPING
    # Copy source mapping to break references even when already proxied.
    frozen = {key: _deep_freeze_value(value) for key, value in data.items()}
    return MappingProxyType(frozen)


def _merge_mapping_updates(
    base: Mapping[str, Any],
    *,
    updates: Mapping[str, Any] | None,
    removals: Iterable[str] | None,
) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    if removals:
        for key in removals:
            merged.pop(key, None)
    if updates:
        merged.update(updates)
    return merged


@dataclass(frozen=True, slots=True)
class TaskConfig:
    """Per-task execution configuration.

    Provides:
    - Task execution parameters (duration, interval)
    - Task-specific configuration (task_params dict)
    - Access to all configured hosts via run_config.hosts
    - Reference to global runner config

    Example task_params patterns:
        # Single host tasks:
        task_params["host_id"] = "server1"

        # Multi-host tasks:
        task_params["local_host"] = "localhost"
        task_params["remote_host"] = "server1"

        # Multi-interface testing:
        task_params["interface_pairs"] = [
            {"host": "support_server", "interfaces": ["eth0", "eth1"]},
            {"host": "backup_server", "interfaces": ["eth0", "eth1"]},
        ]
    """

    # Reserved keys that should not appear in task_params
    # These are framework execution parameters or CLI-specific flags
    RESERVED_KEYS = {
        # Execution control (TaskConfig fields)
        "duration",  # Task execution duration
        "interval",  # Polling/check interval
        "max_log_size_task",  # Task log rotation trigger
        "max_log_file_count_task",  # Task log rotation limit
        "max_data_size",  # Per-task data size limit
        "max_log_size_main",  # Main log rotation (RunConfig)
        "max_log_file_count_main",  # Main log rotation limit (RunConfig)
        # Health monitoring (RunConfig fields)
        "disable_health",  # Disable local host health checks
        "health_interval",  # Health check interval
        # Forced cleanup controls (RunConfig fields)
        "force_cleanup",  # Run forced cleanup after shutdown
        "pre_cleanup",  # Run forced cleanup before tasks start
        "force_cleanup_timeout",  # Trigger forced cleanup on slow shutdown
        "force_cleanup_mode",  # Hint for cleanup aggressiveness
        # CLI-specific flags (argparse)
        "config",  # YAML config file path (--config)
        "list",  # List available tasks (--list)
        "task",  # Positional task names argument
        "module",  # Internal: task module reference
        # Display configuration
        "display",  # Visualization/metrics config dict
    }

    # Common task execution parameters
    duration: str | None = None  # None = indefinite (runs until CTRL+C)
    interval: str = "5"
    password: str = ""
    # Per-task limits (moved from RunConfig)
    # When a log file reaches max size, it rotates (creates .1, .2, etc for long-running tasks)
    max_log_size_task_mb: int = 5  # Triggers rotation when task log hits this size
    max_log_file_count_task: int = 10  # Keep this many rotated task log files
    max_data_size_mb: int = 10
    # Task-specific configuration (from YAML tasks.<name> or CLI args)
    task_params: Mapping[str, Any] = field(default_factory=lambda: _EMPTY_MAPPING)

    # Reference to global runner config (includes hosts)
    run_config: RunConfig = field(default_factory=RunConfig)

    # Display configurations for metrics/visualization
    display: Mapping[str, Any] = field(default_factory=lambda: _EMPTY_MAPPING)

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_params", _freeze_mapping(self.task_params))
        object.__setattr__(self, "display", _freeze_mapping(self.display))

    def with_updates(self, **updates: Any) -> TaskConfig:
        if not updates:
            return self
        normalized = updates.copy()
        if "task_params" in normalized:
            normalized["task_params"] = _freeze_mapping(normalized["task_params"])
        if "display" in normalized:
            normalized["display"] = _freeze_mapping(normalized["display"])
        return cast(TaskConfig, replace(self, **normalized))

    def with_task_params_updates(
        self,
        *,
        updates: Mapping[str, Any] | None = None,
        removals: Iterable[str] | None = None,
    ) -> TaskConfig:
        """Return a copy with task_params merged immutably.

        Args:
            updates: Keys to add/replace in task_params.
            removals: Keys to drop from task_params.
        """

        if not updates and not removals:
            return self
        merged = _merge_mapping_updates(self.task_params, updates=updates, removals=removals)
        return self.with_updates(task_params=merged)

    def with_display_updates(
        self,
        *,
        updates: Mapping[str, Any] | None = None,
        removals: Iterable[str] | None = None,
    ) -> TaskConfig:
        """Return a copy with display overrides applied immutably."""

        if not updates and not removals:
            return self
        merged = _merge_mapping_updates(self.display, updates=updates, removals=removals)
        return self.with_updates(display=merged)

    # Convenience properties to access run config
    @property
    def max_log_size_main_mb(self) -> int:
        """Maximum log size for main runner in MB."""
        return self.run_config.max_log_size_main_mb

    @property
    def enable_runner_health(self) -> bool:
        """Whether local host health monitoring is enabled."""
        return self.run_config.enable_runner_health

    @property
    def runner_health_interval(self) -> int:
        """Local host health check interval in seconds."""
        return self.run_config.runner_health_interval

    def get_host(self, host_id: str) -> HostDefinition:
        """Get host configuration by ID from global run config.

        Example:
            server = config.get_host("server1")
            # Access directly: server.host, server.user, server.port
            # Or convert: server.as_string() -> "user@host:port"

        Returns:
            HostDefinition object (raises KeyError if not found)
        """
        if host_id == "localhost":
            # Localhost should work without explicit hosts config (FR-6.4)
            return HostDefinition(host="localhost", local=True)

        if host_dict := self.run_config.hosts.get(host_id):
            # Copy to plain dict for from_dict compatibility
            return HostDefinition.from_dict(dict(host_dict))

        raise KeyError(f"Host '{host_id}' not found in run config hosts.")

    def get_host_param(self, param_name: str) -> HostDefinition | None:
        """Get host from task_params by parameter name.

        Example:
            # For task_params["remote_host"] = "server1"
            remote = config.get_host_param("remote_host")

        Returns:
            HostDefinition object (or None if param not set or host not found)
        """
        host_id = self.task_params.get(param_name)
        return self.get_host(host_id) if host_id else None

    @classmethod
    def from_args(
        cls,
        args,
        top_defaults: dict[str, Any] | None = None,
        task_defaults: dict[str, Any] | None = None,
        run_config: RunConfig | None = None,
    ):
        """Create TaskConfig from argparse namespace and task-specific config.

        Args:
            args: Top-level CLI argparse namespace
            top_defaults: Top-level YAML defaults (yaml_data["defaults"])
            task_defaults: Task-specific YAML defaults (yaml_data["tasks"][task_name])
            run_config: Global RunConfig (must be provided with hosts already set)

        Returns:
            TaskConfig with all sources merged according to precedence rules.
        """
        top_defaults = top_defaults or {}
        task_defaults = task_defaults or {}

        # RunConfig must be provided by caller (from config_loader or manually created)
        if run_config is None:
            raise ValueError(
                "run_config is required. Use config_loader.load_project_config() "
                "to create RunConfig from YAML, then pass it to from_args()."
            )

        # Merge all config sources using centralized precedence rules
        default_map = {
            "duration": ("duration", None),
            "interval": ("interval", "5"),
            "max_log_size_task": ("max_log_size_task_mb", 5),
            "max_log_file_count_task": ("max_log_file_count_task", 10),
            "max_data_size": ("max_data_size_mb", 10),
        }

        def _field_default(name: str, fallback: Any) -> Any:
            field_info = cls.__dataclass_fields__[name]
            if field_info.default is not MISSING:
                return field_info.default
            if field_info.default_factory is not MISSING:
                factory = field_info.default_factory
                return cast(Callable[[], Any], factory)()
            return fallback

        program_defaults = {
            key: _field_default(field_name, fallback)
            for key, (field_name, fallback) in default_map.items()
        }
        merged = merge_config_sources(args, top_defaults, task_defaults, program_defaults)

        # Extract execution parameters from merged config
        duration_raw = merged.get("duration")  # None = indefinite duration
        duration = str(duration_raw) if duration_raw is not None else None
        interval = str(merged.get("interval", "5"))
        max_log_size_task_mb = int(merged.get("max_log_size_task", 5))
        max_log_file_count_task = int(merged.get("max_log_file_count_task", 10))
        max_data_size_mb = int(merged.get("max_data_size", 10))

        # Extract display config - use merged result which includes top-level defaults
        display = merged.get("display", {})

        # Build task_params from merged config (exclude reserved execution keys)
        task_params = {k: v for k, v in merged.items() if k not in cls.RESERVED_KEYS}

        return cls(
            duration=duration,
            interval=interval,
            max_log_size_task_mb=max_log_size_task_mb,
            max_log_file_count_task=max_log_file_count_task,
            max_data_size_mb=max_data_size_mb,
            task_params=task_params,
            run_config=run_config,
            display=display,
        )
