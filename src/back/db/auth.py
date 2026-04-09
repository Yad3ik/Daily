import bcrypt

from supabase import Client, create_client

from src.config import Config
from src.back.db.exceptions import *

class Auth:
    @staticmethod
    def _get_db() -> Client:
        return create_client(Config.DB_URL, Config.DB_API_KEY)

    @staticmethod
    def create_new_user(login: str, password: str) -> str:
        db = Auth._get_db()

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            res = db.table("users").insert({
                "login": login,
                "pass_hash": hashed }).execute()

            return res.data[0]["id"]
        except Exception as e:
            if "duplicate key" in str(e):
                raise InvalidData(f"User {login=} already exists")
            raise AuthError("Registration faild") from e

    @staticmethod
    def login_user(login: str, password: str) -> str:
        db = Auth._get_db()

        res = db.table("users").select("id, pass_hash").eq("login", login).limit(1).execute()

        if not res.data:
            raise IncorrectData("Invalid login or password")

        user = res.data[0]
        correct_hash = user["pass_hash"]

        if not bcrypt.checkpw(password.encode("utf-8"), correct_hash.encode("utf-8")):
            raise IncorrectData("Invalid login or password")

        return user["id"]

    @staticmethod
    def _delete_user(user_id: str) -> None:
        db = Auth._get_db()

        try:
            res = db.table("users").delete().eq("id", user_id).execute()

            if not res.data:
                raise UserNotFound("User not found")

        except Exception as e:
            raise AuthError(f"Delete failed") from e
