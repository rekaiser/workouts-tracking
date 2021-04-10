class TestEmptyDatabase:
    def test_new_exercises(self, main_window_fixture, groupbox_exercise_fixture,
                           database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        gef = groupbox_exercise_fixture
        gef.button_new.click()
        assert mwf.window_new_exercise.isVisible()
