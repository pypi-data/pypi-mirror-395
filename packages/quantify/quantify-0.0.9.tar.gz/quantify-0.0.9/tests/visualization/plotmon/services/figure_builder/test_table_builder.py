from bokeh.models import ColumnDataSource, DataTable

from quantify.visualization.plotmon.services.figure_builder import table_builder


class DummyTuidData:
    def __init__(self, tuids, selected_tuid=None, active_tuid=None):
        self.tuids = tuids
        self.selected_tuid = selected_tuid or {}
        self.active_tuid = active_tuid or ""


def dummy_on_select(selected_tuids):
    dummy_on_select.called = True
    dummy_on_select.selected = selected_tuids


def test_create_table_creates_new_table():
    sources = {}
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: "tuid1"},
        active_tuid="",
    )
    meta_data = {
        "tuid1": {"start_date": "2023-01-01", "end_date": "2023-01-02"},
        "tuid2": {"start_date": "2023-02-01", "end_date": "2023-02-02"},
    }
    table = table_builder.create_table(sources, dummy_on_select, tuid_data, meta_data)
    assert isinstance(table, DataTable)
    assert "table_source" in sources
    source = sources["table_source"]
    assert source.data["tuid"] == ["tuid1", "tuid2"]
    assert source.data["start_date"] == ["2023-01-01", "2023-02-01"]
    assert source.data["end_date"] == ["2023-01-02", "2023-02-02"]


def test_create_table_updates_existing_table():
    sources = {
        "table_source": ColumnDataSource(
            data={
                "tuid": ["tuid1"],
                "start_date": ["2023-01-01"],
                "end_date": ["2023-01-02"],
            }
        )
    }
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: "tuid2"},
        active_tuid="",
    )
    meta_data = {
        "tuid1": {"start_date": "2023-01-01", "end_date": "2023-01-02"},
        "tuid2": {"start_date": "2023-02-01", "end_date": "2023-02-02"},
    }
    table = table_builder.create_table(sources, dummy_on_select, tuid_data, meta_data)
    assert isinstance(table, DataTable)
    source = sources["table_source"]
    assert "tuid2" in source.data["tuid"]


def test_create_table_selects_active_tuid():
    sources = {}
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: "tuid1"},
        active_tuid="tuid2",
    )
    meta_data = {
        "tuid1": {"start_date": "2023-01-01", "end_date": "2023-01-02"},
        "tuid2": {"start_date": "2023-02-01", "end_date": "2023-02-02"},
    }
    table_builder.create_table(sources, dummy_on_select, tuid_data, meta_data)
    source = sources["table_source"]
    assert source.selected.indices == [1]  # index of "tuid2"


def test_create_table_with_existing_figure():
    sources = {
        "table_source": ColumnDataSource(
            data={
                "tuid": ["tuid1", "tuid2"],
                "start_date": ["2023-01-01", "2023-02-01"],
                "end_date": ["2023-01-02", "2023-02-02"],
            }
        )
    }
    tuid_data = DummyTuidData(
        tuids=["tuid1", "tuid2"],
        selected_tuid={-1: "tuid1"},
        active_tuid="tuid2",
    )
    meta_data = {
        "tuid1": {"start_date": "2023-01-01", "end_date": "2023-01-02"},
        "tuid2": {"start_date": "2023-02-01", "end_date": "2023-02-02"},
    }
    # Pass an existing DataTable as figure
    existing_table = DataTable(source=sources["table_source"])
    result = table_builder.create_table(
        sources, dummy_on_select, tuid_data, meta_data, figure=existing_table
    )
    assert result is existing_table
    assert sources["table_source"].selected.indices == [1]  # active_tuid index


def test_create_table_empty_meta_data():
    sources = {}
    tuid_data = DummyTuidData(
        tuids=["tuid1"],
        selected_tuid={-1: "tuid1"},
        active_tuid="",
    )
    meta_data = {}
    table_builder.create_table(sources, dummy_on_select, tuid_data, meta_data)
    source = sources["table_source"]
    assert source.data["tuid"] == []
    assert source.data["start_date"] == []
    assert source.data["end_date"] == []
