"""SSH client pooling helpers for CommandRunner."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING

from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger
from hil_testbench.utils.runtime_deps import require_paramiko

if TYPE_CHECKING:  # pragma: no cover - import only for typing
    import paramiko

# SSH connection retry configuration
SSH_CONNECTION_MAX_RETRIES = 3
SSH_CONNECTION_RETRY_DELAY_SEC = 1.0


class SSHClientManager:
    """Caches SSH clients per host/user/port combination."""

    def __init__(
        self,
        task_logger: TaskLogger,
        verbose: bool,
        *,
        cancel_event: threading.Event | None = None,
        max_retries: int = SSH_CONNECTION_MAX_RETRIES,
        retry_delay: float = SSH_CONNECTION_RETRY_DELAY_SEC,
    ) -> None:
        self._task_logger = task_logger
        self._verbose = verbose
        self._clients: dict[str, paramiko.SSHClient] = {}
        self._client_meta: dict[str, tuple[str, int, str | None]] = {}
        self._lock = threading.Lock()
        self._cancel_event = cancel_event
        self._max_retries = max(1, int(max_retries))
        self._retry_delay = max(0.0, float(retry_delay))

    def get_client(
        self,
        host: str,
        port: int = 22,
        password: str | None = None,
        command_name: str | None = None,
        *,
        allow_agent: bool = False,
        look_for_keys: bool = True,
    ) -> paramiko.SSHClient:
        key, hostname, username, actual_port = self._normalize_host(host, port)
        with self._lock:
            if key in self._clients:
                return self._clients[key]
            client = self._connect_client(
                key,
                hostname,
                username,
                actual_port,
                password,
                command_name,
                allow_agent,
                look_for_keys,
            )
            self._clients[key] = client
            self._client_meta[key] = (hostname, actual_port, username)
            return client

    def close_all(self) -> None:
        with self._lock:
            items = list(self._clients.items())
            self._clients.clear()
        for key, client in items:
            try:
                client.close()
                if self._verbose:
                    self._task_logger.log(
                        "ssh_connection_closed",
                        LogLevel.DEBUG,
                        scope=LogScope.FRAMEWORK,
                        _key=key,
                    )
            except Exception as exc:  # pylint: disable=broad-except
                self._task_logger.log(
                    "ssh_connection_close_error",
                    LogLevel.WARNING,
                    scope=LogScope.FRAMEWORK,
                    message="Failed to close SSH connection",
                    key=key,
                    error=str(exc),
                )

    def active_client_count(self) -> int:
        with self._lock:
            return len(self._clients)

    def iter_clients(self) -> list[tuple[str, int, paramiko.SSHClient]]:
        with self._lock:
            items = []
            for key, client in self._clients.items():
                host, port, _ = self._client_meta.get(key, (key, 22, None))
                items.append((host, port, client))
            return items

    def _normalize_host(self, host: str, port: int) -> tuple[str, str, str | None, int]:
        username: str | None = None
        hostname = host
        if "@" in hostname:
            username, hostname = hostname.split("@", 1)
        actual_port = port
        if ":" in hostname:
            host_only, port_str = hostname.split(":", 1)
            hostname = host_only
            try:
                actual_port = int(port_str)
            except ValueError:
                actual_port = port
        key = f"{f'{username}@' if username else ''}{hostname}:{actual_port}"
        return key, hostname, username, actual_port

    def _connect_client(
        self,
        key: str,
        hostname: str,
        username: str | None,
        port: int,
        password: str | None,
        command_name: str | None,
        allow_agent: bool,
        look_for_keys: bool,
    ) -> paramiko.SSHClient:
        log_scope = LogScope.COMMAND if command_name else LogScope.FRAMEWORK
        log_task = command_name or None
        self._task_logger.log(
            "ssh_connection_attempt",
            LogLevel.DEBUG,
            message=f"Connecting to {key}",
            scope=log_scope,
            task=log_task,
            show_fields_with_message=True,
            host=key,
        )
        paramiko = require_paramiko()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        last_error: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            self._abort_if_cancelled(key, log_scope, log_task)
            try:
                client.connect(
                    hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    allow_agent=allow_agent,
                    look_for_keys=look_for_keys,
                    timeout=10,
                )
                if self._verbose:
                    self._task_logger.log(
                        "ssh_connection_opened",
                        LogLevel.DEBUG,
                        message="Connected",
                        scope=log_scope,
                        task=log_task,
                        show_fields_with_message=True,
                        host=key,
                    )
                return client
            except Exception as exc:  # pylint: disable=broad-except
                last_error = exc

                # Log transient failures as WARNING with retry info
                if attempt < self._max_retries:
                    reason_hint = self._describe_ssh_failure(paramiko, exc)
                    self._task_logger.log(
                        "ssh_connection_retry",
                        LogLevel.WARNING,
                        scope=log_scope,
                        task=log_task,
                        message=self._format_retry_message(
                            key,
                            attempt,
                            reason_hint,
                            max_attempts=self._max_retries,
                            retry_delay=self._retry_delay,
                        ),
                        host=key,
                        error=str(exc),
                        error_type=type(exc).__name__,
                        attempt=attempt,
                        max_attempts=self._max_retries,
                    )
                    if self._wait_for_retry_delay():
                        self._abort_if_cancelled(key, log_scope, log_task)
                    continue

        # All retries exhausted - raise exception to be logged by CommandRunner
        # CommandRunner has full command context and will log ERROR with remediation
        assert last_error is not None
        raise last_error

    def _abort_if_cancelled(
        self,
        key: str,
        scope: LogScope,
        task: str | None,
    ) -> None:
        if self._cancel_event and self._cancel_event.is_set():
            self._task_logger.log(
                "ssh_connection_cancelled",
                LogLevel.INFO,
                scope=scope,
                task=task,
                message="Aborting SSH connection attempts after cancellation",
                host=key,
            )
            raise InterruptedError("SSH connection aborted due to cancellation")

    def _wait_for_retry_delay(self) -> bool:
        if self._retry_delay <= 0:
            return bool(self._cancel_event and self._cancel_event.is_set())
        if not self._cancel_event:
            time.sleep(self._retry_delay)
            return False
        return self._cancel_event.wait(self._retry_delay)

    @staticmethod
    def _format_retry_message(
        key: str,
        attempt: int,
        reason_hint: str | None,
        *,
        max_attempts: int,
        retry_delay: float,
    ) -> str:
        base = (
            f"Connection to {key} failed (attempt {attempt}/{max_attempts}), "
            f"retrying in {retry_delay}s..."
        )
        if reason_hint:
            return f"{base} ({reason_hint})"
        return base

    @staticmethod
    def _describe_ssh_failure(
        paramiko_module,
        exc: Exception,
    ) -> str | None:
        """Return short reason hint for common SSH failures."""

        try:
            ssh_exc = paramiko_module.ssh_exception
        except AttributeError:  # pragma: no cover - defensive fallback
            return None

        if isinstance(exc, ssh_exc.AuthenticationException):
            return "authentication rejected"

        if isinstance(exc, ssh_exc.BadHostKeyException):
            return "host key mismatch"

        if isinstance(exc, ssh_exc.NoValidConnectionsError):
            return "socket refused"

        if isinstance(exc, (TimeoutError, ssh_exc.SSHException)):
            return "connection timed out"

        return None


__all__ = ["SSHClientManager"]
