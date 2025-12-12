# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
One-dimensional figure builder for Plotmon: provides configuration and
rendering of 1D experiment plots using Bokeh.
"""

from bokeh.models import ColumnDataSource, DataRange1d, HoverTool
from bokeh.models.annotations import Title
from bokeh.plotting import figure

from quantify.visualization.plotmon.services.figure_builder.base_figure_builder import (
    BaseFigureBuilder,
)
from quantify.visualization.plotmon.utils.communication import ParamInfo
from quantify.visualization.plotmon.utils.figures import OneDFigureConfig
from quantify.visualization.plotmon.utils.tuid_data import TuidData


class OneDFigureBuilder(BaseFigureBuilder):
    """Builds a 1D figure using Bokeh, highlighting active and selected TUIDs."""

    def build_figure(
        self,
        config: ParamInfo,
        sources: dict[str, ColumnDataSource],
        tuid_data: TuidData,
        ranges: dict[str, DataRange1d],
        fig: figure | None = None,
    ) -> figure:
        """
        Build a 1D figure for experiments, highlighting active and selected TUIDs.
        Returns a Bokeh figure object.
        """
        if not isinstance(config, OneDFigureConfig):
            raise ValueError(
                f"Config must be an instance of OneDFigureConfig, "
                f"istead was type {type(config)}"
            )

        if fig is None:
            p = figure(
                x_axis_label=f"{config.x_label} ({config.x_units})",
                y_axis_label=f"{config.y_label} ({config.y_units})",
                min_width=config.width,
                min_height=config.height,
                x_range=ranges["x_range"],
                y_range=ranges["y_range"],
                output_backend="webgl",
                sizing_mode="stretch_width",
                background_fill_color="#ffffff",
                border_fill_color="#ffffff",
                outline_line_color="#e1e5e9",
            )
            p.legend.label_text_font_size = "12pt"
            p.xaxis.axis_label_text_font_size = "15pt"
            p.yaxis.axis_label_text_font_size = "15pt"
            title = Title(text_font_size="20pt", align="center", text=config.title)
            p.title = title
        else:
            p = fig
            # Remove all renderers (lines, scatters, etc.)
            p.renderers = []

        selected_tuid = tuid_data.selected_tuid.get(
            tuid_data.session_id, tuid_data.selected_tuid.get(-1, "")
        )
        active_tuid = tuid_data.active_tuid
        renderers = []
        # Prepare data for multi_line
        xs, ys, tuid_labels = [], [], []
        scatter_x, scatter_y, scatter_tuid = [], [], []
        for tuid in tuid_data.tuids:
            source_name = f"{tuid}_{config.plot_name}"
            source = sources.get(source_name)
            if source is None:
                raise ValueError(
                    f"Data source '{source_name}' not found in provided sources. "
                    f"Available: {list(sources.keys())}"
                )

            x_vals = list(source.data[config.x_key])
            y_vals = list(source.data[config.y_key])
            xs.append(x_vals)
            ys.append(y_vals)
            tuid_labels.append(tuid)

            scatter_x.extend(x_vals)
            scatter_y.extend(y_vals)
            scatter_tuid.extend([tuid] * len(x_vals))

        # Multi-line for all tuids (inactive alpha)
        multi_source = ColumnDataSource(data=dict(xs=xs, ys=ys, tuid=tuid_labels))
        scatter_source = ColumnDataSource(
            data=dict(x=scatter_x, y=scatter_y, tuid=scatter_tuid)
        )
        glyph = p.multi_line(
            xs="xs",
            ys="ys",
            source=multi_source,
            line_width=2,
            alpha=config.inactive_alpha,
            color=config.color,
            nonselection_alpha=config.nonselection_alpha,
            nonselection_color=config.nonselection_color,
            hover_alpha=config.hover_alpha,
            hover_color=config.hover_color,
            selection_color=config.selection_color,
        )

        scatter_glyph = p.scatter(
            x="x",
            y="y",
            source=scatter_source,
            marker="circle",
            color=config.selection_color,
            size=8,
            fill_alpha=config.inactive_alpha,
            line_alpha=config.inactive_alpha,
            selection_alpha=1.0,
            selection_color=config.selection_color,
            nonselection_alpha=config.nonselection_alpha,
            nonselection_color=config.nonselection_color,
            hover_alpha=config.hover_alpha,
            hover_color=config.hover_color,
        )
        renderers.append(glyph)
        renderers.append(scatter_glyph)

        # Highlighted line for selected/active tuid
        highlight_tuid = active_tuid if active_tuid else selected_tuid
        if highlight_tuid:
            source_name = f"{highlight_tuid}_{config.plot_name}"
            source = sources.get(source_name)
            if source is None:
                raise ValueError(
                    f"Data source '{source_name}' not found in provided sources. "
                    f"Available: {list(sources.keys())}"
                )
            main_glyph = p.line(
                x=config.x_key,
                y=config.y_key,
                source=source,
                legend_label=highlight_tuid,
                line_width=2,
                alpha=config.active_alpha,
                color=config.selection_color,
                selection_color=config.selection_color,
                nonselection_color=config.nonselection_color,
                nonselection_alpha=config.nonselection_alpha,
                hover_color=config.hover_color,
                hover_alpha=config.hover_alpha,
            )
            renderers.append(main_glyph)
            p.scatter(
                x=config.x_key,
                y=config.y_key,
                source=source,
                marker="circle",
                color=config.selection_color,
                size=8,
                fill_alpha=config.active_alpha,
                line_alpha=config.active_alpha,
                selection_alpha=1.0,
                selection_color=config.selection_color,
                nonselection_alpha=config.nonselection_alpha,
                nonselection_color=config.nonselection_color,
                hover_alpha=config.hover_alpha,
                hover_color=config.hover_color,
            )

        hover = HoverTool(
            renderers=renderers,
            tooltips=[("TUID", "@tuid")],
        )
        p.add_tools(hover)

        return p
