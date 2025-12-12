"""
Module containing instruments that represent quantum devices and elements.

The elements and their components are intended to generate valid
:ref:`device configuration <sec-device-config>` files for compilation from the
:ref:`quantum-circuit layer <sec-user-guide-quantum-circuit>` to the
:ref:`quantum-device layer description<sec-user-guide-quantum-device>`.
"""

# Core device abstractions
# Operations (avoiding duplicates)
from .composite_square_edge import CZ, CompositeSquareEdge
from .device_element import DeviceElement

# Edge types and operations
from .edge import Edge

# Configuration and setup utilities
from .hardware_config import HardwareConfig
from .mock_setup import (
    set_standard_params_basic_nv,
    set_standard_params_transmon,
    set_up_mock_basic_nv_setup,
    set_up_mock_transmon_setup,
)

# Element implementations
from .nv_element import (
    BasicElectronicNVElement,
    ChargeReset,
    ClockFrequencies,
    CRCount,
    Measure,
    Ports,
    PulseCompensationModule,
    ResetSpinpump,
    RxyNV,
    SpectroscopyOperationNV,
)
from .quantum_device import QuantumDevice
from .spin_edge import CNOT, PortSpinEdge, SpinEdge, SpinInit
from .spin_element import BasicSpinElement, ChargeSensor
from .transmon_element import BasicTransmonElement

__all__ = [
    # Core abstractions
    "DeviceElement",
    "QuantumDevice",
    # Edge types
    "Edge",
    "CompositeSquareEdge",
    "SpinEdge",
    # Element types
    "BasicElectronicNVElement",
    "BasicSpinElement",
    "BasicTransmonElement",
    "ChargeSensor",
    # Operations
    "CZ",
    "CNOT",
    "SpinInit",
    "PortSpinEdge",
    "ChargeReset",
    # NV element components
    "ClockFrequencies",
    "CRCount",
    "Measure",
    "Ports",
    "PulseCompensationModule",
    "ResetSpinpump",
    "RxyNV",
    "SpectroscopyOperationNV",
    # Configuration
    "HardwareConfig",
    # Setup utilities
    "set_standard_params_basic_nv",
    "set_standard_params_transmon",
    "set_up_mock_basic_nv_setup",
    "set_up_mock_transmon_setup",
]
