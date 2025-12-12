# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch


from __future__ import annotations

from dataclasses import dataclass
import gc
from unittest.mock import call

import pytest
from qcodes import Instrument
from xarray import DataArray, Dataset

from quantify.instrument_coordinator import (
    InstrumentCoordinator,
)
from quantify.instrument_coordinator.components import base as base_component
from quantify.schedules.schedule import CompiledSchedule, Schedule
from tests.fixtures.mock_setup import *  # noqa: F403


class MyICC(base_component.InstrumentCoordinatorComponentBase):
    @property
    def is_running(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def prepare(self, options):
        pass

    def retrieve_acquisition(self):
        pass

    def wait_done(self, timeout_sec: int = 10):
        pass

    def get_hardware_log(self, compiled_schedule: CompiledSchedule):
        pass


@pytest.fixture(scope="function", name="component_names")
def fixture_component_names() -> int:
    return [f"dev{i}" for i in range(3)]


# creates a few dummy components available to be used in each test
@pytest.fixture(scope="function", name="dummy_components")
def fixture_dummy_components(
    mocker, component_names
) -> base_component.InstrumentCoordinatorComponentBase:
    # Create a QCoDeS instrument for realistic emulation
    instruments = [Instrument(name) for name in component_names]
    components = []

    for instrument in instruments:
        comp = MyICC(instrument)
        for func in ("prepare", "start", "stop", "wait_done", "retrieve_acquisition"):
            mocker.patch.object(
                comp,
                func,
                wraps=getattr(comp, func),
            )
        components.append(comp)

    return components


@pytest.fixture(scope="function", name="instrument_coordinator")
def fixture_instrument_coordinator(component_names) -> InstrumentCoordinator:
    instrument_coordinator = InstrumentCoordinator(
        "ic_0000", add_default_generic_icc=False
    )

    # Mock compiled instructions to make sure data is acquired from components,
    # because in these tests we do not create a compiled schedule.
    instrument_coordinator._compiled_schedule = dict(
        compiled_instructions={name: {} for name in component_names}
    )

    return instrument_coordinator


def test_constructor(instrument_coordinator):
    # Assert
    assert len(instrument_coordinator.components()) == 0


@pytest.mark.parametrize(
    "states,expected",
    [
        ([True, True], True),
        ([False, True], True),
        ([False, False], False),
    ],
)
def test_is_running(
    instrument_coordinator,
    dummy_components,
    states: list[bool],
    expected: bool,
    mocker,
):
    # Arrange
    mocker.patch.object(MyICC, "is_running")  # necessary for overriding `is_running`

    for state in states:
        # popping ensures the reference to the object is released after this for loop
        component = dummy_components.pop(0)
        instrument_coordinator.add_component(component)
        component.is_running = state

    # force garbage collection to emulate qcodes correctly
    gc.collect()

    # Act
    is_running = instrument_coordinator.is_running

    # Assert
    assert is_running == expected


def test_get_component(instrument_coordinator, dummy_components):
    for i in range(len(dummy_components)):
        # Arrange
        component_ = dummy_components.pop(0)
        instrument_coordinator.add_component(component_)

        # Act
        component = instrument_coordinator.get_component(f"ic_dev{i}")

        # Assert
        assert component_ == component


def test_get_component_failed(instrument_coordinator):
    # Act
    with pytest.raises(KeyError) as execinfo:
        instrument_coordinator.get_component("ic_dev1234")

    # Assert
    assert execinfo.value.args[0] == (
        "'dev1234' appears in the hardware config,"
        " but was not added as a component to InstrumentCoordinator 'ic_0000'."
    )


def test_add_component_failed_duplicate(instrument_coordinator, dummy_components):
    # Arrange
    component1 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)

    # Act
    with pytest.raises(ValueError) as execinfo:
        instrument_coordinator.add_component(component1)

    # Assert
    assert execinfo.value.args[0] == "'ic_dev0' has already been added!"


