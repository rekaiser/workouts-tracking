from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QHBoxLayout, QWidget)
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
    main_window.showMaximized()
    return main_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)


class MainWidget(QSplitter):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.left_widget = LeftWidget(self)
        self.right_widget = RightWidget(self)
        self.layout().addWidget(self.left_widget)
        self.layout().addWidget(self.right_widget)


class LeftWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)


class RightWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
