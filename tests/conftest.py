import shutil
import sys
import sqlite3 as sql

import pytest

from workouts_tracking.gui import create_app, create_and_show_main_window
from workouts_tracking.database import Database
from workouts_tracking.exercise import Exercise
from workouts_tracking.constants import TESTS_DIR


@pytest.fixture(scope="session")
def q_app_fixture():
    q_app = create_app(sys.argv)
    yield q_app
    del q_app


@pytest.fixture(scope="session")
def main_window_fixture(q_app_fixture):
    main_window = create_and_show_main_window()
    yield main_window


@pytest.fixture(scope="session")
def central_widget_fixture(main_window_fixture):
    yield main_window_fixture.centralWidget()


@pytest.fixture()
def groupbox_database_fixture(central_widget_fixture):
    yield central_widget_fixture.widget_right.groupbox_database


@pytest.fixture()
def groupbox_workout_fixture(central_widget_fixture):
    yield central_widget_fixture.widget_right.groupbox_workout


@pytest.fixture()
def groupbox_exercise_fixture(central_widget_fixture):
    yield central_widget_fixture.widget_right.groupbox_exercise


@pytest.fixture()
def groupbox_available_exercises_fixture(central_widget_fixture):
    yield central_widget_fixture.widget_right.groupbox_exercises


@pytest.fixture()
def empty_database_fixture(tmp_path):
    database_filename = tmp_path / "test_database.db"
    database = Database(database_filename)
    yield database


@pytest.fixture()
def exercise_fixture():
    exercise = Exercise("Test Exercise", 4)
    yield exercise


@pytest.fixture()
def database_filename_fixture(tmp_path):
    yield tmp_path / "test_database.db"


@pytest.fixture()
def basic_database_fixture(tmp_path):
    shutil.copy(TESTS_DIR / "database" / "basic_database.db", tmp_path / "basic_database.db")
    connection = sql.connect(tmp_path / "basic_database.db")
    cursor = connection.cursor()
    yield connection, cursor
