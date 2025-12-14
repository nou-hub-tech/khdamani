"""
Country Recommender Service
"""

from typing import Literal
from pathlib import Path


class CountryRecommender:
    """
    Service for recommending countries to job seekers
    """
    
    def __init__(self):
        # Load job market data
        self.market_data = self._load_market_data()
    
    async def recommend(
        self,
        job_title: str,
        experience_level: Literal["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"]
    ) -> dict:
        """
        Get country recommendations based on job title and experience level
        
        Returns top 5 countries
        """
        # Normalize job title for matching
        normalized_title = job_title.lower()
        
        # Score countries based on job market data
        scored_countries = []
        
        for country_code, data in self.market_data.items():
            score = self._calculate_country_score(
                country_data=data,
                job_title=normalized_title,
                experience_level=experience_level
            )
            
            if score > 0:
                scored_countries.append({
                    "country": data["name"],
                    "country_code": country_code,
                    "score": round(score, 2),
                    "average_salary_usd": data.get("average_salary", 0),
                    "job_opportunities": data.get("job_opportunities", 0),
                    "growth_rate": data.get("growth_rate", 0),
                    "reasons": self._generate_reasons(data, normalized_title, experience_level)
                })
        
        # Sort by score and get top 5
        top_countries = sorted(scored_countries, key=lambda x: x["score"], reverse=True)[:5]
        
        return {
            "recommended_countries": top_countries
        }
    
    def _calculate_country_score(
        self,
        country_data: dict,
        job_title: str,
        experience_level: str
    ) -> float:
        """Calculate recommendation score for a country"""
        score = 0.0
        
        # Job opportunities (40% weight)
        opportunities = country_data.get("job_opportunities", 0)
        max_opportunities = max([d.get("job_opportunities", 0) for d in self.market_data.values()], default=1)
        opportunity_score = min(opportunities / max_opportunities, 1.0)
        score += opportunity_score * 0.4
        
        # Salary (30% weight)
        avg_salary = country_data.get("average_salary", 0)
        max_salary = max([d.get("average_salary", 0) for d in self.market_data.values()], default=1)
        salary_score = min(avg_salary / max_salary, 1.0)
        score += salary_score * 0.3
        
        # Growth rate (20% weight)
        growth_rate = country_data.get("growth_rate", 0)
        max_growth = max([d.get("growth_rate", 0) for d in self.market_data.values()], default=1)
        growth_score = min(growth_rate / max_growth, 1.0)
        score += growth_score * 0.2
        
        # Experience level match (10% weight)
        # Higher experience levels get better scores in developed markets
        exp_levels = ["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "EXECUTIVE"]
        exp_idx = exp_levels.index(experience_level) if experience_level in exp_levels else 2
        market_development = country_data.get("market_development", 0.5)
        exp_match = 0.5 + (exp_idx / 4.0) * market_development
        score += exp_match * 0.1
        
        return min(score, 1.0)
    
    def _generate_reasons(
        self,
        country_data: dict,
        job_title: str,
        experience_level: str
    ) -> list:
        """Generate reasons for recommendation"""
        reasons = []
        
        if country_data.get("job_opportunities", 0) > 5000:
            reasons.append(f"High demand for {job_title}")
        
        if country_data.get("average_salary", 0) > 100000:
            reasons.append("Competitive salaries")
        
        if country_data.get("growth_rate", 0) > 10:
            reasons.append("Strong job market growth")
        
        if country_data.get("market_development", 0) > 0.7:
            reasons.append("Mature tech industry")
        
        if country_data.get("work_life_balance", False):
            reasons.append("Good work-life balance")
        
        if not reasons:
            reasons.append("Growing opportunities in this market")
        
        return reasons[:3]  # Top 3 reasons
    
    def _load_market_data(self) -> dict:
        """Load job market data (mock data for now)"""
        # In production, this would load from a database or external API
        return {
            "US": {
                "name": "United States",
                "average_salary": 125000.0,
                "job_opportunities": 15000,
                "growth_rate": 12.5,
                "market_development": 0.95,
                "work_life_balance": False
            },
            "GB": {
                "name": "United Kingdom",
                "average_salary": 95000.0,
                "job_opportunities": 8500,
                "growth_rate": 10.2,
                "market_development": 0.85,
                "work_life_balance": True
            },
            "CA": {
                "name": "Canada",
                "average_salary": 105000.0,
                "job_opportunities": 6000,
                "growth_rate": 11.8,
                "market_development": 0.80,
                "work_life_balance": True
            },
            "DE": {
                "name": "Germany",
                "average_salary": 88000.0,
                "job_opportunities": 7500,
                "growth_rate": 9.5,
                "market_development": 0.82,
                "work_life_balance": True
            },
            "AU": {
                "name": "Australia",
                "average_salary": 110000.0,
                "job_opportunities": 4500,
                "growth_rate": 10.8,
                "market_development": 0.78,
                "work_life_balance": True
            },
            "NL": {
                "name": "Netherlands",
                "average_salary": 92000.0,
                "job_opportunities": 3500,
                "growth_rate": 8.5,
                "market_development": 0.75,
                "work_life_balance": True
            },
            "SG": {
                "name": "Singapore",
                "average_salary": 98000.0,
                "job_opportunities": 4000,
                "growth_rate": 11.2,
                "market_development": 0.88,
                "work_life_balance": False
            },
            "CH": {
                "name": "Switzerland",
                "average_salary": 135000.0,
                "job_opportunities": 2500,
                "growth_rate": 7.8,
                "market_development": 0.90,
                "work_life_balance": True
            }
        }
