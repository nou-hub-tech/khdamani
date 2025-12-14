"""
Recruiter Profile Model
SQLite-compatible version
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    company_size = Column(String(20), nullable=True)
    company_location = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True, index=True)
    company_description = Column(Text, nullable=True)
    company_website = Column(String(500), nullable=True)
    company_logo_url = Column(String(500), nullable=True)
    verified = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recruiter_profile")
