"""
ML Integration Service
Handles communication with ML services
"""

import httpx
from typing import Dict, Any, List
from app.core.config import settings
from app.schemas.ml_requests import (
    SalaryPredictionResponse,
    JobRecommendationResponse,
    FraudDetectionResponse,
    CountryRecommendationResponse,
)


class MLIntegrationService:
    """
    Service for integrating with ML microservices
    """
    
    def __init__(self):
        self.ml_service_url = settings.ML_SERVICE_URL
        self.timeout = 30.0
    
    async def predict_salary(
        self,
        job_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> SalaryPredictionResponse:
        """
        Predict salary for a job
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.ml_service_url}/api/salary/predict",
                json={
                    "job_data": job_data,
                    "user_profile": user_profile,
                }
            )
            response.raise_for_status()
            return SalaryPredictionResponse(**response.json())
    
    async def recommend_jobs(
        self,
        user_id: int,
        limit: int = 10
    ) -> JobRecommendationResponse:
        """
        Get job recommendations for a user
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.ml_service_url}/api/jobs/recommend",
                params={"user_id": user_id, "limit": limit}
            )
            response.raise_for_status()
            return JobRecommendationResponse(**response.json())
    
    async def detect_fraud(
        self,
        job_posting: Dict[str, Any]
    ) -> FraudDetectionResponse:
        """
        Detect fraud in a job posting
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.ml_service_url}/api/fraud/detect",
                json={"job_posting": job_posting}
            )
            response.raise_for_status()
            return FraudDetectionResponse(**response.json())
    
    async def recommend_country(
        self,
        user_profile: Dict[str, Any]
    ) -> CountryRecommendationResponse:
        """
        Get country recommendations for a user
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.ml_service_url}/api/country/recommend",
                json={"user_profile": user_profile}
            )
            response.raise_for_status()
            return CountryRecommendationResponse(**response.json())

