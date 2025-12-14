"""
Job Service
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.repositories.job_repository import JobRepository


class JobService:
    """
    Service for handling job-related business logic
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
    
    async def get_jobs(
        self,
        skip: int = 0,
        limit: int = 20,
        location: Optional[str] = None,
        title: Optional[str] = None,
        is_active: Optional[bool] = True
    ) -> List[JobResponse]:
        """
        Get jobs with optional filters
        """
        jobs = self.job_repo.get_all(
            skip=skip,
            limit=limit,
            location=location,
            title=title,
            is_active=is_active
        )
        return [JobResponse.model_validate(job) for job in jobs]
    
    async def get_job_by_id(self, job_id: str) -> Optional[JobResponse]:
        """
        Get a single job by ID
        """
        job = self.job_repo.get_by_id(job_id)
        if job:
            return JobResponse.model_validate(job)
        return None
    
    async def create_job(self, job_data: JobCreate, recruiter_id: str) -> JobResponse:
        """
        Create a new job posting
        """
        job = self.job_repo.create(job_data, recruiter_id)
        return JobResponse.model_validate(job)
    
    async def update_job(
        self,
        job_id: str,
        job_data: JobUpdate,
        recruiter_id: str
    ) -> Optional[JobResponse]:
        """
        Update a job posting
        """
        job = self.job_repo.update(job_id, job_data, recruiter_id)
        if job:
            return JobResponse.model_validate(job)
        return None
    
    async def delete_job(self, job_id: str, recruiter_id: str) -> bool:
        """
        Delete a job posting
        """
        return self.job_repo.delete(job_id, recruiter_id)

