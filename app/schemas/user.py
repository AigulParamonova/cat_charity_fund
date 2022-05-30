from fastapi_users import models


class User(models.BaseUser):
    '''Cхема с базовыми полями модели пользователя (за исключением пароля).'''
    pass


class UserCreate(models.BaseUserCreate):
    '''Cхема для регистрации пользователя; в неё обязательно
    должны быть переданы email и password.
    '''
    pass


class UserUpdate(models.BaseUserUpdate):
    '''Cхема для обновления объекта пользователя; содержит все базовые поля модели
    (в том числе и пароль). Все поля опциональны.
    '''
    pass


class UserDB(User, models.BaseUserDB):
    '''Cхема, описывающая модель в БД; пароль хранится в захэшированном
    виде в поле hashed_password.
    '''
    pass
