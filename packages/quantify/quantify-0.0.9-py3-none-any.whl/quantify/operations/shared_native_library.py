# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Module containing shared native operations."""

from .operation import Operation


class SpectroscopyOperation(Operation):
    """
    Spectroscopy operation to find energy between computational basis states.

    Spectroscopy operations can be supported by various qubit types, but not all of
    them. They are typically translated into a spectroscopy pulse by the quantum
    device. The frequency is taken from a clock of the device element.

    Parameters
    ----------
    qubit : str
        The target device element.
    device_overrides
        Device level parameters that override device configuration values
        when compiling from circuit to device level.

    """

    def __init__(
        self,
        qubit: str,
        **device_overrides,
    ) -> None:
        """Initialize a spectroscopy operation."""
        device_element = qubit
        super().__init__(name=f"Spectroscopy operation {device_element}")
        self.data.update(
            {
                "gate_info": {
                    "unitary": None,
                    "plot_func": "quantify.schedules._visualization"
                    ".circuit_diagram.pulse_modulated",
                    "tex": r"Spectroscopy operation",
                    "device_elements": [device_element],
                    "operation_type": "spectroscopy_operation",
                    "device_overrides": device_overrides,
                },
            }
        )
        self._update()

    def __str__(self) -> str:
        """String representation of the operation."""
        gate_info = self.data["gate_info"]
        device_element = gate_info["device_elements"][0]
        return f'{self.__class__.__name__}(qubit="{device_element}")'
