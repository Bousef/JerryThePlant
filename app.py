from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import uuid
from datetime import datetime
import os

app = Flask(__name__)

# Cloudinary configuration
# Use CLOUDINARY_URL (recommended for Vercel)
cloudinary_url = os.environ.get('CLOUDINARY_URL')
if cloudinary_url:
    cloudinary.config(cloudinary_url=cloudinary_url)
    print("✅ Cloudinary configured with CLOUDINARY_URL")
else:
    # Fallback to individual variables (for local development)
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    if cloud_name and api_key and api_secret:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print("✅ Cloudinary configured with individual variables")
    else:
        print("⚠️  Warning: Cloudinary credentials not found!")
        print("   Set CLOUDINARY_URL environment variable")

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_metadata(image_url, original_filename, file_size, public_id):
    """Save metadata about the uploaded image"""
    metadata = {
        'id': str(uuid.uuid4()),
        'original_filename': original_filename,
        'image_url': image_url,
        'public_id': public_id,
        'file_size': file_size,
        'upload_timestamp': datetime.now().isoformat(),
        'file_type': original_filename.rsplit('.', 1)[1].lower(),
        'storage': 'cloudinary'
    }
    
    # In a real app, you'd save this to a database
    # For demo purposes, we'll just return it
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
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"plantai_{timestamp}_{uuid.uuid4().hex[:8]}"
        
        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                public_id=unique_filename,
                folder="plantai",
                resource_type="image"
            )
            
            # Save metadata
            metadata = save_image_metadata(
                upload_result['secure_url'],
                file.filename,
                file_size,
                upload_result['public_id']
            )
            
            return jsonify({
                'success': True,
                'message': 'Image uploaded successfully',
                'image_id': metadata['id'],
                'image_url': upload_result['secure_url'],
                'public_id': upload_result['public_id'],
                'original_filename': file.filename,
                'file_size': file_size,
                'upload_timestamp': metadata['upload_timestamp'],
                'storage': 'cloudinary'
            }), 200
            
        except Exception as cloudinary_error:
            return jsonify({
                'error': f'Cloudinary upload failed: {str(cloudinary_error)}'
            }), 500
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple home endpoint"""
    return jsonify({
        'service': 'PlantAI Image Storage API',
        'status': 'running',
        'endpoint': '/upload',
        'method': 'POST',
        'storage': 'Cloudinary',
        'timestamp': datetime.now().isoformat()
    })

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🌱 PlantAI Backend - Image Storage API (Vercel)")
    print(f"📷 Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"📏 Max file size: {MAX_FILE_SIZE // (1024 * 1024)}MB")
    print(f"☁️  Storage: Cloudinary")
    print(f"🚀 Server starting on port {port}")
    print(f"📡 API endpoint: POST /upload")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=port)