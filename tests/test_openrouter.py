#!/usr/bin/env python3
"""
Test script to verify OpenRouter integration with ORBIT
"""

import asyncio
import os
from dotenv import load_dotenv
from src.agents.base_agent import OpenRouterLLM
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv('.env.local')

async def test_openrouter_models():
    """Test different OpenRouter models"""
    
    # Test models available through your OpenRouter key
    test_models = [
        "anthropic/claude-3-sonnet-20240229",  # For Supervisor Agent
        "openai/gpt-4-turbo-preview",          # For Optimizer Agent  
        "meta-llama/llama-3.1-8b-instruct:free",  # Free fallback model
        "google/gemini-pro",                   # Alternative to direct Gemini
    ]
    
    test_message = [
        SystemMessage(content="You are a helpful AI assistant for the ORBIT platform."),
        HumanMessage(content="Explain in one sentence what behavioral science is.")
    ]
    
    print("🧪 Testing OpenRouter Models for ORBIT\n")
    print(f"OpenRouter API Key: {os.getenv('OPEN_ROUTER_API_KEY')[:20]}...")
    print("-" * 60)
    
    for model in test_models:
        try:
            print(f"\n🤖 Testing {model}...")
            
            llm = OpenRouterLLM(
                model=model,
                temperature=0.7,
                max_tokens=100,
                api_key=os.getenv('OPEN_ROUTER_API_KEY')
            )
            
            response = await llm.ainvoke(test_message)
            
            print(f"✅ SUCCESS: {model}")
            print(f"Response: {response.content[:100]}...")
            
            if hasattr(response, 'response_metadata'):
                usage = response.response_metadata.get('usage', {})
                print(f"Tokens: {usage.get('total_tokens', 'N/A')}")
            
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {str(e)}")
        
        print("-" * 40)

async def test_orbit_agents():
    """Test ORBIT agents with OpenRouter"""
    
    print("\n🚀 Testing ORBIT Agents with OpenRouter\n")
    
    try:
        from src.agents.worker_agent import WorkerAgent
        from src.agents.supervisor_agent import SupervisorAgent
        from src.agents.base_agent import AgentContext
        
        # Test Worker Agent (should use Gemini directly)
        print("🤖 Testing Worker Agent...")
        worker = WorkerAgent()
        
        context = AgentContext(
            user_id="test_user",
            session_id="test_session",
            current_goals=[{
                "title": "Exercise 3 times per week",
                "domain": "health",
                "progress": 0.6
            }],
            user_state={"energy_level": "high"},
            recent_history=[]
        )
        
        worker_response = await worker.execute(
            context=context,
            user_input="I need motivation to work out today"
        )
        
        print(f"✅ Worker Agent Response: {worker_response.content[:100]}...")
        print(f"Confidence: {worker_response.confidence}")
        
        # Test Supervisor Agent (should use Claude via OpenRouter)
        print("\n🛡️ Testing Supervisor Agent...")
        supervisor = SupervisorAgent()
        
        supervisor_response = await supervisor.execute(
            context=context,
            user_input=worker_response.content
        )
        
        print(f"✅ Supervisor Agent Response: {supervisor_response.content[:100]}...")
        print(f"Confidence: {supervisor_response.confidence}")
        
    except Exception as e:
        print(f"❌ Agent test failed: {str(e)}")

async def main():
    """Main test function"""
    await test_openrouter_models()
    await test_orbit_agents()
    
    print("\n🎉 OpenRouter Integration Test Complete!")
    print("\nModel Configuration:")
    print("- Worker Agent: Google Gemini 1.5 Pro (direct API)")
    print("- Supervisor Agent: Claude 3 Sonnet (via OpenRouter)")
    print("- Optimizer Agent: GPT-4 Turbo (via OpenRouter)")
    print("- Fallback: Llama 3.1 8B (free via OpenRouter)")

if __name__ == "__main__":
    asyncio.run(main())