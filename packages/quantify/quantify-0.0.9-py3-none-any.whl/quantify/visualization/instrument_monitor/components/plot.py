# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Plot component for the instrument monitor UI."""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, cast

from bokeh.models import ColumnDataSource, Div, Title
from bokeh.plotting import figure

from quantify.visualization.instrument_monitor.components.theme import STYLES
from quantify.visualization.instrument_monitor.logging_setup import get_logger

if TYPE_CHECKING:
    from quantify.visualization.instrument_monitor.models import Reading

logger = get_logger(__name__)


class LivePlot:
    """Lightweight live plot with minimal memory footprint."""

    def __init__(self) -> None:
        """Initialize the live plot."""
        self.figure = figure(
            x_axis_label="Time",
            y_axis_label="Value",
            sizing_mode="stretch_both",
            x_axis_type="datetime",
            toolbar_location="above",
            background_fill_color="#ffffff",
            border_fill_color="#ffffff",
            outline_line_color="#e1e5e9",
        )

        self.figure.title = Title(text="Live Plot")

        self._apply_plot_styling()
        self.source = ColumnDataSource(data={"x": [], "y": []})
        self.instruction = Div(
            text=(
                "💡 Select a numeric parameter in the table to see its value update "
                "over time."
            ),
            styles={
                **STYLES["empty_state"],
                "position": "absolute",
                "left": "50%",
                "top": "50%",
                "transform": "translate(-50%, -50%)",
                "pointer-events": "none",
                "z-index": "1",
                "width": "80%",
            },
            visible=True,
        )
        plot_color = "#3b82f6"
        self.figure.line(
            "x", "y", source=self.source, line_width=3, color=plot_color, alpha=0.8
        )
        self.figure.scatter(
            "x", "y", source=self.source, size=8, color=plot_color, alpha=0.9
        )

        self.current_parameter: str | None = None
        self.max_points = 200

    def _apply_plot_styling(self) -> None:
        """Apply consistent plot styling."""
        title = cast("Title", self.figure.title)
        title.text_font = "Segoe UI, sans-serif"
        title.text_font_size = "14px"
        title.text_color = "#374151"
        self.figure.axis.axis_label_text_font = "Segoe UI, sans-serif"
        self.figure.axis.axis_label_text_color = "#6b7280"
        self.figure.axis.major_label_text_font = "Segoe UI, sans-serif"
        self.figure.axis.major_label_text_color = "#6b7280"
        self.figure.grid.grid_line_color = "#f3f4f6"
        self.figure.grid.grid_line_alpha = 0.8

    def set_parameter(self, full_name: str) -> None:
        """Set the parameter to plot."""
        if self.current_parameter != full_name:
            self.current_parameter = full_name
            cast("Title", self.figure.title).text = full_name
            self.source.data = {"x": [], "y": []}
            with contextlib.suppress(Exception):
                self.instruction.visible = True

    def add_point(self, reading: Reading) -> None:
        """Add a new data point to the plot."""
        if self.current_parameter != reading.full_name or not isinstance(
            reading.value, (int, float)
        ):
            return

        try:
            with contextlib.suppress(Exception):
                self.instruction.visible = False
            self.source.stream(
                {"x": [reading.ts], "y": [float(reading.value)]},
                rollover=self.max_points,
            )
        except Exception as e:
            logger.error(
                "Error adding plot point",
                extra={"parameter": reading.full_name, "error": str(e)},
                exc_info=True,
            )
