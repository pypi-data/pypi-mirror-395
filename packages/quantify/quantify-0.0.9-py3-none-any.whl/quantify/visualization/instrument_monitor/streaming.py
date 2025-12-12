# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Helpers for streaming instrument monitor updates to external consumers."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from quantify.visualization.instrument_monitor.config import (
    DEFAULT_INGESTION_CONFIG,
    IngestionConfig,
)
from quantify.visualization.instrument_monitor.discovery import InstrumentDiscovery
from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.poller import SnapshotPoller

if TYPE_CHECKING:
    from quantify.visualization.instrument_monitor.updates import (
        InstrumentMonitorUpdate,
        InstrumentMonitorUpdateHandler,
    )

logger = get_logger(__name__)

__all__ = ["InstrumentMonitorStreamHandle", "start_instrument_monitor_stream"]


class InstrumentMonitorStreamHandle(BaseModel):
    """Handle to manage a running instrument monitor stream."""

    discovery: InstrumentDiscovery
    poller: SnapshotPoller
    stopper: threading.Event
    dispatcher: _StreamDispatcher

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def stop(self) -> None:
        """Stop streaming updates."""
        if self.stopper.is_set():
            return
        self.stopper.set()
        try:
            self.poller.stop()
        finally:
            self.discovery.unregister_listener(self.dispatcher)
            logger.debug("Instrument monitor stream stopped")

    def running(self) -> bool:
        """Return whether streaming is still active."""
        return not self.stopper.is_set()

    def __enter__(self) -> InstrumentMonitorStreamHandle:
        """Start streaming updates."""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Stop streaming updates."""
        self.stop()


class _StreamDispatcher:
    """Internal helper to dispatch updates safely."""

    def __init__(self, handler: InstrumentMonitorUpdateHandler) -> None:
        self._handler = handler

    def __call__(self, update: InstrumentMonitorUpdate) -> None:
        try:
            self._handler(update)
        except Exception as exc:
            logger.warning(
                "Instrument monitor stream handler failed",
                extra={"error": str(exc)},
                exc_info=True,
            )


def start_instrument_monitor_stream(
    handler: InstrumentMonitorUpdateHandler,
    *,
    config: IngestionConfig | None = None,
    poll_interval: float = 0.5,
    discovery: InstrumentDiscovery | None = None,
) -> InstrumentMonitorStreamHandle:
    """Start publishing instrument monitor updates to a handler.

    Parameters
    ----------
    handler
        Callable invoked for each batch of readings produced by the ingestion
        pipeline.
    config
        Optional ingestion configuration. Defaults to the standard ingest config.
    poll_interval
        Poll interval forwarded to :class:`SnapshotPoller`.
    discovery
        Discovery instance to reuse. When omitted, a fresh instance is created.

    Returns
    -------
    InstrumentMonitorStreamHandle
        Handle that can be used to stop the stream.

    """
    discovery = discovery or InstrumentDiscovery()
    ingestion_config = config or DEFAULT_INGESTION_CONFIG
    poller = SnapshotPoller(
        discovery, poll_interval=poll_interval, config=ingestion_config
    )
    stopper = threading.Event()

    dispatcher = _StreamDispatcher(handler)
    discovery.register_listener(dispatcher)

    poller.start()
    logger.debug("Instrument monitor stream started")

    return InstrumentMonitorStreamHandle(
        discovery=discovery,
        poller=poller,
        stopper=stopper,
        dispatcher=dispatcher,
    )
