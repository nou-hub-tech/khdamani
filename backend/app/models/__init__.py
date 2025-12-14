"""
Models Package
Import all models here for Alembic autogenerate
"""

from app.models.user import User, UserRole
from app.models.job_seeker_profile import JobSeekerProfile
from app.models.recruiter_profile import RecruiterProfile
from app.models.job_posting import JobPosting
from app.models.job_application import JobApplication
from app.models.ml_models import (
    SalaryPrediction,
    FraudDetectionResult,
    CountryRecommendation,
    JobRecommendation,
    UserJobInteraction,
)
from app.models.enums import (
    ExperienceLevel,
    EducationLevel,
    EmploymentType,
    ApplicationStatus,
    CompanySize,
)

__all__ = [
    "User",
    "UserRole",
    "JobSeekerProfile",
    "RecruiterProfile",
    "JobPosting",
    "JobApplication",
    "SalaryPrediction",
    "FraudDetectionResult",
    "CountryRecommendation",
    "JobRecommendation",
    "UserJobInteraction",
    "ExperienceLevel",
    "EducationLevel",
    "EmploymentType",
    "ApplicationStatus",
    "CompanySize",
]
