# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
Module for building table figures in Plotmon.
Provides functionality to create and update tables listing TUIDs,
with selection capabilities to highlight related graphs.
"""

from collections.abc import Callable
import logging

from bokeh.models import ColumnDataSource, DataTable, FlexBox, TableColumn

from quantify.visualization.plotmon.utils.tuid_data import TuidData


def get_prev_table_from_layout(current_layout: FlexBox | None) -> DataTable | None:
    """Extract the previous DataTable from the current layout if it exists."""
    if not (current_layout and current_layout.document):
        return None
    table = current_layout.document.get_model_by_name("experiment_table")
    if not isinstance(table, DataTable):
        return None

    return table


def create_table(
    sources: dict[str, ColumnDataSource],
    on_select: Callable,
    tuid_data: TuidData,
    meta_data: dict[str, dict],
    figure: DataTable | None = None,
) -> DataTable:
    """
    Create a table figure based on the provided sources.
    The table lists all TUIDs from the sources.
    It comes with a checkbox,
    which on click highlights all graphs with the selected TUID.

    Parameters
    ----------
    sources : dict[str, ColumnDataSource]
        Dictionary of data sources to be used in the table.
    on_select : Callable
        Callback function to be called when a TUID is selected.
    tuid_data : TuidData
        TUID related data for the application.
    meta_data : dict[str, dict]
        Metadata for the experiments.
    figure : DataTable | None
        Existing DataTable to update, or None to create a new one.


    Returns
    -------
    DataTable
        A Bokeh DataTable object representing the table figure.

    """
    table_source = sources.get("table_source")
    if table_source is None:
        table_source = ColumnDataSource(
            data={"tuid": [], "start_date": [], "end_date": []}
        )
        sources["table_source"] = table_source

    start_dates = []
    end_dates = []
    tuids = []
    for tuid in tuid_data.tuids:
        for key, meta in meta_data.items():
            if tuid in key:
                tuids.append(tuid)
                start_dates.append(meta.get("start_date", ""))
                end_dates.append(meta.get("end_date", ""))
                break

    # Sort by start_date (descending: latest first)
    combined = sorted(
        zip(tuids, start_dates, end_dates),
        key=lambda x: x[1] if x[1] else "",
        reverse=False,
    )
    tuids, start_dates, end_dates = (
        map(list, zip(*combined)) if combined else ([], [], [])
    )

    data = {
        "tuid": list(tuids),
        "start_date": start_dates,
        "end_date": end_dates,
    }

    if isinstance(table_source.data, dict) and table_source.data != data:
        table_source.update(data=data)

    def on_table_select(_: str, old: list[int], new: list[int]) -> None:
        logging.info("Table selection changed from %s to %s", old, new)
        if tuid_data.active_tuid != "":
            return
        selected_indices = new

        if new == []:
            # If nothing is selected, revert to active TUID
            selected_indices = [
                i
                for i, tuid in enumerate(table_source.data["tuid"])
                if tuid_data.active_tuid == tuid
            ]
            if selected_indices == []:
                selected_indices = [
                    i
                    for i, tuid in enumerate(table_source.data["tuid"])
                    if tuid_data.selected_tuid[-1] == tuid
                ]
            table_source.selected.indices = selected_indices
            return
        if len(new) > 1:
            # Select the new one this will trigger on_table_select again
            table_source.selected.indices = [i for i in new if i not in old]
            return

        selected_tuids = set([table_source.data["tuid"][i] for i in selected_indices])

        on_select(selected_tuids)

    if figure is None:
        selected_tuid = tuid_data.active_tuid or tuid_data.selected_tuid.get(-1, "")
        table_source.selected.indices = [
            i
            for i, tuid in enumerate(table_source.data["tuid"])
            if tuid == selected_tuid
        ]
        table_source.selected.on_change("indices", on_table_select)

        return DataTable(
            name="experiment_table",
            source=table_source,
            height=120,  # Slightly larger for 2-3 rows
            row_height=30,
            columns=[
                TableColumn(field="tuid", title="Experiment ID", width=180),
                TableColumn(field="start_date", title="Start Date", width=120),
                TableColumn(field="end_date", title="End Date", width=120),
            ],
            selectable="checkbox",
            sortable=True,
            sizing_mode="stretch_width",
            css_classes=["experiment-table"],  # Optional: for custom CSS
        )

    if tuid_data.active_tuid != "":
        selected_tuid = tuid_data.active_tuid
        table_source.selected.indices = [
            i
            for i, tuid in enumerate(table_source.data["tuid"])
            if tuid == selected_tuid
        ]
    return figure
