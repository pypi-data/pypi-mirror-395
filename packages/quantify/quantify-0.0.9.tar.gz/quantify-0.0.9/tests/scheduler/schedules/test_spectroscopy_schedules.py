import math

import numpy as np

from quantify.backends import SerialCompiler
from quantify.compilation import _determine_absolute_timing
from quantify.schedules import spectroscopy_schedules as sps
from tests.fixtures.mock_setup import *  # noqa: F403


class TestHeterodyneSpecSchedule:
    @classmethod
    def setup_class(cls):
        cls.sched_kwargs = {
            "pulse_amp": 0.15,
            "pulse_duration": 1e-6,
            "port": "q0:res",
            "clock": "q0.ro",
            "frequency": 7.04e9,
            "integration_time": 1e-6,
            "acquisition_delay": 220e-9,
            "init_duration": 18e-6,
            "repetitions": 10,
        }
        cls.uncomp_sched = sps.heterodyne_spec_sched(**cls.sched_kwargs)

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == self.sched_kwargs["repetitions"]

    def test_timing(self):
        """Test that the right operations are added and timing is as expected."""
        sched = _determine_absolute_timing(self.uncomp_sched)

        labels = ["buffer", "spec_pulse", "acquisition"]
        abs_times = [
            0,
            self.sched_kwargs["init_duration"],
            self.sched_kwargs["init_duration"] + self.sched_kwargs["acquisition_delay"],
        ]

        for i, schedulable in enumerate(sched.schedulables.values()):
            assert schedulable["label"] == labels[i]
            assert schedulable["abs_time"] == abs_times[i]

    def test_compiles_device_cfg_only(self, device_compile_config_basic_transmon):
        # assert that files properly compile
        compiler = SerialCompiler(name="compiler")
        compiler.compile(
            schedule=self.uncomp_sched, config=device_compile_config_basic_transmon
        )


class TestHeterodyneSpecScheduleNCO(TestHeterodyneSpecSchedule):
    @classmethod
    def setup_class(cls):
        cls.sched_kwargs = {
            "pulse_amp": 0.15,
            "pulse_duration": 1e-6,
            "port": "q0:res",
            "clock": "q0.ro",
            "frequencies": np.linspace(start=6.8e9, stop=7.2e9, num=5),
            "integration_time": 1e-6,
            "acquisition_delay": 220e-9,
            "init_duration": 18e-6,
            "repetitions": 10,
        }
        cls.uncomp_sched = sps.heterodyne_spec_sched_nco(**cls.sched_kwargs)

    def test_timing(self):
        """Test that the right operations are added and timing is as expected."""
        sched = _determine_absolute_timing(self.uncomp_sched)

        labels = ["buffer", "set_freq", "spec_pulse", "acquisition"]
        labels *= len(self.sched_kwargs["frequencies"])

        rel_times = [
            self.sched_kwargs["init_duration"],
            0,
            self.sched_kwargs["acquisition_delay"],
            self.sched_kwargs["integration_time"],
        ]
        rel_times *= len(self.sched_kwargs["frequencies"])

        abs_time = 0.0
        for i, schedulable in enumerate(sched.schedulables.values()):
            assert labels[i] in schedulable["label"]
            assert math.isclose(
                schedulable["abs_time"], abs_time, abs_tol=0.0, rel_tol=1e-15
            ), schedulable["label"]
            abs_time += rel_times[i]


class TestTwoToneSpecSchedule:
    @classmethod
    def setup_class(cls):
        cls.sched_kwargs = {
            "spec_pulse_amp": 0.5,
            "spec_pulse_duration": 1e-6,
            "spec_pulse_port": "q0:mw",
            "spec_pulse_clock": "q0.01",
            "spec_pulse_frequency": 6.02e9,
            "ro_pulse_amp": 0.15,
            "ro_pulse_duration": 1e-6,
            "ro_pulse_delay": 1e-6,
            "ro_pulse_port": "q0:res",
            "ro_pulse_clock": "q0.ro",
            "ro_pulse_frequency": 7.04e9,
            "ro_integration_time": 1e-6,
            "ro_acquisition_delay": 220e-9,
            "init_duration": 18e-6,
            "repetitions": 10,
        }
        cls.uncomp_sched = sps.two_tone_spec_sched(**cls.sched_kwargs)

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == self.sched_kwargs["repetitions"]

    def test_timing(self):
        """Test that the right operations are added and timing is as expected."""
        sched = _determine_absolute_timing(self.uncomp_sched)

        labels = ["buffer", "spec_pulse", "readout_pulse", "acquisition"]

        t2 = (
            self.sched_kwargs["init_duration"]
            + self.sched_kwargs["spec_pulse_duration"]
            + self.sched_kwargs["ro_pulse_delay"]
        )
        t3 = t2 + self.sched_kwargs["ro_acquisition_delay"]
        abs_times = [0, self.sched_kwargs["init_duration"], t2, t3]

        for i, schedulable in enumerate(sched.schedulables.values()):
            assert schedulable["label"] == labels[i]
            assert schedulable["abs_time"] == abs_times[i]

    def test_compiles_device_cfg_only(self, device_compile_config_basic_transmon):
        # assert that files properly compile
        compiler = SerialCompiler(name="compiler")
        compiler.compile(
            schedule=self.uncomp_sched, config=device_compile_config_basic_transmon
        )


class TestTwoToneSpecScheduleNCO(TestTwoToneSpecSchedule):
    @classmethod
    def setup_class(cls):
        cls.sched_kwargs = {
            "spec_pulse_amp": 0.5,
            "spec_pulse_duration": 1e-6,
            "spec_pulse_port": "q0:mw",
            "spec_pulse_clock": "q0.01",
            "spec_pulse_frequencies": np.linspace(start=6.8e9, stop=7.2e9, num=5),
            "ro_pulse_amp": 0.15,
            "ro_pulse_duration": 1e-6,
            "ro_pulse_delay": 1e-6,
            "ro_pulse_port": "q0:res",
            "ro_pulse_clock": "q0.ro",
            "ro_pulse_frequency": 7.04e9,
            "ro_integration_time": 1e-6,
            "ro_acquisition_delay": 220e-9,
            "init_duration": 18e-6,
            "repetitions": 10,
        }
        cls.uncomp_sched = sps.two_tone_spec_sched_nco(**cls.sched_kwargs)

    def test_timing(self):
        """Test that the right operations are added and timing is as expected."""
        sched = _determine_absolute_timing(self.uncomp_sched)

        labels = ["buffer", "set_freq", "spec_pulse", "readout_pulse", "acquisition"]
        labels *= len(self.sched_kwargs["spec_pulse_frequencies"])

        rel_times = [
            self.sched_kwargs["init_duration"],
            0,
            self.sched_kwargs["spec_pulse_duration"]
            + self.sched_kwargs["ro_pulse_delay"],
            self.sched_kwargs["ro_acquisition_delay"],
            self.sched_kwargs["ro_integration_time"],
        ]
        rel_times *= len(self.sched_kwargs["spec_pulse_frequencies"])

        abs_time = 0.0
        for i, schedulable in enumerate(sched.schedulables.values()):
            assert labels[i] in schedulable["label"]
            assert math.isclose(
                schedulable["abs_time"], abs_time, abs_tol=0.0, rel_tol=1e-15
            ), schedulable["label"]
            abs_time += rel_times[i]
