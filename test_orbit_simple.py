#!/usr/bin/env python3
"""
Simple ORBIT integration test without complex configuration
"""

import asyncio
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

async def test_orbit_simple():
    """Test ORBIT components without complex config"""
    
    print("🚀 ORBIT Simple Integration Test")
    print("=" * 50)
    
    # Test 1: Redis Direct Connection
    print("\n📊 Test 1: Redis Connection")
    print("-" * 30)
    
    try:
        import redis.asyncio as redis
        from urllib.parse import urlparse
        
        redis_url = os.getenv('REDIS_URL')
        parsed = urlparse(redis_url)
        
        client = redis.Redis(
            host=parsed.hostname,
            port=parsed.port,
            username=parsed.username,
            password=parsed.password,
            ssl=True,
            ssl_check_hostname=False,
            decode_responses=True
        )
        
        await client.ping()
        print("✅ Redis connection successful")
        
        # Test caching
        test_data = {
            "user_id": "test_123",
            "goal": "Exercise 3x per week",
            "timestamp": datetime.now().isoformat()
        }
        
        await client.set("orbit_test", str(test_data), ex=60)
        cached_data = await client.get("orbit_test")
        print(f"✅ Cache test: {cached_data[:50]}...")
        
        await client.delete("orbit_test")
        await client.aclose()
        
    except Exception as e:
        print(f"❌ Redis test failed: {str(e)}")
        return False
    
    # Test 2: OpenRouter Models
    print("\n🤖 Test 2: OpenRouter AI Models")
    print("-" * 30)
    
    try:
        import httpx
        
        api_key = os.getenv('OPEN_ROUTER_API_KEY')
        
        # Test Claude (Supervisor)
        payload = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "system", "content": "You are an AI supervisor for ORBIT."},
                {"role": "user", "content": "Rate this intervention from 1-10: 'Take a 5-minute walk.'"}
            ],
            "max_tokens": 50
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            response = await http_client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"✅ Claude (Supervisor): {content.strip()}")
            else:
                print(f"❌ Claude failed: {response.status_code}")
                return False
        
        # Test GPT-3.5 (Optimizer)
        payload["model"] = "openai/gpt-3.5-turbo"
        payload["messages"][1]["content"] = "Suggest one improvement for this goal: 'Exercise more.'"
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            response = await http_client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"✅ GPT-3.5 (Optimizer): {content.strip()}")
            else:
                print(f"❌ GPT-3.5 failed: {response.status_code}")
                return False
        
    except Exception as e:
        print(f"❌ OpenRouter test failed: {str(e)}")
        return False
    
    # Test 3: Google Gemini
    print("\n🌟 Test 3: Google Gemini")
    print("-" * 30)
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(
            "Generate a motivational intervention for someone who wants to read more books. Keep it under 50 words."
        )
        
        print(f"✅ Gemini (Worker): {response.text.strip()}")
        
    except Exception as e:
        print(f"❌ Gemini test failed: {str(e)}")
        return False
    
    # Test 4: Complete Workflow
    print("\n⚡ Test 4: Complete Workflow")
    print("-" * 30)
    
    try:
        # Simulate complete ORBIT workflow
        user_goal = "I want to drink more water daily"
        
        # Step 1: Generate intervention (Gemini)
        intervention_response = model.generate_content(
            f"Create a specific behavioral intervention for this goal: {user_goal}. Use behavioral science principles. Keep it under 100 words."
        )
        intervention = intervention_response.text.strip()
        print(f"✅ Intervention: {intervention[:60]}...")
        
        # Step 2: Evaluate intervention (Claude)
        eval_payload = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "system", "content": "Rate interventions on safety (1-10) and effectiveness (1-10)."},
                {"role": "user", "content": f"Evaluate: {intervention}"}
            ],
            "max_tokens": 100
        }
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            response = await http_client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=eval_payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                evaluation = result["choices"][0]["message"]["content"]
                print(f"✅ Evaluation: {evaluation.strip()[:60]}...")
            else:
                print(f"❌ Evaluation failed: {response.status_code}")
                return False
        
        # Step 3: Cache workflow result
        workflow_data = {
            "id": str(uuid.uuid4()),
            "user_goal": user_goal,
            "intervention": intervention,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat(),
            "models": {
                "worker": "gemini-2.5-flash",
                "supervisor": "claude-3-haiku"
            }
        }
        
        # Reconnect to Redis for caching
        client = redis.Redis(
            host=parsed.hostname,
            port=parsed.port,
            username=parsed.username,
            password=parsed.password,
            ssl=True,
            ssl_check_hostname=False,
            decode_responses=True
        )
        
        await client.set(f"workflow_{workflow_data['id']}", str(workflow_data), ex=300)
        cached_workflow = await client.get(f"workflow_{workflow_data['id']}")
        
        if cached_workflow:
            print(f"✅ Workflow cached: {workflow_data['id']}")
        else:
            print("❌ Workflow caching failed")
            return False
        
        await client.delete(f"workflow_{workflow_data['id']}")
        await client.aclose()
        
    except Exception as e:
        print(f"❌ Workflow test failed: {str(e)}")
        return False
    
    # Success!
    print("\n🎉 ORBIT Integration Test Results")
    print("=" * 50)
    print("✅ Redis Integration: PASSED")
    print("✅ OpenRouter Models: PASSED") 
    print("✅ Google Gemini: PASSED")
    print("✅ Complete Workflow: PASSED")
    print("\n🚀 ORBIT Platform Ready!")
    print("\nConfiguration Summary:")
    print("- Worker: Gemini 2.5 Flash (Google Direct)")
    print("- Supervisor: Claude 3 Haiku (OpenRouter)")
    print("- Optimizer: GPT-3.5 Turbo (OpenRouter)")
    print("- Cache: Upstash Redis (SSL)")
    print("- Cost: Optimized via OpenRouter")
    
    return True

async def main():
    success = await test_orbit_simple()
    if success:
        print("\n✅ All systems operational! ORBIT is ready to launch.")
    else:
        print("\n❌ Integration test failed. Check configuration.")

if __name__ == "__main__":
    asyncio.run(main())