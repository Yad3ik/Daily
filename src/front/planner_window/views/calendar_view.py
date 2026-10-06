"""Вид недельного календаря."""

from collections import Counter
from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from src.back.db.exceptions import AuthError
from src.back.structures import Event
from src.back.to_front.events import delete_event, get_events
from src.config import TAGS

from ..calendar_state import CalendarState
from ..widgets.calendar.add_event_dialog import AddEventDialog
from ..widgets.calendar.confirm_dialog import ConfirmDialog
from ..widgets.calendar.week_grid import WeekGrid
from ..widgets.calendar.week_header import WeekHeader
from .base_view import BaseView


class CalendarView(BaseView):
    """Вид недельного календаря с сеткой событий."""

    def __init__(self, state: CalendarState, on_tags_updated=None) -> None:
        """Собирает шапку недели и WeekGrid."""
        super().__init__()
        self.setObjectName("calendarView")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._state = state
        self._on_tags_updated = on_tags_updated

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self._header = WeekHeader(state)
        self._grid = WeekGrid(state, on_event_clicked=self._on_event_clicked)
        self._header.week_changed.connect(self.refresh)
        self._header.add_event_requested.connect(self._open_add_dialog)

        layout.addWidget(self._header)
        layout.addWidget(self._grid, 1)

    def _open_add_dialog(self) -> None:
        """Открывает диалог создания события."""
        dialog = AddEventDialog(self._state, self)
        if dialog.exec_():
            self.refresh()

    def _on_event_clicked(self, event: Event) -> None:
        """Подтверждение и удаление события по клику."""
        dialog = ConfirmDialog("Удалить событие?", self)
        if dialog.exec_() != dialog.Accepted:
            return
        res = delete_event(event.id)
        if res.status_code == 200:
            self.refresh()

    def refresh(self) -> None:
        """Загружает события недели и обновляет теги в сайдбаре."""
        days = self._state.week_days
        if not days:
            return
        try:
            events_by_day = get_events(days[0], days[-1])
        except (AuthError, RuntimeError):
            events_by_day = [[] for _ in range(len(days))]

        self._header.refresh()
        self._grid.set_events_by_day(events_by_day)
        if date.today() in days:
            self._grid.scroll_to_now()

        counts: Counter[str] = Counter()
        for day_events in events_by_day:
            for event in day_events:
                if event.tag:
                    counts[event.tag] += 1
        tag_counts = {tag: counts.get(tag, 0) for tag in TAGS}
        if self._on_tags_updated:
            self._on_tags_updated(tag_counts)
