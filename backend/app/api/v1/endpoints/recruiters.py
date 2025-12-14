"""
Recruiter Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_recruiter
from app.models.user import User

router = APIRouter()


@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    """
    Get current recruiter profile
    """
    # Implementation here
    return {"message": "Profile endpoint"}

