from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., ge=1)
    comment: Optional[str] = Field(None, min_length=1)


class DonationCreate(DonationBase):
    pass


class DonationDBShort(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationDBShort):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
