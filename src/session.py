from typing import ClassVar
from pydantic import BaseModel, Field
from src.back.db.exceptions import AuthError
from src.back.structures import Task

class CurrentUser(BaseModel):
    id: str = Field(..., min_length=1)
    login: str = Field(..., min_length=1)


class Me:
    '''    Глобальное состояние текущей сессии    '''

    user: ClassVar[CurrentUser | None] = None
    Tasks: ClassVar[list[Task] | None] = None

    @classmethod
    def set_user(cls, user: CurrentUser | None) -> None:
        cls.user = user

    @classmethod
    def require_user_id(cls) -> str:
        '''     Безопасное получение user_id    '''
        if cls.user is None:
            raise AuthError("Not authenticated")
        return cls.user.id

    @classmethod
    def clear(cls) -> None:
        cls.set_user(None)
        cls.Tasks = None
    
    @classmethod
    def is_authenticated(cls) -> bool:
        return cls.user is not None
    
    @classmethod
    def to_dict(cls) -> dict:
        return {
            "user": cls.user.model_dump() if cls.user else None,
            "tasks": cls.Tasks if cls.Tasks else None
        }
