class TestEmptyDatabase:
    def test_new_exercises(self, empty_database_fixture, exercise_fixture):
        edf = empty_database_fixture
        edf.new_exercise(exercise_fixture)
