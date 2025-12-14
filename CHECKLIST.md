# Setup Checklist

## ✅ Pre-Setup Verification

- [ ] Python 3.10+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] PostgreSQL 14+ installed OR Docker installed
- [ ] Git repository cloned

## ✅ Database Setup

- [ ] PostgreSQL is running
- [ ] Database `khadamni` created
- [ ] Schema applied (`backend/database/schema.sql`)
- [ ] Can connect to database

## ✅ Backend Setup

- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] DATABASE_URL configured in `.env`
- [ ] SECRET_KEY set in `.env`
- [ ] Server starts without errors (`python run.py` or `uvicorn app.main:app --reload`)
- [ ] Can access http://localhost:8000/docs

## ✅ ML Services Setup

- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors (`python run.py` or `uvicorn main:app --reload --port 8001`)
- [ ] Can access http://localhost:8001/docs

## ✅ Frontend Setup

- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file created with API URLs
- [ ] Development server starts (`npm run dev`)
- [ ] Can access http://localhost:5173 (or 3000)
- [ ] No console errors in browser

## ✅ Integration Testing

- [ ] Can register a new user
- [ ] Can login with credentials
- [ ] Can view jobs list
- [ ] Can create job (as recruiter)
- [ ] Can apply to job (as job seeker)
- [ ] ML salary prediction works
- [ ] ML job recommendations work
- [ ] ML country recommendations work

## ✅ Docker Setup (Optional)

- [ ] Docker and Docker Compose installed
- [ ] `docker-compose -f docker/docker-compose.yml up` works
- [ ] All services accessible
- [ ] Database initialized in container

## 🎯 Ready to Test!

If all items are checked, the application is ready to run and test!

