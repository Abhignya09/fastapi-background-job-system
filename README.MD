# Background Job Processing System (FastAPI)

## Overview

This project implements an asynchronous job processing system using FastAPI.

## Features

- Submit jobs
- Track job status
- Background processing
- Job lifecycle: pending → in_progress → completed

## Tech Stack

- FastAPI
- SQLite
- SQLAlchemy

## Setup Instructions

1. Clone repo:
   git clone <your-repo-link>

2. Navigate:
   cd job-system

3. Install dependencies:
   pip install -r requirements.txt

4. Run server:
   uvicorn app.main:app --reload

5. Open Swagger:
   http://127.0.0.1:8000/docs

## API Endpoints

### Submit Job

POST /jobs/submit

Response:
{
"job_id": "uuid"
}

### Get Job Status

GET /jobs/status/{job_id}

Response:
{
"status": "pending | in_progress | completed",
"result": "string"
}

## Assumptions

- BackgroundTasks used instead of external queue (Celery)
- SQLite used for simplicity
