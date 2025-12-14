# Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│                    (React + TypeScript)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Components  │  │    Pages     │  │    Hooks     │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                 │                 │
│         └─────────────────┼─────────────────┘                 │
│                           │                                   │
│                  ┌────────▼────────┐                          │
│                  │  API Services  │                          │
│                  │   (Axios)      │                          │
│                  └────────┬───────┘                          │
└───────────────────────────┼───────────────────────────────────┘
                            │ HTTP/REST + JWT
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                      BACKEND LAYER                            │
│                      (FastAPI)                                │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    API LAYER                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │   Auth   │  │   Jobs   │  │    ML    │            │  │
│  │  │ Endpoint │  │ Endpoint │  │ Endpoint │            │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │  │
│  └───────┼─────────────┼─────────────┼───────────────────┘  │
│          │             │             │                       │
│  ┌───────▼─────────────▼─────────────▼───────────────────┐  │
│  │              SERVICE LAYER                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │  │
│  │  │   Auth   │  │   Job    │  │  ML Integration │   │  │
│  │  │ Service  │  │ Service  │  │     Service     │   │  │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │  │
│  └───────┼─────────────┼─────────────────┼──────────────┘  │
│          │             │                 │                   │
│  ┌───────▼─────────────▼─────────────────┼──────────────┐  │
│  │          REPOSITORY LAYER              │              │  │
│  │  ┌──────────┐  ┌──────────┐            │              │  │
│  │  │   User   │  │   Job    │            │              │  │
│  │  │   Repo   │  │   Repo   │            │              │  │
│  │  └────┬─────┘  └────┬─────┘            │              │  │
│  └───────┼─────────────┼──────────────────┼──────────────┘  │
│          │             │                  │                  │
└──────────┼─────────────┼──────────────────┼──────────────────┘
           │             │                  │
           │             │                  │ HTTP/Async
           │             │                  │
┌──────────▼─────────────▼──────────────────▼──────────────────┐
│                    DATABASE                                  │
│                  (PostgreSQL)                                │
└──────────────────────────────────────────────────────────────┘
           │
           │
┌──────────┼──────────────────────────────────────────────────┐
│          │                                                  │
│  ┌───────▼──────────────────────────────────────────────┐  │
│  │              ML SERVICES LAYER                       │  │
│  │              (FastAPI Microservices)                  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │            ML API ENDPOINTS                   │   │  │
│  │  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │   │  │
│  │  │  │Salary│  │  Job │  │Fraud │  │Country│   │   │  │
│  │  │  │Predict│  │Recomm│  │Detect│  │Recomm│   │   │  │
│  │  │  └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘    │   │  │
│  │  └──────┼──────────┼──────────┼─────────┼───────┘   │  │
│  │         │          │          │         │            │  │
│  │  ┌──────▼──────────▼──────────▼─────────▼───────┐  │  │
│  │  │          ML SERVICE LAYER                     │  │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │  │  │
│  │  │  │  Salary  │  │   Job    │  │  Fraud   │   │  │  │
│  │  │  │Predictor │  │Recommender│  │ Detector │   │  │  │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘   │  │  │
│  │  └───────┼─────────────┼─────────────┼──────────┘  │  │
│  │          │             │             │              │  │
│  │  ┌───────▼─────────────▼─────────────▼──────────┐  │  │
│  │  │         MODEL LOADER & CACHE                  │  │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │  │  │
│  │  │  │  Model   │  │  Scaler  │  │ Encoder  │   │  │  │
│  │  │  │  Files   │  │  Files   │  │  Files   │   │  │  │
│  │  │  └──────────┘  └──────────┘  └──────────┘   │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. User Views Job with Salary Prediction

```
User Action (Frontend)
    ↓
React Component calls jobsApi.getJobById(id)
    ↓
API Service (Axios) → GET /api/v1/jobs/{id}
    ↓
Backend: jobs.py endpoint
    ↓
JobService.get_job_by_id()
    ↓
JobRepository.get_by_id() → Database
    ↓
Response with Job Data
    ↓
Frontend displays job
    ↓
User clicks "Predict Salary"
    ↓
React Component calls mlApi.predictSalary()
    ↓
API Service → POST /api/v1/ml/salary/predict
    ↓
Backend: ml_services.py endpoint
    ↓
MLIntegrationService.predict_salary()
    ↓
HTTP Request → ML Service: POST /api/salary/predict
    ↓
ML Service: SalaryPredictor.predict()
    ↓
Model Inference → Prediction Result
    ↓
Response flows back through layers
    ↓
Frontend displays predicted salary
```

### 2. Recruiter Posts Job (with Fraud Detection)

```
Recruiter fills form (Frontend)
    ↓
React Component calls jobsApi.createJob()
    ↓
API Service → POST /api/v1/jobs
    ↓
Backend: jobs.py endpoint (with auth)
    ↓
JobService.create_job()
    ↓
MLIntegrationService.detect_fraud() [Async]
    ↓
HTTP Request → ML Service: POST /api/fraud/detect
    ↓
ML Service: FraudDetector.detect()
    ↓
Model Inference → Fraud Score
    ↓
If fraud_probability > threshold:
    → Flag job for review
    → Return warning to recruiter
Else:
    → JobRepository.create() → Database
    → Return success
```

## Component Interactions

### Frontend-Backend Communication
- **Protocol**: HTTP/HTTPS
- **Format**: JSON
- **Auth**: JWT Bearer tokens
- **Error Handling**: Standardized error responses

### Backend-ML Services Communication
- **Protocol**: HTTP/HTTPS (Async)
- **Format**: JSON
- **Pattern**: Service-to-service communication
- **Timeout**: 30 seconds default
- **Error Handling**: Graceful degradation if ML service unavailable

### Database Access
- **ORM**: SQLAlchemy
- **Pattern**: Repository pattern
- **Connection**: Connection pooling
- **Migrations**: Alembic

