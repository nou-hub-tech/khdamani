"""
ML Service Request/Response Schemas
"""

from pydantic import BaseModel
from typing import Dict, Any, List


class SalaryPredictionRequest(BaseModel):
    job_data: Dict[str, Any]
    user_profile: Dict[str, Any]


class SalaryPredictionResponse(BaseModel):
    predicted_salary: float
    salary_range: Dict[str, float]
    confidence: float


class JobRecommendationResponse(BaseModel):
    jobs: List[Dict[str, Any]]
    scores: List[float]


class FraudDetectionRequest(BaseModel):
    job_posting: Dict[str, Any]


class FraudDetectionResponse(BaseModel):
    is_fraud: bool
    fraud_probability: float
    reasons: List[str]


class CountryRecommendationRequest(BaseModel):
    user_profile: Dict[str, Any]


class CountryRecommendationResponse(BaseModel):
    countries: List[Dict[str, Any]]

