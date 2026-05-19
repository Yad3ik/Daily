from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from src.back.db.exceptions import AuthError
from src.back.to_front.events import get_events
from src.back.to_front.todo import _update_tasks
from src.session import Me

from ..calendar_state import CalendarState
from ..widgets.tasks.network_errors import NETWORK_ERRORS
from ..widgets.tasks.progress_ring import ProgressRing
from ..widgets.tasks.task_filters import TaskFilters
from ..widgets.tasks.task_input import TaskInput
from ..widgets.tasks.task_section import TaskSection
from ..widgets.tasks.tasks_header import TasksHeader
from ..widgets.tasks.today_events_panel import TodayEventsPanel
from ..widgets.tasks.week_overview import WeekOverview
from .base_view import BaseView


class TasksView(BaseView):
    def __init__(
        self,
        calendar_state: CalendarState,
    ) -> None:
        super().__init__()
        self.setObjectName("tasksView")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._state = calendar_state
        self._filter = "all"

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(24)

        main = QVBoxLayout()
        main.setSpacing(18)

        self._header = TasksHeader()
        self._input = TaskInput(self.refresh)
        self._filters = TaskFilters(self._on_filter_changed)
        self._progress = ProgressRing()

        tools = QHBoxLayout()
        tools.setSpacing(16)
        tools.addWidget(self._progress)
        tools.addWidget(self._filters, 1)

        scroll = QScrollArea()
        scroll.setObjectName("tasksScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.viewport().setAutoFillBackground(False)

        scroll_body = QWidget()
        scroll_body.setObjectName("tasksScrollBody")
        scroll_body.setAttribute(Qt.WA_StyledBackground, True)
        self._sections_layout = QVBoxLayout(scroll_body)
        self._sections_layout.setContentsMargins(0, 0, 8, 0)
        self._sections_layout.setSpacing(20)
        scroll.setWidget(scroll_body)

        self._active_section = TaskSection("В РАБОТЕ", completed=False)
        self._done_section = TaskSection("ВЫПОЛНЕНО", completed=True)
        self._sections_layout.addWidget(self._active_section)
        self._sections_layout.addWidget(self._done_section)
        self._sections_layout.addStretch(1)

        main.addWidget(self._header)
        main.addWidget(self._input)
        main.addLayout(tools)
        main.addWidget(scroll, 1)

        side = QVBoxLayout()
        side.setSpacing(16)
        self._week_overview = WeekOverview()
        self._today_panel = TodayEventsPanel()
        side.addWidget(self._week_overview)
        side.addWidget(self._today_panel)
        side.addStretch(1)

        side_wrap = QFrame()
        side_wrap.setObjectName("tasksSidePanel")
        side_wrap.setFixedWidth(340)
        side_wrap.setLayout(side)

        root.addLayout(main, 1)
        root.addWidget(side_wrap)

    def _on_filter_changed(self, key: str) -> None:
        self._filter = key
        self.refresh()

    def refresh(self) -> None:
        try:
            _update_tasks()
        except (*NETWORK_ERRORS, AuthError, RuntimeError):
            pass

        tasks = list(Me.Tasks or []) if Me.Tasks is not None else []
        total = len(tasks)
        done = sum(1 for t in tasks if t.is_complete)
        active = [t for t in tasks if not t.is_complete]
        completed = [t for t in tasks if t.is_complete]

        self._header.set_count(total)
        self._progress.set_values(done, total)

        if self._filter == "active":
            show_active, show_done = active, []
        elif self._filter == "completed":
            show_active, show_done = [], completed
        else:
            show_active, show_done = active, completed

        self._active_section.set_tasks(show_active, self.refresh)
        self._done_section.set_tasks(show_done, self.refresh)
        self._active_section.setVisible(bool(show_active) or self._filter != "completed")
        self._done_section.setVisible(bool(show_done) or self._filter != "active")

        self._refresh_side_panels()

    def _refresh_side_panels(self) -> None:
        days = self._state.week_days
        event_counts: dict[date, int] = {day: 0 for day in days}
        today_events: list = []

        try:
            events_by_day = get_events(days[0], days[-1])
            for day, day_events in zip(days, events_by_day):
                event_counts[day] = len(day_events)
            today = date.today()
            if today in days:
                today_events = events_by_day[days.index(today)]
            else:
                today_lists = get_events(today, today)
                today_events = today_lists[0] if today_lists else []
        except (*NETWORK_ERRORS, AuthError, RuntimeError):
            pass

        self._week_overview.set_week(days, event_counts)
        self._today_panel.set_events(today_events)
