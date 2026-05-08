import os
import requests
import logging
import time

logger = logging.getLogger(__name__)

class SonaTranscriber:
    def __init__(self, base_url=None):
        # Default to the service name in Docker Compose
        self.base_url = os.getenv("SONA_URL", base_url or "http://sona:8000/v1")
        logger.info(f"SonaTranscriber initialized with base_url: {self.base_url}")

    def is_ready(self):
        """
        Check if Sona server is responding (non-blocking).
        """
        try:
            resp = requests.get(f"{self.base_url}/models", timeout=1)
            return resp.status_code == 200
        except:
            return False

    def _ensure_server_ready(self):
        """
        Check if Sona server is responding.
        Wait up to 60 seconds (useful during initial model download).
        """
        for i in range(60):
            try:
                resp = requests.get(f"{self.base_url}/models", timeout=2)
                if resp.status_code == 200:
                    return True
            except:
                if i % 10 == 0:
                    logger.info("Waiting for Sona server to be ready...")
                time.sleep(1)
        
        logger.error("Timed out waiting for Sona server to start")
        raise RuntimeError("Sona transcription server is not responding. It might still be downloading the model.")

    def transcribe(self, audio_path: str, language: str = None) -> dict:
        """
        Transcribes audio file using Sona API.
        Returns a dict with 'text' and 'segments'.
        """
        self._ensure_server_ready()
        
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        url = f"{self.base_url}/audio/transcriptions"
        
        # We don't need to specify model path here as server is already running with a model
        # but the API requires a model name in the request
        model_name = "whisper-1"
        
        with open(audio_path, "rb") as f:
            files = {"file": f}
            data = {
                "model": model_name,
                "response_format": "verbose_json",
            }
            if language:
                data["language"] = language

            logger.info(f"Sending transcription request to Sona server for {audio_path}...")
            try:
                response = requests.post(url, files=files, data=data, timeout=600)
                
                if response.status_code != 200:
                    logger.error(f"Sona transcription failed ({response.status_code}): {response.text}")
                    raise RuntimeError(f"Transcription failed ({response.status_code}): {response.text}")
                    
                logger.info("Successfully received transcription from Sona server")
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Request to Sona server failed: {str(e)}")
                raise e

    def stop(self):
        # No process to stop anymore as it's managed by Docker
        pass

# Global instance
transcriber = SonaTranscriber()
