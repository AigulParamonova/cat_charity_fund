from typing import List

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_project_invest, check_project_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    '''Возвращает список всех проектов.'''
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.
    Создаёт благотворительный проект.
    '''
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create_obj_with_datetime(project, session)
    await investment_process(
        from_obj_invest=new_project,
        in_obj_invest=donation_crud,
        session=session
    )
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: PositiveInt,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    '''Только для суперюзеров.
    Удаляет проект.
    '''
    project = await check_project_invest(project_id, session)
    project_delete = await charity_project_crud.remove(project, session)
    return project_delete


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: PositiveInt,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    '''Только для суперюзеров.
    Обновляет поля проекта.'''
    await check_project_exists(project_id, session)
    project = await check_project_update(project_id, obj_in, session)
    project_update = await charity_project_crud.update(project, obj_in, session)
    return project_update
