"""Factory helpers for constructing TaskLogger instances with shared dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from hil_testbench.config.run_config import RunConfig
from hil_testbench.run.logging.task_logger import TaskLogger


@dataclass(slots=True)
class TaskLoggerFactory:
    """Creates TaskLogger instances with consistent dependency wiring."""

    preconfigured_logger: TaskLogger | None = None

    def create(
        self,
        *,
        run_config: RunConfig,
        log_dir: str = "logs",
        correlation_id: str | None = None,
    ) -> TaskLogger:
        """Instantiate a TaskLogger configured for the current execution."""

        if self.preconfigured_logger is not None:
            logger = self.preconfigured_logger
            self.preconfigured_logger = None
            return logger

        return TaskLogger(
            run_config=run_config,
            log_dir=log_dir,
            correlation_id=correlation_id,
        )
