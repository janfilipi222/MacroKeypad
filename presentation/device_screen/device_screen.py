from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from presentation.device_screen.components.keypad_view import KeypadView
from presentation.device_screen.components.profile_selector import ProfileSelector
from presentation.device_screen.components.page_selector import PageSelector
from presentation.device_screen.components.sidebar import SideBar


class DeviceScreen(QWidget):

    def __init__(self, device_vm, parent=None):
        super().__init__(parent)

        self._device_vm = device_vm

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        center_widget = QWidget(self)
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        top_layout = QHBoxLayout()
        center_layout.addLayout(top_layout)
        self._setup_top_selectors(top_layout)

        center_layout.addStretch(1)

        self._setup_keypad_view()
        center_layout.addWidget(
            self.keypad_view, 0, Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addStretch(1)

        main_layout.addWidget(center_widget, stretch=1)

        self._setup_sidebar()
        main_layout.addWidget(self.sidebar, stretch=0)

    def _setup_top_selectors(self, top_layout: QHBoxLayout):
        self.profile_selector = ProfileSelector(self._device_vm, self)
        top_layout.addWidget(
            self.profile_selector,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.page_selector = PageSelector(self._device_vm, self)
        top_layout.addWidget(
            self.page_selector,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.profile_selector.add_clicked.connect(lambda: print("add clicked"))
        self.profile_selector.settings_clicked.connect(
            lambda: print("settings clicked")
        )
        self.profile_selector.new_profile_selected.connect(
            lambda x: print("new profile: ", x)
        )

    def _setup_keypad_view(self):
        self.keypad_view = KeypadView(self._device_vm, self)
        self.keypad_view.icon_clicked.connect(self._on_icon_clicked)

    def _setup_sidebar(self):
        self.sidebar = SideBar(self)


    def _on_icon_clicked(self, row: int, col: int):
        print(row, col)