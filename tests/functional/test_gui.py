from PySide6.QtWidgets import (QApplication,)

from workouts_tracking.gui import create_and_show_main_window


class TestCaseLoadGui:
    def test_create_app(self, q_app_fixture):
        assert type(q_app_fixture) == QApplication

    def test_app_name(self, q_app_fixture):
        assert q_app_fixture.applicationName() == "Workouts Tracking"

    def test_open_close_window(self):
        main_window = create_and_show_main_window()
        assert main_window.isWindow()
        assert main_window.close()
