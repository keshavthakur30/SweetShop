from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str  # Changed from EmailStr to str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Sweet Schemas
class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None
    image_url: Optional[str] = None

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class Sweet(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Purchase Schema
class PurchaseRequest(BaseModel):
    quantity: int = 1

# Restock Schema
class RestockRequest(BaseModel):
    quantity: int