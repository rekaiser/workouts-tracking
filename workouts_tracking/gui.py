import os

from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget,
                               QVBoxLayout, QTableWidget, QLabel, QFrame, QGroupBox, QComboBox,
                               QPushButton, QGridLayout, QFormLayout, QLineEdit,
                               QFileDialog, QErrorMessage, QPlainTextEdit, QCheckBox,
                               QTableWidgetItem,
                               )
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon

from .constants import APPLICATION_NAME, INSTALL_DIR
from .database import Database


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

        self.database_path = None
        self.database = None

        self.installation_path = INSTALL_DIR
        self.widget_main = MainWidget(self)
        self.setCentralWidget(self.widget_main)
        self.logo = QIcon(str(self.installation_path / "graphics" / "WT-Logo.svg"))
        self.setWindowIcon(self.logo)
        self.setWindowTitle(APPLICATION_NAME)

        self.window_new_exercise = WindowNewExercise(self)

        self.file_dialog_new_database = QFileDialog(self)

        self.file_dialog_load_database = QFileDialog(self)

        self.error_message = QErrorMessage(self)
        self.widgets_to_update = [
            self.window_new_exercise.combobox_category,
            self.window_new_exercise.combobox_difficulty,
            self.window_new_exercise.group_box_muscle_groups,
        ]

    def new_exercise_action(self):
        if self.database is None:
            self.error_message.setWindowTitle("Cannot Create New Exercise!")
            self.error_message.showMessage("No database is loaded. Please create one with 'New "
                                           "Database' or load one with 'Load Database'!")
        else:
            self.window_new_exercise.show()

    def new_database(self, database_path):
        self.database_path = database_path
        if os.path.isfile(self.database_path):
            open(self.database_path, "w").close()
        self.database = Database(self.database_path)
        self.setWindowTitle(APPLICATION_NAME + " - " + str(os.path.basename(self.database_path)))
        self.update_widgets()

    def load_database(self, database_path):
        self.database_path = database_path
        self.database = Database(self.database_path)
        self.setWindowTitle(APPLICATION_NAME + " - " + str(os.path.basename(self.database_path)))
        self.update_widgets()

    def close_database(self):
        self.database_path = None
        self.database = None
        self.setWindowTitle(APPLICATION_NAME)
        self.update_widgets()

    def new_database_action(self):
        database_path = self.file_dialog_new_database.getSaveFileName(self)[0]
        if database_path == "":
            return
        self.new_database(database_path)

    def load_database_action(self):
        database_path = self.file_dialog_load_database.getOpenFileName(self)[0]
        if database_path == "":
            return
        self.load_database(database_path)

    def close_database_action(self):
        self.close_database()

    def update_widgets(self):
        for widget in self.widgets_to_update:
            widget.update()


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
        self.frame_h_line = HLineSunken(self)
        self.layout().addWidget(self.frame_h_line)
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
        self.button_new.clicked.connect(self.super_parent().new_database_action)
        self.layout().addWidget(self.button_new)
        self.button_load = QPushButton("Load Database", self)
        self.button_load.clicked.connect(self.super_parent().load_database_action)
        self.layout().addWidget(self.button_load)
        self.button_close = QPushButton("Close Database", self)
        self.button_close.clicked.connect(self.super_parent().close_database_action)
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
        self.button_new.clicked.connect(self.super_parent().new_exercise_action)
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
        database = self.super_parent().database
        if database:
            categories = database.get_categories()
            self.addItems(categories)

    def update(self) -> None:
        super().update()
        database = self.super_parent().database
        self.clear()
        if database:
            categories = database.get_categories()
            self.addItems(categories)


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
        database = self.super_parent().database
        if database:
            categories = database.get_categories()
            self.addItems(categories)

    def update(self) -> None:
        super().update()
        database = self.super_parent().database
        self.clear()
        if database:
            difficulties = database.get_difficulties()
            self.addItems(difficulties)


