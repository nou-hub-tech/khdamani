"""
Job Recommender Service
"""

from typing import List, Literal, Optional
import joblib
from pathlib import Path


class JobRecommender:
    """
    Service for recommending jobs to users
    """
    
    def __init__(self):
        # Load recommendation model
        self.model = self._load_model()
        # In production, this would load from database or external service
        self.job_database = self._load_job_database()
    
    async def recommend(
        self,
        experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"],
        skills: List[str],
        preferred_location: Optional[str] = None,
        preferred_employment_type: Optional[Literal["FULL_TIME", "PART_TIME", "CONTRACT", "TEMPORARY", "INTERNSHIP", "FREELANCE"]] = None,
        desired_salary_min: Optional[float] = None,
        desired_salary_max: Optional[float] = None
    ) -> dict:
        """
        Get job recommendations based on profile
        
        Returns top 5 matching jobs
        """
        # Feature engineering for recommendation
        profile_features = self._engineer_profile_features(
            experience_level=experience_level,
            skills=skills,
            preferred_location=preferred_location,
            preferred_employment_type=preferred_employment_type
        )
        
        # Get job matches (in production, this would query a database)
        matches = self._find_matching_jobs(
            profile_features=profile_features,
            skills=skills,
            preferred_location=preferred_location,
            preferred_employment_type=preferred_employment_type,
            desired_salary_min=desired_salary_min,
            desired_salary_max=desired_salary_max
        )
        
        # Score and rank jobs
        scored_jobs = self._score_jobs(matches, profile_features, skills)
        
        # Get top 5
        top_jobs = sorted(scored_jobs, key=lambda x: x['match_score'], reverse=True)[:5]
        
        return {
            "recommended_jobs": top_jobs,
            "total_matches": len(matches)
        }
    
    def _engineer_profile_features(
        self,
        experience_level: str,
        skills: List[str],
        preferred_location: Optional[str],
        preferred_employment_type: Optional[str]
    ) -> dict:
        """Engineer features from profile"""
        exp_level_mapping = {
            "ENTRY_LEVEL": 0,
            "JUNIOR": 1,
            "MID_LEVEL": 2,
            "SENIOR": 3,
            "EXECUTIVE": 4
        }
        
        return {
            "experience_level_encoded": exp_level_mapping.get(experience_level, 2),
            "num_skills": len(skills),
            "has_location_preference": preferred_location is not None,
            "has_employment_preference": preferred_employment_type is not None
        }
    
    def _find_matching_jobs(
        self,
        profile_features: dict,
        skills: List[str],
        preferred_location: Optional[str],
        preferred_employment_type: Optional[str],
        desired_salary_min: Optional[float],
        desired_salary_max: Optional[float]
    ) -> List[dict]:
        """Find matching jobs from database"""
        # In production, this would query a real database
        # For now, return mock data
        all_jobs = self.job_database
        
        matches = []
        for job in all_jobs:
            # Filter by location if specified
            if preferred_location and preferred_location.upper() not in job.get("location", "").upper():
                continue
            
            # Filter by employment type if specified
            if preferred_employment_type and job.get("employment_type") != preferred_employment_type:
                continue
            
            # Filter by salary if specified
            if desired_salary_min and job.get("salary_max", 0) < desired_salary_min:
                continue
            if desired_salary_max and job.get("salary_min", float('inf')) > desired_salary_max:
                continue
            
            matches.append(job)
        
        return matches
    
    def _score_jobs(
        self,
        jobs: List[dict],
        profile_features: dict,
        user_skills: List[str]
    ) -> List[dict]:
        """Score jobs based on match"""
        scored = []
        
        for job in jobs:
            score = 0.0
            reasons = []
            
            # Skills match (40% weight)
            job_skills = job.get("required_skills", [])
            skill_matches = set(user_skills) & set(job_skills)
            skill_score = len(skill_matches) / max(len(job_skills), 1)
            score += skill_score * 0.4
            if skill_matches:
                reasons.append(f"Skills match: {', '.join(skill_matches)}")
            
            # Experience level match (30% weight)
            job_exp = job.get("required_experience", "MID_LEVEL")
            exp_levels = ["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"]
            user_exp_idx = exp_levels.index(profile_features.get("experience_level_encoded", 2))
            job_exp_idx = exp_levels.index(job_exp) if job_exp in exp_levels else 2
            exp_match = 1.0 - abs(user_exp_idx - job_exp_idx) / 4.0
            score += exp_match * 0.3
            if exp_match > 0.7:
                reasons.append("Experience level matches")
            
            # Location match (20% weight)
            if job.get("location"):
                score += 0.2
                reasons.append("Location preference matches")
            
            # Salary match (10% weight)
            if job.get("salary_min") or job.get("salary_max"):
                score += 0.1
                reasons.append("Salary range available")
            
            scored.append({
                "job_id": job.get("id", ""),
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "match_score": round(min(score, 1.0), 2),
                "match_reasons": reasons[:3]  # Top 3 reasons
            })
        
        return scored
    
    def _load_model(self):
        """Load recommendation model"""
        # In production, load from file
        # For now, return None (using rule-based scoring)
        return None
    
    def _load_job_database(self) -> List[dict]:
        """Load job database (mock data for now)"""
        # In production, this would query from database
        return [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "New York, NY, US",
                "employment_type": "FULL_TIME",
                "required_experience": "SENIOR",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
                "salary_min": 100000.0,
                "salary_max": 150000.0
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "title": "Backend Developer",
                "company": "StartupXYZ",
                "location": "San Francisco, CA, US",
                "employment_type": "FULL_TIME",
                "required_experience": "MID_LEVEL",
                "required_skills": ["Python", "FastAPI", "PostgreSQL"],
                "salary_min": 90000.0,
                "salary_max": 120000.0
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "title": "Full Stack Engineer",
                "company": "WebDev Inc",
                "location": "Remote, US",
                "employment_type": "FULL_TIME",
                "required_experience": "MID_LEVEL",
                "required_skills": ["Python", "FastAPI", "React", "PostgreSQL"],
                "salary_min": 85000.0,
                "salary_max": 110000.0
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "title": "Python Developer",
                "company": "DataTech",
                "location": "Austin, TX, US",
                "employment_type": "FULL_TIME",
                "required_experience": "JUNIOR",
                "required_skills": ["Python", "Django", "PostgreSQL"],
                "salary_min": 70000.0,
                "salary_max": 90000.0
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440004",
                "title": "Software Engineer",
                "company": "CloudSoft",
                "location": "Seattle, WA, US",
                "employment_type": "FULL_TIME",
                "required_experience": "MID_LEVEL",
                "required_skills": ["Python", "FastAPI", "Docker", "Kubernetes"],
                "salary_min": 95000.0,
                "salary_max": 130000.0
            }
        ]
