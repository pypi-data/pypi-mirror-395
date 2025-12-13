"""Helpers for streaming process output to the OutputStreamer."""

import threading
from collections.abc import Callable, Iterable

from hil_testbench.run.execution.output_streamer import OutputStreamer
from hil_testbench.run.logging.task_logger import LogLevel, TaskLogger


# TODO(long_running): Once transports emit structured stream events, collapse
# this worker into the unified streaming dispatcher instead of having per-stream
# threads. The dispatcher should multiplex stdout/stderr iterables and push
# events through the OutputStreamer replacement, respecting CommandSpec
# metadata for backpressure and heartbeat signaling.
class StreamWorker:
    """Background worker that forwards streamed lines to the OutputStreamer."""

    def __init__(
        self,
        *,
        name: str,
        line_iterator_factory: Callable[..., Iterable[str]],
        streamer: OutputStreamer | None,
        logger: TaskLogger,
        task_name: str,
        mode: str,
        purpose: str,
        is_error: bool = False,
        transform: Callable[[str], str] | None = None,
        stop_event: threading.Event | None = None,
        poll_interval: float = 0.1,
    ) -> None:
        self._name = name
        self._line_iterator_factory = line_iterator_factory
        self._streamer = streamer
        self._logger = logger
        self._task_name = task_name
        self._mode = mode
        self._purpose = purpose
        self._is_error = is_error
        self._transform = transform
        self._thread: threading.Thread | None = None
        self._stop_event = stop_event
        self._poll_interval = max(0.01, poll_interval)

    def start(self) -> "StreamWorker":
        """Start the worker thread."""
        if self._thread is not None:
            return self

        self._thread = threading.Thread(target=self._run, name=self._name)
        self._thread.daemon = True

        self._logger.log(
            "thread_created",
            LogLevel.DEBUG,
            task=self._task_name,
            _thread_name=self._name,
            _daemon=True,
            _purpose=self._purpose,
        )

        self._thread.start()
        return self

    def join(self, timeout: float | None = None) -> None:
        """Wait for the worker to finish processing."""
        if self._thread is None:
            return

        self._thread.join(timeout=timeout)
        self._logger.log(
            "thread_terminated",
            LogLevel.DEBUG,
            task=self._task_name,
            _thread_name=self._name,
            _alive=self._thread.is_alive(),
        )

    def _run(self) -> None:
        try:
            line_iterator = self._build_iterator()
            for raw_line in line_iterator:
                if self._should_stop():
                    break
                line = raw_line
                if self._transform is not None:
                    line = self._transform(raw_line)
                if not line:
                    continue
                if self._streamer:
                    stream_name = "stderr" if self._is_error else "stdout"
                    self._streamer.process_line(line, self._is_error, stream=stream_name)
        except Exception as exc:  # pylint: disable=broad-except
            self._logger.log(
                "stream_error",
                LogLevel.ERROR,
                task=self._task_name,
                message="Stream processing error",
                error=str(exc),
                _mode=self._mode,
            )

    @property
    def is_alive(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def _build_iterator(self) -> Iterable[str]:
        factories: list[Callable[[], Iterable[str]]] = []
        if self._stop_event is not None:
            factories.append(
                lambda: self._line_iterator_factory(self._stop_event, self._poll_interval)
            )
            factories.append(lambda: self._line_iterator_factory(self._stop_event))
        factories.append(self._line_iterator_factory)

        for factory in factories:
            try:
                iterator = factory()
            except TypeError:
                continue
            if iterator is not None:
                return iterator
        raise RuntimeError("line_iterator_factory incompatible with StreamWorker")

    def _should_stop(self) -> bool:
        if self._stop_event and self._stop_event.is_set():
            return True
        streamer = self._streamer
        if not streamer:
            return False
        stop_checker = getattr(streamer, "should_stop", None)
        if not callable(stop_checker):
            return False
        try:
            return stop_checker() is True
        except Exception:  # noqa: BLE001 - defensive guard
            return False
