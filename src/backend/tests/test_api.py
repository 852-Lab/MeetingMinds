import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

test_dir = tempfile.mkdtemp()
db_path = os.path.join(test_dir, "test_api.db")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from main import app
from database.session import Base, get_db

engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MeetingMind Backend is running"}

@patch("api.routers.generation.llm_client.generate")
@patch("api.routers.generation.llm_client.generate_meeting_notes")
def test_generate_endpoint(mock_notes, mock_gen):
    mock_notes.return_value = "Mocked Meeting Notes"
    mock_gen.return_value = "Mocked Summary"

    response = client.post("/api/generate", json={"transcript": "Hello", "template_type": "meeting_notes"})
    assert response.status_code == 200
    assert response.json() == {"content": "Mocked Meeting Notes"}

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

def test_upload_file():
    file_content = b"fake audio content"
    files = {"file": ("test.mp3", file_content, "audio/mpeg")}

    with patch("shutil.copyfileobj"), patch("os.makedirs"):
        response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Upload successful, job queued"
    assert data["original_filename"] == "test.mp3"
    assert "job_id" in data

