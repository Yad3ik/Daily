"""Состояние текущей недели календаря (якорная дата, сдвиги)."""

from __future__ import annotations

from datetime import date, timedelta

from src.back.to_front.events import get_week_monday


class CalendarState:
    """Текущая неделя календаря (якорная дата и сдвиги)."""

    def __init__(self) -> None:
        """Инициализирует неделю от сегодняшней даты."""
        self.anchor: date = date.today()

    @property
    def monday(self) -> date:
        """Понедельник недели, в которую попадает anchor."""
        return get_week_monday(self.anchor)

    @property
    def week_days(self) -> list[date]:
        """Семь дат (пн–вс) относительно monday."""
        start = self.monday
        return [start + timedelta(days=i) for i in range(7)]

    def shift_week(self, delta: int) -> None:
        """Сдвигает anchor на delta недель."""
        self.anchor += timedelta(days=7 * delta)
