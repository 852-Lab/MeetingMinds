from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from services.llm import LLMGenerator
from services.downloader import download_youtube_audio

router = APIRouter(prefix="/api", tags=["generation"])

STORAGE_DIR = "storage"
llm_client = LLMGenerator(model="gemma3:4b")

class DownloadRequest(BaseModel):
    url: str

class GenerateRequest(BaseModel):
    transcript: str
    template_type: str = "meeting_notes"

@router.post("/download")
async def download_video(request: DownloadRequest):
    """
    Downloads audio from YouTube URL.
    """
    try:
        file_path = download_youtube_audio(request.url, STORAGE_DIR)
        return {"message": "Download successful", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
def generate_summary(request: GenerateRequest):
    """
    Generates documents/summaries from transcript using LLM.
    """
    try:
        if request.template_type == "meeting_notes":
            content = llm_client.generate_meeting_notes(request.transcript)
        else:
            prompt = f"Summarize the following transcript:\n\n{request.transcript}"
            content = llm_client.generate(prompt)
            
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
