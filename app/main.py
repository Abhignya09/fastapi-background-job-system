from fastapi import FastAPI
from app.db import Base, engine
from app.routes import jobs

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Background Job Processing API")

app.include_router(jobs.router)