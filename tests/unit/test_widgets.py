from PySide6.QtWidgets import (QSplitter, QLayout, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget,
                               QLabel, QPushButton, QGridLayout, QFormLayout, QLineEdit,
                               QFileDialog, QPlainTextEdit, QCheckBox, QComboBox,
                               )
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from workouts_tracking.gui import (HLineSunken, ComboboxCategory, GroupBoxDatabase, ComboboxMuscles,
                                   GroupBoxWorkout, GroupBoxExercise, GroupBoxAvailableExercises,
                                   ComboboxDifficulty, WindowNewExercise, GroupBoxMuscleGroups,
                                   WindowAddMeasure, ComboboxMeasureTypes,
                                   )

from workouts_tracking.constants import (
    DATABASE_CATEGORY_ENTRIES,
    DATABASE_DIFFICULTY_ENTRIES,
    DATABASE_MUSCLE_GROUP_ENTRIES,
    DATABASE_MEASURE_TYPE_ENTRIES,
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
            (cwf.widget_left.frame_h_line, HLineSunken),
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


class TestWindowAddMeasure:
    def test_existence(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne.window_add_measure, WindowAddMeasure)
        assert wne.window_add_measure.windowTitle() == "Add Measure"
        assert wne.window_add_measure.isModal()
        assert bool(wne.windowFlags() & Qt.Window)
        assert bool(wne.windowFlags() & Qt.WindowStaysOnTopHint)

    def test_layout(self, main_window_fixture):
        wam = main_window_fixture.window_new_exercise.window_add_measure
        assert isinstance(wam.layout(), QFormLayout)
        list_widgets_widget_classes = [
            (wam.label_name, QLabel),
            (wam.line_edit_name, QLineEdit),
            (wam.label_type, QLabel),
            (wam.combobox_type, ComboboxMeasureTypes),
            (wam.label_per_set, QLabel),
            (wam.checkbox_per_set, QCheckBox),
            (wam.button_discard, QPushButton),
            (wam.button_add, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes):
            assert isinstance(widget, widget_class)
            assert isinstance(wam.layout().itemAt(i).widget(), widget_class)

    def test_widgets(self, main_window_fixture, tmp_path):
        main_window_fixture.new_database(tmp_path / "sample_database.db")
        wam = main_window_fixture.window_new_exercise.window_add_measure
        assert wam.label_name.text() == "Measure Name:"

        assert wam.label_type.text() == "Measure Type:"
        type_items = [wam.combobox_type.itemText(i) for i in range(wam.combobox_type.count())]
        type_names = [f"{entry[1]} ({entry[2]})" for entry in DATABASE_MEASURE_TYPE_ENTRIES]
        assert len(type_names) == len(type_items)
        for item in type_items:
            assert item in type_names

        assert wam.label_per_set.text() == "Per Set:"

        assert wam.button_discard.text() == "Discard"
        assert wam.button_add.text() == "Add"

    def test_close_window(self, main_window_fixture):
        wam = main_window_fixture.window_new_exercise.window_add_measure
        wam.line_edit_name.setText("Some Text name")
        wam.checkbox_per_set.setChecked(True)
        wam.close()
        assert wam.line_edit_name.text() == ""
        assert not wam.checkbox_per_set.isChecked()


class TestWindowNewExercise:
    def test_existence(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne, WindowNewExercise)
        assert wne.windowTitle() == "Add New Exercise"
        assert wne.isModal()
        assert bool(wne.windowFlags() & Qt.Window)
        assert bool(wne.windowFlags() & Qt.WindowStaysOnTopHint)

    def test_outer_layout(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne.layout(), QVBoxLayout)
        list_widgets_widget_classes = [
            (wne.new_exercise_form, QWidget),
            (wne.group_box_muscle_groups, GroupBoxMuscleGroups),
            (wne.measure_buttons, QWidget),
            (wne.table_measures, QTableWidget),
            (wne.finish_buttons, QWidget),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes):
            assert isinstance(widget, widget_class)
            assert isinstance(wne.layout().itemAt(i).widget(), widget_class)

    def test_inner_layout1(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne.new_exercise_form.layout(), QFormLayout)
        list_widgets_widget_classes = [
            (wne.label_name, QLabel),
            (wne.line_edit_name, QLineEdit),
            (wne.label_comment, QLabel),
            (wne.text_edit_comment, QPlainTextEdit),
            (wne.label_url, QLabel),
            (wne.line_edit_url, QLineEdit),
            (wne.label_category, QLabel),
            (wne.combobox_category, ComboboxCategory),
            (wne.label_difficulty, QLabel),
            (wne.combobox_difficulty, ComboboxDifficulty),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes):
            assert isinstance(widget, widget_class)
            assert isinstance(wne.new_exercise_form.layout().itemAt(i).widget(), widget_class)

    def test_inner_layout2(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        assert isinstance(wne.finish_buttons.layout(), QHBoxLayout)
        list_widgets_widget_classes = [
            (wne.button_discard, QPushButton),
            (wne.button_add_exercise, QPushButton),
        ]
        for i, (widget, widget_class) in enumerate(list_widgets_widget_classes):
            assert isinstance(widget, widget_class)
            assert isinstance(wne.finish_buttons.layout().itemAt(i).widget(), widget_class)

    def test_widgets(self, main_window_fixture, tmp_path):
        main_window_fixture.new_database(tmp_path / "sample_database.db")
        wne = main_window_fixture.window_new_exercise
        assert wne.label_name.text() == "Exercise Name:"
        assert wne.label_comment.text() == "Comment:"
        assert wne.label_url.text() == "Url:"

        assert wne.label_category.text() == "Category:"
        category_items = [wne.combobox_category.itemText(i)
                          for i in range(wne.combobox_category.count())]
        category_names = [entry[1] for entry in DATABASE_CATEGORY_ENTRIES]
        assert len(category_names) == len(category_items)
        for item in category_items:
            assert item in category_names

        assert wne.label_difficulty.text() == "Difficulty:"
        difficulty_items = [wne.combobox_difficulty.itemText(i)
                            for i in range(wne.combobox_difficulty.count())]
        difficulty_names = [entry[1] for entry in DATABASE_DIFFICULTY_ENTRIES]
        assert len(difficulty_names) == len(difficulty_items)
        for item in difficulty_items:
            assert item in difficulty_names

        assert wne.group_box_muscle_groups.title() == "Muscle Groups:"
        assert isinstance(wne.group_box_muscle_groups.layout(), QGridLayout)
        for i, entry in enumerate(DATABASE_MUSCLE_GROUP_ENTRIES):
            assert isinstance(wne.group_box_muscle_groups.layout().itemAt(i).widget(), QCheckBox)
            assert wne.group_box_muscle_groups.layout().itemAt(i).widget().text() == entry[1]

        assert wne.button_add_measure.text() == "Add Measure"
        assert wne.button_delete_measure.text() == "Delete Measure"

        header_names = ["measure name", "measure type", "per set"]
        for i, header_name in enumerate(header_names):
            assert wne.table_measures.horizontalHeaderItem(i).text() == header_name

        assert wne.button_discard.text() == "Discard"
        assert wne.button_add_exercise.text() == "Add Exercise"

    def test_close_window(self, main_window_fixture):
        wne = main_window_fixture.window_new_exercise
        wne.line_edit_name.setText("Some exercise")
        wne.line_edit_url.setText("Some_url.de")
        wne.text_edit_comment.setPlainText("Some plain text")
        wne.group_box_muscle_groups.checkboxes[0].setChecked(True)
        wne.close()
        assert wne.line_edit_name.text() == ""
        assert wne.line_edit_url.text() == ""
        assert wne.text_edit_comment.toPlainText() == ""
        for checkbox in wne.group_box_muscle_groups.checkboxes:
            assert not checkbox.isChecked()

    def test_discard_button(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        mwf.new_exercise_action()
        wne = mwf.window_new_exercise
        assert wne.isVisible()
        wne.button_discard.click()
        assert not wne.isVisible()

    def test_add_exercise_button(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        mwf.new_exercise_action()
        wne = mwf.window_new_exercise
        assert wne.isVisible()
        wne.line_edit_name.setText("Test Name")
        wne.button_add_exercise.click()
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
        wne.button_add_exercise.click()
        assert wne.isVisible()
        assert wne.line_edit_name.styleSheet() == "QLineEdit {background: rgb(255, 0, 0)}"
        wne.line_edit_name.setText("1")
        assert wne.line_edit_name.styleSheet() == ""

    def test_add_measure_action(self, main_window_fixture, database_filename_fixture):
        mwf = main_window_fixture
        mwf.new_database(database_filename_fixture)
        wne = mwf.window_new_exercise
        mwf.widget_main.widget_right.groupbox_exercise.button_new.click()
        wne.button_add_measure.click()
        assert wne.window_add_measure.isVisible()


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
