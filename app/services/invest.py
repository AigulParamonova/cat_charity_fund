from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


def close_obj(objs: List[Base]) -> None:
    '''Помечает объекты с рапределёнными инвестициями.'''
    for obj in objs:
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()


async def investment_process(
    from_obj_invest: Base,
    in_obj_invest: Base,
    session: AsyncSession
):
    '''Процесс распределения инвестиций.'''
    all_investments = await in_obj_invest.get_for_separations(session)
    for investment in all_investments:
        need_for_invest = from_obj_invest.full_amount - from_obj_invest.invested_amount
        free_for_invest = investment.full_amount - investment.invested_amount
        append_obj = min(need_for_invest, free_for_invest)
        investment.invested_amount += append_obj
        from_obj_invest.invested_amount += append_obj
        close_obj((investment, from_obj_invest))
    session.add_all((*all_investments, from_obj_invest))
    await session.commit()
    await session.refresh(from_obj_invest)
    return from_obj_invest