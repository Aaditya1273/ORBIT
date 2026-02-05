#!/usr/bin/env python3
"""
Test script to check available Gemini models
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('.env.local')

async def check_gemini_models():
    """Check available Gemini models"""
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No Google API key found")
        return
    
    print("🔍 Checking available Gemini models...")
    print(f"API Key: {api_key[:20]}...")
    print("-" * 60)
    
    try:
        genai.configure(api_key=api_key)
        
        # List available models
        models = genai.list_models()
        
        print("📋 Available Gemini models:")
        print("-" * 60)
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"🤖 {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print(f"   Input Token Limit: {model.input_token_limit:,}")
                print(f"   Output Token Limit: {model.output_token_limit:,}")
                print()
                
    except Exception as e:
        print(f"❌ Error checking models: {str(e)}")

async def test_gemini_models():
    """Test some Gemini models"""
    
    api_key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=api_key)
    
    # Try some basic models
    test_models = [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    
    print("\n🧪 Testing Gemini models...")
    print("-" * 60)
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello' in one word.")
            
            print(f"✅ {model_name}: {response.text.strip()}")
                    
        except Exception as e:
            print(f"❌ {model_name}: {str(e)}")

async def main():
    await check_gemini_models()
    await test_gemini_models()

if __name__ == "__main__":
    asyncio.run(main())