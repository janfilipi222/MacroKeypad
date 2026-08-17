import os
from pathlib import Path

from PySide6.QtCore import Signal, Qt, QEvent
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
    params_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        # 1. Cesta k executable
        label = QLabel("Select executable file path (.exe) to run:")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ecf0f1; font-weight: bold;")

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select executable (.exe)...")
        self.path_input.setStyleSheet(self._line_edit_style())

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

        self.layout.addWidget(label)
        self.layout.addWidget(self.path_input)
        self.layout.addWidget(browse_btn)

        # 2. Parametry / Argumenty
        params_label = QLabel("Arguments / Parameters:")
        params_label.setStyleSheet("color: #ecf0f1; font-weight: bold; margin-top: 6px;")
        self.layout.addWidget(params_label)

        # Seznam pro uložení všech dynamických QLineEdit pro parametry
        self.param_inputs: list[QLineEdit] = []

        # Přidáme výchozí první pole pro parametry
        self._add_param_input()

        self.layout.addStretch()

    def _line_edit_style(self) -> str:
        return """
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
        """

    def _add_param_input(self, text: str = "") -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Enter argument...")
        line_edit.setStyleSheet(self._line_edit_style())
        if text:
            line_edit.setText(text)

        # Sledování zmen textu
        line_edit.textChanged.connect(self._on_param_text_changed)

        # Odchytávání události ztráty fokusu (focus out)
        line_edit.installEventFilter(self)

        self.param_inputs.append(line_edit)

        # Vložíme nový LineEdit těsně před Stretch na konci layoutu
        self.layout.insertWidget(self.layout.count() - 1, line_edit)
        return line_edit

    def _on_param_text_changed(self):
        sender: QLineEdit = self.sender()

        # Pokud uživatel začal psát do posledního pole, automaticky vytvoříme nové
        if sender == self.param_inputs[-1] and sender.text().strip() != "":
            self._add_param_input()

        self._emit_params()

    def eventFilter(self, obj, event):
        # Detekce ztráty fokusu u polí s parametry
        if event.type() == QEvent.Type.FocusOut and obj in self.param_inputs:
            # Smaže pole pouze pokud je prázdné a NENÍ to jediné/poslední pole
            if obj.text().strip() == "" and len(self.param_inputs) > 1 and obj != self.param_inputs[-1]:
                self.param_inputs.remove(obj)
                obj.deleteLater()
                self._emit_params()

        return super().eventFilter(obj, event)

    def _emit_params(self):
        # Vrátí text ze všech polí (ignoruje prázdná pole)
        params_list = [line.text() for line in self.param_inputs if line.text().strip() != ""]
        self.params_changed.emit(params_list)

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

    def set_params(self, params: list[str]):
        # Vyčištění stávajících vstupů
        for line_edit in self.param_inputs:
            line_edit.deleteLater()
        self.param_inputs.clear()

        # Přidání polí s hodnotami
        for param in params:
            if param.strip() != "":
                self._add_param_input(param)

        # Vždy přidáme jedno prázdné pole na konec pro další zápis
        self._add_param_input()
        self._emit_params()

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

        self.script_input = QLineEdit()
        self.script_input.setPlaceholderText("Write your script here...")
        self.script_input.setStyleSheet("""
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 6px 10px;
                font-family: Consolas, Monaco, monospace;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        # Vysílání signálu při každé úpravě textu
        self.script_input.textChanged.connect(self.script_changed.emit)

        layout.addWidget(label)
        layout.addWidget(self.script_input)
        layout.addStretch()

    def set_script(self, text: str):
        self.script_input.blockSignals(True)
        self.script_input.setText(text)
        self.script_input.blockSignals(False)

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
            data = {"action": "none"}

        if "icon" in data:
            self.icon_selector.set_icon_path(data["icon"])

        params: dict = data.get("params", {})
        action_name = str(data.get("action", "none")).lower()

        if "keybind" in action_name or "shortcut" in action_name:
            target_id = 0
            val = params.get("keys", params.get("shortcut", ""))
            self.options[0]["view"].set_shortcut(val)

        elif "program" in action_name or "executable" in action_name:
            target_id = 1
            path = params.get("path", params.get("executable", ""))
            args = params.get("args", [])
            
            self.options[1]["view"].set_path(path)
            self.options[1]["view"].set_params(args)

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