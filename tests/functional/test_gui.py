import sys
from time import sleep

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow

from workouts_tracking.gui import create_app, run_app


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

    def test_open_window(self):
        qmw = QMainWindow()
        qmw.show()
        sleep(3)
        qmw.close()
        assert qmw.isWindow()
