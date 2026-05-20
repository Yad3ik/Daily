"""Виджеты вкладки «Календарь»: сетка недели, события, диалоги."""

from .add_event_dialog import AddEventDialog
from .event_block import EventBlock, HOUR_HEIGHT, HOURS_IN_DAY
from .week_grid import WeekGrid
from .week_header import WeekHeader

__all__ = [
    "AddEventDialog",
    "EventBlock",
    "HOUR_HEIGHT",
    "HOURS_IN_DAY",
    "WeekGrid",
    "WeekHeader",
]
