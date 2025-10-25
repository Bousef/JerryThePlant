#!/usr/bin/env python3
"""
Supabase Setup Helper for PlantAI
This script helps you configure Supabase for your PlantAI project
"""

import os
import sys

def create_env_file():
    """Create .env file with Supabase configuration"""
    print("🚀 Supabase Setup for PlantAI")
    print("=" * 40)
    
    # Get Supabase project details
    supabase_url = input("Enter your Supabase URL (e.g., https://xyz.supabase.co): ").strip()
    if not supabase_url:
        print("❌ Supabase URL is required!")
        return False
    
    supabase_key = input("Enter your Supabase Anon Key: ").strip()
    if not supabase_key:
        print("❌ Supabase Anon Key is required!")
        return False
    
    database_url = input("Enter your Database URL (optional): ").strip()
    
    env_content = f"""# Supabase Configuration for PlantAI
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={supabase_key}
"""
    
    if database_url:
        env_content += f"DATABASE_URL={database_url}\n"
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🧪 Testing Supabase connection...")
    
    try:
        from supabase_config import supabase_storage
        
        if supabase_storage.initialized:
            print("✅ Supabase initialized successfully!")
            print(f"🚀 URL: {supabase_storage.supabase_url}")
            return True
        else:
            print("❌ Supabase failed to initialize")
            print("💡 Check your .env file and Supabase credentials")
            return False
            
    except Exception as e:
        print(f"❌ Supabase test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🌱 PlantAI Supabase Setup")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("📁 Using existing .env file")
        else:
            if not create_env_file():
                return
    
    # Test Supabase connection
    if test_supabase_connection():
        print("\n🎉 Supabase setup complete!")
        print("\n📋 Next steps:")
        print("1. Run the SQL schema in Supabase SQL Editor:")
        print("   - Copy contents of supabase_schema.sql")
        print("   - Paste in Supabase Dashboard > SQL Editor")
        print("   - Click 'Run'")
        print("2. Restart your Flask server: python app.py")
        print("3. Test image upload: python test_supabase.py")
        print("4. Your Raspberry Pi can now upload images to Supabase!")
    else:
        print("\n❌ Supabase setup failed")
        print("💡 Please check your Supabase project configuration")

if __name__ == "__main__":
    main()
