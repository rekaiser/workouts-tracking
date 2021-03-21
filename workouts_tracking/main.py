import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout, QLabel,
                               QGroupBox, QGridLayout, QComboBox, QTableWidget, QLineEdit, QPushButton,
                               QTableWidgetItem)

from .gui import run_app, create_app


class Exercise:
    def __init__(self, name):
        self.name = name

    def exercise(self, sets):
        pass


class RepetitionExercise(Exercise):
    def __init__(self, name, number_sets):
        super().__init__(name)
        self.number_sets = number_sets

    def exercise(self, sets, repetitions: list):
        pass


class TimedExercise(Exercise):
    def __init__(self, name):
        super().__init__(name)


class DistanceExercise(Exercise):
    def __init__(self, name):
        super().__init__(name)


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workouts Tracking")
        self.showMaximized()
        self.__main = QSplitter(Qt.Horizontal, self)
        self.setCentralWidget(self.__main)
        self.layout = QHBoxLayout(self.__main)
        self.left_widget = QWidget(self)
        self.right_widget = QWidget(self)
        self.layout.addWidget(self.left_widget)
        self.layout.addWidget(self.right_widget)
        self.left_layout = QVBoxLayout(self.left_widget)
        self.right_layout = QVBoxLayout(self.right_widget)

        self.perform_exercise_box = QGroupBox("Perform Exercise")
        self.left_layout.addWidget(self.perform_exercise_box)
        self.perform_exercise_layout = QGridLayout(self.perform_exercise_box)
        self.perform_exercise_layout.addWidget(QLabel("Choose Exercise:"), 0, 0)
        self.exercise_combobox = QComboBox(self.perform_exercise_box)
        self.perform_exercise_layout.addWidget(self.exercise_combobox, 1, 0)
        self.exercise_combobox.addItem("Running")
        self.exercise_combobox.addItem("Cycling")
        self.exercise_combobox.addItem("Pushups")
        self.exercise_combobox.addItem("Bizeps Curl")
        self.exercise_combobox.addItem("Arnold Press")
        self.exercise_combobox.addItem("Pullup")
        self.exercise_combobox.addItem("Squat")
        self.perform_exercise_layout.addWidget(QLabel("Sets:"), 0, 1)
        self.number_sets_combobox = QComboBox(self.perform_exercise_box)
        self.perform_exercise_layout.addWidget(self.number_sets_combobox, 1, 1)
        self.number_sets_combobox.currentIndexChanged.connect(self.update_edits)
        self.reps_edits = []
        self.time_edits = []
        self.distance_edits = []
        self.weight_edits = []
        for i in range(1, 9):
            self.number_sets_combobox.addItem(str(i))
        self.make_edits_per_set(1)
        self.perform_exercise_layout.addWidget(QLabel("Repetitions:"), 0, 2)
        self.perform_exercise_layout.addWidget(QLabel("Time (hh:mm:ss):"), 0, 3)
        self.perform_exercise_layout.addWidget(QLabel("Distance (km):"), 0, 4)
        self.perform_exercise_layout.addWidget(QLabel("Weight (kg)"), 0, 5)

        self.perform_exercise_button = QPushButton("Perform Exercise", self.perform_exercise_box)
        self.perform_exercise_button.clicked.connect(self.perform_exercise)
        self.perform_exercise_layout.addWidget(self.perform_exercise_button, 0, 6)

        self.exercises_table = QTableWidget(0, 6, self.left_widget)
        self.left_layout.addWidget(self.exercises_table)
        self.header_names = ["Exercise", "Sets", "Repetitions", "Time", "Distance", "Weight"]
        for i, name in enumerate(self.header_names):
            item = QTableWidgetItem(name)
            self.exercises_table.setHorizontalHeaderItem(i, item)

    def perform_exercise(self):
        exercise_name = self.exercise_combobox.currentText()
        sets = self.number_sets_combobox.currentText()
        reps = []
        times = []
        distances = []
        weights = []
        for edit1, edit2, edit3, edit4 in zip(self.reps_edits, self.time_edits, self.distance_edits, self.weight_edits):
            reps.append(edit1.text())
            times.append(edit2.text())
            distances.append(edit3.text())
            weights.append(edit4.text())
        reps_string = str(reps)
        print(reps_string)
        times = str(times)
        distances = str(distances)
        weights = str(weights)
        cells = [exercise_name, sets, reps_string, times, distances, weights]
        self.exercises_table.insertRow(self.exercises_table.rowCount())
        for i, cell in enumerate(cells):
            item = QTableWidgetItem(cell)
            self.exercises_table.setItem(self.exercises_table.rowCount() - 1, i, item)

    def update_edits(self):
        for edit1, edit2, edit3, edit4 in zip(self.reps_edits, self.time_edits, self.distance_edits, self.weight_edits):
            edit1.hide()
            edit2.hide()
            edit3.hide()
            edit4.hide()
            self.perform_exercise_layout.removeWidget(edit1)
            self.perform_exercise_layout.removeWidget(edit2)
            self.perform_exercise_layout.removeWidget(edit3)
            self.perform_exercise_layout.removeWidget(edit4)

        self.make_edits_per_set(self.number_sets_combobox.currentIndex() + 1)

    def make_edits_per_set(self, sets: int):
        self.reps_edits = []
        self.time_edits = []
        self.distance_edits = []
        self.weight_edits = []

        for set_number in range(sets):
            number_repetitions_edit = QLineEdit(self.perform_exercise_box)
            self.reps_edits.append(number_repetitions_edit)
            number_repetitions_edit.setFixedWidth(60)
            self.perform_exercise_layout.addWidget(number_repetitions_edit, set_number + 1, 2)
            time_edit = QLineEdit(self.perform_exercise_box)
            self.time_edits.append(time_edit)
            time_edit.setFixedWidth(80)
            self.perform_exercise_layout.addWidget(time_edit, set_number + 1, 3)
            distance_edit = QLineEdit(self.perform_exercise_box)
            distance_edit.setFixedWidth(80)
            self.distance_edits.append(distance_edit)
            self.perform_exercise_layout.addWidget(distance_edit, set_number + 1, 4)
            weight_edit = QLineEdit(self.perform_exercise_box)
            weight_edit.setFixedWidth(60)
            self.weight_edits.append(weight_edit)
            self.perform_exercise_layout.addWidget(weight_edit, set_number + 1, 5)


def main():
    q_app = create_app(sys.argv)
    exit_code = run_app(q_app)
    if exit_code != 0:
        print(f"Program exited with failure: Exit Code {exit_code}")


if __name__ == '__main__':
    main()
