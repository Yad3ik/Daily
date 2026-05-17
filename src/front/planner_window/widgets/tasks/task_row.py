from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from src.back.structures import Task
from src.back.to_front.todo import delete_task, set_complete


class TaskRow(QFrame):
    def __init__(self, task: Task, on_changed) -> None:
        super().__init__()
        self.setObjectName("taskRow")
        self._task = task
        self._on_changed = on_changed
        self.setFixedHeight(52)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(12)

        self._check = QPushButton("✓" if task.is_complete else "")
        self._check.setObjectName("taskCheck")
        self._check.setProperty("checked", "true" if task.is_complete else "false")
        self._check.setFixedSize(22, 22)
        self._check.setCursor(Qt.PointingHandCursor)
        self._check.clicked.connect(self._toggle)

        self._label = QLabel(task.name)
        self._label.setObjectName("taskRowLabel")
        self._label.setProperty("completed", "true" if task.is_complete else "false")
        self._label.style().unpolish(self._label)
        self._label.style().polish(self._label)

        self._delete = QPushButton("Удалить")
        self._delete.setObjectName("taskDelete")
        self._delete.setCursor(Qt.PointingHandCursor)
        self._delete.hide()
        self._delete.clicked.connect(self._remove)

        layout.addWidget(self._check)
        layout.addWidget(self._label, 1)
        layout.addWidget(self._delete)

    def _toggle(self) -> None:
        set_complete(self._task.id, not self._task.is_complete)
        self._on_changed()

    def _remove(self) -> None:
        delete_task(self._task.id)
        self._on_changed()

    def enterEvent(self, event) -> None:
        self._delete.show()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._delete.hide()
        super().leaveEvent(event)
