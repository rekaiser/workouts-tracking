import sys

import pytest

from workouts_tracking.gui import create_app, create_and_show_main_window


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
