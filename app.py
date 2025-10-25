from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json

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

if __name__ == '__main__':
    print(f"🌱 PlantAI Backend - Image Storage API")
    print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"📷 Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"📏 Max file size: {MAX_FILE_SIZE // (1024 * 1024)}MB")
    print(f"🚀 Server starting on http://localhost:5001")
    print(f"📡 API endpoint: POST /upload")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5001)