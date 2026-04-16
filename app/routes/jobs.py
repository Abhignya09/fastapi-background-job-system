from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import uuid
import time

from app.db import SessionLocal
from app.models import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Background processing function
def process_job(job_id: str):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return

        # Step 1: in_progress
        job.status = "in_progress"
        db.commit()

        # Simulate work
        time.sleep(16)

        # Step 2: completed
        job.status = "completed"
        job.result = "Job completed successfully"
        db.commit()

    except Exception:
        job.status = "failed"
        job.result = "Something went wrong"
        db.commit()

    finally:
        db.close()

# 🔹 Submit Job
@router.post("/submit")
def submit_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job_id = str(uuid.uuid4())

    new_job = Job(id=job_id, status="pending")
    db.add(new_job)
    db.commit()

    background_tasks.add_task(process_job, job_id)

    return {"job_id": job_id}

# 🔹 Get Job Status
@router.get("/status/{job_id}")
def get_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "status": job.status,
        "result": job.result
    }