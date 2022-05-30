from sqlalchemy import Column, String, Text

from .abstract_base import AbstractBase


class CharityProject(AbstractBase):
    '''Модель проектов таблицы charityproject.'''
    name = Column(
        String(100),
        unique=True,
        nullable=False
    )
    description = Column(
        Text,
        nullable=False,
    )
