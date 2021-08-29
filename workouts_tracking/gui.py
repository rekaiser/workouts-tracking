import os

from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget,
                               QVBoxLayout, QTableWidget, QLabel, QFrame, QGroupBox, QComboBox,
                               QPushButton, QGridLayout, QFormLayout, QLineEdit,
                               QFileDialog, QErrorMessage, QPlainTextEdit, QCheckBox,
                               QTableWidgetItem, QRadioButton,
                               )
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon

from .constants import APPLICATION_NAME, INSTALL_DIR
from .database import Database
from .exercise import Exercise
from .measure import Measure


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
            self.window_new_exercise.window_add_measure.combobox_type,
        ]
        self.update_table_exercises()

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
        self.update_table_exercises()

    def load_database(self, database_path):
        self.database_path = database_path
        self.database = Database(self.database_path)
        self.setWindowTitle(APPLICATION_NAME + " - " + str(os.path.basename(self.database_path)))
        self.update_widgets()
        self.update_table_exercises()

    def close_database(self):
        self.database_path = None
        self.database = None
        self.setWindowTitle(APPLICATION_NAME)
        self.update_widgets()
        self.update_table_exercises()

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

    def update_table_exercises(self):
        table_exercises = self.widget_main.widget_right.groupbox_exercises.table_exercises
        if self.database is None:
            table_exercises.setRowCount(0)
        else:
            exercise_rows = self.database.get_exercise_table_rows()
            table_exercises.setRowCount(len(exercise_rows))
            for i, row in enumerate(exercise_rows):
                for j, item in enumerate(row):
                    table_item = QTableWidgetItem(item)
                    table_item.setFlags(table_item.flags() ^ Qt.ItemIsEditable)
                    table_exercises.setItem(i, j, table_item)


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
        self.groupbox_exercises = GroupBoxExercises("Available Exercises", self)
        self.layout().addWidget(self.groupbox_exercises)
        self.groupbox_exercise = GroupBoxExercise("Exercise Actions", self)
        self.layout().addWidget(self.groupbox_exercise)

        self.buttons_disabled_during_workout = [
            self.groupbox_database.button_new,
            self.groupbox_database.button_load,
            self.groupbox_database.button_close,
            self.groupbox_exercise.button_new,
            self.groupbox_exercise.button_edit,
        ]
        self.buttons_enabled_during_workout = [
            self.groupbox_exercise.button_perform,
        ]

    def switch_button_ability(self, during_workout=True):
        for button in self.buttons_disabled_during_workout:
            button.setEnabled(not during_workout)
        for button in self.buttons_enabled_during_workout:
            button.setEnabled(during_workout)


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
        self.button_start.clicked.connect(self.start_workout_action)
        self.layout().addWidget(self.button_start)
        self.button_finish = QPushButton("Finish Workout", self)
        self.button_finish.setDisabled(True)
        self.button_finish.clicked.connect(self.finish_workout_action)
        self.layout().addWidget(self.button_finish)

    def start_workout_action(self):
        if self.super_parent().database is None:
            self.super_parent().error_message.setWindowTitle("Cannot Start Workout!")
            self.super_parent().error_message.showMessage("No database is loaded. "
                                                          "Please create one with 'New "
                                                          "Database' or load one with "
                                                          "'Load Database'!")
            return
        self.switch_button_ability()
        self.parent().switch_button_ability(during_workout=True)

    def finish_workout_action(self):
        self.switch_button_ability()
        self.parent().switch_button_ability(during_workout=False)

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
        self.button_perform.setEnabled(False)
        self.button_new = QPushButton("New Exercise", self)
        self.button_new.clicked.connect(self.super_parent().new_exercise_action)
        self.layout().addWidget(self.button_new)
        self.button_edit = QPushButton("Edit Exercise", self)
        self.layout().addWidget(self.button_edit)


class GroupBoxExercises(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)
        self.table_exercises = QTableWidget(self)
        self.table_exercises.setColumnCount(5)
        self.header_names = ["Exercise Name", "Comment", "Url", "Category", "Difficulty"]
        for i, header_name in enumerate(self.header_names):
            self.table_exercises.setHorizontalHeaderItem(i, QTableWidgetItem(header_name))
        self.__layout.addWidget(self.table_exercises, 1, 0, 1, 3)

    def layout(self):
        return self.__layout


