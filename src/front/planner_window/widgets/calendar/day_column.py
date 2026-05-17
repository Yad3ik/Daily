from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.back.structures import Event

from .event_block import EventBlock, GRID_HEIGHT, HOUR_HEIGHT, HOURS_IN_DAY

_DAY_NAMES = ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")


class DayHeaderCell(QFrame):
    def __init__(self, day: date) -> None:
        super().__init__()
        self.setObjectName("dayHeaderCell")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        self._name = QLabel(_DAY_NAMES[day.weekday()])
        self._name.setObjectName("dayName")
        self._name.setAlignment(Qt.AlignCenter)

        self._num = QLabel(str(day.day))
        self._num.setObjectName("dayNumber")
        self._num.setAlignment(Qt.AlignCenter)

        layout.addWidget(self._name)
        layout.addWidget(self._num)
        self.set_day(day)

    def set_day(self, day: date) -> None:
        self._name.setText(_DAY_NAMES[day.weekday()])
        self._num.setText(str(day.day))
        today = date.today()
        self._num.setProperty("today", "true" if day == today else "false")
        self._num.style().unpolish(self._num)
        self._num.style().polish(self._num)


class DayColumn(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dayColumn")
        self.setMinimumHeight(GRID_HEIGHT)
        self._day: date | None = None
        self._events: list[Event] = []
        self._blocks: list[EventBlock] = []

    def set_day(self, day: date, events: list[Event]) -> None:
        self._day = day
        self._events = list(events)
        self._rebuild_blocks()

    def _rebuild_blocks(self) -> None:
        for block in self._blocks:
            block.deleteLater()
        self._blocks.clear()
        for event in self._events:
            block = EventBlock(event)
            block.setParent(self)
            self._blocks.append(block)
        self._layout_blocks()

    def _layout_blocks(self) -> None:
        width = max(48, self.width() - 10)
        for event, block in zip(self._events, self._blocks):
            block.setGeometry(
                5,
                EventBlock.y_for_time(event.start),
                width,
                EventBlock.height_for_event(event),
            )
            block.show()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._blocks:
            self._layout_blocks()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#221e28"), 1)
        painter.setPen(pen)
        for hour in range(HOURS_IN_DAY + 1):
            y = hour * HOUR_HEIGHT
            painter.drawLine(0, y, self.width(), y)
