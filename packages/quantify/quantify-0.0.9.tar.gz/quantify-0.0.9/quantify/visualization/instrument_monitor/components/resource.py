# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Resource monitor panel component."""

from __future__ import annotations

import contextlib
import logging
from typing import TYPE_CHECKING, Any, cast

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div, HoverTool, Range1d, Span
from bokeh.plotting import figure
import psutil

from quantify.visualization.instrument_monitor.components.theme import create_header

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from bokeh.document import Document


def _sparkline(*, width: int = 320, height: int = 48, y_end: int = 100) -> Any:
    """Create a minimal sparkline figure for KPI display."""
    p = figure(
        width=width,
        height=height,
        toolbar_location=None,
        tools="",
        x_range=Range1d(0, 90),
        y_range=Range1d(0, y_end),
    )
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False
    return p


def _state_color(v: float | None, warn: float, crit: float) -> str:
    """Return color based on warning/critical thresholds."""
    if v is None:
        return "#888"
    return "#b00020" if v >= crit else ("#cc7a00" if v >= warn else "#1f77b4")


def _format_memory_mib(value_mib: float) -> str:
    """Format memory value as MiB or GiB."""
    if value_mib >= 1024:
        return f"{value_mib / 1024:.2f} GiB"
    return f"{value_mib:.2f} MiB"


class _KPI:
    """Single KPI sparkline widget."""

    def __init__(self, title: str, unit: str, ymax: float, *, width: int = 340) -> None:
        self.unit = unit
        self.title = Div(
            text=f"<div style='color:#555;margin-bottom:2px'>{title}</div>"
        )
        self.value = Div(text="", styles={"font-size": "20px", "font-weight": "600"})
        self.src = ColumnDataSource(dict(x=[], y=[]))
        self.fig = _sparkline(width=width - 20, height=48, y_end=int(ymax or 1))
        self.fig.line("x", "y", source=self.src, line_width=2)
        self.fig.add_tools(HoverTool(tooltips=[("Last", "@y")], mode="vline"))
        self.ymax = max(1.0, float(ymax))

        avg_line = Span(
            location=self.ymax / 2,
            dimension="width",
            line_color="green",
            line_dash="dashed",
            line_width=2,
        )
        self.fig.add_layout(avg_line)
        self.layout = column(self.title, self.value, self.fig, width=width)

    def push(self, val: float | None, *, warn: float, crit: float) -> None:
        """Update KPI value and sparkline."""
        if val is None:
            self.value.text = "N/A"
            return

        color = _state_color(val, warn, crit)
        if self.unit.replace("%", "").strip().lower() == "mib":
            self.value.text = (
                f"<span style='color:{color}'>{_format_memory_mib(val)} / "
                f"{_format_memory_mib(self.ymax)}</span>"
            )
        else:
            self.value.text = f"<span style='color:{color}'>{val:.2f}%</span>"

        x_any = self.src.data.get("x")
        x_vals: Sequence[float]
        if isinstance(x_any, (list, tuple)):
            x_vals = cast("Sequence[float]", x_any)
        else:
            x_vals = []
        x_next = (cast("float", x_vals[-1]) + 1) if len(x_vals) > 0 else 0
        self.src.stream(dict(x=[x_next], y=[val]), rollover=90)

        y_any = self.src.data.get("y")
        y_vals: Sequence[float]
        if isinstance(y_any, (list, tuple)):
            y_vals = cast("Sequence[float]", y_any)
        else:
            y_vals = []
        if len(y_vals) == 0:
            ymin = 0.0
            ymax = self.ymax
        else:
            ymin = float(min(y_vals))
            ymax = float(max(y_vals))
        # Narrow the range types for Pyright; Bokeh exposes start/end on Range1d
        y_range = cast("Range1d", self.fig.y_range)
        x_range = cast("Range1d", self.fig.x_range)
        y_range.start = max(0.0, ymin * 0.9)
        y_range.end = max(self.ymax, ymax * 1.1)
        x_range.start = max(0, x_next - 90)
        x_range.end = x_next


class ResourcePanel:
    """Sparkline-based resource monitor as a reusable component.

    Public API kept minimal and backward compatible:
    - `layout_children`: list of Bokeh models for layout composition.
    - `update(cpu_percent, rss_bytes)`: called by the app periodically.
    """

    def __init__(self) -> None:
        """Initialize the resource panel with a header and a placeholder view."""
        self.header = create_header("Resource Monitor", "🖥️")

        self._proc = psutil.Process()
        with contextlib.suppress(Exception):
            psutil.cpu_percent(None)
            self._proc.cpu_percent(None)

        # Derive memory ceiling from host for better scaling
        try:
            mem_total_mib = psutil.virtual_memory().total / (1024**2)
        except Exception:
            mem_total_mib = 8192.0

        self.host_cpu = _KPI("Host CPU (avg)", "%", 100)
        self.proc_cpu = _KPI("Python CPU", "%", 200)
        self.proc_rss = _KPI("Python RSS", "MiB", mem_total_mib)

        self.legend = Div(
            text=(
                "<div style='font-size:12px; color:#555;'>"
                "<b>Legend:</b>"
                "<ul style='margin: 0; padding-left: 20px;'>"
                "<li><b>Host CPU:</b> Average CPU usage across the system (%).</li>"
                "<li><b>Python CPU:</b> CPU usage by this app (can exceed 100% "
                "on multi-core).</li>"
                "<li><b>Python RSS:</b> Memory used by this app (in MiB/GiB).</li>"
                "</ul>"
                "</div>"
            ),
            sizing_mode="stretch_width",
        )

    @property
    def layout_children(self) -> list:
        """Return child models to be included in a column layout."""
        return [
            self.header,
            self.host_cpu.layout,
            self.proc_cpu.layout,
            self.proc_rss.layout,
            self.legend,
        ]

    def update(self, *, cpu_percent: float | None, rss_bytes: int | None) -> None:
        """Update the panel with CPU and memory usage."""
        # Host CPU
        try:
            host_cpu = psutil.cpu_percent()
        except Exception:
            logger.exception("Failed to get host CPU percent")
            host_cpu = None
        self.host_cpu.push(host_cpu, warn=70, crit=90)

        # Process CPU
        self.proc_cpu.push(cpu_percent, warn=100, crit=150)

        # Process RSS memory in MiB
        rss_mib = (rss_bytes / (1024**2)) if rss_bytes is not None else None
        # Thresholds relative to the configured ymax
        warn_mem = self.proc_rss.ymax * 0.8
        crit_mem = self.proc_rss.ymax * 0.9
        self.proc_rss.push(rss_mib, warn=warn_mem, crit=crit_mem)

    # --- Optional self-managed update helpers ---
    def update_from_system(self) -> None:
        """Sample system/process metrics and update KPIs.

        This is a convenience wrapper for periodic callbacks.
        """
        try:
            cpu = self._proc.cpu_percent()
        except Exception:
            cpu = None
        try:
            rss = self._proc.memory_info().rss
        except Exception:
            rss = None
        self.update(cpu_percent=cpu, rss_bytes=rss)

    def start_auto_update(self, doc: Document, period_ms: int = 2000) -> None:
        """Start periodic updates on the provided Bokeh document.

        Parameters
        ----------
        doc
            Bokeh document used to schedule callbacks.
        period_ms
            Update interval in milliseconds. Defaults to 2000ms.

        """
        try:
            doc.add_periodic_callback(self.update_from_system, period_ms)
        except Exception:
            logger.exception("Failed to start resource panel auto update")
