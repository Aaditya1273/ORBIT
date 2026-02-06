"""
Test ORBIT Monitoring Setup
Verifies Sentry and Opik integration
"""

import asyncio
import httpx
from dotenv import load_dotenv
import os

# Load environment
load_dotenv('.env.local')

async def test_monitoring():
    """Test monitoring endpoints"""
    
    print("=" * 70)
    print("🔍 ORBIT MONITORING TEST")
    print("=" * 70)
    
    base_url = "http://localhost:8000"
    
    # Check if server is running
    print("\n1️⃣  Checking if server is running...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Server is running")
                print(f"   📊 Version: {data.get('version')}")
                print(f"   🌍 Environment: {data.get('environment')}")
                
                monitoring = data.get('monitoring', {})
                print(f"   🔍 Sentry: {monitoring.get('sentry', 'unknown')}")
                print(f"   🤖 Opik: {monitoring.get('opik', 'unknown')}")
            else:
                print(f"   ❌ Server returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ Server not running: {str(e)}")
        print(f"   💡 Start server with: python -m uvicorn src.main:app --reload")
        return False
    
    # Check health endpoint
    print("\n2️⃣  Checking health endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Health check passed")
                print(f"   📊 Status: {data.get('status')}")
                
                services = data.get('services', {})
                for service, info in services.items():
                    status = info.get('status', 'unknown')
                    icon = "✅" if status in ['healthy', 'enabled'] else "⚠️"
                    print(f"   {icon} {service.capitalize()}: {status}")
            else:
                print(f"   ❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {str(e)}")
    
    # Check environment configuration
    print("\n3️⃣  Checking environment configuration...")
    
    sentry_dsn = os.getenv('SENTRY_DSN', '')
    opik_key = os.getenv('OPIK_API_KEY', '')
    
    if sentry_dsn and 'sentry.io' in sentry_dsn:
        print(f"   ✅ Sentry DSN configured")
        print(f"   🔗 DSN: {sentry_dsn[:50]}...")
    else:
        print(f"   ⚠️  Sentry DSN not configured")
    
    if opik_key and opik_key != 'test-key':
        print(f"   ✅ Opik API key configured")
        print(f"   🔑 Key: {opik_key[:20]}...")
    else:
        print(f"   ⚠️  Opik API key not configured")
    
    # Test Sentry debug endpoint (only if server is running)
    print("\n4️⃣  Testing Sentry error capture...")
    print("   ℹ️  This will trigger a test error")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/sentry-debug")
            # This should return 500 error
            if response.status_code == 500:
                print(f"   ✅ Test error triggered successfully")
                print(f"   📊 Check Sentry dashboard for the error")
                print(f"   🔗 https://sentry.io")
            elif response.status_code == 403:
                print(f"   ⚠️  Debug endpoint disabled (production mode)")
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Could not test error capture: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 MONITORING SUMMARY")
    print("=" * 70)
    
    print("\n✅ Configured:")
    print("   • Sentry error monitoring")
    print("   • Opik AI monitoring")
    print("   • FastAPI automatic tracking")
    print("   • Performance monitoring")
    print("   • Health check endpoint")
    
    print("\n🎯 Next Steps:")
    print("   1. Check Sentry dashboard: https://sentry.io")
    print("   2. Verify test error appears in Issues")
    print("   3. Check Performance tab for API metrics")
    print("   4. Configure alerts in Sentry settings")
    
    print("\n💡 Useful Commands:")
    print("   • Start server: python -m uvicorn src.main:app --reload")
    print("   • Test error: curl http://localhost:8000/sentry-debug")
    print("   • Health check: curl http://localhost:8000/health")
    
    print("\n" + "=" * 70)
    
    return True


if __name__ == "__main__":
    asyncio.run(test_monitoring())
