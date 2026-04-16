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
        time.sleep(10)

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
@router.post(
    "/submit",
    summary="Submit a new job",
    description="Creates a new job and processes it asynchronously in the background.",
    response_description="Returns the created job ID"
)
def submit_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job_id = str(uuid.uuid4())
    job = Job(id=job_id, status="pending")
    db.add(job)
    time.sleep(3)
    db.commit()

    background_tasks.add_task(process_job, job_id)

    return {
        "message": "Job submitted successfully",
        "job_id": job_id
    }

# 🔹 Get Job Status
@router.get(
    "/status/{job_id}",
    summary="Get job status",
    description="Returns current status and result of a job.",
    responses={
        200: {"description": "Job found"},
        404: {"description": "Job not found"}
    }
)
def get_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job.status,
        "result": job.result
    }


