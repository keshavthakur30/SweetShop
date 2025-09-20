from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional

import models
import schemas
import crud
import auth
from database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sweet Shop Management System", version="1.0.0")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:3001",  # In case port changes
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/")
def root():
    return {"message": "Welcome to Sweet Shop Management System API", "status": "running"}

# Authentication endpoints
@app.post("/api/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user (regular user only)"""
    # Check if user already exists
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create regular user (not admin)
    new_user = crud.create_user(db=db, user=user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = auth.authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information"""
    return current_user

# Sweet endpoints
@app.post("/api/sweets", response_model=schemas.Sweet)
def create_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Create a new sweet (Admin only)"""
    return crud.create_sweet(db=db, sweet=sweet)

@app.get("/api/sweets", response_model=List[schemas.Sweet])
def read_sweets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get all sweets"""
    sweets = crud.get_sweets(db, skip=skip, limit=limit)
    return sweets

@app.get("/api/sweets/search", response_model=List[schemas.Sweet])
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Search sweets by name, category, or price range"""
    return crud.search_sweets(db, name, category, min_price, max_price)

@app.get("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def read_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get a specific sweet"""
    db_sweet = crud.get_sweet(db, sweet_id=sweet_id)
    if db_sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return db_sweet

@app.put("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
    sweet_id: int,
    sweet_update: schemas.SweetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Update a sweet (Admin only)"""
    db_sweet = crud.update_sweet(db, sweet_id, sweet_update)
    if db_sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return db_sweet

@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Delete a sweet (Admin only)"""
    success = crud.delete_sweet(db, sweet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted successfully"}

# Purchase endpoint
@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.Sweet)
def purchase_sweet(
    sweet_id: int,
    purchase: schemas.PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Purchase a sweet, decreasing its quantity"""
    db_sweet = crud.purchase_sweet(db, sweet_id, purchase.quantity)
    if db_sweet is None:
        raise HTTPException(
            status_code=400, 
            detail="Sweet not found or insufficient quantity"
        )
    return db_sweet

# Restock endpoint
@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.Sweet)
def restock_sweet(
    sweet_id: int,
    restock: schemas.RestockRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Restock a sweet, increasing its quantity (Admin only)"""
    db_sweet = crud.restock_sweet(db, sweet_id, restock.quantity)
    if db_sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return db_sweet

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)