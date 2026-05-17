from datetime import date, datetime, timedelta
from src.config import TAGS
from src.back.db.calendar import Calendar
from src.back.structures import Event
from src.response import Response


def get_week_monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


def get_events(date_start: date, date_finish: date) -> list[list[Event]]:
    raw = Calendar.get(date_start, date_finish)
    events = [Event.from_dict(item) for item in raw]

    by_date: dict[date, list[Event]] = {}
    current = date_start
    while current <= date_finish:
        by_date[current] = []
        current += timedelta(days=1)

    for event in events:
        by_date[event.event_date].append(event)

    return list(by_date.values())


def add_new_event(
    event_date: date,
    start: datetime,
    finish: datetime,
    description: str,
    tag: str | None = None,
    color: str | None = None) -> Response:
    if tag is not None:
        color = TAGS[tag]
    try:
        Calendar.add_new(event_date, start, finish, description, tag, color)
        return Response(status_code=200, message="Event added successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))


def delete_event(event_id: str) -> Response:
    try:
        Calendar.delete(event_id)
        return Response(status_code=200, message="Event deleted successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))
