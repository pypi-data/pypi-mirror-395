from bokeh.models import ColumnDataSource, DataRange1d, PanTool
from bokeh.plotting import figure
import pytest

from quantify.visualization.plotmon.services.figure_builder.one_d_figure_builder import (  # noqa: E501
    OneDFigureBuilder,
    OneDFigureConfig,
)


@pytest.fixture
def config():
    return OneDFigureConfig()


class DummyTuidData:
    def __init__(self, tuids, selected_tuid=None, active_tuid=None, session_id=None):
        self.tuids = tuids
        self.selected_tuid = selected_tuid or {}
        self.active_tuid = active_tuid
        self.session_id = session_id if session_id is not None else -1


def make_sources(tuids, plot_name, x_key="x", y_key="y"):
    sources = {}
    for tuid in tuids:
        sources[f"{tuid}_{plot_name}"] = ColumnDataSource(
            data={
                x_key: [1, 2, 3],
                y_key: [4, 5, 6],
                "tuid": [tuid] * 3,
            }
        )
    return sources


def test_build_figure_creates_figure(config):
    builder = OneDFigureBuilder()
    tuids = ["tuid1", "tuid2"]
    sources = make_sources(tuids, "generic_plot")
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid=None,
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    fig = builder.build_figure(config, sources, tuid_data, ranges)
    assert isinstance(fig, figure)
    assert fig.title.text == "1D Plot"
    assert len(fig.renderers) > 0


def test_build_figure_highlights_active_tuid(config):
    builder = OneDFigureBuilder()
    tuids = ["tuid1", "tuid2"]
    sources = make_sources(tuids, "generic_plot")
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid="tuid2",
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    fig = builder.build_figure(config, sources, tuid_data, ranges)
    assert isinstance(fig, figure)
    # Check that the legend contains "tuid2"
    legend_labels = []
    for legend in fig.legend:
        for item in legend.items:
            if hasattr(item, "label") and hasattr(item.label, "value"):
                legend_labels.append(item.label.value)
    assert "tuid2" in legend_labels


def test_build_figure_reuses_existing_figure(config):
    builder = OneDFigureBuilder()
    tuids = ["tuid1"]
    sources = make_sources(tuids, "generic_plot")
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid=None,
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    orig_fig = figure()
    # Add a valid renderer and tool
    orig_fig.line([0, 1], [0, 1])
    orig_fig.add_tools(PanTool())
    fig = builder.build_figure(config, sources, tuid_data, ranges, fig=orig_fig)
    assert fig is orig_fig


def test_build_figure_missing_source_raises(config):
    builder = OneDFigureBuilder()
    tuids = ["tuid1"]
    sources = {}  # Missing source
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid=None,
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    with pytest.raises(ValueError):
        builder.build_figure(config, sources, tuid_data, ranges)
