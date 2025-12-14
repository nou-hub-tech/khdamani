"""
Job Application Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_job_seeker, get_current_recruiter
from app.schemas.job_application import JobApplicationResponse
from app.services.job_application_service import JobApplicationService
from app.models.user import User

router = APIRouter()


@router.get("/my-applications", response_model=List[JobApplicationResponse])
async def get_my_applications(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_job_seeker),
    db: Session = Depends(get_db),
):
    """
    Get all applications for the current job seeker
    """
    application_service = JobApplicationService(db)
    applications = await application_service.get_user_applications(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return applications


@router.get("/job/{job_id}", response_model=List[JobApplicationResponse])
async def get_job_applications(
    job_id: str,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    """
    Get all applications for a specific job (recruiter only)
    """
    application_service = JobApplicationService(db)
    try:
        applications = await application_service.get_job_applications(
            job_id=job_id,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return applications
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

