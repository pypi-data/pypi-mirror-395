# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Thread-safe state store for readings and change events.

This module encapsulates the stateful aspects of ingestion, including
- current readings map
- recent change events buffer
- change detection logic

It is intentionally independent of QCoDeS so it can be reused or tested in
isolation, and makes `InstrumentDiscovery` stateless w.r.t. readings.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import threading

from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.models import ChangeEvent, Reading
from quantify.visualization.instrument_monitor.utils import values_equal

logger = get_logger(__name__)


class StateStore:
    """Thread-safe store of readings and change events."""

    def __init__(self, *, max_events: int = 1000) -> None:
        """Initialize the state store."""
        self._last_readings: dict[str, Reading] = {}
        self._change_buffer: deque[ChangeEvent] = deque(maxlen=max_events)
        self._lock = threading.RLock()

    # --- core operations -------------------------------------------------
    def update_readings(self, new_readings: list[Reading]) -> list[ChangeEvent]:
        """Update readings with change detection.

        Returns change events; also appends them to the internal buffer.
        """
        change_events: list[ChangeEvent] = []
        current_time = datetime.now(timezone.utc)

        with self._lock:
            for reading in new_readings:
                old_reading = self._last_readings.get(reading.full_name)

                if old_reading is None or not values_equal(
                    old_reading.value, reading.value
                ):
                    changed_fields = {"value"} if old_reading else {"value", "unit"}
                    change_event = ChangeEvent(
                        reading=reading, changed_fields=changed_fields, ts=current_time
                    )
                    change_events.append(change_event)
                    self._change_buffer.append(change_event)

                self._last_readings[reading.full_name] = reading

        return change_events

    def direct_update_readings(self, new_readings: list[Reading]) -> list[ChangeEvent]:
        """Direct update without change comparison.

        Intended for post-warmup callback mode, where changes are detected at
        the source (e.g., QCoDeS Parameter callbacks).
        """
        current_time = datetime.now(timezone.utc)

        change_events: list[ChangeEvent] = []

        with self._lock:
            for reading in new_readings:
                change_event = ChangeEvent(
                    reading=reading, changed_fields={"value"}, ts=current_time
                )
                self._change_buffer.append(change_event)
                self._last_readings[reading.full_name] = reading
                change_events.append(change_event)

        return change_events

    # --- queries ---------------------------------------------------------
    def get_current_state(self) -> list[Reading]:
        """Get the current state of readings."""
        with self._lock:
            return list(self._last_readings.values())

    def get_recent_changes(self, limit: int = 100) -> list[ChangeEvent]:
        """Get the recent change events."""
        with self._lock:
            return list(reversed(list(self._change_buffer)))[:limit]
