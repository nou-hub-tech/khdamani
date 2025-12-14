# Quick Start Guide

## Fastest Way to Run (Docker)

```bash
# 1. Start all services
docker-compose -f docker/docker-compose.yml up -d

# 2. Initialize database
docker exec -i $(docker-compose -f docker/docker-compose.yml ps -q postgres) psql -U khadamni -d khadamni < backend/database/schema.sql

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# ML Services: http://localhost:8001/docs
```

## Manual Setup (3 Steps)

### Step 1: Database
```bash
# Create database
createdb khadamni

# Run schema
psql -d khadamni -f backend/database/schema.sql
```

### Step 2: Backend & ML Services
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL
uvicorn app.main:app --reload

# ML Services (new terminal)
cd ml_services
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Step 3: Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
echo "VITE_ML_SERVICE_URL=http://localhost:8001" >> .env
npm run dev
```

## Verify It Works

1. **Backend**: http://localhost:8000/docs
2. **ML Services**: http://localhost:8001/docs
3. **Frontend**: http://localhost:5173

## Test Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","role":"JOB_SEEKER"}'
```

**That's it! The app is ready to use.**

