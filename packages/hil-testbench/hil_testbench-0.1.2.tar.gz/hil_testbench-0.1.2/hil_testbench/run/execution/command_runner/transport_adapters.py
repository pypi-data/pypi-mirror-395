"""Transport and execution context helpers."""

from __future__ import annotations

import inspect
import threading
from typing import Any, cast

from hil_testbench.config.task_config import TaskConfig
from hil_testbench.data_processing.events import (
    CommandOutputCallback,
    CommandOutputCallbackFactory,
)
from hil_testbench.run.exceptions import ConfigurationError
from hil_testbench.run.execution.execution_context import ExecutionContext
from hil_testbench.run.execution.output_streamer import OutputStreamer
from hil_testbench.run.execution.protocols import SSHClientProtocol
from hil_testbench.run.logging.task_logger import LogLevel, LogScope, TaskLogger

from .ssh_client_manager import SSHClientManager
from .types import ExecutionParams


class TransportAdapters:
    """Prepares streamers, execution contexts, and output callbacks."""

    def __init__(
        self,
        *,
        logger: TaskLogger,
        cancel_event: threading.Event,
        config: TaskConfig | None,
        process_tracker: Any,
        ssh_manager: SSHClientManager,
        process_cleanup: Any | None = None,
    ) -> None:
        self._logger = logger
        self._cancel_event = cancel_event
        self._config = config or TaskConfig()
        self._process_tracker = process_tracker
        self._ssh_manager = ssh_manager
        self._process_cleanup = process_cleanup
        self._connection_lock = threading.Lock()
        self._connected_commands: set[str] = set()

    def resolve_output_callback(
        self,
        command_name: str,
        callback: CommandOutputCallback | CommandOutputCallbackFactory | None,
    ) -> CommandOutputCallback | None:
        if callback is None or not callable(callback):
            return None
        try:
            factory = cast(CommandOutputCallbackFactory, callback)
            result = factory(self._logger.get_execution_dir())
        except TypeError as exc:
            self._logger.log(
                "callback_direct_not_factory",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=command_name,
                _callback_type=type(callback).__name__,
                _error=str(exc),
            )
            return self._validate_output_callback(callback, command_name)
        except Exception as exc:  # pylint: disable=broad-except
            self._logger.log(
                "callback_factory_error",
                LogLevel.ERROR,
                scope=LogScope.COMMAND,
                task=command_name,
                message="Callback factory failed",
                error=str(exc),
                _callback_type=type(callback).__name__,
                _error_type=type(exc).__name__,
            )
            return self._validate_output_callback(callback, command_name)

        if callable(result):
            self._logger.log(
                "callback_factory_detected",
                LogLevel.DEBUG,
                scope=LogScope.COMMAND,
                task=command_name,
                _factory_type=type(callback).__name__,
                _result_type=type(result).__name__,
            )
            return self._validate_output_callback(result, command_name)

        self._logger.log(
            "callback_factory_returned_non_callable",
            LogLevel.WARNING,
            scope=LogScope.COMMAND,
            task=command_name,
            message="Callback factory returned non-callable result",
            _factory_type=type(callback).__name__,
            _result_type=type(result).__name__,
        )
        return self._validate_output_callback(callback, command_name)

    def create_streamer(
        self,
        command_name: str,
        callback: CommandOutputCallback | None,
        execution: ExecutionParams,
    ) -> OutputStreamer:
        streamer = OutputStreamer(
            command_name,
            callback,
            self._logger,
            log_output=execution.log_output,
            sample_lines=execution.sample_lines,
        )
        streamer.set_command_spec(execution.spec)
        return streamer

    def create_execution_context(
        self,
        command_name: str,
        execution: ExecutionParams,
        streamer: OutputStreamer,
    ) -> ExecutionContext:
        ssh_client: SSHClientProtocol | None = None
        task_label = execution.task_name or self._extract_task_name(command_name)
        if execution.host:
            self._notify_command_status(task_label, command_name, "connecting")
            try:
                ssh_client = cast(
                    SSHClientProtocol,
                    self._ssh_manager.get_client(
                        execution.host,
                        execution.port,
                        execution.password,
                        command_name,
                        allow_agent=execution.allow_agent,
                        look_for_keys=execution.look_for_keys,
                    ),
                )
                if self._process_cleanup:
                    self._process_cleanup.sweep_host(execution.host, execution.port, ssh_client)
            except Exception:
                self._notify_command_status(task_label, command_name, "failed")
                raise
            else:
                self._mark_command_connected(command_name)
        else:
            self._mark_command_connected(command_name)
        return ExecutionContext(
            ssh_client=ssh_client,
            streamer=streamer,
            cancel_event=self._cancel_event,
            execution_dir=self._logger.get_execution_dir(),
            task_name=command_name,
            use_pty=bool(execution.use_pty),
            logger=self._logger,
            config=self._config,
            process_tracker=self._process_tracker,
            remote_os=execution.remote_os,
            shell_wrapper_mode=execution.shell_wrapper_mode or "auto",
            command_spec=execution.spec,
        )

    def set_process_cleanup(self, cleanup: Any) -> None:
        self._process_cleanup = cleanup

    def _notify_command_status(
        self,
        task_name: str | None,
        command_name: str,
        status: str | None,
        *,
        lifecycle_status: str | None = None,
    ) -> None:
        self._logger.notify_display_command_status(
            task_name,
            command_name,
            status,
            lifecycle_status=lifecycle_status,
        )

    @staticmethod
    def _extract_task_name(command_name: str) -> str | None:
        if ":" in command_name:
            return command_name.split(":", 1)[0]
        return None

    def _mark_command_connected(self, command_name: str) -> None:
        with self._connection_lock:
            self._connected_commands.add(command_name)

    def notify_connection_closed(self, task_name: str | None, command_name: str) -> None:
        with self._connection_lock:
            if command_name not in self._connected_commands:
                return
            self._connected_commands.remove(command_name)
        owner = task_name or self._extract_task_name(command_name)
        self._notify_command_status(owner, command_name, "closed")

    def _validate_output_callback(
        self,
        callback: CommandOutputCallback | CommandOutputCallbackFactory,
        command_name: str,
    ) -> CommandOutputCallback:
        try:
            signature = inspect.signature(callback)
        except (TypeError, ValueError):
            return cast(CommandOutputCallback, callback)

        parameters = list(signature.parameters.values())
        positional = [
            param
            for param in parameters
            if param.kind
            in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]
        required_positional = [
            param for param in positional if param.default is inspect.Signature.empty
        ]
        has_var_positional = any(
            param.kind == inspect.Parameter.VAR_POSITIONAL for param in parameters
        )

        if not positional and not has_var_positional:
            raise ConfigurationError(
                "Output callback must accept a CommandOutputEvent argument",
                context={
                    "command": command_name,
                    "callback_type": type(callback).__name__,
                },
            )

        if len(required_positional) > 1:
            raise ConfigurationError(
                "Output callback must accept exactly one positional argument",
                context={
                    "command": command_name,
                    "callback_type": type(callback).__name__,
                    "required_positional": len(required_positional),
                },
            )

        return cast(CommandOutputCallback, callback)


__all__ = ["TransportAdapters"]
