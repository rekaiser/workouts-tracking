from PySide6.QtWidgets import (QSplitter, QLayout, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget,
                               QLabel, QGroupBox, QComboBox,
                               )

from workouts_tracking.gui import HLineSunken


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
            (cwf.widget_right.group_box_database, QGroupBox),
            (cwf.widget_right.group_box_workout, QGroupBox),
            (cwf.widget_right.label_available_exercises, QLabel),
            (cwf.widget_right.combobox_category, QComboBox),
            (cwf.widget_right.table_available_exercises, QTableWidget),
            (cwf.widget_right.group_box_exercise, QGroupBox),
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
        assert cwf.widget_right.group_box_database.title() == "Database Actions"
        assert cwf.widget_right.group_box_workout.title() == "Workout Actions"
        assert cwf.widget_right.label_available_exercises.text() == "Available Exercises"
        assert cwf.widget_right.group_box_exercise.title() == "Exercise Actions"

        combobox_item_texts = ["Strength Training", "Endurance Training", "Coordination Training"]
        for i, item_text in enumerate(combobox_item_texts):
            assert cwf.widget_right.combobox_category.itemText(i) == item_text
