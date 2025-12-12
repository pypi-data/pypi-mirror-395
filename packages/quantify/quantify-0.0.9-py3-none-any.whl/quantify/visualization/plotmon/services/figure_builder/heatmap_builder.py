# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
2D Heatmap figure builder for Plotmon: provides configuration and
rendering of 2D heatmaps using Bokeh.
"""

import logging

from bokeh.models import (
    ColorBar,
    ColumnDataSource,
    DataRange1d,
    GlyphRenderer,
    HoverTool,
    LinearColorMapper,
    Title,
)
from bokeh.plotting import figure
import numpy as np

from quantify.visualization.plotmon.services.figure_builder.base_figure_builder import (
    BaseFigureBuilder,
)
from quantify.visualization.plotmon.utils.communication import ParamInfo
from quantify.visualization.plotmon.utils.figures import HeatmapConfig
from quantify.visualization.plotmon.utils.tuid_data import TuidData


class HeatmapFigureBuilder(BaseFigureBuilder):
    """
    Builds a 2D image placeholder, the given source is linked to the image data.
    If no TUID is selected or active, a placeholder image with NaN values is shown.
    """

    def build_figure(
        self,
        config: ParamInfo,
        sources: dict[str, ColumnDataSource],
        tuid_data: TuidData,
        ranges: dict[str, DataRange1d],
        fig: figure | None = None,
    ) -> figure:
        """
        Build a 2D heatmap figure for finished experiments.
        Returns a Bokeh figure object.
        """
        if not isinstance(config, HeatmapConfig):
            raise ValueError(
                "Config must be an instance of HeatmapConfig, istead was type %s",
                type(config),
            )

        source_tuid = self._select_source_tuid(tuid_data)
        source = self._get_source(source_tuid, config, sources)
        ranges.clear()
        if fig is None:
            fig = figure(
                title=config.title,
                x_axis_label=f"{config.x_label} ({config.x_units})",
                y_axis_label=f"{config.y_label} ({config.y_units})",
                min_width=config.width,
                min_height=config.height,
                output_backend="webgl",
                background_fill_color="#ffffff",
                border_fill_color="#ffffff",
                outline_line_color="#818589",
                sizing_mode="stretch_width",
            )

            fig.legend.label_text_font_size = "12pt"
            fig.xaxis.axis_label_text_font_size = "15pt"
            fig.yaxis.axis_label_text_font_size = "15pt"
            title = Title(text_font_size="20pt", align="center", text=config.title)
            fig.title = title
        else:
            if fig.title is not None:
                if isinstance(fig.title, Title):
                    fig.title.text = config.title
                else:
                    fig.title = config.title
            fig.xaxis.axis_label = f"{config.x_label} ({config.x_units})"
            fig.yaxis.axis_label = f"{config.y_label} ({config.y_units})"
            if isinstance(fig.renderers[0], GlyphRenderer):
                fig.renderers[0].data_source = source
            return fig

        color_mapper = LinearColorMapper(palette=config.palette)
        image_renderer = fig.image(
            image=config.image_key,
            x=config.x_key,
            y=config.y_key,
            dw=config.dw_key,
            dh=config.dh_key,
            source=source,
        )
        image_renderer.glyph.color_mapper = color_mapper

        color_bar = ColorBar(color_mapper=color_mapper, padding=3)
        color_bar.title = f"{config.z_label} ({config.z_units})"
        color_bar.title_text_font_style = "normal"
        color_bar.title_standoff = 5
        color_bar.title_text_font_size = "15px"
        color_bar.title_text_baseline = "middle"
        fig.add_layout(color_bar, "right")

        hover = HoverTool(
            renderers=[image_renderer],
            tooltips=[
                ("TUID", "@tuid"),
                (f"{config.x_label} ({config.x_units})", "$x"),
                (f"{config.y_label} ({config.y_units})", "$y"),
                (f"{config.z_label} ({config.z_units})", f"@{config.image_key}"),
            ],
        )
        fig.add_tools(hover)
        return fig

    @staticmethod
    def _select_source_tuid(tuid_data: TuidData) -> str | None:
        """Select the TUID to use for the heatmap source."""
        selected_tuid = tuid_data.selected_tuid.get(
            tuid_data.session_id, tuid_data.selected_tuid.get(-1, "")
        )

        if selected_tuid != "":
            return selected_tuid
        if tuid_data.active_tuid != "":
            return tuid_data.active_tuid
        return None

    @staticmethod
    def _get_source(
        source_tuid: str | None,
        config: HeatmapConfig,
        sources: dict[str, ColumnDataSource],
    ) -> ColumnDataSource:
        """Get the ColumnDataSource for the heatmap, or a placeholder if not found."""
        if source_tuid:
            source_name = f"{source_tuid}_{config.plot_name}"
            source = sources.get(source_name)
            if source is None:
                logging.info(
                    "ColumnDataSource for '%s' not found in sources. "
                    "Available sources: %s",
                    source_name,
                    list(sources.keys()),
                )
                source = sources.get(config.plot_name)  # fallback to base source

            if source is not None:
                return source

        # Return placeholder source if no TUID selected or source missing
        placeholder_image = np.full((1, 1), np.nan)
        return ColumnDataSource(
            data={
                config.image_key: [placeholder_image],
                config.x_key: [0],
                config.y_key: [0],
                config.dw_key: [1],
                config.dh_key: [1],
                "tuid": [""],
            }
        )
