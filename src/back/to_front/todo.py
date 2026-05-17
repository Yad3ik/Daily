from src.back.db.task import ToDoList
from src.back.structures import Task
from src.response import Response
from src.session import Me

def _sort_tasks() -> None:
    if Me.Tasks is None:
        return
    Me.Tasks.sort(key=lambda x: x.is_complete)

def update_me_tasks() -> Response:
    return _update_tasks()


def _update_tasks() -> Response:
    try:
        response = ToDoList.get_all()
        Me.Tasks = [Task.from_dict(task) for task in response]
        _sort_tasks()
        return Response(status_code=200, message="Tasks updated successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def add_new_task(name: str, is_complete: bool = False) -> Response:
    try:
        task = ToDoList.add_new(name, is_complete)
        Me.Tasks = [Task.from_dict(task)] + Me.Tasks
        _sort_tasks()
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

        task = next((task for task in Me.Tasks if task.id == id), None)
        if task is None:
            return Response(status_code=404, message="Task not found")
        
        if task.is_complete == is_complete:
            return Response(status_code=200, message="Task already has this status")
        
        ToDoList.set_complete(id, is_complete)

        res = _update_tasks()
        if res.status_code != 200:
            return res

        return Response(status_code=200, message="Task completed successfully")
    except RuntimeError as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))