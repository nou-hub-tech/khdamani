# Database Schema Summary

## Overview

This document provides a quick reference for the database schema design.

## Core Tables

### 1. `users`
- **Purpose**: Core user accounts for both job seekers and recruiters
- **Key Fields**: email (unique), role, is_active
- **Relationships**: One-to-one with job_seeker_profiles or recruiter_profiles

### 2. `job_seeker_profiles`
- **Purpose**: Extended profile for job seekers
- **Key Fields**: full_name, experience_level, skills (array), current_country
- **Relationships**: One-to-one with users

### 3. `recruiter_profiles`
- **Purpose**: Extended profile for recruiters/companies
- **Key Fields**: company_name, company_size, industry, verified
- **Relationships**: One-to-one with users

### 4. `job_postings`
- **Purpose**: Job listings created by recruiters
- **Key Fields**: title, location, salary_range, required_skills (array), is_fraud, is_active
- **Relationships**: Many-to-one with users (recruiter), one-to-many with job_applications

### 5. `job_applications`
- **Purpose**: Applications submitted by job seekers
- **Key Fields**: status, applied_at
- **Relationships**: Many-to-one with job_postings and users (job_seeker)
- **Unique Constraint**: (job_id, job_seeker_id) - one application per job per user

## ML Result Tables

### 6. `salary_predictions`
- **Purpose**: Store ML salary predictions
- **Key Fields**: predicted_salary_usd, confidence_score, model_version
- **Note**: Lightweight - stores only results, not training data

### 7. `fraud_detection_results`
- **Purpose**: Store ML fraud detection results
- **Key Fields**: fraud_probability, is_fraud, reasons (array), model_version
- **Relationships**: Many-to-one with job_postings

### 8. `country_recommendations`
- **Purpose**: Store ML country recommendations
- **Key Fields**: recommended_countries (array), country_scores (JSONB), model_version
- **Relationships**: Many-to-one with users

### 9. `job_recommendations`
- **Purpose**: Store ML job recommendations
- **Key Fields**: recommendation_score, recommendation_reasons (array), model_version
- **Relationships**: Many-to-one with users and job_postings
- **Unique Constraint**: (user_id, job_id, model_version)

### 10. `user_job_interactions`
- **Purpose**: Track user interactions for ML training data
- **Key Fields**: interaction_type, interaction_data (JSONB)
- **Note**: Used for collecting training data, not storing full datasets

## ENUM Types

- `user_role`: JOB_SEEKER, RECRUITER, ADMIN
- `experience_level`: ENTRY_LEVEL, JUNIOR, MID_LEVEL, SENIOR, EXECUTIVE
- `education_level`: HIGH_SCHOOL, ASSOCIATE, BACHELOR, MASTER, DOCTORATE, OTHER
- `employment_type`: FULL_TIME, PART_TIME, CONTRACT, TEMPORARY, INTERNSHIP, FREELANCE
- `application_status`: APPLIED, REVIEWED, SHORTLISTED, INTERVIEWED, ACCEPTED, REJECTED, WITHDRAWN
- `company_size`: STARTUP, SMALL, MEDIUM, LARGE, ENTERPRISE

## Key Design Features

### 1. UUID Primary Keys
- All tables use UUID for better distribution
- Generated using `uuid_generate_v4()`

### 2. Array Columns
- Used for: skills, benefits, reasons, recommended_countries
- Indexed with GIN indexes for efficient querying

### 3. JSONB Columns
- Used for: input_features, interaction_data, country_scores, detected_features
- Flexible schema, supports indexing

### 4. Timestamps
- All tables have `created_at`
- Most have `updated_at` (auto-updated via trigger)
- Some have specific timestamps (applied_at, reviewed_at, detected_at)

### 5. Soft Deletes
- `is_active` flags instead of hard deletes where appropriate
- Foreign keys use CASCADE or SET NULL appropriately

### 6. Constraints
- Check constraints for data validation (salary ranges, probability ranges)
- Unique constraints prevent duplicates
- Foreign keys ensure referential integrity

## Indexes

### Performance Indexes
- All foreign keys are indexed
- Frequently queried columns (email, status, dates)
- Full-text search on job_postings
- GIN indexes on array columns
- Composite indexes for common query patterns

### Full-Text Search
- Job postings have a GIN index on tsvector for title, description, requirements

## Triggers

### Auto-update Timestamps
- `update_updated_at_column()` function
- Applied to tables with `updated_at` column

### Application Count
- `update_job_applications_count()` function
- Automatically updates `applications_count` in job_postings

## Data Integrity

### Foreign Key Actions
- **CASCADE**: Delete related records when parent is deleted
  - Used for: profiles, applications, ML results tied to jobs/users
- **SET NULL**: Set to NULL when parent is deleted
  - Used for: optional references in ML results

### Constraints
- Email format validation
- Salary range validation (min <= max)
- Probability/score range validation (0-1)
- Array length validation (country_recommendations)

## Scalability Considerations

1. **Partitioning**: Consider partitioning large tables (job_applications, user_job_interactions) by date
2. **Archiving**: ML result tables can be archived periodically
3. **Indexing**: All foreign keys and frequently queried columns are indexed
4. **Connection Pooling**: Use connection pooling for better performance

## Migration Strategy

1. Use Alembic for schema migrations
2. Or apply `schema.sql` directly for initial setup
3. Always test migrations on development first
4. Keep migrations small and focused

## Usage with SQLAlchemy

All models are defined in `app/models/`:
- `user.py` - User model
- `job_seeker_profile.py` - Job seeker profile
- `recruiter_profile.py` - Recruiter profile
- `job_posting.py` - Job postings
- `job_application.py` - Job applications
- `ml_models.py` - ML result models
- `enums.py` - Enum type definitions

Models use:
- UUID primary keys
- Proper relationships
- Enum types matching database ENUMs
- Constraints matching database constraints

