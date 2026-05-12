from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import Job
from database.schemas import JobResponse
from typing import List
import os

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.get("/", response_model=List[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/{job_id}/transcript")
def download_transcript(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or not job.transcript_path:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    if not os.path.exists(job.transcript_path):
         raise HTTPException(status_code=404, detail="File missing on disk")
         
    return FileResponse(job.transcript_path, filename=f"transcript_{job_id}.txt")

@router.get("/{job_id}/summary")
def download_summary(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or not job.summary_path:
        raise HTTPException(status_code=404, detail="Summary not found")
        
    if not os.path.exists(job.summary_path):
         raise HTTPException(status_code=404, detail="File missing on disk")
         
    return FileResponse(job.summary_path, filename=f"summary_{job_id}.md")
