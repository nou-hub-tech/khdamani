"""
Job Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_recruiter
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.schemas.job_application import JobApplicationCreate, JobApplicationResponse
from app.services.job_service import JobService
from app.services.job_application_service import JobApplicationService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 20,
    location: Optional[str] = None,
    title: Optional[str] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db),
):
    """
    Get all jobs with optional filters
    """
    job_service = JobService(db)
    jobs = await job_service.get_jobs(
        skip=skip,
        limit=limit,
        location=location,
        title=title,
        is_active=is_active
    )
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a single job by ID
    """
    job_service = JobService(db)
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    """
    Create a new job posting (recruiter only)
    """
    job_service = JobService(db)
    job = await job_service.create_job(job_data, current_user.id)
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    """
    Update a job posting (recruiter only)
    """
    job_service = JobService(db)
    job = await job_service.update_job(job_id, job_data, current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or access denied")
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    """
    Delete a job posting (recruiter only)
    """
    job_service = JobService(db)
    success = await job_service.delete_job(job_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or access denied")


@router.post("/{job_id}/apply", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    job_id: str,
    application_data: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply to a job (authenticated users only)
    """
    application_service = JobApplicationService(db)
    try:
        application = await application_service.apply_to_job(
            job_id=job_id,
            user_id=current_user.id,
            application_data=application_data
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

