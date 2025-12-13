"""Generic helper for rendering grouped sections of parameters."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from rich import box
from rich.table import Table


@dataclass(frozen=True)
class SectionRow:
    """Data-holder representing a metric row inside a section."""

    label: str
    detail: str


def _chunk_rows(rows: Sequence[SectionRow], width: int) -> Iterable[Sequence[SectionRow]]:
    for idx in range(0, len(rows), width):
        yield rows[idx : idx + width]


def render_group_section(
    *,
    title: str,
    caption: str | None,
    rows: Iterable[SectionRow],
    layout_hint: str | None = None,
    sparkline_style: str | None = None,
) -> Table:
    """Render a table for the requested group using schema-driven hints."""

    rows_list = list(rows)
    if layout_hint == "status_grid":
        return _render_status_grid(
            title=title,
            caption=caption,
            rows=rows_list,
            sparkline_style=sparkline_style,
        )

    return _render_basic_section(
        title=title,
        caption=caption,
        rows=rows_list,
        sparkline_style=sparkline_style,
    )


def _render_basic_section(
    *,
    title: str,
    caption: str | None,
    rows: Sequence[SectionRow],
    sparkline_style: str | None = None,
) -> Table:
    table = Table(
        show_header=False,
        box=box.SIMPLE if sparkline_style == "thick" else box.ROUNDED,
        padding=(0, 1),
        expand=True,
        title=title,
        caption=caption,
    )
    table.add_column("Metric", style="bold cyan", no_wrap=True)
    table.add_column("Details", ratio=1, overflow="fold")

    for row in rows:
        table.add_row(row.label, row.detail)

    return table


def _render_status_grid(
    *,
    title: str,
    caption: str | None,
    rows: Sequence[SectionRow],
    sparkline_style: str | None = None,
) -> Table:
    columns = max(1, min(len(rows), 3))
    table = Table(
        show_header=False,
        box=box.MINIMAL_DOUBLE_HEAD,
        padding=(0, 1),
        expand=True,
        title=title,
        caption=caption,
    )
    for _ in range(columns):
        table.add_column(justify="left", no_wrap=False)

    for chunk in _chunk_rows(rows, columns):
        cells = [
            f"[bold]{row.label}[/bold]\n{row.detail}" for row in chunk  # noqa: PERF203
        ]
        while len(cells) < columns:
            cells.append("")
        table.add_row(*cells)

    return table


__all__ = ["SectionRow", "render_group_section"]
