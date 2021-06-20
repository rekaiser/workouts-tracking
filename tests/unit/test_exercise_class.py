from workouts_tracking.exercise import Exercise


class TestExerciseAttributes:
    def test_exercise_attributes(self):
        e = Exercise("Test Name", "Test Comment", "Test Url", 1, 2, [2, 3])
        assert e.name == "Test Name"
        assert e.comment == "Test Comment"
        assert e.url == "Test Url"
        assert e.category_id == 1
        assert e.difficulty_id == 2
        assert e.muscle_group_ids == [2, 3]


class TestExerciseMethods:
    def test_values_for_exercise_table(self):
        e = Exercise("Test Name", "Test Comment", "Test Url", 1, 2, [2, 3])
        assert e.values_for_exercise_table() == ("Test Name", "Test Comment", "Test Url", 1, 2)
