from sqlalchemy import Column, String, DateTime, Enum, Text, JSON
from sqlalchemy.sql import func
import uuid
from .session import Base
import enum

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(str, enum.Enum):
    AUDIO_UPLOAD = "audio_upload"
    YOUTUBE_URL = "youtube_url"

class TranscriptionProvider(str, enum.Enum):
    OPENAI = "openai"
    LOCAL = "local"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(JobType), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    transcription_provider = Column(String, nullable=True)
    
    # Input info
    input_path = Column(String, nullable=True)  # Path to local file or YouTube URL
    original_filename = Column(String, nullable=True)
    
    # Output info
    output_path = Column(String, nullable=True)  # Path to the final combined artifact or folder
    transcript_path = Column(String, nullable=True)
    summary_path = Column(String, nullable=True)
    
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "input_path": self.input_path,
            "original_filename": self.original_filename,
            "output_path": self.output_path,
            "transcript_path": self.transcript_path,
            "summary_path": self.summary_path,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
