"""
Unit tests for selector_builder.py
"""

from bokeh.models import Column, Dropdown
import pytest

from quantify.visualization.plotmon.services.figure_builder import selector_builder
from quantify.visualization.plotmon.utils.tuid_data import TuidData


@pytest.fixture
def tuid_data():
    return TuidData(tuids=set(), active_tuid="", selected_tuid={-1: ""})


def test_get_prev_selector_from_layout_none():
    assert selector_builder.get_prev_selector_from_layout(None) is None


def test_get_prev_selector_from_layout_no_selector():
    layout = Column(children=[])
    assert selector_builder.get_prev_selector_from_layout(layout) is None


def test_build_selector_creates_new_selector(tuid_data):
    titles = {0: "exp1", 1: "exp2"}
    selector = selector_builder.build_selector(tuid_data, titles=titles)
    assert isinstance(selector, Dropdown)
    assert selector.menu == [("exp1", "0"), ("exp2", "1")]
    assert selector.disabled is False
