from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)


class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, icon_path: str | Path, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background-color: #3498db; border-radius: 4px;")

        pixmap = QPixmap(str(icon_path))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                20,
                20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ProfilePopup(QWidget):
    profile_selected = Signal(str)

    def __init__(self, profiles: list, width: int, parent=None):
        super().__init__(
            parent,
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(width)

        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background-color: #2ecc71;
                border-radius: 4px;
            }
        """)

        popup_layout = QVBoxLayout(self)
        popup_layout.setContentsMargins(0, 4, 0, 0)
        popup_layout.addWidget(container)

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 4, 0, 4)
        vbox.setSpacing(2)

        for profile_name in profiles:
            btn = QPushButton(str(profile_name))
            btn.setFixedHeight(32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: black;
                    border: none;
                    text-align: left;
                    padding-left: 12px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                    border-radius: 2px;
                }
            """)
            btn.clicked.connect(
                lambda checked=False, name=profile_name: self._on_select(name)
            )
            vbox.addWidget(btn)

    def _on_select(self, name: str):
        self.profile_selected.emit(name)
        self.close()


class PageSelector(QWidget):
    add_clicked = Signal()
    settings_clicked = Signal()
    new_page_selected = Signal(str)

    RECT_WIDTH = 250

    def __init__(self, vm, parent=None):
        super().__init__(parent)

        self._vm = vm

        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Levý čtverec (ikona Add)
        sq1 = ClickableLabel(f"{self._vm.system_icons}/add.png")
        sq1.clicked.connect(self.add_clicked.emit)

        # Prostřední obdélník
        self.rect = QWidget()
        self.rect.setFixedSize(self.RECT_WIDTH, 40)
        self.rect.setStyleSheet("background-color: #2ecc71; border-radius: 4px;")
        self.rect.setCursor(Qt.CursorShape.PointingHandCursor)

        rect_layout = QHBoxLayout(self.rect)
        rect_layout.setContentsMargins(8, 0, 8, 0)

        self.profile_label = QLabel(str(vm.curr_page.name))
        self.profile_label.setStyleSheet("background: transparent;")

        arrow_pixmap = QPixmap(f"{self._vm.system_icons}/arrow_down.png")
        icon_label = QLabel()
        icon_label.setStyleSheet("background: transparent;")
        if not arrow_pixmap.isNull():
            icon_label.setPixmap(
                arrow_pixmap.scaled(
                    16,
                    16,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        rect_layout.addWidget(
            self.profile_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        rect_layout.addWidget(
            icon_label, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.rect.mousePressEvent = self._show_profiles_popup

        # Pravý čtverec (ikona Settings)
        sq2 = ClickableLabel(f"{self._vm.system_icons}/settings.png")
        sq2.clicked.connect(self.settings_clicked.emit)

        layout.addWidget(sq1)
        layout.addWidget(self.rect)
        layout.addWidget(sq2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def _show_profiles_popup(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            profiles = self._vm.get_all_pages()

            self.popup = ProfilePopup(
                profiles=profiles, width=self.RECT_WIDTH, parent=self
            )
            self.popup.profile_selected.connect(self._select_profile)

            global_pos = self.rect.mapToGlobal(self.rect.rect().bottomLeft())
            self.popup.move(global_pos)
            self.popup.show()

    def _select_profile(self, profile_name: str):
        self.profile_label.setText(str(profile_name))
        self.new_page_selected.emit(profile_name)