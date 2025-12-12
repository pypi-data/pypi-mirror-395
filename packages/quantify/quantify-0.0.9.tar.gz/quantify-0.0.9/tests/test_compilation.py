from copy import deepcopy

import networkx as nx
import numpy as np
import pytest

from quantify.backends import SerialCompiler
from quantify.backends.circuit_to_device import ConfigKeyError
from quantify.compilation import (
    _determine_absolute_timing,
    _normalize_absolute_timing,
    _populate_references_graph,
    _validate_schedulable_references,
)
from quantify.enums import BinMode, SchedulingStrategy
from quantify.operations.composite_factories import hadamard_as_y90z
from quantify.operations.control_flow_library import (
    LoopOperation,
)
from quantify.operations.gate_library import (
    CNOT,
    CZ,
    X90,
    H,
    Measure,
    Reset,
    Rxy,
)
from quantify.operations.operation import Operation
from quantify.operations.pulse_library import SquarePulse
from quantify.resources import BasebandClockResource, ClockResource, Resource
from quantify.schedules.schedule import CompiledSchedule, Schedule, ScheduleBase

from .fixtures.mock_setup import *  # noqa: F403
from .fixtures.schedule import *  # noqa: F403


def test_determine_absolute_timing_ideal_clock():
    sched = Schedule("Test experiment")

    # define the resources
    # q0, q1 = Qubits(n=2) # assumes all to all connectivity
    q0, q1 = ("q0", "q1")

    ref_label_1 = "my_label"

    sched.add(Reset(q0, q1))
    sched.add(Rxy(90, 0, qubit=q0), label=ref_label_1)
    sched.add(operation=CNOT(qc=q0, qt=q1))
    sched.add(Rxy(theta=90, phi=0, qubit=q0))
    sched.add(Measure(q0, q1), label="M0")

    assert len(sched.data["operation_dict"]) == 4
    assert len(sched.data["schedulables"]) == 5

    for schedulable in sched.data["schedulables"].values():
        assert "abs_time" not in schedulable
        assert schedulable["timing_constraints"][0]["rel_time"] == 0

    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 2, 3, 4]

    # add a pulse and schedule simultaneous with the second pulse
    sched.add(Rxy(90, 0, qubit=q1), ref_pt="start", ref_op=ref_label_1)
    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        constr["abs_time"] for constr in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 2, 3, 4, 1]

    sched.add(Rxy(90, 0, qubit=q1), ref_pt="start", ref_op="M0")
    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 2, 3, 4, 1, 4]

    sched.add(Rxy(90, 0, qubit=q1), ref_pt="end", ref_op=ref_label_1)
    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 2, 3, 4, 1, 4, 2]

    sched.add(Rxy(90, 0, qubit=q1), ref_pt="center", ref_op=ref_label_1)
    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 2, 3, 4, 1, 4, 2, 1.5]

    bad_sched = Schedule("no good")
    bad_sched.add(Rxy(180, 0, qubit=q1))
    bad_sched.add(Rxy(90, 0, qubit=q1), ref_pt="bad")
    with pytest.raises(NotImplementedError):
        _ = _determine_absolute_timing(schedule=bad_sched, time_unit="ideal")


def test_determine_absolute_timing_alap(
    mock_setup_basic_transmon_with_standard_params, schedule_with_measurement
):
    quantum_device = mock_setup_basic_transmon_with_standard_params["quantum_device"]
    quantum_device.scheduling_strategy(SchedulingStrategy.ALAP)
    assert quantum_device.scheduling_strategy() == SchedulingStrategy.ALAP

    schedule = _determine_absolute_timing(
        schedule=schedule_with_measurement,
        time_unit="ideal",
        config=quantum_device.generate_compilation_config(),
    )
    assert isinstance(schedule, Schedule)

    references_graph = _populate_references_graph(schedule)
    schedulable_iterator = nx.topological_sort(references_graph)
    root_schedulable = next(schedulable_iterator)

    assert root_schedulable == "measure"


