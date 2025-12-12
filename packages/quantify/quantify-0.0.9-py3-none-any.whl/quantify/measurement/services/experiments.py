# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Services for handling experiment-related commands and data."""

from collections.abc import Generator, Hashable
from typing import Any

import numpy as np
import xarray as xr

from quantify.visualization.plotmon.utils.communication import (
    Data,
    StartExperimentMessage,
    StopExperimentMessage,
    UpdateDataMessage,
)


def start_experiment(
    dataset: xr.Dataset, data_source_name: str
) -> StartExperimentMessage:
    """Create a StartExperiment command from an xarray Dataset.

    Args:
        dataset: The xarray Dataset containing the experiment data.
        data_source_name: The name of the data source.

    Returns:
        A StartExperiment command with the dataset's TUID and data source name.

    """
    return StartExperimentMessage(
        tuid=dataset.attrs["tuid"],
        data_source_name=data_source_name,
    )


def stop_experiment(
    dataset: xr.Dataset, data_source_name: str
) -> StopExperimentMessage:
    """Create a StopExperiment command from an xarray Dataset.

    Args:
        dataset: The xarray Dataset containing the experiment data.
        data_source_name: The name of the data source.

    Returns:
        A StopExperiment command with the dataset's TUID and data source name.

    """
    return StopExperimentMessage(
        tuid=dataset.attrs["tuid"],
        data_source_name=data_source_name,
    )


def _get_first_nan_index(array: list[float]) -> int:
    """Return the index of the first NaN in the array, or -1 if none found."""
    nan_mask = np.isnan(array)
    if nan_mask.any():
        return int(np.argmax(nan_mask))
    return -1


def _generate_update_messages(
    settables: list[tuple[Hashable, Any]],
    gettables: list[tuple[str, Any]],
    tuid: str,
    data_source_name: str,
    nr_acquired_values: int,
    batch_size_last: int,
) -> Generator[UpdateDataMessage, None, None]:
    """Generate UpdateDataMessage for 1D plots."""
    nr_val = nr_acquired_values
    batch_size = batch_size_last
    for settable_key, settable_array in settables:
        for gettable_key, gettable_array in gettables:
            plot_name = f"{settable_key}_{gettable_key}"
            first_nan_index = _get_first_nan_index(settable_array.values)
            if first_nan_index != -1:
                pass
            else:
                len(settable_array.values)
            settable_values = settable_array.values[nr_val - batch_size : nr_val]
            gettable_values = gettable_array.values[nr_val - batch_size : nr_val]

            data = Data(
                sequence_ids=list(range(nr_val - batch_size, nr_val)),
                tuid=[tuid] * batch_size,
                **{
                    settable_key: settable_values.tolist(),
                    gettable_key: gettable_values.tolist(),
                },
            )

            if data:
                yield UpdateDataMessage(
                    data_source_name=data_source_name,
                    plot_name=plot_name,
                    data=data,
                    tuid=tuid,
                )


def _generate_heatmap_messages(
    settables: list[tuple[Hashable, Any]],
    gettables: list[tuple[str, Any]],
    tuid: str,
    data_source_name: str,
) -> Generator[UpdateDataMessage, None, None]:
    """Generate UpdateDataMessage for heatmap plots (2D)."""
    (x_key, x_array), (y_key, y_array) = settables
    for gettable_key, gettable_array in gettables:
        plot_name = f"heatmap_{gettable_key}"
        x_values = x_array.values
        y_values = y_array.values
        z_values = gettable_array.values

        data = Data(
            sequence_ids=list(range(len(z_values))),
            tuid=[tuid] * (len(z_values)),
            **{
                x_key: x_values.tolist(),
                y_key: y_values.tolist(),
                gettable_key: z_values.tolist(),
            },
        )

        if data:
            yield UpdateDataMessage(
                data_source_name=data_source_name,
                plot_name=plot_name,
                data=data,
                tuid=tuid,
            )


def update_experiment(
    dataset: xr.Dataset,
    data_source_name: str,
    nr_aquired_values: int,
    batch_size_last: int,
) -> Generator[UpdateDataMessage, None, None]:
    """
    Yields UpdateDataMessage objects for new data only.

    Args:
        dataset: The xarray Dataset containing experiment data.
        data_source_name: The name of the data source.
        nr_aquired_values: The total number of acquired values in the dataset.
        batch_size_last: The number of new values acquired since the last update.

    Yields:
        UpdateDataMessage for each new data chunk.

    """
    settables = list(dataset.coords.items())
    gettables = list(dataset.data_vars.items())
    tuid = dataset.attrs["tuid"]

    # 1D updates
    yield from _generate_update_messages(
        settables, gettables, tuid, data_source_name, nr_aquired_values, batch_size_last
    )

    # 2D heatmap updates (only if there are exactly two coordinates)
    if len(settables) == 2:
        yield from _generate_heatmap_messages(
            settables, gettables, tuid, data_source_name
        )
