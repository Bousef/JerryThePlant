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
    
    # Your Cloudinary credentials
    cloud_name = "dzgjbemkz"
    api_key = "464178279928238"
    api_secret = "luIssqwibXD6faIl_9d1WECar5k"
    
    # Set environment variables
    os.environ['CLOUDINARY_URL'] = f"cloudinary://{api_key}:{api_secret}@{cloud_name}"
    os.environ['CLOUDINARY_CLOUD_NAME'] = cloud_name
    os.environ['CLOUDINARY_API_KEY'] = api_key
    os.environ['CLOUDINARY_API_SECRET'] = api_secret
    
    print("✅ Cloudinary credentials set!")
    print(f"   Cloud Name: {cloud_name}")
    print(f"   API Key: {api_key}")
    print(f"   API Secret: {api_secret[:8]}...")
    print(f"   CLOUDINARY_URL: cloudinary://{api_key}:{api_secret}@{cloud_name}")
    
    return True

def test_cloudinary():
    """Test Cloudinary connection"""
    try:
        import cloudinary
        from cloudinary import uploader
        
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
        print("\n🚀 Ready for Vercel deployment!")
        print("Environment variables to set in Vercel:")
        print("CLOUDINARY_URL=cloudinary://464178279928238:luIssqwibXD6faIl_9d1WECar5k@dzgjbemkz")
