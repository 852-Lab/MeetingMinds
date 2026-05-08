from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import shutil
import os
import uuid
import traceback
from services.audio import extract_audio
from services.youtube import transcribe_youtube
from services.scribe import transcriber

router = APIRouter(prefix="/api", tags=["transcription"])

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

class TranscribeRequest(BaseModel):
    file_path: str
    language: str = None

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
    print(f"Received file upload request: {file.filename} (ID: {file_id})")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"File saved to {temp_path}. Extracting audio...")
        processed_path = os.path.join(STORAGE_DIR, f"{file_id}_processed.wav")
        extract_audio(temp_path, processed_path)
        print(f"Audio extraction complete: {processed_path}")
        
        return {"message": "Upload successful", "file_path": processed_path, "original_filename": file.filename}
    except Exception as e:
        print(f"Upload error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe")
def transcribe_audio(request: TranscribeRequest):
    """
    Transcribes the audio file.
    """
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"Starting transcription for: {request.file_path}")
        result = transcriber.transcribe(request.file_path, language=request.language)
        return {"text": result["text"], "segments": result["segments"], "language": request.language}
    except Exception as e:
        print(f"Transcription error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
