from __future__ import annotations

import contextlib
from typing import Any

import pytest
from qcodes.instrument import Instrument

from quantify.device_under_test.mock_setup import (
    set_standard_params_transmon,
    set_up_mock_transmon_setup,
)


def close_instruments(instrument_names: list[str] | dict[str, Any]):
    """Close all instruments in the list of names supplied.

    Parameters
    ----------
    instrument_names
        List of instrument names or dict, where keys correspond to instrument names.
    """
    for name in instrument_names:
        with contextlib.suppress(KeyError):
            Instrument.find_instrument(name).close()


@pytest.fixture(scope="function", autouse=True)
def close_all_instruments_at_start():
    """
    This fixture closes all instruments at the start of each test to prevent unexpected
    KeyError from qcodes.Instrument, e.g.'Another instrument has the name: q5', that may
    arise when a previous test already created an instance of an Instrument with that
    name.
    """
    Instrument.close_all()


@pytest.fixture(scope="function", autouse=False)
def mock_setup_basic_transmon():
    """
    Returns a mock setup for a basic 5-qubit transmon device.

    This mock setup is created using the :code:`set_up_mock_transmon_setup`
    function from the .device_under_test.mock_setup module.
    """

    # moved to a separate module to allow using the mock_setup in tutorials.
    mock_instruments = set_up_mock_transmon_setup()

    yield mock_instruments


@pytest.fixture(scope="function", autouse=False)
def mock_setup_basic_transmon_with_standard_params(mock_setup_basic_transmon):
    set_standard_params_transmon(mock_setup_basic_transmon)
    yield mock_setup_basic_transmon


@pytest.fixture(scope="function", autouse=False)
def device_compile_config_basic_transmon(
    mock_setup_basic_transmon_with_standard_params,
):
    """
    A config generated from a quantum device with 5 transmon qubits
    connected in a star configuration.

    The mock setup has no hardware attached to it.
    """
    # N.B. how this fixture produces the hardware config can change in the future
    # as long as it keeps doing what is described in this docstring.

    mock_setup = mock_setup_basic_transmon_with_standard_params
    yield mock_setup["quantum_device"].generate_compilation_config()
