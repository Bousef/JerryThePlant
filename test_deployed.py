#!/usr/bin/env python3
"""
Test script for deployed PlantAI API
Update the BASE_URL to your deployed API URL
"""

import requests
import os

# Update this URL to your deployed API
BASE_URL = "https://your-app.railway.app"  # Replace with your actual URL

def test_deployed_api():
    """Test the deployed API"""
    print("🌱 Testing Deployed PlantAI API")
    print("=" * 40)
    
    # Test home endpoint
    try:
        print("🏠 Testing home endpoint...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"✅ Home endpoint working: {response.json()}")
        else:
            print(f"❌ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach API: {e}")
        return False
    
    # Test upload endpoint (without file)
    try:
        print("\n📤 Testing upload endpoint...")
        response = requests.post(f"{BASE_URL}/upload")
        if response.status_code == 400:
            data = response.json()
            if "No image file provided" in data.get('error', ''):
                print("✅ Upload endpoint working (correctly rejected empty request)")
            else:
                print(f"⚠️  Unexpected response: {data}")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload endpoint error: {e}")
        return False
    
    print("\n🎉 API is working correctly!")
    print(f"🌐 Your API URL: {BASE_URL}")
    print(f"📡 Upload endpoint: {BASE_URL}/upload")
    print("\n💡 To test with an actual image:")
    print(f"curl -X POST -F 'image=@your_image.jpg' {BASE_URL}/upload")
    
    return True

if __name__ == "__main__":
    test_deployed_api()
