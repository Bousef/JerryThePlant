#!/usr/bin/env python3
"""
Test script for PlantAI Sensor Data API
Tests the new sensor data endpoints
"""

import requests
import json
import random
import time

# Backend URL
BASE_URL = "http://localhost:5001"

def test_sensor_data_api():
    """Test the sensor data API endpoint"""
    print("🌡️ Testing Sensor Data API")
    print("-" * 30)
    
    # Generate realistic sensor data
    sensor_data = {
        "temperature": round(random.uniform(15, 30), 2),  # Celsius
        "pressure": round(random.uniform(950, 1050), 2),  # Hectopascals
        "humidity": round(random.uniform(20, 80), 2),     # Percent
        "soil_moisture": round(random.uniform(10, 90), 2) # Percent
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

def test_response_body_api():
    """Test the response body API endpoint"""
    print("\n🤖 Testing Response Body API")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/response-body")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response body retrieved successfully!")
            print(f"   AI Reply: {data['ai_reply']}")
            print(f"   Status Color: {data['status_color']}")
            print(f"   Sensor Readings:")
            for sensor, value in data['sensor_readings'].items():
                print(f"     • {sensor}: {value}")
            return True
        else:
            print(f"❌ Response body failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics_api():
    """Test the metrics storage API endpoint"""
    print("\n📈 Testing Metrics API")
    print("-" * 30)
    
    metrics_data = {
        "metrics": {
            "plant_growth_rate": round(random.uniform(0.1, 2.0), 2),
            "leaf_count": random.randint(5, 25),
            "health_score": round(random.uniform(60, 100), 1),
            "days_since_watering": random.randint(1, 7)
        }
    }
    
    print(f"📊 Sending metrics: {json.dumps(metrics_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/metrics",
            json=metrics_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Metrics stored successfully!")
            print(f"   Metrics ID: {data['metrics_id']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Metrics storage failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_home_endpoint():
    """Test the home endpoint to see all available APIs"""
    print("\n🏠 Testing Home Endpoint")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Home endpoint working!")
            print(f"   Service: {data['service']}")
            print(f"   Status: {data['status']}")
            print("   Available endpoints:")
            for endpoint_name, endpoint_info in data['endpoints'].items():
                print(f"     • {endpoint_info['method']} {endpoint_info['path']} - {endpoint_info['description']}")
            return True
        else:
            print(f"❌ Home endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🌱 PlantAI Complete API Test Suite")
    print("=" * 50)
    
    # Test all endpoints
    tests = [
        ("Home Endpoint", test_home_endpoint),
        ("Sensor Data API", test_sensor_data_api),
        ("Response Body API", test_response_body_api),
        ("Metrics API", test_metrics_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your PlantAI API is working perfectly.")
    else:
        print("💡 Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
