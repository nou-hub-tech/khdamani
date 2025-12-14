# Job Search Platform - Architecture Documentation

## Overview

This document describes the architecture of a scalable job search platform with ML-powered features, supporting both job seekers and recruiters.

## Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ML Services**: Python (scikit-learn, TensorFlow/PyTorch) exposed via FastAPI endpoints

---

## 1. Folder Structure

```
Khadamni/
├── frontend/                    # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── common/          # Common components (Button, Input, etc.)
│   │   │   ├── job-seeker/      # Job seeker specific components
│   │   │   └── recruiter/       # Recruiter specific components
│   │   ├── pages/               # Page components
│   │   │   ├── job-seeker/      # Job seeker pages
│   │   │   └── recruiter/       # Recruiter pages
│   │   ├── services/            # API service layer
│   │   │   ├── api/             # API client functions
│   │   │   └── auth/            # Authentication service
│   │   ├── hooks/               # Custom React hooks
│   │   ├── store/               # State management (Redux/Zustand)
│   │   │   ├── slices/          # Redux slices or Zustand stores
│   │   │   └── middleware/      # Redux middleware
│   │   ├── utils/               # Utility functions
│   │   ├── types/               # TypeScript type definitions
│   │   ├── constants/           # Constants and configuration
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── api/                 # API route handlers
│   │   │   ├── v1/              # API version 1
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   │   ├── job_seekers.py   # Job seeker endpoints
│   │   │   │   │   ├── recruiters.py    # Recruiter endpoints
│   │   │   │   │   ├── jobs.py          # Job listing endpoints
│   │   │   │   │   └── ml_services.py   # ML service endpoints
│   │   │   │   └── router.py            # API router aggregation
│   │   │   └── dependencies.py          # FastAPI dependencies
│   │   │
│   │   ├── core/                # Core configuration
│   │   │   ├── config.py        # Application configuration
│   │   │   ├── security.py      # Security utilities (JWT, hashing)
│   │   │   └── database.py      # Database connection
│   │   │
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── user.py          # User model
│   │   │   ├── job_seeker.py    # Job seeker model
│   │   │   ├── recruiter.py     # Recruiter model
│   │   │   ├── job.py           # Job posting model
│   │   │   └── application.py   # Job application model
│   │   │
│   │   ├── schemas/             # Pydantic schemas (request/response)
│   │   │   ├── user.py
│   │   │   ├── job_seeker.py
│   │   │   ├── recruiter.py
│   │   │   ├── job.py
│   │   │   └── ml_requests.py
│   │   │
│   │   ├── services/            # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── job_seeker_service.py
│   │   │   ├── recruiter_service.py
│   │   │   ├── job_service.py
│   │   │   └── ml_integration_service.py  # ML service integration
│   │   │
│   │   ├── repositories/        # Data access layer
│   │   │   ├── user_repository.py
│   │   │   ├── job_seeker_repository.py
│   │   │   ├── recruiter_repository.py
│   │   │   └── job_repository.py
│   │   │
│   │   ├── middleware/          # Custom middleware
│   │   │   ├── auth_middleware.py
│   │   │   └── error_handler.py
│   │   │
│   │   └── main.py              # FastAPI application entry point
│   │
│   ├── alembic/                 # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/                   # Backend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── ml_services/                 # ML models and services
│   ├── models/                  # Trained ML models
│   │   ├── salary_predictor/
│   │   ├── job_recommender/
│   │   ├── fraud_detector/
│   │   └── country_recommender/
│   │
│   ├── services/                # ML service implementations
│   │   ├── salary_predictor.py
│   │   ├── job_recommender.py
│   │   ├── fraud_detector.py
│   │   └── country_recommender.py
│   │
│   ├── api/                     # FastAPI endpoints for ML services
│   │   ├── endpoints/
│   │   │   ├── salary.py
│   │   │   ├── recommendation.py
│   │   │   ├── fraud.py
│   │   │   └── country.py
│   │   └── router.py
│   │
│   ├── training/                # Model training scripts
│   │   ├── train_salary_predictor.py
│   │   ├── train_job_recommender.py
│   │   ├── train_fraud_detector.py
│   │   └── train_country_recommender.py
│   │
│   ├── data/                    # Training data and preprocessing
│   │   ├── raw/
│   │   ├── processed/
│   │   └── preprocessing.py
│   │
│   ├── utils/                   # ML utilities
│   │   ├── feature_engineering.py
│   │   └── model_loader.py
│   │
│   ├── requirements.txt
│   └── main.py                  # ML service FastAPI app
│
├── shared/                      # Shared code/types
│   ├── types/                   # Shared TypeScript types
│   └── constants/               # Shared constants
│
├── docker/                      # Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── Dockerfile.ml_services
│   └── docker-compose.yml
│
├── scripts/                     # Utility scripts
│   ├── setup.sh
│   └── seed_data.py
│
├── docs/                        # Additional documentation
│   └── api/                     # API documentation
│
├── .gitignore
├── README.md
└── ARCHITECTURE.md              # This file
```

---

## 2. Responsibilities of Each Layer

### Frontend Layer (`frontend/`)

