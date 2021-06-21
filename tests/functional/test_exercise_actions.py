class TestEmptyDatabase:
    def test_new_exercises(self, main_window_fixture, groupbox_exercise_fixture,
                           database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        gef = groupbox_exercise_fixture
        gef.button_new.click()
        assert mwf.window_new_exercise.isVisible()

    def test_added_new_basic_exercise(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        wne = mwf.window_new_exercise
        wne.line_edit_name.setText("Test Exercise")
        wne.button_add_exercise.click()
        exercises = mwf.database.get_exercise_names()
        assert "Test Exercise" in exercises
