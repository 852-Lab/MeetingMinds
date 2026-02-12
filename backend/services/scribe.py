import whisper
import os
import torch
import threading
import time
import ffmpeg

def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds using ffmpeg."""
    try:
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"Could not determine audio duration: {e}")
        return None

class Transcriber:
    def __init__(self, model_name="base"):
        self.model_name = model_name
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"
        self._model = None
        self.lock = threading.Lock()

    @property
    def model(self):
        if self._model is None:
            with self.lock:
                if self._model is None:
                    print(f"Loading Whisper model '{self.model_name}' on {self.device}...")
                    self._model = whisper.load_model(self.model_name, device=self.device)
        return self._model

    def transcribe(self, audio_path: str, language: str = None) -> dict:
        """
        Transcribes audio file.
        language: 'en', 'de', 'zh', etc. or None for auto-detect.
        Returns detailed result with segments.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        options = {}
        if language:
            options["language"] = language

        with self.lock:
            result = self.model.transcribe(audio_path, **options)
        return result

    def transcribe_with_progress(self, audio_path: str, language: str = None):
        """
        Transcribed audio file with progress updates.
        Handles large files by splitting into 10-minute chunks.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # 1. IMMEDIATE YIELD
        if self._model is None:
            yield {"message": "Initializing AI Engine (this may take a moment)...", "progress": 0, "done": False}
        else:
            yield {"message": "AI Engine Ready. Analyzing audio...", "progress": 1, "done": False}

        duration = get_audio_duration(audio_path)
        CHUNK_LENGTH = 600  # 10 minutes in seconds

        if duration and duration > CHUNK_LENGTH:
            num_chunks = int(duration // CHUNK_LENGTH) + (1 if duration % CHUNK_LENGTH > 0 else 0)
            yield {"message": f"Long audio detected ({duration/60:.1f}m). Processing in {num_chunks} segments...", "progress": 2, "done": False}
            
            combined_text = ""
            combined_segments = []
            
            for i in range(num_chunks):
                start_time_sec = i * CHUNK_LENGTH
                chunk_path = f"{audio_path}_chunk_{i}.mp3"
                
                yield {"message": f"Preparing segment {i+1} of {num_chunks}...", "progress": int((i / num_chunks) * 100), "done": False}
                
                # Split using FFmpeg
                try:
                    (
                        ffmpeg
                        .input(audio_path, ss=start_time_sec, t=CHUNK_LENGTH)
                        .output(chunk_path, acodec='copy', loglevel="error")
                        .overwrite_output()
                        .run()
                    )
                except Exception as e:
                    yield {"message": f"Error splitting segment {i+1}: {str(e)}", "progress": None, "done": False}
                    # Fallback or skip? For now, we continue if possible
                
                if not os.path.exists(chunk_path):
                    continue

                # Process this chunk
                result_holder = {"result": None, "error": None, "done": False}
                def run_chunk_transcription():
                    try:
                        options = {"language": language} if language else {}
                        with self.lock:
                            result_holder["result"] = self.model.transcribe(chunk_path, **options)
                    except Exception as e:
                        result_holder["error"] = e
                    finally:
                        result_holder["done"] = True

                thread = threading.Thread(target=run_chunk_transcription)
                thread.start()

                while not result_holder["done"]:
                    time.sleep(1.5)
                    progress = int(((i + 0.5) / num_chunks) * 100) # Simple mid-chunk progress
                    msg = f"Transcribing segment {i+1} of {num_chunks} (Minutes {int(start_time_sec/60)}-{int((start_time_sec+CHUNK_LENGTH)/60)})..."
                    yield {"message": msg, "progress": progress, "done": False}

                thread.join()
                
                if result_holder["error"]:
                    # Cleanup if failed
                    if os.path.exists(chunk_path): os.remove(chunk_path)
                    raise result_holder["error"]

                # Aggregate
                chunk_result = result_holder["result"]
                combined_text += chunk_result["text"] + " "
                
                # Adjust segment timestamps
                for seg in chunk_result["segments"]:
                    seg["start"] += start_time_sec
                    seg["end"] += start_time_sec
                    combined_segments.append(seg)

                # Cleanup chunk
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)

            yield {"message": "Merging segments and finalizing...", "progress": 99, "done": False}
            yield {
                "result": {"text": combined_text.strip(), "segments": combined_segments},
                "progress": 100,
                "done": True,
                "message": "Transcription complete."
            }
        else:
            # ORIGINAL LOGIC for short files
            result_holder = {"result": None, "error": None, "done": False}
            def run_transcription():
                try:
                    options = {"language": language} if language else {}
                    with self.lock:
                        result_holder["result"] = self.model.transcribe(audio_path, **options)
                except Exception as e:
                    result_holder["error"] = e
                finally:
                    result_holder["done"] = True

            thread = threading.Thread(target=run_transcription)
            thread.start()
            
            start_time = time.time()
            estimated_total_time = (duration * 2) if duration else None
            
            while not result_holder["done"]:
                time.sleep(1.5)
                if estimated_total_time:
                    progress = min(98, int(((time.time() - start_time) / estimated_total_time) * 100))
                    yield {"message": "AI Pattern Recognition...", "progress": progress, "done": False}
                else:
                    yield {"message": "AI Processing Internal Patterns...", "progress": None, "done": False}

            thread.join()
            if result_holder["error"]: raise result_holder["error"]
            
            yield {"message": "Finalizing...", "progress": 100, "done": False}
            yield {"result": result_holder["result"], "progress": 100, "done": True, "message": "Transcription complete."}


# Global instance (lazy load ensured by property)
transcriber = Transcriber(model_name="base")
