from PySide6.QtWidgets import (QSplitter, QLayout, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget,
                               QLabel, QGroupBox, QPushButton,
                               )

from workouts_tracking.gui import (HLineSunken, ComboboxCategory, GroupBoxDatabase, ComboboxMuscles,
                                   )


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
            (cwf.widget_right.groupbox_workout, QGroupBox),
            (cwf.widget_right.label_available_exercises, QLabel),
            (cwf.widget_right.combobox_category, ComboboxCategory),
            (cwf.widget_right.combobox_muscles, ComboboxMuscles),
            (cwf.widget_right.table_available_exercises, QTableWidget),
            (cwf.widget_right.groupbox_exercise, QGroupBox),
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
        assert cwf.widget_right.label_available_exercises.text() == "Available Exercises"
        assert cwf.widget_right.groupbox_exercise.title() == "Exercise Actions"

        combobox_category_item_texts = ["All Categories", "Strength Training", "Endurance Training",
                                        "Coordination Training"]
        for i, item_text in enumerate(combobox_category_item_texts):
            assert cwf.widget_right.combobox_category.itemText(i) == item_text

        combobox_muscles_item_texts = ["All muscles groups", "Chest", "Abdominal Muscles", "Neck",
                                       "Upper Back", "Upper Arms", "Shoulders", "Forearms",
                                       "Lower Back", "Gluteal Muscles", "Upper Legs", "Lower Legs"]
        for i, item_text in enumerate(combobox_muscles_item_texts):
            assert cwf.widget_right.combobox_muscles.itemText(i) == item_text

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
