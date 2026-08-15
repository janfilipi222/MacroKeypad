from PySide6.QtWidgets import QMainWindow

from presentation.device_screen.device_screen import DeviceScreen


class MainWindow(QMainWindow):

    def __init__(self, device_vm, parent=None):
        super().__init__(parent)

        self.device_vm = device_vm

        self.device_view = DeviceScreen(
            self.device_vm,
            self
        )

        self.setCentralWidget(self.device_view)

        self.setWindowTitle("Macro Keypad")
        self.resize(1200, 800)



        