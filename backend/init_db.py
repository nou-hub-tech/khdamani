"""
Initialize SQLite Database
Creates all tables from models
"""

from app.core.database import Base, engine
from app.models import (
    User,
    JobSeekerProfile,
    RecruiterProfile,
    JobPosting,
    JobApplication,
    SalaryPrediction,
    FraudDetectionResult,
    CountryRecommendation,
    JobRecommendation,
    UserJobInteraction,
)

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print(f"📁 Database file: khadamni.db")
    print("\nYou can now start the backend server:")
    print("  uvicorn app.main:app --reload")

if __name__ == "__main__":
    init_db()

