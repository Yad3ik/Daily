"""Панель «Сегодня в календаре» на вкладке задач."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout

from src.back.structures import Event
from src.config import TAGS


def _events_title(count: int) -> str:
    """Склонение: «N событие/события/событий сегодня»."""
    n = count % 100
    if 11 <= n <= 14:
        word = "событий"
    else:
        rem = count % 10
        if rem == 1:
            word = "событие"
        elif 2 <= rem <= 4:
            word = "события"
        else:
            word = "событий"
    return f"{count} {word} сегодня"


class _TodayEventRow(QFrame):
    """Компактная строка: время, цветная полоска, название."""

    def __init__(self, event: Event) -> None:
        """Строит разметку из Event."""
        super().__init__()
        self.setObjectName("todayEventRow")
        self.setFixedHeight(34)
        color = event.color or TAGS.get(event.tag or "", "#8E8794")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        time_lbl = QLabel(event.start.strftime("%H:%M"))
        time_lbl.setObjectName("todayEventTime")
        time_lbl.setFixedWidth(40)
        time_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        bar = QFrame()
        bar.setObjectName("todayEventBar")
        bar.setFixedSize(3, 22)
        bar.setStyleSheet(
            f"QFrame#todayEventBar {{ background-color: {color}; border-radius: 2px; }}"
        )

        self._full_title = event.description
        self._title_lbl = QLabel(self._full_title)
        self._title_lbl.setObjectName("todayEventTitle")
        self._title_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        layout.addWidget(time_lbl)
        layout.addWidget(bar)
        layout.addWidget(self._title_lbl, 1)

    def resizeEvent(self, event) -> None:
        """Обрезает длинное название."""
        super().resizeEvent(event)
        self._elide_title()

    def showEvent(self, event) -> None:
        """Первичная обрезка названия."""
        super().showEvent(event)
        self._elide_title()

    def _elide_title(self) -> None:
        """ElideRight для _title_lbl."""
        w = self._title_lbl.width()
        if w <= 0:
            return
        self._title_lbl.setText(
            self._title_lbl.fontMetrics().elidedText(
                self._full_title, Qt.ElideRight, w
            )
        )


class TodayEventsPanel(QFrame):
    """Карточка со списком событий на сегодня (до 4 шт.)."""

    def __init__(self) -> None:
        """Заголовок, счётчик и список строк."""
        super().__init__()
        self.setObjectName("todayEventsPanel")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 12)
        root.setSpacing(10)

        caption = QLabel("СЕГОДНЯ В КАЛЕНДАРЕ")
        caption.setObjectName("todayEventsCaption")
        root.addWidget(caption)

        header = QHBoxLayout()
        header.setSpacing(6)
        header.setContentsMargins(0, 0, 0, 0)

        self._title = QLabel(_events_title(0))
        self._title.setObjectName("todayEventsTitle")

        dot = QLabel("●")
        dot.setObjectName("todayEventsDot")

        header.addWidget(self._title)
        header.addWidget(dot)
        header.addStretch(1)
        root.addLayout(header)

        self._list_host = QVBoxLayout()
        self._list_host.setSpacing(8)
        self._list_host.setContentsMargins(0, 0, 0, 0)
        root.addLayout(self._list_host)

        self._empty = QLabel("Нет событий")
        self._empty.setObjectName("todayEventsEmpty")
        self._empty.setVisible(False)
        root.addWidget(self._empty)

    def set_events(self, events: list[Event]) -> None:
        """Перестраивает список; пустое — «Нет событий»."""
        while self._list_host.count():
            item = self._list_host.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sorted_events = sorted(events, key=lambda e: e.start)
        self._title.setText(_events_title(len(sorted_events)))
        self._empty.setVisible(not sorted_events)

        for event in sorted_events[:4]:
            self._list_host.addWidget(_TodayEventRow(event))
