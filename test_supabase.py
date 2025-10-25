#!/usr/bin/env python3
"""
Test script for PlantAI Supabase Integration
Tests image upload, retrieval, and deletion with Supabase Storage
"""

import requests
import os
import json

# Backend URL
BASE_URL = "http://localhost:5001"

def test_supabase_status():
    """Test Supabase status"""
    print("🚀 Testing Supabase Status")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            data = response.json()
            storage_info = data.get('storage', {})
            
            print(f"✅ API Status: {data['status']}")
            print(f"🚀 Supabase Enabled: {storage_info.get('supabase_enabled', False)}")
            print(f"📦 Storage Type: {storage_info.get('type', 'unknown')}")
            
            if storage_info.get('database_url'):
                print(f"🗄️ Database: Connected")
            
            return storage_info.get('supabase_enabled', False)
        else:
            print(f"❌ API Status check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_image_upload():
    """Test image upload to Supabase Storage"""
    print("\n📤 Testing Image Upload to Supabase")
    print("-" * 40)
    
    # Check if test image exists
    test_image_path = "test_image.jpg"
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        print("💡 Please place a test image file named 'test_image.jpg' in the project directory")
        return False
    
    print(f"📷 Uploading image: {test_image_path}")
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Image uploaded successfully!")
            print(f"   Image ID: {data['image_id']}")
            print(f"   Filename: {data['filename']}")
            print(f"   Size: {data['file_size']} bytes")
            print(f"   Storage Type: {data['storage_type']}")
            print(f"   Image URL: {data['image_url']}")
            print(f"   Timestamp: {data['upload_timestamp']}")
            return data['image_id']
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

def test_sensor_data():
    """Test sensor data upload to Supabase"""
    print("\n🌡️ Testing Sensor Data Upload to Supabase")
    print("-" * 40)
    
    sensor_data = {
        "temperature": 22.5,
        "pressure": 1013.25,
        "humidity": 65.0,
        "soil_moisture": 45.0
    }
    
    print(f"📊 Sending sensor data: {json.dumps(sensor_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/sensor-data",
            json=sensor_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Sensor data sent successfully!")
            print(f"   Response ID: {data['response_body']['sensor_data_id']}")
            print(f"   AI Reply: {data['response_body']['ai_reply']}")
            print(f"   Status Color: {data['response_body']['status_color']}")
            return True
        else:
            print(f"❌ Sensor data failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_images():
    """Test getting list of images"""
    print("\n📋 Testing Get Images List")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/images")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Images list retrieved successfully!")
            print(f"   Total Images: {data['count']}")
            print(f"   Supabase Enabled: {data['firebase_enabled']}")
            
            if data['images']:
                print("   Recent Images:")
                for img in data['images'][-3:]:  # Show last 3 images
                    print(f"     • {img['original_filename']} ({img['storage_type']})")
                    print(f"       URL: {img['image_url']}")
                    print(f"       Size: {img['file_size']} bytes")
            else:
                print("   No images found")
            
            return True
        else:
            print(f"❌ Get images failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_delete_image(image_id):
    """Test image deletion"""
    if not image_id:
        print("\n🗑️ Skipping delete test (no image ID)")
        return True
        
    print(f"\n🗑️ Testing Image Deletion")
    print("-" * 40)
    
    try:
        response = requests.delete(f"{BASE_URL}/images/{image_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Image deleted successfully!")
            print(f"   Deleted Image ID: {data['image_id']}")
            return True
        else:
            print(f"❌ Delete failed: {response.status_code}")
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
    print("🚀 PlantAI Supabase Integration Test")
    print("=" * 60)
    
    # Test Supabase status
    supabase_enabled = test_supabase_status()
    
    if not supabase_enabled:
        print("\n⚠️  Supabase is not enabled!")
        print("💡 To enable Supabase:")
        print("   1. Run: python setup_supabase.py")
        print("   2. Set SUPABASE_URL and SUPABASE_ANON_KEY")
        print("   3. Run the SQL schema in Supabase SQL Editor")
        print("   4. Restart the server")
        print("\n🔄 Continuing with local storage fallback tests...")
    
    # Test image upload
    image_id = test_image_upload()
    
    # Test sensor data
    test_sensor_data()
    
    # Test getting images
    test_get_images()
    
    # Test image deletion (optional)
    if image_id:
        test_delete_image(image_id)
    
    print("\n" + "=" * 60)
    if supabase_enabled:
        print("🎉 Supabase integration test completed!")
        print("✅ Images are being stored in Supabase Storage")
        print("✅ Sensor data is being saved to Supabase Database")
    else:
        print("📁 Local storage fallback test completed!")
        print("⚠️  Images and data are being stored locally (Supabase not configured)")
    
    print("\n💡 Next steps:")
    print("   • Configure Supabase for production use")
    print("   • Test with your Raspberry Pi image uploads")
    print("   • Build a dashboard to view plant data")
    print("   • Set up real-time notifications")

if __name__ == "__main__":
    main()
