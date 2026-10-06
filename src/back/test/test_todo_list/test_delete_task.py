from src.back.to_front.todo import add_new_task, delete_task
from src.session import Me


def test_delete_task_success(auth_user):
    add_new_task("Задача для удаления")
    task_id = next(t.id for t in Me.Tasks if t.name == "Задача для удаления")

    res = delete_task(task_id)
    assert res.status_code == 200
    assert not any(t.id == task_id for t in Me.Tasks)
