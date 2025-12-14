# 🚀 RUN THE APP NOW - SQLite Setup

## ✅ Everything is ready! Follow these exact steps:

---

## STEP 1: Backend (Open Terminal 1)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

**Wait for:** `Application startup complete`

**✅ Backend running at:** http://localhost:8000

---

## STEP 2: ML Services (Open Terminal 2)

```bash
cd ml_services
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

**Wait for:** `Application startup complete`

**✅ ML Services running at:** http://localhost:8001

---

## STEP 3: Frontend (Open Terminal 3)

```bash
cd frontend
npm install
npm run dev
```

**Wait for:** `Local: http://localhost:5173/`

**✅ Frontend running at:** http://localhost:5173

---

## STEP 4: Test It!

### Quick Test in Browser:
1. Open: http://localhost:5173
2. Click "Get Started"
3. Register a user
4. Explore the app!

### Quick Test with curl:
```bash
# Test backend
curl http://localhost:8000/health

# Test ML services
curl http://localhost:8001/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test123\",\"role\":\"JOB_SEEKER\"}"
```

---

## ✅ That's It!

All three services are running. The database file (`khadamni.db`) is automatically created in the `backend/` folder.

**No PostgreSQL needed! No Docker needed!**

---

## 📚 More Info

- **API Docs:** http://localhost:8000/docs
- **ML API Docs:** http://localhost:8001/docs
- **Database file:** `backend/khadamni.db`

**You're ready to test! 🎉**

