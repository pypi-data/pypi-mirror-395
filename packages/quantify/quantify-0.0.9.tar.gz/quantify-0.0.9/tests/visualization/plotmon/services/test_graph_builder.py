# File: /home/kiki/quantify/tests/visualization/plotmon/services/test_graph_builder.py

from unittest import mock

from bokeh.models import Column, ColumnDataSource, DataRange1d, Row
from bokeh.models.widgets import DataTable
from bokeh.plotting import figure
import pytest

from quantify.visualization.plotmon.services import graph_builder
from quantify.visualization.plotmon.utils.communication import PlotmonConfig
from quantify.visualization.plotmon.utils.figures import OneDFigureConfig
from quantify.visualization.plotmon.utils.tuid_data import TuidData


class DummyFigureBuilder:
    def build_figure(self, config, *_):
        f = mock.Mock(spec=figure)
        f.id = f"{config.plot_name}_id"
        return f


@pytest.fixture
def patch_figure_builder(monkeypatch):
    monkeypatch.setattr(
        graph_builder.FigureBuilderFactory,
        "get_builder",
        lambda _: DummyFigureBuilder(),
    )


@pytest.fixture
def configs():
    return PlotmonConfig(
        graph_configs=[
            [
                OneDFigureConfig(
                    plot_name="plot1", plot_type="1d", x_key="x", y_key="y"
                ),
                OneDFigureConfig(
                    plot_name="plot2", plot_type="1d", x_key="x2", y_key="y2"
                ),
            ]
        ],
        data_source_name="ds",
    )


def test_make_source_name_empty_tuid():
    assert graph_builder._make_source_name("", "plot1") == "plot1"


def test_make_source_name_with_tuid():
    assert graph_builder._make_source_name("TUID123", "plot1") == "TUID123_plot1"


def test_create_shared_ranges_basic(configs):
    ranges = graph_builder._create_shared_ranges(configs.graph_configs)
    assert isinstance(ranges["x"], DataRange1d)
    assert isinstance(ranges["y"], DataRange1d)
    assert isinstance(ranges["x2"], DataRange1d)
    assert isinstance(ranges["y2"], DataRange1d)


def test_create_rows_creates_rows(configs):
    sources = {
        "tuid_1_plot1": ColumnDataSource(data={"x": [], "y": [], "tuid": []}),
        "tuid_2_plot1": ColumnDataSource(data={"x": [], "y": [], "tuid": []}),
        "tuid_1_plot2": ColumnDataSource(data={"x2": [], "y2": [], "tuid": []}),
        "tuid_2_plot2": ColumnDataSource(data={"x2": [], "y2": [], "tuid": []}),
    }
    tuid_data = TuidData(
        tuids=set(["tuid_1", "tuid_2"]),
        selected_tuid={-1: "tuid_1"},
        active_tuid="",
        session_id=-1,
    )
    rows = graph_builder._create_rows(configs.graph_configs, sources, tuid_data)
    assert isinstance(rows, list)
    assert all(isinstance(row, Row) for row in rows)
    assert len(rows) == 1


def test_build_figure_calls_builder(monkeypatch):
    monkeypatch.setattr(
        graph_builder.FigureBuilderFactory,
        "get_builder",
        lambda _: DummyFigureBuilder(),
    )
    config = OneDFigureConfig(plot_name="plot1", plot_type="1d", x_key="x", y_key="y")
    sources = {"plot1_plot1": ColumnDataSource(data={"x": [], "y": [], "tuid": []})}
    tuid_data = TuidData(
        tuids=set(["plot1"]), selected_tuid={-1: "plot1"}, active_tuid="", session_id=-1
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    fig = None
    result = graph_builder._build_figure(config, sources, tuid_data, ranges, fig)
    assert hasattr(result, "id")
    assert result.id == "plot1_id"


def test_build_layout_returns_column(monkeypatch, configs):
    dummy_table = DataTable()
    monkeypatch.setattr(
        graph_builder.table_builder, "create_table", lambda *_, **__: dummy_table
    )
    # The key should be "tuid_1_plot1" to match what build_layout expects
    sources = {
        "tuid_1_plot1": ColumnDataSource(data={"x": [], "y": [], "tuid": []}),
        "tuid_1_plot2": ColumnDataSource(data={"x2": [], "y2": [], "tuid": []}),
    }
    tuid_data = TuidData(
        tuids=["tuid_1"],
        selected_tuid={-1: "tuid_1"},
        active_tuid="",
        session_id=-1,
    )
    meta_data = {"tuid_1": {}}

    def on_select():
        pass

    # config: PlotmonConfig,
    # sources: dict[str, ColumnDataSource],
    # tuid_data: TuidData,
    # meta_data: dict[str, dict],
    # on_select: Callable,
    # on_history_select: Callable,
    # titles: dict[int, str],
    layout = graph_builder.build_layout(
        configs, sources, tuid_data, meta_data, on_select, on_select, {}
    )
    assert isinstance(layout, Column)
    assert any(isinstance(child, Column) for child in layout.children)


def test_create_sources_raises_on_invalid_plot_type(configs):
    configs.graph_configs[0][0].plot_type = "invalid_type"
    with pytest.raises(ValueError):
        graph_builder.create_sources(configs.graph_configs, tuid="TUID")
