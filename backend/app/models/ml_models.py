"""
ML Result Models
SQLite-compatible version
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Numeric, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class SalaryPrediction(Base):
    __tablename__ = "salary_predictions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="SET NULL"), nullable=True, index=True)
    job_title = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True, index=True)
    experience_level = Column(String(20), nullable=True)
    education_level = Column(String(20), nullable=True)
    predicted_salary_usd = Column(Numeric(12, 2), nullable=False)
    salary_min_usd = Column(Numeric(12, 2), nullable=True)
    salary_max_usd = Column(Numeric(12, 2), nullable=True)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    model_version = Column(String(50), nullable=False, index=True)
    input_features = Column(JSON, nullable=True)  # JSON for SQLite
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)


class FraudDetectionResult(Base):
    __tablename__ = "fraud_detection_results"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    fraud_probability = Column(Numeric(5, 4), nullable=False, index=True)
    is_fraud = Column(Boolean, nullable=False, default=False, index=True)
    model_version = Column(String(50), nullable=False, index=True)
    detected_features = Column(JSON, nullable=True)  # JSON for SQLite
    reasons = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    reviewed_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    detected_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    job = relationship("JobPosting", back_populates="fraud_detection_results")


class CountryRecommendation(Base):
    __tablename__ = "country_recommendations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_title = Column(String(255), nullable=True, index=True)
    experience_level = Column(String(20), nullable=True)
    skills = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    recommended_countries = Column(JSON, nullable=False)  # JSON array for SQLite
    country_scores = Column(JSON, nullable=True)  # JSON for SQLite
    model_version = Column(String(50), nullable=False, index=True)
    input_features = Column(JSON, nullable=True)  # JSON for SQLite
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)


class JobRecommendation(Base):
    __tablename__ = "job_recommendations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_score = Column(Numeric(5, 4), nullable=False, index=True)
    model_version = Column(String(50), nullable=False)
    recommendation_reasons = Column(JSON, default=[], nullable=True)  # JSON array for SQLite
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=True)


class UserJobInteraction(Base):
    __tablename__ = "user_job_interactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False, index=True)
    interaction_data = Column(JSON, nullable=True)  # JSON for SQLite
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
