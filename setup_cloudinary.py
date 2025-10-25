#!/usr/bin/env python3
"""
Cloudinary Setup Script for PlantAI API
This script helps you test Cloudinary integration locally
"""

import os
from dotenv import load_dotenv

def setup_cloudinary():
    """Setup Cloudinary environment variables"""
    print("☁️  Cloudinary Setup for PlantAI API")
    print("=" * 40)
    
    # Load .env file if it exists
    load_dotenv()
    
    # Check if credentials are already set
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    if cloud_name and api_key and api_secret:
        print("✅ Cloudinary credentials found!")
        print(f"   Cloud Name: {cloud_name}")
        print(f"   API Key: {api_key[:8]}...")
        print("   API Secret: [HIDDEN]")
        return True
    
    print("❌ Cloudinary credentials not found!")
    print("\n📋 To get your credentials:")
    print("1. Sign up at https://cloudinary.com")
    print("2. Go to Dashboard")
    print("3. Copy your Cloud Name, API Key, and API Secret")
    print("\n🔧 To set them locally:")
    print("Create a .env file with:")
    print("CLOUDINARY_CLOUD_NAME=your_cloud_name")
    print("CLOUDINARY_API_KEY=your_api_key")
    print("CLOUDINARY_API_SECRET=your_api_secret")
    
    return False

def test_cloudinary():
    """Test Cloudinary connection"""
    try:
        import cloudinary
        from cloudinary import uploader
        
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET')
        )
        
        # Test connection
        result = uploader.upload("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", 
                               public_id="test_connection")
        
        print("✅ Cloudinary connection successful!")
        print(f"   Test image URL: {result['secure_url']}")
        
        # Clean up test image
        uploader.destroy("test_connection")
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Cloudinary test failed: {e}")
        return False

if __name__ == "__main__":
    if setup_cloudinary():
        test_cloudinary()
    else:
        print("\n💡 After setting up credentials, run this script again to test!")
