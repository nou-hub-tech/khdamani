# FastAPI Backend Implementation

## Overview

Complete FastAPI backend implementation with user authentication, role-based access control, job postings CRUD, and job applications.

## Features Implemented

### ✅ User Authentication
- User registration with email and password
- User login with JWT token generation
- Password hashing using bcrypt
- JWT access and refresh tokens

### ✅ Role-Based Access Control
- Two user roles: `JOB_SEEKER` and `RECRUITER`
- Role-based endpoint protection
- Dependency injection for role verification

### ✅ Job Postings CRUD
- **Create**: Recruiters can create job postings
- **Read**: Anyone can view jobs (with filters)
- **Update**: Recruiters can update their own jobs
- **Delete**: Recruiters can delete their own jobs

### ✅ Job Applications
- Job seekers can apply to jobs
- View own applications (job seekers)
- View applications for jobs (recruiters)
- Prevents duplicate applications

## Project Structure

```
backend/app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── jobs.py          # Job CRUD endpoints
│   │   │   └── applications.py  # Application endpoints
│   │   └── router.py            # API router
│   └── dependencies.py          # Auth dependencies
├── core/
│   ├── config.py                # Configuration
│   ├── database.py              # Database connection
│   └── security.py              # Security utilities
├── models/                       # SQLAlchemy models
├── repositories/                # Data access layer
│   ├── user_repository.py
│   ├── job_repository.py
│   └── job_application_repository.py
├── schemas/                      # Pydantic schemas
│   ├── user.py
│   ├── job.py
│   └── job_application.py
└── services/                     # Business logic
    ├── auth_service.py
    ├── job_service.py
    └── job_application_service.py
```

## Key Components

### Models (SQLAlchemy)
- `User` - User accounts with roles
- `JobPosting` - Job listings
- `JobApplication` - Job applications
- All use UUID primary keys

### Schemas (Pydantic)
- Request/response validation
- Type safety
- Automatic API documentation

### Repositories
- Data access layer
- CRUD operations
- Query building

### Services
- Business logic
- Validation
- Error handling

### Endpoints
- RESTful API design
- Proper HTTP status codes
- Error handling

## API Endpoints

See [API_ENDPOINTS.md](./API_ENDPOINTS.md) for complete API documentation.

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens

### Jobs
- `GET /api/v1/jobs` - List jobs (with filters)
- `GET /api/v1/jobs/{job_id}` - Get job by ID
- `POST /api/v1/jobs` - Create job (recruiter only)
- `PUT /api/v1/jobs/{job_id}` - Update job (recruiter only)
- `DELETE /api/v1/jobs/{job_id}` - Delete job (recruiter only)
- `POST /api/v1/jobs/{job_id}/apply` - Apply to job

### Applications
- `GET /api/v1/applications/my-applications` - Get my applications (job seeker)
- `GET /api/v1/applications/job/{job_id}` - Get job applications (recruiter)

## Security

### Authentication
- JWT tokens for authentication
- Password hashing with bcrypt
- Token expiration

### Authorization
- Role-based access control
- Endpoint-level protection
- User ownership verification

## Usage

### 1. Set up environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure database
Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/khadamni
SECRET_KEY=your-secret-key-here
```

### 3. Run database migrations
```bash
# Apply schema
psql -U postgres -d khadamni -f database/schema.sql

# Or use Alembic
alembic upgrade head
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

### 5. Access API documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Register a Job Seeker
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "seeker@example.com", "password": "pass123", "role": "JOB_SEEKER"}'
```

### Register a Recruiter
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "recruiter@example.com", "password": "pass123", "role": "RECRUITER"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "recruiter@example.com", "password": "pass123"}'
```

### Create Job (with token)
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

## Design Decisions

### UUID Primary Keys
- Better for distributed systems
- More secure (no sequential IDs)
- Easier to merge data

### Repository Pattern
- Separates data access from business logic
- Easier to test and maintain
- Can swap database implementations

### Service Layer
- Business logic separation
- Reusable across endpoints
- Easier to test

### Pydantic Schemas
- Request/response validation
- Automatic API documentation
- Type safety

## Next Steps

1. **Add Tests**: Unit tests, integration tests
2. **Add Validation**: More business rule validation
3. **Add Pagination**: Better pagination support
4. **Add Filtering**: More advanced filtering options
5. **Add Search**: Full-text search implementation
6. **Add Caching**: Redis caching for frequently accessed data

