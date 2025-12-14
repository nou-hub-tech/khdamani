"""
ML Services API Router
"""

from fastapi import APIRouter
from api.endpoints import (
    salary,
    recommendation,
    fraud,
    country,
)

api_router = APIRouter()

# Include all ML endpoint routers
api_router.include_router(salary.router, prefix="/salary", tags=["salary-prediction"])
api_router.include_router(recommendation.router, prefix="/jobs", tags=["job-recommendation"])
api_router.include_router(fraud.router, prefix="/fraud", tags=["fraud-detection"])
api_router.include_router(country.router, prefix="/country", tags=["country-recommendation"])

