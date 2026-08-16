import os
from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QButtonGroup,
    QStackedWidget,
    QGroupBox,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QTextEdit
)


class ShortcutView(QWidget):
    shortcut_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel("Shortcut")
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")

        self.shortcut_input = QLineEdit()
        self.shortcut_input.setPlaceholderText("Write a shortcut...")
        self.shortcut_input.setStyleSheet("""
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        self.shortcut_input.textChanged.connect(self.shortcut_changed.emit)

        layout.addWidget(label)
        layout.addWidget(self.shortcut_input)
        layout.addStretch()

    def set_shortcut(self, text: str):
        self.shortcut_input.setText(text)


class ExecutablePathView(QWidget):
    path_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel("Select executable file path (.exe) to run:")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select executable (.exe)...")
        self.path_input.setStyleSheet("""
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        browse_btn = QPushButton("Browse...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.path_input.textChanged.connect(self.path_changed.emit)
        browse_btn.clicked.connect(self._browse_file)

        layout.addWidget(label)
        layout.addWidget(self.path_input)
        layout.addWidget(browse_btn)
        layout.addStretch()

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable",
            "",
            "Executable Files (*.exe);;All Files (*)",
        )
        if file_path:
            self.path_input.setText(file_path)

    def set_path(self, path: str):
        self.path_input.setText(path)


class ScriptSelectorView(QWidget):
    script_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel("Enter script code or command:")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")

        self.script_input = QTextEdit()
        self.script_input.setPlaceholderText("Write your script here...")
        self.script_input.setStyleSheet("""
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 6px;
                font-family: Consolas, Monaco, monospace;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        # Vysílání signálu při každé úpravě textu
        self.script_input.textChanged.connect(self._on_text_changed)

        layout.addWidget(label)
        layout.addWidget(self.script_input)

    def _on_text_changed(self):
        self.script_changed.emit(self.script_input.toPlainText())

    def set_script(self, text: str):
        self.script_input.setPlainText(text)


class SystemView(QWidget):
    selected_changed = Signal(str)

    def __init__(self, items: list[str], parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel("Select an option:")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")
        layout.addWidget(label)

        self._button_group = QButtonGroup(self)

        for index, item_text in enumerate(items):
            radio_btn = QRadioButton(item_text)
            radio_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            radio_btn.setStyleSheet("""
                QRadioButton {
                    color: #ecf0f1;
                    padding: 4px;
                    font-size: 13px;
                }
                QRadioButton::indicator {
                    width: 14px;
                    height: 14px;
                }
            """)
            layout.addWidget(radio_btn)
            self._button_group.addButton(radio_btn, index)

        self._button_group.idClicked.connect(self._on_radio_clicked)
        layout.addStretch()

    def _on_radio_clicked(self, index: int):
        button = self._button_group.button(index)
        if button:
            self.selected_changed.emit(button.text())

    def set_selected(self, text: str):
        for button in self._button_group.buttons():
            if button.text() == text:
                button.setChecked(True)
                break

class EmptyView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)


class IconSelectorView(QWidget):
    icon_path_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel("Icon Path:")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select icon path...")
        self.path_input.setStyleSheet("""
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        browse_btn = QPushButton("Browse...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.path_input.textChanged.connect(self.icon_path_changed.emit)
        browse_btn.clicked.connect(self._browse_file)

        layout.addWidget(label)
        layout.addWidget(self.path_input)
        layout.addWidget(browse_btn)

    def _browse_file(self):
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        appdata = Path(local_appdata)
        appdata = appdata / "CGM" / "MacroKeypadBackgroundApp" / "icons"

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            str(appdata),
            "Image Files (*.png *.jpg *.jpeg *.ico *.svg);;All Files (*)",
        )
        if file_path:
            self.path_input.setText(file_path)

    def set_icon_path(self, path: str):
        if path == None:
            path = ""
        self.path_input.setText(path)


class SideBar(QWidget):
    option_changed = Signal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        system_actions = [
            "next slide",
            "prev slide",
            "calculator",
        ]

        self.options = [
            {"id": 0, "name": "Shortcut", "view": ShortcutView()},
            {"id": 1, "name": "Run Program", "view": ExecutablePathView()},
            {"id": 2, "name": "Run Script", "view": ScriptSelectorView()},
            {"id": 3, "name": "System Action", "view": SystemView(system_actions)},
            {"id": 4, "name": "None", "view": EmptyView()},
        ]

        self.setFixedWidth(260)
        self.setStyleSheet("""
            SideBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QGroupBox {
                color: #ecf0f1;
                font-weight: bold;
                border: 1px solid #34495e;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QRadioButton {
                color: #ecf0f1;
                padding: 4px;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        self.icon_selector = IconSelectorView(self)
        main_layout.addWidget(self.icon_selector)

        radio_box = QGroupBox("Options")
        radio_layout = QVBoxLayout(radio_box)
        radio_layout.setSpacing(6)

        self._button_group = QButtonGroup(self)

        for option in self.options:
            radio_btn = QRadioButton(option["name"])
            radio_layout.addWidget(radio_btn)
            self._button_group.addButton(radio_btn, option["id"])

        main_layout.addWidget(radio_box)

        settings_box = QGroupBox("Detail Settings")
        settings_layout = QVBoxLayout(settings_box)

        self._stacked_widget = QStackedWidget()

        for option in self.options:
            self._stacked_widget.addWidget(option["view"])

        settings_layout.addWidget(self._stacked_widget)
        main_layout.addWidget(settings_box)

        main_layout.addStretch()


        self._button_group.idClicked.connect(self._on_radio_selected)

        if self.options:
            first_btn = self._button_group.button(0)
            if first_btn:
                first_btn.setChecked(True)
                self._on_radio_selected(0)


    def set_data(self, data: dict):

        if not data or "action" not in data:
            action_name = "none"

        if "icon" in data:
            self.icon_selector.set_icon_path(data["icon"])

        params: dict = data.get("params", {})
        action_name = str(data["action"]).lower()

        if "keybind" in action_name or "shortcut" in action_name:
            target_id = 0
            val = params.get("keys", params.get("shortcut", ""))
            self.options[0]["view"].set_shortcut(val)

        elif "program" in action_name or "executable" in action_name:
            target_id = 1
            val = params.get("path", params.get("executable", ""))
            self.options[1]["view"].set_path(val)

        elif "script" in action_name:
            target_id = 2
            val = params.get("name", params.get("code", ""))
            self.options[2]["view"].set_script(val)

        elif "system" in action_name:
            target_id = 3
            val = params.get("action", params.get("name", params.get("selected", "")))
            self.options[3]["view"].set_selected(val)
            
        elif "none" in action_name:
            target_id = 4


        else:
            return

        btn = self._button_group.button(target_id)
        if btn:
            btn.setChecked(True)
            self._on_radio_selected(target_id)

    def _on_radio_selected(self, option_id: int):
        self._stacked_widget.setCurrentIndex(option_id)

        selected_name = next(
            (opt["name"] for opt in self.options if opt["id"] == option_id), ""
        )
        self.option_changed.emit(option_id, selected_name)