def test_determine_absolute_timing_asap(
    mock_setup_basic_transmon_with_standard_params, schedule_with_measurement
):
    quantum_device = mock_setup_basic_transmon_with_standard_params["quantum_device"]
    quantum_device.scheduling_strategy(SchedulingStrategy.ASAP)
    assert quantum_device.scheduling_strategy() == SchedulingStrategy.ASAP

    schedule = _determine_absolute_timing(
        schedule=schedule_with_measurement,
        time_unit="ideal",
        config=quantum_device.generate_compilation_config(),
    )
    assert isinstance(schedule, Schedule)

    references_graph = _populate_references_graph(schedule)
    schedulable_iterator = nx.topological_sort(references_graph)
    root_schedulable = next(schedulable_iterator)

    assert root_schedulable == "reset"


def test_missing_ref_op():
    sched = Schedule("test")
    q0, q1 = ("q0", "q1")
    ref_label_1 = "test_label"
    sched.add(operation=CNOT(qc=q0, qt=q1), ref_op=ref_label_1)
    graph = _populate_references_graph(sched)

    with pytest.raises(ValueError):
        _validate_schedulable_references(sched, graph)


def test_compile_transmon_program(mock_setup_basic_transmon_with_standard_params):
    sched = Schedule("Test schedule")

    # Define the resources
    q0, q2 = ("q0", "q2")

    sched.add(Reset(q0, q2))
    sched.add(Rxy(90, 0, qubit=q0))
    sched.add(operation=CZ(qc=q0, qt=q2))
    sched.add(Rxy(theta=90, phi=0, qubit=q0))
    sched.add(Measure(q0, q2), label="M0")

    compiler = SerialCompiler(name="compiler")
    compiler.compile(
        sched,
        mock_setup_basic_transmon_with_standard_params[
            "quantum_device"
        ].generate_compilation_config(),
    )


def test_compiled_schedule_returns_compiled_schedule_type(
    device_compile_config_basic_transmon,
):
    """Regression test for !110: compilation must return a CompiledSchedule."""

    sched = Schedule("test")
    sched.add(Rxy(90, 0, qubit="q0"))

    compiler = SerialCompiler(name="compiler")
    result = compiler.compile(sched, config=device_compile_config_basic_transmon)

    assert isinstance(result, CompiledSchedule)


def test_compile_gates_to_subschedule(mock_setup_basic_transmon_with_standard_params):
    compiler = SerialCompiler(name="compiler")

    # Add H composite gate to sched and compile to subschedules
    sched = Schedule("Schedule")
    sched.add(H("q0", "q1"))
    compiled_sched = compiler.compile(
        sched,
        mock_setup_basic_transmon_with_standard_params[
            "quantum_device"
        ].generate_compilation_config(),
    )

    # Add H constituent gates Y90 and Z to sched directly as subschedules
    expected_inner_sched = Schedule("Inner schedule for H('q0','q1')")
    ref_h = expected_inner_sched.add(hadamard_as_y90z("q0"))
    expected_inner_sched.add(hadamard_as_y90z("q1"), ref_op=ref_h, ref_pt="start")

    expected_sched = Schedule("Expected sched")
    expected_sched.add(expected_inner_sched)

    expected_compiled_sched = compiler.compile(
        expected_sched,
        mock_setup_basic_transmon_with_standard_params[
            "quantum_device"
        ].generate_compilation_config(),
    )

    def _compare_op(op, expected_op):
        assert type(op) is type(expected_op)
        if isinstance(op, ScheduleBase):
            assert len(op) == len(expected_op)
            for schedulable, expected_schedulable in zip(
                op.schedulables.values(),
                expected_op.schedulables.values(),
            ):
                inner_op = op.operations[schedulable["operation_id"]]
                inner_expected_op = expected_op.operations[
                    expected_schedulable["operation_id"]
                ]
                _compare_op(inner_op, inner_expected_op)
        elif isinstance(op, LoopOperation):
            assert op.data["control_flow"] == expected_op["control_flow"]
            _compare_op(op.body, expected_op.body)
        else:
            assert op == expected_op

    _compare_op(compiled_sched, expected_compiled_sched)


def test_missing_edge(mock_setup_basic_transmon):
    sched = Schedule("Missing edge")

    quantum_device = mock_setup_basic_transmon["quantum_device"]
    quantum_device.remove_edge("q0_q2")

    q0, q2 = ("q0", "q2")
    sched.add(operation=CZ(qc=q0, qt=q2))
    with pytest.raises(
        ConfigKeyError,
        match='edge "q0_q2" is not present in the configuration file',
    ):
        compiler = SerialCompiler(name="compiler")
        compiler.compile(
            sched,
            quantum_device.generate_compilation_config(),
        )


