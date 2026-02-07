import whisper
import os
import torch

class Transcriber:
    def __init__(self, model_name="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model '{model_name}' on {self.device}...")
        self.model = whisper.load_model(model_name, device=self.device)

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

        result = self.model.transcribe(audio_path, **options)
        return result

# Global instance (lazy load or startup load could be better, but for now global)
# We might want to load this on startup in main.py to avoid delay on first request
# or keep it here.
transcriber = Transcriber(model_name="base")
