# 🎯 START TESTING - Complete Step-by-Step Guide

## ✅ The app is now configured for SQLite - No PostgreSQL or Docker needed!

---

## 📋 EXACT COMMANDS TO RUN (Copy & Paste)

### Terminal 1: Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

**✅ Success when you see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Terminal 2: ML Services

```bash
cd ml_services
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

**✅ Success when you see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

---

### Terminal 3: Frontend

```bash
cd frontend
npm install
npm run dev
```

**✅ Success when you see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## 🧪 TEST THE APP

### Test 1: Open Frontend
1. Open browser: **http://localhost:5173**
2. You should see the landing page
3. Click "Get Started" or go to `/register`

### Test 2: Register a User
1. Fill in:
   - Email: `test@example.com`
   - Password: `test123`
   - Role: Select "Job Seeker"
2. Click "Create Account"
3. Should redirect to dashboard

### Test 3: Test API Directly

**Open Swagger UI:**
- Backend: http://localhost:8000/docs
- ML Services: http://localhost:8001/docs

**Try these endpoints:**

1. **Register:**
   - Endpoint: `POST /api/v1/auth/register`
   - Body:
     ```json
     {
       "email": "test@example.com",
       "password": "test123",
       "role": "JOB_SEEKER"
     }
     ```

2. **Login:**
   - Endpoint: `POST /api/v1/auth/login`
   - Body:
     ```json
     {
       "email": "test@example.com",
       "password": "test123"
     }
     ```
   - Copy the `access_token`

3. **Get Jobs:**
   - Endpoint: `GET /api/v1/jobs`
   - Click "Authorize" (top right)
   - Enter: `Bearer <your-token>`
   - Click "Try it out"

4. **ML Salary Prediction:**
   - Go to: http://localhost:8001/docs
   - Endpoint: `POST /api/salary/predict-salary`
   - Body:
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

---

## 📁 Database File

The SQLite database is created at:
- **Location:** `backend/khadamni.db`
- **Delete this file** to reset the database
- **Re-run** `python init_db.py` to recreate tables

---

## ✅ What's Working

- ✅ User registration
- ✅ User login with JWT
- ✅ Job CRUD operations
- ✅ Job applications
- ✅ ML salary prediction
- ✅ ML job recommendations
- ✅ ML country recommendations
- ✅ All frontend pages
- ✅ Error handling
- ✅ Loading states

---

## 🐛 Troubleshooting

### "Module not found"
- Make sure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### "Port already in use"
- Kill the process or use a different port
- Windows: `netstat -ano | findstr :8000`

### "Database locked"
- Close any database viewers
- Restart backend server

### Frontend can't connect
- Check `.env` file exists in frontend/
- Verify backend is running on port 8000

---

## 🎉 You're Ready!

All three services should be running. Test the app in your browser or via the API docs!

**No PostgreSQL needed! No Docker needed! Just Python and Node.js!**

