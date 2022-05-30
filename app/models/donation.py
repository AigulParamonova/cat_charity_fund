from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import Column, ForeignKey, Text

from .abstract_base import AbstractBase


class Donation(AbstractBase):
    '''Модель пожертвований таблицы donation.'''
    user_id = Column(GUID, ForeignKey('user.id'))
    comment = Column(Text)
