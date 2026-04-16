from pydantic import BaseModel
from typing import Optional

class JobCreateResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    status: str
    result: Optional[str] = None