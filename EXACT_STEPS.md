# ✅ EXACT STEPS TO RUN THE APP

## 🎯 You're ready! Follow these steps in order:

---

## STEP 1: Setup Backend (Terminal 1)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

**✅ Wait for:** `Application startup complete`  
**✅ Backend URL:** http://localhost:8000  
**✅ API Docs:** http://localhost:8000/docs

---

## STEP 2: Setup ML Services (Terminal 2)

```bash
cd ml_services
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

**✅ Wait for:** `Application startup complete`  
**✅ ML Services URL:** http://localhost:8001  
**✅ API Docs:** http://localhost:8001/docs

---

## STEP 3: Setup Frontend (Terminal 3)

```bash
cd frontend
npm install
```

**⏱️ Note:** `npm install` can take 2-5 minutes. Be patient!  
**✅ If it seems stuck:** Wait a bit, or press `Ctrl+C` and try again.

After installation completes:
```bash
npm run dev
```

**✅ Wait for:** `Local: http://localhost:5173/`  
**✅ Frontend URL:** http://localhost:5173

---

## STEP 4: Test It!

### Option A: Browser Testing
1. Open: **http://localhost:5173**
2. Click "Get Started"
3. Register a user
4. Explore!

### Option B: API Testing
1. Open: **http://localhost:8000/docs**
2. Try `POST /api/v1/auth/register`
3. Try `POST /api/v1/auth/login`
4. Copy token and test protected endpoints

### Option C: Quick curl Test
```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test123\",\"role\":\"JOB_SEEKER\"}"

# Login
curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test123\"}"
```

---

## ✅ What You Have Now

- ✅ **Backend API** - Full CRUD, authentication, job applications
- ✅ **ML Services** - Salary prediction, recommendations, fraud detection
- ✅ **Frontend UI** - Modern React interface with all pages
- ✅ **SQLite Database** - No installation needed! File: `backend/khadamni.db`

---

## 🎉 You're Done!

**The app is running and ready to test!**

No PostgreSQL needed! No Docker needed! Just Python and Node.js!

---

## 📚 Quick Reference

- **Backend:** http://localhost:8000/docs
- **ML Services:** http://localhost:8001/docs  
- **Frontend:** http://localhost:5173
- **Database:** `backend/khadamni.db` (SQLite file)

**Start testing now! 🚀**

