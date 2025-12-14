# Architecture Summary

## Quick Reference

This document provides a quick overview of the architecture. For detailed documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 1. Folder Structure Overview

```
Khadamni/
├── frontend/          # React + TypeScript + Tailwind CSS
├── backend/           # FastAPI (Python)
├── ml_services/       # ML models as FastAPI microservices
├── docker/            # Docker configurations
└── docs/              # Documentation
```

---

## 2. Layer Responsibilities

### Frontend (`frontend/`)
- **Components**: Reusable UI components
- **Pages**: Route-level page components
- **Services**: API communication layer (axios)
- **Store**: Global state management (Zustand)
- **Hooks**: Custom React hooks
- **Types**: TypeScript type definitions

### Backend (`backend/app/`)
- **API Layer** (`api/`): HTTP endpoints, request/response handling
- **Core Layer** (`core/`): Configuration, security, database connection
- **Models Layer** (`models/`): SQLAlchemy ORM models
- **Schemas Layer** (`schemas/`): Pydantic validation schemas
- **Services Layer** (`services/`): Business logic
- **Repositories Layer** (`repositories/`): Data access (CRUD operations)

### ML Services (`ml_services/`)
- **Models** (`models/`): Trained ML model files
- **Services** (`services/`): Model inference logic
- **API** (`api/`): FastAPI endpoints for ML predictions
- **Training** (`training/`): Model training scripts

---

## 3. Frontend-Backend Communication

### Flow
```
React Component → API Service → Axios Client → Backend API → Service → Repository → Database
```

### Implementation
- **Protocol**: RESTful API over HTTP/HTTPS
- **Format**: JSON request/response
- **Authentication**: JWT tokens in `Authorization: Bearer <token>` header
- **Error Handling**: Standardized error responses with HTTP status codes
- **API Client**: Centralized axios instance with interceptors (`frontend/src/services/api/client.ts`)

### Example
```typescript
// Frontend
import { jobsApi } from './services/api/jobs';
const jobs = await jobsApi.getJobs({ location: 'New York' });
```

```python
# Backend
@router.get("/jobs")
async def get_jobs(location: str = None):
    return await job_service.get_jobs(location=location)
```

---

## 4. ML Models Integration

### Architecture Pattern
ML models are **separate microservices** that can scale independently.

### Flow
```
Backend Service → ML Integration Service → ML Service API → ML Model → Prediction
```

### Implementation

#### 1. ML Service Endpoint (`ml_services/api/endpoints/`)
Each ML feature has its own FastAPI endpoint:
- `/api/salary/predict` - Salary prediction
- `/api/jobs/recommend` - Job recommendations
- `/api/fraud/detect` - Fraud detection
- `/api/country/recommend` - Country recommendations

#### 2. Backend Integration (`backend/app/services/ml_integration_service.py`)
The backend service acts as a client to ML services:
```python
ml_service = MLIntegrationService()
prediction = await ml_service.predict_salary(job_data, user_profile)
```

#### 3. Frontend Access (`backend/app/api/v1/endpoints/ml_services.py`)
Backend exposes ML features to frontend:
```python
@router.post("/ml/salary/predict")
async def predict_salary(request: SalaryPredictionRequest):
    return await ml_service.predict_salary(...)
```

### ML Features

1. **Salary Prediction**
   - Input: Job details + user profile
   - Output: Predicted salary range
   - Trigger: When job seeker views a job

2. **Job Recommendation**
   - Input: User profile, history, preferences
   - Output: Ranked job list
   - Trigger: On login or search

3. **Fraud Detection**
   - Input: Job posting details
   - Output: Fraud probability score
   - Trigger: When recruiter posts a job

4. **Country Recommendation**
   - Input: User skills, experience, preferences
   - Output: Recommended countries
   - Trigger: When user sets preferences

---

## 5. Key Design Decisions

### Separation of Concerns
- **Frontend**: UI/UX only, no business logic
- **Backend**: Business logic, data validation, orchestration
- **ML Services**: Model inference only, isolated from main backend

### Scalability
- **Microservices**: ML services can scale independently
- **Stateless**: Backend is stateless, can run multiple instances
- **Database**: Connection pooling, read replicas for scaling

### Security
- **JWT Authentication**: Stateless token-based auth
- **Role-Based Access**: Job seeker, recruiter, admin roles
- **Input Validation**: Pydantic schemas validate all inputs
- **Password Hashing**: bcrypt with salt

### Maintainability
- **Layered Architecture**: Clear separation between layers
- **Repository Pattern**: Isolates data access logic
- **Service Layer**: Centralizes business logic
- **Type Safety**: TypeScript on frontend, Pydantic on backend

---

## 6. Development Workflow

1. **Local Development**
   ```bash
   # Backend
   cd backend && uvicorn app.main:app --reload
   
   # ML Services
   cd ml_services && uvicorn main:app --reload --port 8001
   
   # Frontend
   cd frontend && npm run dev
   ```

2. **Docker Development**
   ```bash
   docker-compose up
   ```

3. **Database Migrations**
   ```bash
   cd backend
   alembic revision --autogenerate -m "description"
   alembic upgrade head
   ```

---

## 7. API Endpoints Overview

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens

### Jobs
- `GET /api/v1/jobs` - Get all jobs (with filters)
- `GET /api/v1/jobs/{id}` - Get single job
- `POST /api/v1/jobs` - Create job (recruiter)
- `PUT /api/v1/jobs/{id}` - Update job (recruiter)
- `DELETE /api/v1/jobs/{id}` - Delete job (recruiter)
- `POST /api/v1/jobs/{id}/apply` - Apply to job (job seeker)

### ML Services
- `POST /api/v1/ml/salary/predict` - Predict salary
- `GET /api/v1/ml/jobs/recommend` - Get job recommendations
- `POST /api/v1/ml/fraud/detect` - Detect fraud
- `POST /api/v1/ml/country/recommend` - Get country recommendations

---

## 8. Next Steps

1. **Database Setup**: Create PostgreSQL database and run migrations
2. **Model Training**: Train and save ML models in `ml_services/models/`
3. **Frontend UI**: Build React components and pages
4. **Testing**: Add unit, integration, and E2E tests
5. **Deployment**: Set up CI/CD and deploy to production

---

For detailed information, see [ARCHITECTURE.md](./ARCHITECTURE.md).

