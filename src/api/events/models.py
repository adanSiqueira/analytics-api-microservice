# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime, timezone
import sqlmodel

def get_utc_now():
    return datetime.now(timezone.utc)

class EventModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page: str | None = None
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

class EventCreateSchema(SQLModel):
    page: str
    description: str | None = Field(default=None, max_length=255)

class EventUpdateSchema(SQLModel):
    description: str

class EventListSchema(SQLModel):
    events: list[EventModel] ## List[EventSchema]