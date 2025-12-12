import numpy as np

from quantify.backends import SerialCompiler
from quantify.schedules import timedomain_schedules as ts
from tests.fixtures.mock_setup import *  # noqa: F403


# FIXME classmethods cannot use fixtures, these test are mixing testing style
class TestRabiPulse:
    @classmethod
    def setup_class(cls):
        # Clock frequency should match the one defined in the device_cfg
        # to avoid conflicts
        cls.sched_kwargs = {
            "init_duration": 200e-6,
            "mw_g_amp": 0.5,
            "mw_d_amp": 0,
            "mw_frequency": 6.02e9,
            "mw_clock": "q0.01",
            "mw_port": "q0:mw",
            "mw_pulse_duration": 20e-9,
            "ro_pulse_amp": 0.1,
            "ro_pulse_duration": 1e-6,
            "ro_pulse_delay": 200e-9,
            "ro_pulse_port": "q0:res",
            "ro_pulse_clock": "q0.ro",
            "ro_pulse_frequency": 7.04e9,
            "ro_integration_time": 400e-9,
            "ro_acquisition_delay": 120e-9,
            "repetitions": 10,
        }
        cls.uncomp_sched = ts.rabi_pulse_sched(**cls.sched_kwargs)

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == self.sched_kwargs["repetitions"]

    def test_timing(self, device_compile_config_basic_transmon):
        # This will determine the timing
        compiler = SerialCompiler(name="compiler")
        sched = compiler.compile(
            schedule=self.uncomp_sched, config=device_compile_config_basic_transmon
        )

        # test that the right operations are added and timing is as expected.
        labels = ["qubit reset 0", "Rabi_pulse 0", "readout_pulse 0", "acquisition 0"]
        t2 = (
            self.sched_kwargs["init_duration"]
            + self.sched_kwargs["mw_pulse_duration"]
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


class TestRabiSched:
    @classmethod
    def setup_class(cls):
        # Clock frequency should match the one defined in the device_cfg
        # to avoid conflicts
        cls.sched_kwargs = {
            "pulse_amp": 0.2,
            "pulse_duration": 20e-9,
            "frequency": 6.02e9,
            "qubit": "q0",
            "port": None,
            "clock": None,
            "repetitions": 10,
        }
        cls.uncomp_sched = ts.rabi_sched(**cls.sched_kwargs)

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == self.sched_kwargs["repetitions"]

    def test_timing(self, device_compile_config_basic_transmon):
        # This will determine the timing
        compiler = SerialCompiler(name="compiler")
        sched = compiler.compile(
            schedule=self.uncomp_sched, config=device_compile_config_basic_transmon
        )

        # test that the right operations are added and timing is as expected.
        labels = ["Reset 0", "Rabi_pulse 0", "Measurement 0"]
        abs_times = [0, 200e-6, 200e-6 + 20e-9]

        assert len(sched.schedulables) == len(labels)
        for i, schedulable in enumerate(sched.schedulables.values()):
            assert schedulable["label"] == labels[i]
            assert schedulable["abs_time"] == abs_times[i]

    def test_rabi_pulse_ops(self):
        rabi_op_hash = list(self.uncomp_sched.schedulables.values())[1]["operation_id"]
        rabi_pulse = self.uncomp_sched.operations[rabi_op_hash]["pulse_info"][0]
        assert rabi_pulse["G_amp"] == 0.2
        assert rabi_pulse["D_amp"] == 0
        assert rabi_pulse["duration"] == 20e-9
        assert self.uncomp_sched.resources["q0.01"]["freq"] == 6.02e9

    def test_batched_variant_single_val(self, device_compile_config_basic_transmon):
        sched = ts.rabi_sched(
            pulse_amp=np.array([0.5]),
            pulse_duration=20e-9,
            frequency=6.02e9,
            qubit="q0",
            port=None,
            clock=None,
        )
        compiler = SerialCompiler(name="compiler")
        _ = compiler.compile(
            schedule=sched, config=device_compile_config_basic_transmon
        )

        # test that the right operations are added and timing is as expected.
        labels = ["Reset 0", "Rabi_pulse 0", "Measurement 0"]
        assert len(sched.schedulables) == len(labels)
        for i, schedulable in enumerate(sched.schedulables.values()):
            assert schedulable["label"] == labels[i]

        rabi_op_hash = list(sched.schedulables.values())[1]["operation_id"]
        rabi_pulse = sched.operations[rabi_op_hash]["pulse_info"][0]
        assert rabi_pulse["G_amp"] == 0.5
        assert rabi_pulse["D_amp"] == 0
        assert rabi_pulse["duration"] == 20e-9
