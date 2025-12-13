#!/usr/bin/env python3
"""
Test script to verify CPZ AI platform access
This will test the actual connection to your CPZ AI platform using your API keys
Direct endpoint: https://api.cpz-lab.com
"""

import os
import sys
from dotenv import load_dotenv

try:
    from cpz.common.cpz_ai import CPZAIClient
    print("✅ Successfully imported CPZAIClient")
except ImportError as e:
    print(f"❌ Failed to import CPZAIClient: {e}")
    sys.exit(1)

def test_cpz_ai_access():
    """Test CPZ AI platform access"""
    
    print("🚀 Testing CPZ AI Platform Access")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are set
    api_key = os.getenv("CPZ_AI_API_KEY")
    secret_key = os.getenv("CPZ_AI_SECRET_KEY")
    
    # Use the main Supabase REST API endpoint
    url = "https://your-platform-url.supabase.co"
    
    print(f"🔑 API Key: {'✅ Set' if api_key else '❌ Missing'}")
    print(f"🔐 Secret Key: {'✅ Set' if secret_key else '❌ Missing'}")
    print(f"🌐 URL: {url}")
    
    if not api_key or not secret_key:
        print("\n❌ Please set CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY in your .env file")
        return False
    
    try:
        # Create client with actual Supabase endpoint
        print("\n🔌 Creating CPZ AI client...")
        client = CPZAIClient(api_key=api_key, secret_key=secret_key, url=url)
        print("✅ Client created successfully")
        
        # Test connection health
        print("\n🏥 Testing connection health...")
        if client.health():
            print("✅ Platform is healthy and accessible")
        else:
            print("❌ Platform health check failed")
            return False
        
        # Test getting strategies
        print("\n📊 Testing strategies access...")
        strategies = client.get_strategies(limit=5)
        print(f"✅ Retrieved {len(strategies)} strategies")
        
        if strategies:
            print("Sample strategies:")
            for i, strategy in enumerate(strategies[:3], 1):
                name = strategy.get('name', 'Unknown')
                desc = strategy.get('description', 'No description')
                print(f"  {i}. {name}: {desc}")
        
        # Test getting files from storage
        print("\n📁 Testing storage files access...")
        files = client.get_files(bucket_name="default")
        print(f"✅ Retrieved {len(files)} files from storage")
        
        if files:
            print("Sample files:")
            for i, file in enumerate(files[:3], 1):
                name = file.get('name', 'Unknown')
                file_type = file.get('mimetype', 'Unknown type')
                print(f"  {i}. {name} ({file_type})")
        
        # Test listing tables
        print("\n📋 Testing table listing...")
        tables = client.list_tables()
        print(f"✅ Available tables: {', '.join(tables) if tables else 'None'}")
        
        print("\n🎉 All tests passed! CPZ AI platform access is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cpz_ai_access()
    sys.exit(0 if success else 1)
