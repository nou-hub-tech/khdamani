# Common Database Queries

This document contains useful SQL queries for the job search platform.

## User Queries

### Get user with profile
```sql
-- Get job seeker with profile
SELECT u.*, jsp.*
FROM users u
LEFT JOIN job_seeker_profiles jsp ON u.id = jsp.user_id
WHERE u.id = 'user-uuid-here';

-- Get recruiter with profile
SELECT u.*, rp.*
FROM users u
LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
WHERE u.id = 'user-uuid-here';
```

## Job Queries

### Search jobs with filters
```sql
-- Search jobs by location and title
SELECT *
FROM job_postings
WHERE is_active = TRUE
  AND (location ILIKE '%New York%' OR location ILIKE '%NYC%')
  AND title ILIKE '%Software Engineer%'
  AND (salary_min IS NULL OR salary_min >= 80000)
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;
```

### Full-text search
```sql
-- Full-text search on job postings
SELECT *, ts_rank_cd(
    to_tsvector('english', title || ' ' || description || ' ' || COALESCE(requirements, '')),
    plainto_tsquery('english', 'python developer')
) AS rank
FROM job_postings
WHERE to_tsvector('english', title || ' ' || description || ' ' || COALESCE(requirements, ''))
      @@ plainto_tsquery('english', 'python developer')
  AND is_active = TRUE
ORDER BY rank DESC, created_at DESC;
```

### Jobs by recruiter
```sql
-- Get all jobs posted by a recruiter
SELECT jp.*, COUNT(ja.id) as application_count
FROM job_postings jp
LEFT JOIN job_applications ja ON jp.id = ja.job_id
WHERE jp.recruiter_id = 'recruiter-uuid-here'
GROUP BY jp.id
ORDER BY jp.created_at DESC;
```

## Application Queries

### User's applications
```sql
-- Get all applications for a job seeker
SELECT ja.*, jp.title, jp.location, jp.company_name
FROM job_applications ja
JOIN job_postings jp ON ja.job_id = jp.id
WHERE ja.job_seeker_id = 'user-uuid-here'
ORDER BY ja.applied_at DESC;
```

### Job applications summary
```sql
-- Get application statistics for a job
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM job_applications
WHERE job_id = 'job-uuid-here'
GROUP BY status;
```

## ML Queries

### Recent salary predictions
```sql
-- Get recent salary predictions for a user
SELECT *
FROM salary_predictions
WHERE user_id = 'user-uuid-here'
ORDER BY created_at DESC
LIMIT 10;
```

### Fraud detection results
```sql
-- Get jobs flagged as potential fraud
SELECT jp.*, fdr.fraud_probability, fdr.reasons
FROM job_postings jp
JOIN fraud_detection_results fdr ON jp.id = fdr.job_id
WHERE fdr.is_fraud = TRUE
  AND fdr.reviewed_at IS NULL
ORDER BY fdr.fraud_probability DESC;
```

### Job recommendations for user
```sql
-- Get top job recommendations for a user
SELECT jp.*, jr.recommendation_score, jr.recommendation_reasons
FROM job_recommendations jr
JOIN job_postings jp ON jr.job_id = jp.id
WHERE jr.user_id = 'user-uuid-here'
  AND jp.is_active = TRUE
  AND (jr.expires_at IS NULL OR jr.expires_at > NOW())
ORDER BY jr.recommendation_score DESC
LIMIT 20;
```

### Country recommendations
```sql
-- Get country recommendations for a user
SELECT recommended_countries, country_scores, created_at
FROM country_recommendations
WHERE user_id = 'user-uuid-here'
ORDER BY created_at DESC
LIMIT 1;
```

## Analytics Queries

### Popular job titles
```sql
-- Most popular job titles
SELECT 
    title,
    COUNT(*) as job_count,
    AVG(salary_min + salary_max) / 2 as avg_salary
FROM job_postings
WHERE is_active = TRUE
  AND salary_min IS NOT NULL
  AND salary_max IS NOT NULL
GROUP BY title
ORDER BY job_count DESC
LIMIT 20;
```

### User engagement
```sql
-- User interaction statistics
SELECT 
    interaction_type,
    COUNT(*) as count,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT job_id) as unique_jobs
FROM user_job_interactions
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY interaction_type;
```

### Application conversion funnel
```sql
-- Application funnel analysis
WITH interactions AS (
    SELECT 
        job_id,
        COUNT(*) FILTER (WHERE interaction_type = 'VIEW') as views,
        COUNT(*) FILTER (WHERE interaction_type = 'CLICK') as clicks,
        COUNT(*) FILTER (WHERE interaction_type = 'APPLY') as applies
    FROM user_job_interactions
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY job_id
)
SELECT 
    SUM(views) as total_views,
    SUM(clicks) as total_clicks,
    SUM(applies) as total_applies,
    ROUND(SUM(clicks) * 100.0 / NULLIF(SUM(views), 0), 2) as click_rate,
    ROUND(SUM(applies) * 100.0 / NULLIF(SUM(clicks), 0), 2) as apply_rate
FROM interactions;
```

## Maintenance Queries

### Table sizes
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Index usage
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

### Archive old ML predictions
```sql
-- Archive salary predictions older than 1 year
DELETE FROM salary_predictions
WHERE created_at < NOW() - INTERVAL '1 year';
```

