# Quick Test Guide - SQLite Setup

## ✅ Complete Step-by-Step Instructions

### Prerequisites Check
- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ No PostgreSQL or Docker needed!

---

## Step 1: Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (SQLite is already the default)
# No need to change anything - SQLite is configured!

# Initialize database (creates khadamni.db file)
python init_db.py

# Start backend server
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**✅ Backend is running at:** http://localhost:8000
**✅ API Docs at:** http://localhost:8000/docs

---

## Step 2: ML Services Setup (Terminal 2)

```bash
# Navigate to ML services
cd ml_services

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start ML services server
uvicorn main:app --reload --port 8001
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

**✅ ML Services running at:** http://localhost:8001
**✅ API Docs at:** http://localhost:8001/docs

---

## Step 3: Frontend Setup (Terminal 3)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
echo VITE_API_URL=http://localhost:8000 > .env
echo VITE_ML_SERVICE_URL=http://localhost:8001 >> .env

# Start frontend development server
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ Frontend running at:** http://localhost:5173

---

## Step 4: Verify Everything Works

### Test 1: Backend Health Check
```bash
curl http://localhost:8000/health
```
**Expected:** `{"status":"healthy"}`

### Test 2: ML Services Health Check
```bash
curl http://localhost:8001/health
```
**Expected:** `{"status":"healthy"}`

### Test 3: Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\",\"role\":\"JOB_SEEKER\"}"
```

**Expected response:**
```json
{
  "message": "User registered successfully",
  "user_id": "uuid-here"
}
```

### Test 4: Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\"}"
```

**Expected response:**
```json
{
  "access_token": "jwt-token-here",
  "refresh_token": "refresh-token-here",
  "token_type": "bearer"
}
```

### Test 5: Get Jobs
```bash
curl http://localhost:8000/api/v1/jobs
```

**Expected:** Empty array `[]` (no jobs yet) or list of jobs

### Test 6: ML Salary Prediction
```bash
curl -X POST http://localhost:8001/api/salary/predict-salary \
  -H "Content-Type: application/json" \
  -d "{\"work_year\":2024,\"experience_level\":\"MID_LEVEL\",\"employment_type\":\"FULL_TIME\",\"job_title\":\"Software Engineer\",\"employee_residence\":\"US\",\"remote_ratio\":50,\"company_location\":\"US\",\"company_size\":\"LARGE\"}"
```

**Expected:** Salary prediction response

---

## Step 5: Test in Browser

1. **Open Frontend:** http://localhost:5173
2. **Click "Get Started"** or navigate to `/register`
3. **Register a new user:**
   - Email: `test@example.com`
   - Password: `test123`
   - Role: Select "Job Seeker" or "Recruiter"
4. **After registration, you'll be logged in**
5. **Test features:**
   - View dashboard
   - Navigate to salary prediction
   - Try job recommendations
   - Create a job (if recruiter)

---

## Step 6: Test API via Swagger UI

### Backend API
1. Open: http://localhost:8000/docs
2. Try the `/auth/register` endpoint
3. Try the `/auth/login` endpoint
4. Copy the access_token
5. Click "Authorize" button (top right)
6. Enter: `Bearer <your-token>`
7. Try protected endpoints like `/jobs`

### ML Services API
1. Open: http://localhost:8001/docs
2. Try `/salary/predict-salary` endpoint
3. Try `/jobs/recommend-jobs` endpoint
4. Try `/country/recommend-countries` endpoint

---

## Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed

### Issue: "Port already in use"
**Solution:** 
- Kill the process using the port
- Or change the port in the command (e.g., `--port 8002`)

### Issue: "Database locked" (SQLite)
**Solution:** 
- Close any database viewers
- Restart the backend server

### Issue: Frontend can't connect to backend
**Solution:**
- Check `.env` file has correct URLs
- Check backend is running on port 8000
- Check CORS settings in backend

### Issue: "No such table" error
**Solution:**
- Run `python init_db.py` again in the backend directory

---

## Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
python init_db.py
uvicorn app.main:app --reload

# ML Services
cd ml_services
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
uvicorn main:app --reload --port 8001

# Frontend
cd frontend
npm install
npm run dev
```

---

## Database File Location

The SQLite database file will be created at:
- **Location:** `backend/khadamni.db`
- **You can delete this file** to reset the database
- **Then run** `python init_db.py` again to recreate tables

---

## What's Working

✅ User registration and login
✅ JWT token authentication
✅ Job CRUD operations
✅ Job applications
✅ ML salary prediction
✅ ML job recommendations
✅ ML country recommendations
✅ All frontend pages
✅ Error handling
✅ Loading states

---

## Next Steps After Testing

1. **Create test data:**
   - Register users (job seekers and recruiters)
   - Create job postings
   - Apply to jobs

2. **Test ML features:**
   - Try salary prediction with different inputs
   - Get job recommendations
   - Get country recommendations

3. **Test UI:**
   - Navigate through all pages
   - Test forms and interactions
   - Check responsive design

**🎉 You're all set! The app is ready to test!**

