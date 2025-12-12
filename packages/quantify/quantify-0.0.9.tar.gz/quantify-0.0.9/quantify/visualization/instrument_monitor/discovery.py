# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""QCoDeS instrument discovery and reading state delegation.

This module isolates QCoDeS-specific discovery logic and delegates stateful
operations to `StateStore`.
"""

from __future__ import annotations

import contextlib
import gc
from typing import TYPE_CHECKING, Any

from qcodes.instrument import Instrument
from qcodes.station import Station

from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.snapshot_parser import parse_snapshot
from quantify.visualization.instrument_monitor.state_store import StateStore
from quantify.visualization.instrument_monitor.updates import (
    InstrumentMonitorUpdate,
    InstrumentMonitorUpdateHandler,
    InstrumentMonitorUpdateMode,
)

if TYPE_CHECKING:
    from quantify.visualization.instrument_monitor.models import ChangeEvent, Reading

logger = get_logger(__name__)


class InstrumentDiscovery:
    """QCoDeS instrument discovery and change tracking state delegation."""

    def __init__(self) -> None:
        """Initialize the QCoDeS discovery and state delegation."""
        self._known_instruments: set[str] = set()
        self._store = StateStore(max_events=1000)
        self._listeners: list[InstrumentMonitorUpdateHandler] = []

    # --- discovery -------------------------------------------------------
    def discover_instruments(self) -> list[Instrument]:
        """Discover QCoDeS instruments using public APIs.

        Preference order:
        1) Station.default components
        2) Aggregate instances from all Instrument subclasses via instances()
        3) Fallback to GC scan as last resort
        """
        discovered: dict[str, Instrument] = {}

        self._discover_from_station(discovered)
        if not discovered:
            self._discover_from_subclasses(discovered)
        if not discovered:
            self._discover_from_gc(discovered)

        instruments = list(discovered.values())
        self._log_instrument_changes(set(discovered.keys()))
        return instruments

    def _discover_from_station(self, discovered: dict[str, Instrument]) -> None:
        try:
            station = Station.default
            if station is None:
                return

            for comp in station.components.values():
                if not isinstance(comp, Instrument) or not Instrument.is_valid(comp):
                    continue

                root = getattr(comp, "root_instrument", None)
                inst = (
                    root if isinstance(root, Instrument) and root is not None else comp
                )
                discovered[inst.name] = inst
        except Exception as e:
            logger.warning("Station-based discovery failed", extra={"error": str(e)})

    def _discover_from_subclasses(self, discovered: dict[str, Instrument]) -> None:
        for subcls in Instrument.__subclasses__():
            try:
                # Broad exception handling: instances() may fail, accessing
                # attributes on closed/invalid instruments may raise AttributeError,
                # and custom instrument implementations may have unexpected behavior
                for inst in getattr(subcls, "instances", list)():
                    if not isinstance(inst, Instrument) or not Instrument.is_valid(
                        inst
                    ):
                        continue

                    root = getattr(inst, "root_instrument", None)
                    root_inst = (
                        root
                        if isinstance(root, Instrument) and root is not None
                        else inst
                    )
                    discovered[root_inst.name] = root_inst
            except Exception as e:
                logger.exception(
                    "Subclass instance discovery error",
                    extra={
                        "subclass": getattr(subcls, "__name__", str(subcls)),
                        "error": str(e),
                    },
                )
                continue

    def _discover_from_gc(self, discovered: dict[str, Instrument]) -> None:
        for obj in gc.get_objects():
            if isinstance(obj, Instrument) and hasattr(obj, "name"):
                try:
                    name = obj.name
                    if not name or name in discovered:
                        continue

                    root_instr = getattr(obj, "root_instrument", None)
                    inst = (
                        root_instr
                        if isinstance(root_instr, Instrument) and root_instr is not None
                        else obj
                    )
                    discovered[name] = inst
                except Exception:
                    logger.exception("GC discovery object error")
                    continue

    def _log_instrument_changes(self, current_names: set[str]) -> None:
        if current_names != self._known_instruments:
            new_instruments = current_names - self._known_instruments
            removed_instruments = self._known_instruments - current_names

            if new_instruments:
                logger.debug(
                    "New root instruments",
                    extra={
                        "count": len(new_instruments),
                        "names": list(new_instruments),
                    },
                )
            if removed_instruments:
                logger.debug(
                    "Removed root instruments",
                    extra={
                        "count": len(removed_instruments),
                        "names": list(removed_instruments),
                    },
                )

            self._known_instruments = current_names

    # --- snapshots and state --------------------------------------------
    def get_snapshot(self, instrument: Instrument) -> dict[str, Any]:
        """Get a snapshot of an instrument."""
        try:
            return instrument.snapshot()
        except Exception:
            logger.exception("Snapshot failed for {instrument.name}")
            return {}

    def process_snapshot(
        self, instrument: Instrument, snapshot: dict[str, Any]
    ) -> list[Reading]:
        """Process a snapshot of an instrument."""
        try:
            return parse_snapshot(instrument, snapshot)
        except Exception:
            logger.exception("Snapshot processing failed for {instrument.name}")
            return []

    def update_readings(self, new_readings: list[Reading]) -> list[ChangeEvent]:
        """Update readings in the state store."""
        change_events = self._store.update_readings(new_readings)
        if change_events and self._listeners:
            self._notify_listeners("snapshot", new_readings, change_events)
        return change_events

    def direct_update_readings(self, new_readings: list[Reading]) -> list[ChangeEvent]:
        """Directly update readings in the state store."""
        change_events = self._store.direct_update_readings(new_readings)
        if change_events and self._listeners:
            self._notify_listeners("delta", new_readings, change_events)
        return change_events

    def get_current_state(self) -> list[Reading]:
        """Get the current state of the state store."""
        return self._store.get_current_state()

    def get_recent_changes(self, limit: int = 100) -> list[ChangeEvent]:
        """Get the recent changes from the state store."""
        return self._store.get_recent_changes(limit)

    # --- external listeners ----------------------------------------------
    def register_listener(self, listener: InstrumentMonitorUpdateHandler) -> None:
        """Register a listener that receives state updates."""
        self._listeners.append(listener)

    def unregister_listener(self, listener: InstrumentMonitorUpdateHandler) -> None:
        """Remove a previously registered listener."""
        with contextlib.suppress(ValueError):
            self._listeners.remove(listener)

    def _notify_listeners(
        self,
        mode: InstrumentMonitorUpdateMode,
        readings: list[Reading],
        change_events: list[ChangeEvent],
    ) -> None:
        if not self._listeners:
            return

        update = InstrumentMonitorUpdate(
            mode=mode,
            readings=readings,
            change_events=change_events,
            current_state=self.get_current_state,
        )
        for listener in list(self._listeners):
            try:
                listener(update)
            except Exception:
                logger.exception("Instrument monitor listener failed")
