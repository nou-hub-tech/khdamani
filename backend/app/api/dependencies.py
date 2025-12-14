"""
FastAPI Dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    # user_id_str is already a string (UUID as string for SQLite compatibility)
    user_id = user_id_str
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_recruiter(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a recruiter
    """
    if current_user.role != "RECRUITER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Recruiter access required."
        )
    return current_user


async def get_current_job_seeker(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a job seeker
    """
    if current_user.role != "JOB_SEEKER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Job seeker access required."
        )
    return current_user

