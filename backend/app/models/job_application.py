"""
Job Application Model
SQLite-compatible version
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    job_seeker_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="APPLIED", index=True)
    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    applied_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    reviewed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    job = relationship("JobPosting", back_populates="applications")
    job_seeker = relationship("User", back_populates="job_applications")
