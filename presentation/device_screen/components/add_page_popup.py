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


class AddPagePopup(QDialog):
    add_page = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(420)

        self._user_edited_id = False

        # Skrytí rámce okna a zapnutí průhlednosti
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Vnější layout okna bez okrajů
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Vnitřní pozadí (Container Widget)
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

        # Layout uvnitř kontejneru
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Header
        header = QLabel("New Page")
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

        # Připojení logiky generování ID
        self.name_input.textChanged.connect(self._on_name_changed)
        self.id_input.installEventFilter(self)

        # Přidání prvků
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)

        # Spodní tlačítka (Add Page, Cancel)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 12, 0, 0)

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

        self.add_btn = QPushButton("Add Page")
        self.add_btn.setFixedHeight(36)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet("""
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

        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn.clicked.connect(self._handle_add)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.add_btn)

        layout.addLayout(buttons_layout)

        # Přidání vnitřního kontejneru do hlavního okna
        main_layout.addWidget(container)

    def eventFilter(self, obj, event):
        if obj == self.id_input and event.type() in (QEvent.Type.FocusIn, QEvent.Type.MouseButtonPress):
            self._user_edited_id = True
        return super().eventFilter(obj, event)

    def _on_name_changed(self, text: str):
        if self._user_edited_id:
            return

        ignored_words = {"view", "profile", "screen", "page"}

        # Rozdělení textu podle mezer i podtržítek
        words = re.split(r'[\s_]+', text.lower())

        # Vyfiltrování prázdných řetězců a ignorovaných slov
        filtered_words = [w for w in words if w and w not in ignored_words]

        # Spojení zbývajících slov podtržítkem
        formatted = "_".join(filtered_words)

        self.id_input.setText(formatted)

    def _handle_add(self):
        data = {
            "name": self.name_input.text().strip(),
            "id": self.id_input.text().strip(),
        }
        self.add_page.emit(data)
        self.accept()