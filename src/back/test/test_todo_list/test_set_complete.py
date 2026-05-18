from src.back.to_front.todo import add_new_task, delete_task, set_complete
from src.session import Me


def test_set_complete_true(auth_user):
    add_new_task("Задача для завершения")
    task_id = next(t.id for t in Me.Tasks if t.name == "Задача для завершения")

    res = set_complete(task_id, True)
    assert res.status_code == 200
    assert next(t.is_complete for t in Me.Tasks if t.id == task_id)
    delete_task(task_id)


def test_set_complete_already_set(auth_user):
    add_new_task("Уже выполнена")
    task_id = next(t.id for t in Me.Tasks if t.name == "Уже выполнена")
    set_complete(task_id, True)

    res = set_complete(task_id, True)
    assert res.status_code == 200
    delete_task(task_id)


def test_set_complete_not_found(auth_user):
    res = set_complete("nonexistent-id-000", True)
    assert res.status_code == 404
