"""
Job Repository
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job_posting import JobPosting
from app.schemas.job import JobCreate, JobUpdate


class JobRepository:
    """
    Repository for job data access
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        location: Optional[str] = None,
        title: Optional[str] = None,
        is_active: Optional[bool] = True
    ) -> List[JobPosting]:
        """
        Get all jobs with optional filters
        """
        query = self.db.query(JobPosting)
        
        if is_active is not None:
            query = query.filter(JobPosting.is_active == is_active)
        if location:
            # SQLite compatible case-insensitive search
            query = query.filter(JobPosting.location.like(f"%{location}%"))
        if title:
            # SQLite compatible case-insensitive search
            query = query.filter(JobPosting.title.like(f"%{title}%"))
        
        return query.order_by(JobPosting.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_id(self, job_id: str) -> Optional[JobPosting]:
        """
        Get job by ID
        """
        return self.db.query(JobPosting).filter(JobPosting.id == job_id).first()
    
    def create(self, job_data: JobCreate, recruiter_id: str) -> JobPosting:
        """
        Create a new job
        """
        job = JobPosting(**job_data.model_dump(), recruiter_id=recruiter_id)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def update(
        self,
        job_id: str,
        job_data: JobUpdate,
        recruiter_id: str
    ) -> Optional[JobPosting]:
        """
        Update a job
        """
        job = self.get_by_id(job_id)
        if not job or job.recruiter_id != recruiter_id:
            return None
        
        update_data = job_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def delete(self, job_id: str, recruiter_id: str) -> bool:
        """
        Delete a job
        """
        job = self.get_by_id(job_id)
        if not job or job.recruiter_id != recruiter_id:
            return False
        
        self.db.delete(job)
        self.db.commit()
        return True