def test_add_component_failed_type_validation(instrument_coordinator):
    @dataclass
    class DummyComponent:
        name: str

        def __repr__(self) -> str:
            return "<DummyComponent>"

    component = DummyComponent("abc")

    # Act
    with pytest.raises(TypeError) as execinfo:
        instrument_coordinator.add_component(component)

    # Assert
    assert execinfo.value.args[0] == (
        "<DummyComponent> is not quantify.instrument_coordinator."
        "components.base.InstrumentCoordinatorComponentBase."
    )


def test_remove_component(instrument_coordinator, dummy_components):
    # Arrange
    component1, component2 = dummy_components.pop(0), dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)

    # Act
    assert instrument_coordinator.components() == ["ic_dev0", "ic_dev1"]
    instrument_coordinator.remove_component("ic_dev0")
    assert instrument_coordinator.components() == ["ic_dev1"]


def test_prepare(
    instrument_coordinator, dummy_components, mocker
):  # NB order of fixtures matters for teardown, keep mocker as last!
    # Arrange
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)

    get_component_spy = mocker.patch.object(
        instrument_coordinator,
        "get_component",
        wraps=instrument_coordinator.get_component,
    )

    # Act
    test_sched = Schedule(name="test_schedule")
    args = {"dev0": {"foo": 0}, "dev1": {"foo": 1}}
    test_sched["compiled_instructions"] = args
    compiled_sched = CompiledSchedule(test_sched)

    instrument_coordinator.prepare(compiled_sched)

    # Assert
    assert get_component_spy.call_args_list == [call("ic_dev0"), call("ic_dev1")]

    component1.prepare.assert_called_with(args["dev0"])
    component2.prepare.assert_called_with(args["dev1"])


def test_start(instrument_coordinator, dummy_components):
    # Arrange
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    component3 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)
    instrument_coordinator.add_component(component3)

    # Act
    test_sched = Schedule(name="test_schedule")
    args = {"dev0": {"foo": 0}, "dev1": {"foo": 1}}
    test_sched["compiled_instructions"] = args
    compiled_sched = CompiledSchedule(test_sched)
    instrument_coordinator.prepare(compiled_sched)

    instrument_coordinator.start()

    # Assert
    component1.start.assert_called()
    component2.start.assert_called()
    component3.start.assert_not_called()


def test_stop(instrument_coordinator, dummy_components):
    # Arrange
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)

    # Act
    instrument_coordinator.stop()

    # Assert
    component1.stop.assert_called()
    component2.stop.assert_called()


def test_retrieve_acquisition(instrument_coordinator, dummy_components):
    # Arrange
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    component3 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)
    instrument_coordinator.add_component(component3)

    dummy_dataarray = DataArray(
        [[1, 2, 3, 4]], coords=[[0], [0, 1, 2, 3]], dims=["repetition", "acq_index"]
    )

    component1.retrieve_acquisition.return_value = Dataset({0: dummy_dataarray})
    component2.retrieve_acquisition.return_value = None

    # Act
    data = instrument_coordinator.retrieve_acquisition()

    # Assert
    component1.retrieve_acquisition.assert_called()
    component2.retrieve_acquisition.assert_called()
    component3.retrieve_acquisition.assert_called()

    expected_dataset = Dataset({0: dummy_dataarray})
    assert data.equals(expected_dataset)


def test_wait_done(instrument_coordinator, dummy_components):
    # Arrange
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)

    timeout: int = 1

    # Act
    instrument_coordinator.wait_done(timeout)

    # Assert
    component1.wait_done.assert_called_with(timeout)
    component2.wait_done.assert_called_with(timeout)


def test_last_schedule(instrument_coordinator, dummy_components):
    component1 = dummy_components.pop(0)
    component2 = dummy_components.pop(0)
    instrument_coordinator.add_component(component1)
    instrument_coordinator.add_component(component2)

    # assert that first there is no schedule prepared yet
    with pytest.raises(ValueError):
        _ = instrument_coordinator.last_schedule

    test_sched = Schedule(name="test_schedule")
    compiled_sched = CompiledSchedule(test_sched)

    # assert that the uploaded schedule is retrieved
    instrument_coordinator.prepare(compiled_sched)
    last_sched = instrument_coordinator.last_schedule

    assert last_sched == compiled_sched
