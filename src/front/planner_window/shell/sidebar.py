from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QColor,
    QLinearGradient,
    QPainter,
    QPen,
    QRadialGradient,
)
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

_ICON_COLOR = QColor("#c8b6e2")


class CheckSquareIcon(QWidget):
    """Rounded square with checkmark (tasks nav icon)."""

    def __init__(self, size: int = 30) -> None:
        super().__init__()
        self.setFixedSize(size, size)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(_ICON_COLOR, 2.4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        m = 3.0
        side = self.width() - 2 * m
        painter.drawRoundedRect(QRectF(m, m, side, side), 5.5, 5.5)

        # Checkmark inside the square.
        painter.drawLine(9, 16, 13, 20)
        painter.drawLine(13, 20, 22, 11)


class Sidebar(QFrame):
    """Navigation sidebar (tasks only for now)."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("plannerSidebar")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 26, 20, 28)
        root.setSpacing(20)

        view_cap = QLabel("ВИД")
        view_cap.setObjectName("sectionCaption")
        root.addWidget(view_cap)

        tasks_tab = QFrame()
        tasks_tab.setObjectName("viewTab")
        tasks_tab.setProperty("active", "true")
        tasks_tab.setFixedHeight(58)
        tab_layout = QHBoxLayout(tasks_tab)
        tab_layout.setContentsMargins(16, 0, 18, 0)
        tab_layout.setSpacing(14)
        tab_layout.addWidget(CheckSquareIcon(32))
        tasks_label = QLabel("Задачи")
        tasks_label.setObjectName("viewTabLabel")
        tab_layout.addWidget(tasks_label, 1)

        root.addWidget(tasks_tab)
        root.addStretch(1)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w, h = self.width(), self.height()

        # Diagonal backbone: magenta (top-left) → violet → navy (bottom-right).
        backbone = QLinearGradient(0, 0, w, h)
        backbone.setColorAt(0.0, QColor("#ff5aab"))
        backbone.setColorAt(0.18, QColor("#e8388a"))
        backbone.setColorAt(0.42, QColor("#5a2d6e"))
        backbone.setColorAt(0.68, QColor("#1a1428"))
        backbone.setColorAt(1.0, QColor("#0a1020"))
        painter.fillRect(rect, backbone)

        # Bright pink bloom — top-left (main accent #F03F83 family).
        pink_glow = QRadialGradient(-w * 0.12, -h * 0.08, w * 1.1)
        pink_glow.setColorAt(0.0, QColor("#ff6eb8"))
        pink_glow.setColorAt(0.22, QColor(240, 63, 131, 210))
        pink_glow.setColorAt(0.5, QColor(180, 40, 100, 70))
        pink_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, pink_glow)

        # Deep purple / near-black — top-right and center.
        violet_shadow = QRadialGradient(w * 1.05, h * 0.05, w * 0.95)
        violet_shadow.setColorAt(0.0, QColor("#120e1c"))
        violet_shadow.setColorAt(0.45, QColor(18, 12, 28, 160))
        violet_shadow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, violet_shadow)

        # Royal blue glow — bottom-right.
        blue_glow = QRadialGradient(w * 1.08, h * 1.05, w * 0.92)
        blue_glow.setColorAt(0.0, QColor("#3d7cff"))
        blue_glow.setColorAt(0.25, QColor(50, 90, 220, 170))
        blue_glow.setColorAt(0.55, QColor(25, 45, 120, 60))
        blue_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, blue_glow)

        # Subtle dark vignette along the bottom edge.
        bottom_fade = QLinearGradient(0, h * 0.72, 0, h)
        bottom_fade.setColorAt(0.0, QColor(0, 0, 0, 0))
        bottom_fade.setColorAt(1.0, QColor(6, 8, 16, 140))
        painter.fillRect(rect, bottom_fade)

        super().paintEvent(event)
