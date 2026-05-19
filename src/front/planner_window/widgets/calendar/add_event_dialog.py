"""Диалог создания события (безрамочный, с тегами)."""

from datetime import date, datetime, time
from pathlib import Path

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import (
    QButtonGroup,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.back.to_front.events import add_new_event
from src.config import TAGS
from src.front.common.widgets import TitleBar

from ...calendar_state import CalendarState

_PLANNER_DIR = Path(__file__).resolve().parents[2]
_AUTH_QSS = _PLANNER_DIR.parent / "auth_window" / "auth_styles.qss"
_PLANNER_QSS = _PLANNER_DIR / "planner_styles.qss"


class _TagChip(QPushButton):
    """Переключаемая кнопка-тег с цветной рамкой."""

    def __init__(self, name: str, color: str, group: QButtonGroup) -> None:
        """Добавляется в QButtonGroup как checkable chip."""
        super().__init__(name)
        self._tag_name = name
        self._color = color
        self.setObjectName("dialogTagChip")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        group.addButton(self)
        self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked: bool) -> None:
        """Подсвечивает выбранный тег цветом."""
        if checked:
            self.setStyleSheet(
                f"QPushButton#dialogTagChip {{"
                f" background-color: #1e1c26;"
                f" border: 1px solid {self._color};"
                f" border-radius: 18px;"
                f" color: #F6F0F4;"
                f" padding: 8px 16px;"
                f" font-size: 13px;"
                f"}}"
            )
        else:
            self.setStyleSheet("")


