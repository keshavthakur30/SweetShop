# Deployment Guide

## 🚀 Deploy to Production

### Option 1: Quick Deploy (Recommended)

#### Frontend - Deploy to Vercel

1. **Push code to GitHub** (follow Git setup instructions)

2. **Go to [Vercel.com](https://vercel.com)**

3. **Sign in with GitHub**

4. **Click "New Project"**

5. **Select your repository**: `sweet-shop-system`

6. **Configure settings**:
   - Framework: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

7. **Environment Variables**:
   ```
   REACT_APP_API_URL = https://your-backend-url.railway.app
   ```

8. **Click "Deploy"**

Your frontend will be live at: `https://your-app.vercel.app`

#### Backend - Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**

2. **Sign in with GitHub**

3. **Click "New Project" → "Deploy from GitHub repo"**

4. **Select your repository**

5. **Configure settings**:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

6. **Add Environment Variables**:
   ```
   PORT = 8000
   SECRET_KEY = your-super-secret-key-here
   DATABASE_URL = postgresql://user:pass@host:port/db (for production)
   ```

7. **Deploy and get URL**: `https://your-api.railway.app`

### Option 2: Manual Deployment

#### Prepare Backend for Production

1. **Update database.py for production**:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sweet_shop.db")

# Fix for SQLAlchemy 1.4+ with PostgreSQL URLs
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

2. **Update main.py CORS for production**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://your-app.vercel.app",  # Production frontend
        "https://*.vercel.app",  # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Add production requirements**:
```bash
echo "psycopg2-binary==2.9.9" >> requirements.txt
```

#### Deploy Backend to Heroku

1. **Install Heroku CLI**

2. **Login to Heroku**:
```bash
heroku login
```

3. **Create Heroku app**:
```bash
cd backend
heroku create your-sweetshop-api
```

4. **Add PostgreSQL addon**:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Set environment variables**:
```bash
heroku config:set SECRET_KEY=your-super-secret-key
```

6. **Create Procfile** in backend directory:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

7. **Deploy**:
```bash
git add .
git commit -m "feat: Prepare for production deployment"
git push heroku main
```

8. **Setup database**:
```bash
heroku run python create_admin.py
heroku run python seed_data.py
```

#### Deploy Frontend to Netlify

1. **Build the frontend**:
```bash
cd frontend
npm run build
```

2. **Go to [Netlify.com](https://netlify.com)**

3. **Drag and drop the `build` folder**

4. **Configure environment variables**:
   - `REACT_APP_API_URL` = Your backend URL

5. **Update site settings** for SPA routing:
   - Create `public/_redirects` file:
   ```
   /*    /index.html   200
   ```

## 🔧 Production Configuration

### Environment Variables

#### Backend (.env):
```bash
SECRET_KEY=your-super-secret-production-key
DATABASE_URL