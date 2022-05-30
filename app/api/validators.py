from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

PROJECT_NAME_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_EXISTS = 'Проект не найден!'
PROJECT_HAS_INVEST = 'В проект уже инвестированы средства!'
PROJECT_IS_CLOSED = 'Закрытый проект нельзя редактировать!'
FULL_AMOUNT_ERROR = 'Нельзя установить требуемую сумму меньше уже вложенной.'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    '''Проверяет название проекта на уникальность.'''
    new_project_name = await charity_project_crud.get_project_by_name(project_name, session)
    if new_project_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_EXISTS,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_EXISTS
        )
    return project


async def check_project_invest(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    '''Проверяет внесённую сумму в проект.'''
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=PROJECT_HAS_INVEST
        )
    return project


async def check_project_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    '''Только для суперюзеров.
    Редактирование проекта'''
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_IS_CLOSED
        )
    if obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=FULL_AMOUNT_ERROR
        )
    return project
