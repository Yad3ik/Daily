from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

_DAY_NAMES = ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")


class _DayCell(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("weekDayCell")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(8)
        self.setMinimumHeight(72)
        layout.setAlignment(Qt.AlignCenter)

        self._name = QLabel()
        self._name.setObjectName("weekDayName")
        self._name.setAlignment(Qt.AlignCenter)

        self._num = QLabel()
        self._num.setObjectName("weekDayNumber")
        self._num.setAlignment(Qt.AlignCenter)

        self._dot = QLabel()
        self._dot.setObjectName("weekDayDot")
        self._dot.setFixedSize(8, 8)
        self._dot.setAlignment(Qt.AlignCenter)

        layout.addWidget(self._name)
        layout.addWidget(self._num)
        layout.addWidget(self._dot, 0, Qt.AlignCenter)

    def set_day(self, day: date, *, has_events: bool) -> None:
        self._name.setText(_DAY_NAMES[day.weekday()])
        self._num.setText(str(day.day))
        today = date.today()
        is_today = day == today
        self.setProperty("today", "true" if is_today else "false")
        self.setProperty("hasEvents", "false")
        self._dot.setProperty("today", "true" if is_today else "false")
        self._dot.setProperty("hasEvents", "true" if has_events else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self._dot.style().unpolish(self._dot)
        self._dot.style().polish(self._dot)


class WeekOverview(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("weekOverview")
        self._cells: list[_DayCell] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(14)

        title = QLabel("НЕДЕЛЯ")
        title.setObjectName("weekOverviewTitle")
        root.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(8)
        for _ in range(7):
            cell = _DayCell()
            row.addWidget(cell, 1)
            self._cells.append(cell)
        root.addLayout(row)

    def set_week(self, days: list[date], event_counts: dict[date, int]) -> None:
        for day, cell in zip(days, self._cells):
            cell.set_day(day, has_events=event_counts.get(day, 0) > 0)
