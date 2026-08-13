from PySide6.QtWidgets import QMainWindow

from presentation.main_window.main_view_model import MainViewModel


class MainWindow(QMainWindow):
    def __init__(self, view_model: MainViewModel):
        super().__init__()

        self.view_model = view_model

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        pass

    def _connect_signals(self):
        pass



