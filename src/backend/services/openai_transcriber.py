import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAITranscriber:
    def transcribe(self, audio_path: str, api_key: str, language: str = None) -> dict:
        client = OpenAI(api_key=api_key)
        with open(audio_path, "rb") as f:
            params = {
                "model": "whisper-1",
                "file": f,
                "response_format": "verbose_json",
            }
            if language:
                params["language"] = language
            logger.info(f"Sending transcription request to OpenAI Whisper for {audio_path}...")
            result = client.audio.transcriptions.create(**params)
        logger.info("Successfully received transcription from OpenAI")
        return {
            "text": result.text,
            "segments": [s.model_dump() for s in result.segments] if result.segments else [],
        }

openai_transcriber = OpenAITranscriber()
