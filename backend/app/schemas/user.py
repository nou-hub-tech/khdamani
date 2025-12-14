"""
User Schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserRegister(UserBase):
    password: str
    role: Optional[str] = "JOB_SEEKER"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

