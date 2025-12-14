"""
Job Application Service
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.job_application import JobApplicationCreate, JobApplicationResponse
from app.repositories.job_application_repository import JobApplicationRepository
from app.repositories.job_repository import JobRepository


class JobApplicationService:
    """
    Service for handling job application business logic
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.application_repo = JobApplicationRepository(db)
        self.job_repo = JobRepository(db)
    
    async def apply_to_job(
        self,
        job_id: str,
        user_id: str,
        application_data: JobApplicationCreate
    ) -> JobApplicationResponse:
        """
        Apply to a job
        """
        # Check if job exists and is active
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")
        if not job.is_active:
            raise ValueError("Job is not active")
        
        # Create application
        application = self.application_repo.create(
            job_id=job_id,
            user_id=user_id,
            cover_letter=application_data.cover_letter,
            resume_url=application_data.resume_url
        )
        
        return JobApplicationResponse.model_validate(application)
    
    async def get_user_applications(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[JobApplicationResponse]:
        """
        Get all applications for a user
        """
        applications = self.application_repo.get_by_user(user_id, skip=skip, limit=limit)
        return [JobApplicationResponse.model_validate(app) for app in applications]
    
    async def get_job_applications(
        self,
        job_id: str,
        user_id: str,  # Recruiter who owns the job
        skip: int = 0,
        limit: int = 20
    ) -> List[JobApplicationResponse]:
        """
        Get all applications for a job (recruiter only)
        """
        # Verify job belongs to recruiter
        job = self.job_repo.get_by_id(job_id)
        if not job or job.recruiter_id != user_id:
            raise ValueError("Job not found or access denied")
        
        applications = self.application_repo.get_by_job(job_id, skip=skip, limit=limit)
        return [JobApplicationResponse.model_validate(app) for app in applications]