def test_empty_sched():
    sched = Schedule("empty")
    with pytest.raises(ValueError, match="schedule 'empty' contains no schedulables"):
        _ = _determine_absolute_timing(schedule=sched)


def test_bad_gate(device_compile_config_basic_transmon):
    class NotAGate(Operation):
        def __init__(self, q):
            plot_func = "quantify.schedules._visualization.circuit_diagram.cnot"
            data = {
                "gate_info": {
                    "unitary": np.array(
                        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
                    ),
                    "tex": r"bad",
                    "plot_func": plot_func,
                    "device_elements": [q],
                    "operation_type": "bad",
                }
            }
            super().__init__(f"bad ({q})")
            self.data.update(data)

    sched = Schedule("Bell experiment")
    sched.add(Reset("q0"))
    sched.add(NotAGate("q0"))
    with pytest.raises(
        ConfigKeyError,
        match='\'operation "bad" is not present in the configuration file.*',
    ):
        compiler = SerialCompiler(name="compiler")
        compiler.compile(
            sched,
            config=device_compile_config_basic_transmon,
        )


def test_pulse_and_clock(device_compile_config_basic_transmon):
    sched = Schedule("pulse_no_clock")
    mystery_clock = "BigBen"
    schedulable = sched.add(SquarePulse(0.5, 20e-9, "q0:mw_ch", clock=mystery_clock))
    op = sched.operations[schedulable["operation_id"]]

    compiler = SerialCompiler(name="compiler")
    with pytest.raises(ValueError) as execinfo:
        compiler.compile(
            sched,
            config=device_compile_config_basic_transmon,
        )
    assert str(execinfo.value) == (
        f"Operation '{op!s}' contains an unknown clock '{mystery_clock}'; "
        f"ensure this resource has been added to the schedule "
        f"or to the device config."
    )

    sched.add_resource(ClockResource(mystery_clock, 6e9))
    compiler.compile(
        sched,
        config=device_compile_config_basic_transmon,
    )


def test_resource_resolution(device_compile_config_basic_transmon):
    sched = Schedule("resource_resolution")
    qcm0_s0 = Resource("qcm0.s0")
    qcm0_s0["type"] = "qcm"
    qrm0_s0 = Resource("qrm0.s0")
    qrm0_s0["type"] = "qrm"

    sched.add(Rxy(90, 0, "q0"))
    sched.add(SquarePulse(0.6, 20e-9, "q0:mw_ch", clock=BasebandClockResource.IDENTITY))
    sched.add(SquarePulse(0.4, 20e-9, "q0:ro_ch", clock=BasebandClockResource.IDENTITY))

    sched.add_resources([qcm0_s0, qrm0_s0])
    compiler = SerialCompiler(name="compiler")
    _ = compiler.compile(
        sched,
        config=device_compile_config_basic_transmon,
    )


def test_schedule_modified(device_compile_config_basic_transmon):
    q0, q1 = ("q0", "q1")

    ref_label_1 = "my_label"
    sched = Schedule("Test experiment")
    sched.add(Reset(q0, q1))
    sched.add(Rxy(90, 0, qubit=q0), label=ref_label_1)
    sched.add(Rxy(theta=90, phi=0, qubit=q0))
    sched.add(Measure(q0, q1), label="M0")

    copy_of_sched = deepcopy(sched)
    # to verify equality of schedule object works
    assert copy_of_sched == sched

    config = device_compile_config_basic_transmon
    config.keep_original_schedule = True

    compiler = SerialCompiler(name="compiler")
    _ = compiler.compile(
        sched,
        config=device_compile_config_basic_transmon,
    )
    # Fails if schedule is modified
    assert copy_of_sched == sched


