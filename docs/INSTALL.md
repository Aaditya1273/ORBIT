# 📦 ORBIT Installation Guide

## Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- Git installed

## Quick Install

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database ORM)
- Pydantic (data validation)
- Python-Jose (JWT tokens)
- Bcrypt (password hashing)
- Redis client
- Google Generative AI
- OpenAI client
- And more...

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
```

This will install:
- React
- TypeScript
- React Router
- Zustand (state management)
- Axios (HTTP client)
- Tailwind CSS
- And more...

### 3. Verify Installation
```bash
# Go back to root
cd ..

# Verify setup
python verify_setup.py
```

## Detailed Installation

### Backend Setup

1. **Create Virtual Environment (Recommended)**
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify Installation**
```bash
python -c "from src.main import app; print('✅ Backend ready')"
```

### Frontend Setup

1. **Navigate to Frontend**
```bash
cd frontend
```

2. **Install Dependencies**
```bash
npm install
```

3. **Verify Installation**
```bash
npm run build
```

## Environment Setup

### 1. Copy Environment File
```bash
# Already done - .env.local exists
```

### 2. Verify Configuration
```bash
python verify_setup.py
```

Expected output:
```
✅ Google Gemini API         Configured
✅ OpenRouter API            Configured
✅ Upstash Redis             Configured
✅ Opik Monitoring           Configured
✅ Sentry Error Tracking     Configured
✅ Database                  Configured
✅ App Secret                Configured
✅ JWT Secret                Configured
✅ Email (SMTP)              Configured
```

## Initialize Platform

```bash
python initialize_orbit.py
```

This will:
- Create database tables
- Set up initial data
- Verify all services

## Start Development Servers

### Terminal 1: Backend
```bash
python -m uvicorn src.main:app --reload
```

Backend runs at: http://localhost:8000

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

Frontend runs at: http://localhost:3000

## Verify Everything Works

### 1. Check Backend
```bash
# Health check
curl http://localhost:8000/health

# API docs
# Open: http://localhost:8000/docs
```

### 2. Check Frontend
1. Open http://localhost:3000
2. Should see login page
3. Click "Sign Up"
4. Register new account

### 3. Test Authentication
1. Register with email/password
2. Login
3. Should redirect to dashboard
4. Check browser console for JWT token

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `Database error`
```bash
# Solution: Initialize database
python initialize_orbit.py
```

**Problem**: `Redis connection error`
```bash
# Solution: Check REDIS_URL in .env.local
# Upstash Redis should work out of the box
```

### Frontend Issues

**Problem**: `npm: command not found`
```bash
# Solution: Install Node.js
# Download from: https://nodejs.org/
```

**Problem**: `Module not found`
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Problem**: `Port 3000 already in use`
```bash
# Solution: Kill process or use different port
# Windows: netstat -ano | findstr :3000
# Mac/Linux: lsof -ti:3000 | xargs kill
```

### Email Issues

**Problem**: `SMTP connection timeout`
```bash
# Solution: See docs/EMAIL_TROUBLESHOOTING.md
# Platform works without email!
```

## Dependencies List

### Backend (requirements.txt)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
python-multipart==0.0.6
python-dotenv==1.0.0
redis==5.0.1
google-generativeai==0.3.2
openai==1.10.0
anthropic==0.8.1
opik==0.1.0
sentry-sdk[fastapi]==1.40.0
structlog==24.1.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.5",
    "typescript": "^5.3.3"
  }
}
```

## Next Steps

After installation:

1. ✅ Verify setup: `python verify_setup.py`
2. ✅ Initialize: `python initialize_orbit.py`
3. ✅ Start backend: `python -m uvicorn src.main:app --reload`
4. ✅ Start frontend: `cd frontend && npm start`
5. ✅ Test: Open http://localhost:3000

## Quick Commands

```bash
# Install everything
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Verify
python verify_setup.py

# Initialize
python initialize_orbit.py

# Start (2 terminals)
# Terminal 1:
python -m uvicorn src.main:app --reload

# Terminal 2:
cd frontend && npm start
```

## Production Deployment

See: `docs/README_DEPLOYMENT.md`

## Support

- **Documentation**: `docs/` folder
- **API Docs**: http://localhost:8000/docs
- **Issues**: Check `CURRENT_STATUS.md`
