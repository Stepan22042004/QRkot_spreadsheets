from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDBCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBGet(DonationBase):
    user_id: Optional[int]
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True