from fastapi import FastAPI
from app.db import Base, engine
from app.routes import jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Background Job Processing System",
    description="""
A simple backend system that handles asynchronous job processing.

Features:
- Submit background jobs
- Track job status (pending → in_progress → completed/failed)
- Simulated processing delay
- Error handling for invalid jobs
""",
    version="1.0.0",
    contact={
        "name": "FastAPI Assignment Project"
    }
)

app.include_router(jobs.router)