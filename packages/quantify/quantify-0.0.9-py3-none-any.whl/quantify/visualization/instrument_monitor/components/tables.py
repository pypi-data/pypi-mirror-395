# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""UI table components for the instrument monitor."""

from __future__ import annotations

import hashlib
import json
import time
from typing import TYPE_CHECKING, Any, cast

from bokeh.models import (
    ColumnDataSource,
    DataTable,
    DateFormatter,
    Div,
    HTMLTemplateFormatter,
    TableColumn,
)

from quantify.visualization.instrument_monitor.components.theme import STYLES
from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.utils import safe_value_format

if TYPE_CHECKING:
    from quantify.visualization.instrument_monitor.models import Reading

logger = get_logger(__name__)


class BaseTable:
    """Base class for data tables with common functionality."""

    def __init__(
        self, columns: list[tuple[str, str, int]], selectable: bool = False
    ) -> None:
        """Initialize base table with column configuration."""
        fields: dict[str, list[object]] = {col[0]: [] for col in columns}
        self.source = ColumnDataSource(data=fields)

        table_columns = []
        for field, title, width in columns:
            if field == "ts":
                table_columns.append(
                    TableColumn(
                        field=field,
                        title=title,
                        width=width,
                        formatter=DateFormatter(format="%Y-%m-%d %H:%M:%S"),
                    )
                )
            elif field == "value":
                table_columns.append(
                    TableColumn(
                        field=field,
                        title=title,
                        width=width,
                        formatter=HTMLTemplateFormatter(
                            template=(
                                '<div style="white-space:nowrap; overflow:hidden; '
                                'text-overflow:ellipsis; max-width:100%;">'
                                "<%= value %></div>"
                            )
                        ),
                    )
                )
            else:
                table_columns.append(TableColumn(field=field, title=title, width=width))

        self.table = DataTable(
            source=self.source,
            columns=table_columns,
            sizing_mode="stretch_both",
            selectable=selectable,
            index_position=None,
            styles=STYLES["table"],
        )
        self._last_hash: str | None = None

    def update_data(self, data: dict[str, list[object]]) -> bool:
        """Table update with minimal overhead."""
        data_hash = self._compute_data_hash(data)
        if data_hash == self._last_hash:
            return False
        # ColumnDataSource.data expects DataDictLike; cast to Any for pyright
        self.source.data = cast("Any", data)
        self._last_hash = data_hash
        return True

    def _compute_data_hash(self, data: dict[str, list[object]]) -> str:
        """Hash computation with optimized serialization."""
        try:
            stable_repr = json.dumps(
                data, sort_keys=True, default=str, separators=(",", ":")
            )
            return hashlib.sha256(stable_repr.encode()).hexdigest()
        except Exception:
            return str(hash(str(data)))


