# from pydantic import BaseModel, Field
from typing import Optional
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
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default="", index=True)

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"

class EventCreateSchema(SQLModel):
    page: str = Field (index=True)
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default="", index=True)

# class EventUpdateSchema(SQLModel):
#     description: str

class EventListSchema(SQLModel):
    events: list[EventModel] ## List[EventSchema]

class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    count: int