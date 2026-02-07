from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import uuid
from services.downloader import download_youtube_audio
from services.audio import extract_audio
from services.youtube import transcribe_youtube

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

@app.get("/")
def read_root():
    return {"message": "MeetingMind Backend is running"}

class DownloadRequest(BaseModel):
    url: str

@app.post("/api/download")
async def download_video(request: DownloadRequest):
    """
    Downloads audio from YouTube URL.
    """
    try:
        file_path = download_youtube_audio(request.url, STORAGE_DIR)
        return {"message": "Download successful", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/youtube-transcribe")
async def youtube_transcribe(request: DownloadRequest):
    """
    Handles YouTube transcription (captions or Whisper).
    """
    try:
        result = transcribe_youtube(request.url, STORAGE_DIR)
        return {
            "message": "Transcription successful",
            "method": result["method"],
            "text": result["text"],
            "file_path": result["file_path"],
            "segments": result["segments"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file upload and extracts audio.
    """
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    temp_path = os.path.join(STORAGE_DIR, f"{file_id}{file_ext}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # If it's a video or non-standard audio, convert/extract
        # For simplicity, we just run everything through extract_audio to standardize to 16k mono wav/pcm
        # But `extract_audio` in our services/audio.py converts to pcm_s16le/wav basically
        processed_path = os.path.join(STORAGE_DIR, f"{file_id}_processed.wav")
        extract_audio(temp_path, processed_path)
        
        return {"message": "Upload successful", "file_path": processed_path, "original_filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from services.scribe import Transcriber
from services.llm import LLMGenerator

# Services Initialization
# We load the model once. For production, consider lazy loading or separate worker.
transcriber = Transcriber(model_name="base")
llm_client = LLMGenerator(model="llama3.2")

class TranscribeRequest(BaseModel):
    file_path: str
    language: str = None  # 'en', 'de', 'zh', 'yue'

class GenerateRequest(BaseModel):
    transcript: str
    template_type: str = "meeting_notes" # meeting_notes, summary, action_items

@app.post("/api/transcribe")
def transcribe_audio(request: TranscribeRequest):
    """
    Transcribes the audio file.
    Runs in a threadpool (def instead of async def) to avoid blocking event loop.
    """
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        result = transcriber.transcribe(request.file_path, language=request.language)
        return {"text": result["text"], "segments": result["segments"], "language": request.language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
def generate_summary(request: GenerateRequest):
    """
    Generates documents/summaries from transcript using LLM.
    """
    try:
        if request.template_type == "meeting_notes":
            content = llm_client.generate_meeting_notes(request.transcript)
        else:
            # Fallback or generic summary
            prompt = f"Summarize the following transcript:\n\n{request.transcript}"
            content = llm_client.generate(prompt)
            
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
