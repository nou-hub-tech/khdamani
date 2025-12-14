# Quick Test Commands

## All-in-One Test Script

Copy and paste these commands in order:

### Terminal 1: Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

### Terminal 2: ML Services
```bash
cd ml_services
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Terminal 3: Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Test API Endpoints

### 1. Health Checks
```bash
# Backend
curl http://localhost:8000/health

# ML Services
curl http://localhost:8001/health
```

### 2. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"password\":\"test123\",\"role\":\"JOB_SEEKER\"}"
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"password\":\"test123\"}"
```

### 4. Get Jobs (after login, use token)
```bash
curl http://localhost:8000/api/v1/jobs ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. ML Salary Prediction
```bash
curl -X POST http://localhost:8001/api/salary/predict-salary ^
  -H "Content-Type: application/json" ^
  -d "{\"work_year\":2024,\"experience_level\":\"MID_LEVEL\",\"employment_type\":\"FULL_TIME\",\"job_title\":\"Software Engineer\",\"employee_residence\":\"US\",\"remote_ratio\":50,\"company_location\":\"US\",\"company_size\":\"LARGE\"}"
```

---

## Browser Testing

1. **Frontend:** http://localhost:5173
2. **Backend API Docs:** http://localhost:8000/docs
3. **ML Services API Docs:** http://localhost:8001/docs

---

## Expected Results

✅ All three services running
✅ Database file created: `backend/khadamni.db`
✅ Can register and login users
✅ Can create and view jobs
✅ ML predictions working
✅ Frontend UI accessible

