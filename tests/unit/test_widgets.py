from PySide6.QtWidgets import QSplitter, QLayout, QHBoxLayout, QWidget


class TestGuiLayout:
    def test_layout(self, main_window_fixture):
        mwf = main_window_fixture
        assert isinstance(mwf.centralWidget(), QSplitter)
        assert isinstance(mwf.layout(), QLayout)
        assert isinstance(mwf.centralWidget().layout(), QHBoxLayout)
        assert isinstance(mwf.centralWidget().left_widget, QWidget)
        assert isinstance(mwf.centralWidget().right_widget, QWidget)
        assert mwf.centralWidget().layout().count() == 2
