import os
import subprocess
import time
import requests
import atexit
import threading
import signal

class SonaTranscriber:
    def __init__(self, binary_path=None, model_path=None, port=52341):
        # Paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.binary_path = binary_path or os.path.join(base_dir, "bin", "sona")
        
        # Default model path from Vibe installation on Mac
        self.model_path = model_path or os.path.expanduser("~/Library/Application Support/github.com.thewh1teagle.vibe/ggml-large-v3-turbo.bin")
        
        self.port = port
        self.host = "127.0.0.1"
        self.base_url = f"http://{self.host}:{self.port}/v1"
        self._process = None
        self._lock = threading.Lock()
        
        # Register cleanup
        atexit.register(self.stop)

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
                        raise FileNotFoundError(f"Whisper model not found at {self.model_path}. Please download a model using Vibe app or 'sona pull'")
                else:
                    raise FileNotFoundError(f"Whisper model not found at {self.model_path}")

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
