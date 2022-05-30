from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate


async def investment_process(
    session: AsyncSession
):
    '''Процесс распределения пожертвований.'''
    pass


async def project_invest_process(
    new_project: CharityProjectCreate,
    session: AsyncSession
):
    '''Процесс распределения инвестиций после создания проекта.'''
    project = charity_project_crud.create_obj_with_datetime(new_project, session)
    if project.fully_invested is True:
        project.close_date = datetime.now()


async def donation_invest_process(
    new_donation: DonationCreate
):
    '''Процесс распределения инвестиций после нового пожертования.'''
    pass