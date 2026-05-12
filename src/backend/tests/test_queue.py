import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

# Create a temporary directory for the test database
test_dir = tempfile.mkdtemp()
db_path = os.path.join(test_dir, "test_queue.db")

# Set DATABASE_URL before any app imports to avoid connection attempts to Postgres
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

# Now import the app and models
from main import app
from database.session import Base, get_db
from database.models import Job, JobStatus, JobType

# Setup test database (SQLite file in temp dir)
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)

def test_create_upload_job():
    """Test that uploading a file correctly creates a PENDING job."""
    file_content = b"fake audio content"
    files = {"file": ("test.mp3", file_content, "audio/mpeg")}
    
    with patch("shutil.copyfileobj"), patch("os.makedirs"):
        response = client.post("/api/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["message"] == "Upload successful, job queued"
    
    # Verify job in database
    job_id = data["job_id"]
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["id"] == job_id
    assert job_data["status"] == "pending"

def test_create_youtube_job():
    """Test that submitting a YouTube URL correctly creates a PENDING job."""
    response = client.post("/api/youtube-transcribe", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["message"] == "Job created"
    
    # Verify job in database
    job_id = data["job_id"]
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["type"] == "youtube_url"

def test_list_jobs():
    """Test retrieving the list of all jobs."""
    db = TestingSessionLocal()
    job1 = Job(id="job1", type=JobType.AUDIO_UPLOAD, status=JobStatus.PENDING, input_path="path1")
    job2 = Job(id="job2", type=JobType.YOUTUBE_URL, status=JobStatus.COMPLETED, input_path="path2")
    db.add(job1)
    db.add(job2)
    db.commit()
    db.close()
    
    response = client.get("/api/jobs")
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 2

def test_worker_processing_success():
    """Test the worker's processing logic (mocked)."""
    from worker import process_job
    db = TestingSessionLocal()
    
    job = Job(
        id="worker_test_job",
        type=JobType.YOUTUBE_URL,
        status=JobStatus.PENDING,
        input_path="https://youtube.com/test"
    )
    db.add(job)
    db.commit()
    
    # Mock YouTube transcript and LLM summarization
    with patch("worker.YouTubeTranscriptApi.fetch") as mock_fetch, \
         patch("worker.llm_service.generate_meeting_notes") as mock_summarize, \
         patch("os.makedirs"), \
         patch("builtins.open", MagicMock()):
        
        mock_fetch.return_value = [{"text": "Hello from YouTube"}]
        mock_summarize.return_value = "Summary of YouTube video"
        
        process_job(db, job)
        
        db.refresh(job)
        assert job.status == JobStatus.COMPLETED

def test_worker_processing_failure():
    """Test that the worker correctly handles and records failures."""
    from worker import process_job
    db = TestingSessionLocal()
    
    job = Job(
        id="failed_job",
        type=JobType.YOUTUBE_URL,
        status=JobStatus.PENDING,
        input_path="https://youtube.com/invalid"
    )
    db.add(job)
    db.commit()
    
    # Mock failure in transcript fetching
    with patch("worker.YouTubeTranscriptApi.fetch", side_effect=Exception("API Error")):
        with patch("worker.download_youtube_audio", side_effect=Exception("Download Error")):
            process_job(db, job)
        
        db.refresh(job)
        assert job.status == JobStatus.FAILED
