from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from .nav_icons import CalendarNavIcon, CheckSquareIcon


class ViewSwitcher(QFrame):
    view_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("viewSwitcherWrap")
        self._buttons: dict[str, QPushButton] = {}
        self._icons: dict[str, QFrame] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        for key, label in (("calendar", "Календарь"), ("tasks", "Задачи")):
            btn = QPushButton()
            btn.setObjectName("viewSwitchBtn")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _=False, k=key: self._select(k))

            inner = QHBoxLayout(btn)
            inner.setContentsMargins(12, 10, 14, 10)
            inner.setSpacing(8)

            icon = CalendarNavIcon(18, False) if key == "calendar" else CheckSquareIcon(18, False)
            inner.addWidget(icon)
            lbl = QLabel(label)
            lbl.setObjectName("viewSwitchLabel")
            inner.addWidget(lbl)

            self._icons[key] = icon
            self._buttons[key] = btn
            layout.addWidget(btn, 1)

        self.set_active("calendar")

    def _select(self, key: str) -> None:
        self.set_active(key)
        self.view_changed.emit(key)

    def set_active(self, key: str) -> None:
        for name, btn in self._buttons.items():
            active = name == key
            btn.setProperty("active", "true" if active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            icon = self._icons[name]
            if hasattr(icon, "_active"):
                icon._active = active
                icon.update()
