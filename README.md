# PlantAI Backend - Image Storage API

A simple Flask backend service for receiving and storing plant images locally.

## Features

- **Single API**: One endpoint to upload and store images
- **Local Storage**: Store images in organized directory structure  
- **File Validation**: Validate file types and sizes
- **Metadata Tracking**: Track image information and upload timestamps

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

## Troubleshooting

If you get an "externally-managed-environment" error on macOS:
- Use the virtual environment approach above
- Or use: `pip install --break-system-packages -r requirements.txt` (not recommended)

## API Endpoint

### Upload Image
- **POST** `/upload`
- **Content-Type**: `multipart/form-data`
- **Body**: `image` (file)
- **Response**: Image metadata including unique ID

**Example Response:**
```json
{
  "success": true,
  "message": "Image uploaded successfully",
  "image_id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "20241201_143022_a1b2c3d4_plant.jpg",
  "original_filename": "plant.jpg",
  "file_size": 245760,
  "upload_timestamp": "2024-12-01T14:30:22.123456"
}
```

## File Storage

Images are stored in the `uploads/` directory with the following structure:
```
uploads/
├── metadata.json          # Image metadata
├── 20241201_143022_a1b2c3d4_plant.jpg
├── 20241201_143045_e5f6g7h8_leaf.png
└── ...
```

## Configuration

- **Allowed file types**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
- **Max file size**: 16MB
- **Upload directory**: `uploads/`

## Testing

Run the simple test script to verify functionality:
```bash
python test_upload.py
```

Make sure to place a test image file named `test_image.jpg` in the project directory before running tests.

## Example Usage

### Upload an image using curl:
```bash
curl -X POST -F "image=@your_plant_image.jpg" http://localhost:5001/upload
```

### Upload an image using Python:
```python
import requests

with open('plant_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5001/upload', files=files)
    print(response.json())
```

## Next Steps

This backend is ready for integration with:
- Plant identification AI models
- Image preprocessing pipelines
- Database storage for production use
- Authentication and user management
