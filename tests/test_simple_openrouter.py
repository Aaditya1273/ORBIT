#!/usr/bin/env python3
"""
Simple test script to verify OpenRouter integration with ORBIT
"""

import asyncio
import os
from dotenv import load_dotenv
from src.agents.base_agent import OpenRouterLLM
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv('.env.local')

async def test_openrouter_basic():
    """Test basic OpenRouter functionality"""
    
    print("🧪 Testing OpenRouter Integration for ORBIT\n")
    print(f"OpenRouter API Key: {os.getenv('OPEN_ROUTER_API_KEY')[:20]}...")
    print(f"Google API Key: {os.getenv('GOOGLE_API_KEY')[:20]}...")
    print("-" * 60)
    
    # Test models available through your OpenRouter key
    test_models = [
        "anthropic/claude-3-haiku",  # For Supervisor Agent
        "openai/gpt-3.5-turbo",     # For Optimizer Agent  
        "meta-llama/llama-3-8b-instruct",  # Free fallback model
    ]
    
    test_message = [
        SystemMessage(content="You are a helpful AI assistant for the ORBIT platform."),
        HumanMessage(content="Explain in one sentence what behavioral science is.")
    ]
    
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

async def test_google_gemini():
    """Test Google Gemini directly"""
    try:
        print("\n🌟 Testing Google Gemini Direct API...")
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            max_output_tokens=100,
            google_api_key=os.getenv('GOOGLE_API_KEY'),
        )
        
        test_message = [
            SystemMessage(content="You are a helpful AI assistant for the ORBIT platform."),
            HumanMessage(content="Explain in one sentence what goal achievement is.")
        ]
        
        response = await llm.ainvoke(test_message)
        
        print(f"✅ SUCCESS: Google Gemini 1.5 Pro")
        print(f"Response: {response.content[:100]}...")
        
    except Exception as e:
        print(f"❌ FAILED: Google Gemini")
        print(f"Error: {str(e)}")

async def main():
    """Main test function"""
    await test_openrouter_basic()
    await test_google_gemini()
    
    print("\n🎉 OpenRouter Integration Test Complete!")
    print("\nModel Configuration for ORBIT:")
    print("- Worker Agent: Google Gemini 2.5 Flash (direct API)")
    print("- Supervisor Agent: Claude 3 Haiku (via OpenRouter)")
    print("- Optimizer Agent: GPT-3.5 Turbo (via OpenRouter)")
    print("- Fallback: Llama 3 8B (via OpenRouter)")

if __name__ == "__main__":
    asyncio.run(main())