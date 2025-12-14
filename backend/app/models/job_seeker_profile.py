"""
Job Seeker Profile Model
SQLite-compatible version
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class JobSeekerProfile(Base):
    __tablename__ = "job_seeker_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    experience_level = Column(String(20), nullable=True)
    education_level = Column(String(20), nullable=True)
    current_country = Column(String(100), nullable=True, index=True)
    desired_job_title = Column(String(255), nullable=True, index=True)
    skills = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    bio = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="job_seeker_profile")
