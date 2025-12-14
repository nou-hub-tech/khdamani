"""
Job Recommendation Endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from services.job_recommender import JobRecommender

router = APIRouter()


class JobSeekerProfile(BaseModel):
    """
    Job seeker profile for recommendations
    """
    experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"] = Field(
        ..., description="Experience level"
    )
    skills: List[str] = Field(..., description="List of skills", min_length=1)
    preferred_location: Optional[str] = Field(None, description="Preferred location (country code or city)")
    preferred_employment_type: Optional[Literal["FULL_TIME", "PART_TIME", "CONTRACT", "TEMPORARY", "INTERNSHIP", "FREELANCE"]] = Field(
        None, description="Preferred employment type"
    )
    desired_salary_min: Optional[float] = Field(None, description="Minimum desired salary in USD", ge=0)
    desired_salary_max: Optional[float] = Field(None, description="Maximum desired salary in USD", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "experience_level": "MID_LEVEL",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "preferred_location": "US",
                "preferred_employment_type": "FULL_TIME",
                "desired_salary_min": 80000.0,
                "desired_salary_max": 120000.0
            }
        }


class RecommendedJob(BaseModel):
    """
    Recommended job information
    """
    job_id: str = Field(..., description="Job ID")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    salary_min: Optional[float] = Field(None, description="Minimum salary")
    salary_max: Optional[float] = Field(None, description="Maximum salary")
    match_score: float = Field(..., description="Match score (0-1)", ge=0, le=1)
    match_reasons: List[str] = Field(..., description="Reasons for recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "New York, NY",
                "salary_min": 100000.0,
                "salary_max": 150000.0,
                "match_score": 0.92,
                "match_reasons": [
                    "Skills match: Python, FastAPI, PostgreSQL",
                    "Experience level matches",
                    "Location preference matches"
                ]
            }
        }


class JobRecommendationResponse(BaseModel):
    """
    Response model for job recommendations
    """
    recommended_jobs: List[RecommendedJob] = Field(..., description="Top 5 recommended jobs")
    total_matches: int = Field(..., description="Total number of matching jobs found")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_jobs": [
                    {
                        "job_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Senior Software Engineer",
                        "company": "Tech Corp",
                        "location": "New York, NY",
                        "salary_min": 100000.0,
                        "salary_max": 150000.0,
                        "match_score": 0.92,
                        "match_reasons": [
                            "Skills match: Python, FastAPI, PostgreSQL",
                            "Experience level matches"
                        ]
                    }
                ],
                "total_matches": 15
            }
        }


@router.post("/recommend-jobs", response_model=JobRecommendationResponse)
async def recommend_jobs(profile: JobSeekerProfile):
    """
    Get personalized job recommendations based on job seeker profile.
    
    This endpoint uses a trained recommendation model to find the top 5 jobs
    that best match the job seeker's profile, considering:
    - Experience level
    - Skills
    - Location preferences
    - Employment type preferences
    - Salary expectations
    
    **Example Request:**
    ```json
    {
        "experience_level": "MID_LEVEL",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "preferred_location": "US",
        "preferred_employment_type": "FULL_TIME",
        "desired_salary_min": 80000.0,
        "desired_salary_max": 120000.0
    }
    ```
    
    **Example Response:**
    ```json
    {
        "recommended_jobs": [
            {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "New York, NY",
                "salary_min": 100000.0,
                "salary_max": 150000.0,
                "match_score": 0.92,
                "match_reasons": [
                    "Skills match: Python, FastAPI, PostgreSQL",
                    "Experience level matches"
                ]
            }
        ],
        "total_matches": 15
    }
    ```
    """
    try:
        recommender = JobRecommender()
        recommendations = await recommender.recommend(
            experience_level=profile.experience_level,
            skills=profile.skills,
            preferred_location=profile.preferred_location,
            preferred_employment_type=profile.preferred_employment_type,
            desired_salary_min=profile.desired_salary_min,
            desired_salary_max=profile.desired_salary_max
        )
        return JobRecommendationResponse(**recommendations)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")
