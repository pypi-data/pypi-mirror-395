import contextlib
from unittest import mock

import pytest

from quantify.visualization.plotmon.plotmon_app import PlotmonApp
from quantify.visualization.plotmon.utils.commands import CommandType
from quantify.visualization.plotmon.utils.communication import PlotmonConfig
from quantify.visualization.plotmon.utils.figures import OneDFigureConfig, PlotType


@pytest.fixture
def mock_config():
    return PlotmonConfig(
        graph_configs=[
            [
                OneDFigureConfig(
                    plot_name="test_plot", plot_type="1d", x_key="x", y_key="y"
                )
            ]
        ],
        data_source_name="ds",
    )


@pytest.fixture
def mock_services():
    cache = mock.Mock()
    cache.get.return_value = {}
    cache.get_all.return_value = {}
    cache.set.return_value = None
    return mock.Mock(cache=cache)


@pytest.fixture
def app(mock_config, mock_services):
    # Pass the cache from mock_services and the data_source_name from mock_config
    application = PlotmonApp(
        cache=mock_services.cache,
        data_source_name=mock_config.data_source_name,
    )
    application.config = mock_config
    return application


def test_modify_document_sets_layout_and_callbacks(app):
    doc = mock.Mock()
    app.session_manager.get_doc_and_sources = mock.Mock(return_value=(doc, {}, None))
    app.session_manager.get_current_session_id = mock.Mock(return_value=1)
    app.session_manager.get_layout = mock.Mock(return_value=mock.Mock())
    app.session_manager.set_layout = mock.Mock(return_value=None)
    app.serve = mock.Mock()
    app.initialize_sources_from_cache = mock.Mock()
    app._check_for_base_sources = mock.Mock()
    app.modify_document(doc)
    app.serve.assert_called()
    app.initialize_sources_from_cache.assert_called()


def test_enqueue_data_puts_to_queue(app):
    app.data_queue = mock.Mock()
    app.enqueue_data("plot", "tuid", {"x": [1]})
    app.data_queue.put.assert_called_with(("plot", "tuid", {"x": [1]}))


def test_start_experiment_updates_tuid_and_cache(app, mock_services):
    app._tuid_data.tuids = set()
    app._tuid_data.selected_tuid = {}
    app.session_manager.update_sources = mock.Mock()
    app._re_render = mock.Mock()
    mock_services.cache.get.return_value = {}
    mock_services.cache.set.return_value = None
    app.start_experiment("tuid1", "2024-01-01")
    assert "tuid1" in app._tuid_data.tuids
    assert app._tuid_data.active_tuid == "tuid1"
    app.session_manager.update_sources.assert_called()
    app._re_render.assert_called()
    mock_services.cache.set.assert_called()


def test_end_experiment_updates_selected_and_cache(app, mock_services):
    app._tuid_data.selected_tuid = {}
    app.session_manager.get_all_session_ids = mock.Mock(return_value=[1, 2])
    app._re_render = mock.Mock()
    mock_services.cache.get.return_value = {}
    mock_services.cache.set.return_value = None
    app.end_experiment("tuid2", "2024-01-02")
    assert app._tuid_data.selected_tuid[-1] == "tuid2"
    assert app._tuid_data.active_tuid == ""
    assert app._tuid_data.selected_tuid[1] == "tuid2"
    assert app._tuid_data.selected_tuid[2] == "tuid2"
    app._re_render.assert_called()
    mock_services.cache.set.assert_called()


def test_get_plot_names_returns_names(app):
    names = app._get_plot_names()
    assert names == ["test_plot"]


def test_get_source_returns_source_and_name(app):
    sources = {"tuid_test_plot": "source_obj"}
    source, name = app._get_source(sources, "test_plot", "tuid")
    assert source == "source_obj"
    assert name == "tuid_test_plot"


def test_make_cache_key_and_source_name(app):
    assert app._make_cache_key("plot", "tuid") == "ds_tuid_plot"
    assert app._make_source_name("tuid", "plot") == "tuid_plot"


def test_get_plot_type_returns_type_and_config(app):
    plot_type, config = app._get_plot_type("test_plot")
    assert plot_type.name.lower() == "one_d"
    assert config.plot_name == "test_plot"


def test_get_plot_type_raises_for_unknown(app):
    with pytest.raises(ValueError):
        app._get_plot_type("unknown_plot")


def test_get_current_timestamp_format(app):
    ts = app.get_current_timestamp()
    assert isinstance(ts, str)
    assert "_" in ts


def test_add_event_next_tick_calls_next_tick(app):
    doc = mock.Mock()
    app.session_manager.all_sessions = mock.Mock(return_value=[(1, doc)])
    app._process_event = mock.Mock()
    app.add_event_next_tick("event", "data")
    doc.add_next_tick_callback.assert_called()


def test_process_event_calls_start_and_stop(app):
    app.start_experiment = mock.Mock()
    app.end_experiment = mock.Mock()
    app.get_current_timestamp = mock.Mock(return_value="ts")
    app._process_event(CommandType.START, "data")
    app.start_experiment.assert_called_with("data", "ts")
    app._process_event(CommandType.STOP, "data")
    app.end_experiment.assert_called_with("data", "ts")


