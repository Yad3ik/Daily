'''     Кастомные исключения авторизации пользователя      '''

class AuthError(RuntimeError):
    pass

class IncorrectData(AuthError):
    '''     Неверный пароль     '''
    pass

class InvalidData(AuthError):
    '''     Логин уже занят     '''
    pass

class UserNotFound(AuthError):
    pass