# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Abstract base class for figure builders."""

from abc import ABC, abstractmethod

from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.plotting import figure

from quantify.visualization.plotmon.utils.communication import ParamInfo
from quantify.visualization.plotmon.utils.tuid_data import TuidData


class BaseFigureBuilder(ABC):
    """Abstract base class for building different types of figures."""

    @abstractmethod
    def build_figure(
        self,
        config: ParamInfo,
        sources: dict[str, ColumnDataSource],
        tuid_data: TuidData,
        ranges: dict[str, DataRange1d],
        fig: figure | None,
    ) -> figure:
        """
        Build a figure based on the provided configuration and
        plot data from the sources.

        Parameters
        ----------
        config : dict
            Configuration dictionary for the figure.
        sources : dict[str, ColumnDataSource]
            Dictionary of data sources to be used in the figure.
        tuid_data : TuidData
            TUID related data for the application.
        ranges : dict[str, Range]
            Shared x and y ranges for the figure.
        fig : figure | None
            Existing figure to update, or None to create a new one.

        Returns
        -------
        A Bokeh Figure object.

        """
