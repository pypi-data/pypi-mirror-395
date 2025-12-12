# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
Module for processing and transforming data for heatmap and other plot types
in the quantify plotting monitor service.

Provides functions to reshape, interpolate, and prepare data for visualization,
including support for uniform grids, uniform settables, and interpolation.
"""

from collections.abc import Sequence
import logging
from typing import Any

from quantify.visualization.plotmon.services.data_processors.heatmap_processor import (
    process_heatmap_data,
)
from quantify.visualization.plotmon.utils.communication import ParamInfo
from quantify.visualization.plotmon.utils.figures import HeatmapConfig, PlotType


def process(
    plot_type: PlotType, data: dict[str, Sequence[Any]], config: ParamInfo
) -> dict[str, Sequence[Any]]:
    """
    Process incoming data based on plot type and configuration.
    Currently, only heatmap requires special processing.
    """
    if plot_type == PlotType.HEATMAP:
        if not isinstance(config, HeatmapConfig):
            raise ValueError(
                f"Config must be an instance of HeatmapConfig for heatmap plots, "
                f"instead was type {type(config)}",
            )
        heatmap_data = process_heatmap_data(data, config)
        return heatmap_data
    if plot_type == PlotType.ONE_D:
        for k, v in data.items():
            if not isinstance(v, list):
                data[k] = [v]
    return data


def extract_data(
    old_data: dict[int, dict[str, Sequence[Any]]],
    plot_type: PlotType,
    config: ParamInfo,
) -> dict[str, Sequence[Any]]:
    """
    Extract and combine data from old and new data dictionaries.
    This is particularly useful for heatmaps where we want to accumulate data over time.
    """
    data = {}

    prev_index = None
    for idx, value in sorted(old_data.items(), key=lambda item: int(item[0])):
        index = int(idx)
        if prev_index is None:
            prev_index = index - 1
        elif index != prev_index + 1:
            # Log a warning if indices are not sequential
            logging.info(
                "Non-sequential indices in cached data for %s: %s followed by %s",
                old_data,
                prev_index,
                index,
            )

        prev_index = index
        for k, v in value.items():
            if plot_type == PlotType.ONE_D:
                data.setdefault(k, []).append(v)
                continue
            if plot_type == PlotType.HEATMAP and isinstance(config, HeatmapConfig):
                data.setdefault(k, []).append(v)

    return data
