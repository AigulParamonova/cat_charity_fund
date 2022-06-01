from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer

from app.core.db import Base


class AbstractBase(Base):
    __abstract__ = True

    full_amount = Column(
        Integer,
        nullable=False
    )
    invested_amount = Column(
        Integer,
        nullable=False,
        default=0
    )
    fully_invested = Column(
        Boolean,
        nullable=False,
        default=False
    )
    create_date = Column(
        DateTime,
        nullable=False
    )
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount')
    )