class AddEventDialog(QDialog):
    """Форма: название, дата, время, тег; сохранение через add_new_event."""

    def __init__(self, state: CalendarState, parent=None) -> None:
        """Собирает UI и центрирует относительно parent."""
        super().__init__(parent)
        self._state = state
        self.setObjectName("addEventDialog")
        self.setWindowTitle("Новое событие")
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(420, 520)

        self._apply_styles()
        self._build_ui()

        if parent is not None:
            parent_geo = parent.frameGeometry()
            self.move(
                parent_geo.center().x() - self.width() // 2,
                parent_geo.center().y() - self.height() // 2,
            )

    def _apply_styles(self) -> None:
        """Подключает QSS auth + planner."""
        auth_qss = _AUTH_QSS.read_text(encoding="utf-8")
        planner_qss = _PLANNER_QSS.read_text(encoding="utf-8")
        self.setStyleSheet(auth_qss + "\n" + planner_qss)

    @staticmethod
    def _caption(text: str) -> QLabel:
        """Подпись поля в верхнем регистре."""
        label = QLabel(text.upper())
        label.setObjectName("dialogFieldCaption")
        return label

    def _add_field(self, layout: QVBoxLayout, caption: str, widget: QWidget) -> None:
        """Добавляет caption + виджет в layout."""
        layout.addWidget(self._caption(caption))
        layout.addWidget(widget)

    def _build_ui(self) -> None:
        """Поля формы, чипы тегов и кнопки Добавить/Отмена."""
        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        surface = QFrame()
        surface.setObjectName("windowSurface")
        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(0, 0, 0, 0)
        surface_layout.setSpacing(0)

        bar_title = '<b><span style="color:#F03F83;">Daily</span></b> · Событие'
        surface_layout.addWidget(TitleBar(self, bar_title))

        body = QFrame()
        body.setObjectName("addEventDialogBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(0)

        heading = QLabel("Новое событие")
        heading.setObjectName("dialogHeading")
        layout.addWidget(heading)
        layout.addSpacing(22)

        self._name = QLineEdit()
        self._name.setObjectName("dialogField")
        self._name.setPlaceholderText("Название события")
        self._add_field(layout, "Название", self._name)
        layout.addSpacing(18)

        row = QHBoxLayout()
        row.setSpacing(14)

        date_col = QVBoxLayout()
        date_col.setSpacing(8)
        self._date = QLineEdit(date.today().strftime("%d.%m.%Y"))
        self._date.setObjectName("dialogField")
        self._date.setPlaceholderText("ДД.ММ.ГГГГ")
        date_col.addWidget(self._caption("Дата"))
        date_col.addWidget(self._date)

        start_col = QVBoxLayout()
        start_col.setSpacing(8)
        self._start = QLineEdit("09:00")
        self._start.setObjectName("dialogField")
        self._start.setPlaceholderText("ЧЧ:ММ")
        start_col.addWidget(self._caption("Начало"))
        start_col.addWidget(self._start)

        end_col = QVBoxLayout()
        end_col.setSpacing(8)
        self._end = QLineEdit("10:00")
        self._end.setObjectName("dialogField")
        self._end.setPlaceholderText("ЧЧ:ММ")
        end_col.addWidget(self._caption("Конец"))
        end_col.addWidget(self._end)

        row.addLayout(date_col, 2)
        row.addLayout(start_col, 1)
        row.addLayout(end_col, 1)
        layout.addLayout(row)
        layout.addSpacing(18)

        layout.addWidget(self._caption("Тег"))
        layout.addSpacing(8)

        tag_row = QHBoxLayout()
        tag_row.setSpacing(8)
        self._tag_group = QButtonGroup(self)
        self._tag_group.setExclusive(True)
        self._tag_chips: list[_TagChip] = []
        for tag_name, color in TAGS.items():
            chip = _TagChip(tag_name, color, self._tag_group)
            tag_row.addWidget(chip)
            self._tag_chips.append(chip)
        tag_row.addStretch(1)
        layout.addLayout(tag_row)
        if self._tag_chips:
            self._tag_chips[0].setChecked(True)

        layout.addStretch(1)
        layout.addSpacing(16)

        footer = QHBoxLayout()
        footer.setSpacing(12)
        footer.addStretch(1)

        cancel = QPushButton("Отмена")
        cancel.setObjectName("dialogCancelButton")
        cancel.setCursor(Qt.PointingHandCursor)
        cancel.clicked.connect(self.reject)

        save = QPushButton("Сохранить")
        save.setObjectName("dialogSaveButton")
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self._try_accept)

        footer.addWidget(cancel)
        footer.addWidget(save)
        layout.addLayout(footer)

        surface_layout.addWidget(body, 1)
        root.addWidget(surface)

        self._name.setFocus()

    def toggle_maximized(self) -> None:
        """Для TitleBar: развернуть/свернуть (редко используется)."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def paintEvent(self, event) -> None:
        """Скруглённый фон диалога."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)
        painter.fillPath(path, QColor("#15131a"))
        painter.setPen(QColor("#393443"))
        painter.drawPath(path)
        super().paintEvent(event)

    def _selected_tag(self) -> str | None:
        """Имя отмеченного тега или None."""
        for chip in self._tag_chips:
            if chip.isChecked():
                return chip._tag_name
        return None

    def _parse_date(self, text: str) -> date | None:
        """Парсит ДД.ММ.ГГГГ."""
        text = text.strip()
        try:
            parts = text.split(".")
            if len(parts) != 3:
                return None
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            return date(year, month, day)
        except ValueError:
            return None

    def _parse_time(self, text: str) -> time | None:
        """Парсит ЧЧ:ММ."""
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
        """Валидирует форму и вызывает add_new_event; при успехе accept()."""
        name = self._name.text().strip()
        if not name:
            return
        start_t = self._parse_time(self._start.text())
        end_t = self._parse_time(self._end.text())
        if start_t is None or end_t is None:
            return

        event_date = self._parse_date(self._date.text())
        if event_date is None:
            return
        start_dt = datetime.combine(event_date, start_t)
        end_dt = datetime.combine(event_date, end_t)
        if end_dt <= start_dt:
            return

        tag = self._selected_tag()
        res = add_new_event(event_date, start_dt, end_dt, name, tag=tag)
        if res.status_code == 200:
            self.accept()
