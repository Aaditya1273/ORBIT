#!/usr/bin/env python3
"""
Test script to verify Redis integration with ORBIT
"""

import asyncio
import os
from dotenv import load_dotenv
from src.core.redis import init_redis, cache, session_manager, health_check_redis

# Load environment variables
load_dotenv('.env.local')

async def test_redis_basic():
    """Test basic Redis operations"""
    
    print("🧪 Testing Redis Integration for ORBIT\n")
    print(f"Redis URL: {os.getenv('REDIS_URL')[:30]}...")
    print("-" * 60)
    
    try:
        # Initialize Redis
        await init_redis()
        print("✅ Redis connection established")
        
        # Test health check
        health = await health_check_redis()
        print(f"✅ Health check: {health['status']}")
        
        # Test basic cache operations
        print("\n🔧 Testing cache operations...")
        
        # Set a value
        success = await cache.set("test_key", {"message": "Hello ORBIT!", "number": 42}, expire=60)
        print(f"✅ Set operation: {'Success' if success else 'Failed'}")
        
        # Get the value
        value = await cache.get("test_key")
        print(f"✅ Get operation: {value}")
        
        # Test increment
        counter = await cache.increment("test_counter", amount=5, expire=60)
        print(f"✅ Increment operation: {counter}")
        
        # Test hash operations
        hash_success = await cache.set_hash("test_hash", {
            "user_id": "12345",
            "session_data": {"logged_in": True, "role": "user"},
            "timestamp": "2026-02-05T21:00:00Z"
        }, expire=60)
        print(f"✅ Hash set operation: {'Success' if hash_success else 'Failed'}")
        
        # Get hash
        hash_data = await cache.get_hash("test_hash")
        print(f"✅ Hash get operation: {hash_data}")
        
        # Test session management
        print("\n👤 Testing session management...")
        
        session_id = await session_manager.create_session(
            user_id="test_user_123",
            session_data={
                "email": "test@orbit.ai",
                "preferences": {"theme": "dark", "notifications": True}
            }
        )
        print(f"✅ Session created: {session_id}")
        
        # Get session
        session_data = await session_manager.get_session(session_id)
        print(f"✅ Session retrieved: {session_data}")
        
        # Update session
        update_success = await session_manager.update_session(
            session_id,
            {"last_action": "test_completed", "score": 100}
        )
        print(f"✅ Session updated: {'Success' if update_success else 'Failed'}")
        
        # Get updated session
        updated_session = await session_manager.get_session(session_id)
        print(f"✅ Updated session: {updated_session}")
        
        # Clean up
        await cache.delete("test_key")
        await cache.delete("test_counter")
        await cache.delete("test_hash")
        await session_manager.delete_session(session_id)
        print("\n🧹 Cleanup completed")
        
        print("\n🎉 Redis integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Redis test failed: {str(e)}")

async def test_redis_performance():
    """Test Redis performance with multiple operations"""
    
    print("\n⚡ Testing Redis performance...")
    print("-" * 60)
    
    try:
        import time
        
        # Test bulk operations
        start_time = time.time()
        
        # Set 100 keys
        for i in range(100):
            await cache.set(f"perf_test_{i}", {"index": i, "data": f"test_data_{i}"}, expire=30)
        
        set_time = time.time() - start_time
        print(f"✅ Set 100 keys in {set_time:.3f} seconds")
        
        # Get 100 keys
        start_time = time.time()
        
        for i in range(100):
            value = await cache.get(f"perf_test_{i}")
        
        get_time = time.time() - start_time
        print(f"✅ Get 100 keys in {get_time:.3f} seconds")
        
        # Clean up
        for i in range(100):
            await cache.delete(f"perf_test_{i}")
        
        print(f"✅ Performance test completed")
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")

async def main():
    """Main test function"""
    await test_redis_basic()
    await test_redis_performance()

if __name__ == "__main__":
    asyncio.run(main())