import sqlmodel
from sqlmodel import SQLModel, Session
from sqlalchemy import text
import timescaledb

from .config import DATABASE_URL, DB_TIMEZONE

engine = timescaledb.create_engine(DATABASE_URL, echo=True, timezone=DB_TIMEZONE)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("SELECT pg_advisory_lock(1)"))
        SQLModel.metadata.create_all(engine)
        conn.execute(text("SELECT pg_advisory_unlock(1)"))
        print('creating hypertables')
        timescaledb.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session