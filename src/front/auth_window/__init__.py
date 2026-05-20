"""Окно входа и регистрации."""

__all__ = ["AuthWindow"]


def __getattr__(name: str):
    """Ленивый импорт AuthWindow по имени из __all__."""
    if name == "AuthWindow":
        from .auth_window import AuthWindow

        return AuthWindow
    raise AttributeError(name)
