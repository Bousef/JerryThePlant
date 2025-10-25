import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import Supabase dependencies
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase dependencies not installed. Install with: pip install supabase postgrest")

class SupabaseStorage:
    def __init__(self):
        """Initialize Supabase Storage and Database"""
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_ANON_KEY')
        self.supabase_service_key = os.environ.get('SUPABASE_SERVICE_KEY')
        self.database_url = os.environ.get('DATABASE_URL')
        
        self.client = None
        self.initialized = False
        
        if not SUPABASE_AVAILABLE:
            print("⚠️  Supabase dependencies not available, using local storage")
            return
            
        if not self.supabase_url or not self.supabase_key:
            print("⚠️  Supabase credentials not set, using local storage")
            print("💡 Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
            return
            
        try:
            # Initialize Supabase client
            self.client = create_client(self.supabase_url, self.supabase_key)
            self.initialized = True
            print(f"✅ Supabase initialized successfully!")
            print(f"🔗 URL: {self.supabase_url}")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            print(f"❌ Supabase initialization failed: {e}")
            print("⚠️  Falling back to local storage")
    
    def _test_connection(self):
        """Test Supabase connection"""
        try:
            # Try to query a simple table or create test table
            result = self.client.table('plant_images').select('*').limit(1).execute()
            print("✅ Supabase connection test successful")
        except Exception as e:
            print(f"⚠️  Supabase connection test failed: {e}")
            print("💡 This is normal if tables don't exist yet")
    
    def upload_image(self, file_data, filename, content_type):
        """Upload image to Supabase Storage"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return None
            
        try:
            # Upload to Supabase Storage
            bucket_name = "plant-images"
            file_path = f"uploads/{filename}"
            
            # Upload file to storage
            result = self.client.storage.from_(bucket_name).upload(
                file_path, 
                file_data,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_path)
            
            print(f"✅ Image uploaded to Supabase: {public_url}")
            return {
                'url': public_url,
                'file_path': file_path,
                'bucket': bucket_name
            }
            
        except Exception as e:
            print(f"❌ Supabase upload failed: {e}")
            return None
    
    def delete_image(self, file_path):
        """Delete image from Supabase Storage"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return False
            
        try:
            bucket_name = "plant-images"
            result = self.client.storage.from_(bucket_name).remove([file_path])
            print(f"✅ Image deleted from Supabase: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Supabase delete failed: {e}")
            return False
    
    def get_image_url(self, file_path):
        """Get public URL for an image"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return None
            
        try:
            bucket_name = "plant-images"
            return self.client.storage.from_(bucket_name).get_public_url(file_path)
        except Exception as e:
            print(f"❌ Failed to get image URL: {e}")
            return None
    
    def save_sensor_data(self, sensor_data):
        """Save sensor data to Supabase database"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return None
            
        try:
            # Insert sensor data into database
            result = self.client.table('sensor_readings').insert(sensor_data).execute()
            print(f"✅ Sensor data saved to Supabase: {result.data}")
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Failed to save sensor data: {e}")
            return None
    
    def get_latest_sensor_data(self):
        """Get latest sensor data from Supabase"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return None
            
        try:
            result = self.client.table('sensor_readings').select('*').order('created_at', desc=True).limit(1).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Failed to get sensor data: {e}")
            return None
    
    def save_image_metadata(self, metadata):
        """Save image metadata to Supabase database"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return None
            
        try:
            result = self.client.table('plant_images').insert(metadata).execute()
            print(f"✅ Image metadata saved to Supabase: {result.data}")
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Failed to save image metadata: {e}")
            return None
    
    def get_images(self):
        """Get all images from Supabase"""
        if not self.initialized or not SUPABASE_AVAILABLE:
            return []
            
        try:
            result = self.client.table('plant_images').select('*').order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"❌ Failed to get images: {e}")
            return []

# Global Supabase instance
supabase_storage = SupabaseStorage()
