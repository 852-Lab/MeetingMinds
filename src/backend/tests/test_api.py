import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

test_dir = tempfile.mkdtemp()
db_path = os.path.join(test_dir, "test_api.db")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MeetingMind Backend is running"}

@patch("api.routers.generation.llm_client.generate")
@patch("api.routers.generation.llm_client.generate_meeting_notes")
def test_generate_endpoint(mock_notes, mock_gen):
    mock_notes.return_value = "Mocked Meeting Notes"
    mock_gen.return_value = "Mocked Summary"
    
    # Test meeting_notes template
    response = client.post("/api/generate", json={"transcript": "Hello", "template_type": "meeting_notes"})
    assert response.status_code == 200
    assert response.json() == {"content": "Mocked Meeting Notes"}
    
    # Test summary template
    response = client.post("/api/generate", json={"transcript": "Hello", "template_type": "summary"})
    assert response.status_code == 200
    assert response.json() == {"content": "Mocked Summary"}

@patch("api.routers.generation.download_youtube_audio")
def test_download_endpoint(mock_download):
    mock_download.return_value = "storage/test.mp3"
    response = client.post("/api/download", json={"url": "https://youtube.com/watch?v=123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Download successful", "file_path": "storage/test.mp3"}

def test_upload_endpoint_missing_file():
    response = client.post("/api/upload")
    assert response.status_code == 422

@patch("api.routers.transcription.extract_audio")
def test_upload_m4a(mock_extract):
    mock_extract.return_value = "storage/test_processed.wav"
    
    # Create a dummy m4a file content
    file_content = b"fake m4a content"
    files = {"file": ("test.m4a", file_content, "audio/mp4")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Upload successful"
    assert response.json()["original_filename"] == "test.m4a"
    assert "_processed.wav" in response.json()["file_path"]

@patch("api.routers.transcription.transcriber.transcribe")
def test_transcribe_endpoint(mock_transcribe):
    mock_transcribe.return_value = {"text": "Transcribed text", "segments": []}
    
    # Mock os.path.exists to return True for the test path
    with patch("os.path.exists", return_value=True):
        response = client.post("/api/transcribe", json={"file_path": "test.wav", "language": "en"})
        assert response.status_code == 200
        assert response.json()["text"] == "Transcribed text"
