from datetime import date, time, timedelta

from src.back.to_front.events import add_new_event, get_events, delete_event


def test_get_events_empty_days(auth_user):
    date_start = date.today()
    date_finish = date_start + timedelta(days=6)

    events = get_events(date_start, date_finish)
    assert len(events) == 7
    assert all(day == [] for day in events)


def test_get_events_range(auth_user):
    date_start = date.today()
    event_date = date_start + timedelta(days=2)
    date_finish = date_start + timedelta(days=6)

    add_new_event(event_date, time(10, 0), time(11, 0), "Событие в среду")

    events = get_events(date_start, date_finish)
    day_index = (event_date - date_start).days
    assert len(events[day_index]) == 1
    assert events[day_index][0].description == "Событие в среду"

    delete_event(events[day_index][0].id)
