"""
Salary Prediction Endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from services.salary_predictor import SalaryPredictor

router = APIRouter()


class SalaryPredictionRequest(BaseModel):
    """
    Request model for salary prediction
    """
    work_year: int = Field(..., description="Year of work (e.g., 2023, 2024)", ge=2020, le=2030)
    experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"] = Field(
        ..., description="Experience level"
    )
    employment_type: Literal["FULL_TIME", "PART_TIME", "CONTRACT", "TEMPORARY", "INTERNSHIP", "FREELANCE"] = Field(
        ..., description="Employment type"
    )
    job_title: str = Field(..., description="Job title (e.g., 'Software Engineer', 'Data Scientist')", min_length=1, max_length=200)
    employee_residence: str = Field(..., description="Employee residence country code (e.g., 'US', 'GB', 'CA')", min_length=2, max_length=2)
    remote_ratio: int = Field(..., description="Remote work ratio (0-100)", ge=0, le=100)
    company_location: str = Field(..., description="Company location country code (e.g., 'US', 'GB', 'CA')", min_length=2, max_length=2)
    company_size: Literal["STARTUP", "SMALL", "MEDIUM", "LARGE", "ENTERPRISE"] = Field(
        ..., description="Company size"
    )
    
    @field_validator('employee_residence', 'company_location')
    @classmethod
    def validate_country_code(cls, v: str) -> str:
        """Validate country code is uppercase"""
        return v.upper()
    
    class Config:
        json_schema_extra = {
            "example": {
                "work_year": 2024,
                "experience_level": "MID_LEVEL",
                "employment_type": "FULL_TIME",
                "job_title": "Software Engineer",
                "employee_residence": "US",
                "remote_ratio": 50,
                "company_location": "US",
                "company_size": "LARGE"
            }
        }


class SalaryPredictionResponse(BaseModel):
    """
    Response model for salary prediction
    """
    predicted_salary_usd: float = Field(..., description="Predicted salary in USD")
    salary_range_min: float = Field(..., description="Minimum salary estimate")
    salary_range_max: float = Field(..., description="Maximum salary estimate")
    confidence_score: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_salary_usd": 125000.0,
                "salary_range_min": 100000.0,
                "salary_range_max": 150000.0,
                "confidence_score": 0.85
            }
        }


@router.post("/predict-salary", response_model=SalaryPredictionResponse)
async def predict_salary(request: SalaryPredictionRequest):
    """
    Predict salary based on job and employee features.
    
    This endpoint uses a trained ML model to predict salary in USD based on:
    - Work year
    - Experience level
    - Employment type
    - Job title
    - Employee residence
    - Remote work ratio
    - Company location
    - Company size
    
    **Example Request:**
    ```json
    {
        "work_year": 2024,
        "experience_level": "MID_LEVEL",
        "employment_type": "FULL_TIME",
        "job_title": "Software Engineer",
        "employee_residence": "US",
        "remote_ratio": 50,
        "company_location": "US",
        "company_size": "LARGE"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "predicted_salary_usd": 125000.0,
        "salary_range_min": 100000.0,
        "salary_range_max": 150000.0,
        "confidence_score": 0.85
    }
    ```
    """
    try:
        predictor = SalaryPredictor()
        prediction = await predictor.predict(
            work_year=request.work_year,
            experience_level=request.experience_level,
            employment_type=request.employment_type,
            job_title=request.job_title,
            employee_residence=request.employee_residence,
            remote_ratio=request.remote_ratio,
            company_location=request.company_location,
            company_size=request.company_size
        )
        return SalaryPredictionResponse(**prediction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
