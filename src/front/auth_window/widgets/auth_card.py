"""Карточка входа/регистрации с вкладками."""

from collections.abc import Callable
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
)

from src.back.to_front.auth import sign_in, sign_up

from .auth_result import error_message_for_response
from .input_field import AuthInput


class FormPage(QFrame):
    """Одна форма: логин, пароль, опционально повтор пароля."""

    MIN_PASSWORD_LEN = 5

    def __init__(
        self,
        asserts_dir: Path,
        title: str,
        subtitle: str,
        login_hint: str,
        password_hint: str,
        button_text: str,
        require_password_repeat: bool = False,
    ):
        """Собирает поля; при require_password_repeat — валидация паролей."""
        super().__init__()
        self.setObjectName("formPage")
        self._require_password_repeat = require_password_repeat
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

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

        self._api_error = QLabel()
        self._api_error.setObjectName("fieldError")
        self._api_error.setWordWrap(True)
        self._api_error.hide()

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
            layout.addStretch(1)
            layout.addWidget(self._api_error)
            layout.addSpacing(36)
            layout.addWidget(self.submit)
        else:
            layout.addStretch(1)
            layout.addWidget(self._api_error)
            layout.addSpacing(36)
            layout.addWidget(self.submit)

    def _update_register_password_hints(self):
        """Показывает ошибки длины и несовпадения паролей."""
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

    def register_form_valid(self) -> bool:
        """Проверяет пароль перед sign_up."""
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

    def show_api_error(self, message: str) -> None:
        """Показывает текст ошибки API под формой."""
        self._api_error.setText(message)
        self._api_error.show()

    def clear_api_error(self) -> None:
        """Скрывает блок ошибки API."""
        self._api_error.clear()
        self._api_error.hide()


class AuthCard(QFrame):
    """Вкладки Войти/Регистрация и вызов sign_in / sign_up."""

    def __init__(self, asserts_dir: Path, on_auth_success: Callable[[], None]):
        """on_auth_success — после успешного входа или регистрации."""
        super().__init__()
        self.setObjectName("authCard")
        self._on_auth_success = on_auth_success
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

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
        self.stack.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
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
        layout.addWidget(self.stack, 1)
        self.login_page.submit.clicked.connect(self._on_login_clicked)
        self.register_page.submit.clicked.connect(self._on_register_clicked)
        self._wire_clear_api_error_on_edit()
        self.show_login()

    def _wire_clear_api_error_on_edit(self) -> None:
        """Сбрасывает ошибку API при изменении полей."""
        self.login_page.login_input.line_edit.textChanged.connect(self.login_page.clear_api_error)
        self.login_page.password_input.line_edit.textChanged.connect(self.login_page.clear_api_error)
        self.register_page.login_input.line_edit.textChanged.connect(self.register_page.clear_api_error)
        self.register_page.password_input.line_edit.textChanged.connect(
            self.register_page.clear_api_error
        )
        rep = self.register_page.repeat_password_input
        if rep is not None:
            rep.line_edit.textChanged.connect(self.register_page.clear_api_error)

    def _clear_api_error(self) -> None:
        """Сбрасывает ошибки на обеих формах."""
        self.login_page.clear_api_error()
        self.register_page.clear_api_error()

    def _on_login_clicked(self) -> None:
        """sign_in и on_auth_success при успехе."""
        login = self.login_page.login_input.text().strip()
        password = self.login_page.password_input.text()
        if not login or not password:
            self.login_page.show_api_error("Введите логин и пароль.")
            return
        response = sign_in(login, password)
        err = error_message_for_response(response)
        if err is not None:
            self.login_page.show_api_error(err)
            return
        self._clear_api_error()
        self._on_auth_success()

    def _on_register_clicked(self) -> None:
        """sign_up после валидации формы."""
        if not self.register_page.register_form_valid():
            return
        login = self.register_page.login_input.text().strip()
        password = self.register_page.password_input.text()
        if not login:
            self.register_page.show_api_error("Введите логин.")
            return
        response = sign_up(login, password)
        err = error_message_for_response(response)
        if err is not None:
            self.register_page.show_api_error(err)
            return
        self._clear_api_error()
        self._on_auth_success()

    def show_login(self):
        """Переключает стек на форму входа."""
        self._clear_api_error()
        self.stack.setCurrentWidget(self.login_page)
        self.login_tab.setProperty("active", True)
        self.register_tab.setProperty("active", False)
        self._refresh_tabs()

    def show_register(self):
        """Переключает стек на регистрацию."""
        self._clear_api_error()
        self.stack.setCurrentWidget(self.register_page)
        self.login_tab.setProperty("active", False)
        self.register_tab.setProperty("active", True)
        self._refresh_tabs()

    def _refresh_tabs(self):
        """Переприменяет QSS к вкладкам после смены active."""
        for button in (self.login_tab, self.register_tab):
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
