"""
ML Services Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.ml_requests import (
    SalaryPredictionRequest,
    SalaryPredictionResponse,
    JobRecommendationResponse,
    FraudDetectionRequest,
    FraudDetectionResponse,
    CountryRecommendationRequest,
    CountryRecommendationResponse,
)
from app.services.ml_integration_service import MLIntegrationService
from app.models.user import User

router = APIRouter()


@router.post("/salary/predict", response_model=SalaryPredictionResponse)
async def predict_salary(
    request: SalaryPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Predict salary for a job based on job details and user profile
    """
    ml_service = MLIntegrationService()
    prediction = await ml_service.predict_salary(
        job_data=request.job_data,
        user_profile=request.user_profile
    )
    return prediction


@router.get("/jobs/recommend", response_model=JobRecommendationResponse)
async def recommend_jobs(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get personalized job recommendations (ML-powered)
    """
    ml_service = MLIntegrationService()
    recommendations = await ml_service.recommend_jobs(
        user_id=current_user.id,
        limit=limit
    )
    return recommendations


@router.post("/fraud/detect", response_model=FraudDetectionResponse)
async def detect_fraud(
    request: FraudDetectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Detect potential fraud in job posting
    """
    ml_service = MLIntegrationService()
    detection = await ml_service.detect_fraud(request.job_posting)
    return detection


@router.post("/country/recommend", response_model=CountryRecommendationResponse)
async def recommend_country(
    request: CountryRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get country recommendations based on user profile
    """
    ml_service = MLIntegrationService()
    recommendations = await ml_service.recommend_country(request.user_profile)
    return recommendations

