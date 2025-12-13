"""Centralized process cleanup for local and remote entries."""

from __future__ import annotations

import os
import signal
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

import psutil

from hil_testbench.run.exceptions import ExecutionError
from hil_testbench.run.logging.task_logger import LogLevel, LogScope
from hil_testbench.run.session.process_state_store import ProcessEntry, ProcessStateStore


@dataclass(slots=True)
class CleanupStats:
    attempted: int = 0
    long_running: int = 0
    cleared: int = 0
    stale: int = 0
    skipped: int = 0
    failed: int = 0
    remaining: list[ProcessEntry] = field(default_factory=list)

    @property
    def unresolved(self) -> int:
        return len(self.remaining)


class ProcessCleanup:
    """Orchestrates cleanup of tracked processes."""

    def __init__(
        self,
        *,
        logger: Any,
        state_store: ProcessStateStore,
        cleanup_required: bool = False,
        cleanup_window_seconds: int | None = None,
    ) -> None:
        self._logger = logger
        self._state_store = state_store
        self._cleanup_required = cleanup_required
        self._lock = Lock()
        if cleanup_window_seconds is None:
            self._cleanup_window_seconds = None
        else:
            self._cleanup_window_seconds = max(int(cleanup_window_seconds), 0)

    def sweep_local(self) -> CleanupStats:
        with self._lock:
            return self._sweep_local_locked()

    def _sweep_local_locked(self) -> CleanupStats:
        stats = CleanupStats()
        for entry in self._iter_local_entries():
            stats.attempted += 1
            self._note_entry_metadata(entry, stats, stage="local")
            outcome = self._cleanup_local_entry(entry)
            self._apply_outcome(stats, entry, outcome)
        self._log_summary(stats, scope=LogScope.FRAMEWORK, stage="local")
        self._enforce_policy(stats, stage="local_cleanup")
        return stats

    def sweep_host(self, host: str, port: int, ssh_client: Any) -> CleanupStats:
        with self._lock:
            return self._sweep_host_locked(host, port, ssh_client)

    def _sweep_host_locked(self, host: str, port: int, ssh_client: Any) -> CleanupStats:
        normalized_host = self._normalize_host(host)
        peer_host = self._extract_remote_host(ssh_client)
        candidates = {normalized_host}
        if peer_host:
            candidates.add(self._normalize_host(peer_host))
        entries: list[ProcessEntry] = []
        for entry in self._state_store.list_entries():
            if not entry.host or (self._normalize_host(entry.host) not in candidates):
                continue
            if not self._within_window(entry):
                continue
            self._log_entry_considered(entry, stage=f"remote:{normalized_host}")
            entries.append(entry)
        stats = CleanupStats()
        for entry in entries:
            if entry.port and entry.port != port:
                continue
            stats.attempted += 1
            self._note_entry_metadata(entry, stats, stage=f"remote:{normalized_host}")
            outcome = self._cleanup_remote_entry(entry, ssh_client)
            self._apply_outcome(stats, entry, outcome)
        self._log_summary(stats, scope=LogScope.FRAMEWORK, stage=f"remote:{host}:{port}")
        self._enforce_policy(stats, stage=f"remote_cleanup:{host}:{port}")
        return stats

    def sweep_clients(self, clients: list[tuple[str, int, Any]]) -> CleanupStats:
        aggregate = CleanupStats()
        for host, port, client in clients:
            stats = self.sweep_host(host, port, client)
            aggregate.attempted += stats.attempted
            aggregate.cleared += stats.cleared
            aggregate.stale += stats.stale
            aggregate.skipped += stats.skipped
            aggregate.failed += stats.failed
            aggregate.long_running += stats.long_running
            aggregate.remaining.extend(stats.remaining)
        self._enforce_policy(aggregate, stage="shutdown_cleanup")
        return aggregate

    def _iter_local_entries(self) -> Iterable[ProcessEntry]:
        for entry in self._state_store.list_entries():
            if entry.host:
                continue
            if not self._within_window(entry):
                continue
            self._log_entry_considered(entry, stage="local")
            yield entry

    def _apply_outcome(self, stats: CleanupStats, entry: ProcessEntry, outcome: str) -> None:
        if outcome == "cleared":
            stats.cleared += 1
        elif outcome == "stale":
            stats.stale += 1
        elif outcome == "skipped":
            stats.skipped += 1
            stats.remaining.append(entry)
        elif outcome == "failed":
            stats.failed += 1
            stats.remaining.append(entry)

    # Internal helpers
    def _cleanup_local_entry(self, entry: ProcessEntry) -> str:
        pid = entry.pid
        proc_or_status = self._resolve_local_process(entry)
        if isinstance(proc_or_status, str):
            return proc_or_status
        proc = proc_or_status

        stale_status = self._prune_if_exited(proc, entry)
        if stale_status:
            return stale_status

        success = self._terminate_process_tree(proc)
        if success:
            self._state_store.remove_by_pid(pid)
            self._logger.log(
                "process_cleanup_killed",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                _host="local",
            )
            return "cleared"

        self._logger.log(
            "process_cleanup_failed",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            _pid=pid,
        )
        return "failed"

    def _resolve_local_process(self, entry: ProcessEntry) -> psutil.Process | str:
        pid = entry.pid
        if pid <= 1:
            self._logger.log(
                "process_cleanup_skipped",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="Skipping cleanup for reserved PID",
                _pid=pid,
            )
            return "skipped"
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            self._state_store.remove_by_pid(pid)
            self._logger.log(
                "process_cleanup_pruned",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                reason="not_found",
            )
            return "stale"
        except Exception as exc:  # pragma: no cover - defensive
            self._logger.log(
                "process_cleanup_probe_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                error=str(exc),
            )
            return "failed"

        if not self._same_identity(proc, entry):
            self._logger.log(
                "process_cleanup_skipped",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                message="PID reused or identity mismatch; leaving entry for review",
                _pid=pid,
            )
            return "skipped"
        return proc

    def _prune_if_exited(self, proc: psutil.Process, entry: ProcessEntry) -> str | None:
        if proc.is_running():
            return None
        self._state_store.remove_by_pid(entry.pid)
        self._logger.log(
            "process_cleanup_pruned",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            _pid=entry.pid,
            reason="exited",
        )
        return "stale"

    def _cleanup_remote_entry(self, entry: ProcessEntry, ssh_client: Any) -> str:
        pid = entry.pid
        try:
            if not self._probe_remote(ssh_client, pid):
                self._state_store.remove_by_pid(pid)
                self._logger.log(
                    "process_cleanup_pruned",
                    LogLevel.DEBUG,
                    scope=LogScope.FRAMEWORK,
                    _pid=pid,
                    _host=entry.host or "remote",
                    reason="not_found",
                )
                return "stale"
        except Exception as exc:  # pragma: no cover - defensive
            self._logger.log(
                "process_cleanup_probe_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                _host=entry.host or "remote",
                error=str(exc),
            )
            return "failed"

        # Identity check not available remotely; rely on PID+metadata.
        if not self._signal_remote(ssh_client, pid, "TERM"):
            return "failed"
        time.sleep(1.5)
        if not self._probe_remote(ssh_client, pid):
            self._state_store.remove_by_pid(pid)
            self._logger.log(
                "process_cleanup_killed",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                _host=entry.host or "remote",
                _signal="TERM",
            )
            return "cleared"

        self._signal_remote(ssh_client, pid, "KILL")
        time.sleep(0.5)
        if not self._probe_remote(ssh_client, pid):
            self._state_store.remove_by_pid(pid)
            self._logger.log(
                "process_cleanup_killed",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                _host=entry.host or "remote",
                _signal="KILL",
            )
            return "cleared"

        self._logger.log(
            "process_cleanup_failed",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            _pid=pid,
            _host=entry.host or "remote",
        )
        return "failed"

    def _terminate_process_tree(self, proc: psutil.Process) -> bool:
        try:
            procs = [proc] + proc.children(recursive=True)
            seen: dict[int, psutil.Process] = {}
            for p in procs:
                seen[p.pid] = p
            targets = list(seen.values())
            for p in targets:
                self._send_signal(p, signal.SIGTERM)
            _, alive = psutil.wait_procs(targets, timeout=3)
            if alive:
                for p in alive:
                    self._send_signal(
                        p, signal.SIGKILL if hasattr(signal, "SIGKILL") else signal.SIGTERM
                    )
                _, alive = psutil.wait_procs(alive, timeout=1.5)
            return not alive
        except Exception as exc:  # pragma: no cover - defensive
            self._logger.log(
                "process_cleanup_signal_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                error=str(exc),
            )
            return False

    def _send_signal(self, proc: psutil.Process, sig: signal.Signals) -> None:
        try:
            if os.name != "nt" and sig in (
                signal.SIGTERM,
                getattr(signal, "SIGKILL", signal.SIGTERM),
            ):
                try:
                    os.killpg(proc.pid, sig)
                    return
                except Exception:
                    pass
            proc.send_signal(sig)
        except Exception:
            pass

    def _probe_remote(self, ssh_client: Any, pid: int) -> bool:
        stdin, stdout, stderr = ssh_client.exec_command(f"kill -0 -- -{pid} 2>/dev/null || exit 1")
        self._close_ssh_stream(stdin)
        self._drain_ssh_stream(stderr)
        return stdout.channel.recv_exit_status() == 0

    def _signal_remote(self, ssh_client: Any, pid: int, sig: str) -> bool:
        try:
            stdin, stdout, stderr = ssh_client.exec_command(
                f"kill -{sig} -- -{pid} 2>/dev/null || true"
            )
            self._close_ssh_stream(stdin)
            self._drain_ssh_stream(stdout)
            self._drain_ssh_stream(stderr)
            return True
        except Exception as exc:  # pragma: no cover - defensive
            self._logger.log(
                "process_cleanup_signal_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                _pid=pid,
                _signal=sig,
                error=str(exc),
            )
            return False

    def _same_identity(self, proc: psutil.Process, entry: ProcessEntry) -> bool:
        try:
            create_time = proc.create_time()
        except Exception:
            return False
        if abs(create_time - entry.create_time) > 1.0:
            return False
        if entry.username:
            try:
                if proc.username() != entry.username:
                    return False
            except Exception:
                return False
        return True

    def _log_summary(self, stats: CleanupStats, *, scope: LogScope, stage: str) -> None:
        self._logger.log(
            "process_cleanup_summary",
            LogLevel.DEBUG if stats.unresolved == 0 else LogLevel.WARNING,
            scope=scope,
            stage=stage,
            attempted=stats.attempted,
            cleared=stats.cleared,
            stale=stats.stale,
            skipped=stats.skipped,
            failed=stats.failed,
            long_running_attempted=stats.long_running,
            remaining=stats.unresolved,
        )

    def _enforce_policy(self, stats: CleanupStats, *, stage: str) -> None:
        if not self._cleanup_required or stats.unresolved == 0:
            return
        raise ExecutionError(
            "Cleanup required but leftover processes remain",
            context={
                "stage": stage,
                "remaining": stats.unresolved,
            },
        )

    def _within_window(self, entry: ProcessEntry) -> bool:
        window = self._cleanup_window_seconds
        if window is None:
            return True
        timestamp = entry.started_at or entry.create_time
        if timestamp is None:
            return True
        now = time.time()
        age = float(now - float(timestamp))
        session_label = entry.session_id or entry.command_name or str(entry.pid)
        if age < 0:
            self._logger.log(
                "process_cleanup_future_entry",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                session_id=session_label,
                _pid=entry.pid,
                message="Entry timestamp is in the future; ignored",
            )
            return False
        if age > window:
            self._logger.log(
                "process_cleanup_outside_window",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                session_id=session_label,
                _pid=entry.pid,
                message="Entry outside cleanup window; skipped",
                age_seconds=int(age),
                window_seconds=int(window),
            )
            return False
        return True

    def _extract_spec_long_running(self, entry: ProcessEntry) -> bool | None:
        identity = entry.spec_identity
        if isinstance(identity, dict):
            raw = identity.get("long_running")
            if isinstance(raw, bool):
                return raw
            if isinstance(raw, str):
                lowered = raw.strip().lower()
                if lowered in {"true", "yes", "1"}:
                    return True
                if lowered in {"false", "no", "0"}:
                    return False
        return None

    def _note_entry_metadata(self, entry: ProcessEntry, stats: CleanupStats, *, stage: str) -> None:
        is_long_running = self._extract_spec_long_running(entry)
        if is_long_running:
            stats.long_running += 1
            self._logger.log(
                "process_cleanup_long_running",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                stage=stage,
                _pid=entry.pid,
                command=entry.command_name,
                message="Enforcing cleanup for long-running command",
            )

    def _log_entry_considered(self, entry: ProcessEntry, *, stage: str) -> None:
        session_label = entry.session_id or entry.command_name or str(entry.pid)
        self._logger.log(
            "process_cleanup_considered",
            LogLevel.DEBUG,
            scope=LogScope.FRAMEWORK,
            stage=stage,
            session_id=session_label,
            _pid=entry.pid,
            message="Entry considered for cleanup",
        )

    @staticmethod
    def _normalize_host(host: str) -> str:
        cleaned = host
        if "@" in cleaned:
            cleaned = cleaned.split("@", 1)[1]
        if ":" in cleaned:
            cleaned = cleaned.split(":", 1)[0]
        return cleaned

    @staticmethod
    def _extract_remote_host(ssh_client: Any) -> str | None:
        try:
            transport = ssh_client.get_transport()
            if transport:
                peer = transport.getpeername()
                if peer and isinstance(peer, (list, tuple)) and peer:
                    return str(peer[0])
        except Exception:
            return None
        return None

    @staticmethod
    def _close_ssh_stream(stream: Any) -> None:
        if not stream:
            return
        try:
            stream.close()
        except Exception:
            pass

    @staticmethod
    def _drain_ssh_stream(stream: Any) -> None:
        if not stream:
            return
        try:
            stream.read()
        except Exception:
            pass
        finally:
            ProcessCleanup._close_ssh_stream(stream)


__all__ = ["CleanupStats", "ProcessCleanup"]
