# Entity Relationship Diagram

## Database Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                         CORE ENTITIES                           │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │    users    │
                    │  (UUID PK)  │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            │              │              │
    ┌───────▼──────┐  ┌────▼──────┐  ┌───▼──────────┐
    │job_seeker_   │  │recruiter_ │  │job_postings  │
    │profiles      │  │profiles   │  │              │
    │(1:1)         │  │(1:1)      │  │(1:many)      │
    └──────────────┘  └───────────┘  └───┬──────────┘
                                          │
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
            ┌───────▼──────┐      ┌───────▼──────┐    ┌────────▼────────┐
            │job_          │      │fraud_         │    │user_job_        │
            │applications  │      │detection_     │    │interactions     │
            │(many:many)   │      │results        │    │(many:many)       │
            └──────┬───────┘      └───────────────┘    └─────────────────┘
                   │
                   │
            ┌───────▼──────┐
            │    users     │
            │ (job_seeker) │
            └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      ML RESULT ENTITIES                          │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   users     │
    └──────┬──────┘
           │
    ┌──────┼──────────────────────────────────────┐
    │      │                                      │
    │      │                                      │
┌───▼──────▼──┐  ┌──────────────┐  ┌─────────────▼────────┐
│salary_      │  │country_      │  │job_                   │
│predictions  │  │recommendations│  │recommendations       │
│             │  │              │  │                      │
│(many:1)     │  │(many:1)      │  │(many:1)              │
└─────────────┘  └──────────────┘  └──────────────────────┘
```

## Relationship Details

### One-to-One Relationships
- `users` ↔ `job_seeker_profiles` (via user_id)
- `users` ↔ `recruiter_profiles` (via user_id)

### One-to-Many Relationships
- `users` (recruiter) → `job_postings` (via recruiter_id)
- `users` (job_seeker) → `job_applications` (via job_seeker_id)
- `job_postings` → `job_applications` (via job_id)
- `job_postings` → `fraud_detection_results` (via job_id)
- `users` → `salary_predictions` (via user_id, optional)
- `users` → `country_recommendations` (via user_id)
- `users` → `job_recommendations` (via user_id)
- `users` → `user_job_interactions` (via user_id)
- `job_postings` → `user_job_interactions` (via job_id)
- `job_postings` → `job_recommendations` (via job_id)

### Many-to-Many (via junction table)
- `users` (job_seekers) ↔ `job_postings` (via `job_applications`)
- `users` ↔ `job_postings` (via `user_job_interactions`)

## Foreign Key Actions

- **CASCADE**: Delete related records when parent is deleted
  - Profiles, applications, ML results tied to jobs/users
- **SET NULL**: Set to NULL when parent is deleted
  - Optional references in ML results (user_id, job_id in salary_predictions)

## Key Constraints

- **Unique**: (user_id) in job_seeker_profiles and recruiter_profiles
- **Unique**: (job_id, job_seeker_id) in job_applications
- **Unique**: (user_id, job_id, model_version) in job_recommendations

