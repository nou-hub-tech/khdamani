# ML Services

FastAPI microservice for ML-powered features of the job search platform.

## Features

1. **Salary Prediction** - Predicts salary based on job and employee features
2. **Job Recommendations** - Recommends top 5 jobs based on job seeker profile
3. **Country Recommendations** - Recommends top 5 countries for job hunting
4. **Fraud Detection** - Detects fraudulent job postings (placeholder)

## Setup

### 1. Install Dependencies

```bash
cd ml_services
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Prepare Models (Optional)

Place trained models in:
```
ml_services/models/
├── salary_predictor/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── encoders/
│       ├── experience_level.pkl
│       └── ...
```

If models are not present, the services will use rule-based implementations for development.

### 3. Run the Service

```bash
uvicorn main:app --reload --port 8001
```

The service will be available at:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API Endpoints

See [ML_ENDPOINTS.md](./ML_ENDPOINTS.md) for complete API documentation.

### Quick Examples

#### Predict Salary
```bash
curl -X POST http://localhost:8001/api/salary/predict-salary \
  -H "Content-Type: application/json" \
  -d '{
    "work_year": 2024,
    "experience_level": "MID_LEVEL",
    "employment_type": "FULL_TIME",
    "job_title": "Software Engineer",
    "employee_residence": "US",
    "remote_ratio": 50,
    "company_location": "US",
    "company_size": "LARGE"
  }'
```

#### Recommend Jobs
```bash
curl -X POST http://localhost:8001/api/jobs/recommend-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "experience_level": "MID_LEVEL",
    "skills": ["Python", "FastAPI", "PostgreSQL"]
  }'
```

#### Recommend Countries
```bash
curl -X POST http://localhost:8001/api/country/recommend-countries \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "experience_level": "MID_LEVEL"
  }'
```

## Model Training

To train models, use the scripts in `training/`:

```bash
python training/train_salary_predictor.py
python training/train_job_recommender.py
python training/train_country_recommender.py
```

## Integration

The main backend can call these services via HTTP:

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8001/api/salary/predict-salary",
        json={...}
    )
    result = response.json()
```

## Development

- Models are loaded once at startup and cached
- Services use rule-based implementations if models are not found
- All endpoints include input validation and error handling
- Responses include confidence scores and explanations

## Production Considerations

1. **Model Versioning**: Track model versions in responses
2. **Caching**: Cache predictions for frequently requested data
3. **Monitoring**: Track prediction latency and accuracy
4. **Scaling**: Run multiple instances behind a load balancer
5. **Model Updates**: Implement model hot-reloading or rolling updates

