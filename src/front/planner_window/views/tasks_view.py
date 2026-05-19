from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from src.back.to_front.todo import update_me_tasks
from src.session import Me

from ..widgets.tasks.progress_ring import ProgressRing
from ..widgets.tasks.task_filters import TaskFilters
from ..widgets.tasks.task_input import TaskInput
from ..widgets.tasks.task_section import TaskSection
from ..widgets.tasks.tasks_header import TasksHeader
from .base_view import BaseView


class TasksView(BaseView):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("tasksView")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._filter = "all"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

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

        layout.addWidget(self._header)
        layout.addWidget(self._input)
        layout.addLayout(tools)
        layout.addWidget(scroll, 1)

    def _on_filter_changed(self, key: str) -> None:
        self._filter = key
        self.refresh()

    def refresh(self) -> None:
        update_me_tasks()

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
