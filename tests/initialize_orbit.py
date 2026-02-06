"""
ORBIT Initialization Script
Initializes database, creates tables, and sets up the platform
"""

import asyncio
from dotenv import load_dotenv
import sys

# Load environment
load_dotenv('.env.local')

def initialize_database():
    """Initialize SQLite database and create tables"""
    print("=" * 70)
    print("🗄️  INITIALIZING ORBIT DATABASE")
    print("=" * 70)
    
    try:
        from src.database.database import init_db, engine
        from src.database.models import Base
        
        print("\n1️⃣  Creating database tables...")
        init_db()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Database initialized successfully!")
        print(f"📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_redis():
    """Test Redis connection"""
    print("\n" + "=" * 70)
    print("⚡ TESTING REDIS CONNECTION")
    print("=" * 70)
    
    try:
        from src.core.redis import init_redis, cache
        
        print("\n1️⃣  Connecting to Redis...")
        await init_redis()
        
        print("2️⃣  Testing cache operations...")
        test_key = "init_test"
        await cache.set(test_key, {"status": "working"}, expire=10)
        result = await cache.get(test_key)
        await cache.delete(test_key)
        
        if result and result.get("status") == "working":
            print("\n✅ Redis connection successful!")
            return True
        else:
            print("\n❌ Redis test failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Redis connection failed: {str(e)}")
        return False


def test_ai_models():
    """Test AI model configuration"""
    print("\n" + "=" * 70)
    print("🤖 TESTING AI MODELS")
    print("=" * 70)
    
    try:
        from src.core.config import MODEL_CONFIGS
        
        print("\n📋 Configured Models:")
        for agent_type, config in MODEL_CONFIGS.items():
            print(f"\n{agent_type.upper()} Agent:")
            print(f"   Model: {config['model']}")
            print(f"   Provider: {config['provider']}")
            print(f"   Max Tokens: {config['max_tokens']}")
        
        print("\n✅ AI models configured!")
        return True
        
    except Exception as e:
        print(f"\n❌ AI model configuration error: {str(e)}")
        return False


def test_email():
    """Test email configuration"""
    print("\n" + "=" * 70)
    print("📧 TESTING EMAIL CONFIGURATION")
    print("=" * 70)
    
    try:
        from src.core.config import settings
        
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            print(f"\n✅ Email configured:")
            print(f"   SMTP Host: {settings.SMTP_HOST}")
            print(f"   SMTP Port: {settings.SMTP_PORT}")
            print(f"   From Email: {settings.FROM_EMAIL}")
            return True
        else:
            print("\n⚠️  Email not fully configured")
            return False
            
    except Exception as e:
        print(f"\n❌ Email configuration error: {str(e)}")
        return False


async def main():
    """Main initialization function"""
    print("\n")
    print("🚀" * 35)
    print("🎯 ORBIT PLATFORM INITIALIZATION")
    print("🚀" * 35)
    print("\n")
    
    results = {}
    
    # Initialize database
    results['database'] = initialize_database()
    
    # Test Redis
    results['redis'] = await test_redis()
    
    # Test AI models
    results['ai_models'] = test_ai_models()
    
    # Test email
    results['email'] = test_email()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 INITIALIZATION SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.upper().replace('_', ' ')}: {'PASSED' if status else 'FAILED'}")
    
    print("\n" + "=" * 70)
    print(f"🎯 RESULT: {passed}/{total} components initialized")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS READY!")
        print("\n✅ Your ORBIT platform is fully initialized and ready to use!")
        print("\n🚀 Next Steps:")
        print("   1. Start backend:  python -m uvicorn src.main:app --reload")
        print("   2. Start frontend: cd frontend && npm start")
        print("   3. Open browser:   http://localhost:3000")
        print("   4. Register account and start using ORBIT!")
        
        print("\n💡 Test Commands:")
        print("   • Test email:      python test_email.py")
        print("   • Test monitoring: python test_monitoring.py")
        print("   • Verify setup:    python verify_setup.py")
        
    elif passed >= total - 1:
        print("\n✅ CORE SYSTEMS READY!")
        print("\n⚠️  Some optional features need configuration")
        print("   But you can start using ORBIT now!")
        
        print("\n🚀 Start the platform:")
        print("   Backend:  python -m uvicorn src.main:app --reload")
        print("   Frontend: cd frontend && npm start")
        
    else:
        print("\n⚠️  SOME SYSTEMS NEED ATTENTION")
        print("\nPlease fix the failed components before starting.")
    
    print("\n" + "=" * 70)
    print("\n")
    
    return passed >= total - 1


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
