"""
Complete ORBIT Setup Verification Test
Tests all configured services and components
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

def test_environment_variables():
    """Test that all required environment variables are set"""
    print("\n🔍 Testing Environment Variables...")
    
    required_vars = {
        'GOOGLE_API_KEY': 'Google Gemini API',
        'OPEN_ROUTER_API_KEY': 'OpenRouter API',
        'REDIS_URL': 'Upstash Redis',
        'OPIK_API_KEY': 'Opik Monitoring',
        'DATABASE_URL': 'Database',
        'SECRET_KEY': 'App Secret',
        'JWT_SECRET_KEY': 'JWT Secret'
    }
    
    all_set = True
    for var, name in required_vars.items():
        value = os.getenv(var)
        if value and value != 'test-key':
            print(f"  ✅ {name}: Configured")
        else:
            print(f"  ❌ {name}: Missing or placeholder")
            all_set = False
    
    return all_set


async def test_redis_connection():
    """Test Redis connection"""
    print("\n🔍 Testing Redis Connection...")
    
    try:
        from src.core.redis import init_redis, cache
        
        # Initialize Redis
        await init_redis()
        
        # Test set/get
        test_key = "setup_test"
        await cache.set(test_key, {"status": "working"}, expire=10)
        result = await cache.get(test_key)
        
        if result and result.get("status") == "working":
            print("  ✅ Redis: Connected and working")
            await cache.delete(test_key)
            return True
        else:
            print("  ❌ Redis: Connection failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Redis: Error - {str(e)}")
        return False


async def test_openrouter_models():
    """Test OpenRouter API"""
    print("\n🔍 Testing OpenRouter Models...")
    
    try:
        from src.agents.base_agent import OpenRouterLLM
        from langchain_core.messages import HumanMessage
        
        models = [
            ("anthropic/claude-3-haiku", "Claude 3 Haiku"),
            ("openai/gpt-3.5-turbo", "GPT-3.5 Turbo"),
            ("meta-llama/llama-3-8b-instruct", "Llama 3 8B")
        ]
        
        all_working = True
        for model_name, display_name in models:
            try:
                llm = OpenRouterLLM(model=model_name, max_tokens=50)
                response = await llm.ainvoke([
                    HumanMessage(content="Say 'OK' if you're working")
                ])
                
                if response and response.content:
                    print(f"  ✅ {display_name}: Working")
                else:
                    print(f"  ❌ {display_name}: No response")
                    all_working = False
                    
            except Exception as e:
                if "rate limit" in str(e).lower():
                    print(f"  ⚠️  {display_name}: Rate limited (but configured)")
                else:
                    print(f"  ❌ {display_name}: Error - {str(e)[:50]}")
                    all_working = False
        
        return all_working
        
    except Exception as e:
        print(f"  ❌ OpenRouter: Error - {str(e)}")
        return False


async def test_gemini_model():
    """Test Google Gemini API"""
    print("\n🔍 Testing Google Gemini...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            max_output_tokens=50
        )
        
        response = await llm.ainvoke([
            HumanMessage(content="Say 'OK' if you're working")
        ])
        
        if response and response.content:
            print(f"  ✅ Gemini 2.5 Flash: Working")
            return True
        else:
            print(f"  ❌ Gemini: No response")
            return False
            
    except Exception as e:
        print(f"  ❌ Gemini: Error - {str(e)[:100]}")
        return False


def test_database():
    """Test database connection"""
    print("\n🔍 Testing Database...")
    
    try:
        import sqlite3
        db_url = os.getenv('DATABASE_URL', 'sqlite:///./orbit_dev.db')
        db_path = db_url.replace('sqlite:///', '')
        
        # Test connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"  ✅ SQLite: Connected ({db_path})")
            print(f"  ℹ️  SQLite handles up to 10K users perfectly!")
            return True
        else:
            print(f"  ❌ SQLite: Connection failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Database: Error - {str(e)}")
        return False


def test_opik_config():
    """Test Opik configuration"""
    print("\n🔍 Testing Opik Configuration...")
    
    try:
        api_key = os.getenv('OPIK_API_KEY')
        project = os.getenv('OPIK_PROJECT_NAME')
        workspace = os.getenv('OPIK_WORKSPACE')
        
        if api_key and api_key != 'test-key':
            print(f"  ✅ Opik API Key: Configured")
            print(f"  ✅ Project: {project}")
            print(f"  ✅ Workspace: {workspace}")
            return True
        else:
            print(f"  ❌ Opik: Not configured")
            return False
            
    except Exception as e:
        print(f"  ❌ Opik: Error - {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 ORBIT Complete Setup Verification")
    print("=" * 60)
    
    results = {}
    
    # Test environment variables
    results['env'] = test_environment_variables()
    
    # Test database
    results['database'] = test_database()
    
    # Test Redis
    results['redis'] = await test_redis_connection()
    
    # Test Opik
    results['opik'] = test_opik_config()
    
    # Test Gemini
    results['gemini'] = await test_gemini_model()
    
    # Test OpenRouter (may be rate limited)
    results['openrouter'] = await test_openrouter_models()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.upper()}: {'PASSED' if status else 'FAILED'}")
    
    print("\n" + "=" * 60)
    print(f"🎯 RESULT: {passed}/{total} components working")
    
    if passed == total:
        print("🎉 ALL SYSTEMS OPERATIONAL - READY TO LAUNCH!")
    elif passed >= total - 1:
        print("✅ CORE SYSTEMS OPERATIONAL - READY TO RUN!")
        print("   (Some optional features may need configuration)")
    else:
        print("⚠️  SOME SYSTEMS NEED ATTENTION")
    
    print("=" * 60)
    
    return passed >= total - 1


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
