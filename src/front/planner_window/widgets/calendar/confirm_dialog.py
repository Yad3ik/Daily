from pathlib import Path

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

_PLANNER_DIR = Path(__file__).resolve().parents[2]
_AUTH_QSS = _PLANNER_DIR.parent / "auth_window" / "auth_styles.qss"
_PLANNER_QSS = _PLANNER_DIR / "planner_styles.qss"


class ConfirmDialog(QDialog):
    """Small frameless yes/no dialog in app style."""

    def __init__(self, message: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("confirmDialog")
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(340, 148)

        auth_qss = _AUTH_QSS.read_text(encoding="utf-8")
        planner_qss = _PLANNER_QSS.read_text(encoding="utf-8")
        self.setStyleSheet(auth_qss + "\n" + planner_qss)

        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        surface = QFrame()
        surface.setObjectName("confirmDialogSurface")
        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(24, 22, 24, 20)
        surface_layout.setSpacing(20)

        text = QLabel(message)
        text.setObjectName("confirmDialogMessage")
        text.setAlignment(Qt.AlignCenter)
        text.setWordWrap(True)
        surface_layout.addWidget(text)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        buttons.addStretch(1)

        no_btn = QPushButton("Нет")
        no_btn.setObjectName("dialogCancelButton")
        no_btn.setCursor(Qt.PointingHandCursor)
        no_btn.clicked.connect(self.reject)

        yes_btn = QPushButton("Да")
        yes_btn.setObjectName("dialogSaveButton")
        yes_btn.setCursor(Qt.PointingHandCursor)
        yes_btn.clicked.connect(self.accept)

        buttons.addWidget(no_btn)
        buttons.addWidget(yes_btn)
        surface_layout.addLayout(buttons)

        root.addWidget(surface)

        if parent is not None:
            parent_geo = parent.frameGeometry()
            self.move(
                parent_geo.center().x() - self.width() // 2,
                parent_geo.center().y() - self.height() // 2,
            )

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)
        painter.fillPath(path, QColor("#15131a"))
        painter.setPen(QColor("#393443"))
        painter.drawPath(path)
        super().paintEvent(event)
