from quantify.operations.control_flow_library import LoopOperation
from quantify.operations.gate_library import Measure, Rxy
from quantify.schedules.schedule import Schedule


class TestSubschedules:
    @classmethod
    def setup_class(cls):
        inner_schedule = Schedule("inner", repetitions=1)
        ref = inner_schedule.add(Rxy(0, 0, "q0"), label="inner0")
        inner_schedule.add(Rxy(0, 1, "q0"), rel_time=40e-9, ref_op=ref, label="inner1")

        outer_schedule = Schedule("outer", repetitions=10)
        ref = outer_schedule.add(Rxy(1, 0, "q0"), label="outer0")
        outer_schedule.add(inner_schedule, rel_time=80e-9, ref_op=ref)
        outer_schedule.add(Measure("q0"), label="measure")
        cls.uncomp_sched = outer_schedule

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == 10


class TestLoops:
    @classmethod
    def setup_class(cls):
        inner_schedule = Schedule("inner", repetitions=1)
        ref = inner_schedule.add(Rxy(0, 0, "q0"), label="inner0")
        inner_schedule.add(Rxy(0, 1, "q0"), rel_time=40e-9, ref_op=ref, label="inner1")

        outer_schedule = Schedule("outer", repetitions=1)
        ref = outer_schedule.add(Rxy(1, 0, "q0"), label="outer0")

        outer_schedule.add(
            LoopOperation(body=inner_schedule, repetitions=10),
            label="loop",
        )

        outer_schedule.add(Measure("q0"), label="measure")
        cls.uncomp_sched = outer_schedule

    def test_repetitions(self):
        assert self.uncomp_sched.repetitions == 1
