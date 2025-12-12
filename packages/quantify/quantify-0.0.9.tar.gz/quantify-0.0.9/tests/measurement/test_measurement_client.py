import random
import string
from unittest import mock

import numpy as np
import pytest
import xarray as xr

from quantify.measurement.client import MeasurementClient
from quantify.measurement.control import MeasurementControl
from quantify.measurement.services.ui_tool import UITool
from quantify.visualization.plotmon.utils.commands import CommandType


@pytest.fixture
def uitool():
    class DummyUITool(UITool):
        def callback(self, *args, **kwargs):
            pass  # Dummy implementation

    return DummyUITool()


@pytest.fixture
def client_fixture(monkeypatch, uitool):
    # Patch all MeasurementControl methods used in tests to do nothing
    monkeypatch.setattr(MeasurementControl, "_init", lambda _, __: None)
    monkeypatch.setattr(MeasurementControl, "_finish", lambda _: None)
    # You can patch more methods as needed

    # Generate a random string for the name

    random_name = "".join(random.choices(string.ascii_letters, k=10))
    mc = MeasurementControl(name=random_name)
    return MeasurementClient(mc=mc, ui_tool=uitool)


def make_test_dataset_1d():
    """Create a simple 1D xarray.Dataset for testing."""
    coords = {"x": np.arange(5)}
    data_vars = {"y": ("x", np.arange(5) * 2)}
    attrs = {"tuid": "test_tuid"}
    return xr.Dataset(data_vars, coords=coords, attrs=attrs)


def make_test_dataset_2d():
    """Create a proper 2D xarray.Dataset for testing heatmap updates."""
    x = np.arange(3)
    y = np.arange(4)
    z = np.arange(12).reshape(3, 4)
    coords = {"x": x, "y": y}
    data_vars = {"z": (("x", "y"), z)}
    attrs = {"tuid": "test_tuid"}
    return xr.Dataset(data_vars=data_vars, coords=coords, attrs=attrs)


def test_init_with_no_dataset_logs_warning(client_fixture, caplog):
    client_fixture._dataset = None
    with caplog.at_level("WARNING"):
        client_fixture._init("test_experiment")
    assert "Dataset not found." in caplog.text


def test_init_reconfigures_graph_and_starts_experiment(client_fixture):
    client_fixture.mc._dataset = xr.Dataset(attrs={"tuid": "1234"})
    client_fixture.mc._last_experiment_name = "old_experiment"
    with mock.patch.object(client_fixture, "_send_message") as mock_send:
        client_fixture._init("test_experiment")
        # Should send graph config and start messages
        assert mock_send.call_count == 2
        graph_msg = mock_send.call_args_list[0][0][0]
        start_msg = mock_send.call_args_list[1][0][0]
        assert graph_msg.event.event_type == CommandType.GRAPH_CONFIG
        assert start_msg.event.event_type == CommandType.START
        assert client_fixture._last_experiment_name == "test_experiment"


def test_init_does_not_reconfigure_if_same_experiment(client_fixture):
    client_fixture.mc._dataset = xr.Dataset(attrs={"tuid": "1234"})
    client_fixture._last_experiment_name = "test_experiment"
    with mock.patch.object(client_fixture, "_send_message") as mock_send:
        client_fixture._init("test_experiment")
        # Should only send start message
        assert mock_send.call_count == 1
        start_msg = mock_send.call_args[0][0]
        assert start_msg.event.event_type == CommandType.START


def test_finish_with_no_dataset_logs_warning(client_fixture, caplog):
    client_fixture.mc._dataset = None
    client_fixture._last_experiment_name = "test_experiment"
    with caplog.at_level("WARNING"):
        client_fixture._finish()
    assert "Dataset not found." in caplog.text


def test_finish_sends_stop_message(client_fixture):
    client_fixture.mc._dataset = xr.Dataset(attrs={"tuid": "1234"})
    with mock.patch.object(client_fixture, "_send_message") as mock_send:
        client_fixture._finish()
        assert mock_send.call_count == 1
        stop_msg = mock_send.call_args[0][0]
        assert stop_msg.event.event_type == CommandType.STOP


def test_update_sends_update_data_messages_1d(client_fixture):
    client_fixture.mc._dataset = make_test_dataset_1d()
    client_fixture.mc._nr_acquired_values = 5
    client_fixture.mc._batch_size_last = 2

    with mock.patch.object(client_fixture, "_send_message") as mock_send:
        client_fixture._update()
        update_calls = [
            call
            for call in mock_send.call_args_list
            if call[0][0].event.event_type == CommandType.UPDATE_DATA
        ]
        assert len(update_calls) > 0
        for call in update_calls:
            msg = call[0][0]
            assert msg.event.event_type == CommandType.UPDATE_DATA
            assert hasattr(msg.event, "plot_name")
            assert hasattr(msg.event, "data")


def test_update_sends_heatmap_update_message_2d(client_fixture):
    client_fixture.mc._dataset = make_test_dataset_2d()
    client_fixture.mc._nr_acquired_values = 12
    client_fixture.mc._batch_size_last = 4

    with mock.patch.object(client_fixture, "_send_message") as mock_send:
        client_fixture._update()
        update_calls = [
            call
            for call in mock_send.call_args_list
            if call[0][0].event.event_type == CommandType.UPDATE_DATA
        ]
        assert len(update_calls) > 0
        msg = update_calls[-1][0][0]
        assert msg.event.event_type == CommandType.UPDATE_DATA
        assert msg.event.plot_name.startswith("heatmap_")