**Components:**
- **UI Components** (`components/`): Reusable, presentational components
- **Pages** (`pages/`): Route-level components that compose UI components
- **Services** (`services/`): API communication layer, handles HTTP requests/responses
- **Store** (`store/`): Global state management (user auth, job listings, etc.)
- **Hooks** (`hooks/`): Custom React hooks for reusable logic
- **Utils** (`utils/`): Helper functions, formatters, validators

**Responsibilities:**
- User interface rendering and interaction
- Client-side routing
- Form validation and user input handling
- State management for UI state
- API communication with backend
- Authentication token management
- Error handling and user feedback

### Backend Layer (`backend/app/`)

**API Layer** (`api/`):
- **Endpoints**: Define HTTP routes, request/response handling
- **Dependencies**: Shared dependencies (auth, database sessions)
- **Router**: Aggregates all API routes

**Core Layer** (`core/`):
- **Config**: Environment variables, application settings
- **Security**: JWT token generation/validation, password hashing
- **Database**: Database connection, session management

**Models Layer** (`models/`):
- SQLAlchemy ORM models representing database tables
- Relationships between entities
- Database schema definition

**Schemas Layer** (`schemas/`):
- Pydantic models for request/response validation
- Data serialization/deserialization
- API contract definition

**Services Layer** (`services/`):
- **Business Logic**: Core application logic
- **Validation**: Business rule validation
- **Orchestration**: Coordinates between repositories and external services
- **ML Integration**: Communicates with ML services

**Repositories Layer** (`repositories/`):
- **Data Access**: Database CRUD operations
- **Query Building**: Complex database queries
- **Data Mapping**: ORM to domain object conversion

**Middleware Layer** (`middleware/`):
- **Authentication**: Token validation, user context
- **Error Handling**: Global exception handling, error formatting
- **Logging**: Request/response logging
- **CORS**: Cross-origin resource sharing

**Responsibilities:**
- RESTful API endpoints
- Authentication and authorization
- Business logic execution
- Database operations
- Data validation
- Integration with ML services
- Error handling and logging

### ML Services Layer (`ml_services/`)

**Models** (`models/`):
- Trained model files (pickle, joblib, or TensorFlow SavedModel)
- Model metadata and versioning

**Services** (`services/`):
- Model inference logic
- Feature preprocessing
- Prediction generation
- Model loading and caching

**API** (`api/`):
- FastAPI endpoints for ML predictions
- Request/response handling for ML features
- Model version management

**Training** (`training/`):
- Model training scripts
- Hyperparameter tuning
- Model evaluation and validation
- Model persistence

**Responsibilities:**
- Salary prediction based on job details and user profile
- Job recommendation based on user preferences and history
- Fraud detection for job postings and applications
- Country recommendation for job seekers
- Model training and retraining
- Model versioning and deployment

---

## 3. Frontend-Backend Communication

### Communication Flow

```
Frontend (React) → API Service Layer → Backend (FastAPI) → Service Layer → Repository → Database
                                                              ↓
                                                         ML Services
```

### Implementation Details

#### 1. **API Service Layer** (`frontend/src/services/api/`)

```typescript
// Example: frontend/src/services/api/jobs.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
    }
    return Promise.reject(error);
  }
);
```

#### 2. **Backend API Endpoints** (`backend/app/api/v1/endpoints/`)

```python
# Example: backend/app/api/v1/endpoints/jobs.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends()
):
    return await job_service.create_job(job_data, current_user.id)
```

#### 3. **Communication Patterns**

- **RESTful API**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **Authentication**: JWT tokens sent in `Authorization: Bearer <token>` header
- **Error Handling**: Standardized error responses with status codes
- **Request/Response Format**: JSON
- **API Versioning**: `/api/v1/` prefix for future compatibility

#### 4. **Data Flow Example**

1. User action in React component
2. Component calls service function (`services/api/jobs.ts`)
3. Service makes HTTP request to backend
4. Backend endpoint receives request
5. Endpoint validates request using Pydantic schema
6. Endpoint calls service layer
7. Service layer executes business logic
8. Service calls repository for data access
9. Repository queries database
10. Response flows back through layers
11. Frontend receives response and updates UI

---

## 4. ML Models Integration

### Architecture Pattern

ML models are integrated as **separate microservices** that can be called by the main backend application.

### Integration Flow

```
Backend Service → ML Integration Service → ML Service API → ML Model → Prediction Response
```

### Implementation Details

#### 1. **ML Service API** (`ml_services/api/`)

Each ML feature is exposed as a FastAPI endpoint:

```python
# Example: ml_services/api/endpoints/salary.py
from fastapi import APIRouter
from ml_services.services.salary_predictor import SalaryPredictor
from ml_services.schemas.salary import SalaryPredictionRequest, SalaryPredictionResponse

router = APIRouter(prefix="/salary", tags=["salary"])

@router.post("/predict", response_model=SalaryPredictionResponse)
async def predict_salary(request: SalaryPredictionRequest):
    predictor = SalaryPredictor()
    prediction = predictor.predict(
        experience_years=request.experience_years,
        job_title=request.job_title,
        location=request.location,
        skills=request.skills
    )
    return SalaryPredictionResponse(predicted_salary=prediction)
```