def test_measurement_specification_of_binmode(device_compile_config_basic_transmon):
    qubit = "q0"

    ####################################################################################
    # Append selected
    ####################################################################################

    schedule = Schedule("binmode-test", 1)
    schedule.add(Reset(qubit), label=f"Reset {0}")
    schedule.add(
        Measure(qubit, coords={"index": 0}, bin_mode=BinMode.APPEND),
        label=f"Measurement {0}",
    )

    compiler = SerialCompiler(name="compiler")
    comp_sched = compiler.compile(
        schedule=schedule,
        config=device_compile_config_basic_transmon,
    )

    for value in comp_sched.data["operation_dict"].values():
        if "Measure" in str(value):
            assert value.data["acquisition_info"][0]["bin_mode"] == BinMode.APPEND

    ####################################################################################
    # AVERAGE selected
    ####################################################################################

    schedule = Schedule("binmode-test", 1)
    schedule.add(Reset(qubit), label=f"Reset {0}")
    schedule.add(
        Measure(qubit, coords={"index": 0}, bin_mode=BinMode.AVERAGE),
        label=f"Measurement {0}",
    )

    comp_sched = compiler.compile(
        schedule=schedule,
        config=device_compile_config_basic_transmon,
    )

    for value in comp_sched.data["operation_dict"].values():
        if "Measure" in str(value):
            assert value.data["acquisition_info"][0]["bin_mode"] == BinMode.AVERAGE

    ####################################################################################
    # Not specified uses default average mode
    ####################################################################################

    schedule = Schedule("binmode-test", 1)
    schedule.add(Reset(qubit), label=f"Reset {0}")
    schedule.add(Measure(qubit, coords={"index": 0}), label=f"Measurement {0}")

    comp_sched = compiler.compile(
        schedule=schedule,
        config=device_compile_config_basic_transmon,
    )

    for value in comp_sched.data["operation_dict"].values():
        if "Measure" in str(value):
            assert value.data["acquisition_info"][0]["bin_mode"] == BinMode.AVERAGE


def test_compile_trace_acquisition(
    device_compile_config_basic_transmon, get_subschedule_operation
):
    sched = Schedule("Test schedule")
    q0 = "q0"
    sched.add(Reset(q0))
    sched.add(Rxy(90, 0, qubit=q0))
    sched.add(Measure(q0, acq_protocol="Trace"), label="M0")

    compiler = SerialCompiler(name="compile")
    sched = compiler.compile(
        schedule=sched, config=device_compile_config_basic_transmon
    )

    assert (
        get_subschedule_operation(sched, [2, 2])["acquisition_info"][0]["protocol"]
        == "Trace"
    )


def test_compile_no_device_cfg_determine_absolute_timing(
    mocker, device_compile_config_basic_transmon
):
    sched = Schedule("One pulse schedule")
    sched.add(SquarePulse(amp=1 / 4, duration=12e-9, port="q0:mw", clock="q0.01"))

    mock = mocker.patch("quantify.compilation._determine_absolute_timing")
    compiler = SerialCompiler(name="compile")
    compiler.compile(schedule=sched, config=device_compile_config_basic_transmon)
    assert mock.is_called()


def test_determine_absolute_timing_subschedule():
    sched = Schedule("Outer")
    inner_sched = Schedule("Inner")

    # define the resources
    # q0, q1 = Qubits(n=2) # assumes all to all connectivity
    q0, q1 = ("q0", "q1")

    ref_label_1 = "ref0_2"

    inner_sched.add(Reset(q0, q1), label="ref1_0")
    inner_sched.add(Rxy(90, 0, qubit=q0), label="ref1_1")

    sched.add(operation=CNOT(qc=q0, qt=q1), label="ref0_0")
    sched.add(inner_sched, label="ref0_1")
    sched.add(Measure(q0), label="ref0_2")

    assert len(sched.data["operation_dict"]) == 3
    assert len(sched.data["schedulables"]) == 3

    for schedulable in sched.data["schedulables"].values():
        assert "abs_time" not in schedulable
        assert schedulable["timing_constraints"][0]["rel_time"] == 0

    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 3]
    inner_sched_schedulable = timed_sched.data["schedulables"]["ref0_1"]
    timed_inner = timed_sched.operations[inner_sched_schedulable["operation_id"]]
    abs_times = [
        schedulable["abs_time"]
        for schedulable in timed_inner.data["schedulables"].values()
    ]
    assert abs_times == [0, 1]

    # add a pulse and schedule simultaneous with the second pulse
    sched.add(Rxy(90, 0, qubit=q1), ref_pt="start", ref_op=ref_label_1)
    timed_sched = _determine_absolute_timing(sched, time_unit="ideal")

    abs_times = [
        constr["abs_time"] for constr in timed_sched.data["schedulables"].values()
    ]
    assert abs_times == [0, 1, 3, 3]


