import xarray as xr

from quantify.measurement.services.plot_config import get_config_from_dataset
from quantify.visualization.plotmon.utils.communication import PlotmonConfig
from quantify.visualization.plotmon.utils.figures import HeatmapConfig, OneDFigureConfig


def test_get_config_from_dataset_basic():
    # Create mock coordinates and data variables
    coords = {
        "x": xr.DataArray(
            [1, 2, 3], attrs={"name": "x", "long_name": "Frequency", "units": "Hz"}
        ),
    }
    data_vars = {
        "y": xr.DataArray(
            [10, 20, 30], attrs={"name": "y", "long_name": "Voltage", "units": "V"}
        ),
    }
    attrs = {"name": "test_experiment"}
    ds = xr.Dataset(data_vars=data_vars, coords=coords, attrs=attrs)

    config = get_config_from_dataset(ds, data_source_name="test_source")

    assert isinstance(config, PlotmonConfig)
    assert config.data_source_name == "test_source"
    assert config.title == "test_experiment"
    assert len(config.graph_configs) == 1
    assert isinstance(config.graph_configs[0][0], OneDFigureConfig)
    assert config.graph_configs[0][0].x_label == "Frequency"
    assert config.graph_configs[0][0].y_label == "Voltage"


def test_two_by_two_grid():
    coords = {
        "x": xr.DataArray(
            [1, 2, 3], attrs={"name": "x", "long_name": "X-axis", "units": "units"}
        ),
        "x2": xr.DataArray(
            [1, 2, 3], attrs={"name": "x2", "long_name": "X2-axis", "units": "units"}
        ),
    }
    data_vars = {
        "y": xr.DataArray(
            [10, 20, 30], attrs={"name": "y", "long_name": "Y-axis", "units": "units"}
        ),
        "y2": xr.DataArray(
            [15, 25, 35], attrs={"name": "y2", "long_name": "Y2-axis", "units": "units"}
        ),
    }
    ds = xr.Dataset(
        data_vars=data_vars,
        coords=coords,
        attrs={
            "grid_2d": True,
            "grid_2d_uniformly_spaced": True,
            "1d_2_settables_uniformly_spaced": True,
        },
    )

    config = get_config_from_dataset(ds, data_source_name="test_source")

    assert len(config.graph_configs) == 3  # 2 rows of 1D plots and 1 heatmap
    assert len(config.graph_configs[0]) == 2  # First row has 2 plots
    assert len(config.graph_configs[1]) == 2  # Second row has 2 plots
    # In column x axis has the same x_key
    assert config.graph_configs[0][0].x_key == "x"
    assert config.graph_configs[1][0].x_key == "x"
    # In row y axis has the same y_key
    assert config.graph_configs[0][0].y_key == "y"
    assert config.graph_configs[0][1].y_key == "y"
    # Test heatmap creation
    assert isinstance(config.graph_configs[2][0], HeatmapConfig)


def test_three_settable_with_no_heatmap():
    coords = {
        "x": xr.DataArray(
            [1, 2, 3], attrs={"name": "x", "long_name": "X-axis", "units": "units"}
        ),
        "x2": xr.DataArray(
            [1, 2, 3], attrs={"name": "x2", "long_name": "X2-axis", "units": "units"}
        ),
        "x3": xr.DataArray(
            [1, 2, 3], attrs={"name": "x3", "long_name": "X3-axis", "units": "units"}
        ),
    }
    data_vars = {
        "y": xr.DataArray(
            [10, 20, 30], attrs={"name": "y", "long_name": "Y-axis", "units": "units"}
        ),
        "y2": xr.DataArray(
            [15, 25, 35], attrs={"name": "y2", "long_name": "Y2-axis", "units": "units"}
        ),
    }
    ds = xr.Dataset(data_vars=data_vars, coords=coords)

    config = get_config_from_dataset(ds, data_source_name="test_source")

    assert len(config.graph_configs) == 2
    assert len(config.graph_configs[0]) == 3
    assert len(config.graph_configs[1]) == 3
    # In column x axis has the same x_key
    assert config.graph_configs[0][0].x_key == "x"
    assert config.graph_configs[1][0].x_key == "x"
    # In row y axis has the same y_key
    assert config.graph_configs[0][0].y_key == "y"
    assert config.graph_configs[0][1].y_key == "y"
