from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import (
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
)


class IconLabel(QLabel):
    clicked = Signal(int, int)

    # Jemnější rozdíl ve velikosti tlačítek
    NORMAL_SIZE = 64
    ACTIVE_SIZE = 72

    NORMAL_ICON_SIZE = 54
    ACTIVE_ICON_SIZE = 62

    RADIUS = 10

    def __init__(self, row: int, col: int, parent=None):
        super().__init__(parent)

        self._row = row
        self._col = col
        self._current_path: str | Path | None = None
        self._is_active = False

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #505050;
                border-radius: 10px;
            }
        """)

        self.set_active_state(False)

    def set_active_state(self, is_active: bool):
        self._is_active = is_active

        size = self.ACTIVE_SIZE if is_active else self.NORMAL_SIZE
        self.setFixedSize(size, size)

        if self._current_path:
            self.set_icon(self._current_path)

    def set_icon(self, path: str | Path | None):
        self._current_path = path

        if not path:
            self.clear()
            return

        pixmap = QPixmap(str(path))

        if pixmap.isNull():
            self.clear()
            return

        icon_size = (
            self.ACTIVE_ICON_SIZE if self._is_active else self.NORMAL_ICON_SIZE
        )

        pixmap = pixmap.scaled(
            icon_size,
            icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        pixmap = self._rounded_pixmap(
            pixmap,
            self.RADIUS,
        )

        self.setPixmap(pixmap)

    def _rounded_pixmap(
        self,
        pixmap: QPixmap,
        radius: int,
    ) -> QPixmap:
        result = QPixmap(pixmap.size())
        result.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(
            0,
            0,
            pixmap.width(),
            pixmap.height(),
            radius,
            radius,
        )

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return result

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._row, self._col)

        super().mousePressEvent(event)


class KeypadView(QWidget):
    icon_clicked = Signal(int, int)

    ROWS = 6
    COLS = 4

    CELL_SIZE = 72
    SPACING = 8
    PADDING = 10

    def __init__(self, device_vm, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self._device_vm = device_vm
        self._labels: list[list[IconLabel]] = []

        self.setStyleSheet("""
            KeypadView {
                background-color: #303030;
                border-radius: 12px;
            }
        """)

        self._setup_ui()

        initial_btn = getattr(self._device_vm, "curr_btn", [0, 0])
        self._set_active_button(initial_btn[0], initial_btn[1])

        self.refresh_icons()

    def _setup_ui(self):
        layout = QGridLayout(self)

        layout.setContentsMargins(
            self.PADDING,
            self.PADDING,
            self.PADDING,
            self.PADDING,
        )

        layout.setHorizontalSpacing(self.SPACING)
        layout.setVerticalSpacing(self.SPACING)

        for row in range(self.ROWS):
            label_row = []

            layout.setRowMinimumHeight(row, self.CELL_SIZE)

            for col in range(self.COLS):
                if row == 0:
                    layout.setColumnMinimumWidth(col, self.CELL_SIZE)

                label = IconLabel(row, col, self)
                label.clicked.connect(self._on_label_clicked)

                layout.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)
                label_row.append(label)

            self._labels.append(label_row)

        width = (
            self.PADDING * 2
            + self.COLS * self.CELL_SIZE
            + (self.COLS - 1) * self.SPACING
        )

        height = (
            self.PADDING * 2
            + self.ROWS * self.CELL_SIZE
            + (self.ROWS - 1) * self.SPACING
        )

        self.setFixedSize(width, height)

    def _on_label_clicked(self, row: int, col: int):
        self._set_active_button(row, col)
        self.icon_clicked.emit(row, col)

    def _set_active_button(self, row: int, col: int):
        for r in range(self.ROWS):
            for c in range(self.COLS):
                is_active = r == row and c == col
                self._labels[r][c].set_active_state(is_active)

    def refresh_icons(self):
        icon_paths = self._device_vm.get_curr_icon_paths()
        self._set_active_button(0, 0)
        self.icon_clicked.emit(0, 0)

        for row in range(self.ROWS):
            for col in range(self.COLS):
                self._labels[row][col].set_icon(icon_paths[row][col])