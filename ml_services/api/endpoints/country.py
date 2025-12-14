"""
Country Recommendation Endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from services.country_recommender import CountryRecommender

router = APIRouter()


class CountryRecommendationRequest(BaseModel):
    """
    Request model for country recommendations
    """
    job_title: str = Field(..., description="Job title (e.g., 'Software Engineer', 'Data Scientist')", min_length=1, max_length=200)
    experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"] = Field(
        ..., description="Experience level"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Software Engineer",
                "experience_level": "MID_LEVEL"
            }
        }


class CountryRecommendation(BaseModel):
    """
    Country recommendation information
    """
    country: str = Field(..., description="Country name")
    country_code: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    score: float = Field(..., description="Recommendation score (0-1)", ge=0, le=1)
    average_salary_usd: float = Field(..., description="Average salary in USD")
    job_opportunities: int = Field(..., description="Number of job opportunities")
    growth_rate: float = Field(..., description="Job market growth rate (%)")
    reasons: List[str] = Field(..., description="Reasons for recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "country": "United States",
                "country_code": "US",
                "score": 0.95,
                "average_salary_usd": 125000.0,
                "job_opportunities": 15000,
                "growth_rate": 12.5,
                "reasons": [
                    "High demand for Software Engineers",
                    "Competitive salaries",
                    "Strong tech industry"
                ]
            }
        }


class CountryRecommendationResponse(BaseModel):
    """
    Response model for country recommendations
    """
    recommended_countries: List[CountryRecommendation] = Field(..., description="Top 5 recommended countries")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_countries": [
                    {
                        "country": "United States",
                        "country_code": "US",
                        "score": 0.95,
                        "average_salary_usd": 125000.0,
                        "job_opportunities": 15000,
                        "growth_rate": 12.5,
                        "reasons": [
                            "High demand for Software Engineers",
                            "Competitive salaries",
                            "Strong tech industry"
                        ]
                    },
                    {
                        "country": "United Kingdom",
                        "country_code": "GB",
                        "score": 0.88,
                        "average_salary_usd": 95000.0,
                        "job_opportunities": 8500,
                        "growth_rate": 10.2,
                        "reasons": [
                            "Growing tech sector",
                            "Good work-life balance"
                        ]
                    }
                ]
            }
        }


@router.post("/recommend-countries", response_model=CountryRecommendationResponse)
async def recommend_countries(request: CountryRecommendationRequest):
    """
    Get country recommendations for job hunting based on job title and experience level.
    
    This endpoint uses job market data to recommend the top 5 countries where
    the job seeker is most likely to find opportunities, considering:
    - Job title demand
    - Experience level requirements
    - Average salaries
    - Job market growth
    - Number of opportunities
    
    **Example Request:**
    ```json
    {
        "job_title": "Software Engineer",
        "experience_level": "MID_LEVEL"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "recommended_countries": [
            {
                "country": "United States",
                "country_code": "US",
                "score": 0.95,
                "average_salary_usd": 125000.0,
                "job_opportunities": 15000,
                "growth_rate": 12.5,
                "reasons": [
                    "High demand for Software Engineers",
                    "Competitive salaries",
                    "Strong tech industry"
                ]
            },
            {
                "country": "United Kingdom",
                "country_code": "GB",
                "score": 0.88,
                "average_salary_usd": 95000.0,
                "job_opportunities": 8500,
                "growth_rate": 10.2,
                "reasons": [
                    "Growing tech sector",
                    "Good work-life balance"
                ]
            }
        ]
    }
    ```
    """
    try:
        recommender = CountryRecommender()
        recommendations = await recommender.recommend(
            job_title=request.job_title,
            experience_level=request.experience_level
        )
        return CountryRecommendationResponse(**recommendations)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Country recommendation error: {str(e)}")
