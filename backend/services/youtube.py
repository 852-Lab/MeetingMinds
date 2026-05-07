import os
import re
import json
import queue
import threading
from youtube_transcript_api import YouTubeTranscriptApi
from .downloader import download_youtube_audio
from .scribe import transcriber

def get_video_id(url: str) -> str:
    """
    Extracts video ID from a YouTube URL, including /live/, /v/, /embed/, etc.
    """
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?|live|shorts)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def transcribe_youtube(url: str, storage_dir: str):
    """
    Handles YouTube transcription with prioritized caption fetching and AI fallback.
    Yields status updates as JSON strings.
    """
    video_id = get_video_id(url)
    if not video_id:
        yield json.dumps({"type": "error", "message": f"Invalid YouTube URL: {url}"})
        return

    output_file = os.path.join(storage_dir, f"{video_id}_transcript.txt")
    
    # 1. Try Captions
    try:
        yield json.dumps({"type": "status", "message": f"Attempting to fetch captions for {video_id}..."})
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        consolidated_text = " ".join([s['text'] if isinstance(s, dict) else s.text for s in transcript])
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(consolidated_text)
            
        yield json.dumps({
            "type": "complete",
            "method": "captions",
            "text": consolidated_text,
            "file_path": output_file
        })
        return
    except Exception as e:
        yield json.dumps({"type": "status", "message": "Captions unavailable. Falling back to Vibe AI transcription..."})
        print(f"Captions unavailable for {video_id}: {e}")
        
    # 2. Fallback to AI Transcription (Vibe/Sona)
    audio_path = None
    try:
        yield json.dumps({"type": "status", "message": "Downloading high-quality audio from YouTube..."})
        
        progress_q = queue.Queue()
        def progress_callback(p):
            progress_q.put(p)
            
        def run_download():
            nonlocal audio_path
            try:
                audio_path = download_youtube_audio(url, storage_dir, progress_callback=progress_callback)
                progress_q.put("DONE")
            except Exception as de:
                progress_q.put(f"ERROR: {str(de)}")

        thread = threading.Thread(target=run_download, daemon=True)
        thread.start()
        
        while True:
            try:
                item = progress_q.get(timeout=0.1)
                if item == "DONE":
                    break
                if isinstance(item, str) and item.startswith("ERROR:"):
                    raise RuntimeError(item[6:])
                yield json.dumps({"type": "progress", "progress": item})
            except queue.Empty:
                if not thread.is_alive():
                    break
        
        if not audio_path or not os.path.exists(audio_path):
            raise RuntimeError("Download failed: Audio file not found")

        file_size = os.path.getsize(audio_path)
        yield json.dumps({
            "type": "status", 
            "message": f"Download complete ({file_size/1024/1024:.1f} MB). Starting AI transcription...", 
            "progress": 100
        })
        
        # Start Vibe Transcription
        print(f"Transcribing with Vibe: {audio_path}")
        result = transcriber.transcribe(audio_path)
        consolidated_text = result.get("text", "")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(consolidated_text)
            
        yield json.dumps({
            "type": "complete",
            "method": "vibe",
            "text": consolidated_text,
            "file_path": output_file,
            "segments": result.get("segments", [])
        })
    except Exception as ve:
        error_msg = str(ve).split("ERROR:")[-1].strip()
        yield json.dumps({"type": "error", "message": f"Vibe transcription failed: {error_msg}"})
    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception as fe:
                print(f"Cleanup failed for {audio_path}: {fe}")
