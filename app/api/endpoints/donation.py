from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationDB, DonationCreate, DonationGetUser
from app.schemas.user import UserDB
from app.core.user import current_user

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
) -> List[DonationDB]:
    '''Возвращает список всех пожертвований.'''
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationGetUser,
    response_model_exclude_none=True,
)
async def create_donation(
        new_donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
) -> DonationGetUser:
    '''Только для зарегистрированных пользователей.
    Создаёт пожертвование.
    '''
    donation = await donation_crud.create_obj_with_datetime(new_donation, session, user)
    return donation


@router.get(
    '/my',
    response_model=List[DonationGetUser]
)
async def get_user_donations(
    user: UserDB = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> List[DonationGetUser]:
    '''Возвращает список пожертвований пользователя.'''
    my_donations = await donation_crud.get_by_user(session, user)
    return my_donations