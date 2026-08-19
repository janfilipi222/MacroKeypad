from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from presentation.device_screen.components.keypad_view import KeypadView
from presentation.device_screen.components.profile_selector import ProfileSelector
from presentation.device_screen.components.page_selector import PageSelector
from presentation.device_screen.components.sidebar import SideBar
from presentation.device_screen.components.add_profile_popup import AddProfilePopup
from presentation.device_screen.components.add_page_popup import AddPagePopup
from presentation.device_screen.components.profile_settings_popup import ProfileSettingsPopup
from presentation.device_screen.components.page_settings_profile import PageSettingsPopup

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
        top_layout.setContentsMargins(50, 0, 50, 0)
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
        self.profile_selector.add_clicked.connect(self._show_add_profile_popup)
        self.profile_selector.settings_clicked.connect(self._show_profile_settings_popup)

        self._setup_save(top_layout)

        self.page_selector = PageSelector(self._vm, self)
        top_layout.addWidget(
            self.page_selector, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.page_selector.new_page_selected.connect(self._handle_new_page_selected)
        self.page_selector.add_clicked.connect(self._show_add_page_popup)
        self.page_selector.settings_clicked.connect(self._show_page_settings_popup)


        
    def _show_add_profile_popup(self):
        popup = AddProfilePopup(self)
        popup.add_profile.connect(self._handle_add_profile)
        popup.exec()

    def _show_profile_settings_popup(self):
        popup = ProfileSettingsPopup(self)
        if hasattr(self._vm, "curr_profile"):
            popup.set_data(self._vm.curr_profile)
        popup.save_profile.connect(self._vm.edit_curr_profile)
        popup.delete_profile.connect(self._handle_delete_profile)
        popup.exec()

    def _show_add_page_popup(self):
        popup = AddPagePopup(self)
        popup.add_page.connect(self._handle_add_page)
        popup.exec()

    def _show_page_settings_popup(self):
        popup = PageSettingsPopup(self)
        if hasattr(self._vm, "curr_page"):
            popup.set_data(self._vm.curr_page)
        popup.save_page.connect(self._vm.edit_curr_page)
        popup.delete_page.connect(self._handle_delete_page)
        popup.exec()


    def _handle_add_profile(self, profile: dict):
        self._vm.add_new_profile(profile)
        self.profile_selector.select_profile(profile["name"])

    def _handle_delete_profile(self, profile_id: str):
        self._vm.delete_profile(profile_id)
        self.profile_selector.select_profile(self._vm.get_all_profiles()[0])

    def _handle_add_page(self, page: dict):
        self._vm.add_new_page(page)
        self.page_selector.select_page(self._vm.curr_profile.pages[-1].name)

    def _handle_delete_page(self, page_id):
        self._vm.delete_page(page_id)
        self.page_selector.select_page(self._vm.curr_profile.pages[0].name)
        

    def _setup_save(self, top_layout):
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedHeight(40)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                font-weight: normal;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)

        self.save_btn.clicked.connect(self._handle_save_btn)

        top_layout.addWidget(
            self.save_btn, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

    def _handle_save_btn(self):
        self._vm.save_curr()
        self.keypad_view.refresh_icons()


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

        self.sidebar.options[0]["view"].shortcut_changed.connect(
            self._vm.select_new_params
        )
        self.sidebar.options[1]["view"].path_changed.connect(
            self._vm.select_new_params
        )
        self.sidebar.options[1]["view"].params_changed.connect(
            self._vm.select_new_args
        )
        self.sidebar.options[2]["view"].script_changed.connect(
            self._vm.select_new_params
        )
        self.sidebar.options[3]["view"].selected_changed.connect(
            self._vm.select_new_params
        )
        self.sidebar.options[4]["view"].action_changed.connect(
            self._vm.select_new_params
        )

        self.sidebar._button_group.idClicked.connect(
            self._vm.select_new_action
        )

        self.sidebar.icon_selector.icon_path_changed.connect(
            self._vm.select_new_icon_path
        )
