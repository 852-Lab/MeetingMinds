from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import shutil
import os
import uuid
from services.audio import extract_audio
from services.youtube import transcribe_youtube
from services.scribe import transcriber

import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["transcription"])

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

class TranscribeRequest(BaseModel):
    file_path: str
    language: str = None

@router.get("/sona-status")
def get_sona_status():
    """
    Checks if the Sona transcription server is ready.
    """
    ready = transcriber.is_ready()
    return {"ready": ready}

@router.post("/youtube-transcribe")
async def youtube_transcribe(request: DownloadRequest):
    """
    Handles YouTube transcription (captions or Whisper) with streaming status.
    """
    def generate():
        for chunk in transcribe_youtube(request.url, STORAGE_DIR):
            yield chunk + "\n"
            
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file upload and extracts audio.
    """
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    temp_path = os.path.join(STORAGE_DIR, f"{file_id}{file_ext}")
    
    logger.info(f"Uploading file: {file.filename} (extension: {file_ext})")
    logger.info(f"Saving temporary file to: {temp_path}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        processed_path = os.path.join(STORAGE_DIR, f"{file_id}_processed.wav")
        logger.info(f"Extracting audio to: {processed_path}")
        
        extract_audio(temp_path, processed_path)
        logger.info(f"Audio extraction successful: {processed_path}")
        
        return {"message": "Upload successful", "file_path": processed_path, "original_filename": file.filename}
    except Exception as e:
        logger.error(f"Error during upload/extraction: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe")
def transcribe_audio(request: TranscribeRequest):
    """
    Transcribes the audio file.
    """
    logger.info(f"Received transcription request for: {request.file_path}")
    try:
        if not os.path.exists(request.file_path):
            logger.error(f"File not found: {request.file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"Starting transcription for: {request.file_path} (language: {request.language})")
        result = transcriber.transcribe(request.file_path, language=request.language)
        logger.info("Transcription successful")
        
        return {"text": result["text"], "segments": result["segments"], "language": request.language}
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
