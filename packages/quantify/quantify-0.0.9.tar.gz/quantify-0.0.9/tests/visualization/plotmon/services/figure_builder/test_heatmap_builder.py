from bokeh.models import ColumnDataSource, DataRange1d, Title
from bokeh.plotting import figure
import numpy as np
import pytest

from quantify.visualization.plotmon.services.figure_builder.heatmap_builder import (
    HeatmapConfig,
    HeatmapFigureBuilder,
)


@pytest.fixture
def config():
    return HeatmapConfig()


class DummyTuidData:
    def __init__(self, tuids, selected_tuid=None, active_tuid=None, session_id=None):
        self.tuids = tuids
        self.selected_tuid = selected_tuid or {}
        self.active_tuid = active_tuid or ""
        self.session_id = session_id if session_id is not None else -1


def make_sources(
    tuids, plot_name, image_key="image", x_key="x", y_key="y", dw_key="dw", dh_key="dh"
):
    sources = {}
    for tuid in tuids:
        sources[f"{tuid}_{plot_name}"] = ColumnDataSource(
            data={
                image_key: [np.ones((2, 2))],
                x_key: [0],
                y_key: [0],
                dw_key: [1],
                dh_key: [1],
                "tuid": [tuid],
            }
        )
    return sources


def test_select_source_tuid_selected():
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: "tuid1"},
        active_tuid="tuid2",
        session_id=-1,
    )
    tuid = HeatmapFigureBuilder._select_source_tuid(tuid_data)
    assert tuid == "tuid1"


def test_select_source_tuid_active():
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: ""},
        active_tuid="tuid2",
        session_id=-1,
    )
    tuid = HeatmapFigureBuilder._select_source_tuid(tuid_data)
    assert tuid == "tuid2"


def test_select_source_tuid_none():
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: ""},
        active_tuid="",
        session_id=-1,
    )
    tuid = HeatmapFigureBuilder._select_source_tuid(tuid_data)
    assert tuid is None


def test_get_source_found():
    cfg = HeatmapConfig()
    sources = make_sources(["tuid1"], cfg.plot_name)
    source = HeatmapFigureBuilder._get_source("tuid1", cfg, sources)
    assert isinstance(source, ColumnDataSource)
    assert source.data["tuid"][0] == "tuid1"


def test_get_source_missing_returns_placeholder():
    cfg = HeatmapConfig()
    sources = {}
    source = HeatmapFigureBuilder._get_source("tuid1", cfg, sources)
    assert isinstance(source, ColumnDataSource)
    assert np.isnan(source.data[cfg.image_key][0][0, 0])


def test_build_figure_creates_new_figure(config):
    builder = HeatmapFigureBuilder()
    tuids = ["tuid1"]
    sources = make_sources(tuids, "generic_heatmap")
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid="",
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    fig = builder.build_figure(config, sources, tuid_data, ranges)
    assert isinstance(fig, figure)
    assert fig.title.text.startswith("2D Heatmap")
    assert len(fig.renderers) > 0


def test_build_figure_reuses_existing_figure(config):
    builder = HeatmapFigureBuilder()
    tuids = ["tuid1"]
    sources = make_sources(tuids, "generic_heatmap")
    tuid_data = DummyTuidData(
        tuids=tuids,
        selected_tuid={-1: "tuid1"},
        active_tuid="",
        session_id=-1,
    )
    ranges = {"x_range": DataRange1d(), "y_range": DataRange1d()}
    orig_fig = figure()
    # Add a dummy image renderer
    orig_fig.image(
        image="image",
        x="x",
        y="y",
        dw="dw",
        dh="dh",
        source=sources["tuid1_generic_heatmap"],
    )
    orig_fig.title = Title(text="Old Title")
    fig = builder.build_figure(config, sources, tuid_data, ranges, fig=orig_fig)
    assert fig is orig_fig
    assert fig.title.text.startswith("2D Heatmap")
    assert fig.xaxis.axis_label.startswith("X")
    assert fig.yaxis.axis_label.startswith("Y")
    assert fig.renderers[0].data_source is sources["tuid1_generic_heatmap"]
