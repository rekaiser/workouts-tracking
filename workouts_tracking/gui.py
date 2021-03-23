from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget,
                               QVBoxLayout, QTableWidget, QLabel, QFrame, QGroupBox,
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
        self.group_box_database = QGroupBox("Some name of the 1. group box", self)
        self.layout().addWidget(self.group_box_database)
        self.group_box_workout = QGroupBox("Some name of 2. group box", self)
        self.layout().addWidget(self.group_box_workout)
        self.label_available_exercises = QLabel("Label for Table below", self)
        self.layout().addWidget(self.label_available_exercises)
        self.table_available_exercises = QTableWidget(self)
        self.layout().addWidget(self.table_available_exercises)
        self.group_box_exercise = QGroupBox("Some name for this box", self)
        self.layout().addWidget(self.group_box_exercise)


class HLineSunken(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameStyle(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(1)
