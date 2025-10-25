from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json
import random

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_metadata(image_path, original_filename, file_size):
    """Save metadata about the uploaded image"""
    metadata = {
        'id': str(uuid.uuid4()),
        'original_filename': original_filename,
        'stored_path': image_path,
        'file_size': file_size,
        'upload_timestamp': datetime.now().isoformat(),
        'file_type': original_filename.rsplit('.', 1)[1].lower()
    }
    
    metadata_file = os.path.join(UPLOAD_FOLDER, 'metadata.json')
    
    # Load existing metadata or create new list
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            all_metadata = json.load(f)
    else:
        all_metadata = []
    
    # Add new metadata
    all_metadata.append(metadata)
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(all_metadata, f, indent=2)
    
    return metadata

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload requests - THE MAIN API"""
    try:
        # Check if file is present in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'File type not allowed',
                'allowed_types': list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'error': 'File too large',
                'max_size_mb': MAX_FILE_SIZE // (1024 * 1024)
            }), 400
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{filename}"
        
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Save metadata
        metadata = save_image_metadata(file_path, file.filename, file_size)
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_id': metadata['id'],
            'filename': unique_filename,
            'original_filename': file.filename,
            'file_size': file_size,
            'upload_timestamp': metadata['upload_timestamp']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Handle sensor data from Raspberry Pi - THE MAIN SENSOR API"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required sensor fields
        required_fields = ['temperature', 'pressure', 'humidity', 'soil_moisture']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400
        
        # Validate data types and ranges
        try:
            temperature = float(data['temperature'])
            pressure = float(data['pressure'])
            humidity = float(data['humidity'])
            soil_moisture = float(data['soil_moisture'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid data types. All sensor values must be numbers.'}), 400
        
        # Add timestamp and unique ID
        sensor_data = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'source': 'raspberry_pi'
        }
        
        # Store sensor data locally (in production, this would go to a database)
        sensor_file = os.path.join(UPLOAD_FOLDER, 'sensor_data.json')
        
        # Load existing sensor data or create new list
        if os.path.exists(sensor_file):
            with open(sensor_file, 'r') as f:
                all_sensor_data = json.load(f)
        else:
            all_sensor_data = []
        
        # Add new sensor data
        all_sensor_data.append(sensor_data)
        
        # Keep only last 1000 readings to prevent file from growing too large
        if len(all_sensor_data) > 1000:
            all_sensor_data = all_sensor_data[-1000:]
        
        # Save updated sensor data
        with open(sensor_file, 'w') as f:
            json.dump(all_sensor_data, f, indent=2)
        
        # Generate AI response and status
        ai_response = generate_ai_response(sensor_data)
        status_color = determine_status_color(sensor_data)
        
        response_body = {
            'ai_reply': ai_response,
            'status_color': status_color,
            'sensor_data_id': sensor_data['id'],
            'timestamp': sensor_data['timestamp']
        }
        
        return jsonify({
            'success': True,
            'message': 'Sensor data received and processed',
            'response_body': response_body
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Sensor data processing failed: {str(e)}'}), 500

def generate_ai_response(sensor_data):
    """Generate AI-like response based on sensor data"""
    temp = sensor_data['temperature']
    humidity = sensor_data['humidity']
    soil_moisture = sensor_data['soil_moisture']
    
    responses = []
    
    # Temperature analysis
    if temp < 15:
        responses.append("🌡️ Temperature is quite cool - consider moving to a warmer spot.")
    elif temp > 30:
        responses.append("🌡️ Temperature is getting hot - ensure adequate ventilation.")
    else:
        responses.append("🌡️ Temperature looks comfortable for your plant.")
    
    # Humidity analysis
    if humidity < 30:
        responses.append("💧 Humidity is low - consider misting or using a humidifier.")
    elif humidity > 80:
        responses.append("💧 Humidity is very high - ensure good air circulation.")
    else:
        responses.append("💧 Humidity levels are good for plant health.")
    
    # Soil moisture analysis
    if soil_moisture < 20:
        responses.append("🌱 Soil is quite dry - time to water your plant!")
    elif soil_moisture > 80:
        responses.append("🌱 Soil is very wet - be careful not to overwater.")
    else:
        responses.append("🌱 Soil moisture looks healthy.")
    
    return " ".join(responses)

def determine_status_color(sensor_data):
    """Determine status color based on sensor readings"""
    temp = sensor_data['temperature']
    humidity = sensor_data['humidity']
    soil_moisture = sensor_data['soil_moisture']
    
    # Count issues
    issues = 0
    
    if temp < 10 or temp > 35:
        issues += 2  # Critical temperature
    elif temp < 15 or temp > 30:
        issues += 1  # Warning temperature
    
    if humidity < 20 or humidity > 90:
        issues += 2  # Critical humidity
    elif humidity < 30 or humidity > 80:
        issues += 1  # Warning humidity
    
    if soil_moisture < 10 or soil_moisture > 90:
        issues += 2  # Critical soil moisture
    elif soil_moisture < 20 or soil_moisture > 80:
        issues += 1  # Warning soil moisture
    
    # Determine color based on total issues
    if issues >= 4:
        return "red"    # Critical issues
    elif issues >= 2:
        return "yellow" # Warning issues
    else:
        return "green"  # All good

@app.route('/metrics', methods=['POST'])
def store_metrics():
    """Optional endpoint to store metrics in database/S3 bucket"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No metrics data provided'}), 400
        
        # Validate metrics data structure
        if 'metrics' not in data:
            return jsonify({'error': 'Missing metrics field'}), 400
        
        metrics = data['metrics']
        
        # Add metadata
        metrics_data = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'source': 'api_request'
        }
        
        # Store metrics locally (in production, this would go to S3 or database)
        metrics_file = os.path.join(UPLOAD_FOLDER, 'metrics.json')
        
        # Load existing metrics or create new list
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                all_metrics = json.load(f)
        else:
            all_metrics = []
        
        # Add new metrics
        all_metrics.append(metrics_data)
        
        # Keep only last 500 entries to prevent file from growing too large
        if len(all_metrics) > 500:
            all_metrics = all_metrics[-500:]
        
        # Save updated metrics
        with open(metrics_file, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Metrics stored successfully',
            'metrics_id': metrics_data['id'],
            'timestamp': metrics_data['timestamp']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Metrics storage failed: {str(e)}'}), 500

@app.route('/response-body', methods=['GET'])
def get_response_body():
    """Get the latest response body with AI reply and status color"""
    try:
        # Get the latest sensor data
        sensor_file = os.path.join(UPLOAD_FOLDER, 'sensor_data.json')
        
        if not os.path.exists(sensor_file):
            return jsonify({
                'error': 'No sensor data available',
                'ai_reply': 'No recent sensor data to analyze.',
                'status_color': 'yellow'
            }), 404
        
        with open(sensor_file, 'r') as f:
            all_sensor_data = json.load(f)
        
        if not all_sensor_data:
            return jsonify({
                'error': 'No sensor data available',
                'ai_reply': 'No recent sensor data to analyze.',
                'status_color': 'yellow'
            }), 404
        
        # Get the most recent sensor reading
        latest_sensor_data = all_sensor_data[-1]
        
        # Generate AI response and status
        ai_response = generate_ai_response(latest_sensor_data)
        status_color = determine_status_color(latest_sensor_data)
        
        response_body = {
            'ai_reply': ai_response,
            'status_color': status_color,
            'sensor_data_id': latest_sensor_data['id'],
            'timestamp': latest_sensor_data['timestamp'],
            'sensor_readings': {
                'temperature': latest_sensor_data['temperature'],
                'pressure': latest_sensor_data['pressure'],
                'humidity': latest_sensor_data['humidity'],
                'soil_moisture': latest_sensor_data['soil_moisture']
            }
        }
        
        return jsonify(response_body), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get response body: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple home endpoint"""
    return jsonify({
        'service': 'PlantAI Backend API',
        'status': 'running',
        'endpoints': {
            'upload_image': {
                'path': '/upload',
                'method': 'POST',
                'description': 'Upload plant images'
            },
            'sensor_data': {
                'path': '/sensor-data',
                'method': 'POST',
                'description': 'Receive sensor data from Raspberry Pi'
            },
            'metrics': {
                'path': '/metrics',
                'method': 'POST',
                'description': 'Store additional metrics (optional)'
            },
            'response_body': {
                'path': '/response-body',
                'method': 'GET',
                'description': 'Get latest AI response and status'
            }
        },
        'storage': 'local',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🌱 PlantAI Backend - Complete Plant Monitoring API")
    print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"📷 Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"📏 Max file size: {MAX_FILE_SIZE // (1024 * 1024)}MB")
    print(f"☁️  Storage: Local")
    print(f"🚀 Server starting on port {port}")
    print(f"📡 API endpoints:")
    print(f"   • POST /upload - Upload plant images")
    print(f"   • POST /sensor-data - Receive sensor data from Pi")
    print(f"   • POST /metrics - Store additional metrics")
    print(f"   • GET /response-body - Get AI response and status")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=port)