class WindowNewExercise(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Add New Exercise")
        self.setWindowModality(Qt.WindowModal)
        self.setLayout(QVBoxLayout(self))

        self.new_exercise_form = NewExerciseForm(self)
        self.layout().addWidget(self.new_exercise_form)
        self.new_exercise_form.setLayout(QFormLayout(self.new_exercise_form))
        self.label_name = QLabel("Exercise Name:", self.new_exercise_form)
        self.line_edit_name = QLineEdit(self.new_exercise_form)
        self.line_edit_name.textChanged.connect(self.remove_style_sheet_line_edit_name)
        self.new_exercise_form.layout().addRow(self.label_name, self.line_edit_name)
        self.label_comment = QLabel("Comment:", self.new_exercise_form)
        self.text_edit_comment = QPlainTextEdit(self.new_exercise_form)
        self.new_exercise_form.layout().addRow(self.label_comment, self.text_edit_comment)
        self.label_url = QLabel("Url:", self.new_exercise_form)
        self.line_edit_url = QLineEdit(self.new_exercise_form)
        self.new_exercise_form.layout().addRow(self.label_url, self.line_edit_url)
        self.label_category = QLabel("Category:", self.new_exercise_form)
        self.combobox_category = ComboboxCategory(self.new_exercise_form)
        self.new_exercise_form.layout().addRow(self.label_category, self.combobox_category)
        self.label_difficulty = QLabel("Difficulty:", self.new_exercise_form)
        self.combobox_difficulty = ComboboxDifficulty(self.new_exercise_form)
        self.new_exercise_form.layout().addRow(self.label_difficulty, self.combobox_difficulty)

        self.group_box_muscle_groups = GroupBoxMuscleGroups("Muscle Groups:", self)
        self.layout().addWidget(self.group_box_muscle_groups)

        self.button_add_measure = QPushButton("Add Measure", self)
        self.layout().addWidget(self.button_add_measure)

        self.table_measures = QTableWidget(0, 3, self)
        self.layout().addWidget(self.table_measures)
        header_items = [QTableWidgetItem("measure name"), QTableWidgetItem("measure type"),
                        QTableWidgetItem("per set")]
        for i, header_item in enumerate(header_items):
            self.table_measures.setHorizontalHeaderItem(i, header_item)

        self.finish_buttons = QWidget(self)
        self.layout().addWidget(self.finish_buttons)
        self.finish_buttons.setLayout(QHBoxLayout(self.finish_buttons))
        self.button_discard = QPushButton("Discard", self.finish_buttons)
        self.finish_buttons.layout().addWidget(self.button_discard)
        self.button_discard.clicked.connect(self.button_discard_action)
        self.button_add_exercise = QPushButton("Add Exercise", self.finish_buttons)
        self.finish_buttons.layout().addWidget(self.button_add_exercise)
        self.button_add_exercise.clicked.connect(self.button_add_exercise_action)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.line_edit_name.setText("")
        self.text_edit_comment.setPlainText("")
        self.line_edit_url.setText("")
        self.group_box_muscle_groups.uncheck_checkboxes()
        return super().closeEvent(event)

    def button_discard_action(self):
        self.close()

    def button_add_exercise_action(self):
        valid_text = True
        if self.line_edit_name.text() == "":
            self.line_edit_name.setStyleSheet("QLineEdit {background: rgb(255, 0, 0)}")
            valid_text = False
        if valid_text:
            self.close()

    def remove_style_sheet_line_edit_name(self):
        self.line_edit_name.setStyleSheet("")


class NewExerciseForm(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)


class ComboboxMeasureTypes(QComboBox, BasicWidget):
    def __init__(self, parent, related_line_edit):
        super().__init__(parent)
        self.related_line_edit = related_line_edit
        measure_types = [
            "number (integer)", "number (float)", "sets", "repetitions", "repetitions per set",
            "time", "time per set", "weight", "weight per set", "distance (m)",
            "distance per set (m)", "text"
        ]
        self.addItems(measure_types)

        self.currentIndexChanged.connect(self.set_default_measure_name)

    def set_default_measure_name(self, index):
        default_measure_names = [
            "", "", "Sets", "Repetitions", "Repetitions per Set", "Time", "Time per Set", "Weight",
            "Weight per Set", "Distance", "Distance per Set", ""
        ]
        self.related_line_edit.setText(default_measure_names[index])


class GroupBoxMuscleGroups(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QGridLayout(self))
        self.number_columns = 3
        database = self.super_parent().database
        self.checkboxes = []
        if database:
            muscle_groups = database.get_muscle_groups()
            for i, muscle_group in enumerate(muscle_groups):
                checkbox = QCheckBox(muscle_group, self)
                self.checkboxes.append(checkbox)
                self.layout().addWidget(checkbox, i // 3, i % 3)

    def update(self) -> None:
        super().update()
        database = self.super_parent().database
        self.checkboxes = []
        if database:
            muscle_groups = database.get_muscle_groups()
            for i, muscle_group in enumerate(muscle_groups):
                checkbox = QCheckBox(muscle_group, self)
                self.checkboxes.append(checkbox)
                self.layout().addWidget(checkbox, i // 3, i % 3)

    def uncheck_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
