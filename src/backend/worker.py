import time
import os
import shutil
import logging
from database.session import SessionLocal, engine
from database.models import Job, JobStatus, JobType, Base, TranscriptionProvider
from services.audio import extract_audio
from services.youtube import get_video_id
from youtube_transcript_api import YouTubeTranscriptApi
from services.downloader import download_youtube_audio
from services.scribe import transcriber
from services.openai_transcriber import openai_transcriber
from services.llm import llm_service
from api.routers.settings import get_decrypted_openai_key
from sqlalchemy.orm import Session

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

STORAGE_DIR = os.getenv("STORAGE_DIR", "data")
INPUT_DIR = os.path.join(STORAGE_DIR, "input")
OUTPUT_DIR = os.path.join(STORAGE_DIR, "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def _transcribe(audio_path: str, openai_api_key: str | None) -> tuple[dict, TranscriptionProvider]:
    if openai_api_key:
        logger.info("OpenAI API key configured — using OpenAI Whisper")
        return openai_transcriber.transcribe(audio_path, openai_api_key), TranscriptionProvider.OPENAI
    logger.info("No OpenAI key — using local Sona transcription")
    return transcriber.transcribe(audio_path), TranscriptionProvider.LOCAL

def process_job(db: Session, job: Job):
    job.status = JobStatus.PROCESSING
    db.commit()
    db.refresh(job)

    openai_api_key = get_decrypted_openai_key(db)

    try:
        transcript_text = ""

        if job.type == JobType.AUDIO_UPLOAD:
            processed_wav = os.path.join(INPUT_DIR, f"{job.id}_processed.wav")

            logger.info(f"Extracting audio from {job.input_path} to {processed_wav}...")
            extract_audio(job.input_path, processed_wav)

            logger.info(f"Transcribing {processed_wav}...")
            result, provider = _transcribe(processed_wav, openai_api_key)
            job.transcription_provider = provider
            transcript_text = result["text"]

        elif job.type == JobType.YOUTUBE_URL:
            url = job.input_path
            video_id = get_video_id(url)

            # Step 1: Try Captions
            try:
                logger.info(f"Attempting to fetch captions for {video_id}...")
                api = YouTubeTranscriptApi()
                transcript = api.fetch(video_id)
                transcript_text = " ".join([s['text'] if isinstance(s, dict) else s.text for s in transcript])
                logger.info(f"Successfully fetched captions for {video_id}")
            except Exception as e:
                logger.info(f"Captions unavailable for {video_id}: {str(e)}. Falling back to AI transcription...")

                audio_path = download_youtube_audio(url, INPUT_DIR)
                logger.info(f"Transcribing downloaded audio: {audio_path}")
                result, provider = _transcribe(audio_path, openai_api_key)
                job.transcription_provider = provider
                transcript_text = result["text"]

                if os.path.exists(audio_path):
                    os.remove(audio_path)
        
        if not transcript_text:
            raise ValueError("No transcript generated")

        # Save transcript to output
        transcript_filename = f"{job.id}_transcript.txt"
        transcript_path = os.path.join(OUTPUT_DIR, transcript_filename)
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        job.transcript_path = transcript_path
        
        # Step 3: Summarize
        logger.info(f"Generating summary for job {job.id}...")
        summary_text = llm_service.generate_meeting_notes(transcript_text)
        
        # Save summary to output
        summary_filename = f"{job.id}_summary.md"
        summary_path = os.path.join(OUTPUT_DIR, summary_filename)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        
        job.summary_path = summary_path
        job.status = JobStatus.COMPLETED
        
        db.commit()
        logger.info(f"Job {job.id} completed successfully.")
        
    except Exception as e:
        logger.error(f"Error processing job {job.id}: {str(e)}")
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        db.commit()

def run_worker():
    logger.info("Worker started. Polling for jobs...")
    while True:
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.status == JobStatus.PENDING).order_by(Job.created_at.asc()).first()
            if job:
                logger.info(f"Found pending job: {job.id}")
                process_job(db, job)
            else:
                time.sleep(5)
        finally:
            db.close()

if __name__ == "__main__":
    run_worker()
