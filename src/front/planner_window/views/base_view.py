"""Базовый класс экранов планировщика."""

from PyQt5.QtWidgets import QWidget


class BaseView(QWidget):
    """Базовый вид контента планировщика (календарь / задачи)."""

    def refresh(self) -> None:
        """Перезагружает данные из сессии и бэкенда."""
