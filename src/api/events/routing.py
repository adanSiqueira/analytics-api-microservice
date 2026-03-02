from fastapi import APIRouter, Depends, HTTPException
from src.api.db.session import get_session

from src.api.db.config import DATABASE_URL
from src.api.db.session import get_session
from sqlmodel import Session, select

from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

# GET
# List view
# GET /api/events/ -> list of events
@router.get("/", response_model = EventListSchema)
def read_events(session: Session = Depends(get_session)):

    print(DATABASE_URL)
    
    query = select(EventModel)
    results = session.exec(query).all()
    
    return EventListSchema(events=results)

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
@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, 
                 payload: EventUpdateSchema,
                 session: Session = Depends(get_session)):
    
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException (status_code=404, detail="Event not found.")
    
    data = payload.model_dump()

    for key, value in data.items():
        setattr(obj, key, value)

    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj