#!/usr/bin/env python3
"""
Comprehensive integration test for ORBIT platform
Tests OpenRouter AI models and Redis caching together
"""

import asyncio
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

async def test_orbit_integration():
    """Test complete ORBIT integration"""
    
    print("🚀 ORBIT Platform Integration Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"OpenRouter API Key: {os.getenv('OPEN_ROUTER_API_KEY')[:20]}...")
    print(f"Google API Key: {os.getenv('GOOGLE_API_KEY')[:20]}...")
    print(f"Redis URL: {os.getenv('REDIS_URL')[:30]}...")
    print("=" * 60)
    
    # Test 1: Redis Connection and Caching
    print("\n📊 Test 1: Redis Integration")
    print("-" * 40)
    
    try:
        from src.core.redis import init_redis, cache, session_manager
        
        # Initialize Redis
        await init_redis()
        print("✅ Redis connection established")
        
        # Test session management
        session_id = await session_manager.create_session(
            user_id="test_user_orbit",
            session_data={
                "email": "test@orbit.ai",
                "goals": ["Exercise 3x/week", "Read 30min/day"],
                "preferences": {"theme": "dark"}
            }
        )
        print(f"✅ Session created: {session_id}")
        
        # Cache some AI model responses
        await cache.set("ai_responses", {
            "worker_model": "gemini-2.5-flash",
            "supervisor_model": "claude-3-haiku",
            "optimizer_model": "gpt-3.5-turbo"
        }, expire=300)
        print("✅ AI model config cached")
        
    except Exception as e:
        print(f"❌ Redis test failed: {str(e)}")
        return False
    
    # Test 2: OpenRouter AI Models
    print("\n🤖 Test 2: OpenRouter AI Integration")
    print("-" * 40)
    
    try:
        from src.agents.base_agent import OpenRouterLLM
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Test Supervisor Agent (Claude)
        supervisor_llm = OpenRouterLLM(
            model="anthropic/claude-3-haiku",
            temperature=0.3,
            max_tokens=100,
            api_key=os.getenv('OPEN_ROUTER_API_KEY')
        )
        
        supervisor_messages = [
            SystemMessage(content="You are an AI supervisor for the ORBIT platform. Evaluate interventions for safety and effectiveness."),
            HumanMessage(content="Evaluate this intervention: 'Take a 10-minute walk to boost your energy levels.'")
        ]
        
        supervisor_response = await supervisor_llm.ainvoke(supervisor_messages)
        print(f"✅ Supervisor Agent (Claude): {supervisor_response.content[:80]}...")
        
        # Cache the response
        await cache.set(f"supervisor_response_{uuid.uuid4()}", {
            "content": supervisor_response.content,
            "model": "claude-3-haiku",
            "timestamp": datetime.utcnow().isoformat()
        }, expire=300)
        
        # Test Optimizer Agent (GPT-3.5)
        optimizer_llm = OpenRouterLLM(
            model="openai/gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=100,
            api_key=os.getenv('OPEN_ROUTER_API_KEY')
        )
        
        optimizer_messages = [
            SystemMessage(content="You are an AI optimizer for the ORBIT platform. Suggest improvements to user interventions."),
            HumanMessage(content="How can we improve this goal: 'Exercise more often'?")
        ]
        
        optimizer_response = await optimizer_llm.ainvoke(optimizer_messages)
        print(f"✅ Optimizer Agent (GPT-3.5): {optimizer_response.content[:80]}...")
        
        # Cache the response
        await cache.set(f"optimizer_response_{uuid.uuid4()}", {
            "content": optimizer_response.content,
            "model": "gpt-3.5-turbo",
            "timestamp": datetime.utcnow().isoformat()
        }, expire=300)
        
    except Exception as e:
        print(f"❌ OpenRouter test failed: {str(e)}")
        return False
    
    # Test 3: Google Gemini Direct API
    print("\n🌟 Test 3: Google Gemini Integration")
    print("-" * 40)
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Test Worker Agent (Gemini)
        worker_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            max_output_tokens=100,
            google_api_key=os.getenv('GOOGLE_API_KEY'),
        )
        
        worker_messages = [
            SystemMessage(content="You are an AI worker for the ORBIT platform. Generate personalized interventions to help users achieve their goals."),
            HumanMessage(content="Generate a motivational intervention for someone who wants to exercise but feels tired.")
        ]
        
        worker_response = await worker_llm.ainvoke(worker_messages)
        print(f"✅ Worker Agent (Gemini): {worker_response.content[:80]}...")
        
        # Cache the response
        await cache.set(f"worker_response_{uuid.uuid4()}", {
            "content": worker_response.content,
            "model": "gemini-2.5-flash",
            "timestamp": datetime.utcnow().isoformat()
        }, expire=300)
        
    except Exception as e:
        print(f"❌ Gemini test failed: {str(e)}")
        return False
    
    # Test 4: Complete Workflow Simulation
    print("\n⚡ Test 4: Complete ORBIT Workflow")
    print("-" * 40)
    
    try:
        # Simulate a complete user interaction
        user_goal = "I want to read more books but I keep getting distracted by my phone"
        
        # Step 1: Worker generates intervention
        intervention_prompt = f"Generate a behavioral intervention for this goal: {user_goal}"
        worker_messages = [
            SystemMessage(content="Generate a specific, actionable intervention using behavioral science principles."),
            HumanMessage(content=intervention_prompt)
        ]
        
        intervention = await worker_llm.ainvoke(worker_messages)
        print(f"✅ Step 1 - Intervention Generated: {intervention.content[:60]}...")
        
        # Step 2: Supervisor evaluates intervention
        evaluation_prompt = f"Evaluate this intervention for safety and effectiveness: {intervention.content}"
        supervisor_messages = [
            SystemMessage(content="Evaluate interventions on a scale of 1-10 for safety and effectiveness."),
            HumanMessage(content=evaluation_prompt)
        ]
        
        evaluation = await supervisor_llm.ainvoke(supervisor_messages)
        print(f"✅ Step 2 - Intervention Evaluated: {evaluation.content[:60]}...")
        
        # Step 3: Cache complete workflow
        workflow_id = str(uuid.uuid4())
        await cache.set(f"workflow_{workflow_id}", {
            "user_goal": user_goal,
            "intervention": intervention.content,
            "evaluation": evaluation.content,
            "models_used": {
                "worker": "gemini-2.5-flash",
                "supervisor": "claude-3-haiku"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id
        }, expire=3600)
        
        print(f"✅ Step 3 - Workflow Cached: {workflow_id}")
        
        # Step 4: Retrieve and verify cached data
        cached_workflow = await cache.get(f"workflow_{workflow_id}")
        if cached_workflow and cached_workflow["user_goal"] == user_goal:
            print("✅ Step 4 - Cache Verification Successful")
        else:
            print("❌ Step 4 - Cache Verification Failed")
            return False
        
    except Exception as e:
        print(f"❌ Workflow test failed: {str(e)}")
        return False
    
    # Test 5: Performance Metrics
    print("\n📈 Test 5: Performance Metrics")
    print("-" * 40)
    
    try:
        import time
        
        # Test response times
        start_time = time.time()
        await cache.set("perf_test", {"test": "performance"}, expire=60)
        cache_time = time.time() - start_time
        print(f"✅ Redis Cache Write: {cache_time*1000:.2f}ms")
        
        start_time = time.time()
        await cache.get("perf_test")
        cache_read_time = time.time() - start_time
        print(f"✅ Redis Cache Read: {cache_read_time*1000:.2f}ms")
        
        # Clean up
        await cache.delete("perf_test")
        await session_manager.delete_session(session_id)
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False
    
    # Final Results
    print("\n🎉 ORBIT Integration Test Results")
    print("=" * 60)
    print("✅ Redis Integration: PASSED")
    print("✅ OpenRouter AI Models: PASSED")
    print("✅ Google Gemini API: PASSED")
    print("✅ Complete Workflow: PASSED")
    print("✅ Performance Metrics: PASSED")
    print("\n🚀 ORBIT Platform is ready for deployment!")
    print("\nModel Configuration:")
    print("- Worker Agent: Google Gemini 2.5 Flash (direct API)")
    print("- Supervisor Agent: Claude 3 Haiku (via OpenRouter)")
    print("- Optimizer Agent: GPT-3.5 Turbo (via OpenRouter)")
    print("- Fallback: Llama 3 8B (via OpenRouter)")
    print("\nInfrastructure:")
    print("- Redis: Upstash Redis (cloud-hosted)")
    print("- Caching: Session management and AI response caching")
    print("- API Integration: Cost-effective via OpenRouter")
    
    return True

async def main():
    success = await test_orbit_integration()
    if success:
        print("\n✅ All tests passed! ORBIT is ready to launch.")
    else:
        print("\n❌ Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    asyncio.run(main())