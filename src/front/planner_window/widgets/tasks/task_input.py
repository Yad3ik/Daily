from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from src.back.to_front.todo import add_new_task


class TaskInput(QFrame):
    def __init__(self, on_added) -> None:
        super().__init__()
        self.setObjectName("taskInputWrap")
        self._on_added = on_added
        self.setFixedHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 12, 0)
        layout.setSpacing(12)

        plus = QLabel("+")
        plus.setStyleSheet("color: #6f6875; font-size: 20px; border: 1px dashed #4a4354; border-radius: 14px;")
        plus.setFixedSize(28, 28)
        plus.setAlignment(Qt.AlignCenter)

        field_wrap = QVBoxLayout()
        field_wrap.setSpacing(0)
        self._field = QLineEdit()
        self._field.setObjectName("taskInputField")
        self._field.setPlaceholderText("Что хочешь сделать?")
        self._field.returnPressed.connect(self._submit)
        hint = QLabel("Введи задачу и нажми Enter")
        hint.setObjectName("taskInputHint")
        field_wrap.addWidget(self._field)

        enter = QPushButton("Enter")
        enter.setObjectName("enterChip")
        enter.setCursor(Qt.PointingHandCursor)
        enter.clicked.connect(self._submit)

        layout.addWidget(plus)
        layout.addLayout(field_wrap, 1)
        layout.addWidget(enter)

    def _submit(self) -> None:
        text = self._field.text().strip()
        if not text:
            return
        add_new_task(text)
        self._field.clear()
        self._on_added()
