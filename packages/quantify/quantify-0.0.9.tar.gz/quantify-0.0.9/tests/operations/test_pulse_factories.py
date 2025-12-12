"""Tests for pulse factory functions."""

import pytest

from quantify.operations.pulse_factories import (
    nv_spec_pulse_mw,
    rxy_drag_pulse,
    rxy_gauss_pulse,
    rxy_pulse,
)


def test_rxy_drag_pulse():
    """Test a long_ramp_pulse that is composed of one part."""
    pulse = rxy_drag_pulse(
        amp180=0.6,
        motzoi=0.2,
        theta=200,
        phi=19,
        port="q0:res",
        duration=1e-7,
        clock="q0.ro",
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.drag",
            "G_amp": 0.6 * 200 / 180,
            "D_amp": 0.2,
            "reference_magnitude": None,
            "duration": 1e-7,
            "phase": 19,
            "nr_sigma": 4,
            "sigma": None,
            "clock": "q0.ro",
            "port": "q0:res",
            "t0": 0,
        }
    ]


def test_rxy_gauss_pulse():
    """Test a long_ramp_pulse that is composed of one part."""
    pulse = rxy_gauss_pulse(
        amp180=0.8, theta=180, phi=10, port="q0:res", duration=1e-7, clock="q0.ro"
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.drag",
            "G_amp": 0.8,
            "D_amp": 0,
            "reference_magnitude": None,
            "duration": 1e-7,
            "phase": 10,
            "nr_sigma": 4,
            "sigma": None,
            "clock": "q0.ro",
            "port": "q0:res",
            "t0": 0,
        }
    ]


def test_rxy_pulse():
    """Test the rxy_pulse"""
    pulse = rxy_pulse(
        amp180=0.8,
        theta=180,
        phi=10,
        port="q0:res",
        duration=100e-9,
        clock="q0.ro",
        skewness=0.0,
        pulse_shape="SkewedHermitePulse",
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.skewed_hermite",
            "duration": 100e-9,
            "amplitude": 0.8,
            "skewness": 0.0,
            "phase": 10,
            "port": "q0:res",
            "clock": "q0.ro",
            "reference_magnitude": None,
            "t0": 0.0,
        }
    ]


def test_unsupported_pulse_shape_rxy():
    """Test rxy_pulse with unsupported pulse shape."""
    with pytest.raises(
        ValueError,
        match=(
            r"Unsupported pulse shape: \w+\. Use 'SkewedHermitePulse' or "
            r"'GaussPulse'\."
        ),
    ):
        rxy_pulse(
            amp180=0.8,
            theta=180,
            phi=10,
            port="q0:res",
            duration=100e-9,
            clock="q0.ro",
            skewness=0.0,
            pulse_shape="Staircase",  # type: ignore
        )


def test_unsupported_pulse_shape_nv_spec():
    """Test nv_spec_pulse_mw with unsupported pulse shape."""
    with pytest.raises(
        ValueError,
        match=(
            r"Unsupported pulse shape: \w+\. "
            r"Use 'SquarePulse', 'SkewedHermitePulse', or 'GaussPulse'\."
        ),
    ):
        nv_spec_pulse_mw(
            duration=10e-9,
            amplitude=0.5,
            clock="q0.ro",
            port="q0:res",
            pulse_shape="Staircase",  # type: ignore
        )


def test_nv_spec_pulse_mw_square():
    """Test the nv_spec_pulse_mw with SquarePulse."""
    pulse = nv_spec_pulse_mw(
        duration=1e-7,
        amplitude=0.8,
        clock="q0.ro",
        port="q0:res",
        pulse_shape="SquarePulse",
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.square",
            "amp": 0.8,
            "duration": 1e-7,
            "port": "q0:res",
            "clock": "q0.ro",
            "reference_magnitude": None,
            "t0": 0,
        }
    ]


def test_nv_spec_pulse_mw_skewed_hermite():
    """Test the nv_spec_pulse_mw with SkewedHermitePulse."""
    pulse = nv_spec_pulse_mw(
        duration=1e-7,
        amplitude=0.8,
        clock="q0.ro",
        port="q0:res",
        pulse_shape="SkewedHermitePulse",
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.skewed_hermite",
            "amplitude": 0.8,
            "duration": 1e-7,
            "skewness": 0.0,
            "phase": 0,
            "port": "q0:res",
            "clock": "q0.ro",
            "reference_magnitude": None,
            "t0": 0.0,
        }
    ]


def test_nv_spec_pulse_mw_gauss():
    """Test the nv_spec_pulse_mw with GaussPulse."""
    pulse = nv_spec_pulse_mw(
        duration=1e-7,
        amplitude=0.8,
        clock="q0.ro",
        port="q0:res",
        pulse_shape="GaussPulse",
    )
    assert pulse.data["pulse_info"] == [
        {
            "wf_func": "quantify.waveforms.drag",
            "G_amp": 0.8,
            "D_amp": 0,
            "reference_magnitude": None,
            "duration": 100e-9,
            "phase": 0,
            "nr_sigma": 4,
            "sigma": None,
            "clock": "q0.ro",
            "port": "q0:res",
            "t0": 0,
        }
    ]
