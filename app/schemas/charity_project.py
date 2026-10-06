from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: int = Field(..., gt=0)

    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=5, max_length=100)
    description: str | None = Field(None, min_length=10)
    full_amount: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
