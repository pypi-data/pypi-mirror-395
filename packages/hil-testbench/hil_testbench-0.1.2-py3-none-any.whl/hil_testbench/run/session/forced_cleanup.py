"""Forced cleanup executor independent of PID tracking."""

from __future__ import annotations

import contextlib
import os
import shlex
import signal
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import psutil

from hil_testbench.data_structs.hosts import HostDefinition
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.task.cleanup_spec import CleanupSpec


@dataclass(frozen=True, slots=True)
class ForcedCleanupPlanEntry:
    """Represents cleanup spec plus hosts to apply it to."""

    task_name: str
    spec: CleanupSpec
    hosts: tuple[HostDefinition | None, ...]


@dataclass(frozen=True, slots=True)
class OrphanMatch:
    """Captured orphan match details for logging."""

    task_name: str
    host: str | None
    pids: tuple[int, ...]
    patterns: tuple[str, ...]
    ports: tuple[int, ...]


class OrphanDetector:
    """Detect (but do not terminate) orphan processes that match cleanup specs."""

    def __init__(self, *, logger: TaskLogger, ssh_manager: Any | None) -> None:
        self._logger = logger
        self._ssh_manager = ssh_manager

    def detect(self, plan: dict[str, ForcedCleanupPlanEntry]) -> list[OrphanMatch]:
        findings: list[OrphanMatch] = []
        if not plan:
            return findings

        for entry in plan.values():
            spec = entry.spec
            if spec is None or spec.is_empty():
                continue
            hosts = entry.hosts or (None,)
            for host in hosts:
                if host is None or host.local:
                    match = self._detect_local(entry)
                else:
                    match = self._detect_remote(entry, host)
                if match:
                    findings.append(match)
        return findings

    def _detect_local(self, entry: ForcedCleanupPlanEntry) -> OrphanMatch | None:
        spec = entry.spec
        pids: set[int] = set()
        pattern_hits: set[str] = set()
        port_hits: set[int] = set()

        search_patterns = set(spec.patterns)
        for command in spec.commands:
            head = (command or "").split()
            if head:
                search_patterns.add(head[0])

        if search_patterns:
            for proc in psutil.process_iter(attrs=["pid", "cmdline", "name"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    name = proc.info.get("name") or ""
                    haystack = f"{name} {cmdline}".strip()
                    for pattern in search_patterns:
                        if pattern and pattern in haystack:
                            pids.add(proc.pid)
                            pattern_hits.add(pattern)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        if spec.ports:
            # Some psutil versions reject "connections" in attrs; request pid only.
            for proc in psutil.process_iter(attrs=["pid"]):
                try:
                    for conn in proc.net_connections(kind="inet"):
                        if conn.laddr and conn.laddr.port in spec.ports:
                            pids.add(proc.pid)
                            port_hits.add(conn.laddr.port)
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    continue

        if not pids:
            return None

        return OrphanMatch(
            task_name=entry.task_name,
            host=None,
            pids=tuple(sorted(pids)),
            patterns=tuple(sorted(pattern_hits))
            if pattern_hits
            else tuple(sorted(search_patterns)),
            ports=tuple(sorted(port_hits)) if port_hits else tuple(spec.ports),
        )

    def _detect_remote(
        self, entry: ForcedCleanupPlanEntry, host: HostDefinition
    ) -> OrphanMatch | None:
        if self._ssh_manager is None:
            self._logger.log(
                "orphan_detection_remote_skipped",
                LogLevel.DEBUG,
                scope=LogScope.FRAMEWORK,
                task=entry.task_name,
                host=host.as_string(),
                message="SSH manager unavailable; skipping remote orphan detection",
            )
            return None
        try:
            client = self._ssh_manager.get_client(
                host.as_string(),
                host.port,
                host.password or None,
                command_name=entry.task_name,
                allow_agent=host.allow_agent,
                look_for_keys=host.look_for_keys,
            )
        except Exception:  # pragma: no cover - best effort
            return None

        script = self._build_remote_detection_script(entry.spec)
        try:
            stdin, stdout, stderr = client.exec_command(script, timeout=5.0)
            if stdin:
                with contextlib.suppress(Exception):
                    stdin.close()
            stdout_text = (stdout.read() or b"").decode("utf-8", errors="replace")
            stderr_text = (stderr.read() or b"").decode("utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover - best effort
            self._logger.log(
                "orphan_detection_remote_failed",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=entry.task_name,
                host=host.as_string(),
                error=str(exc),
                error_type=type(exc).__name__,
            )
            return None

        pids: set[int] = set()
        pattern_hits: set[str] = set()
        port_hits: set[int] = set()

        for raw_line in (stdout_text + "\n" + stderr_text).splitlines():
            line = raw_line.strip()
            if not line or not line.startswith("__ORPHAN__"):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            _, kind, label, pid_text = parts[:4]
            try:
                pid = int(pid_text)
            except ValueError:
                continue
            pids.add(pid)
            if kind == "pattern":
                pattern_hits.add(label)
            elif kind == "port":
                with contextlib.suppress(ValueError):
                    port_hits.add(int(label))

        if not pids:
            return None

        return OrphanMatch(
            task_name=entry.task_name,
            host=host.as_string(),
            pids=tuple(sorted(pids)),
            patterns=tuple(sorted(pattern_hits)) if pattern_hits else tuple(entry.spec.patterns),
            ports=tuple(sorted(port_hits)) if port_hits else tuple(entry.spec.ports),
        )

    @staticmethod
    def _build_remote_detection_script(spec: CleanupSpec) -> str:
        parts: list[str] = []
        for pattern in spec.patterns:
            safe = shlex.quote(pattern)
            parts.append(
                f"pgrep -f {safe} 2>/dev/null | xargs -r -n1 printf '__ORPHAN__ pattern {pattern} %s\\n' || true"
            )
        for command in spec.commands:
            head = (command or "").split()
            if not head:
                continue
            safe_head = shlex.quote(head[0])
            parts.append(
                f"pgrep -f {safe_head} 2>/dev/null | xargs -r -n1 printf '__ORPHAN__ pattern {head[0]} %s\\n' || true"
            )
        for port in spec.ports:
            parts.append(
                f"fuser -n tcp {port} 2>/dev/null | xargs -r -n1 printf '__ORPHAN__ port {port} %s\\n' || true"
            )
        return "; ".join(parts) or "true"


class ForcedCleanupExecutor:
    """Execute forced cleanup actions when PID tracking cannot cover remaining processes."""

    def __init__(
        self,
        *,
        logger: TaskLogger,
        ssh_manager: Any | None,
        timeout_seconds: float = 5.0,
    ) -> None:
        self._logger = logger
        self._ssh_manager = ssh_manager
        self._timeout = float(timeout_seconds)

    def execute(self, plan: dict[str, ForcedCleanupPlanEntry], *, reason: str) -> None:
        if not plan:
            return
        handled = False
        for entry in plan.values():
            spec = entry.spec
            if spec is None or spec.is_empty():
                continue
            hosts = entry.hosts or (None,)
            for host in hosts:
                if host is None or host.local:
                    self._cleanup_local(entry, reason)
                else:
                    self._cleanup_remote(entry, host, reason)
                handled = True
        if not handled:
            self._logger.log(
                "forced_cleanup_no_targets",
                LogLevel.INFO,
                scope=LogScope.FRAMEWORK,
                message="Forced cleanup plan contained no actionable targets",
                reason=reason,
            )

    def _cleanup_local(self, entry: ForcedCleanupPlanEntry, reason: str) -> None:
        spec = entry.spec
        killed: set[int] = set()

        for port in spec.ports:
            killed.update(self._terminate_port_processes(port, entry.task_name, reason))

        for pattern in spec.patterns:
            killed.update(self._terminate_pattern_processes(pattern, entry.task_name, reason))

        for command in spec.commands:
            self._execute_local_command(command, entry.task_name, reason)

        self._logger.log(
            "forced_cleanup_local",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            task=entry.task_name,
            message="Forced cleanup executed (local)",
            reason=reason,
            patterns=list(spec.patterns),
            ports=list(spec.ports),
            commands=list(spec.commands),
            terminated=list(sorted(killed)),
            mode=spec.mode,
        )

    def _terminate_pattern_processes(self, pattern: str, task: str, reason: str) -> set[int]:
        matched: list[psutil.Process] = []
        for proc in psutil.process_iter(attrs=["pid", "cmdline", "name"]):
            try:
                cmdline = " ".join(proc.info.get("cmdline") or [])
                name = proc.info.get("name") or ""
                haystack = f"{name} {cmdline}".strip()
                if pattern in haystack:
                    matched.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return self._terminate_processes(matched, task, reason, target=f"pattern:{pattern}")

    def _terminate_port_processes(self, port: int, task: str, reason: str) -> set[int]:
        matched: list[psutil.Process] = []
        # Some psutil builds reject "connections" in attrs; request basics only.
        for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:
                for conn in proc.connections(kind="inet"):
                    if conn.laddr and conn.laddr.port == port:
                        matched.append(proc)
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            except AttributeError:
                # connections() unsupported; abandon port-based matching in this run
                break
        return self._terminate_processes(matched, task, reason, target=f"port:{port}")

    def _terminate_processes(
        self, processes: Iterable[psutil.Process], task: str, reason: str, *, target: str
    ) -> set[int]:
        killed: set[int] = set()
        procs = [p for p in processes if p.pid > 1]
        if not procs:
            return killed

        for proc in procs:
            self._send_signal(proc.pid, signal.SIGTERM)
        try:
            _, alive = psutil.wait_procs(procs, timeout=self._timeout)
        except Exception:  # pragma: no cover - best effort
            alive = procs

        if alive:
            for proc in alive:
                self._send_signal(proc.pid, signal.SIGKILL)
            with contextlib.suppress(Exception):
                psutil.wait_procs(alive, timeout=self._timeout / 2)

        for proc in procs:
            killed.add(proc.pid)

        self._logger.log(
            "forced_cleanup_match",
            LogLevel.WARNING,
            scope=LogScope.FRAMEWORK,
            task=task,
            reason=reason,
            target=target,
            terminated=list(sorted(killed)),
        )
        return killed

    def _execute_local_command(self, command: str, task: str, reason: str) -> None:
        try:
            result = subprocess.run(
                command,
                check=False,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            self._logger.log(
                "forced_cleanup_command",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=task,
                reason=reason,
                command=command,
                exit_code=result.returncode,
                stdout=(result.stdout or "").strip(),
                stderr=(result.stderr or "").strip(),
            )
        except subprocess.TimeoutExpired as exc:
            self._logger.log(
                "forced_cleanup_command_timeout",
                LogLevel.ERROR,
                scope=LogScope.FRAMEWORK,
                task=task,
                reason=reason,
                command=command,
                timeout=self._timeout,
                error=str(exc),
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.log(
                "forced_cleanup_command_error",
                LogLevel.ERROR,
                scope=LogScope.FRAMEWORK,
                task=task,
                reason=reason,
                command=command,
                error=str(exc),
                error_type=type(exc).__name__,
            )

    def _cleanup_remote(
        self, entry: ForcedCleanupPlanEntry, host: HostDefinition, reason: str
    ) -> None:
        if self._ssh_manager is None:
            self._logger.log(
                "forced_cleanup_remote_skipped",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=entry.task_name,
                reason=reason,
                host=host.as_string(),
                message="SSH manager unavailable; skipping remote forced cleanup",
            )
            return
        try:
            client = self._ssh_manager.get_client(
                host.as_string(),
                host.port,
                host.password or None,
                command_name=entry.task_name,
                allow_agent=host.allow_agent,
                look_for_keys=host.look_for_keys,
            )
            script = self._build_remote_script(entry.spec)
            stdin, stdout, stderr = client.exec_command(script, timeout=self._timeout)
            if stdin:
                with contextlib.suppress(Exception):
                    stdin.close()
            exit_code = stdout.channel.recv_exit_status()
            stdout_text = (stdout.read() or b"").decode("utf-8", errors="replace")
            stderr_text = (stderr.read() or b"").decode("utf-8", errors="replace")
            self._logger.log(
                "forced_cleanup_remote",
                LogLevel.WARNING,
                scope=LogScope.FRAMEWORK,
                task=entry.task_name,
                reason=reason,
                host=host.as_string(),
                exit_code=exit_code,
                stdout=stdout_text.strip(),
                stderr=stderr_text.strip(),
                mode=entry.spec.mode,
                patterns=list(entry.spec.patterns),
                ports=list(entry.spec.ports),
                commands=list(entry.spec.commands),
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.log(
                "forced_cleanup_remote_failed",
                LogLevel.ERROR,
                scope=LogScope.FRAMEWORK,
                task=entry.task_name,
                reason=reason,
                host=host.as_string(),
                error=str(exc),
                error_type=type(exc).__name__,
            )

    def _build_remote_script(self, spec: CleanupSpec) -> str:
        parts: list[str] = []
        for port in spec.ports:
            parts.append(f"fuser -kn tcp {port} 2>/dev/null || true")
        for pattern in spec.patterns:
            safe = shlex.quote(pattern)
            parts.append(f"pkill -TERM -f {safe} || true; sleep 0.5; pkill -KILL -f {safe} || true")
        for command in spec.commands:
            parts.append(command)
        return "; ".join(parts) or "true"

    @staticmethod
    def _send_signal(pid: int, sig: signal.Signals) -> None:
        with contextlib.suppress(Exception):
            if hasattr(os, "killpg"):
                os.killpg(pid, sig)
            else:
                os.kill(pid, sig)


__all__ = ["ForcedCleanupPlanEntry", "ForcedCleanupExecutor", "OrphanDetector"]
