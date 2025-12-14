"""
Job Application Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: str
    job_id: str
    job_seeker_id: str
    status: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    applied_at: datetime
    reviewed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

