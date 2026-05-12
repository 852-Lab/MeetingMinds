from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
import shutil
import os
import uuid
from database.session import get_db
from database.models import Job, JobType, JobStatus
from sqlalchemy.orm import Session
from services.scribe import transcriber

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["transcription"])

STORAGE_DIR = os.getenv("STORAGE_DIR", "data")
INPUT_DIR = os.path.join(STORAGE_DIR, "input")
os.makedirs(INPUT_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

@router.get("/sona-status")
def get_sona_status():
    """
    Checks if the Sona transcription server is ready.
    """
    ready = transcriber.is_ready()
    return {"ready": ready}

@router.post("/youtube-transcribe")
async def youtube_transcribe(request: DownloadRequest, db: Session = Depends(get_db)):
    """
    Creates a new YouTube transcription job.
    """
    job = Job(
        type=JobType.YOUTUBE_URL,
        input_path=request.url,
        status=JobStatus.PENDING
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    return {"message": "Job created", "job_id": job.id}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Handles file upload and creates a transcription job.
    """
    job_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(INPUT_DIR, f"{job_id}{file_ext}")
    
    logger.info(f"Uploading file: {file.filename} (extension: {file_ext})")
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        job = Job(
            id=job_id,
            type=JobType.AUDIO_UPLOAD,
            input_path=input_path,
            original_filename=file.filename,
            status=JobStatus.PENDING
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        return {"message": "Upload successful, job queued", "job_id": job.id, "original_filename": file.filename}
    except Exception as e:
        logger.error(f"Error during upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
