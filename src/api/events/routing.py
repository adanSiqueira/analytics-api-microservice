from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from src.api.db.config import DATABASE_URL
from src.api.db.session import get_session
from sqlmodel import Session, select

from .models import (
    EventModel, 
    EventBucketSchema, 
    EventCreateSchema,
    get_utc_now
)   

from datetime import datetime, timedelta, timezone
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy import func

router = APIRouter()

DEFAULT_LOOKUP_PAGES = ['/about', '/contact', '/pages', '/pricing']

# GET
# List view
# GET /api/events/ -> list of events
@router.get("/", response_model = List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session) 
    ):

    print(DATABASE_URL)
    
    bucket = time_bucket("1 day", EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES 

    query = (
        select(
            bucket.label('bucket'),
            EventModel.page.label('page'),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            EventModel.page,)
    )
    results = session.exec(query).fetchall()
    
    return [
    EventBucketSchema(
        bucket=row.bucket,
        page=row.page,
        count=row.count,
    )
    for row in results
    ]

# GET
# Individual view
# GET /api/events/{event_id} -> event details
@router.get("/{event_id}" , response_model=EventModel)
def read_event(event_id: int, session: Session = Depends(get_session)):

    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException (status_code=404, detail="Event not found.")

    return result

# POST
# Create view
# POST /api/events/ -> create event
@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)) -> EventModel:

    print(DATABASE_URL)

    data = payload.model_dump() # payload -> dict -> pydantic

    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj


#PUT
# @router.put("/{event_id}", response_model=EventModel)
# def update_event(event_id: int, 
#                  payload: EventUpdateSchema,
#                  session: Session = Depends(get_session)):
    
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException (status_code=404, detail="Event not found.")
    
#     data = payload.model_dump()

#     for key, value in data.items():
#         setattr(obj, key, value)
    
#     obj.updated_at = get_utc_now()

#     session.add(obj)
#     session.commit()
#     session.refresh(obj)

#     return obj