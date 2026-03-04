from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from src.api.events import router as events_router
from src.api.db.session import init_db
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources here (e.g., database connection)
    print("Starting up...")
    init_db()  # Call the function to initialize the database
    yield
    # Clean up resources here (e.g., close database connection)
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(events_router, prefix="/api/events")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def api_health():
    return {"status": "ok"}
