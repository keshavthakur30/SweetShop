from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
import schemas

# Indian sweets data with simple placeholder images that will work
INDIAN_SWEETS = [
    {
        "name": "Gulab Jamun",
        "category": "Traditional",
        "price": 150.0,
        "quantity": 50,
        "description": "Soft and spongy milk solid balls soaked in rose flavored sugar syrup",
        "image_url": "https://picsum.photos/300/200?random=1"
    },
    {
        "name": "Rasgulla",
        "category": "Bengali",
        "price": 120.0,
        "quantity": 40,
        "description": "Spongy white balls made from cottage cheese and soaked in light sugar syrup",
        "image_url": "https://picsum.photos/300/200?random=2"
    },
    {
        "name": "Jalebi",
        "category": "Traditional",
        "price": 100.0,
        "quantity": 60,
        "description": "Crispy and syrupy sweet made from fermented batter in spiral shapes",
        "image_url": "https://picsum.photos/300/200?random=3"
    },
    {
        "name": "Laddu",
        "category": "Traditional",
        "price": 80.0,
        "quantity": 70,
        "description": "Round sweet balls made from flour, ghee, and sugar with nuts",
        "image_url": "https://picsum.photos/300/200?random=4"
    },
    {
        "name": "Kaju Katli",
        "category": "Premium",
        "price": 400.0,
        "quantity": 30,
        "description": "Diamond-shaped cashew fudge covered with silver leaf",
        "image_url": "https://picsum.photos/300/200?random=5"
    },
    {
        "name": "Barfi",
        "category": "Traditional",
        "price": 200.0,
        "quantity": 45,
        "description": "Milk-based sweet cut into square or diamond shapes with pistachios",
        "image_url": "https://picsum.photos/300/200?random=6"
    },
    {
        "name": "Soan Papdi",
        "category": "Traditional",
        "price": 180.0,
        "quantity": 35,
        "description": "Flaky and crispy sweet with a melt-in-mouth texture",
        "image_url": "https://picsum.photos/300/200?random=7"
    },
    {
        "name": "Sandesh",
        "category": "Bengali",
        "price": 160.0,
        "quantity": 25,
        "description": "Delicate Bengali sweet made from fresh cottage cheese and cardamom",
        "image_url": "https://picsum.photos/300/200?random=8"
    },
    {
        "name": "Mysore Pak",
        "category": "South Indian",
        "price": 250.0,
        "quantity": 20,
        "description": "Rich and ghee-laden sweet from Karnataka with gram flour",
        "image_url": "https://picsum.photos/300/200?random=9"
    },
    {
        "name": "Peda",
        "category": "Traditional",
        "price": 120.0,
        "quantity": 55,
        "description": "Milk-based sweet flavored with cardamom and saffron",
        "image_url": "https://picsum.photos/300/200?random=10"
    }
]

def clear_database():
    """Clear all existing data"""
    db = SessionLocal()
    try:
        # Delete all sweets and users
        db.query(models.Sweet).delete()
        db.query(models.User).delete()
        db.commit()
        print("✅ Database cleared successfully!")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

def seed_database():
    """Seed the database with initial sweet data"""
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if sweets already exist
        existing_sweets = db.query(models.Sweet).count()
        if existing_sweets > 0:
            print("Database already seeded! Use clear_database() first if you want to reseed.")
            return
        
        # Add sweets
        for sweet_data in INDIAN_SWEETS:
            sweet = schemas.SweetCreate(**sweet_data)
            crud.create_sweet(db=db, sweet=sweet)
        
        print(f"✅ Successfully seeded database with {len(INDIAN_SWEETS)} Indian sweets!")
        print("Images are loaded from Picsum (placeholder service)")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_database()
    else:
        seed_database()