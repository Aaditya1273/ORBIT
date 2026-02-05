#!/usr/bin/env python3
"""
Debug Redis connection for ORBIT
"""

import asyncio
import os
from dotenv import load_dotenv
import redis.asyncio as redis
from urllib.parse import urlparse

# Load environment variables
load_dotenv('.env.local')

async def debug_redis_connection():
    """Debug Redis connection details"""
    
    redis_url = os.getenv('REDIS_URL')
    
    print("🔍 Debugging Redis Connection for ORBIT\n")
    print(f"Full Redis URL: {redis_url}")
    
    # Parse URL
    parsed = urlparse(redis_url)
    print(f"Scheme: {parsed.scheme}")
    print(f"Hostname: {parsed.hostname}")
    print(f"Port: {parsed.port}")
    print(f"Username: {parsed.username}")
    print(f"Password: {parsed.password[:10]}..." if parsed.password else "None")
    print("-" * 60)
    
    # Try different connection methods
    connection_methods = [
        {
            "name": "Method 1: from_url with SSL",
            "params": {
                "url": redis_url,
                "ssl": True,
                "ssl_check_hostname": False,
                "ssl_cert_reqs": "none"
            }
        },
        {
            "name": "Method 2: from_url basic",
            "params": {
                "url": redis_url,
                "decode_responses": True
            }
        },
        {
            "name": "Method 3: Direct connection",
            "params": {
                "host": parsed.hostname,
                "port": parsed.port,
                "username": parsed.username,
                "password": parsed.password,
                "ssl": True,
                "ssl_check_hostname": False,
                "decode_responses": True
            }
        }
    ]
    
    for method in connection_methods:
        print(f"\n🧪 Testing {method['name']}...")
        try:
            if "url" in method["params"]:
                client = redis.from_url(**method["params"])
            else:
                client = redis.Redis(**method["params"])
            
            # Test connection
            result = await client.ping()
            print(f"✅ SUCCESS: {result}")
            
            # Test basic operation
            await client.set("test", "hello", ex=10)
            value = await client.get("test")
            print(f"✅ Set/Get test: {value}")
            
            await client.delete("test")
            await client.close()
            break
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            try:
                await client.close()
            except:
                pass

async def main():
    await debug_redis_connection()

if __name__ == "__main__":
    asyncio.run(main())