from src.back.to_front.todo import add_new_task, delete_task
from src.session import Me


def test_add_task_success(auth_user):
    res = add_new_task("Тестовая задача")
    assert res.status_code == 200
    assert any(t.name == "Тестовая задача" for t in Me.Tasks)

    task_id = next(t.id for t in Me.Tasks if t.name == "Тестовая задача")
    delete_task(task_id)
