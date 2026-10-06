from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: str = ''

    model_config = ConfigDict(extra='forbid')


class DonationCreateResponse(DonationCreate):
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationDB(DonationCreate):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    pass


class DonationUserDB(DonationCreate):
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)
