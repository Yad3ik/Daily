from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
)

from .input_field import AuthInput


class FormPage(QFrame):
    def __init__(
        self,
        asserts_dir: Path,
        title: str,
        subtitle: str,
        login_hint: str,
        password_hint: str,
        button_text: str,
        bottom_text: Optional[str] = None,
    ):
        super().__init__()
        self.setObjectName("formPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title_label = QLabel(title)
        title_label.setObjectName("formTitle")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("formSubtitle")

        login_label = QLabel("ЛОГИН")
        login_label.setObjectName("fieldLabel")
        self.login_input = AuthInput(asserts_dir, login_hint, "user.png")

        password_label = QLabel("ПАРОЛЬ")
        password_label.setObjectName("fieldLabel")
        self.password_input = AuthInput(asserts_dir, password_hint, "lock.png", password=True)

        submit = QPushButton(button_text)
        submit.setObjectName("mainButton")
        submit.setFixedHeight(56)
        submit.setCursor(Qt.PointingHandCursor)

        layout.addWidget(title_label)
        layout.addSpacing(8)
        layout.addWidget(subtitle_label)
        layout.addSpacing(34)
        layout.addWidget(login_label)
        layout.addSpacing(9)
        layout.addWidget(self.login_input)
        layout.addSpacing(28)
        layout.addWidget(password_label)
        layout.addSpacing(9)
        layout.addWidget(self.password_input)
        layout.addSpacing(36)
        layout.addWidget(submit)

        if bottom_text:
            bottom = QLabel(bottom_text)
            bottom.setObjectName("bottomText")
            bottom.setAlignment(Qt.AlignCenter)
            layout.addSpacing(34)
            layout.addWidget(bottom)

        layout.addStretch(1)


class AuthCard(QFrame):
    def __init__(self, asserts_dir: Path):
        super().__init__()
        self.setObjectName("authCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 18, 26, 26)
        layout.setSpacing(0)

        tabs_wrap = QFrame()
        tabs_wrap.setObjectName("tabsWrap")
        tabs_wrap.setFixedSize(340, 48)
        tabs = QHBoxLayout(tabs_wrap)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setSpacing(0)

        self.login_tab = QPushButton("Войти")
        self.register_tab = QPushButton("Регистрация")
        for button in (self.login_tab, self.register_tab):
            button.setFixedSize(170, 48)
            button.setCursor(Qt.PointingHandCursor)

        self.login_tab.clicked.connect(self.show_login)
        self.register_tab.clicked.connect(self.show_register)
        tabs.addWidget(self.login_tab)
        tabs.addWidget(self.register_tab)

        centered_tabs = QHBoxLayout()
        centered_tabs.addStretch(1)
        centered_tabs.addWidget(tabs_wrap)
        centered_tabs.addStretch(1)

        self.stack = QStackedWidget()
        self.login_page = FormPage(
            asserts_dir,
            "С возвращением!",
            "Войдите, чтобы продолжить планировать свой день с Daily.",
            "Введите логин",
            "Введите пароль",
            "Войти",
        )
        self.register_page = FormPage(
            asserts_dir,
            "Создайте аккаунт",
            "Начните планировать свой день с Daily.",
            "Придумайте логин",
            "Придумайте пароль",
            "Создать аккаунт",
        )
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)

        layout.addLayout(centered_tabs)
        layout.addSpacing(44)
        layout.addWidget(self.stack)
        self.show_login()

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)
        self.login_tab.setProperty("active", True)
        self.register_tab.setProperty("active", False)
        self._refresh_tabs()

    def show_register(self):
        self.stack.setCurrentWidget(self.register_page)
        self.login_tab.setProperty("active", False)
        self.register_tab.setProperty("active", True)
        self._refresh_tabs()

    def _refresh_tabs(self):
        for button in (self.login_tab, self.register_tab):
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
