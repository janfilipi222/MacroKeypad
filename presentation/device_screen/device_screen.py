from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from presentation.device_screen.components.keypad_view import KeypadView
from presentation.device_screen.components.profile_selector import ProfileSelector
from presentation.device_screen.components.page_selector import PageSelector
from presentation.device_screen.components.sidebar import SideBar

from presentation.main_window.main_view_model import MainViewModel


class DeviceScreen(QWidget):

    def __init__(self, device_vm: MainViewModel, parent=None):
        super().__init__(parent)

        self._vm = device_vm

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

        self.profile_selector = ProfileSelector(self._vm, self)
        top_layout.addWidget(
            self.profile_selector, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.profile_selector.new_profile_selected.connect(self._handle_new_profile_selected)

        self.page_selector = PageSelector(self._vm, self)
        top_layout.addWidget(
            self.page_selector, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.page_selector.new_page_selected.connect(self._handle_new_page_selected)


        self.profile_selector.add_clicked.connect(lambda: print("add clicked"))
        self.profile_selector.settings_clicked.connect(
            lambda: print("settings clicked")
        )

    def _handle_new_profile_selected(self, profile):
        self._vm.select_new_profile(profile)
        self.keypad_view.refresh_icons()

    def _handle_new_page_selected(self, page):
        self._vm.select_new_page(page)
        self.keypad_view.refresh_icons()


    def _handle_icon_selected(self, row, col):
        self._vm.select_new_icon(row, col)
        action = self._vm.curr_action
        if action == None:
            type = None
            icon = None
            params = None
        else:
            type = action.type
            icon = action.icon
            params = action.params
        self.sidebar.set_data({
            "action": type,
            "icon": icon,
            "params": params
        })



    def _setup_keypad_view(self):
        self.keypad_view = KeypadView(self._vm, self)
        self.keypad_view.icon_clicked.connect(self._handle_icon_selected)


    def _setup_sidebar(self):
        self.sidebar = SideBar(self)
        action = self._vm.curr_action
        action = self._vm.curr_action
        if action == None:
            type = None
            icon = None
            params = None
        else:
            type = action.type
            icon = action.icon
            params = action.params
        self.sidebar.set_data({
            "action": type,
            "icon": icon,
            "params": params
        })
