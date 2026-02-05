#!/usr/bin/env python3
"""
Simple test script to verify Redis connection with ORBIT
"""

import asyncio
import os
from dotenv import load_dotenv
import redis.asyncio as redis

# Load environment variables
load_dotenv('.env.local')

async def test_redis_connection():
    """Test basic Redis connection"""
    
    redis_url = os.getenv('REDIS_URL')
    
    print("🧪 Testing Redis Connection for ORBIT\n")
    print(f"Redis URL: {redis_url[:30]}...")
    print("-" * 60)
    
    try:
        # Parse URL for Upstash Redis
        from urllib.parse import urlparse
        parsed = urlparse(redis_url)
        
        # Create Redis client with direct connection
        client = redis.Redis(
            host=parsed.hostname,
            port=parsed.port,
            username=parsed.username,
            password=parsed.password,
            ssl=True,
            ssl_check_hostname=False,
            decode_responses=True,
            socket_connect_timeout=30,
            socket_timeout=30
        )
        
        # Test connection
        await client.ping()
        print("✅ Redis connection successful")
        
        # Test basic operations
        await client.set("test_key", "Hello ORBIT!", ex=60)
        value = await client.get("test_key")
        print(f"✅ Set/Get test: {value}")
        
        # Test increment
        counter = await client.incr("test_counter")
        print(f"✅ Increment test: {counter}")
        
        # Clean up
        await client.delete("test_key", "test_counter")
        print("✅ Cleanup completed")
        
        # Close connection
        await client.aclose()
        
        print("\n🎉 Redis integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Redis test failed: {str(e)}")

async def main():
    await test_redis_connection()

if __name__ == "__main__":
    asyncio.run(main())