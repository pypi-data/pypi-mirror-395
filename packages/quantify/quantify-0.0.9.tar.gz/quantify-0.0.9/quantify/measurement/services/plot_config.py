# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Services for generating Plotmon configurations from measurement data."""

from collections.abc import Hashable
from typing import Any, TypedDict

import xarray as xr

from quantify.visualization.plotmon.utils.communication import PlotmonConfig
from quantify.visualization.plotmon.utils.figures import HeatmapConfig, OneDFigureConfig


class _AttrsDict(TypedDict):
    """TypedDict for xarray attribute extraction results."""

    long_name: str
    units: str


def _extract_attrs(array: xr.DataArray) -> _AttrsDict:
    """Extracts name, long_name, and units from xarray attributes."""
    long_name = str(array.attrs.get("long_name", ""))
    units = str(array.attrs.get("units", ""))
    return {"long_name": long_name, "units": units}


def _create_one_d_figures(
    gettable_key: str,
    gettable_array: xr.DataArray,
    settables: list[tuple[Hashable, Any]],
) -> list[OneDFigureConfig]:
    """Creates 1D figure configs for a gettable against all settables."""
    gettable_attrs = _extract_attrs(gettable_array)
    configs = []
    for settable_key, settable_array in settables:
        settable_attrs = _extract_attrs(settable_array)
        config = OneDFigureConfig(
            plot_name=f"{settable_key}_{gettable_key}",
            x_key=settable_key,
            y_key=gettable_key,
            title=f"{gettable_attrs['long_name']} vs {settable_attrs['long_name']}",
            x_label=settable_attrs["long_name"],
            y_label=gettable_attrs["long_name"],
            x_units=settable_attrs["units"],
            y_units=gettable_attrs["units"],
        )  # type: ignore
        configs.append(config)
    return configs


def _create_heatmap_figures(
    gettable_items: list[tuple[str, Any]],
    settable_items: list[tuple[Hashable, Any]],
    grid_2d: bool,
    grid_2d_uniformly_spaced: bool,
    settables_uniformly_spaced: bool,
) -> list[HeatmapConfig]:
    """Creates heatmap configs for each gettable against two settables."""
    (settable_key_1, settable_array_1) = settable_items[0]
    (settable_key_2, settable_array_2) = settable_items[1]
    settable_attrs_1 = _extract_attrs(settable_array_1)
    settable_attrs_2 = _extract_attrs(settable_array_2)
    configs = []
    for gettable_key, gettable_array in gettable_items:
        gettable_attrs = _extract_attrs(gettable_array)
        config = HeatmapConfig(
            plot_name=f"heatmap_{gettable_key}",
            x_key=settable_key_1,
            y_key=settable_key_2,
            image_key=gettable_key,
            title=f"{gettable_attrs['long_name']}",
            x_label=settable_attrs_1["long_name"],
            y_label=settable_attrs_2["long_name"],
            z_label=gettable_attrs["long_name"],
            x_units=settable_attrs_1["units"],
            y_units=settable_attrs_2["units"],
            z_units=gettable_attrs["units"],
            grid_2d=grid_2d,
            grid_2d_uniformly_spaced=grid_2d_uniformly_spaced,
            one_d_2_settables_uniformly_spaced=settables_uniformly_spaced,
        )  # type: ignore
        configs.append(config)
    return configs


def get_config_from_dataset(
    dataset: xr.Dataset, data_source_name: str
) -> PlotmonConfig:
    """
    Generate a PlotmonConfig from an xarray Dataset.
    Each data variable (gettable) is plotted against each coordinate (settable)
    as a 1D plot. If there are exactly two coordinates, a heatmap is also created
    for each data variable against the two coordinates.

    Args:
        dataset: The xarray Dataset containing data variables and coordinates.
        data_source_name: The name of the data source for Plotmon.

    Returns:
        A PlotmonConfig object with the generated plot configurations.

    """
    settables = list(dataset.coords.items())  # List of (coord_name, DataArray)
    gettables = list(dataset.data_vars.items())  # List of (var_name, DataArray)

    graph_configs: list[list[Any]] = [
        _create_one_d_figures(gettable_key, gettable_array, settables)
        for gettable_key, gettable_array in gettables
    ]

    if len(settables) == 2:
        grid_2d = dataset.grid_2d
        grid_2d_uniformly_spaced = dataset.grid_2d_uniformly_spaced
        settables_uniformly_spaced = dataset.attrs["1d_2_settables_uniformly_spaced"]
        graph_configs.append(
            _create_heatmap_figures(
                gettables,
                settables,
                grid_2d,
                grid_2d_uniformly_spaced,
                settables_uniformly_spaced,
            )
        )

    return PlotmonConfig(
        graph_configs=graph_configs,
        data_source_name=data_source_name,
        title=str(dataset.attrs.get("name", "experiment")),
    )
