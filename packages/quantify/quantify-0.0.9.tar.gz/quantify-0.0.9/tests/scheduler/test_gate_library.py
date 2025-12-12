# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Unit tests for the gate library for use with quantify."""

import json
from unittest import TestCase

import numpy as np
import pytest

from quantify.compilation import (
    _populate_references_graph,
    _validate_schedulable_references,
)
from quantify.json_utils import SchedulerJSONDecoder, SchedulerJSONEncoder
from quantify.operations.gate_library import (
    CNOT,
    CZ,
    X90,
    Y90,
    Z90,
    H,
    Measure,
    Reset,
    Rxy,
    Rz,
    X,
    Y,
    Z,
)
from quantify.operations.operation import Operation
from quantify.schedules import Schedulable, Schedule


def test_schedule_add_schedulables() -> None:
    sched = Schedule("my exp")
    test_lab = "test label"
    x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]
    assert x90_label == test_lab

    with pytest.raises(ValueError):
        x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]

    uuid_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"))["label"]
    assert uuid_label != x90_label

    # not specifying a label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=None)

    # specifying existing label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=x90_label)

    # All schedulables should be valid
    for schedulable in sched.schedulables.values():
        assert Schedulable.is_valid(schedulable)

    graph = _populate_references_graph(sched)
    _validate_schedulable_references(sched, graph)
    assert Schedule.is_valid(sched)


def test_schedule_add_schedulables_one_missing() -> None:
    sched = Schedule("my exp")
    test_lab = "test label"
    x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]
    assert x90_label == test_lab

    with pytest.raises(ValueError):
        x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]

    uuid_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"))["label"]
    assert uuid_label != x90_label

    # not specifying a label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=None)

    # specifying existing label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=x90_label)

    # specifying non-existing label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op="non-existing-operation")

    # All schedulables should be valid
    for schedulable in sched.schedulables.values():
        assert Schedulable.is_valid(schedulable)

    # The schedule should not be valid
    graph = _populate_references_graph(sched)
    with pytest.raises(ValueError):
        _validate_schedulable_references(sched, graph)
        Schedule.is_valid(sched)


def test_schedule_add_schedulables_missing_reference() -> None:
    sched = Schedule("my exp")
    test_lab = "test label"
    x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]
    assert x90_label == test_lab

    with pytest.raises(ValueError):
        x90_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"), label=test_lab)["label"]

    uuid_label = sched.add(Rxy(theta=90, phi=0, qubit="q0"))["label"]
    assert uuid_label != x90_label

    # not specifying a label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=None)

    # specifying existing label should work
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=x90_label)

    # specifying a Schedulable that is not in the Schedule should work
    new_sched = Schedule("redundant")
    new_schedulable = new_sched.add(Rxy(theta=15.4, phi=42.6, qubit="q0"))
    sched.add(Rxy(theta=90, phi=0, qubit="q0"), ref_op=new_schedulable)

    # All schedulables should be valid
    for schedulable in sched.schedulables.values():
        assert Schedulable.is_valid(schedulable)

    # The schedule should not be valid
    graph = _populate_references_graph(sched)
    with pytest.raises(ValueError):
        _validate_schedulable_references(sched, graph)
        Schedule.is_valid(sched)


def test_rxy_angle_modulo() -> None:
    """asserts that theta angles fall in the domain -180 to 180"""
    rxy_270 = Rxy(theta=270, phi=23.9, qubit="q5")
    rxy_m90 = Rxy(theta=-90, phi=23.9, qubit="q5")
    assert rxy_270 == rxy_m90

    assert rxy_270.data["gate_info"]["theta"] == -90.0

    rxy_360 = Rxy(theta=360, phi=23.9, qubit="q5")
    assert rxy_360.data["gate_info"]["theta"] == 0


