from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget,
                               QVBoxLayout, QTableWidget, QLabel, QFrame, QGroupBox, QComboBox,
                               QPushButton, QGridLayout, QFormLayout, QLineEdit, QSpinBox,
                               )
from PySide6.QtCore import Qt

from .constants import APPLICATION_NAME


def create_app(sys_argv):
    q_app = QApplication(sys_argv)
    q_app.setApplicationName(APPLICATION_NAME)
    return q_app


def run_app(q_app: QApplication):
    return q_app.exec_()


def create_and_show_main_window():
    main_window = MainWindow()
    main_window.show()
    main_window.showMaximized()
    return main_window


class BasicWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def super_parent(self):
        try:
            return self.parent().super_parent()
        except AttributeError:
            return self.parent()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_main = MainWidget(self)
        self.setCentralWidget(self.widget_main)

        self.window_new_exercise = WindowNewExercise(self)

    def show_window_new_exercise(self):
        self.window_new_exercise.show()


class MainWidget(QSplitter, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.widget_left = LeftWidget(self)
        self.widget_right = RightWidget(self)
        self.layout().addWidget(self.widget_left)
        self.layout().addWidget(self.widget_right)


class LeftWidget(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))
        self.label_workouts = QLabel("Workouts", self)
        self.layout().addWidget(self.label_workouts)
        self.table_workouts = QTableWidget(self)
        self.layout().addWidget(self.table_workouts)
        self.frame_hline = HLineSunken(self)
        self.layout().addWidget(self.frame_hline)
        self.label_performed_exercises = QLabel("Performed Exercises: Double click a line in the "
                                                "workouts table!", self)
        self.layout().addWidget(self.label_performed_exercises)
        self.table_performed_exercises = QTableWidget(self)
        self.layout().addWidget(self.table_performed_exercises)


class RightWidget(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))
        self.groupbox_database = GroupBoxDatabase("Database Actions", self)
        self.layout().addWidget(self.groupbox_database)
        self.groupbox_workout = GroupBoxWorkout("Workout Actions", self)
        self.layout().addWidget(self.groupbox_workout)
        self.groupbox_available_exercises = GroupBoxAvailableExercises("Available Exercises", self)
        self.layout().addWidget(self.groupbox_available_exercises)
        self.groupbox_exercise = GroupBoxExercise("Exercise Actions", self)
        self.layout().addWidget(self.groupbox_exercise)


class HLineSunken(QFrame, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameStyle(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(1)


class GroupBoxDatabase(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QHBoxLayout(self))
        self.button_new = QPushButton("New Database", self)
        self.layout().addWidget(self.button_new)
        self.button_load = QPushButton("Load Database", self)
        self.layout().addWidget(self.button_load)
        self.button_close = QPushButton("Close Database", self)
        self.layout().addWidget(self.button_close)


class GroupBoxWorkout(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QHBoxLayout(self))
        self.button_start = QPushButton("Start Workout", self)
        self.button_start.clicked.connect(self.switch_button_ability)
        self.layout().addWidget(self.button_start)
        self.button_finish = QPushButton("Finish Workout", self)
        self.button_finish.setDisabled(True)
        self.button_finish.clicked.connect(self.switch_button_ability)
        self.layout().addWidget(self.button_finish)

    def switch_button_ability(self):
        if self.button_start.isEnabled() and not self.button_finish.isEnabled():
            self.button_start.setDisabled(True)
            self.button_finish.setEnabled(True)
        elif not self.button_start.isEnabled() and self.button_finish.isEnabled():
            self.button_start.setEnabled(True)
            self.button_finish.setDisabled(True)


class GroupBoxExercise(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QHBoxLayout(self))
        self.button_perform = QPushButton("Perform Exercise", self)
        self.layout().addWidget(self.button_perform)
        self.button_new = QPushButton("New Exercise", self)
        self.button_new.clicked.connect(self.super_parent().show_window_new_exercise)
        self.layout().addWidget(self.button_new)
        self.button_edit = QPushButton("Edit Exercise", self)
        self.layout().addWidget(self.button_edit)


class GroupBoxAvailableExercises(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)
        self.combobox_category = ComboboxCategory(self)
        self.__layout.addWidget(self.combobox_category, 0, 0)
        self.combobox_muscles = ComboboxMuscles(self)
        self.__layout.addWidget(self.combobox_muscles, 0, 1)
        self.combobox_difficulty = ComboboxDifficulty(self)
        self.__layout.addWidget(self.combobox_difficulty, 0, 2)
        self.table_available_exercises = QTableWidget(self)
        self.__layout.addWidget(self.table_available_exercises, 1, 0, 1, 3)

    def layout(self):
        return self.__layout


class ComboboxCategory(QComboBox, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        workout_categories = ["All Categories", "Strength Training", "Endurance Training",
                              "Coordination Training"]
        self.addItems(workout_categories)


class ComboboxMuscles(QComboBox, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        muscle_groups = ["All muscles groups", "Chest", "Abdominal Muscles", "Neck", "Upper Back",
                         "Upper Arms", "Shoulders", "Forearms", "Lower Back", "Gluteal Muscles",
                         "Upper Legs", "Lower Legs"]
        self.addItems(muscle_groups)


class ComboboxDifficulty(QComboBox, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        difficulties = ["All Difficulties", "Very Hard", "Hard", "Medium", "Easy", "Very Easy"]
        self.addItems(difficulties)


class WindowNewExercise(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Add New Exercise")
        self.setWindowModality(Qt.WindowModal)
        self.setLayout(QFormLayout())

        self.label_name = QLabel("Exercise Name:", self)
        self.line_edit_name = QLineEdit(self)
        self.layout().addRow(self.label_name, self.line_edit_name)
        self.label_measures = QLabel("Number of Measures:", self)
        self.spin_box_measures = QSpinBox(self)
        self.min, self.max = 0, 5
        self.spin_box_measures.setRange(self.min, self.max)
        self.spin_box_measures.valueChanged.connect(self.change_visibility_measure_widgets)
        self.layout().addRow(self.label_measures, self.spin_box_measures)

        self.labels_measure_type = []
        self.comboboxes_type = []
        self.labels_measure_name = []
        self.line_edits_measure_name = []
        for i in range(self.min, self.max):
            label_measure_type = QLabel(f"Type of Measure {i + 1}:", self)
            self.labels_measure_type.append(label_measure_type)
            combobox_type = QComboBox(self)
            self.comboboxes_type.append(combobox_type)
            self.layout().addRow(label_measure_type, combobox_type)
            combobox_type.hide()
            label_measure_type.hide()

            label_measure_name = QLabel(f"Name of Measure {i + 1}:", self)
            self.labels_measure_name.append(label_measure_name)
            line_edit_measure_name = QLineEdit(self)
            self.line_edits_measure_name.append(line_edit_measure_name)
            self.layout().addRow(label_measure_name, line_edit_measure_name)
            label_measure_name.hide()
            line_edit_measure_name.hide()

        self.button_discard = QPushButton("Discard Exercise", self)
        self.button_add = QPushButton("Add Exercise", self)
        self.layout().addRow(self.button_discard, self.button_add)

    def change_visibility_measure_widgets(self):
        number_measures = self.spin_box_measures.value()
        for i in range(self.min, self.max):
            if number_measures > i:
                self.labels_measure_type[i].show()
                self.comboboxes_type[i].show()
                self.labels_measure_name[i].show()
                self.line_edits_measure_name[i].show()
            else:
                self.labels_measure_type[i].hide()
                self.comboboxes_type[i].hide()
                self.labels_measure_name[i].hide()
                self.line_edits_measure_name[i].hide()
