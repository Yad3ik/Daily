from datetime import date, datetime, time

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from src.back.to_front.events import add_new_event
from src.config import TAGS

from ...calendar_state import CalendarState


class AddEventDialog(QDialog):
    def __init__(self, state: CalendarState, parent=None) -> None:
        super().__init__(parent)
        self._state = state
        self.setObjectName("addEventDialog")
        self.setWindowTitle("Новое событие")
        self.setModal(True)
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Добавить событие")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)

        self._name = QLineEdit()
        self._name.setObjectName("dialogField")
        self._name.setPlaceholderText("Название события")

        self._date = QDateEdit()
        self._date.setObjectName("dialogField")
        self._date.setCalendarPopup(True)
        self._date.setDisplayFormat("dd.MM.yyyy")
        self._date.setDate(QDate.currentDate())

        self._start = QLineEdit("09:00")
        self._start.setObjectName("dialogField")
        self._start.setPlaceholderText("ЧЧ:ММ")

        self._end = QLineEdit("10:00")
        self._end.setObjectName("dialogField")
        self._end.setPlaceholderText("ЧЧ:ММ")

        self._tag = QComboBox()
        self._tag.setObjectName("dialogField")
        for tag_name in TAGS:
            self._tag.addItem(tag_name, tag_name)

        form.addRow("Название", self._name)
        form.addRow("Дата", self._date)
        form.addRow("Начало", self._start)
        form.addRow("Конец", self._end)
        form.addRow("Тег", self._tag)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setObjectName("primaryButton")
        buttons.accepted.connect(self._try_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _parse_time(self, text: str) -> time | None:
        text = text.strip()
        try:
            parts = text.split(":")
            if len(parts) != 2:
                return None
            h, m = int(parts[0]), int(parts[1])
            if 0 <= h <= 23 and 0 <= m <= 59:
                return time(h, m)
        except ValueError:
            return None
        return None

    def _try_accept(self) -> None:
        name = self._name.text().strip()
        if not name:
            return
        start_t = self._parse_time(self._start.text())
        end_t = self._parse_time(self._end.text())
        if start_t is None or end_t is None:
            return

        qd = self._date.date()
        event_date = date(qd.year(), qd.month(), qd.day())
        start_dt = datetime.combine(event_date, start_t)
        end_dt = datetime.combine(event_date, end_t)
        if end_dt <= start_dt:
            return

        tag = self._tag.currentData()
        res = add_new_event(event_date, start_dt, end_dt, name, tag=tag)
        if res.status_code == 200:
            self.accept()
