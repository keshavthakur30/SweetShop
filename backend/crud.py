from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import models
import schemas
from auth import get_password_hash

# User CRUD operations
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Sweet CRUD operations
def get_sweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sweet).offset(skip).limit(limit).all()

def get_sweet(db: Session, sweet_id: int):
    return db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

def create_sweet(db: Session, sweet: schemas.SweetCreate):
    db_sweet = models.Sweet(**sweet.dict())
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def update_sweet(db: Session, sweet_id: int, sweet_update: schemas.SweetUpdate):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet:
        update_data = sweet_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sweet, field, value)
        db.commit()
        db.refresh(db_sweet)
    return db_sweet

def delete_sweet(db: Session, sweet_id: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet:
        db.delete(db_sweet)
        db.commit()
        return True
    return False

def search_sweets(
    db: Session, 
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = db.query(models.Sweet)
    
    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Sweet.price <= max_price)
    
    return query.all()

def purchase_sweet(db: Session, sweet_id: int, quantity: int = 1):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet and db_sweet.quantity >= quantity:
        db_sweet.quantity -= quantity
        db.commit()
        db.refresh(db_sweet)
        return db_sweet
    return None

def restock_sweet(db: Session, sweet_id: int, quantity: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet:
        db_sweet.quantity += quantity
        db.commit()
        db.refresh(db_sweet)
        return db_sweet
    return None