from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserDB


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        '''Получение одного объекта.'''
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        '''Получение всех объектов в БД.'''
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create_obj_with_datetime(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[UserDB] = None,
        create_date: bool = True
    ):
        '''Сохраняет запись в БД с датой создания.'''
        obj_in_data = obj_in.dict()

        if create_date:
            obj_in_data['create_date'] = datetime.now()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        '''Обновление объекта в БД.'''
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        '''Удаление объекта из БД.'''
        await session.delete(db_obj)
        await session.commit()
        return db_obj