def test_check_for_base_sources_creates_sources(app):
    app.cache.get.return_value = {"now": ("tuid", mock.Mock(name="STARTED"))}
    app._tuid_data.tuids = set()
    app.session_manager.update_sources = mock.Mock()
    # Use a config with string keys, not mocks
    app.config = PlotmonConfig(
        graph_configs=[
            [
                OneDFigureConfig(
                    plot_name="test_plot", plot_type="1d", x_key="x", y_key="y"
                )
            ]
        ]
    )
    app._check_for_base_sources()
    app.session_manager.update_sources.assert_called()


def test_initialize_sources_from_cache_sets_source_data(app):
    # Prepare mock sources and tuids
    tuid = "tuid1"
    plot_name = "test_plot"
    app._tuid_data.tuids = {tuid}
    sources = {f"{tuid}_{plot_name}": mock.Mock(spec=["data"])}

    # Prepare mock cache and configs
    app._make_cache_key(plot_name, tuid)
    cached_data = {"x": [1, 2, 3], "y": [4, 5, 6]}
    app.cache.get = mock.Mock(return_value=cached_data)
    app._get_plot_names = mock.Mock(return_value=[plot_name])
    app._get_source = mock.Mock(
        return_value=(sources[f"{tuid}_{plot_name}"], f"{tuid}_{plot_name}")
    )
    app._get_plot_type = mock.Mock(
        return_value=(
            PlotType.ONE_D,
            {"plot_name": plot_name, "plot_type": "1d", "x_key": "x"},
        )
    )

    # Patch data_processor methods
    with (
        mock.patch(
            "quantify.visualization.plotmon.services.data_processor.extract_data",
            return_value=cached_data,
        ) as extract_data_mock,
        mock.patch(
            "quantify.visualization.plotmon.services.data_processor.process",
            return_value=cached_data,
        ) as process_mock,
    ):
        app.initialize_sources_from_cache(sources)
        # Check that source.data was set
        assert sources[f"{tuid}_{plot_name}"].data == cached_data
        extract_data_mock.assert_called_once()
        process_mock.assert_called_once()


def test_check_for_update_empty_queue(app):
    doc = mock.Mock()
    app.data_queue = mock.Mock()
    app.data_queue.qsize.return_value = 0
    app.data_queue.empty.return_value = True
    app.data_queue.queue = []
    app.session_manager.all_sessions = mock.Mock(return_value=[])
    doc.add_next_tick_callback = mock.Mock()
    app.check_for_update()


def test_check_for_update_queue_overflow(app):
    doc = mock.Mock()
    app.data_queue = mock.Mock()
    app.data_queue.qsize.return_value = app.MAX_QUEUE_ITEMS + 1
    app.data_queue.empty.return_value = False
    app.data_queue.queue = mock.Mock()
    app.data_queue.mutex = contextlib.nullcontext()
    app.data_queue.queue.clear = mock.Mock()
    app.session_manager.all_sessions = mock.Mock(return_value=[(1, doc)])
    app.session_manager.get_sources = mock.Mock(return_value={"plot": mock.Mock()})
    app.initialize_sources_from_cache = mock.Mock()
    app._safe_callback = mock.Mock()
    app.data_queue.get.return_value = ("plot", "tuid", {"x": [1]})
    app.check_for_update()
    app.data_queue.queue.clear.assert_called()
    app._safe_callback.assert_called()


def test_check_for_update_normal_update(app):
    doc = mock.Mock()
    app.data_queue = mock.Mock()
    app.data_queue.qsize.return_value = 1

    # Use a side_effect that returns False once, then always True
    def empty_side_effect():
        calls = [False, True]

        def inner():
            return calls.pop(0) if calls else True

        return inner

    app.data_queue.empty.side_effect = empty_side_effect()
    app.data_queue.get.return_value = ("plot", "tuid", {"x": [1]})
    app.data_queue.task_done = mock.Mock()
    app.session_manager.all_sessions = mock.Mock(return_value=[(1, doc)])
    app._safe_callback = mock.Mock()
    app.check_for_update()
    app._safe_callback.assert_called()
    app.data_queue.task_done.assert_called()


def test_check_for_update_leftover_tasks(app):
    doc = mock.Mock()
    app.data_queue = mock.Mock()
    app.data_queue.qsize.return_value = 2

    # Use a side_effect that returns False twice, then always True
    def empty_side_effect():
        calls = [False, False, True]

        def inner():
            return calls.pop(0) if calls else True

        return inner

    app.data_queue.empty.side_effect = empty_side_effect()
    app.data_queue.get.side_effect = [
        ("plot", "tuid", {"x": [1]}),
        ("plot", "tuid", {"x": [2]}),
    ]
    app.data_queue.task_done = mock.Mock()
    app.session_manager.all_sessions = mock.Mock(return_value=[(1, doc)])
    app._safe_callback = mock.Mock()
    doc.add_next_tick_callback = mock.Mock()
    app.check_for_update()
    assert app.data_queue.task_done.call_count == 2
