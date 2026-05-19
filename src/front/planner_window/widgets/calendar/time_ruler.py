from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from .event_block import GRID_HEIGHT, HOUR_HEIGHT, HOURS_IN_DAY


class TimeRuler(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("timeRuler")
        self.setFixedWidth(64)
        self.setMinimumHeight(GRID_HEIGHT)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(0)

        self._hour_labels: list[QLabel] = []
        for hour in range(HOURS_IN_DAY):
            lbl = QLabel(f"{hour:02d}:00")
            lbl.setObjectName("timeLabel")
            lbl.setFixedHeight(HOUR_HEIGHT)
            lbl.setAlignment(Qt.AlignTop | Qt.AlignRight)
            layout.addWidget(lbl)
            self._hour_labels.append(lbl)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        from datetime import datetime

        now = datetime.now()
        minutes = now.hour * 60 + now.minute
        y = int(minutes / 60 * HOUR_HEIGHT) + 4

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#F03F83"))
        painter.drawRoundedRect(0, y - 12, 52, 24, 4, 4)
        painter.setPen(QColor("#F6F0F4"))
        scale_font = self._hour_labels[0].font() if self._hour_labels else QFont("Noto Sans", 14)
        painter.setFont(scale_font)
        painter.drawText(4, y + 5, now.strftime("%H:%M"))
