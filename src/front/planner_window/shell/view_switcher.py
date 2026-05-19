from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

_ICONS = Path(__file__).resolve().parents[1] / "asserts" / "icons"


class _NavIcon(QLabel):
    def __init__(self, name: str, *, active: bool = False, size: int = 24) -> None:
        super().__init__()
        self._name = name
        self._active = active
        self._size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self._apply()

    def set_active(self, active: bool) -> None:
        self._active = active
        self._apply()

    def _apply(self) -> None:
        if self._name == "calendar":
            path = _ICONS / ("calendar_active.png" if self._active else "calendar.png")
        else:
            path = _ICONS / ("tasks_active.png" if self._active else "tasks.png")
        if not path.exists():
            self.clear()
            return
        pix = QPixmap(str(path)).scaled(
            self._size,
            self._size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.setPixmap(pix)


class ViewSwitcher(QFrame):
    view_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("viewSwitcherWrap")
        self._buttons: dict[str, QPushButton] = {}
        self._icons: dict[str, _NavIcon] = {}
        self._labels: dict[str, QLabel] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for key, label in (("calendar", "Календарь"), ("tasks", "Задачи")):
            btn = QPushButton()
            btn.setObjectName("viewSwitchBtn")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(52)
            btn.clicked.connect(lambda _=False, k=key: self._select(k))

            inner = QHBoxLayout(btn)
            inner.setContentsMargins(16, 0, 18, 0)
            inner.setSpacing(12)

            icon = _NavIcon(key, active=False, size=26)
            inner.addWidget(icon)
            lbl = QLabel(label)
            lbl.setObjectName("viewSwitchLabel")
            lbl.setProperty("active", "false")
            lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            inner.addWidget(lbl, 1)

            self._icons[key] = icon
            self._labels[key] = lbl
            self._buttons[key] = btn
            layout.addWidget(btn)

        self.set_active("calendar")

    def _select(self, key: str) -> None:
        self.set_active(key)
        self.view_changed.emit(key)

    def set_active(self, key: str) -> None:
        for name, btn in self._buttons.items():
            active = name == key
            flag = "true" if active else "false"
            btn.setProperty("active", flag)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            lbl = self._labels[name]
            lbl.setProperty("active", flag)
            lbl.style().unpolish(lbl)
            lbl.style().polish(lbl)
            self._icons[name].set_active(active)
