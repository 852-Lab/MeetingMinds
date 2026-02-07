import whisper
import os
import torch
import threading

class Transcriber:
    def __init__(self, model_name="base"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
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

# Global instance (lazy load ensured by property)
transcriber = Transcriber(model_name="base")
