# Khadamni - AI-Powered Job Search Platform

A full-stack job search platform with ML-powered features including salary prediction, job recommendations, fraud detection, and country recommendations.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Initialize database
docker exec -i $(docker-compose -f docker/docker-compose.yml ps -q postgres) psql -U khadamni -d khadamni < backend/database/schema.sql

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# ML Services: http://localhost:8001/docs
```

### Option 2: Manual Setup

See [QUICK_START.md](./QUICK_START.md) for detailed instructions.

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ (or Docker)
- Docker & Docker Compose (optional)

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: FastAPI (Python)
- **ML Services**: FastAPI microservice
- **Database**: PostgreSQL

## 📁 Project Structure

```
Khadamni/
├── frontend/          # React frontend
├── backend/           # FastAPI backend
├── ml_services/       # ML microservices
├── docker/            # Docker configurations
└── docs/              # Documentation
```

## 🎯 Features

- ✅ User authentication (Job Seekers & Recruiters)
- ✅ Job postings CRUD
- ✅ Job applications
- ✅ AI-powered salary prediction
- ✅ Personalized job recommendations
- ✅ Country recommendations
- ✅ Fraud detection

## 📚 Documentation

- [Architecture Documentation](./ARCHITECTURE.md)
- [Setup Guide](./SETUP_GUIDE.md)
- [Quick Start](./QUICK_START.md)
- [API Endpoints](./backend/API_ENDPOINTS.md)
- [Database Schema](./backend/database/README.md)

## 🔧 Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### ML Services
```bash
cd ml_services
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Test API Endpoints

Visit Swagger UI:
- Backend: http://localhost:8000/docs
- ML Services: http://localhost:8001/docs

### Test Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","role":"JOB_SEEKER"}'
```

## 📝 Environment Variables

### Backend
See `backend/.env.example`

### Frontend
See `frontend/.env.example`

## 🐳 Docker

All services can be run with Docker Compose:
```bash
docker-compose -f docker/docker-compose.yml up
```

## 📖 API Documentation

- Backend API: http://localhost:8000/docs
- ML Services API: http://localhost:8001/docs

## 🎨 UI Preview

Modern, clean interface with:
- Glassmorphism design
- Smooth animations
- Responsive layout
- Dark mode support

## 🔒 Security

- JWT authentication
- Password hashing (bcrypt)
- Role-based access control
- Input validation

## 📊 Database

PostgreSQL with:
- UUID primary keys
- Proper relationships
- ML result tables
- Optimized indexes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT

## 🆘 Support

For setup issues, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)

---

**Status**: ✅ Ready to run and test!
