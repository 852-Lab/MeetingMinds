import os
import re
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

def transcribe_youtube(url: str, storage_dir: str) -> dict:
    """
    Case 1: YouTube videos with caption enabled.
    Case 2: YouTube videos without caption enabled (fallback to Whisper).
    """
    video_id = get_video_id(url)
    if not video_id:
        print(f"Failed to extract video ID from URL: {url}")
        raise ValueError(f"Invalid YouTube URL: {url}")

    output_file = os.path.join(storage_dir, f"{video_id}_transcript.txt")
    
    # Try fetching captions (Case 1)
    try:
        print(f"Attempting to fetch captions for video: {video_id}")
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        consolidated_text = " ".join([snippet.text for snippet in transcript])
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(consolidated_text)
            
        return {
            "method": "captions",
            "text": consolidated_text,
            "file_path": output_file,
            "segments": transcript.to_raw_data()
        }
    except Exception as caption_error:
        print(f"Could not fetch captions for {video_id}: {caption_error}")
        print(f"Falling back to audio transcription (Whisper) for {url}")
        
        # Fallback to audio transcription (Case 2)
        # Note: download_youtube_audio already has internal retries
        audio_path = None
        try:
            audio_path = download_youtube_audio(url, storage_dir)
            if not audio_path or not os.path.exists(audio_path):
                raise RuntimeError(f"Download failed: Audio file not found at {audio_path}")

            print(f"Transcribing audio with Whisper: {audio_path}")
            result = transcriber.transcribe(audio_path)
            consolidated_text = result["text"]
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(consolidated_text)
                
            return {
                "method": "whisper",
                "text": consolidated_text,
                "file_path": output_file,
                "segments": result["segments"]
            }
        except Exception as whisper_error:
            print(f"Fallback transcription failed for {url}: {whisper_error}")
            # Raise a more descriptive error for the frontend
            raise RuntimeError(f"Transcription failed: Captions unavailable and fallback failed. {whisper_error}")
        finally:
            # Clean up audio file after transcription
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    print(f"Failed to remove temporary audio file {audio_path}: {e}")
