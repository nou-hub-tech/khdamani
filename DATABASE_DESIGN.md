# Database Design Documentation

## Overview

This document describes the PostgreSQL database schema for the Khadamni job search platform. The schema is designed to be normalized, scalable, and ML-ready.

## Schema Files

- **`backend/database/schema.sql`**: Complete PostgreSQL schema with all tables, indexes, triggers, and functions
- **`backend/database/README.md`**: Database documentation and usage guide
- **`backend/database/SCHEMA_SUMMARY.md`**: Quick reference for the schema
- **`backend/database/QUERIES.md`**: Common SQL queries for the platform

## Key Design Principles

### 1. Normalization
- Follows 3NF (Third Normal Form) to reduce data redundancy
- Separate tables for user profiles (job_seeker_profiles, recruiter_profiles)
- Proper foreign key relationships

### 2. UUID Primary Keys
- All tables use UUID for better distribution
- Generated using PostgreSQL's `uuid_generate_v4()`
- Better for distributed systems and security

### 3. ENUM Types
- Used for fixed sets of values (roles, statuses, levels)
- Provides type safety and better performance
- Defined at database level for consistency

### 4. Array Columns
- PostgreSQL arrays for multi-value fields (skills, benefits)
- Indexed with GIN indexes for efficient querying
- Simpler than junction tables for simple cases

### 5. JSONB Columns
- Flexible metadata storage (input_features, interaction_data)
- Supports indexing and efficient querying
- Allows schema evolution without migrations

### 6. ML Result Tables
- **Lightweight**: Store only prediction results, not training data
- **Versioned**: Track model versions for predictions
- **Queryable**: Indexed for analytics and debugging

## Core Tables

### users
- Base user accounts for both job seekers and recruiters
- Email-based authentication
- Role-based access control (JOB_SEEKER, RECRUITER, ADMIN)

### job_seeker_profiles
- Extended profile for job seekers
- Skills, experience, education, location
- One-to-one relationship with users

### recruiter_profiles
- Extended profile for recruiters/companies
- Company information, verification status
- One-to-one relationship with users

### job_postings
- Job listings created by recruiters
- Salary ranges, requirements, skills
- Fraud detection flag
- Full-text search support

### job_applications
- Applications submitted by job seekers
- Status tracking (APPLIED → ACCEPTED/REJECTED)
- Unique constraint: one application per job per user

## ML Result Tables

### salary_predictions
- Store ML salary predictions
- Includes confidence scores and model version
- Links to user and job (optional)

### fraud_detection_results
- Store ML fraud detection results
- Probability scores and reasons
- Links to job postings

### country_recommendations
- Store ML country recommendations
- Array of recommended countries
- JSONB for country scores

### job_recommendations
- Store ML job recommendations
- Recommendation scores and reasons
- Can expire for freshness

### user_job_interactions
- Track user interactions for ML training
- VIEW, CLICK, APPLY, SAVE, SHARE, DISMISS
- Used for collecting training data, not storing full datasets

## ENUM Types

All ENUM types are defined at the database level:

- **user_role**: JOB_SEEKER, RECRUITER, ADMIN
- **experience_level**: ENTRY_LEVEL, JUNIOR, MID_LEVEL, SENIOR, EXECUTIVE
- **education_level**: HIGH_SCHOOL, ASSOCIATE, BACHELOR, MASTER, DOCTORATE, OTHER
- **employment_type**: FULL_TIME, PART_TIME, CONTRACT, TEMPORARY, INTERNSHIP, FREELANCE
- **application_status**: APPLIED, REVIEWED, SHORTLISTED, INTERVIEWED, ACCEPTED, REJECTED, WITHDRAWN
- **company_size**: STARTUP, SMALL, MEDIUM, LARGE, ENTERPRISE

## Indexes

### Performance Indexes
- All foreign keys are indexed
- Frequently queried columns (email, status, dates)
- Composite indexes for common query patterns

### Special Indexes
- **Full-text search**: GIN index on job_postings (title, description, requirements)
- **Array columns**: GIN indexes on skills, benefits, recommended_countries
- **JSONB columns**: Can be indexed for specific queries

## Triggers

### Auto-update Timestamps
- `update_updated_at_column()` function
- Automatically updates `updated_at` on row updates

### Application Count
- `update_job_applications_count()` function
- Automatically maintains `applications_count` in job_postings

## Constraints

### Data Validation
- Email format validation
- Salary range validation (min <= max)
- Probability/score range validation (0-1)
- Array length validation

### Referential Integrity
- Foreign keys with CASCADE or SET NULL
- Unique constraints prevent duplicates
- Check constraints validate data ranges

## SQLAlchemy Models

All models are defined in `backend/app/models/`:

- `user.py` - User model
- `job_seeker_profile.py` - Job seeker profile
- `recruiter_profile.py` - Recruiter profile
- `job_posting.py` - Job postings
- `job_application.py` - Job applications
- `ml_models.py` - ML result models
- `enums.py` - Enum type definitions

Models use:
- UUID primary keys (matching database)
- Proper relationships (matching foreign keys)
- Enum types (matching database ENUMs)
- Constraints (matching database constraints)

## Usage

### Create Database

```sql
CREATE DATABASE khadamni;
\c khadamni
\i backend/database/schema.sql
```

### Using with Alembic

```bash
cd backend
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Direct SQL

```bash
psql -U postgres -d khadamni -f backend/database/schema.sql
```

## Scalability Considerations

1. **Partitioning**: Consider partitioning large tables (job_applications, user_job_interactions) by date
2. **Archiving**: ML result tables can be archived periodically
3. **Connection Pooling**: Use connection pooling (SQLAlchemy default: 10)
4. **Read Replicas**: Use read replicas for scaling read operations

## Security

- Password hashes stored, never plain passwords
- Foreign keys ensure data integrity
- Constraints prevent invalid data
- Indexes on sensitive columns for quick lookups

## ML Integration

The schema supports ML features by:

1. **Storing Predictions**: Lightweight tables store only results
2. **Model Versioning**: Track which model version made predictions
3. **Input Features**: JSONB columns store input features for debugging
4. **Interaction Tracking**: user_job_interactions table for training data collection

## Maintenance

### Regular Tasks
- Run `VACUUM ANALYZE` regularly
- Monitor index usage
- Archive old ML predictions
- Update table statistics

### Monitoring
See `backend/database/QUERIES.md` for monitoring queries.

## Next Steps

1. **Apply Schema**: Run `schema.sql` to create the database
2. **Update Models**: Ensure SQLAlchemy models match the schema
3. **Test Queries**: Use queries from `QUERIES.md` to test
4. **Set Up Migrations**: Configure Alembic for future changes

