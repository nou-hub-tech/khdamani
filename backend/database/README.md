# Database Schema Documentation

## Overview

This directory contains the PostgreSQL database schema for the Khadamni job search platform. The schema is designed to be:

- **Normalized**: Follows 3NF to reduce data redundancy
- **Scalable**: Uses indexes and proper data types for performance
- **ML-Ready**: Includes lightweight tables for storing ML prediction results
- **Type-Safe**: Uses ENUMs and constraints for data integrity

## Schema Files

- `schema.sql`: Complete database schema with all tables, indexes, triggers, and functions

## Key Design Decisions

### 1. UUID Primary Keys
- All tables use UUID primary keys for better distribution and security
- Enables easier sharding and replication in the future

### 2. ENUM Types
- Used for fixed sets of values (roles, statuses, levels)
- Provides type safety and better performance than VARCHAR
- Easier to maintain and validate

### 3. Array Columns
- Used for skills, benefits, and other multi-value fields
- PostgreSQL arrays are efficient and support GIN indexes
- Easier to query than separate junction tables for simple cases

### 4. JSONB Columns
- Used for flexible metadata storage (input_features, interaction_data)
- Supports indexing and efficient querying
- Allows schema evolution without migrations

### 5. ML Result Tables
- Store only prediction results, not training data
- Include model versioning for tracking
- Lightweight and queryable

## Table Relationships

```
users (1) ──< (1) job_seeker_profiles
users (1) ──< (1) recruiter_profiles
users (1) ──< (*) job_postings
users (1) ──< (*) job_applications
job_postings (1) ──< (*) job_applications
job_postings (1) ──< (*) fraud_detection_results
users (1) ──< (*) salary_predictions
users (1) ──< (*) country_recommendations
users (1) ──< (*) job_recommendations
users (1) ──< (*) user_job_interactions
```

## Usage

### Create Database

```sql
CREATE DATABASE khadamni;
\c khadamni
\i schema.sql
```

### Using with Alembic

The schema is designed to work with Alembic migrations. You can:

1. Generate initial migration from models:
```bash
alembic revision --autogenerate -m "Initial schema"
```

2. Or use the SQL file directly:
```bash
psql -U postgres -d khadamni -f database/schema.sql
```

## Indexes

The schema includes indexes for:
- Foreign keys (for JOIN performance)
- Frequently queried columns (email, status, dates)
- Full-text search (job postings)
- Array columns (GIN indexes for skills)
- Composite indexes for common query patterns

## Performance Considerations

1. **Indexes**: All foreign keys and frequently queried columns are indexed
2. **Partitioning**: Consider partitioning large tables (job_applications, user_job_interactions) by date if needed
3. **Archiving**: ML result tables can be archived periodically to keep them lightweight
4. **Connection Pooling**: Use connection pooling (SQLAlchemy default pool size: 10)

## Security

- Password hashes are stored, never plain passwords
- Foreign keys with CASCADE/SET NULL for data integrity
- Constraints prevent invalid data entry
- Indexes on sensitive columns (email) for quick lookups

## ML Integration

The schema supports ML features by:

1. **Storing Predictions**: Lightweight tables store only results
2. **Model Versioning**: Track which model version made predictions
3. **Input Features**: JSONB columns store input features for debugging
4. **Interaction Tracking**: user_job_interactions table for training data collection

## Maintenance

### Regular Tasks

1. **Vacuum**: Run `VACUUM ANALYZE` regularly
2. **Index Maintenance**: Monitor index usage and remove unused indexes
3. **Archiving**: Archive old ML predictions and interactions
4. **Statistics**: Update table statistics for query planner

### Monitoring Queries

```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

