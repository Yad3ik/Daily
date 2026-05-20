"""Сетка недели: заголовки дней, шкала времени и колонки событий."""

from collections.abc import Callable
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
    """Розовая линия текущего времени поверх колонок."""

    def __init__(self, parent: QWidget) -> None:
        """Прозрачный оверлей без перехвата мыши."""
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.raise_()

    def paintEvent(self, event) -> None:
        """Рисует горизонтальную линию «сейчас»."""
        now = datetime.now()
        y = int((now.hour * 60 + now.minute) / 60 * HOUR_HEIGHT)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#F03F83"), 2)
        painter.setPen(pen)
        painter.drawLine(0, y, self.width(), y)


class WeekGrid(QFrame):
    """Прокручиваемая недельная сетка с 7 колонками."""

    def __init__(
        self,
        state: CalendarState,
        on_event_clicked: Callable[[Event], None] | None = None,
    ) -> None:
        """Шапка дней, TimeRuler и DayColumn на каждый день."""
        super().__init__()
        self.setObjectName("weekGridWrap")
        self._state = state
        self._on_event_clicked = on_event_clicked
        self._header_cells: list[DayHeaderCell] = []
        self._day_columns: list[DayColumn] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        headers = QHBoxLayout()
        headers.setContentsMargins(64, 0, 0, 0)
        headers.setSpacing(0)
        for day in state.week_days:
            cell = DayHeaderCell(day)
            headers.addWidget(cell, 1)
            self._header_cells.append(cell)
        outer.addLayout(headers)

        self._scroll = QScrollArea()
        self._scroll.setObjectName("weekGridScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.viewport().setAutoFillBackground(False)

        scroll_body = QWidget()
        scroll_body.setObjectName("weekGridScrollBody")
        scroll_body.setAttribute(Qt.WA_StyledBackground, True)
        scroll_body.setMinimumHeight(GRID_HEIGHT)
        body_layout = QHBoxLayout(scroll_body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._ruler = TimeRuler()
        body_layout.addWidget(self._ruler)

        cols_host = QWidget()
        cols_host.setObjectName("weekGridCols")
        cols_host.setAttribute(Qt.WA_StyledBackground, True)
        cols_host.setMinimumHeight(GRID_HEIGHT)
        cols_layout = QHBoxLayout(cols_host)
        cols_layout.setContentsMargins(0, 0, 0, 0)
        cols_layout.setSpacing(0)

        self._day_columns = [
            DayColumn(on_event_clicked=on_event_clicked) for _ in range(7)
        ]
        for col in self._day_columns:
            cols_layout.addWidget(col, 1)

        body_layout.addWidget(cols_host, 1)
        self._scroll.setWidget(scroll_body)
        outer.addWidget(self._scroll, 1)

        self._overlay_host = cols_host
        self._now_line = _NowLineOverlay(cols_host)

    def resizeEvent(self, event) -> None:
        """Подгоняет геометрию линии «сейчас»."""
        super().resizeEvent(event)
        if hasattr(self, "_overlay_host"):
            self._now_line.setGeometry(0, 0, self._overlay_host.width(), GRID_HEIGHT)

    def set_events_by_day(self, events_by_day: list[list[Event]]) -> None:
        """Заполняет колонки событиями и обновляет оверлей."""
        days = self._state.week_days
        for day, col, header, day_events in zip(
            days, self._day_columns, self._header_cells, events_by_day
        ):
            header.set_day(day)
            col.set_day(day, day_events)
        self._now_line.update()
        self._scroll_to_morning()

    def _scroll_to_morning(self) -> None:
        """Прокрутка к ~07:00 по умолчанию."""
        self._scroll.verticalScrollBar().setValue(7 * HOUR_HEIGHT)

    def scroll_to_now(self) -> None:
        """Прокручивает так, чтобы текущее время было в зоне видимости."""
        now = datetime.now()
        y = int((now.hour * 60 + now.minute) / 60 * HOUR_HEIGHT)
        self._scroll.verticalScrollBar().setValue(max(0, y - self._scroll.height() // 3))
