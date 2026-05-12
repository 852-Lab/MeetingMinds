from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .models import JobStatus, JobType

class JobBase(BaseModel):
    type: JobType
    input_path: str
    original_filename: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: str
    status: JobStatus
    output_path: Optional[str] = None
    transcript_path: Optional[str] = None
    summary_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
