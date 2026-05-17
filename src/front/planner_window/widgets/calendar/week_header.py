from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from ...calendar_state import CalendarState

_MONTHS = (
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
)


def format_week_range(state: CalendarState) -> str:
    days = state.week_days
    start, end = days[0], days[-1]
    if start.month == end.month:
        return f"{start.day} — {end.day} {_MONTHS[end.month - 1]} {end.year}"
    return (
        f"{start.day} {_MONTHS[start.month - 1]} — "
        f"{end.day} {_MONTHS[end.month - 1]} {end.year}"
    )


class WeekHeader(QFrame):
    week_changed = pyqtSignal()
    add_event_requested = pyqtSignal()

    def __init__(self, state: CalendarState) -> None:
        super().__init__()
        self.setObjectName("weekHeaderBar")
        self._state = state

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(12)

        nav_left = QPushButton("‹")
        nav_left.setObjectName("navButton")
        nav_left.setFixedSize(40, 40)
        nav_left.setCursor(Qt.PointingHandCursor)
        nav_left.clicked.connect(lambda: self._shift(-1))

        self._range_label = QLabel()
        self._range_label.setObjectName("weekRangeLabel")
        self._range_label.setAlignment(Qt.AlignCenter)

        nav_right = QPushButton("›")
        nav_right.setObjectName("navButton")
        nav_right.setFixedSize(40, 40)
        nav_right.setCursor(Qt.PointingHandCursor)
        nav_right.clicked.connect(lambda: self._shift(1))

        center = QHBoxLayout()
        center.addStretch(1)
        center.addWidget(nav_left)
        center.addWidget(self._range_label)
        center.addWidget(nav_right)
        center.addStretch(1)

        add_btn = QPushButton("+  Событие")
        add_btn.setObjectName("primaryButton")
        add_btn.setFixedHeight(42)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_event_requested.emit)

        layout.addLayout(center, 1)
        layout.addWidget(add_btn)
        self.refresh()

    def _shift(self, weeks: int) -> None:
        self._state.shift_week(weeks)
        self.refresh()
        self.week_changed.emit()

    def refresh(self) -> None:
        self._range_label.setText(format_week_range(self._state))
