"""Console output helpers for TaskLogger."""

from __future__ import annotations

import json
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar, Protocol

from rich.console import Console


class _BackendProtocol(Protocol):
    console: Console | None

    def add_event(self, message: str, level: str) -> None:  # pragma: no cover - Protocol signature
        ...


@dataclass(slots=True)
class ConsolePrinter:
    """Render console output for TaskLogger with minimal branching."""

    daemon_mode: bool
    quiet_errors_only: bool
    json_console: bool
    no_color: bool
    correlation_id: str
    print_fn: Callable[[str], None] = print
    time_provider: Callable[[], datetime] = datetime.now
    console_factory: Callable[[], Console] = lambda: Console(soft_wrap=True)

    _backend: _BackendProtocol | None = None
    _rich_console: Console | None = None

    _CONTEXT_WIDTH: ClassVar[int] = 14
    _DEFAULT_CONTEXT_LABEL: ClassVar[str] = "FRAMEWORK"
    _DEFAULT_ICON: ClassVar[str] = "•"
    _ICON_PAD_WIDTH: ClassVar[int] = 4
    _SCOPE_ICONS: ClassVar[dict[str, str]] = {
        "FRAMEWORK": "⚙️",
        "TASK": "📋",
        "COMMAND": "🛠️",
    }

    def set_backend(self, backend: Any | None) -> None:
        self._backend = backend if backend else None

    def emit(
        self,
        message: str,
        level: str,
        *,
        context_label: str | None,
        module_label: str | None,
        force_inline: bool = False,
        plain: bool = False,
        icon_override: str | None = None,
    ) -> None:
        if self.daemon_mode:
            return
        if self.quiet_errors_only and level not in {"ERROR", "CRITICAL"}:
            return
        if not message.strip():
            return
        use_plain = plain or force_inline
        if use_plain:
            self._emit_plain(message, icon_override)
        elif self.json_console:
            self._emit_json(message, level, icon_override)
        else:
            self._emit_console(
                message,
                level,
                context_label,
                module_label,
                icon_override,
            )
        self._notify_backend(message, level)

    @property
    def rich_console(self) -> Console | None:
        return self._rich_console

    def _emit_json(self, message: str, level: str, icon: str | None = None) -> None:
        payload = {
            "ts": self.time_provider().strftime("%H:%M:%S"),
            "level": level,
            "message": message,
            "cid": self.correlation_id,
        }
        if icon:
            payload["icon"] = icon
        self.print_fn(json.dumps(payload, ensure_ascii=False))

    def _emit_plain(self, message: str, icon: str | None = None) -> None:
        icon_plain, _ = self._format_icon_block(icon)
        payload = f"{icon_plain}{message}"
        console = self._resolve_console()
        if console is not None:
            console.print(payload)  # hil: allow-print (plain console output)
        else:
            try:
                self.print_fn(payload)
            except UnicodeEncodeError:
                self.print_fn(payload.encode("ascii", errors="replace").decode("ascii"))

    def _emit_console(
        self,
        message: str,
        level: str,
        context_label: str | None,
        module_label: str | None,
        icon_override: str | None = None,
    ) -> None:
        timestamp = self.time_provider().strftime("%H:%M:%S")
        context_plain = self._normalize_context(context_label)
        icon = icon_override or self._scope_icon_for(context_label)
        level_upper = (level or "").upper() or "INFO"
        level_abbr = {
            "TRACE": "T",
            "DEBUG": "D",
            "INFO": "I",
            "WARNING": "W",
            "ERROR": "E",
            "CRITICAL": "C",
        }.get(level_upper, level_upper[:1])
        level_plain = f"{level_abbr:<1}"
        module_plain, module_rich = self._format_module_label(module_label)
        icon_block, icon_block_rich = self._format_icon_block(icon)
        prefix_plain = (
            f"{icon_block}[{timestamp}] {context_plain} {level_plain} {module_plain}"
        ).rstrip()
        indent = " " * (len(prefix_plain) + 1)
        message_block = self._indent_message(message, indent)
        line_plain = f"{prefix_plain} {message_block}".rstrip()

        color = self._level_color(level_upper)
        context_rich = f"[{self._context_style()}]{self._escape_label(context_plain)}[/]"
        level_rich = f"[{color}]{level_plain}[/{color}]"
        prefix_rich = (
            f"{icon_block_rich}[dim]\\[{timestamp}][/dim] {context_rich} {level_rich} {module_rich}"
        ).rstrip()
        message_rich = self._indent_message(message, indent)
        line_rich = f"{prefix_rich} {message_rich}".rstrip()

        console = self._resolve_console()
        if console is not None:
            console.print(line_rich)  # hil: allow-print (console renderer)
            return
        try:
            self.print_fn(line_plain)
        except UnicodeEncodeError:
            safe = line_plain.encode("ascii", errors="replace").decode("ascii")
            self.print_fn(safe)

    def _notify_backend(self, message: str, level: str) -> None:
        backend = self._backend
        if backend and hasattr(backend, "add_event"):
            try:
                backend.add_event(message, level)
            except Exception:  # pragma: no cover - backend errors ignored
                pass

    def _resolve_console(self) -> Console | None:
        backend = self._backend
        if backend and hasattr(backend, "console") and backend.console:
            return backend.console
        if self.no_color:
            return None
        if self._rich_console is None:
            try:
                self._rich_console = self.console_factory()
            except Exception:  # pragma: no cover - Rich unavailable
                self._rich_console = None
        return self._rich_console

    @staticmethod
    def _level_color(level: str) -> str:
        return {
            "TRACE": "grey62",
            "DEBUG": "dim",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red bold",
            "CRITICAL": "red bold reverse",
        }.get(level, "white")

    @staticmethod
    def _escape_label(value: str | None) -> str:
        if not value:
            return ""
        return value.replace("[", "\\[").replace("]", "\\]")

    def _normalize_context(self, label: str | None) -> str:
        raw = (label or self._DEFAULT_CONTEXT_LABEL).upper()
        trimmed = raw[: self._CONTEXT_WIDTH]
        return trimmed.ljust(self._CONTEXT_WIDTH)

    def _scope_icon_for(self, label: str | None) -> str:
        if not label:
            return self._DEFAULT_ICON
        return self._SCOPE_ICONS.get(label.upper(), self._DEFAULT_ICON)

    def _context_style(self) -> str:
        return "bright_cyan"

    @staticmethod
    def _indent_message(message: str, indent: str) -> str:
        if "\n" not in message:
            return message
        return message.replace("\n", f"\n{indent}")

    def _format_module_label(self, module_label: str | None) -> tuple[str, str]:
        if not module_label:
            return "", ""
        escaped = self._escape_label(module_label)
        plain = f"[{module_label}] "
        rich = f"[dim][{escaped}][/dim] "
        return plain, rich

    def _format_icon_block(self, icon: str | None) -> tuple[str, str]:
        glyph = icon or ""
        if not glyph:
            pad = " " * self._ICON_PAD_WIDTH
            return pad, pad
        width = max(1, self._measure_display_width(glyph))
        space_count = self._ICON_PAD_WIDTH - width
        space_count = max(space_count, 1)
        suffix = " " * space_count
        block = f"{glyph}{suffix}"
        return block, block

    def _measure_display_width(self, text: str) -> int:
        width = 0
        for char in text:
            category = unicodedata.category(char)
            if category in {"Mn", "Me", "Cf"}:
                continue
            east = unicodedata.east_asian_width(char)
            width += 2 if east in {"W", "F"} else 1
        return width