@pytest.mark.parametrize(
    "operation",
    [
        Rxy(theta=124, phi=23.9, qubit="q5"),
        X90("q1"),
        X("q0"),
        Y90("q1"),
        Y("q1"),
        Rz(theta=124, qubit="q5"),
        Z("q0"),
        Z90("q1"),
        Reset("q0"),
        Reset("q0", "q1"),
        CZ("q0", "q1"),
        CNOT("q0", "q6"),
        H("q0", "q1"),
        Measure("q0", "q6"),
        Measure("q0"),
        Measure("q0", "q6", acq_index=92),
    ],
)
class TestGateLevelOperation:
    def test_gate_is_valid(self, operation: Operation) -> None:
        assert Operation.is_valid(operation)

    def test__repr__(self, operation: Operation) -> None:
        """
        Asserts that evaluating the representation
        of an operation is identical to the operation
        itself.
        """
        # Arrange
        operation_state: str = json.dumps(operation, cls=SchedulerJSONEncoder)

        # Act
        obj = json.loads(operation_state, cls=SchedulerJSONDecoder)
        assert obj == operation

    def test__str__(self, operation: Operation) -> None:
        """
        Asserts that the evaluation of the string representation
        is an instance of the the operation type.
        """
        assert isinstance(eval(str(operation)), type(operation))  # nosec B307

    def test_deserialize(self, operation: Operation) -> None:
        # Arrange
        operation_state: str = json.dumps(operation, cls=SchedulerJSONEncoder)

        # Act
        obj = json.loads(operation_state, cls=SchedulerJSONDecoder)

        # Assert
        if (
            "unitary" in operation.data["gate_info"]
            and operation.data["gate_info"]["unitary"] is not None
        ):
            assert isinstance(obj.data["gate_info"]["unitary"], np.generic | np.ndarray)
            np.testing.assert_array_almost_equal(
                obj.data["gate_info"]["unitary"],
                operation.data["gate_info"]["unitary"],
                decimal=9,
            )

            # TestCase().assertDictEqual cannot compare numpy arrays for equality
            # therefore "unitary" is removed
            del obj.data["gate_info"]["unitary"]
            del operation.data["gate_info"]["unitary"]

        TestCase().assertDictEqual(obj.data, operation.data)


def test_rotation_unitaries() -> None:
    # Set the tolerance in terms of machine precision, one machine epsilon by default
    # Could be increased to allow for less pretty computations with more round-off
    # error.

    atol = float(1 * np.finfo(np.complex128).eps)
    # Test Rxy for all angles:
    # The tests are written in form: target, desired
    np.testing.assert_allclose(
        Rxy(theta=0, phi=0, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) * np.array([[1, 0], [0, 1]]),
        atol=atol,
    )
    np.testing.assert_allclose(
        Rxy(theta=90, phi=0, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1, -1j], [-1j, 1]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        Rxy(theta=-90, phi=90, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1, 1], [-1, 1]]),
        atol=atol,
    )

    # Test for the X180, X90, Y180 and Y90 gates which are derived from Rxy
    np.testing.assert_allclose(
        X(qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) * np.array([[0, -1j], [-1j, 0]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        X90(qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1, -1j], [-1j, 1]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        Y(qubit="q0").data["gate_info"]["unitary"],
        -(1.0 + 0.0j) * np.array([[0, 1], [-1, 0]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        Y90(qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1, -1], [1, 1]]),
        atol=atol,
    )

    # Test Rz for all angles:
    # The tests are written in form: target, desired
    np.testing.assert_allclose(
        Rz(theta=0, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) * np.array([[1, 0], [0, 1]]),
        atol=atol,
    )
    np.testing.assert_allclose(
        Rz(theta=90, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1 - 1j, 0], [0, 1 + 1j]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        Rz(theta=-90, qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1 + 1j, 0], [0, 1 - 1j]]),
        atol=atol,
    )

    # Test for the Z180, Z90 gates which are derived from Rz
    np.testing.assert_allclose(
        Z(qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) * np.array([[-1j, 0], [0, 1j]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        Z90(qubit="q0").data["gate_info"]["unitary"],
        (1.0 + 0.0j) / np.sqrt(2) * np.array([[1 - 1j, 0], [0, 1 + 1j]]),
        atol=atol,
    )

    np.testing.assert_allclose(
        H("q0").data["gate_info"]["unitary"],
        -1j / np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex),
        atol=atol,
    )
