from datetime import date, time

from src.back.to_front.events import add_new_event, get_events, delete_event
from src.config import TAGS


def test_add_event_with_tag(auth_user):
    event_date = date.today()
    res = add_new_event(event_date, time(9, 0), time(10, 0), "Рабочее совещание", tag="Работа")
    assert res.status_code == 200

    events = get_events(event_date, event_date)
    event = events[0][0]
    assert event.tag == "Работа"
    assert event.color == TAGS["Работа"]
    delete_event(event.id)


def test_add_event_no_tag(auth_user):
    event_date = date.today()
    res = add_new_event(event_date, time(14, 0), time(15, 0), "Личный план")
    assert res.status_code == 200

    events = get_events(event_date, event_date)
    event = events[0][0]
    assert event.tag is None
    delete_event(event.id)
