"""Current week anchor for the calendar view."""

from __future__ import annotations

from datetime import date, timedelta

from src.back.to_front.events import get_week_monday


class CalendarState:
    def __init__(self) -> None:
        self.anchor: date = date.today()

    @property
    def monday(self) -> date:
        return get_week_monday(self.anchor)

    @property
    def week_days(self) -> list[date]:
        start = self.monday
        return [start + timedelta(days=i) for i in range(7)]

    def shift_week(self, delta: int) -> None:
        self.anchor += timedelta(days=7 * delta)
