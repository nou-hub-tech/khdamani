"""
Salary Predictor Service
"""

from typing import Literal
import joblib
import os
from pathlib import Path
from utils.model_loader import ModelLoader


class SalaryPredictor:
    """
    Service for predicting salary based on job and employee features
    """
    
    def __init__(self):
        # Load model and preprocessor on initialization
        self.model = ModelLoader.load_model("salary_predictor")
        self.scaler = ModelLoader.load_scaler("salary_predictor")
        self.label_encoders = ModelLoader.load_encoders("salary_predictor")
    
    async def predict(
        self,
        work_year: int,
        experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"],
        employment_type: Literal["FULL_TIME", "PART_TIME", "CONTRACT", "TEMPORARY", "INTERNSHIP", "FREELANCE"],
        job_title: str,
        employee_residence: str,
        remote_ratio: int,
        company_location: str,
        company_size: Literal["STARTUP", "SMALL", "MEDIUM", "LARGE", "ENTERPRISE"]
    ) -> dict:
        """
        Predict salary for given features
        
        Args:
            work_year: Year of work
            experience_level: Experience level
            employment_type: Employment type
            job_title: Job title
            employee_residence: Employee residence country code
            remote_ratio: Remote work ratio (0-100)
            company_location: Company location country code
            company_size: Company size
        
        Returns:
            Dictionary with predicted_salary_usd, salary_range, and confidence_score
        """
        # Feature engineering
        features = self._engineer_features(
            work_year=work_year,
            experience_level=experience_level,
            employment_type=employment_type,
            job_title=job_title,
            employee_residence=employee_residence,
            remote_ratio=remote_ratio,
            company_location=company_location,
            company_size=company_size
        )
        
        # Preprocessing
        features_scaled = self.scaler.transform([features])
        
        # Prediction
        predicted_salary = float(self.model.predict(features_scaled)[0])
        
        # Calculate confidence and range
        # In a real implementation, this would come from model uncertainty
        confidence_score = 0.85
        salary_range_min = predicted_salary * 0.8
        salary_range_max = predicted_salary * 1.2
        
        return {
            "predicted_salary_usd": round(predicted_salary, 2),
            "salary_range_min": round(salary_range_min, 2),
            "salary_range_max": round(salary_range_max, 2),
            "confidence_score": round(confidence_score, 2),
        }
    
    def _engineer_features(
        self,
        work_year: int,
        experience_level: str,
        employment_type: str,
        job_title: str,
        employee_residence: str,
        remote_ratio: int,
        company_location: str,
        company_size: str
    ) -> list:
        """
        Engineer features from input data
        """
        # Encode categorical features if encoders are available
        exp_level_encoded = self._encode_experience_level(experience_level)
        emp_type_encoded = self._encode_employment_type(employment_type)
        company_size_encoded = self._encode_company_size(company_size)
        
        # Encode job title (simplified - in production, use proper encoding)
        job_title_encoded = hash(job_title.lower()) % 1000  # Simple hash encoding
        
        # Encode locations (simplified)
        employee_residence_encoded = hash(employee_residence.upper()) % 100
        company_location_encoded = hash(company_location.upper()) % 100
        
        # Feature vector
        features = [
            work_year,
            exp_level_encoded,
            emp_type_encoded,
            job_title_encoded,
            employee_residence_encoded,
            remote_ratio,
            company_location_encoded,
            company_size_encoded,
        ]
        
        return features
    
    def _encode_experience_level(self, level: str) -> int:
        """Encode experience level to numeric"""
        mapping = {
            "ENTRY_LEVEL": 0,
            "JUNIOR": 1,
            "MID_LEVEL": 2,
            "SENIOR": 3,
            "EXECUTIVE": 4
        }
        return mapping.get(level, 2)
    
    def _encode_employment_type(self, emp_type: str) -> int:
        """Encode employment type to numeric"""
        mapping = {
            "FULL_TIME": 0,
            "PART_TIME": 1,
            "CONTRACT": 2,
            "TEMPORARY": 3,
            "INTERNSHIP": 4,
            "FREELANCE": 5
        }
        return mapping.get(emp_type, 0)
    
    def _encode_company_size(self, size: str) -> int:
        """Encode company size to numeric"""
        mapping = {
            "STARTUP": 0,
            "SMALL": 1,
            "MEDIUM": 2,
            "LARGE": 3,
            "ENTERPRISE": 4
        }
        return mapping.get(size, 2)
