# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch

"""Spin qubit specific operations for use with the quantify."""

from __future__ import annotations

from .operation import Operation


class SpinInit(Operation):
    """
    Initialize a spin qubit system.

    Parameters
    ----------
    qc
        The control device element.
    qt
        The target device element
    device_overrides
        Device level parameters that override device configuration values
        when compiling from circuit to device level.

    """

    def __init__(self, qc: str, qt: str, **device_overrides) -> None:
        """Initialize a spin qubit system."""
        device_element_control, device_element_target = qc, qt
        super().__init__(
            name=f"SpinInit ({device_element_control}, {device_element_target})"
        )
        self.data.update(
            {
                "name": self.name,
                "gate_info": {
                    "unitary": None,
                    "plot_func": "quantify.schedules._visualization."
                    + "circuit_diagram.reset",
                    "tex": r"SpinInit",
                    "device_elements": [device_element_control, device_element_target],
                    "operation_type": "SpinInit",
                    "device_overrides": device_overrides,
                },
            }
        )
        self.update()

    def __str__(self) -> str:
        """String representation of the operation."""
        device_elements = map(
            lambda x: f"'{x}'", self.data["gate_info"]["device_elements"]
        )
        return f"{self.__class__.__name__}({','.join(device_elements)})"
