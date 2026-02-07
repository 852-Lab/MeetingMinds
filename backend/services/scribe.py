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
        Transcribes audio file with progress updates.
        Yields progress updates during transcription, then yields the final result.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Get audio duration for progress estimation
        duration = get_audio_duration(audio_path)
        
        # Shared state between threads
        result_holder = {"result": None, "error": None, "done": False}
        
        def run_transcription():
            try:
                options = {}
                if language:
                    options["language"] = language
                with self.lock:
                    result_holder["result"] = self.model.transcribe(audio_path, **options)
            except Exception as e:
                result_holder["error"] = e
            finally:
                result_holder["done"] = True
        
        # Start transcription in background thread
        thread = threading.Thread(target=run_transcription)
        thread.start()
        
        # Yield progress updates while transcription is running
        start_time = time.time()
        if duration:
            # Estimate transcription takes 2x audio duration (conservative)
            estimated_total_time = duration * 2
        else:
            # If we can't get duration, just report that work is happening
            estimated_total_time = None
        
        last_progress = 0
        while not result_holder["done"]:
            time.sleep(2)  # Update every 2 seconds
            
            if estimated_total_time:
                elapsed = time.time() - start_time
                progress = min(95, int((elapsed / estimated_total_time) * 100))
                
                # Only yield if progress increased
                if progress > last_progress:
                    last_progress = progress
                    yield {"progress": progress, "done": False}
            else:
                # No duration info, just pulse to show activity
                yield {"progress": None, "done": False}
        
        thread.join()
        
        # Check for errors
        if result_holder["error"]:
            raise result_holder["error"]
        
        # Yield final result
        yield {"result": result_holder["result"], "progress": 100, "done": True}


# Global instance (lazy load ensured by property)
transcriber = Transcriber(model_name="base")