def test_negative_absolute_timing_is_normalized():
    schedule = Schedule("test")
    schedule.add(SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"))
    schedule.add(
        SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"), rel_time=-2
    )

    schedule = _normalize_absolute_timing(_determine_absolute_timing(schedule))
    schedulables = schedule.schedulables.values()
    abs_times = [schedulable["abs_time"] for schedulable in schedulables]
    np.testing.assert_almost_equal(abs_times, np.array([2 - 100e-9, 0]))


@pytest.mark.xfail(
    reason="Normalization of absolute timing in subschedules is not yet supported.",
    strict=True,
)
def test_negative_absolute_timing_is_normalized_with_subschedule():
    """Test that absolute timing is properly normalized in schedules with
    subschedules.

    TODO: This test is currently marked as xfail because normalization of
    absolute timing in subschedules is not yet supported. When implementing
    this feature, please remove the xfail marker. See
    https://gitlab.com/quantify-os/quantify-scheduler/-/issues/489
    """
    schedule = Schedule("test")
    subschedule = Schedule("subschedule")
    subschedule.add(SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"))
    subschedule.add(
        SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"), rel_time=-3
    )
    schedule.add(subschedule, label="subsched")
    schedule.add(SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"))
    schedule.add(
        SquarePulse(duration=100e-9, amp=0.1, port="q0:mw", clock="q0.mw"), rel_time=-2
    )

    schedule = _normalize_absolute_timing(_determine_absolute_timing(schedule))
    schedulables = schedule.schedulables.values()
    abs_times = [schedulable["abs_time"] for schedulable in schedulables]
    np.testing.assert_almost_equal(abs_times, np.array([2 - 200e-9, 2 - 100e-9, 0]))

    operation_id = schedule.schedulables["subsched"]["operation_id"]
    subschedulables = schedule.operations[operation_id].schedulables.values()
    abs_times = [schedulable["abs_time"] for schedulable in subschedulables]
    np.testing.assert_almost_equal(abs_times, np.array([3, 0]))


def test_multiple_timing_constraints_asap(
    mock_setup_basic_transmon_with_standard_params,
):
    quantum_device = mock_setup_basic_transmon_with_standard_params["quantum_device"]
    quantum_device.scheduling_strategy(SchedulingStrategy.ASAP)
    assert quantum_device.scheduling_strategy() == SchedulingStrategy.ASAP

    # Create a schedule with multiple timing constraints
    sched = Schedule("Test schedule with multiple timing constraints")

    for idx, theta in enumerate(np.linspace(0, 360, 21)):
        sched.add(Reset("q0", "q2"))
        x0 = sched.add(X90("q0"))
        sched.add(X90("q2"), ref_pt="start")  # Start at the same time as the other X90
        cz = sched.add(CZ("q0", "q2"))
        cz.add_timing_constraint(
            ref_schedulable=x0
        )  # Required in case x1 is longer than x0
        sched.add(Rxy(theta=theta, phi=0, qubit="q0"))

        sched.add(Measure("q0", coords={"index": idx}), label=f"M q0 {theta:.2f} deg")
        sched.add(
            Measure("q2", coords={"index": idx}),
            label=f"M q2 {theta:.2f} deg",
            ref_pt="start",  # Start at the same time as the other measure
        )
    # Setting rxy pulse durations to check for correct scheduling
    mock_setup_basic_transmon_with_standard_params["q0"].rxy.duration(40e-9)
    mock_setup_basic_transmon_with_standard_params["q2"].rxy.duration(20e-9)

    # Compile the schedule
    compiler = SerialCompiler(name="compiler")
    compiled_sched = compiler.compile(
        schedule=sched, config=quantum_device.generate_compilation_config()
    )
    # Timing table of the compiled schedule
    timing_table = compiled_sched.timing_table.data

    # Extract the absolute times of CZ operations and the X90 operations
    cz_abs_time = [
        row["abs_time"]
        for i, row in timing_table.iterrows()
        if row["operation"] == "CZ(qc='q0',qt='q2')"
    ]
    x90_abs_time = [
        row["abs_time"]
        for i, row in timing_table.iterrows()
        if row["operation"] == "X90(qubit='q0')"
    ]
    # Based on the timing constraints, the CZ operation should start 40ns
    # after the X90 operation
    assert cz_abs_time[0] - x90_abs_time[0] == pytest.approx(40e-9), (
        "CZ operation should start 40ns after the X90 operation"
    )
