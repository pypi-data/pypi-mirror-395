"""ProcessTracker: isolated active process lifecycle tracking.

Single responsibility: maintain in-memory registry of active command processes.
Logging of tracking events delegated to provided `TaskLogger`.
"""

from __future__ import annotations

from threading import Lock

from hil_testbench.run.logging.task_logger import LogLevel
from hil_testbench.run.session.process_state import ProcessInfo
from hil_testbench.run.session.process_state_store import ProcessEntry, ProcessStateStore


class ProcessTracker:
    """Tracks active processes for orphan cleanup.

    Methods are thread-safe. Persistence is delegated to `ProcessStateStore`.
    """

    # The tracker intentionally remains in-memory only; command specs are not
    # persisted or replayed across runs. Tracking focuses on active processes
    # for the current execution window.

    def __init__(self, logger, state_store: ProcessStateStore | None = None):
        self._logger = logger
        self._lock = Lock()
        self._active: dict[int, ProcessInfo] = {}
        self._state_store = state_store or ProcessStateStore(logger=logger)

    def track_start(
        self,
        command_name: str,
        pid: int,
        create_time: float,
        command_hash: str,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        *,
        spec_identity: dict[str, object] | None = None,
    ) -> None:
        """Record process start."""
        entry = ProcessInfo(
            pid=pid,
            command_name=command_name,
            command_hash=command_hash,
            create_time=create_time,
            host=host,
            port=port,
            username=username,
            spec_identity=spec_identity,
        )
        with self._lock:
            self._active[pid] = entry
        self._state_store.add(
            ProcessEntry(
                pid=pid,
                command_name=command_name,
                command_hash=command_hash,
                create_time=create_time,
                host=host,
                port=port,
                username=username,
                task=command_name,
                session_id=self._logger.get_correlation_id(),
                started_at=create_time,
                spec_identity=spec_identity,
            )
        )
        self._logger.log(
            "process_tracked",
            LogLevel.DEBUG,
            task=command_name,
            _pid=pid,
            _host=host or "local",
        )

    def track_end(self, command_name: str) -> None:
        """Record process end if tracked."""
        removed: list[ProcessInfo] = []
        with self._lock:
            target_pids = [
                pid for pid, proc in self._active.items() if proc.command_name == command_name
            ]
            for pid in target_pids:
                proc = self._active.pop(pid)
                removed.append(proc)
        if removed:
            for proc in removed:
                self._state_store.remove_by_pid(proc.pid)
                self._logger.log(
                    "process_untracked",
                    LogLevel.DEBUG,
                    task=command_name,
                    _pid=proc.pid,
                )

    def list_active_processes(self) -> list[ProcessInfo]:
        """Return snapshot list of active processes."""
        with self._lock:
            return list(self._active.values())
