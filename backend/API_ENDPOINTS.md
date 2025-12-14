# API Endpoints Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

### Register User
**POST** `/auth/register`

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "JOB_SEEKER"  // or "RECRUITER"
}
```

Response (201):
```json
{
  "message": "User registered successfully",
  "user_id": "uuid-here"
}
```

### Login
**POST** `/auth/login`

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response (200):
```json
{
  "access_token": "jwt-token-here",
  "refresh_token": "refresh-token-here",
  "token_type": "bearer"
}
```

**Note**: Include the access token in subsequent requests:
```
Authorization: Bearer <access_token>
```

---

## Jobs

### Get All Jobs
**GET** `/jobs`

Query parameters:
- `skip` (int, default: 0) - Pagination offset
- `limit` (int, default: 20) - Number of results
- `location` (string, optional) - Filter by location
- `title` (string, optional) - Filter by job title
- `is_active` (bool, default: true) - Filter by active status

Response (200):
```json
[
  {
    "id": "uuid",
    "title": "Software Engineer",
    "description": "Job description...",
    "location": "New York, NY",
    "salary_min": 80000.00,
    "salary_max": 120000.00,
    "required_skills": ["Python", "FastAPI"],
    "recruiter_id": "uuid",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

### Get Job by ID
**GET** `/jobs/{job_id}`

Response (200):
```json
{
  "id": "uuid",
  "title": "Software Engineer",
  "description": "Job description...",
  "location": "New York, NY",
  "salary_min": 80000.00,
  "salary_max": 120000.00,
  "required_skills": ["Python", "FastAPI"],
  "recruiter_id": "uuid",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Create Job (Recruiter Only)
**POST** `/jobs`

Headers:
```
Authorization: Bearer <token>
```

Request body:
```json
{
  "title": "Software Engineer",
  "description": "We are looking for...",
  "location": "New York, NY",
  "salary_min": 80000.00,
  "salary_max": 120000.00,
  "required_skills": ["Python", "FastAPI", "PostgreSQL"]
}
```

Response (201):
```json
{
  "id": "uuid",
  "title": "Software Engineer",
  "description": "We are looking for...",
  "location": "New York, NY",
  "salary_min": 80000.00,
  "salary_max": 120000.00,
  "required_skills": ["Python", "FastAPI", "PostgreSQL"],
  "recruiter_id": "uuid",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Update Job (Recruiter Only)
**PUT** `/jobs/{job_id}`

Headers:
```
Authorization: Bearer <token>
```

Request body (all fields optional):
```json
{
  "title": "Senior Software Engineer",
  "salary_max": 150000.00
}
```

Response (200): Updated job object

### Delete Job (Recruiter Only)
**DELETE** `/jobs/{job_id}`

Headers:
```
Authorization: Bearer <token>
```

Response (204): No content

### Apply to Job
**POST** `/jobs/{job_id}/apply`

Headers:
```
Authorization: Bearer <token>
```

Request body:
```json
{
  "cover_letter": "I am interested in this position...",
  "resume_url": "https://example.com/resume.pdf"
}
```

Response (201):
```json
{
  "id": "uuid",
  "job_id": "uuid",
  "job_seeker_id": "uuid",
  "status": "APPLIED",
  "cover_letter": "I am interested in this position...",
  "resume_url": "https://example.com/resume.pdf",
  "applied_at": "2024-01-01T00:00:00Z",
  "reviewed_at": null
}
```

---

## Applications

### Get My Applications (Job Seeker Only)
**GET** `/applications/my-applications`

Headers:
```
Authorization: Bearer <token>
```

Query parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 20)

Response (200):
```json
[
  {
    "id": "uuid",
    "job_id": "uuid",
    "job_seeker_id": "uuid",
    "status": "APPLIED",
    "cover_letter": "...",
    "resume_url": "...",
    "applied_at": "2024-01-01T00:00:00Z",
    "reviewed_at": null
  }
]
```

### Get Job Applications (Recruiter Only)
**GET** `/applications/job/{job_id}`

Headers:
```
Authorization: Bearer <token>
```

Query parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 20)

Response (200): List of applications for the job

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message here"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions. Recruiter access required."
}
```

### 404 Not Found
```json
{
  "detail": "Job not found"
}
```

---

## Example Usage

### 1. Register as Job Seeker
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jobseeker@example.com",
    "password": "password123",
    "role": "JOB_SEEKER"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jobseeker@example.com",
    "password": "password123"
  }'
```

### 3. Get Jobs
```bash
curl http://localhost:8000/api/v1/jobs?location=New%20York&limit=10
```

### 4. Apply to Job
```bash
curl -X POST http://localhost:8000/api/v1/jobs/{job_id}/apply \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "cover_letter": "I am very interested in this position..."
  }'
```

### 5. Create Job (Recruiter)
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "description": "We are looking for...",
    "location": "New York, NY",
    "salary_min": 80000,
    "salary_max": 120000,
    "required_skills": ["Python", "FastAPI"]
  }'
```

