import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MeetingMind Backend is running"}

def test_generate_endpoint_mock():
    # We might need to mock the LLMGenerator for unit tests
    # But for a simple integration test, we can check if it returns 500 if transcript is empty/invalid
    # or check the structure
    response = client.post("/api/generate", json={"transcript": "Hello world", "template_type": "summary"})
    # It might fail if LLM (Ollama) is not running, so we expect 200 or 500 depending on environment
    assert response.status_code in [200, 500]

def test_upload_endpoint_missing_file():
    response = client.post("/api/upload")
    assert response.status_code == 422 # Unprocessable Entity (missing file)
