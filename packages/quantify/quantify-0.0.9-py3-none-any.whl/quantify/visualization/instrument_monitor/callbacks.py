# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Callback integrations for ingestion (e.g., QCoDeS global on-set).

This is kept separate from the ingestion logic so alternate strategies can be
swapped in the future without touching the rest of the pipeline.
"""

from __future__ import annotations

from datetime import datetime, timezone
import threading
from typing import TYPE_CHECKING

from qcodes.parameters import ParameterBase

from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.models import Reading

if TYPE_CHECKING:
    from collections.abc import Callable

logger = get_logger(__name__)


class GlobalParameterCallbackManager:
    """Install a single global on-set callback on QCoDeS ParameterBase."""

    def __init__(self, on_change: Callable[[Reading], None]) -> None:
        """Initialize the global parameter callback manager."""
        self._on_change = on_change
        self._lock = threading.RLock()
        # Keep a reference to our callback so we can verify/remove safely
        self._callback = self._make_global_callback()
        self._installed = False

    def _make_global_callback(self) -> Callable[[ParameterBase, object], None]:
        def cb(param: ParameterBase, value: object) -> None:
            try:
                root_instr = getattr(param, "root_instrument", None)
                if root_instr is None:
                    return

                instrument_name = getattr(root_instr, "name", "")
                if not instrument_name:
                    return

                parts = list(getattr(param, "name_parts", []) or [])
                if parts and parts[0] == instrument_name:
                    parameter_path = ".".join(parts[1:]) if len(parts) > 1 else ""
                else:
                    parameter_path = getattr(param, "name", "")

                if not parameter_path:
                    return

                unit = getattr(param, "unit", None)

                reading = Reading(
                    full_name=f"{instrument_name}.{parameter_path}",
                    instrument=instrument_name,
                    parameter=parameter_path,
                    value=value,
                    unit=unit if isinstance(unit, str) else None,
                    ts=datetime.now(timezone.utc),
                )
                self._on_change(reading)
            except Exception as e:
                logger.warning("Global callback error: %s", str(e))

        return cb

    def start(self) -> None:
        """Start the global parameter callback manager."""
        with self._lock:
            if self._installed:
                return
            # Install our callback as the global callback
            ParameterBase.global_on_set_callback = self._callback
            self._installed = True

    def stop(self) -> None:
        """Stop the global parameter callback manager."""
        with self._lock:
            if not self._installed:
                return
            # Only clear if our callback is still installed
            if getattr(ParameterBase, "global_on_set_callback", None) is self._callback:
                ParameterBase.global_on_set_callback = None
            self._installed = False
