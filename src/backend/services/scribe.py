import os
import subprocess
import time
import requests
import atexit
import threading
import signal
import traceback

class SonaTranscriber:
    def __init__(self, binary_path=None, model_path=None, port=52341):
        # Paths from environment or defaults
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.binary_path = os.getenv("SONA_BINARY_PATH", binary_path or os.path.join(base_dir, "bin", "sona"))
        
        # Default model path
        default_model = os.path.join(base_dir, "models", "ggml-large-v3-turbo.bin")
        self.model_path = os.getenv("WHISPER_MODEL_PATH", model_path or default_model)
        
        # Fallback to Mac path if not in Docker and default doesn't exist
        if not os.path.exists(self.model_path) and not os.path.exists(default_model):
            mac_path = os.path.expanduser("~/Library/Application Support/github.com.thewh1teagle.vibe/ggml-large-v3-turbo.bin")
            if os.path.exists(mac_path):
                self.model_path = mac_path
        
        self.port = port
        self.host = "127.0.0.1"
        self.base_url = f"http://{self.host}:{self.port}/v1"
        self._process = None
        self._lock = threading.Lock()
        
        # Register cleanup
        atexit.register(self.stop)

    def _download_model(self):
        """Downloads the Whisper model if it's missing."""
        model_url = f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/{os.path.basename(self.model_path)}"
        print(f"Downloading model from {model_url}...")
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        try:
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(self.model_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0 and downloaded % (1024 * 1024 * 10) == 0: # Print every 10MB
                            print(f"Downloaded {downloaded // (1024 * 1024)}MB / {total_size // (1024 * 1024)}MB")
            
            print(f"Model downloaded successfully to {self.model_path}")
        except Exception as e:
            print(f"Error downloading model: {e}")
            if os.path.exists(self.model_path):
                os.remove(self.model_path)
            raise RuntimeError(f"Failed to download Whisper model: {e}")

    def _ensure_server_running(self):
        with self._lock:
            # Check if already responding
            try:
                resp = requests.get(f"{self.base_url}/models", timeout=1)
                if resp.status_code == 200:
                    return True
            except:
                pass

            if not os.path.exists(self.binary_path):
                raise FileNotFoundError(f"Sona binary not found at {self.binary_path}. Please ensure it is copied to backend/bin/sona")

            if not os.path.exists(self.model_path):
                # Try to find any other ggml model in the same directory
                model_dir = os.path.dirname(self.model_path)
                if os.path.exists(model_dir):
                    models = [f for f in os.listdir(model_dir) if f.endswith(".bin") and f.startswith("ggml")]
                    if models:
                        self.model_path = os.path.join(model_dir, models[0])
                        print(f"Using alternative model: {self.model_path}")
                    else:
                        print(f"Model not found at {self.model_path}. Attempting to download...")
                        self._download_model()
                else:
                    print(f"Model directory {model_dir} not found. Attempting to download...")
                    self._download_model()

            print(f"Starting Sona server on port {self.port} with model {os.path.basename(self.model_path)}...")
            
            # Start process
            cmd = [self.binary_path, "serve", self.model_path, "--port", str(self.port)]
            self._process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid # Ensure it can be killed with its group
            )
            
            # Wait for ready
            for i in range(20):
                try:
                    resp = requests.get(f"{self.base_url}/models", timeout=1)
                    if resp.status_code == 200:
                        print("Sona server is ready.")
                        return True
                except:
                    time.sleep(1)
            
            raise RuntimeError("Timed out waiting for Sona server to start")

    def transcribe(self, audio_path: str, language: str = None) -> dict:
        """
        Transcribes audio file using Sona API.
        Returns a dict with 'text' and 'segments'.
        """
        self._ensure_server_running()
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        url = f"{self.base_url}/audio/transcriptions"
        
        with open(audio_path, "rb") as f:
            files = {"file": f}
            data = {
                "model": os.path.basename(self.model_path),
                "response_format": "verbose_json",
            }
            if language:
                data["language"] = language

            print(f"Sending transcription request for {audio_path}...")
            response = requests.post(url, files=files, data=data)
            
            if response.status_code != 200:
                raise RuntimeError(f"Transcription failed ({response.status_code}): {response.text}")
                
            return response.json()

    def stop(self):
        if self._process:
            print("Shutting down Sona server...")
            try:
                os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
                self._process.wait(timeout=5)
            except:
                pass
            self._process = None

# Global instance
transcriber = SonaTranscriber()
