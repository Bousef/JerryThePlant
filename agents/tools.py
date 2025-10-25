"""
Shared tools for plant identification agents.
"""
import os
from PIL import Image
from google.adk.tools import FunctionTool


def load_image(image_path: str) -> str:
    """Load and validate a plant image file.
    
    This tool loads an image file from the uploads directory and verifies
    it's a valid image that can be analyzed. Returns information about
    the image including size, format, and path.
    
    Args:
        image_path: Path to the image file (can be relative to uploads/ or absolute)
        
    Returns:
        Image information and status
    """
    # Handle relative paths
    if not image_path.startswith('/'):
        # Try uploads directory first
        test_path = os.path.join('uploads', image_path)
        if os.path.exists(test_path):
            image_path = test_path
    
    # Verify the image exists
    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"
    
    try:
        # Open and verify the image is valid
        with Image.open(image_path) as img:
            info = {
                'path': os.path.abspath(image_path),
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'status': 'valid'
            }
            return f"Image loaded: {info['path']}\nSize: {info['size']}\nFormat: {info['format']}\nReady for analysis."
    except Exception as e:
        return f"Error loading image: {str(e)}"


def get_image_metadata(image_path: str) -> str:
    """Get detailed metadata about an uploaded plant image.
    
    Retrieves metadata including upload timestamp, original filename,
    and file information from the metadata.json file.
    
    Args:
        image_path: Path or filename of the image
        
    Returns:
        Metadata information as a formatted string
    """
    import json
    
    # Extract filename
    filename = os.path.basename(image_path)
    
    # Load metadata
    metadata_file = 'uploads/metadata.json'
    if not os.path.exists(metadata_file):
        return "No metadata file found"
    
    try:
        with open(metadata_file, 'r') as f:
            all_metadata = json.load(f)
        
        # Find matching metadata
        for meta in all_metadata:
            if filename in meta.get('stored_path', ''):
                return (
                    f"Image Metadata:\n"
                    f"- Original filename: {meta.get('original_filename')}\n"
                    f"- Upload time: {meta.get('upload_timestamp')}\n"
                    f"- File size: {meta.get('file_size')} bytes\n"
                    f"- File type: {meta.get('file_type')}"
                )
        
        return "Metadata not found for this image"
    except Exception as e:
        return f"Error reading metadata: {str(e)}"


# Create tool instances
load_image_tool = FunctionTool(func=load_image)
get_metadata_tool = FunctionTool(func=get_image_metadata)

