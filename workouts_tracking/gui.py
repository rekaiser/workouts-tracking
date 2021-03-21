from PySide6.QtWidgets import QApplication, QMainWindow
from .constants import APPLICATION_NAME


def create_app(sys_argv):
    q_app = QApplication(sys_argv)
    q_app.setApplicationName(APPLICATION_NAME)
    return q_app


def run_app(q_app: QApplication):
    main_window = QMainWindow()
    main_window.show()
    return q_app.exec_()
