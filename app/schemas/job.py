from typing import Dict, Optional
from pydantic import BaseModel

class JobCreate(BaseModel):
    prompt: str

class JobStatusResponse(BaseModel):
    job_id: int
    status: str
    result_url: Optional[str]
    error_message: Optional[str]
    retry_attempts: int
