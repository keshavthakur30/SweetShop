import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }

@pytest.fixture
def test_sweet_data():
    return {
        "name": "Gulab Jamun",
        "category": "Traditional",
        "price": 150.0,
        "quantity": 20,
        "description": "Soft and spongy milk solid balls soaked in rose flavored sugar syrup"
    }

def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data

def test_login_user(client: TestClient, test_user_data):
    """Test user login"""
    # First register
    client.post("/api/auth/register", json=test_user_data)
    
    # Then login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_sweet(client: TestClient, test_user_data, test_sweet_data):
    """Test creating a sweet (admin only)"""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/sweets", json=test_sweet_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_sweet_data["name"]
    assert data["price"] == test_sweet_data["price"]

def test_get_sweets(client: TestClient, test_user_data, test_sweet_data):
    """Test getting all sweets"""
    # Register, login, and create a sweet
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/api/sweets", json=test_sweet_data, headers=headers)
    
    # Get all sweets
    response = client.get("/api/sweets", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == test_sweet_data["name"]

def test_purchase_sweet(client: TestClient, test_user_data, test_sweet_data):
    """Test purchasing a sweet"""
    # Setup
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create sweet
    sweet_response = client.post("/api/sweets", json=test_sweet_data, headers=headers)
    sweet_id = sweet_response.json()["id"]
    original_quantity = sweet_response.json()["quantity"]
    
    # Purchase sweet
    purchase_data = {"quantity": 2}
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json=purchase_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == original_quantity - 2

def test_search_sweets(client: TestClient, test_user_data, test_sweet_data):
    """Test searching sweets"""
    # Setup
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/api/sweets", json=test_sweet_data, headers=headers)
    
    # Search by name
    response = client.get("/api/sweets/search?name=Gulab", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Gulab" in data[0]["name"]