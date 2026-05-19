from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from src.back.structures import Task

from .task_row import TaskRow


class TaskSection(QFrame):
    def __init__(self, title: str, completed: bool) -> None:
        super().__init__()
        self.setObjectName("taskSection")
        self._completed = completed
        self._rows_layout = QVBoxLayout()
        self._rows_layout.setSpacing(8)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        header = QHBoxLayout()
        cap = QLabel(title)
        cap.setObjectName("sectionTitle")
        self._badge = QLabel("0")
        self._badge.setObjectName("sectionBadge")
        self._badge.setAlignment(Qt.AlignCenter)
        header.addWidget(cap)
        header.addWidget(self._badge)
        header.addStretch(1)

        root.addLayout(header)
        root.addLayout(self._rows_layout)

    def set_tasks(self, tasks: list[Task], on_changed) -> None:
        while self._rows_layout.count():
            item = self._rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._badge.setText(str(len(tasks)))
        for task in tasks:
            self._rows_layout.addWidget(TaskRow(task, on_changed))
