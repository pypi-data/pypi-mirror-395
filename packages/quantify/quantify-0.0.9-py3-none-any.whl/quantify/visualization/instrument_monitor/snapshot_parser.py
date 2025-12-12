# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Snapshot parsing helpers to transform QCoDeS snapshots into readings.

This module is pure logic (no state, no I/O) to keep ingestion modular.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.models import Reading

if TYPE_CHECKING:
    from qcodes.instrument import Instrument

logger = get_logger(__name__)


def parse_snapshot(instrument: Instrument, snapshot: dict[str, Any]) -> list[Reading]:
    """Parse a QCoDeS instrument snapshot into a list of Reading objects."""
    readings: list[Reading] = []
    try:
        # Use root instrument name for proper hierarchy
        root_instr = getattr(instrument, "root_instrument", None)
        root_name = (
            getattr(root_instr, "name", instrument.name)
            if root_instr
            else instrument.name
        )
        _process_parameters(readings, root_name, "", snapshot)
    except Exception:
        logger.warning("Snapshot parsing failed", exc_info=True)
    return readings


def _process_parameters(
    readings: list[Reading],
    instrument_name: str,
    prefix: str,
    snapshot_section: dict[str, Any],
) -> None:
    # Process direct parameters
    parameters = snapshot_section.get("parameters", {})
    for param_name, param_data in parameters.items():
        if not isinstance(param_data, dict):
            continue

        value = param_data.get("value")
        unit = param_data.get("unit")
        ts_str = param_data.get("ts")

        # Parse timestamp
        ts = None
        if ts_str:
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
            except Exception:
                ts = None

        # Build parameter names
        parameter_path = f"{prefix}.{param_name}" if prefix else param_name
        full_name = f"{instrument_name}.{parameter_path}"

        readings.append(
            Reading(
                full_name=full_name,
                instrument=instrument_name,
                parameter=parameter_path,
                value=value,
                unit=unit,
                ts=ts,
            )
        )

    # Recursively process submodules
    for submodule_name, submodule_data in snapshot_section.get(
        "submodules", {}
    ).items():
        if isinstance(submodule_data, dict):
            new_prefix = f"{prefix}.{submodule_name}" if prefix else submodule_name
            _process_parameters(readings, instrument_name, new_prefix, submodule_data)
