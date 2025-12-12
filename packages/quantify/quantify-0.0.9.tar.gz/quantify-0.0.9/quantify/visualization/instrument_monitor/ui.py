# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Bokeh UI composition for the instrument monitor.

This module wires together reusable UI components from ``components/`` into the
final dashboard layout. It re-exports key components for backward compatibility.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, cast

from bokeh.events import DocumentReady
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Spacer, TextInput

from quantify.visualization.instrument_monitor.components.resource import ResourcePanel
from quantify.visualization.instrument_monitor.components.tables import (
    CurrentStateTable,
)
from quantify.visualization.instrument_monitor.components.theme import (
    STYLES,
    create_header,
)
from quantify.visualization.instrument_monitor.components.tree import SnapshotTree
from quantify.visualization.instrument_monitor.logging_setup import get_logger

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.models.layouts import Row


logger = get_logger(__name__)


class InstrumentMonitorUI:
    """Bokeh UI with optimized data structures and minimal overhead."""

    def __init__(self) -> None:
        """Initialize the UI components."""
        self.current_state_table = CurrentStateTable()
        self.snapshot_tree = SnapshotTree()

        self.resource_panel = ResourcePanel()

        self.current_state_table.source.selected.on_change(
            "indices", self._on_current_state_selection
        )

        # UI state: track whether the filter TextInput is focused on the client.
        self.ui_state = ColumnDataSource(
            data={
                "filter_focused": [False],
                "table_scrolling": [False],
            }
        )

    def _on_current_state_selection(
        self, _attr: str, _old: object, new: list[int]
    ) -> None:
        try:
            if not new:
                return
            data = self.current_state_table.source.data
            data_dict = cast("dict[str, list[object]]", data)
            idx = new[0]

            if (
                "is_group" in data_dict
                and idx < len(data_dict.get("is_group", []))
                and bool(data_dict["is_group"][idx])
            ):
                return

            full_names = data_dict.get("full_name", [])
            if idx < len(full_names):
                full_name_obj = full_names[idx]
                full_name = str(full_name_obj)
                self.snapshot_tree.focus_on_full_name(full_name)

            with contextlib.suppress(Exception):
                self.current_state_table.source.selected.indices = []
        except Exception as e:
            logger.error(
                "Error handling current state selection",
                extra={"error": str(e)},
                exc_info=True,
            )

    def create_layout(self) -> Row:
        """Create dashboard layout with two columns."""
        TOP_ROW_HEIGHT = 560
        BOTTOM_ROW_HEIGHT = 360
        tree_header = create_header("Hierarchy Explorer", "🧭")
        current_state_header = create_header("Current State of Instruments", "📊")

        self._filter_input = TextInput(
            title="🔍 Filter (Instruments / Parameters)",
            value="",
            placeholder="Type to filter",
        )

        def _on_filter_change(_attr: str, _old: str, new: str) -> None:
            try:
                self.current_state_table.set_filter(new)
            except Exception as e:
                logger.error(
                    "Error applying filter",
                    extra={"error": str(e)},
                    exc_info=True,
                )

        self._filter_input.on_change("value", _on_filter_change)

        tree_container = column(
            self.snapshot_tree.empty_message,
            self.snapshot_tree.wrapper,
            sizing_mode="stretch_width",
            styles={"position": "relative"},
            min_height=360,
            height_policy="min",
        )

        tree_card = column(
            tree_header,
            tree_container,
            sizing_mode="stretch_width",
            styles=STYLES["card"],
            min_height=TOP_ROW_HEIGHT,
            height=TOP_ROW_HEIGHT,
            height_policy="min",
        )

        table_container = column(
            self.current_state_table.empty_message,
            self.current_state_table.table,
            sizing_mode="stretch_width",
            styles={"position": "relative"},
            min_height=360,
            height_policy="min",
        )

        current_state_card = column(
            current_state_header,
            self._filter_input,
            table_container,
            sizing_mode="stretch_width",
            styles=STYLES["card"],
            min_height=TOP_ROW_HEIGHT,
            height=TOP_ROW_HEIGHT,
            height_policy="min",
        )

        # Right column contains the hierarchy explorer and resource monitor
        resource_card = column(
            *self.resource_panel.layout_children,
            sizing_mode="stretch_width",
            styles=STYLES["card"],
            min_height=BOTTOM_ROW_HEIGHT,
            height=BOTTOM_ROW_HEIGHT,
            height_policy="min",
        )

        left_column = column(
            current_state_card,
            Spacer(height=BOTTOM_ROW_HEIGHT),
            sizing_mode="stretch_width",
            min_height=TOP_ROW_HEIGHT + BOTTOM_ROW_HEIGHT,
            height_policy="min",
        )

        right_column = column(
            tree_card,
            resource_card,
            sizing_mode="stretch_width",
            min_height=TOP_ROW_HEIGHT + BOTTOM_ROW_HEIGHT,
            height_policy="min",
        )

        self._root_row = row(
            left_column,
            right_column,
            sizing_mode="stretch_width",
            min_height=400,
            height_policy="min",
        )

        return self._root_row

    def attach_client_listeners(self, doc: Document) -> None:
        """Attach client-side focus and scroll listeners via CustomJS."""
        try:
            ready_js = CustomJS(
                args=dict(
                    inp=self._filter_input,
                    state=self.ui_state,
                    table=self.current_state_table.table,
                    table_source=self.current_state_table.source,
                ),
                code="""
                // Track focus on filter input
                const view = Bokeh.index[inp.id];
                if (view && view.input_el) {
                  const setFocused = (v) => {
                    const d = Object.assign({}, state.data);
                    d.filter_focused = [v];
                    state.data = d;
                  }
                  const currentlyFocused =
                    (document.activeElement === view.input_el);
                  setFocused(currentlyFocused);
                  view.input_el.addEventListener('focus', () => setFocused(true));
                  view.input_el.addEventListener('blur', () => setFocused(false));
                }

                // Track scrolling on the DataTable and
                // clear selection to avoid auto-jumps
                const tview = Bokeh.index[table.id];
                if (tview && tview.el) {
                  const viewport =
                    tview.el.querySelector('.slick-viewport') || tview.el;
                  const setScrolling = (v) => {
                    const d = Object.assign({}, state.data);
                    d.table_scrolling = [v];
                    state.data = d;
                  }
                  let scrollTimer = null;
                  const onScroll = () => {
                    setScrolling(true);
                    try { table_source.selected.indices = []; } catch (e) {}
                    if (scrollTimer) clearTimeout(scrollTimer);
                    scrollTimer = setTimeout(() => setScrolling(false), 400);
                  }
                  viewport.addEventListener('wheel', onScroll, { passive: true });
                  viewport.addEventListener('scroll', onScroll, { passive: true });
                  viewport.addEventListener('touchmove', onScroll, { passive: true });
                }

                """,
            )
            doc.js_on_event(DocumentReady, ready_js)
        except Exception as e:
            logger.warning(
                f"Failed to attach focus/scroll listeners: {e}", exc_info=True
            )
