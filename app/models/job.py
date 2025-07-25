from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: str
    # The next line ensures 'parameters' is stored as a JSON column in Postgres
    parameters: Optional[Dict[str, Any]] = Field(default={}, sa_column=Column(JSON, nullable=True))
    status: str = Field(default="queued")
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    retry_attempts: int = Field(default=0)
