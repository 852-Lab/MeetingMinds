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
    Case 1: YouTube videos with caption enabled.
    Case 2: YouTube videos without caption enabled (fallback to Whisper).
    Yields status updates as JSON strings.
    """
    video_id = get_video_id(url)
    if not video_id:
        yield json.dumps({"type": "error", "message": f"Invalid YouTube URL: {url}"})
        return

    output_file = os.path.join(storage_dir, f"{video_id}_transcript.txt")
    
    # Try fetching captions (Case 1)
    try:
        yield json.dumps({"type": "status", "message": f"Attempting to fetch captions for video: {video_id}..."})
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        consolidated_text = " ".join([snippet['text'] if isinstance(snippet, dict) else snippet.text for snippet in transcript])
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(consolidated_text)
            
        yield json.dumps({
            "type": "complete",
            "method": "captions",
            "text": consolidated_text,
            "file_path": output_file
        })
        return
    except Exception as caption_error:
        yield json.dumps({"type": "status", "message": f"Captions unavailable. Falling back to AI transcription (this will take longer)..."})
        print(f"Could not fetch captions for {video_id}: {caption_error}")
        
        # Fallback to audio transcription (Case 2)
        audio_path = None
        try:
            yield json.dumps({"type": "status", "message": "Downloading audio from YouTube..."})
            
            progress_q = queue.Queue()
            def progress_callback(p):
                progress_q.put(p)
                
            def run_download():
                nonlocal audio_path
                try:
                    audio_path = download_youtube_audio(url, storage_dir, progress_callback=progress_callback)
                    progress_q.put("DONE")
                except Exception as e:
                    progress_q.put(f"ERROR: {str(e)}")

            thread = threading.Thread(target=run_download)
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
                raise RuntimeError(f"Download failed: Audio file not found")

            # Check file size
            file_size = os.path.getsize(audio_path)
            yield json.dumps({"type": "status", "message": f"Download complete (Size: {file_size/1024/1024:.2f} MB). Starting transcription...", "progress": 100})
            
            if file_size == 0:
                raise RuntimeError("Downloaded audio file is empty (0 bytes).")

            print(f"Transcribing audio with Whisper: {audio_path} ({file_size} bytes)")
            result = transcriber.transcribe(audio_path)
            consolidated_text = result["text"]
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(consolidated_text)
                
            yield json.dumps({
                "type": "complete",
                "method": "whisper",
                "text": consolidated_text,
                "file_path": output_file,
                "segments": result["segments"]
            })
        except Exception as whisper_error:
            error_msg = str(whisper_error).split("ERROR:")[-1].strip() if "ERROR:" in str(whisper_error) else str(whisper_error)
            yield json.dumps({"type": "error", "message": f"Transcription failed: {error_msg}"})
        finally:
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    print(f"Failed to remove temporary audio file {audio_path}: {e}")
