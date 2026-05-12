from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from api.routers import transcription, generation, jobs, settings
from database.session import engine
from database.models import Base

app = FastAPI(title="MeetingMind Backend")

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

# Configuration
STORAGE_DIR = os.getenv("STORAGE_DIR", "data")
os.makedirs(os.path.join(STORAGE_DIR, "input"), exist_ok=True)
os.makedirs(os.path.join(STORAGE_DIR, "output"), exist_ok=True)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(transcription.router)
app.include_router(generation.router)
app.include_router(jobs.router)
app.include_router(settings.router)

@app.get("/")
def read_root():
    return {"message": "MeetingMind Backend is running"}
