# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Utility functions for the instrument coordinator and components."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
from qcodes.parameters.parameter import Parameter
import xarray
from xarray import DataArray

if TYPE_CHECKING:
    from collections.abc import Hashable

    from qcodes.instrument.base import InstrumentBase

logger = logging.getLogger(__name__)


def search_settable_param(
    instrument: InstrumentBase, nested_parameter_name: str
) -> Parameter:
    """
    Searches for a settable parameter in nested instrument hierarchies.

    For example `instrument.submodule_1.channel_1.parameter.`

    Parameters
    ----------
    instrument:
        The root QCoDeS instrument where the parameter resides.
    nested_parameter_name:
        Hierarchical nested parameter name.

    Returns
    -------
    Parameter
    """
    root_obj: object = instrument
    parts = nested_parameter_name.split(".")

    for part in parts:
        found = False
        for attr_name in ("parameters", "submodules", "functions"):
            attr = getattr(root_obj, attr_name, None)
            if isinstance(attr, dict) and part in attr:
                root_obj = attr[part]
                found = True
                break
        if not found:
            raise ValueError(
                f'Could not find settable parameter "{nested_parameter_name}" '
                f'in instrument "{instrument}"'
            )

    if isinstance(root_obj, Parameter):
        return root_obj

    # We only return a Parameter. If the resolved object is not a Parameter
    # (e.g., a callable), raise and let the caller handle it.
    raise ValueError(
        f'"{nested_parameter_name}" in instrument "{instrument}" is not a Parameter'
    )


def parameter_value_same_as_cache(
    instrument: InstrumentBase, parameter_name: str, val: object
) -> bool:
    """
    Returns whether the value of a QCoDeS parameter is the same as the value in cache.

    Parameters
    ----------
    instrument:
        The QCoDeS instrument to set the parameter on.
    parameter_name:
        Name of the parameter to set.
    val:
        Value to set it to.

    Returns
    -------
    bool

    """
    parameter = search_settable_param(
        instrument=instrument, nested_parameter_name=parameter_name
    )
    # parameter.cache() throws for non-gettable parameters if the cache is invalid.
    # This order prevents the exception.
    return parameter.cache.valid and parameter.cache() == val


def lazy_set(instrument: InstrumentBase, parameter_name: str, val: object) -> None:
    """
    Set the value of a QCoDeS parameter only if it is different from the value in cache.

    Parameters
    ----------
    instrument:
        The QCoDeS instrument to set the parameter on.
    parameter_name:
        Name of the parameter to set.
    val:
        Value to set it to.

    """
    parameter = search_settable_param(
        instrument=instrument, nested_parameter_name=parameter_name
    )
    # parameter.cache() throws for non-gettable parameters if the cache is invalid.
    # This order prevents the exception.
    if not parameter_value_same_as_cache(instrument, parameter_name, val):
        parameter(val)
    else:
        logger.info(
            f"Lazy set skipped setting parameter {instrument.name}.{parameter_name}"
        )


def check_already_existing_acquisition(
    new_dataset: xarray.Dataset, current_dataset: xarray.Dataset
) -> None:
    """
    Verifies non-overlapping data in new_dataset and current_dataset.

    If there is, it will raise an error.

    Parameters
    ----------
    new_dataset
        New dataset.
    current_dataset
        Current dataset.

    """
    conflicting_indices_str = []
    for acq_channel, _data_array in new_dataset.items():
        if acq_channel not in current_dataset:
            continue
        # The return values are two `DataArray`s with only coordinates
        # which are common in the inputs.
        common_0, common_1 = xarray.align(
            _data_array, current_dataset[acq_channel], join="inner"
        )

        # We need to check if the values are `math.nan`, because if they are,
        # that means there is no value at that position (xarray standard).
        def mask_func(x: float, y: float) -> int:
            return 0 if np.isnan(x) or np.isnan(y) else 1

        if len(common_0) and len(common_1):
            conflict_mask = xarray.apply_ufunc(
                mask_func, common_0, common_1, vectorize=True
            )
            for conflict in conflict_mask:
                if conflict.values != [1]:
                    continue
                conflicting_coords = [("acq_channel", acq_channel)]
                conflicting_coords += [
                    (dim, conflict[dim].values) for dim in conflict.coords
                ]
                coords_str = [f"{dim}={coord}" for dim, coord in conflicting_coords]
                conflicting_indices_str.append("; ".join(coords_str))

    if conflicting_indices_str:
        conflicting_indices_str = "\n".join(conflicting_indices_str)
        raise RuntimeError(
            "Attempting to gather acquisitions. "
            "Make sure an acq_channel, acq_index corresponds to not more than "
            "one acquisition.\n"
            "The following indices are defined multiple times.\n"
            f"{conflicting_indices_str}"
        )


def add_acquisition_coords_binned(
    data_array: DataArray,
    coords: list[dict],
    acq_index_dim_name: Hashable,
) -> None:
    """
    Modifies the argument data_array,
    it adds the coords to it.

    This function only applies to binned acquisitions.

    Coordinates in the acquisition channels data is a list of dictionary,
    and each dictionary is a coordinate. In the return data however,
    it should be a dict, for each coords key it should store a list of the values.

    xarray requires the coordinates to specify on which xarray dimension
    they are applied to. That's why the acq_index_dim_name is used here.
    Note: dimension and coords are different.
    """
    data_array_coords = {}
    len_acq_indices = len(data_array[acq_index_dim_name].values)

    all_keys = set()
    for coord_dict in coords:
        all_keys.update(coord_dict.keys())

    for key in all_keys:
        data_array_coords[key] = (acq_index_dim_name, [np.nan] * len_acq_indices)

    for i, acq_index in enumerate(data_array[acq_index_dim_name].values):
        coord_dict = coords[acq_index]
        for key, value in coord_dict.items():
            data_array_coords[key][1][i] = value

    data_array.coords.update(data_array_coords)


def add_acquisition_coords_nonbinned(
    data_array: DataArray,
    coords: dict,
    acq_index_dim_name: Hashable,
) -> None:
    """
    Modifies the argument data_array,
    it adds the coords to it.

    This function only applies to nonbinned acquisitions.

    Coordinates in the acquisition channels data is a dictionary,
    and each dictionary is a coordinate. In the return data however,
    it should be a dict, for each coords key it should store a list of the values.

    xarray requires the coordinates to specify on which xarray dimension
    they are applied to. That's why the acq_index_dim_name is used here.
    Note: dimension and coords are different.
    """
    data_array_coords = {}

    for key, value in coords.items():
        data_array_coords[key] = (acq_index_dim_name, [value])

    data_array.coords.update(data_array_coords)
