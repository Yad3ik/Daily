from supabase import Client, create_client
from src.config import Config
from src.back.db.exceptions import *
from src.session import Session

class ToDoList:
    @staticmethod
    def _get_db() -> Client:
        return create_client(Config.DB_URL, Config.DB_API_KEY)
    
    @staticmethod
    def add_new(desc: str) -> list[str, str, str, bool]:
        db = ToDoList._get_db()

        res = db.table('tasks').insert({
            'user_id' : Session.USERID,
            'name' : desc
        }).execute()

        return res[0]
    
    @staticmethod
    def delete_task(task_id: str) -> None:
        db = ToDoList._get_db()

        res = db.table('tasks').delete().eq('id', task_id).execute()
    
    @staticmethod
    def set_complete(task_id: str, value: bool) -> None:
        db = ToDoList._get_db()

        res = db.table('tasks').update({
            'is_complete' : value
        }).eq('id', task_id).execute()
    
    @staticmethod
    def get_all(user_id: str) -> list[dict]:
        db = ToDoList._get_db()