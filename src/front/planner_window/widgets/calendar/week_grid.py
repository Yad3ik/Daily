from datetime import date, datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from src.back.structures import Event

from ...calendar_state import CalendarState
from .day_column import DayColumn, DayHeaderCell
from .event_block import GRID_HEIGHT, HOUR_HEIGHT
from .time_ruler import TimeRuler


class _NowLineOverlay(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.raise_()

    def paintEvent(self, event) -> None:
        now = datetime.now()
        y = int((now.hour * 60 + now.minute) / 60 * HOUR_HEIGHT)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#F03F83"), 2)
        painter.setPen(pen)
        painter.drawLine(0, y, self.width(), y)


class WeekGrid(QFrame):
    def __init__(self, state: CalendarState) -> None:
        super().__init__()
        self.setObjectName("weekGridWrap")
        self._state = state
        self._header_cells: list[DayHeaderCell] = []
        self._day_columns: list[DayColumn] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        headers = QHBoxLayout()
        headers.setContentsMargins(56, 0, 0, 0)
        headers.setSpacing(0)
        for day in state.week_days:
            cell = DayHeaderCell(day)
            headers.addWidget(cell, 1)
            self._header_cells.append(cell)
        outer.addLayout(headers)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QFrame.NoFrame)

        scroll_body = QWidget()
        scroll_body.setMinimumHeight(GRID_HEIGHT)
        body_layout = QHBoxLayout(scroll_body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._ruler = TimeRuler()
        body_layout.addWidget(self._ruler)

        cols_host = QWidget()
        cols_host.setMinimumHeight(GRID_HEIGHT)
        cols_layout = QHBoxLayout(cols_host)
        cols_layout.setContentsMargins(0, 0, 0, 0)
        cols_layout.setSpacing(0)

        self._day_columns = [DayColumn() for _ in range(7)]
        for col in self._day_columns:
            cols_layout.addWidget(col, 1)

        body_layout.addWidget(cols_host, 1)
        self._scroll.setWidget(scroll_body)
        outer.addWidget(self._scroll, 1)

        self._overlay_host = cols_host
        self._now_line = _NowLineOverlay(cols_host)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "_overlay_host"):
            self._now_line.setGeometry(0, 0, self._overlay_host.width(), GRID_HEIGHT)

    def set_events_by_day(self, events_by_day: list[list[Event]]) -> None:
        days = self._state.week_days
        for day, col, header, day_events in zip(
            days, self._day_columns, self._header_cells, events_by_day
        ):
            header.set_day(day)
            col.set_day(day, day_events)
        self._now_line.update()
        self._scroll_to_morning()

    def _scroll_to_morning(self) -> None:
        """Default scroll position: ~07:00 like the mockup."""
        self._scroll.verticalScrollBar().setValue(7 * HOUR_HEIGHT)

    def scroll_to_now(self) -> None:
        now = datetime.now()
        y = int((now.hour * 60 + now.minute) / 60 * HOUR_HEIGHT)
        self._scroll.verticalScrollBar().setValue(max(0, y - self._scroll.height() // 3))
