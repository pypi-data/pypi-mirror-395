# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Background snapshot poller and callback-driven ingestion.

This module separates the polling orchestration from discovery/state logic.
"""

from __future__ import annotations

from collections import deque
from concurrent.futures import ThreadPoolExecutor
import contextlib
import threading
import time
from typing import TYPE_CHECKING

from quantify.visualization.instrument_monitor.callbacks import (
    GlobalParameterCallbackManager,
)
from quantify.visualization.instrument_monitor.config import IngestionConfig
from quantify.visualization.instrument_monitor.logging_setup import get_logger

if TYPE_CHECKING:
    from collections.abc import Sequence

    from quantify.visualization.instrument_monitor.discovery import InstrumentDiscovery
    from quantify.visualization.instrument_monitor.models import Reading

logger = get_logger(__name__)


class SnapshotPoller:
    """Snapshot polling with callback-based ingestion after warmup."""

    def __init__(
        self,
        discovery: InstrumentDiscovery,
        poll_interval: float = 1.0,
        config: IngestionConfig | None = None,
    ) -> None:
        """Initialize the snapshot poller."""
        self.discovery = discovery
        self.poll_interval = poll_interval
        self._executor = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="snapshot"
        )
        self._running = False
        self._poll_thread: threading.Thread | None = None

        self._config = config or IngestionConfig(
            event_batch_limit=100,
            warmup_total_passes=5,
            warmup_interval_s=1.0,
        )
        # Align queue capacity with batch size to minimize drops
        self._event_queue: deque[Reading] = deque(
            maxlen=max(1, int(self._config.event_batch_limit))
        )
        self._subscriber_mgr = GlobalParameterCallbackManager(self._event_queue.append)
        self._warmup_total_passes = self._config.warmup_total_passes
        self._warmup_interval_s = self._config.warmup_interval_s
        self._warmup_done_passes = 0
        self._last_warmup_ts = 0.0
        self._warmup_complete = False

    def start(self) -> None:
        """Start the polling loop."""
        if self._running:
            return

        self._running = True
        self._subscriber_mgr.start()
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()
        logger.debug(
            "Started snapshot polling", extra={"poll_interval": self.poll_interval}
        )

    def stop(self) -> None:
        """Stop the polling loop."""
        self._running = False
        if self._poll_thread:
            self._poll_thread.join(timeout=5.0)
        self._executor.shutdown(wait=True)
        try:
            self._subscriber_mgr.stop()
        except Exception as e:
            logger.debug(
                "Failed to stop global parameter callback manager",
                extra={"error": str(e)},
                exc_info=True,
            )
        logger.debug("Stopped snapshot polling")

    def _poll_loop(self) -> None:
        """Main polling loop."""
        while self._running:
            try:
                self._tick_once()
            except Exception as e:
                logger.exception("Error in polling loop: %s", str(e))

            # Sleep in small increments to allow quick shutdown
            sleep_time = 0.0
            while sleep_time < self.poll_interval and self._running:
                time.sleep(0.1)
                sleep_time += 0.1

    def _tick_once(self) -> None:
        """Polling tick: warmup then callback-based ingestion."""
        now = time.time()

        # Always drain callback events to minimize memory usage
        drained: list[Reading] = []
        while self._event_queue and len(drained) < self._config.event_batch_limit:
            drained.append(self._event_queue.popleft())

        if drained:
            # After warmup, no more change comparison - just direct updates
            if self._warmup_complete:
                self.discovery.direct_update_readings(drained)
            else:
                self.discovery.update_readings(drained)

        # Only run snapshots during warmup
        if (
            not self._warmup_complete
            and self._warmup_done_passes < self._warmup_total_passes
        ) and (now - self._last_warmup_ts) >= self._warmup_interval_s:
            instruments = self.discovery.discover_instruments()
            self._run_snapshot_pass(instruments)
            self._warmup_done_passes += 1
            self._last_warmup_ts = now

            if self._warmup_done_passes >= self._warmup_total_passes:
                self._warmup_complete = True
                logger.debug("Warmup complete - switching to callback-only mode")

    def _get_readings_for_instrument(self, instrument: object) -> list[Reading]:
        """Get readings for single instrument."""
        try:
            snapshot = self.discovery.get_snapshot(instrument)  # type: ignore[arg-type]
            return self.discovery.process_snapshot(instrument, snapshot)  # type: ignore[arg-type]
        except Exception as e:
            logger.debug(
                "Snapshot collection failed",
                extra={
                    "instrument": getattr(instrument, "name", "<unknown>"),
                    "error": str(e),
                },
                exc_info=True,
            )
            return []

    def _run_snapshot_pass(self, instruments: Sequence[object]) -> None:
        """Parallel snapshot processing."""
        if not instruments:
            return

        futures = []
        for instrument in instruments:
            try:
                futures.append(
                    self._executor.submit(self._get_readings_for_instrument, instrument)
                )
            except RuntimeError:
                return

        all_readings: list[Reading] = []
        for fut in futures:
            with contextlib.suppress(Exception):
                readings = fut.result(timeout=3.0)
                if readings:
                    all_readings.extend(readings)

        if all_readings:
            self.discovery.update_readings(all_readings)
