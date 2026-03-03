# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime, timezone
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

# page visits at any given time
class EventModel(TimescaleModel, table=True):
    # TimescaleModel already gives: 'id' and 'created_at'.

    page: str = Field (index=True)
    description: str | None = Field(default=None, max_length=255)
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"

class EventCreateSchema(SQLModel):
    page: str
    description: str | None = Field(default=None, max_length=255)

class EventUpdateSchema(SQLModel):
    description: str

class EventListSchema(SQLModel):
    events: list[EventModel] ## List[EventSchema]