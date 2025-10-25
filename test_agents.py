#!/usr/bin/env python3
"""
Test script to verify the A2A agent system is working.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🌱 Testing A2A Agent System")
    print("=" * 50)
    print()
    
    # Test 1: Import agent
    try:
        from agents.root import root_agent
        
        print("✅ Agent module imported successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to import agent: {e}")
        return False
    
    # Test 2: Root agent configuration
    print(f"📋 Agent Name: {root_agent.name}")
    print(f"   Model: {root_agent.model}")
    print(f"   Description: {root_agent.description[:60]}...")
    print()
    
    # Test 3: Tools
    print(f"🔧 Available Tools: {len(root_agent.tools)}")
    for tool in root_agent.tools:
        tool_name = tool.func.__name__ if hasattr(tool, 'func') else 'tool'
        print(f"   ✅ {tool_name}")
    print()
    
    # Test 5: API Key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print(f"✅ API Key configured (starts with: {api_key[:10]}...)")
    else:
        print("⚠️  API Key not configured - add to .env file")
    print()
    
    # Test 6: Check for images
    uploads_dir = 'uploads'
    if os.path.exists(uploads_dir):
        images = [f for f in os.listdir(uploads_dir) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
        print(f"📷 Found {len(images)} image(s) in uploads/")
        if images:
            for img in images[:3]:  # Show first 3
                print(f"   - {img}")
    else:
        print("⚠️  No uploads directory")
    print()
    
    print("=" * 50)
    print("✅ A2A Agent System Test Complete!")
    print()
    print("Next steps:")
    print("1. Upload image: curl -X POST -F 'image=@plant.jpg' http://localhost:5001/upload")
    print("2. Run agents: python run_agent.py")
    print("3. Or use web UI: adk web")
    print()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

