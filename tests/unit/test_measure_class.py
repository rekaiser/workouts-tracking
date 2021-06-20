from workouts_tracking.measure import Measure


class TestMeasureAttributes:
    def test_measure_attributes(self):
        m = Measure("Test Name", 3, True)
        assert m.name == "Test Name"
        assert m.type_id == 3
        assert m.per_set is True


class TestMeasureMethods:
    def test_values_for_measure_table(self):
        m1 = Measure("Test Name", 3, True)
        assert m1.values_for_measure_table() == ("Test Name", 3, 1)
        m2 = Measure("Test Name", 1, False)
        assert m2.values_for_measure_table() == ("Test Name", 1, 0)
