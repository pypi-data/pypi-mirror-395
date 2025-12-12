# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Factory class to get the appropriate figure builder based on plot type."""

from quantify.visualization.plotmon.services.figure_builder.base_figure_builder import (
    BaseFigureBuilder,
)
from quantify.visualization.plotmon.services.figure_builder.heatmap_builder import (
    HeatmapFigureBuilder,
)
from quantify.visualization.plotmon.services.figure_builder.one_d_figure_builder import (  # noqa: E501
    OneDFigureBuilder,
)
from quantify.visualization.plotmon.utils.figures import PlotType


class FigureBuilderFactory:
    """Factory class to get the appropriate figure builder based on plot type."""

    _builders = {
        PlotType.ONE_D: OneDFigureBuilder(),
        PlotType.HEATMAP: HeatmapFigureBuilder(),
        # PlotType.ONE_D_MULTILINE: OneDMultilineFigureBuilder(),
        # PlotType.TWO_D: TwoDFigureBuilder(),
    }

    @classmethod
    def get_builder(cls, plot_type: PlotType) -> BaseFigureBuilder:
        """
        Get the appropriate figure builder based on the plot type.

        Parameters
        ----------
        plot_type : PlotType
            The type of plot for which the figure builder is requested.

        Returns
        -------
            BaseFigureBuilder
                An instance of a figure builder corresponding to the plot type.

        """
        return cls._builders[plot_type]
