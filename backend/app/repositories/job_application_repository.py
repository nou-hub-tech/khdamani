"""
Job Application Repository
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job_application import JobApplication


class JobApplicationRepository:
    """
    Repository for job application data access
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, application_id: str) -> Optional[JobApplication]:
        """
        Get application by ID
        """
        return self.db.query(JobApplication).filter(JobApplication.id == application_id).first()
    
    def get_by_job_and_user(
        self,
        job_id: str,
        user_id: str
    ) -> Optional[JobApplication]:
        """
        Get application by job and user
        """
        return self.db.query(JobApplication).filter(
            JobApplication.job_id == job_id,
            JobApplication.job_seeker_id == user_id
        ).first()
    
    def get_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[JobApplication]:
        """
        Get all applications for a user
        """
        return self.db.query(JobApplication).filter(
            JobApplication.job_seeker_id == user_id
        ).order_by(JobApplication.applied_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_job(
        self,
        job_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[JobApplication]:
        """
        Get all applications for a job
        """
        return self.db.query(JobApplication).filter(
            JobApplication.job_id == job_id
        ).order_by(JobApplication.applied_at.desc()).offset(skip).limit(limit).all()
    
    def create(
        self,
        job_id: str,
        user_id: str,
        cover_letter: Optional[str] = None,
        resume_url: Optional[str] = None
    ) -> JobApplication:
        """
        Create a new job application
        """
        # Check if application already exists
        existing = self.get_by_job_and_user(job_id, user_id)
        if existing:
            raise ValueError("Application already exists for this job")
        
        application = JobApplication(
            job_id=job_id,
            job_seeker_id=user_id,
            status="APPLIED",
            cover_letter=cover_letter,
            resume_url=resume_url
        )
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application
    
    def update_status(
        self,
        application_id: str,
        status: str
    ) -> Optional[JobApplication]:
        """
        Update application status
        """
        application = self.get_by_id(application_id)
        if not application:
            return None
        
        application.status = status
        from datetime import datetime
        if status != "APPLIED":
            application.reviewed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(application)
        return application

