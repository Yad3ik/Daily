"""Чипы фильтра задач: все / активные / выполненные."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton


class TaskFilters(QFrame):
    """Три кнопки-фильтра с подсветкой активной."""

    def __init__(self, on_changed) -> None:
        """on_changed(key) при смене фильтра."""
        super().__init__()
        self.setObjectName("taskFilters")
        self._on_changed = on_changed
        self._buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for key, label in (("all", "Все"), ("active", "Активные"), ("completed", "Выполненные")):
            btn = QPushButton(label)
            btn.setObjectName("filterChip")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _=False, k=key: self._select(k))
            layout.addWidget(btn)
            self._buttons[key] = btn
        layout.addStretch(1)
        self._select("all", notify=False)

    def _select(self, key: str, notify: bool = True) -> None:
        """Активирует chip и опционально вызывает on_changed."""
        for name, btn in self._buttons.items():
            btn.setProperty("active", "true" if name == key else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        if notify:
            self._on_changed(key)
