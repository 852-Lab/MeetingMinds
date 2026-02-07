import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class LLMGenerator:
    def __init__(self, model="llama3.2"):
        self.model = model

    def generate(self, prompt: str, system: str = None) -> str:
        """
        Generates text using Ollama.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Ollama API Error: {e}")
            raise e

    def generate_meeting_notes(self, transcript: str) -> str:
        system_prompt = "You are a helpful assistant that summarizes meeting transcripts."
        prompt = f"""
        Please generate comprehensive meeting notes for the following transcript.
        Include:
        - Executive Summary
        - Key Discussion Points
        - Action Items (with assignees if mentioned)
        
        Transcript:
        {transcript}
        """
        return self.generate(prompt, system_prompt)

llm_service = LLMGenerator()
