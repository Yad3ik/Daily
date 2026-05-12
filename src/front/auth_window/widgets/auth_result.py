"""Сообщения об ошибках для UI по ответу бэкенда (Response)."""

from src.response import Response

MSG_DUPLICATE_USER = "Уже существует пользователь с таким логином."
MSG_AUTH_FAILED = "Ошибка аутентификации."
MSG_INTERNAL = "Internal server error"


def error_message_for_response(resp: Response) -> str | None:
    """
    Возвращает текст ошибки для пользователя или None, если запрос успешен (2xx).
    """
    if 200 <= resp.status_code < 300:
        return None
    if resp.status_code == 500:
        return MSG_INTERNAL
    if resp.status_code == 400:
        combined = f"{resp.message or ''} {resp.exception or ''}".lower()
        if "duplicate" in combined:
            return MSG_DUPLICATE_USER
        return MSG_AUTH_FAILED
    return resp.message or "Произошла ошибка. Попробуйте позже."