class ComboboxCategory(QComboBox, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.index_id_dict = {}
        self.add_items_from_database()

    def update(self) -> None:
        super().update()
        self.clear()
        self.index_id_dict = {}
        self.add_items_from_database()

    def add_items_from_database(self):
        database = self.super_parent().database
        if database:
            categories = database.get_categories()
            for index, (category_id, category) in enumerate(categories):
                self.addItem(category)
                self.index_id_dict[index] = category_id

    def get_id(self):
        return self.index_id_dict[self.currentIndex()]


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
        self.index_id_dict = {}
        self.add_items_from_database()

    def update(self) -> None:
        super().update()
        self.clear()
        self.index_id_dict = {}
        self.add_items_from_database()

    def add_items_from_database(self):
        database = self.super_parent().database
        if database:
            difficulties = database.get_difficulties()
            for index, (difficulty_id, difficulty) in enumerate(difficulties):
                self.addItem(difficulty)
                self.index_id_dict[index] = difficulty_id

    def get_id(self):
        return self.index_id_dict[self.currentIndex()]


class ComboboxMeasureTypes(QComboBox, BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.index_id_dict = {}
        self.add_items_from_database()

    def update(self) -> None:
        super().update()
        self.clear()
        self.add_items_from_database()

    def add_items_from_database(self):
        database = self.super_parent().database
        if database:
            measure_types = database.get_measure_types(without_sets=True)
            for index, (measure_type_id, measure_type_name, measure_type_unit) \
                    in enumerate(measure_types):
                self.addItem(f"{measure_type_name} ({measure_type_unit})")
                self.index_id_dict[index] = measure_type_id

    def get_id(self):
        return self.index_id_dict[self.currentIndex()]


class WindowAddMeasure(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Add Measure")
        self.setWindowModality(Qt.WindowModal)
        self.setLayout(QFormLayout(self))

        self.label_name = QLabel("Measure Name:", self)
        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.textChanged.connect(self.remove_style_sheet_line_edit_name)
        self.layout().addRow(self.label_name, self.line_edit_name)
        self.label_type = QLabel("Measure Type:", self)
        self.combobox_type = ComboboxMeasureTypes(self)
        self.layout().addRow(self.label_type, self.combobox_type)
        self.label_per_set = QLabel("Per Set:", self)
        self.checkbox_per_set = QCheckBox(self)
        self.layout().addRow(self.label_per_set, self.checkbox_per_set)
        self.button_discard = QPushButton("Discard", self)
        self.button_discard.clicked.connect(self.button_discard_action)
        self.button_add = QPushButton("Add", self)
        self.button_add.clicked.connect(self.button_add_measure_action)
        self.layout().addRow(self.button_discard, self.button_add)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.line_edit_name.setText("")
        self.checkbox_per_set.setChecked(False)
        return super().closeEvent(event)

    def button_discard_action(self):
        self.close()

    def button_add_measure_action(self):
        if self.line_edit_name.text() == "":
            self.line_edit_name.setStyleSheet("QLineEdit {background: rgb(255, 0, 0)}")
        else:
            measure = self.create_measure_from_input()
            self.close()
            self.parent().insert_measure_into_table(measure)

    def remove_style_sheet_line_edit_name(self):
        self.line_edit_name.setStyleSheet("")

    def create_measure_from_input(self):
        name = self.line_edit_name.text()
        type_id = self.combobox_type.get_id()
        per_set = self.checkbox_per_set.isChecked()
        return Measure(name, type_id, per_set)


class WindowNewExercise(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Add New Exercise")
        self.setWindowModality(Qt.WindowModal)
        self.setLayout(QVBoxLayout(self))
        self.measures = []

        self.new_exercise_form = WidgetNewExerciseForm(self)
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

        self.window_add_measure = WindowAddMeasure(self)

        self.measure_buttons = QWidget(self)
        self.layout().addWidget(self.measure_buttons)
        self.measure_buttons.setLayout(QHBoxLayout(self.measure_buttons))
        self.button_delete_measure = QPushButton("Delete Measure", self.measure_buttons)
        self.button_delete_measure.clicked.connect(self.delete_measures_action)
        self.measure_buttons.layout().addWidget(self.button_delete_measure)
        self.button_add_measure = QPushButton("Add Measure", self.measure_buttons)
        self.measure_buttons.layout().addWidget(self.button_add_measure)
        self.button_add_measure.clicked.connect(self.add_measure_action)
        self.radio_button_sets = QRadioButton("Add Sets Measure", self.measure_buttons)
        self.measure_buttons.layout().addWidget(self.radio_button_sets)
        self.radio_button_sets.toggled.connect(self.sets_measure_action)

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

        self.error_message = QErrorMessage(self)

    def add_measure_action(self):
        self.window_add_measure.show()

    def sets_measure_action(self, checked):
        if checked:
            self.measures.append(Measure("Sets", 5, False))
        else:
            self.measures.remove(Measure("Sets", 5, False))

    def closeEvent(self, event: QCloseEvent) -> None:
        self.line_edit_name.setText("")
        self.text_edit_comment.setPlainText("")
        self.line_edit_url.setText("")
        self.group_box_muscle_groups.uncheck_checkboxes()
        self.table_measures.setRowCount(0)
        self.measures = []
        return super().closeEvent(event)

    def button_discard_action(self):
        self.close()

    def button_add_exercise_action(self):
        valid_input = True
        if self.line_edit_name.text() == "":
            self.line_edit_name.setStyleSheet("QLineEdit {background: rgb(255, 0, 0)}")
            valid_input = False
        per_set_consistency = True
        for measure in self.measures:
            if measure.type_id == 5:
                per_set_consistency = True
                break
            if measure.per_set:
                per_set_consistency = False
        if not per_set_consistency:
            self.error_message.setWindowTitle("Cannot Add New Exercise!")
            self.error_message.showMessage("A measure is specified as 'per set', but the measure "
                                           "'sets' was not selected.")
            return
        if valid_input:
            exercise = self.create_exercise_from_input()
            exercise_id = self.super_parent().database.new_exercise(exercise)
            for measure in self.measures:
                self.super_parent().database.new_measure(measure, exercise_id)
            self.close()
            self.super_parent().update_table_exercises()

    def remove_style_sheet_line_edit_name(self):
        self.line_edit_name.setStyleSheet("")

    def create_exercise_from_input(self):
        name = self.line_edit_name.text()
        comment = self.text_edit_comment.toPlainText()
        url = self.line_edit_url.text()
        category_id = self.combobox_category.get_id()
        difficulty_id = self.combobox_difficulty.get_id()
        muscle_group_ids = self.group_box_muscle_groups.get_ids()
        return Exercise(name, comment, url, category_id, difficulty_id, muscle_group_ids)

    def insert_measure_into_table(self, measure):
        self.measures.append(measure)
        row_count = self.table_measures.rowCount()
        self.table_measures.insertRow(row_count)
        self.table_measures.setItem(row_count, 0, QTableWidgetItem(measure.name))
        type_string = self.super_parent().database.get_measure_type_string_for_id(measure.type_id)
        self.table_measures.setItem(row_count, 1, QTableWidgetItem(type_string))
        per_set_string = "yes" if measure.per_set else "no"
        self.table_measures.setItem(row_count, 2, QTableWidgetItem(per_set_string))

    def delete_measures_action(self):
        selection_model = self.table_measures.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        rows_to_delete = set()
        for index in selected_indexes:
            rows_to_delete.add(index.row())
        rows_to_delete = list(rows_to_delete)
        rows_to_delete.sort(reverse=True)
        for row in rows_to_delete:
            self.table_measures.removeRow(row)
            del self.measures[row]


class WidgetNewExerciseForm(BasicWidget):
    def __init__(self, parent):
        super().__init__(parent)


class GroupBoxMuscleGroups(QGroupBox, BasicWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setLayout(QGridLayout(self))
        self.number_columns = 3
        self.checkboxes = []
        self.muscle_group_ids = []
        self.create_checkboxes_from_database()

    def update(self) -> None:
        super().update()
        for checkbox in self.checkboxes:
            checkbox.hide()
            self.layout().removeWidget(checkbox)
        self.create_checkboxes_from_database()

    def uncheck_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def create_checkboxes_from_database(self):
        database = self.super_parent().database
        self.checkboxes = []
        self.muscle_group_ids = []
        if database:
            muscle_groups = database.get_muscle_groups()
            for i, (id_muscle_group, muscle_group) in enumerate(muscle_groups):
                checkbox = QCheckBox(muscle_group, self)
                self.checkboxes.append(checkbox)
                self.muscle_group_ids.append(id_muscle_group)
                self.layout().addWidget(checkbox, i // 3, i % 3)

    def get_ids(self):
        ids = []
        for muscle_group_id, checkbox in zip(self.muscle_group_ids, self.checkboxes):
            if checkbox.isChecked():
                ids.append(muscle_group_id)
        return ids
