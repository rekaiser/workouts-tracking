from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget,
                               QVBoxLayout, QTableWidget, QLabel, QFrame, QGroupBox, QComboBox,
                               QPushButton,
                               )
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_main = MainWidget(self)
        self.setCentralWidget(self.widget_main)


class MainWidget(QSplitter):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.widget_left = LeftWidget(self)
        self.widget_right = RightWidget(self)
        self.layout().addWidget(self.widget_left)
        self.layout().addWidget(self.widget_right)


class LeftWidget(QWidget):
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


class RightWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))
        self.groupbox_database = GroupBoxDatabase("Database Actions", self)
        self.layout().addWidget(self.groupbox_database)
        self.groupbox_workout = GroupBoxWorkout("Workout Actions", self)
        self.layout().addWidget(self.groupbox_workout)
        self.label_available_exercises = QLabel("Available Exercises", self)
        self.layout().addWidget(self.label_available_exercises)
        self.combobox_category = ComboboxCategory(self)
        self.layout().addWidget(self.combobox_category)
        self.combobox_muscles = ComboboxMuscles(self)
        self.layout().addWidget(self.combobox_muscles)
        self.table_available_exercises = QTableWidget(self)
        self.layout().addWidget(self.table_available_exercises)
        self.groupbox_exercise = GroupBoxExercise("Exercise Actions", self)
        self.layout().addWidget(self.groupbox_exercise)


class HLineSunken(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameStyle(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(1)


class ComboboxCategory(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        workout_categories = ["All Categories", "Strength Training", "Endurance Training",
                              "Coordination Training"]
        self.addItems(workout_categories)


class GroupBoxDatabase(QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QHBoxLayout(self))
        self.button_new = QPushButton("New Database", self)
        self.layout().addWidget(self.button_new)
        self.button_load = QPushButton("Load Database", self)
        self.layout().addWidget(self.button_load)
        self.button_close = QPushButton("Close Database", self)
        self.layout().addWidget(self.button_close)


class GroupBoxWorkout(QGroupBox):
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


class ComboboxMuscles(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        muscle_groups = ["All muscles groups", "Chest", "Abdominal Muscles", "Neck", "Upper Back",
                         "Upper Arms", "Shoulders", "Forearms", "Lower Back", "Gluteal Muscles",
                         "Upper Legs", "Lower Legs"]
        self.addItems(muscle_groups)


class GroupBoxExercise(QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QHBoxLayout(self))
        self.button_perform = QPushButton("Perform Exercise", self)
        self.layout().addWidget(self.button_perform)
        self.button_new = QPushButton("New Exercise", self)
        self.layout().addWidget(self.button_new)
        self.button_edit = QPushButton("Edit Exercise", self)
        self.layout().addWidget(self.button_edit)