class CurrentStateTable(BaseTable):
    """Table showing current state of all parameters."""

    def __init__(self) -> None:
        """Initialize the current state table and interaction state.

        The table is grouped by instrument with expandable sections that reveal
        parameter rows. A short update interval throttles rebuilds to keep the UI
        responsive when typing in the filter.
        """
        columns = [
            ("display_full_name", "Name", 240),
            ("instrument", "Instrument", 120),
            ("parameter", "Parameter", 120),
            ("value", "Value", 100),
            ("unit", "Unit", 80),
            ("ts", "Timestamp", 150),
        ]
        super().__init__(columns, selectable=True)

        self._last_update = 0.0
        self._update_interval = 0.3
        self._last_readings_hash = 0
        self._expanded: set[str] = set()
        self._value_lookup: dict[str, str] = {}

        self._filter = ""
        self.source.selected.on_change("indices", self._on_row_selected)

        self.empty_message: Div = Div(
            text=(
                "⏳ No data available right now.\n"
                "The table will update automatically when instrument data arrives."
            ),
            styles={
                **STYLES["empty_state"],
                "position": "absolute",
                "left": "50%",
                "top": "50%",
                "transform": "translate(-50%, -50%)",
                "pointer-events": "none",
                "z-index": "1",
                "width": "80%",
            },
            visible=True,
        )

    def get_full_value_for(self, full_name: str) -> str:
        """Return the formatted value for a parameter by its full name."""
        try:
            return str(self._value_lookup.get(full_name, ""))
        except Exception as e:
            logger.error(
                "get_full_value_for failed", extra={"error": str(e)}, exc_info=True
            )
            return ""

    def _on_row_selected(self, _attr: str, _old: object, new: list[int]) -> None:
        try:
            if not new:
                return
            data = cast("dict[str, list[object]]", self.source.data)
            idx = new[0]
            instrument_list = cast("list[object]", data.get("instrument", []))
            is_group_list = cast(
                "list[object]", data.get("is_group", [False] * len(instrument_list))
            )
            if idx < len(is_group_list) and bool(is_group_list[idx]):
                instrument_name = (
                    str(instrument_list[idx]) if idx < len(instrument_list) else ""
                )
                if instrument_name in self._expanded:
                    self._expanded.discard(instrument_name)
                else:
                    self._expanded.add(instrument_name)
                self.source.selected.indices = []
                self._last_readings_hash = 0
        except Exception as e:
            logger.warning(f"Group toggle error: {e}")

    def _build_tree(self, readings: list[Reading]) -> list[dict[str, object]]:
        if not readings:
            return []

        by_instrument: dict[str, list[Reading]] = {}
        for r in readings:
            by_instrument.setdefault(r.instrument or "unknown", []).append(r)

        filter_text = (self._filter or "").strip().lower()

        def matches_filter(reading: Reading) -> bool:
            if not filter_text:
                return True
            return any(
                filter_text in str(getattr(reading, field, "")).lower()
                for field in ("full_name", "instrument", "parameter", "value")
            )

        rows = []
        for instrument_name in sorted(by_instrument.keys()):
            instrument_readings = by_instrument[instrument_name]
            if filter_text:
                instrument_readings = [
                    r for r in instrument_readings if matches_filter(r)
                ]
                if not instrument_readings:
                    continue

            is_expanded = (instrument_name in self._expanded) or bool(filter_text)
            latest_ts = max((r.ts for r in instrument_readings if r.ts), default=None)
            arrow = "▼" if is_expanded else "▶"
            rows.append(
                {
                    "display_full_name": f"{arrow} {instrument_name}",
                    "full_name": instrument_name,
                    "instrument": instrument_name,
                    "parameter": "",
                    "value": f"{len(instrument_readings)} parameters",
                    "unit": "",
                    "ts": latest_ts,
                    "is_group": True,
                }
            )

            if is_expanded:
                for reading in sorted(
                    instrument_readings, key=lambda r: r.parameter or ""
                ):
                    rows.append(
                        {
                            "display_full_name": f"  {reading.parameter or 'unknown'}",
                            "full_name": reading.full_name,
                            "instrument": reading.instrument,
                            "parameter": reading.parameter,
                            "value": self._format_value(reading.value),
                            "unit": reading.unit or "",
                            "ts": reading.ts,
                            "is_group": False,
                        }
                    )
        return rows

    def _format_value(self, value: object) -> str:
        return safe_value_format(value)

    def set_filter(self, value: str) -> None:
        """Set the current filter text and force a view refresh."""
        self._filter = value or ""
        self._last_readings_hash = 0

    def _hash_readings(self, readings: list[Reading]) -> int:
        try:
            if not readings:
                return 0
            values_hash = hash(
                tuple(
                    (r.full_name, str(r.value), r.ts.isoformat() if r.ts else None)
                    for r in sorted(readings, key=lambda x: x.full_name or "")
                )
            )
            return values_hash
        except Exception:
            return len(readings)

    def update_readings(self, readings: list[Reading]) -> None:
        """Update the table rows from a list of ``Reading`` instances.

        This method is throttled by a short interval to maintain UI
        responsiveness when the user is interacting with the page.
        """
        now = time.time()
        if now - self._last_update < self._update_interval:
            return
        self._last_update = now
        try:
            self._rebuild_view_from_readings(readings)
        except Exception as e:
            logger.error(
                "Error updating readings", extra={"error": str(e)}, exc_info=True
            )

    def _rebuild_view_from_readings(self, readings: list[Reading]) -> None:
        current_hash = self._hash_readings(readings)
        if current_hash == self._last_readings_hash:
            return
        self._last_readings_hash = current_hash
        self._last_update = time.time()
        rows = self._build_tree(readings)
        data = self._rows_to_cds_data(rows)
        try:
            self._value_lookup = {
                r.full_name: self._format_value(r.value)
                for r in readings
                if getattr(r, "full_name", None)
            }
        except Exception:
            self._value_lookup = {}
        try:
            filter_text = (self._filter or "").strip()
            if not readings:
                self.empty_message.text = (
                    "⏳ No data available right now.\n"
                    "The table will update automatically when instrument data arrives."
                )
                self.empty_message.visible = True
            elif not rows and filter_text:
                self.empty_message.text = (
                    "🔎 No results match your filter.\n"
                    "Clear or adjust the filter to see parameters."
                )
                self.empty_message.visible = True
            else:
                self.empty_message.visible = False
        except Exception as e:
            logger.debug(
                "Failed to update empty-state message",
                extra={"error": str(e)},
            )
        self.update_data(data)

    def _rows_to_cds_data(
        self, rows: list[dict[str, object]]
    ) -> dict[str, list[object]]:
        """Convert row dicts to ``ColumnDataSource`` compatible dict of lists."""
        fields = (
            "display_full_name",
            "full_name",
            "instrument",
            "parameter",
            "value",
            "unit",
            "ts",
            "is_group",
        )
        return {
            field: [row.get(field, "" if field != "ts" else None) for row in rows]
            for field in fields
        }
