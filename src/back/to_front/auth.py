from src.back.db.auth import Auth
from src.back.db.exceptions import *
from src.session import Me, CurrentUser
from src.response import Response
from src.back.to_front.todo import _update_me_tasks

def sign_up(login: str, password: str) -> Response:
    try:
        user_id = Auth.create_new_user(login, password)
        Me.set_user(CurrentUser(id=user_id, login=login))
        res = _update_me_tasks()
        if res.status_code != 200:
            return res
        
        return Response(status_code=200, message="User created successfully")
    except InvalidData as e:
        return Response(status_code=400, message="duplicate key", exception=str(e))
    except AuthError as e:
        return Response(status_code=400, message="Registration faild", exception=str(e))
    except Exception as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def sign_in(login: str, password: str) -> Response:
    try:
        user_id = Auth.login_user(login, password)
        Me.set_user(CurrentUser(id=user_id, login=login))

        res = update_me_tasks()
        if res.status_code != 200:
            return res
        
        return Response(status_code=200, message="User logged in successfully")
    except IncorrectData as e:
        return Response(status_code=400, message="Invalid login or password", exception=str(e))
    except AuthError as e:
        return Response(status_code=400, message="Login faild", exception=str(e))
    except Exception as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))

def sign_out() -> Response:
    Me.clear()
    return Response(status_code=200, message="User logged out successfully")

def delete_user(id: str | None = None) -> Response: # id is optional for testing
    try:
        if id is None:
            id = Me.require_user_id()
        Auth._delete_user(id)
        Me.clear()
        return Response(status_code=200, message="User deleted successfully")
    except AuthError as e:
        return Response(status_code=400, message="User not found", exception=str(e))
    except Exception as e:
        return Response(status_code=500, message="Internal server error", exception=str(e))