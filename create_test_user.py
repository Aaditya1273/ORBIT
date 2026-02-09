"""
Create a test user directly in the database for development
"""
import sys
import uuid
from datetime import datetime
sys.path.append('.')

from src.database.database import SessionLocal
from src.database.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    db = SessionLocal()
    try:
        # Test credentials
        email = "test@orbit.com"
        password = "orbit123"
        name = "Test User"
        
        # Delete existing user if exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"🗑️  Deleting existing user...")
            db.delete(existing)
            db.commit()
        
        # Hash password (truncate to 72 bytes like in auth.py)
        password_truncated = password[:72] if len(password) > 72 else password
        hashed = pwd_context.hash(password_truncated)
        
        # Create user
        user = User(
            id=uuid.uuid4(),
            email=email,
            name=name,
            password_hash=hashed,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow(),
            onboarding_completed=False  # Set to False so they go through onboarding
        )
        
        db.add(user)
        db.commit()
        
        print("\n" + "="*60)
        print("✅ TEST USER CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"👤 Name: {name}")
        print("="*60)
        print("\n🚀 You can now login at: http://localhost:3000/login")
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
