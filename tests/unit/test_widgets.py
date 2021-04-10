import pytest
from PySide6.QtWidgets import (QSplitter, QLayout, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget,
                               QLabel, QPushButton, QGridLayout, QFormLayout, QLineEdit, QSpinBox,
                               QComboBox, QFileDialog,
                               )
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from workouts_tracking.gui import (HLineSunken, ComboboxCategory, GroupBoxDatabase, ComboboxMuscles,
                                   GroupBoxWorkout, GroupBoxExercise, GroupBoxAvailableExercises,
                                   ComboboxDifficulty, WindowNewExercise,
                                   )


class TestMainProperties:
    def test_main_window_title(self, main_window_fixture):
        main_window_fixture.close_database()
        assert main_window_fixture.windowTitle() == "Workouts Tracking"

    def test_logo(self, main_window_fixture):
        assert isinstance(main_window_fixture.logo, QIcon)
        assert not main_window_fixture.logo.pixmap(QSize(32, 32)).isNull()


class TestGuiLayout:
    def test_main_layout(self, main_window_fixture):
        mwf = main_window_fixture
        assert isinstance(mwf.centralWidget(), QSplitter)
        assert isinstance(mwf.layout(), QLayout)
        assert isinstance(mwf.centralWidget().layout(), QHBoxLayout)
        assert isinstance(mwf.centralWidget().widget_left, QWidget)
        assert isinstance(mwf.centralWidget().widget_right, QWidget)
        assert isinstance(mwf.centralWidget().layout().itemAt(0).widget(), QWidget)
        assert isinstance(mwf.centralWidget().layout().itemAt(1).widget(), QWidget)

    def test_left_layout(self, central_widget_fixture):
        cwf = central_widget_fixture
        left_layout = cwf.widget_left.layout()
        assert isinstance(left_layout, QVBoxLayout)

        list_widgets_widget_classes_left = [
            (cwf.widget_left.label_workouts, QLabel),
            (cwf.widget_left.table_workouts, QTableWidget),
            (cwf.widget_left.frame_hline, HLineSunken),
            (cwf.widget_left.label_performed_exercises, QLabel),
            (cwf.widget_left.table_performed_exercises, QTableWidget),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_left):
            assert isinstance(left_layout.itemAt(i).widget(), widget_class)
            assert isinstance(widget, widget_class)

    def test_right_layout(self, central_widget_fixture):
        cwf = central_widget_fixture
        right_layout = cwf.widget_right.layout()
        assert isinstance(right_layout, QVBoxLayout)

        list_widgets_widget_classes_right = [
            (cwf.widget_right.groupbox_database, GroupBoxDatabase),
            (cwf.widget_right.groupbox_workout, GroupBoxWorkout),
            (cwf.widget_right.groupbox_available_exercises, GroupBoxAvailableExercises),
            (cwf.widget_right.groupbox_exercise, GroupBoxExercise),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_right):
            assert isinstance(right_layout.itemAt(i).widget(), widget_class)
            assert isinstance(widget, widget_class)

    def test_left_widgets(self, central_widget_fixture):
        cwf = central_widget_fixture
        assert cwf.widget_left.label_workouts.text() == "Workouts"
        assert cwf.widget_left.label_performed_exercises.text() == "Performed Exercises: Double " \
                                                                   "click a line in the workouts" \
                                                                   " table!"

    def test_right_widgets(self, central_widget_fixture):
        cwf = central_widget_fixture
        assert cwf.widget_right.groupbox_database.title() == "Database Actions"
        assert cwf.widget_right.groupbox_workout.title() == "Workout Actions"
        assert cwf.widget_right.groupbox_available_exercises.title() == "Available Exercises"
        assert cwf.widget_right.groupbox_exercise.title() == "Exercise Actions"

    def test_groupbox_database(self, groupbox_database_fixture):
        gdf = groupbox_database_fixture
        assert isinstance(gdf.layout(), QHBoxLayout)

        list_widgets_widget_classes_database = [
            (gdf.button_new, QPushButton),
            (gdf.button_load, QPushButton),
            (gdf.button_close, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_database):
            assert isinstance(widget, widget_class)
            assert isinstance(gdf.layout().itemAt(i).widget(), widget_class)

    def test_database_buttons(self, groupbox_database_fixture):
        gdf = groupbox_database_fixture
        list_button_texts = ["New Database", "Load Database", "Close Database"]
        for i, button_text in enumerate(list_button_texts):
            assert gdf.layout().itemAt(i).widget().text() == button_text

    def test_groupbox_workout(self, groupbox_workout_fixture):
        gwf = groupbox_workout_fixture
        assert isinstance(gwf.layout(), QHBoxLayout)

        list_widgets_widget_classes_workout = [
            (gwf.button_start, QPushButton),
            (gwf.button_finish, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_workout):
            assert isinstance(widget, widget_class)
            assert isinstance(gwf.layout().itemAt(i).widget(), widget_class)

    def test_workout_buttons(self, groupbox_workout_fixture):
        gwf = groupbox_workout_fixture
        list_button_texts = ["Start Workout", "Finish Workout"]
        for i, button_text in enumerate(list_button_texts):
            assert gwf.layout().itemAt(i).widget().text() == button_text
        assert gwf.button_start.isEnabled() and not gwf.button_finish.isEnabled()
        gwf.button_start.click()
        assert not gwf.button_start.isEnabled() and gwf.button_finish.isEnabled()
        gwf.button_finish.click()
        assert gwf.button_start.isEnabled() and not gwf.button_finish.isEnabled()

    def test_groupbox_exercise(self, groupbox_exercise_fixture):
        gef = groupbox_exercise_fixture
        assert isinstance(gef.layout(), QHBoxLayout)

        list_widgets_widget_classes_exercise = [
            (gef.button_perform, QPushButton),
            (gef.button_new, QPushButton),
            (gef.button_edit, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_exercise):
            assert isinstance(widget, widget_class)
            assert isinstance(gef.layout().itemAt(i).widget(), widget_class)

    def test_exercise_buttons(self, groupbox_exercise_fixture):
        gef = groupbox_exercise_fixture
        list_button_texts = ["Perform Exercise", "New Exercise", "Edit Exercise"]
        for i, button_text in enumerate(list_button_texts):
            assert gef.layout().itemAt(i).widget().text() == button_text

    def test_groupbox_available_exercises(self, groupbox_available_exercises_fixture):
        gaf = groupbox_available_exercises_fixture
        assert isinstance(gaf.layout(), QGridLayout)

        list_widgets_widget_classes_available_exercises = [
            (gaf.combobox_category, ComboboxCategory),
            (gaf.combobox_muscles, ComboboxMuscles),
            (gaf.combobox_difficulty, ComboboxDifficulty),
            (gaf.table_available_exercises, QTableWidget),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes_available_exercises):
            assert isinstance(widget, widget_class)
            assert isinstance(gaf.layout().itemAt(i).widget(), widget_class)

    def test_comboboxes_exercises(self, groupbox_available_exercises_fixture):
        gaf = groupbox_available_exercises_fixture
        combobox_category_item_texts = ["All Categories", "Strength Training", "Endurance Training",
                                        "Coordination Training"]
        for i, item_text in enumerate(combobox_category_item_texts):
            assert gaf.combobox_category.itemText(i) == item_text

        combobox_muscles_item_texts = ["All muscles groups", "Chest", "Abdominal Muscles", "Neck",
                                       "Upper Back", "Upper Arms", "Shoulders", "Forearms",
                                       "Lower Back", "Gluteal Muscles", "Upper Legs", "Lower Legs"]
        for i, item_text in enumerate(combobox_muscles_item_texts):
            assert gaf.combobox_muscles.itemText(i) == item_text

        combobox_difficulty_texts = ["All Difficulties", "Very Hard", "Hard", "Medium", "Easy",
                                     "Very Easy"]
        for i, item_text in enumerate(combobox_difficulty_texts):
            assert gaf.combobox_difficulty.itemText(i) == item_text


class TestWindowNewExercise:
    def test_existence(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne, WindowNewExercise)
        assert wne.windowTitle() == "Add New Exercise"
        assert wne.isModal()
        assert bool(wne.windowFlags() & Qt.Window)
        assert bool(wne.windowFlags() & Qt.WindowStaysOnTopHint)

    def test_layout(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne.layout(), QFormLayout)
        list_widgets_widget_classes = [
            (wne.label_name, QLabel),
            (wne.line_edit_name, QLineEdit),
            (wne.label_measures, QLabel),
            (wne.spin_box_measures, QSpinBox),
            ]
        for i in range(5):
            list_widgets_widget_classes.append((wne.labels_measure_type[i], QLabel))
            list_widgets_widget_classes.append((wne.comboboxes_type[i], QComboBox))
            list_widgets_widget_classes.append((wne.labels_measure_name[i], QLabel))
            list_widgets_widget_classes.append((wne.line_edits_measure_name[i], QLineEdit))
        list_widgets_widget_classes += [
            (wne.button_discard, QPushButton),
            (wne.button_add, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes):
            assert isinstance(widget, widget_class)
            assert isinstance(wne.layout().itemAt(i).widget(), widget_class)

    def test_widgets(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert wne.label_name.text() == "Exercise Name:"
        assert wne.label_measures.text() == "Number of Measures:"
        assert wne.spin_box_measures.minimum() == 0
        assert wne.spin_box_measures.maximum() == 5
        assert wne.button_add.text() == "Add Exercise"
        assert wne.button_discard.text() == "Discard Exercise"
        for i in range(5):
            assert wne.labels_measure_type[i].text() == f"Type of Measure {i + 1}:"
            assert wne.labels_measure_name[i].text() == f"Name of Measure {i + 1}:"

    @pytest.mark.parametrize("value", [0, 1, 4, 5])
    def test_spin_box_measures(self, main_window_fixture, database_filename_fixture, value):
        main_window_fixture.new_database(database_filename_fixture)
        wne = main_window_fixture.window_new_exercise
        wne.spin_box_measures.setValue(value)
        for i in range(5):
            if value > i:
                assert wne.labels_measure_type[i].isVisible()
                assert wne.comboboxes_type[i].isVisible()
                assert wne.labels_measure_name[i].isVisible()
                assert wne.line_edits_measure_name[i].isVisible()
            else:
                assert not wne.labels_measure_type[i].isVisible()
                assert not wne.comboboxes_type[i].isVisible()
                assert not wne.labels_measure_name[i].isVisible()
                assert not wne.line_edits_measure_name[i].isVisible()

    def test_close_window(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        wne.spin_box_measures.setValue(5)
        wne.line_edit_name.setText("Some exercise")
        wne.line_edits_measure_name[3].setText("Sets")
        wne.line_edits_measure_name[4].setText("SIOMBD")
        wne.close()
        assert wne.line_edit_name.text() == ""
        assert wne.line_edits_measure_name[3].text() == ""
        assert wne.line_edits_measure_name[4].text() == ""
        for i in range(5):
            assert not wne.labels_measure_type[i].isVisible()
            assert not wne.comboboxes_type[i].isVisible()
            assert not wne.labels_measure_name[i].isVisible()
            assert not wne.line_edits_measure_name[i].isVisible()

    def test_discard_button(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        mwf.new_exercise_action()
        wne = mwf.window_new_exercise
        assert wne.isVisible()
        wne.button_discard.click()
        assert not wne.isVisible()

    def test_add_button(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.close_database()
        mwf.new_database(database_filename_fixture)
        mwf.new_exercise_action()
        wne = mwf.window_new_exercise
        assert wne.isVisible()
        wne.line_edit_name.setText("Test Name")
        wne.button_add.click()
        assert not wne.isVisible()

    def test_new_exercise_without_database(self, main_window_fixture):
        mwf = main_window_fixture
        mwf.close_database()
        assert mwf.database is None
        mwf.widget_main.widget_right.groupbox_exercise.button_new.click()
        assert not mwf.window_new_exercise.isVisible()
        assert mwf.error_message.isVisible()
        assert mwf.error_message.windowTitle() == "Cannot Create New Exercise!"
        assert mwf.error_message.layout().itemAt(1).widget().toPlainText() == \
               "No database is loaded. Please create one with 'New Database' or load one with " \
               "'Load Database'!"

    def test_add_exercise_without_name(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        wne = mwf.window_new_exercise
        mwf.widget_main.widget_right.groupbox_exercise.button_new.click()
        assert wne.isVisible()
        assert wne.line_edit_name.text() == ""
        wne.button_add.click()
        assert wne.isVisible()
        assert wne.line_edit_name.styleSheet() == "QLineEdit {background: rgb(255, 0, 0)}"
        wne.line_edit_name.setText("1")
        assert wne.line_edit_name.styleSheet() == ""

    def test_add_exercise_without_measure_name(self, main_window_fixture,
                                               database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        wne = mwf.window_new_exercise
        mwf.widget_main.widget_right.groupbox_exercise.button_new.click()
        wne.line_edit_name.setText("Test Exercise")
        assert wne.isVisible()
        wne.spin_box_measures.setValue(1)
        wne.button_add.click()
        assert wne.isVisible()
        assert wne.line_edits_measure_name[0].styleSheet() == "QLineEdit " \
                                                              "{background: rgb(255, 0, 0)}"
        wne.line_edits_measure_name[0].setText("Some name")
        assert wne.line_edits_measure_name[0].styleSheet() == ""


class TestDatabaseFileDialogs:
    def test_file_dialog_new_database(self, main_window_fixture):
        mwf = main_window_fixture
        assert isinstance(mwf.file_dialog_new_database, QFileDialog)
        assert not mwf.file_dialog_new_database.isVisible()

    def test_file_dialog_load_database(self, main_window_fixture):
        mwf = main_window_fixture
        assert isinstance(mwf.file_dialog_load_database, QFileDialog)
        assert not mwf.file_dialog_load_database.isVisible()

    def test_close_database(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        mwf.close_database()
        assert mwf.database_path is None
        assert mwf.database is None
        assert mwf.windowTitle() == "Workouts Tracking"
