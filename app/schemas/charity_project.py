from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., title='Название проекта', min_length=1, max_length=100)
    description: str = Field(..., title='Описание', min_length=1)
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, title='Название проекта', min_length=1, max_length=100)
    description: Optional[str] = Field(None, title='Описание', min_length=1)
    full_amount: Optional[PositiveInt] = Field(None, title='Сумма пожертвования')


class CharityProjectDB(CharityProjectBase):
    id: PositiveInt = Field(..., title='id проекта')
    invested_amount: int = Field(..., title='Сумма пожертвования')
    fully_invested: bool = Field(..., title='Закрыт ли проект')
    create_date: datetime = Field(..., title='Дата создания проекта')
    close_date: Optional[datetime] = Field(None, title='Дата закрытия проекта')

    class Config:
        orm_mode = True
