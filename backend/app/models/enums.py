"""
Enum Types for Database Models
"""

import enum


class ExperienceLevel(str, enum.Enum):
    ENTRY_LEVEL = "ENTRY_LEVEL"
    JUNIOR = "JUNIOR"
    MID_LEVEL = "MID_LEVEL"
    SENIOR = "SENIOR"
    EXECUTIVE = "EXECUTIVE"


class EducationLevel(str, enum.Enum):
    HIGH_SCHOOL = "HIGH_SCHOOL"
    ASSOCIATE = "ASSOCIATE"
    BACHELOR = "BACHELOR"
    MASTER = "MASTER"
    DOCTORATE = "DOCTORATE"
    OTHER = "OTHER"


class EmploymentType(str, enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    TEMPORARY = "TEMPORARY"
    INTERNSHIP = "INTERNSHIP"
    FREELANCE = "FREELANCE"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    REVIEWED = "REVIEWED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEWED = "INTERVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class CompanySize(str, enum.Enum):
    STARTUP = "STARTUP"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    ENTERPRISE = "ENTERPRISE"

