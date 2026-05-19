"""Поле ввода новой задачи."""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from src.back.to_front.todo import add_new_task

from .network_errors import NETWORK_ERRORS


class TaskInput(QFrame):
    """Строка «+», поле и кнопка «Добавить»."""

    def __init__(self, on_added) -> None:
        """on_added вызывается после успешного add_new_task."""
        super().__init__()
        self.setObjectName("taskInputWrap")
        self._on_added = on_added
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 14, 0)
        layout.setSpacing(12)

        plus = QLabel("+")
        plus.setObjectName("taskInputPlus")
        plus.setFixedSize(32, 32)
        plus.setAlignment(Qt.AlignCenter)

        field_wrap = QVBoxLayout()
        field_wrap.setSpacing(0)
        self._field = QLineEdit()
        self._field.setObjectName("taskInputField")
        self._default_placeholder = "Что хочешь сделать?"
        self._field.setPlaceholderText(self._default_placeholder)
        self._field.returnPressed.connect(self._submit)
        field_wrap.addWidget(self._field)

        add_btn = QPushButton("Добавить")
        add_btn.setObjectName("taskAddButton")
        add_btn.setFlat(True)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self._submit)

        layout.addWidget(plus)
        layout.addLayout(field_wrap, 1)
        layout.addWidget(add_btn)

    def _submit(self) -> None:
        """Отправляет задачу на сервер; при ошибке сети — placeholder."""
        text = self._field.text().strip()
        if not text:
            return
        try:
            res = add_new_task(text)
        except NETWORK_ERRORS:
            self._show_error("Нет связи с сервером. Попробуйте позже.")
            return
        if res.status_code != 200:
            self._show_error("Не удалось сохранить задачу")
            return
        self._field.clear()
        self._on_added()

    def _show_error(self, message: str) -> None:
        """Временно показывает ошибку в placeholder."""
        self._field.setPlaceholderText(message)
        QTimer.singleShot(3000, self._reset_placeholder)

    def _reset_placeholder(self) -> None:
        """Возвращает стандартный placeholder."""
        self._field.setPlaceholderText(self._default_placeholder)
