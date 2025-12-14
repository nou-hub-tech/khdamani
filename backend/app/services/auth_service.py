"""
Authentication Service
"""

from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.config import settings
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister, TokenResponse


class AuthService:
    """
    Service for handling authentication logic
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def register(self, user_data: UserRegister) -> User:
        """
        Register a new user
        """
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        role_value = user_data.role.upper() if user_data.role else "JOB_SEEKER"
        from app.models.user import UserRole
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            role=role_value
        )
        
        return self.user_repo.create(user)
    
    async def login(self, email: str, password: str) -> Optional[TokenResponse]:
        """
        Authenticate user and return tokens
        """
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        # Create tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

