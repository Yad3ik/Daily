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
    MIN_PASSWORD_LEN = 5

    def __init__(
        self,
        asserts_dir: Path,
        title: str,
        subtitle: str,
        login_hint: str,
        password_hint: str,
        button_text: str,
        bottom_text: Optional[str] = None,
        require_password_repeat: bool = False,
    ):
        super().__init__()
        self.setObjectName("formPage")
        self._require_password_repeat = require_password_repeat

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

        self.submit = QPushButton(button_text)
        self.submit.setObjectName("mainButton")
        self.submit.setFixedHeight(56)
        self.submit.setCursor(Qt.PointingHandCursor)

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

        self.repeat_password_input: Optional[AuthInput] = None
        self._password_error: Optional[QLabel] = None
        self._repeat_error: Optional[QLabel] = None

        if require_password_repeat:
            self._password_error = QLabel()
            self._password_error.setObjectName("fieldError")
            self._password_error.setWordWrap(True)
            self._password_error.hide()

            layout.addSpacing(6)
            layout.addWidget(self._password_error)

            repeat_label = QLabel("ПОВТОРИТЕ ПАРОЛЬ")
            repeat_label.setObjectName("fieldLabel")
            layout.addSpacing(22)
            layout.addWidget(repeat_label)
            layout.addSpacing(9)
            self.repeat_password_input = AuthInput(
                asserts_dir, "Повторите пароль", "lock.png", password=True
            )
            layout.addWidget(self.repeat_password_input)

            self._repeat_error = QLabel()
            self._repeat_error.setObjectName("fieldError")
            self._repeat_error.setWordWrap(True)
            self._repeat_error.hide()
            layout.addSpacing(6)
            layout.addWidget(self._repeat_error)

            self.password_input.line_edit.textChanged.connect(self._update_register_password_hints)
            self.repeat_password_input.line_edit.textChanged.connect(
                self._update_register_password_hints
            )
            self.submit.clicked.connect(self._on_register_submit)
            layout.addSpacing(36)
            layout.addWidget(self.submit)
        else:
            layout.addStretch(1)
            layout.addSpacing(36)
            layout.addWidget(self.submit)

        if bottom_text:
            bottom = QLabel(bottom_text)
            bottom.setObjectName("bottomText")
            bottom.setAlignment(Qt.AlignCenter)
            layout.addSpacing(34)
            layout.addWidget(bottom)

        if require_password_repeat:
            layout.addStretch(1)

    def _update_register_password_hints(self):
        if not self._require_password_repeat or self._password_error is None:
            return
        pw = self.password_input.text()
        rep = self.repeat_password_input.text() if self.repeat_password_input else ""

        if pw and len(pw) < self.MIN_PASSWORD_LEN:
            self._password_error.setText(
                f"Пароль должен содержать не менее {self.MIN_PASSWORD_LEN} символов"
            )
            self._password_error.show()
        else:
            self._password_error.hide()

        if rep and pw != rep:
            self._repeat_error.setText("Пароли не совпадают")
            self._repeat_error.show()
        else:
            self._repeat_error.hide()

    def _register_form_valid(self) -> bool:
        pw = self.password_input.text()
        rep = self.repeat_password_input.text()
        if len(pw) < self.MIN_PASSWORD_LEN:
            self._password_error.setText(
                f"Пароль должен содержать не менее {self.MIN_PASSWORD_LEN} символов"
            )
            self._password_error.show()
            self._repeat_error.hide()
            return False
        self._password_error.hide()
        if pw != rep:
            self._repeat_error.setText("Пароли не совпадают")
            self._repeat_error.show()
            return False
        self._repeat_error.hide()
        return True

    def _on_register_submit(self):
        if not self._register_form_valid():
            return


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
            require_password_repeat=True,
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
