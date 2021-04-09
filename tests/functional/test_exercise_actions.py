class TestEmptyDatabase:
    def test_new_exercises(self, main_window_fixture, groupbox_exercise_fixture):
        mwf = main_window_fixture
        gef = groupbox_exercise_fixture
        gef.button_new.click()
        mwf.window_new_exercise.isVisible()
