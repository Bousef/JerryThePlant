#!/usr/bin/env python3
"""
Simple test for PlantAI Image Storage API
"""

import requests
import os

# Backend URL
BASE_URL = "http://localhost:5001"

def test_upload_image(image_path):
    """Test uploading an image to the storage API"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    print(f"📤 Uploading image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload successful!")
            print(f"   Image ID: {data['image_id']}")
            print(f"   Filename: {data['filename']}")
            print(f"   Size: {data['file_size']} bytes")
            print(f"   Timestamp: {data['upload_timestamp']}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🌱 PlantAI Image Storage API Test")
    print("=" * 40)
    
    # Test image upload
    test_image_path = "test_image.jpg"  # Change this to your test image path
    
    if test_upload_image(test_image_path):
        print("\n🎉 Test completed successfully!")
        print("Your image has been stored locally in the 'uploads' directory.")
    else:
        print("\n💡 To test with your own image:")
        print("1. Place an image file in this directory")
        print("2. Update the 'test_image_path' variable in this script")
        print("3. Run: python test_upload.py")

if __name__ == "__main__":
    main()
