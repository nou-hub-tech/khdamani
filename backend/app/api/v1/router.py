"""
API Router - Aggregates all API endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    job_seekers,
    recruiters,
    jobs,
    applications,
    ml_services,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(job_seekers.router, prefix="/job-seekers", tags=["job-seekers"])
api_router.include_router(recruiters.router, prefix="/recruiters", tags=["recruiters"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(ml_services.router, prefix="/ml", tags=["ml-services"])

