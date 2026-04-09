class AuthError(RuntimeError):
    pass

class IncorrectData(AuthError):
    pass

class InvalidData(AuthError):
    pass

class UserNotFound(AuthError):
    pass