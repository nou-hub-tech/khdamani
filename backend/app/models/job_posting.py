"""
Job Posting Model
SQLite-compatible version
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Text, Numeric, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    recruiter_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    department = Column(String(100), nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    salary_currency = Column(String(3), default="USD", nullable=True)
    employment_type = Column(String(20), nullable=False, default="FULL_TIME", index=True)
    required_experience = Column(String(20), nullable=True)
    required_education = Column(String(20), nullable=True)
    industry = Column(String(100), nullable=True, index=True)
    function = Column(String(100), nullable=True, index=True)  # Job function
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    company_profile = Column(Text, nullable=True)
    required_skills = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    benefits = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    is_fraud = Column(Boolean, nullable=False, default=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    views_count = Column(Integer, nullable=False, default=0)
    applications_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, onupdate=func.now())
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    recruiter = relationship("User", back_populates="job_postings")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    fraud_detection_results = relationship("FraudDetectionResult", back_populates="job", cascade="all, delete-orphan")
