import sys
from time import sleep

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from workouts_tracking.gui import create_app, create_and_show_main_window


@pytest.fixture(scope="session")
def q_app_fixture():
    q_app = create_app(sys.argv)
    yield q_app
    del q_app


class TestCaseLoadGui:
    def test_create_app(self, q_app_fixture):
        assert type(q_app_fixture) == QApplication

    def test_app_name(self, q_app_fixture):
        assert q_app_fixture.applicationName() == "Workouts Tracking"

    def test_open_close_window(self):
        main_window = create_and_show_main_window()
        sleep(0.05)
        assert main_window.isWindow()
        assert main_window.close()
