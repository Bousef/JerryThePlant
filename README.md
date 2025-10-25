# PlantAI Backend - Complete Plant Monitoring API

A comprehensive Flask backend service for receiving sensor data from Raspberry Pi, storing plant images, and providing AI-powered plant health analysis.

## Features

- **Sensor Data Processing**: Receive and analyze environmental sensor data (temperature, pressure, humidity, soil moisture)
- **Image Storage**: Upload and store plant images with metadata tracking
- **AI Health Analysis**: Generate intelligent responses based on sensor readings
- **Status Monitoring**: Color-coded status indicators (green/yellow/red)
- **Metrics Storage**: Optional storage for additional plant metrics
- **Local Storage**: Store all data locally with organized file structure

## Setup

1. **Create Virtual Environment** (Recommended for macOS)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend**
   
   **Option A: Use the startup script (recommended)**
   ```bash
   ./start.sh
   ```
   
   **Option B: Manual start**
   ```bash
   source venv/bin/activate
   python app.py
   ```

   The server will start on `http://localhost:5001`

## API Endpoints

### 1. Sensor Data (Main API)
- **POST** `/sensor-data`
- **Content-Type**: `application/json`
- **Body**: JSON with sensor readings
- **Response**: AI analysis and status color

**Example Request:**
```json
{
  "temperature": 22.5,
  "pressure": 1013.25,
  "humidity": 65.0,
  "soil_moisture": 45.0
}
```

**Example Response:**
```json
{
  "success": true,
  "message": "Sensor data received and processed",
  "response_body": {
    "ai_reply": "🌡️ Temperature looks comfortable for your plant. 💧 Humidity levels are good for plant health. 🌱 Soil moisture looks healthy.",
    "status_color": "green",
    "sensor_data_id": "123e4567-e89b-12d3-a456-426614174000",
    "timestamp": "2024-12-01T14:30:22.123456"
  }
}
```

### 2. Upload Image
- **POST** `/upload`
- **Content-Type**: `multipart/form-data`
- **Body**: `image` (file)
- **Response**: Image metadata including unique ID

### 3. Response Body
- **GET** `/response-body`
- **Response**: Latest AI response and status color

### 4. Metrics Storage (Optional)
- **POST** `/metrics`
- **Content-Type**: `application/json`
- **Body**: Custom metrics data
- **Response**: Storage confirmation

### 5. Home
- **GET** `/`
- **Response**: API information and available endpoints

## Testing

### Test Sensor Data API
```bash
python test_sensor_api.py
```

### Test Image Upload
```bash
python test_upload.py
```

## File Storage

Data is stored in the `uploads/` directory with the following structure:
```
uploads/
├── metadata.json          # Image metadata
├── sensor_data.json       # Sensor readings history
├── metrics.json          # Additional metrics
├── 20241201_143022_a1b2c3d4_plant.jpg
└── ...
```

## Configuration

- **Allowed file types**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
- **Max file size**: 16MB
- **Upload directory**: `uploads/`
- **Data retention**: Last 1000 sensor readings, 500 metrics entries

## AI Health Analysis

The system analyzes sensor data and provides:
- **Temperature analysis**: Comfortable (15-30°C), cool (<15°C), hot (>30°C)
- **Humidity analysis**: Good (30-80%), low (<30%), high (>80%)
- **Soil moisture analysis**: Healthy (20-80%), dry (<20%), wet (>80%)

## Status Colors

- **🟢 Green**: All sensor readings within healthy ranges
- **🟡 Yellow**: Some readings outside optimal ranges (warnings)
- **🔴 Red**: Critical readings requiring immediate attention

## Example Usage

### Send sensor data from Raspberry Pi:
```python
import requests
import json

sensor_data = {
    "temperature": 22.5,
    "pressure": 1013.25,
    "humidity": 65.0,
    "soil_moisture": 45.0
}

response = requests.post(
    'http://localhost:5001/sensor-data',
    json=sensor_data,
    headers={'Content-Type': 'application/json'}
)

result = response.json()
print(f"AI Reply: {result['response_body']['ai_reply']}")
print(f"Status: {result['response_body']['status_color']}")
```

### Upload an image:
```python
import requests

with open('plant_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5001/upload', files=files)
    print(response.json())
```

## Architecture Integration

This API integrates with:
- **Raspberry Pi**: Receives sensor data and images
- **Sense Hat**: Environmental sensors (temperature, pressure, humidity)
- **Soil Sensor**: Soil moisture readings
- **Pi Camera**: Plant image capture
- **TTS System**: Text-to-speech for AI responses
- **LED Control**: Status color indicators

## Next Steps

This backend is ready for integration with:
- Production database storage (PostgreSQL, MongoDB)
- Cloud storage (AWS S3, Google Cloud Storage)
- Advanced AI models for plant disease detection
- Real-time notifications and alerts
- User authentication and multi-plant support
