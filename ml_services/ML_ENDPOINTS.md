# ML Services API Endpoints

## Base URL
```
http://localhost:8001/api
```

## Endpoints

### 1. Predict Salary

**POST** `/salary/predict-salary`

Predicts salary in USD based on job and employee features.

#### Request Body
```json
{
  "work_year": 2024,
  "experience_level": "MID_LEVEL",
  "employment_type": "FULL_TIME",
  "job_title": "Software Engineer",
  "employee_residence": "US",
  "remote_ratio": 50,
  "company_location": "US",
  "company_size": "LARGE"
}
```

#### Request Fields
- `work_year` (int, required): Year of work (2020-2030)
- `experience_level` (string, required): One of `ENTRY_LEVEL`, `JUNIOR`, `MID_LEVEL`, `SENIOR`, `EXECUTIVE`
- `employment_type` (string, required): One of `FULL_TIME`, `PART_TIME`, `CONTRACT`, `TEMPORARY`, `INTERNSHIP`, `FREELANCE`
- `job_title` (string, required): Job title (1-200 characters)
- `employee_residence` (string, required): Country code (2 letters, e.g., "US", "GB")
- `remote_ratio` (int, required): Remote work ratio 0-100
- `company_location` (string, required): Country code (2 letters)
- `company_size` (string, required): One of `STARTUP`, `SMALL`, `MEDIUM`, `LARGE`, `ENTERPRISE`

#### Response (200)
```json
{
  "predicted_salary_usd": 125000.0,
  "salary_range_min": 100000.0,
  "salary_range_max": 150000.0,
  "confidence_score": 0.85
}
```

#### Example cURL
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

---

### 2. Recommend Jobs

**POST** `/jobs/recommend-jobs`

Get personalized job recommendations based on job seeker profile. Returns top 5 matching jobs.

#### Request Body
```json
{
  "experience_level": "MID_LEVEL",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "preferred_location": "US",
  "preferred_employment_type": "FULL_TIME",
  "desired_salary_min": 80000.0,
  "desired_salary_max": 120000.0
}
```

#### Request Fields
- `experience_level` (string, required): One of `ENTRY_LEVEL`, `JUNIOR`, `MID_LEVEL`, `SENIOR`, `EXECUTIVE`
- `skills` (array, required): List of skills (minimum 1 skill)
- `preferred_location` (string, optional): Preferred location (country code or city)
- `preferred_employment_type` (string, optional): One of `FULL_TIME`, `PART_TIME`, `CONTRACT`, `TEMPORARY`, `INTERNSHIP`, `FREELANCE`
- `desired_salary_min` (float, optional): Minimum desired salary in USD (>= 0)
- `desired_salary_max` (float, optional): Maximum desired salary in USD (>= 0)

#### Response (200)
```json
{
  "recommended_jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "New York, NY",
      "salary_min": 100000.0,
      "salary_max": 150000.0,
      "match_score": 0.92,
      "match_reasons": [
        "Skills match: Python, FastAPI, PostgreSQL",
        "Experience level matches",
        "Location preference matches"
      ]
    }
  ],
  "total_matches": 15
}
```

#### Example cURL
```bash
curl -X POST http://localhost:8001/api/jobs/recommend-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "experience_level": "MID_LEVEL",
    "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "preferred_location": "US",
    "preferred_employment_type": "FULL_TIME",
    "desired_salary_min": 80000.0,
    "desired_salary_max": 120000.0
  }'
```

---

### 3. Recommend Countries

**POST** `/country/recommend-countries`

Get country recommendations for job hunting based on job title and experience level. Returns top 5 countries.

#### Request Body
```json
{
  "job_title": "Software Engineer",
  "experience_level": "MID_LEVEL"
}
```

#### Request Fields
- `job_title` (string, required): Job title (1-200 characters)
- `experience_level` (string, required): One of `ENTRY_LEVEL`, `JUNIOR`, `MID_LEVEL`, `SENIOR`, `EXECUTIVE`

#### Response (200)
```json
{
  "recommended_countries": [
    {
      "country": "United States",
      "country_code": "US",
      "score": 0.95,
      "average_salary_usd": 125000.0,
      "job_opportunities": 15000,
      "growth_rate": 12.5,
      "reasons": [
        "High demand for Software Engineers",
        "Competitive salaries",
        "Strong tech industry"
      ]
    },
    {
      "country": "United Kingdom",
      "country_code": "GB",
      "score": 0.88,
      "average_salary_usd": 95000.0,
      "job_opportunities": 8500,
      "growth_rate": 10.2,
      "reasons": [
        "Growing tech sector",
        "Good work-life balance"
      ]
    }
  ]
}
```

#### Response Fields
- `country` (string): Country name
- `country_code` (string): ISO 3166-1 alpha-2 country code
- `score` (float): Recommendation score (0-1)
- `average_salary_usd` (float): Average salary in USD
- `job_opportunities` (int): Number of job opportunities
- `growth_rate` (float): Job market growth rate (%)
- `reasons` (array): Reasons for recommendation

#### Example cURL
```bash
curl -X POST http://localhost:8001/api/country/recommend-countries \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "experience_level": "MID_LEVEL"
  }'
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Prediction error: error message"
}
```

---

## Model Loading

The ML services use `joblib` to load trained models. Models should be placed in:
```
ml_services/models/
├── salary_predictor/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── encoders/
└── ...
```

If models are not found, the services will use dummy/rule-based implementations for development.

---

## Testing

### Test Salary Prediction
```bash
curl -X POST http://localhost:8001/api/salary/predict-salary \
  -H "Content-Type: application/json" \
  -d '{
    "work_year": 2024,
    "experience_level": "SENIOR",
    "employment_type": "FULL_TIME",
    "job_title": "Data Scientist",
    "employee_residence": "US",
    "remote_ratio": 100,
    "company_location": "US",
    "company_size": "LARGE"
  }'
```

### Test Job Recommendations
```bash
curl -X POST http://localhost:8001/api/jobs/recommend-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "experience_level": "SENIOR",
    "skills": ["Python", "Machine Learning", "TensorFlow"]
  }'
```

### Test Country Recommendations
```bash
curl -X POST http://localhost:8001/api/country/recommend-countries \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Data Scientist",
    "experience_level": "SENIOR"
  }'
```

---

## Integration with Main Backend

The main backend can call these ML services via HTTP:

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8001/api/salary/predict-salary",
        json={
            "work_year": 2024,
            "experience_level": "MID_LEVEL",
            # ... other fields
        }
    )
    prediction = response.json()
```

