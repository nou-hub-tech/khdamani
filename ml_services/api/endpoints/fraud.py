"""
Fraud Detection Endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.fraud_detector import FraudDetector

router = APIRouter()


class FraudDetectionRequest(BaseModel):
    job_posting: Dict[str, Any]


class FraudDetectionResponse(BaseModel):
    is_fraud: bool
    fraud_probability: float
    reasons: List[str]


@router.post("/detect", response_model=FraudDetectionResponse)
async def detect_fraud(request: FraudDetectionRequest):
    """
    Detect potential fraud in a job posting
    """
    try:
        detector = FraudDetector()
        detection = await detector.detect(request.job_posting)
        return detection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fraud detection error: {str(e)}")

