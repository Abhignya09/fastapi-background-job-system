from sqlalchemy import Column, String
from app.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="pending")
    result = Column(String, nullable=True)