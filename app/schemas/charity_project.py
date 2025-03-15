from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None, )
    invested_amount: Optional[int] = Field(None, readOnly=True)
    fully_invested: Optional[bool] = Field(None, readOnly=True)
    create_date: Optional[datetime] = Field(None, readOnly=True)
    close_date: Optional[datetime] = Field(None, readOnly=True)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True
