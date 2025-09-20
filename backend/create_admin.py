from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
import schemas
from auth import get_password_hash

def create_admin_user():
    """Create a dedicated admin user"""
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin_user = crud.get_user_by_username(db, username="admin")
        if admin_user:
            print("Admin user already exists!")
            print("Admin Credentials:")
            print("Username: admin")
            print("Password: admin123")
            return
        
        # Create admin user
        hashed_password = get_password_hash("admin123")
        admin = models.User(
            username="admin",
            email="admin@sweetshop.com",
            hashed_password=hashed_password,
            is_admin=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("✅ Admin user created successfully!")
        print("Admin Credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("\nYou can now login with these credentials and access the admin panel.")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_regular_user():
    """Create a sample regular user for testing"""
    db = SessionLocal()
    try:
        # Check if user already exists
        user = crud.get_user_by_username(db, username="user")
        if user:
            print("Regular user already exists!")
            print("User Credentials:")
            print("Username: user")
            print("Password: user123")
            return
        
        # Create regular user
        hashed_password = get_password_hash("user123")
        regular_user = models.User(
            username="user",
            email="user@sweetshop.com",
            hashed_password=hashed_password,
            is_admin=False
        )
        
        db.add(regular_user)
        db.commit()
        db.refresh(regular_user)
        
        print("✅ Regular user created successfully!")
        print("User Credentials:")
        print("Username: user")
        print("Password: user123")
        
    except Exception as e:
        print(f"❌ Error creating regular user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating admin and user accounts...")
    create_admin_user()
    print("\n" + "="*50 + "\n")
    create_regular_user()
    print("\n" + "="*50)
    print("Setup complete! You can now login with either account.")