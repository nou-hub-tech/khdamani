# Complete Setup Guide

## Prerequisites

- **Python 3.10+** (for backend and ML services)
- **Node.js 18+** (for frontend)
- **PostgreSQL 14+** (or use Docker)
- **Docker & Docker Compose** (optional, for containerized setup)

## Quick Start (Recommended: Docker)

### 1. Using Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up

# Or run in background
docker-compose -f docker/docker-compose.yml up -d

# Stop services
docker-compose -f docker/docker-compose.yml down
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- ML Services (port 8001)
- Frontend (port 3000)

### 2. Initialize Database

```bash
# Connect to PostgreSQL container
docker exec -it khadamni-postgres-1 psql -U khadamni -d khadamni

# Or run SQL file directly
docker exec -i khadamni-postgres-1 psql -U khadamni -d khadamni < backend/database/schema.sql
```

---

## Manual Setup (Without Docker)

### 1. Database Setup

#### Install PostgreSQL
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql@14`
- **Linux**: `sudo apt-get install postgresql-14`

#### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE khadamni;
CREATE USER khadamni_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE khadamni TO khadamni_user;

# Exit psql
\q
```

#### Run Schema

```bash
psql -U khadamni_user -d khadamni -f backend/database/schema.sql
```

### 2. Backend Setup

```bash
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

# Create .env file
cp .env.example .env

# Edit .env with your database URL:
# DATABASE_URL=postgresql://khadamni_user:your_password@localhost:5432/khadamni
# SECRET_KEY=your-secret-key-here

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

### 3. ML Services Setup

```bash
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

# Run the server
uvicorn main:app --reload --port 8001
```

ML Services will be available at: http://localhost:8001
API Docs: http://localhost:8001/docs

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
echo "VITE_ML_SERVICE_URL=http://localhost:8001" >> .env

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:5173 (or 3000)

---

## Environment Variables

### Backend (.env)

```env
# Application
APP_NAME=Khadamni
DEBUG=True

# Database
DATABASE_URL=postgresql://khadamni_user:password@localhost:5432/khadamni

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# ML Services
ML_SERVICE_URL=http://localhost:8001
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_ML_SERVICE_URL=http://localhost:8001
```

---

## Verification Steps

### 1. Check Backend

```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### 2. Check ML Services

```bash
# Health check
curl http://localhost:8001/health

# Should return: {"status":"healthy"}
```

### 3. Check Frontend

Open http://localhost:5173 (or 3000) in your browser.

### 4. Test API Endpoints

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "role": "JOB_SEEKER"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

---

## Common Issues & Solutions

### Issue: Database Connection Error

**Solution:**
- Check PostgreSQL is running: `pg_isready` or `docker ps`
- Verify DATABASE_URL in .env file
- Check database exists: `psql -U postgres -l`

### Issue: Port Already in Use

**Solution:**
- Change port in docker-compose.yml or command
- Kill process using port:
  - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <pid> /F`
  - macOS/Linux: `lsof -ti:8000 | xargs kill`

### Issue: Module Not Found (Python)

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### Issue: Module Not Found (Node)

**Solution:**
- Delete node_modules and package-lock.json
- Reinstall: `npm install`
- Check Node version: `node --version` (should be 18+)

### Issue: CORS Errors

**Solution:**
- Add frontend URL to CORS_ORIGINS in backend .env
- Restart backend server

### Issue: ML Service Not Responding

**Solution:**
- Check ML service is running on port 8001
- Verify ML_SERVICE_URL in backend .env
- Check ML service logs

---

## Development Workflow

### Running All Services Manually

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 2 - ML Services:**
```bash
cd ml_services
source venv/bin/activate
uvicorn main:app --reload --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Database Migrations (Future)

When using Alembic for migrations:

```bash
cd backend

# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

---

## Testing the Application

### 1. Test User Registration

1. Open frontend: http://localhost:5173
2. Click "Get Started" or navigate to /register
3. Fill in registration form
4. Select role (Job Seeker or Recruiter)
5. Submit form

### 2. Test Login

1. Navigate to /login
2. Enter credentials
3. Should redirect to dashboard

### 3. Test Job Creation (Recruiter)

1. Login as recruiter
2. Navigate to job creation page
3. Fill in job details
4. Submit

### 4. Test ML Features

1. Navigate to /salary-prediction
2. Fill in form
3. Submit and see prediction

### 5. Test API Directly

Visit API documentation:
- Backend: http://localhost:8000/docs
- ML Services: http://localhost:8001/docs

---

## Production Deployment

### Important Notes

1. **Change SECRET_KEY** in production
2. **Set DEBUG=False** in production
3. **Configure CORS_ORIGINS** properly
4. **Use environment variables** for all secrets
5. **Set up SSL/TLS** for HTTPS
6. **Configure database backups**
7. **Set up monitoring and logging**

---

## Next Steps

1. ✅ All services are running
2. ✅ Database is initialized
3. ✅ Test user registration and login
4. ✅ Test API endpoints via Swagger UI
5. ✅ Test frontend pages
6. ✅ Test ML features

## Support

If you encounter issues:
1. Check logs in terminal/console
2. Verify all services are running
3. Check environment variables
4. Review error messages in browser console (F12)

---

## Summary

The application is **ready to run**! Follow the setup steps above and you should have:

- ✅ Backend API running on port 8000
- ✅ ML Services running on port 8001
- ✅ Frontend running on port 5173/3000
- ✅ PostgreSQL database initialized
- ✅ All endpoints accessible
- ✅ UI components working

**You can now test the full application!**

