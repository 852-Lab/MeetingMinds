from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from api.routers import transcription, generation

app = FastAPI(title="MeetingMind Backend")

# Configuration
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

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

@app.get("/")
def read_root():
    return {"message": "MeetingMind Backend is running"}
