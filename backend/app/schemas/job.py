"""
Job Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class JobBase(BaseModel):
    title: str
    description: str
    location: str
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    required_skills: List[str] = []


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    required_skills: Optional[List[str]] = None


class JobResponse(JobBase):
    id: str
    recruiter_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

