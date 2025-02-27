from datetime import datetime

from sqlalchemy import (Column, String, Integer,
                        DateTime, Boolean, ForeignKey)
from sqlalchemy.orm import validates

from app.core.db import Base


class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(String, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime, nullable=True)

    @validates('full_amount', 'invested_amount')
    def validate_positive_amounts(self, key, value):
        if value < 0:
            raise ValueError(f"Поле {key} должно быть больше 0.")
        return value
