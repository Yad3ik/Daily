from datetime import date, time

from src.back.to_front.events import add_new_event, get_events, delete_event


def test_delete_event_success(auth_user):
    event_date = date.today()
    add_new_event(event_date, time(11, 0), time(12, 0), "Событие для удаления")

    events = get_events(event_date, event_date)
    event = events[0][0]

    res = delete_event(event.id)
    assert res.status_code == 200

    events_after = get_events(event_date, event_date)
    assert events_after[0] == []
