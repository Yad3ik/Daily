from datetime import datetime

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.back.structures import Event
from src.config import TAGS

HOUR_HEIGHT = 56
HOURS_IN_DAY = 24
GRID_HEIGHT = HOUR_HEIGHT * HOURS_IN_DAY


class EventBlock(QFrame):
    def __init__(self, event: Event) -> None:
        super().__init__()
        color = event.color or TAGS.get(event.tag or "", "#8E8794")
        self.setObjectName("eventBlock")
        self.setStyleSheet(
            f"QFrame#eventBlock {{"
            f" background-color: rgba(18, 16, 26, 215);"
            f" border: 1px solid {color};"
            f" border-left: 3px solid {color};"
            f" border-radius: 8px;"
            f"}}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        time_lbl = QLabel(
            f"{event.start.strftime('%H:%M')} – {event.finish.strftime('%H:%M')}"
        )
        time_lbl.setObjectName("eventBlockTime")

        title_lbl = QLabel(event.description)
        title_lbl.setObjectName("eventBlockTitle")
        title_lbl.setWordWrap(True)

        tag_name = event.tag or "Другое"
        tag_lbl = QLabel(f"● {tag_name}")
        tag_lbl.setObjectName("eventBlockTag")
        tag_lbl.setStyleSheet(f"color: {color};")

        layout.addWidget(time_lbl)
        layout.addWidget(title_lbl)
        layout.addWidget(tag_lbl)

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
        return max(44, int(minutes / 60 * HOUR_HEIGHT))
