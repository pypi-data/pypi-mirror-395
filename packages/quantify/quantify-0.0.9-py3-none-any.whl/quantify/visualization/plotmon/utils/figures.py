# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Configuration models for different types of figures used in Plotmon."""

from enum import Enum

from pydantic import BaseModel, Field

from quantify.visualization.plotmon.utils.colors import Colors


class PlotType(Enum):
    """Enumeration of supported plot types."""

    ONE_D = "1d"
    HEATMAP = "heatmap"
    ONE_D_MULTILINE = "1d_multiline"

    @staticmethod
    def from_str(label: str) -> "PlotType":
        """Convert a string to a PlotType enum member."""
        match label.lower():
            case "1d":
                return PlotType.ONE_D
            case "heatmap":
                return PlotType.HEATMAP
            case "1d_multiline":
                return PlotType.ONE_D_MULTILINE
            case _:
                raise ValueError(f"Unknown plot type: {label}")


class HeatmapConfig(BaseModel):
    """Configuration parameters for a 2D heatmap figure."""

    plot_type: str = Field(PlotType.HEATMAP.value, description="Type of the plot.")
    image_key: str = Field(
        "image",
        description="Key for the image data in the source."
        "When sending data, this should be the name under which the image data is sent."
        "Example: if image_key = 'img' => source.data = {'img': [...], ...}",
    )
    x_key: str = Field(
        "x",
        description="Key for the x-axis data in the source."
        " When sending data, this should be the name under which the x data is sent."
        "Example: if x_key = 'omega' => source.data = {'omega': [...], ...}",
    )
    y_key: str = Field(
        "y",
        description="Key for the y-axis data in the source."
        " When sending data, this should be the name under which the y data is sent."
        "Example: if y_key = 'time' => source.data = {'time': [...], ...}",
    )
    dw_key: str = Field("dw", description="Key for the width of each image pixel.")
    dh_key: str = Field("dh", description="Key for the height of each image pixel.")
    plot_name: str = Field("generic_heatmap", description="Name of the plot type.")
    x_label: str = Field("X", description="Label for the x-axis.")
    y_label: str = Field("Y", description="Label for the y-axis.")
    z_label: str = Field("Z", description="Label for the z-axis.")
    x_units: str = Field("", description="Units for the x-axis.")
    y_units: str = Field("", description="Units for the y-axis.")
    z_units: str = Field("", description="Units for the z-axis.")
    title: str = Field("2D Heatmap", description="Title of the heatmap figure.")
    width: int = Field(750, description="Width of the figure in pixels.")
    height: int = Field(600, description="Height of the figure in pixels.")
    palette: str = Field("Viridis256", description="Color palette for the heatmap.")
    grid_2d_uniformly_spaced: bool = Field(
        False,
        description="Whether the heatmap data is on a uniformly spaced 2D grid.",
    )
    grid_2d: bool = Field(
        False,
        description="Whether the heatmap should or not be displayed.",
    )
    one_d_2_settables_uniformly_spaced: bool = Field(
        False,
        description="Whether the 1D data is on a uniformly spaced grid.",
    )


class OneDFigureConfig(BaseModel):
    """Configuration parameters for a 1D figure."""

    plot_type: str = Field(PlotType.ONE_D.value, description="Type of the plot.")
    x_label: str = Field("X-axis", description="Label for the x-axis.")
    y_label: str = Field("Y-axis", description="Label for the y-axis.")
    x_units: str = Field("units", description="Units for the x-axis.")
    y_units: str = Field("units", description="Units for the y-axis.")
    title: str = Field("1D Plot", description="Title of the 1D figure.")
    width: int = Field(300, description="Width of the figure in pixels.")
    height: int = Field(300, description="Height of the figure in pixels.")
    plot_name: str = Field("generic_plot", description="Name of the plot type.")
    inactive_alpha: float = Field(0.3, description="Alpha value for inactive lines.")
    active_alpha: float = Field(1.0, description="Alpha value for the active line.")
    color: str = Field(Colors.BLUE.value, description="Color for inactive lines.")
    selection_color: str = Field(
        Colors.BLUE.value, description="Color for the selected/active line."
    )
    nonselection_color: str = Field(
        Colors.ORANGE.value, description="Color for non-selected lines."
    )
    nonselection_alpha: float = Field(
        0.08, description="Alpha value for non-selected lines."
    )
    hover_color: str = Field(
        Colors.ORANGE.value, description="Color for lines on hover."
    )
    hover_alpha: float = Field(1.0, description="Alpha value for lines on hover.")
    x_key: str = Field(
        "x",
        description="Key for the x-axis data in the source."
        " When sending data, this should be the name under which the x data is sent."
        "Example: if x_key = 'omega' => source.data = {'omega': [...], ...}",
    )
    y_key: str = Field(
        "y",
        description="Key for the y-axis data in the source."
        " When sending data, this should be the name under which the y data is sent."
        "Example: if y_key = 'signal' => source.data = {'signal': [...], ...}",
    )
    legend_title: str = Field("Experiments", description="Title for the legend.")
    legend_location: tuple[float, float] | str = Field(
        "top_right", description="Location of the legend."
    )
    legend_click_policy: str = Field("hide", description="Legend click policy.")
