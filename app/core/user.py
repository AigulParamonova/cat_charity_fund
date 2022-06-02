import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import UserTable
from app.schemas.user import User, UserCreate, UserDB, UserUpdate
from app.services import constans as const


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    '''Асинхронный генератор, обеспечивает доступ к БД'''
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    '''Cтратегия хранения токенов в виде JWT'''
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    '''Производит валидацию, верификацию, регистрацию и пр.'''
    user_db_model = UserDB
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, UserDB],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason=const.PASSSWORD_LEN_ERROR
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=const.PASSWORD_VALIDATION
            )

    async def on_after_register(
            self, user: UserDB, request: Optional[Request] = None
    ):
        logging.error(const.USER_EXISTS_ERROR)


async def get_user_manager(user_db=Depends(get_user_db)):
    '''Возвращает объект класса UserManager'''
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
