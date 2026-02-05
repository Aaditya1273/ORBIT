#!/usr/bin/env python3
"""
Test script to check available models on OpenRouter
"""

import asyncio
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

async def check_openrouter_models():
    """Check available models on OpenRouter"""
    
    api_key = os.getenv('OPEN_ROUTER_API_KEY')
    
    if not api_key:
        print("❌ No OpenRouter API key found")
        return
    
    print("🔍 Checking available models on OpenRouter...")
    print(f"API Key: {api_key[:20]}...")
    print("-" * 60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                models = response.json()
                
                print(f"✅ Found {len(models.get('data', []))} models")
                
                # Filter for relevant models
                relevant_models = []
                for model in models.get('data', []):
                    model_id = model.get('id', '')
                    if any(keyword in model_id.lower() for keyword in ['claude', 'gpt', 'llama', 'gemini']):
                        relevant_models.append({
                            'id': model_id,
                            'name': model.get('name', ''),
                            'pricing': model.get('pricing', {}),
                            'context_length': model.get('context_length', 0)
                        })
                
                print(f"\n📋 Relevant models for ORBIT ({len(relevant_models)} found):")
                print("-" * 60)
                
                for model in relevant_models[:20]:  # Show first 20
                    pricing = model['pricing']
                    prompt_cost = pricing.get('prompt', 'N/A')
                    completion_cost = pricing.get('completion', 'N/A')
                    
                    print(f"🤖 {model['id']}")
                    print(f"   Name: {model['name']}")
                    print(f"   Context: {model['context_length']:,} tokens")
                    print(f"   Cost: ${prompt_cost}/1M prompt, ${completion_cost}/1M completion")
                    print()
                
            else:
                print(f"❌ Failed to fetch models: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Error checking models: {str(e)}")

async def test_simple_models():
    """Test some basic models that should work"""
    
    api_key = os.getenv('OPEN_ROUTER_API_KEY')
    
    # Try some basic models
    test_models = [
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3-haiku",
        "meta-llama/llama-3-8b-instruct",
        "google/gemini-pro"
    ]
    
    print("\n🧪 Testing basic models...")
    print("-" * 60)
    
    for model in test_models:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Say 'Hello' in one word."}
                ],
                "max_tokens": 10
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ {model}: {content.strip()}")
                else:
                    print(f"❌ {model}: {response.status_code} - {response.text[:100]}")
                    
        except Exception as e:
            print(f"❌ {model}: {str(e)}")

async def main():
    await check_openrouter_models()
    await test_simple_models()

if __name__ == "__main__":
    asyncio.run(main())