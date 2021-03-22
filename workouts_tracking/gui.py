from PySide6.QtWidgets import QApplication, QMainWindow
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
    return main_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
