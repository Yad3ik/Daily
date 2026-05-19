from datetime import datetime

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.back.structures import Event
from src.config import TAGS

HOUR_HEIGHT = 56
HOURS_IN_DAY = 24
GRID_HEIGHT = HOUR_HEIGHT * HOURS_IN_DAY


def _tag_rgba(hex_color: str, alpha: float = 0.22) -> str:
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return f"rgba(142, 135, 148, {alpha})"
    r, g, b = (int(value[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


class EventBlock(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, event: Event) -> None:
        super().__init__()
        self._event = event
        self.setCursor(Qt.PointingHandCursor)
        color = event.color or TAGS.get(event.tag or "", "#8E8794")
        bg = _tag_rgba(color, 0.22)
        self.setObjectName("eventBlock")
        self.setStyleSheet(
            f"QFrame#eventBlock {{"
            f" background-color: {bg};"
            f" border: 1px solid {color};"
            f" border-left: 3px solid {color};"
            f" border-radius: 8px;"
            f"}}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        self._time_lbl = QLabel(
            f"{event.start.strftime('%H:%M')} – {event.finish.strftime('%H:%M')}"
        )
        self._time_lbl.setObjectName("eventBlockTime")
        self._time_lbl.setStyleSheet(f"color: {color};")
        self._time_lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self._title_lbl = QLabel(event.description)
        self._title_lbl.setObjectName("eventBlockTitle")
        self._title_lbl.setWordWrap(True)
        self._title_lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self._full_title = event.description

        tag_name = event.tag or "Другое"
        self._tag_lbl = QLabel(f"● {tag_name}")
        self._tag_lbl.setObjectName("eventBlockTag")
        self._tag_lbl.setStyleSheet(f"color: {color};")
        self._tag_lbl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        layout.addWidget(self._time_lbl, 0, Qt.AlignTop)
        layout.addWidget(self._title_lbl, 0, Qt.AlignTop)
        layout.addStretch(1)
        layout.addWidget(self._tag_lbl, 0, Qt.AlignBottom)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self._event)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        compact = self.height() < 56
        self._title_lbl.setWordWrap(not compact)
        if compact:
            text = self._title_lbl.fontMetrics().elidedText(
                self._full_title,
                Qt.ElideRight,
                max(20, self._title_lbl.width()),
            )
            self._title_lbl.setText(text)
        else:
            self._title_lbl.setText(self._full_title)

    @staticmethod
    def y_for_time(dt: datetime) -> int:
        minutes = dt.hour * 60 + dt.minute
        return int(minutes / 60 * HOUR_HEIGHT)

    @staticmethod
    def height_for_event(event: Event) -> int:
        start = event.start.hour * 60 + event.start.minute
        end = event.finish.hour * 60 + event.finish.minute
        if end <= start:
            end += 24 * 60
        minutes = max(30, end - start)
        return max(40, int(minutes / 60 * HOUR_HEIGHT))
