from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import validates

from app.core.db import Base


NAME_LEN = 100


class CharityProject(Base):
    name = Column(String(NAME_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime, nullable=True)

    @validates('invested_amount')
    def validate_invested_amount(self, key, value):
        if value < 0:
            raise ValueError(
                "Поле invested_amount не может быть отрицательным."
            )
        return value

    @validates('full_amount')
    def validate_full_amount(self, key, value):
        if value <= 0:
            raise ValueError("Поле full_amount должно быть больше 0.")
        return value