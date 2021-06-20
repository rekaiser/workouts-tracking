from workouts_tracking.measure import Measure


class TestMeasureAttributes:
    def test_measure_attributes(self):
        m = Measure("Test Name", 3, True, 9)
        assert m.name == "Test Name"
        assert m.type_id == 3
        assert m.per_set is True
        assert m.exercise_id == 9


class TestMeasureMethods:
    def test_values_for_measure_table(self):
        m1 = Measure("Test Name", 3, True, 9)
        assert m1.values_for_measure_table() == ("Test Name", 3, 1, 9)
        m2 = Measure("Test Name", 1, False, 12)
        assert m2.values_for_measure_table() == ("Test Name", 1, 0, 12)
