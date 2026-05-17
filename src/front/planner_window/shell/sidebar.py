from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QColor,
    QLinearGradient,
    QPainter,
    QRadialGradient,
)
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.config import TAGS

from ..calendar_state import CalendarState
from .view_switcher import ViewSwitcher

_ICON_COLOR = QColor("#c8b6e2")


class _TagRow(QFrame):
    def __init__(self, name: str, color: str, count: int) -> None:
        super().__init__()
        self.setObjectName("tagRow")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(10)

        dot = QLabel("●")
        dot.setObjectName("tagDot")
        dot.setStyleSheet(f"color: {color};")
        dot.setFixedWidth(14)

        title = QLabel(name)
        title.setObjectName("tagName")

        badge = QLabel(str(count))
        badge.setObjectName("tagCount")
        badge.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        lay.addWidget(dot)
        lay.addWidget(title, 1)
        lay.addWidget(badge)


class Sidebar(QFrame):
    def __init__(self, on_view_changed, calendar_state: CalendarState) -> None:
        super().__init__()
        self.setObjectName("plannerSidebar")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._calendar_state = calendar_state
        self._on_view_changed = on_view_changed
        self._tag_rows: list[_TagRow] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 26, 20, 28)
        root.setSpacing(20)

        view_cap = QLabel("ВИД")
        view_cap.setObjectName("sectionCaption")
        root.addWidget(view_cap)

        self._switcher = ViewSwitcher()
        self._switcher.view_changed.connect(self._on_view_changed)
        root.addWidget(self._switcher)

        self._tags_wrap = QWidget()
        tags_layout = QVBoxLayout(self._tags_wrap)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        tags_layout.setSpacing(6)

        tags_cap = QLabel("ТЕГИ")
        tags_cap.setObjectName("sectionCaption")
        tags_layout.addWidget(tags_cap)
        self._tags_list = QVBoxLayout()
        self._tags_list.setSpacing(2)
        tags_layout.addLayout(self._tags_list)
        root.addWidget(self._tags_wrap)

        root.addStretch(1)

    def set_active_view(self, key: str) -> None:
        self._switcher.set_active(key)
        self._tags_wrap.setVisible(key == "calendar")

    def refresh_tags(self, tag_counts: dict[str, int] | None = None) -> None:
        counts = tag_counts or {}
        while self._tags_list.count():
            item = self._tags_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._tag_rows.clear()
        for tag_name, color in TAGS.items():
            row = _TagRow(tag_name, color, counts.get(tag_name, 0))
            self._tags_list.addWidget(row)
            self._tag_rows.append(row)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w, h = self.width(), self.height()

        backbone = QLinearGradient(0, 0, w, h)
        backbone.setColorAt(0.0, QColor("#ff5aab"))
        backbone.setColorAt(0.18, QColor("#e8388a"))
        backbone.setColorAt(0.42, QColor("#5a2d6e"))
        backbone.setColorAt(0.68, QColor("#1a1428"))
        backbone.setColorAt(1.0, QColor("#0a1020"))
        painter.fillRect(rect, backbone)

        pink_glow = QRadialGradient(-w * 0.12, -h * 0.08, w * 1.1)
        pink_glow.setColorAt(0.0, QColor("#ff6eb8"))
        pink_glow.setColorAt(0.22, QColor(240, 63, 131, 210))
        pink_glow.setColorAt(0.5, QColor(180, 40, 100, 70))
        pink_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, pink_glow)

        violet_shadow = QRadialGradient(w * 1.05, h * 0.05, w * 0.95)
        violet_shadow.setColorAt(0.0, QColor("#120e1c"))
        violet_shadow.setColorAt(0.45, QColor(18, 12, 28, 160))
        violet_shadow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, violet_shadow)

        blue_glow = QRadialGradient(w * 1.08, h * 1.05, w * 0.92)
        blue_glow.setColorAt(0.0, QColor("#3d7cff"))
        blue_glow.setColorAt(0.25, QColor(50, 90, 220, 170))
        blue_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(rect, blue_glow)

        bottom_fade = QLinearGradient(0, h * 0.72, 0, h)
        bottom_fade.setColorAt(0.0, QColor(0, 0, 0, 0))
        bottom_fade.setColorAt(1.0, QColor(6, 8, 16, 140))
        painter.fillRect(rect, bottom_fade)

        super().paintEvent(event)
