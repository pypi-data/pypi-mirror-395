"""Console encoding helpers for platform-specific runtimes."""

from __future__ import annotations

import sys
import warnings
from abc import ABC, abstractmethod


class _ConsoleEncodingStrategy(ABC):
    @abstractmethod
    def configure(self) -> None:
        """Apply platform-specific encoding configuration."""


class _NoOpConsoleEncoding(_ConsoleEncodingStrategy):
    def configure(self) -> None:  # pragma: no cover - trivial
        return


class _WindowsConsoleEncoding(_ConsoleEncodingStrategy):
    def configure(self) -> None:
        import io  # hil: allow-lazy

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
        try:
            import ctypes  # hil: allow-lazy

            windll = getattr(ctypes, "windll", None)
            if windll is None:  # pragma: no cover - defensive
                raise AttributeError("ctypes.windll unavailable")
            kernel32 = windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"Failed to set Windows console to UTF-8: {exc}",
                stacklevel=2,
            )


def configure_console_encoding() -> None:
    """Normalize console encoding for the active platform."""

    strategy = _WindowsConsoleEncoding() if sys.platform == "win32" else _NoOpConsoleEncoding()
    strategy.configure()
    _enable_line_buffering(sys.stdout)
    _enable_line_buffering(sys.stderr)


def _enable_line_buffering(stream) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if not callable(reconfigure):  # pragma: no cover - depends on python build
        return
    try:
        reconfigure(line_buffering=True, write_through=True)
    except TypeError:  # Older CPython lacks write_through
        reconfigure(line_buffering=True)
