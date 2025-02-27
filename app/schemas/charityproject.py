from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


NAME_MIN_LEN = 1
NAME_MAX_LEN = 100
DESCRIPTION_MIN_LEN = 1
MIN_FULL_AMOUNT = 0


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN)
    description: str = Field(..., min_length=DESCRIPTION_MIN_LEN)
    full_amount: int = Field(..., gt=MIN_FULL_AMOUNT)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LEN,
        max_length=NAME_MAX_LEN
    )
    description: Optional[str] = Field(None, min_length=DESCRIPTION_MIN_LEN)
    full_amount: Optional[int] = Field(None, gt=MIN_FULL_AMOUNT)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True