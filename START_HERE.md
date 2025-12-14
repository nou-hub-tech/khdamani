# 🚀 START HERE - Get Running in 5 Minutes

## Yes, the app is ready to run! ✅

Follow these steps to get everything running:

## Option 1: Docker (Easiest) 🐳

```bash
# 1. Start everything
docker-compose -f docker/docker-compose.yml up -d

# 2. Initialize database (wait 10 seconds for postgres to start)
sleep 10
docker exec -i $(docker-compose -f docker/docker-compose.yml ps -q postgres) psql -U khadamni -d khadamni < backend/database/schema.sql

# 3. Done! Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000/docs
# - ML Services: http://localhost:8001/docs
```

## Option 2: Manual Setup (3 Terminals)

### Terminal 1: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: Set DATABASE_URL=postgresql://user:pass@localhost:5432/khadamni
uvicorn app.main:app --reload
```

### Terminal 2: ML Services
```bash
cd ml_services
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Terminal 3: Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
echo "VITE_ML_SERVICE_URL=http://localhost:8001" >> .env
npm run dev
```

### Database Setup (One-time)
```bash
# Create database
createdb khadamni

# Run schema
psql -d khadamni -f backend/database/schema.sql
```

## ✅ Verification

1. **Backend**: http://localhost:8000/docs (should show Swagger UI)
2. **ML Services**: http://localhost:8001/docs (should show Swagger UI)
3. **Frontend**: http://localhost:5173 (should show landing page)

## 🧪 Quick Test

```bash
# Test registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","role":"JOB_SEEKER"}'
```

## 📚 Need More Help?

- **Detailed Setup**: See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Quick Reference**: See [QUICK_START.md](./QUICK_START.md)
- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🎉 You're Ready!

The application is **fully set up and ready to test**. All components are in place:

- ✅ Backend API with authentication
- ✅ ML Services with predictions
- ✅ Frontend UI with all pages
- ✅ Database schema
- ✅ API services and hooks
- ✅ Error handling
- ✅ Loading states

**Start the services and begin testing!**