#### 2. **ML Integration Service** (`backend/app/services/ml_integration_service.py`)

This service acts as a client to communicate with ML services:

```python
# Example: backend/app/services/ml_integration_service.py
import httpx
from app.core.config import settings

class MLIntegrationService:
    def __init__(self):
        self.ml_service_url = settings.ML_SERVICE_URL
    
    async def predict_salary(self, job_data: dict, user_profile: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ml_service_url}/api/salary/predict",
                json={
                    "experience_years": user_profile.get("experience_years"),
                    "job_title": job_data.get("title"),
                    "location": job_data.get("location"),
                    "skills": user_profile.get("skills")
                }
            )
            return response.json()
    
    async def recommend_jobs(self, user_id: int, limit: int = 10):
        # Similar implementation for job recommendations
        pass
    
    async def detect_fraud(self, job_posting: dict):
        # Similar implementation for fraud detection
        pass
    
    async def recommend_country(self, user_profile: dict):
        # Similar implementation for country recommendation
        pass
```

#### 3. **Backend Endpoint Integration** (`backend/app/api/v1/endpoints/ml_services.py`)

Backend exposes ML features to frontend:

```python
# Example: backend/app/api/v1/endpoints/ml_services.py
from fastapi import APIRouter, Depends
from app.services.ml_integration_service import MLIntegrationService
from app.schemas.ml_requests import SalaryPredictionRequest

router = APIRouter(prefix="/ml", tags=["ml-services"])

@router.post("/salary/predict")
async def predict_salary(
    request: SalaryPredictionRequest,
    ml_service: MLIntegrationService = Depends(),
    current_user: User = Depends(get_current_user)
):
    prediction = await ml_service.predict_salary(
        job_data=request.job_data,
        user_profile=request.user_profile
    )
    return prediction
```

#### 4. **ML Model Loading** (`ml_services/services/`)

Models are loaded once at startup and cached:

```python
# Example: ml_services/services/salary_predictor.py
import joblib
from ml_services.utils.model_loader import ModelLoader

class SalaryPredictor:
    def __init__(self):
        self.model = ModelLoader.load_model("salary_predictor")
        self.scaler = ModelLoader.load_scaler("salary_predictor")
    
    def predict(self, experience_years, job_title, location, skills):
        # Feature engineering
        features = self._engineer_features(
            experience_years, job_title, location, skills
        )
        # Preprocessing
        features_scaled = self.scaler.transform([features])
        # Prediction
        prediction = self.model.predict(features_scaled)[0]
        return float(prediction)
```

### ML Features Integration Points

1. **Salary Prediction**:
   - Triggered when: Job seeker views a job posting
   - Input: Job details + user profile
   - Output: Predicted salary range

2. **Job Recommendation**:
   - Triggered when: Job seeker logs in or searches
   - Input: User profile, search history, preferences
   - Output: Ranked list of recommended jobs

3. **Fraud Detection**:
   - Triggered when: Recruiter posts a job
   - Input: Job posting details
   - Output: Fraud probability score

4. **Country Recommendation**:
   - Triggered when: Job seeker sets preferences
   - Input: User skills, experience, preferences
   - Output: Recommended countries with opportunities

### Deployment Considerations

- **ML Services** can run as separate containers/services
- **Model Versioning**: Track model versions and allow rollback
- **Caching**: Cache predictions for frequently requested data
- **Async Processing**: For heavy ML tasks, use background jobs (Celery)
- **Monitoring**: Track prediction latency and accuracy

---

## 5. Database Schema Overview

### Key Tables

- `users`: Base user table (email, password_hash, role)
- `job_seekers`: Job seeker profile (skills, experience, preferences)
- `recruiters`: Recruiter profile (company, verification status)
- `jobs`: Job postings (title, description, salary_range, location)
- `applications`: Job applications (status, applied_at)
- `user_job_interactions`: For ML (views, clicks, applications)

---

## 6. Security Considerations

- **Authentication**: JWT tokens with refresh mechanism
- **Authorization**: Role-based access control (job_seeker, recruiter, admin)
- **Password Hashing**: bcrypt with salt
- **Input Validation**: Pydantic schemas for all inputs
- **SQL Injection**: SQLAlchemy ORM prevents SQL injection
- **CORS**: Configured for frontend domain
- **Rate Limiting**: Implement rate limiting on API endpoints

---

## 7. Scalability Considerations

- **Database**: Connection pooling, read replicas for scaling
- **Caching**: Redis for frequently accessed data
- **Background Jobs**: Celery for async tasks (email sending, ML batch processing)
- **Load Balancing**: Multiple backend instances behind load balancer
- **CDN**: Static assets served via CDN
- **Microservices**: ML services can scale independently

---

## 8. Development Workflow

1. **Local Development**: Docker Compose for all services
2. **Database Migrations**: Alembic for schema changes
3. **Testing**: Unit tests, integration tests, E2E tests
4. **CI/CD**: Automated testing and deployment
5. **Monitoring**: Logging, error tracking, performance monitoring

