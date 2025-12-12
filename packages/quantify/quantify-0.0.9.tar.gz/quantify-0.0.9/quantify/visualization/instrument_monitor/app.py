# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Bokeh application for instrument monitoring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

from quantify.visualization.instrument_monitor.discovery import InstrumentDiscovery
from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.poller import SnapshotPoller
from quantify.visualization.instrument_monitor.ui import InstrumentMonitorUI

if TYPE_CHECKING:
    from bokeh.document import Document

    from quantify.visualization.instrument_monitor.config import IngestionConfig
    from quantify.visualization.instrument_monitor.models import ChangeEvent, Reading

logger = get_logger(__name__)


class InstrumentMonitorApp:
    """Instrument monitor with dependency-injected discovery and poller.

    This allows swapping out real components with fakes in tests, while keeping
    the UI logic independent from ingestion details.
    """

    def __init__(
        self,
        config: IngestionConfig | None = None,
        *,
        discovery: InstrumentDiscovery | None = None,
        poller: SnapshotPoller | None = None,
        start_poller: bool = True,
    ) -> None:
        """Initialize instrument monitor application.

        Parameters
        ----------
        config
            Optional ingestion configuration used when constructing the default
            poller. Ignored if a custom ``poller`` is provided.
        discovery
            Optional discovery port implementation. Defaults to the built-in
            QCoDeS-backed discovery.
        poller
            Optional snapshot poller port implementation. Defaults to the
            built-in snapshot poller when not provided.
        start_poller
            When ``True`` (default) start the provided or default poller.
            Set to ``False`` to disable polling entirely, allowing data to be fed
            into the discovery externally via ``app.discovery.update_readings()``
            or ``app.discovery.direct_update_readings()``.

        """
        # Use None default to avoid mutable default argument pitfall
        self.discovery: InstrumentDiscovery = discovery or InstrumentDiscovery()
        self.poller: SnapshotPoller | None
        if poller is not None:
            self.poller = poller
        elif start_poller:
            self.poller = SnapshotPoller(
                self.discovery, poll_interval=0.5, config=config
            )
        else:
            self.poller = None
        self._poller_started = False
        self._should_start_poller = start_poller and self.poller is not None
        self.ui: InstrumentMonitorUI | None = None
        self.doc: Document | None = None

    def create_document(self, doc: Document) -> None:
        """Create and configure the Bokeh document."""
        logger.debug("Creating instrument monitor document")

        self.doc = doc
        doc.title = "Quantify Instrument Monitor"

        # Create a fresh UI per session to prevent reusing models across documents
        self.ui = InstrumentMonitorUI()

        # Create layout
        layout = self.ui.create_layout()
        doc.add_root(layout)

        # Attach client-side listeners and tree toggle bridges via UI/components
        try:
            self.ui.attach_client_listeners(doc)
        except Exception:
            logger.warning("Failed to attach client listeners", exc_info=True)
        try:
            self.ui.snapshot_tree.bind_js(doc)
            self.ui.snapshot_tree.bind_python_toggle_handler()
        except Exception:
            logger.warning("Failed to bind tree events", exc_info=True)

        # Start resource panel auto updates
        try:
            self.ui.resource_panel.start_auto_update(doc, period_ms=2000)
        except Exception:
            logger.warning("Failed to start resource auto updates", exc_info=True)

        # Start background polling only once per server lifetime
        self._ensure_poller_started()

        # 333ms update interval for smooth performance
        doc.add_periodic_callback(self._periodic_update, period_milliseconds=333)

        # Session cleanup
        doc.on_session_destroyed(
            lambda _: logger.debug("Session for instrument monitor ended")
        )

        logger.debug("Instrument monitor document created successfully")

    def _ensure_poller_started(self) -> None:
        """Start background polling only once per server lifetime."""
        if self.poller is None or not self._should_start_poller:
            return

        if not self._poller_started:
            self.poller.start()
            self._poller_started = True

    def _periodic_update(self) -> None:
        """Gather data and schedule UI updates on the next tick."""
        try:
            current_readings = self.discovery.get_current_state()
            recent_changes = self.discovery.get_recent_changes(limit=50)
            self._schedule_apply_updates(current_readings, recent_changes)
        except Exception as e:
            logger.error("UI update failed", extra={"error": str(e)}, exc_info=True)

    def _schedule_apply_updates(
        self, current_readings: list[Reading], recent_changes: list[ChangeEvent]
    ) -> None:
        """Schedule UI updates on the document's next tick."""
        if not self.doc:
            return

        def apply_updates() -> None:
            self._apply_updates(current_readings, recent_changes)

        self.doc.add_next_tick_callback(apply_updates)

    def _apply_updates(
        self, current_readings: list[Reading], _recent_changes: list[ChangeEvent]
    ) -> None:
        """Apply gated UI updates and resource monitoring."""
        ui = self.ui
        if ui is None:
            return
        focused = False
        scrolling = False
        try:
            data = ui.ui_state.data
            if isinstance(data, dict):
                focused_list = data.get("filter_focused")
                if isinstance(focused_list, list) and focused_list:
                    focused = bool(focused_list[0])
                scrolling_list = data.get("table_scrolling")
                if isinstance(scrolling_list, list) and scrolling_list:
                    scrolling = bool(scrolling_list[0])
        except Exception:
            focused = False
            scrolling = False

        if not (focused or scrolling):
            try:
                ui.current_state_table.update_readings(current_readings)
            except Exception as e:
                logger.warning(
                    "Current state update failed",
                    extra={"error": str(e)},
                    exc_info=True,
                )

            try:
                ui.snapshot_tree.update_readings(current_readings)
            except Exception as e:
                logger.warning(
                    "Snapshot tree update failed",
                    extra={"error": str(e)},
                    exc_info=True,
                )


def create_bokeh_app(
    config: IngestionConfig | None = None,
    *,
    discovery: InstrumentDiscovery | None = None,
    poller: SnapshotPoller | None = None,
) -> Application:
    """Create the Bokeh application with optional dependency injection."""
    monitor_app = InstrumentMonitorApp(
        config=config, discovery=discovery, poller=poller
    )
    handler = FunctionHandler(monitor_app.create_document)
    return Application(handler)


def create_instrument_monitor_app(config: IngestionConfig | None = None) -> Application:
    """Create the instrument monitor application (alias for compatibility)."""
    return create_bokeh_app(config)
