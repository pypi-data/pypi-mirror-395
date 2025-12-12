# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Pytest fixtures for quantify."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

import numpy as np
import pytest

from quantify import Schedule
from quantify.backends import SerialCompiler
from quantify.backends.circuit_to_device import (
    DeviceCompilationConfig,
    compile_circuit_to_device_with_config_validation,
)
from quantify.backends.graph_compilation import SerialCompilationConfig
from quantify.compilation import _determine_absolute_timing
from quantify.operations.gate_library import CZ, X90, Measure, Reset, X
from quantify.schedules.schedule import ScheduleBase
from quantify.schemas.examples.device_example_cfgs import (
    example_transmon_cfg,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from quantify.operations.operation import Operation


@pytest.fixture
def device_cfg_transmon_example() -> Generator[DeviceCompilationConfig, None, None]:
    """
    Circuit to device level compilation for the circuit_to_device
    compilation backend.
    """
    yield DeviceCompilationConfig.model_validate(example_transmon_cfg)


@pytest.fixture
def create_schedule_with_pulse_info(
    device_cfg_transmon_example, basic_schedule: Schedule
):
    def _create_schedule_with_pulse_info(
        schedule: Schedule | None = None, device_config: dict | None = None
    ) -> Schedule:
        _schedule = schedule if schedule is not None else deepcopy(basic_schedule)
        _device_config = (
            DeviceCompilationConfig.model_validate(device_config)
            if device_config is not None
            else device_cfg_transmon_example
        )
        _schedule = compile_circuit_to_device_with_config_validation(
            schedule=_schedule,
            config=SerialCompilationConfig(
                name="test", device_compilation_config=_device_config
            ),
        )
        _schedule = _determine_absolute_timing(schedule=_schedule, time_unit="physical")
        return _schedule

    yield _create_schedule_with_pulse_info


@pytest.fixture
def empty_schedule() -> Schedule:
    return Schedule("Empty Experiment")


@pytest.fixture
def basic_schedule(make_basic_schedule) -> Schedule:
    return make_basic_schedule("q0")


@pytest.fixture
def make_basic_schedule() -> Callable[[str], Schedule]:
    def _make_basic_schedule(qubit: str) -> Schedule:
        schedule = Schedule(f"Basic schedule{' ' + qubit if qubit != 'q0' else ''}")
        schedule.add(X90(qubit))
        return schedule

    return _make_basic_schedule


@pytest.fixture
def make_basic_multi_qubit_schedule() -> Callable[[list[str]], Schedule]:
    def _make_basic_schedule(qubits: list[str]) -> Schedule:
        schedule = Schedule(f"Basic schedule {qubits}")
        for qubit in qubits:
            schedule.add(X90(qubit))
        return schedule

    return _make_basic_schedule


@pytest.fixture
def schedule_with_measurement(make_schedule_with_measurement) -> Schedule:
    """
    Simple schedule with gate and measurement on qubit 0.
    """
    return make_schedule_with_measurement("q0")


@pytest.fixture
def schedule_with_measurement_q2(make_schedule_with_measurement) -> Schedule:
    """
    Simple schedule with gate and measurement on qubit 2.
    """
    return make_schedule_with_measurement("q2")


@pytest.fixture
def make_schedule_with_measurement() -> Callable[[str], Schedule]:
    """
    Simple schedule with gate and measurement on single qubit.
    """

    def _make_schedule_with_measurement(qubit: str):
        schedule = Schedule(f"Schedule with measurement {qubit}")
        schedule.add(Reset(qubit), label="reset")
        schedule.add(X90(qubit))
        schedule.add(Measure(qubit), label="measure")
        return schedule

    return _make_schedule_with_measurement


@pytest.fixture
def two_qubit_gate_schedule():
    sched = Schedule("two_qubit_gate_schedule")
    sched.add(Reset("q2", "q3"))
    sched.add(CZ(qc="q2", qt="q3"))
    return sched


@pytest.fixture
def schedule_with_pulse_info(create_schedule_with_pulse_info) -> Schedule:
    return create_schedule_with_pulse_info()


@pytest.fixture
def compiled_two_qubit_t1_schedule(mock_setup_basic_transmon_with_standard_params):
    """
    a schedule performing T1 on two-qubits simultaneously
    """
    mock_setup = mock_setup_basic_transmon_with_standard_params
    mock_setup["q0"].measure.acq_channel(0)
    mock_setup["q1"].measure.acq_channel(1)

    q0, q1 = ("q0", "q1")
    repetitions = 1024
    schedule = Schedule("Multi-qubit T1", repetitions)

    times = np.arange(0, 60e-6, 3e-6)
    for i, tau in enumerate(times):
        schedule.add(Reset(q0, q1), label=f"Reset {i}")
        schedule.add(X(q0), label=f"pi {i} {q0}")
        schedule.add(X(q1), label=f"pi {i} {q1}", ref_pt="start")

        schedule.add(
            Measure(q0, coords={"index": i}),
            ref_pt="start",
            rel_time=tau,
            label=f"Measurement {q0}{i}",
        )
        schedule.add(
            Measure(q1, oords={"index": i}),
            ref_pt="start",
            rel_time=tau,
            label=f"Measurement {q1}{i}",
        )

    compiler = SerialCompiler(name="compiler")
    comp_t1_sched = compiler.compile(
        schedule, config=mock_setup["quantum_device"].generate_compilation_config()
    )
    return comp_t1_sched


@pytest.fixture
def get_subschedule_operation():
    """
    Circuit to device level compilation for the circuit_to_device
    compilation backend.
    """

    def _get_subschedule_operation(
        operation: ScheduleBase | Operation, indices: list[int]
    ) -> ScheduleBase | Operation | None:
        if isinstance(operation, ScheduleBase) and len(indices) > 0:
            index: int = indices[0]
            schedulable = list(operation.schedulables.values())[index]
            inner_operation = operation.operations[schedulable["operation_id"]]
            return _get_subschedule_operation(inner_operation, indices[1:])
        elif len(indices) == 0:
            return operation
        else:
            return None

    yield _get_subschedule_operation
