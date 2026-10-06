from supabase import Client
from src.config import Config
from src.back.db.exceptions import *
from src.session import Me

class ToDoList:
    @staticmethod
    def _get_db() -> Client:
        return Config.DB
    
    @staticmethod
    def add_new(desc: str, is_complete: bool = False) -> dict:
        '''  Добавление новой задачи, is_comlete не обязателен   '''

        db = ToDoList._get_db()

        res = db.table('tasks').insert({
            'user_id': Me.require_user_id(),
            'name': desc,
            'is_complete': is_complete,
        }).execute()

        return res.data[0]
    
    @staticmethod
    def delete_task(task_id: str) -> None:
        '''      Удаление задачи из бд       '''

        db = ToDoList._get_db()

        res = db.table('tasks').delete().eq('id', task_id).execute()
    
    @staticmethod
    def set_complete(task_id: str, value: bool) -> None:
        '''    Установить статус задачи: done/not done    '''

        db = ToDoList._get_db()

        res = db.table('tasks').update({
            'is_complete' : value
        }).eq('id', task_id).execute()
    
    @staticmethod
    def get_all() -> list[dict]:
        '''    Получение всех задач текущего пользователя в порядке добавление.   '''

        db = ToDoList._get_db()

        res = db.table('tasks').select('*').eq('user_id', Me.require_user_id()).order('created_at', desc=True).execute()

        return res.data
