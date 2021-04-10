from workouts_tracking.exercise import Exercise


class TestExerciseMethods:
    def test_record(self):
        exercise = Exercise("Test Name", 3)
        assert exercise.record() == ("Test Name", 3)

    def test_create_columns_string(self):
        exercise = Exercise("Test Exercise", 1)
        assert exercise.create_columns_string() == "name TEXT, number_measures INT"
