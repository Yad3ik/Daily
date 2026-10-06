"""Поле ввода с иконкой для форм auth."""

from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton


class AuthInput(QFrame):
    """Иконка + QLineEdit; для пароля — кнопка «глаз»."""

    def __init__(self, asserts_dir: Path, placeholder: str, icon_name: str, password=False):
        """password=True включает EchoMode и кнопку показа."""
        super().__init__()
        self.setObjectName("inputFrame")
        self.setFixedHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 12, 0)
        layout.setSpacing(14)

        icon = QLabel()
        icon.setObjectName("inputIcon")
        icon.setFixedSize(26, 26)
        icon_path = asserts_dir / "icons" / icon_name
        icon.setPixmap(QPixmap(str(icon_path)).scaled(26, 26, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.line_edit = QLineEdit()
        self.line_edit.setObjectName("innerInput")
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setFrame(False)
        if password:
            self.line_edit.setEchoMode(QLineEdit.Password)

        layout.addWidget(icon)
        layout.addWidget(self.line_edit, 1)

        if password:
            eye = QPushButton()
            eye.setObjectName("eyeButton")
            eye.setIcon(QIcon(str(asserts_dir / "icons" / "eye.png")))
            eye.setIconSize(QSize(26, 26))
            eye.setFixedSize(34, 34)
            eye.setCursor(Qt.PointingHandCursor)
            eye.clicked.connect(self.toggle_password)
            layout.addWidget(eye)

    def text(self):
        """Текст из line_edit."""
        return self.line_edit.text()

    def toggle_password(self):
        """Переключает видимость пароля."""
        mode = self.line_edit.echoMode()
        self.line_edit.setEchoMode(
            QLineEdit.Normal if mode == QLineEdit.Password else QLineEdit.Password
        )
