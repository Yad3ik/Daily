"""Заголовок вкладки задач."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class TasksHeader(QFrame):
    """«Задачи» и бейдж с общим числом."""

    def __init__(self) -> None:
        """Заголовок «Задачи» и бейдж счётчика."""
        super().__init__()
        self.setObjectName("tasksHeader")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self._title = QLabel("Задачи")
        self._title.setObjectName("tasksTitle")

        self._badge = QLabel("0")
        self._badge.setObjectName("countBadge")
        self._badge.setAlignment(Qt.AlignCenter)
        self._badge.setFixedHeight(26)

        layout.addWidget(self._title)
        layout.addWidget(self._badge)
        layout.addStretch(1)

    def set_count(self, count: int) -> None:
        """Обновляет бейдж; скрывает при count == 0."""
        self._badge.setText(str(count))
        self._badge.setVisible(count > 0)
