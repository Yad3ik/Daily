from src.back.db.task import ToDoList
from src.back.structures import Task
from src.response import Response
from src.session import Me

def sort_tasks() -> None:
    Me.Tasks.sort(key=lambda x: x.is_complete, reverse=True)

def update_me_tasks() -> Response:
    try:
        response = ToDoList.get_all()
        Me.Tasks = [Task(id=task["id"], name=task["name"], is_complete=task["is_complete"]) for task in response]
        sort_tasks()
        return Response(status_code=200, message="Tasks updated successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def add_new_task(name: str, is_complete: bool = False) -> Response:
    try:
        task = ToDoList.add_new(name, is_complete)
        Me.Tasks.append(Task(id=task["id"], name=task["name"], is_complete=task["is_complete"]))
        sort_tasks()
        return Response(status_code=200, message="Task added successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def delete_task(id: str) -> Response:
    try:
        ToDoList.delete_task(id)
        Me.Tasks = [task for task in Me.Tasks if task.id != id]
        return Response(status_code=200, message="Task deleted successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def set_complete(id: str, is_complete: bool) -> Response:
    try:
        ToDoList.set_complete(id, is_complete)

        res = update_me_tasks()
        if res.status_code != 200:
            return res

        return Response(status_code=200, message="Task completed successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))