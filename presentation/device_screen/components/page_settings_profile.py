import re
from PySide6.QtCore import Signal, Qt, QEvent
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
)


class PageSettingsPopup(QDialog):
    save_page = Signal(dict)
    delete_page = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(420)

        self._user_edited_id = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgb(40, 40, 40);
                border-radius: 12px;
            }
            QLabel {
                color: #f5f6fa;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2f3640;
                color: #f5f6fa;
                border: 1px solid #718093;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        header = QLabel("Page Settings")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(header)

        # Page Name
        name_label = QLabel("Page Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter page name...")

        # Page ID
        id_label = QLabel("Page ID:")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter custom page ID...")

        self.name_input.textChanged.connect(self._on_name_changed)
        self.id_input.installEventFilter(self)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)

        # Spodní tlačítka
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 12, 0, 0)

        # Delete button
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setFixedHeight(36)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)

        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)

        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedHeight(36)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)

        self.delete_btn.clicked.connect(self._handle_delete)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self._handle_save)

        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)
        main_layout.addWidget(container)

    def set_data(self, page):
        if not page:
            return
        self._user_edited_id = True  # Při načtení existujících dat vypneme auto-přepisování ID
        self.name_input.setText(getattr(page, "name", ""))
        self.id_input.setText(getattr(page, "id", ""))

    def eventFilter(self, obj, event):
        if obj == self.id_input and event.type() in (QEvent.Type.FocusIn, QEvent.Type.MouseButtonPress):
            self._user_edited_id = True
        return super().eventFilter(obj, event)

    def _on_name_changed(self, text: str):
        if self._user_edited_id:
            return
        ignored_words = {"view", "profile", "screen", "page"}
        words = re.split(r'[\s_]+', text.lower())
        filtered_words = [w for w in words if w and w not in ignored_words]
        self.id_input.setText("_".join(filtered_words))

    def _handle_save(self):
        data = {
            "name": self.name_input.text().strip(),
            "id": self.id_input.text().strip(),
        }
        self.save_page.emit(data)
        self.accept()

    def _handle_delete(self):
        page_id = self.id_input.text().strip()
        self.delete_page.emit(page_id)
        self.accept()