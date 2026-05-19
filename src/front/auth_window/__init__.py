__all__ = ["AuthWindow"]


def __getattr__(name: str):
    if name == "AuthWindow":
        from .auth_window import AuthWindow

        return AuthWindow
    raise AttributeError(name)
