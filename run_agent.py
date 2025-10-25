#!/usr/bin/env python3
"""
Run the A2A plant identification agent system.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_setup():
    """Verify the setup is correct."""
    issues = []
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        issues.append("⚠️  GOOGLE_API_KEY not configured in .env")
        issues.append("   Get your key from: https://aistudio.google.com/apikey")
    
    # Check for images
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        issues.append("⚠️  No uploads directory found")
    else:
        images = [f for f in os.listdir(uploads_dir) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
        if not images:
            issues.append("⚠️  No images in uploads directory")
            issues.append("   Upload an image first: curl -X POST -F 'image=@plant.jpg' http://localhost:5001/upload")
    
    if issues:
        print("🌱 Plant Identification System - Setup Check")
        print("=" * 50)
        for issue in issues:
            print(issue)
        print("=" * 50)
        print("\nFix these issues before running the agent.")
        return False
    
    return True


def list_images():
    """List available images to analyze."""
    uploads_dir = 'uploads'
    images = [f for f in os.listdir(uploads_dir) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
    return images


def main():
    """Main entry point."""
    print("🌱 Jerry the Plant - AI Identification System")
    print("=" * 50)
    print()
    
    # Check setup
    if not check_setup():
        sys.exit(1)
    
    # Import agent
    try:
        from agents.root import root_agent
        print("✅ Agent system loaded successfully")
        print(f"   Agent: {root_agent.name}")
        print(f"   Model: {root_agent.model}")
        print(f"   Tools: {len(root_agent.tools)}")
        print()
    except Exception as e:
        print(f"❌ Failed to load agent: {e}")
        print("\nMake sure dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # List available images
    images = list_images()
    print(f"📷 Found {len(images)} image(s) in uploads:")
    for idx, img in enumerate(images, 1):
        print(f"   {idx}. {img}")
    print()
    
    # Get user selection
    try:
        choice = int(input("Select image number (or 0 to exit): "))
        if choice == 0:
            print("Exiting...")
            return
        if 1 <= choice <= len(images):
            image_path = images[choice - 1]
            print(f"\n🔍 Analyzing: {image_path}")
            print("=" * 50)
            print()
            
            # Run the multi-agent system
            prompt = f"Please analyze this plant image: uploads/{image_path}"
            print(f"💬 User: {prompt}\n")
            
            response = root_agent.run(prompt)
            
            print(f"🤖 System Response:")
            print("=" * 50)
            print(response)
            print("=" * 50)
            
        else:
            print("❌ Invalid selection")
    except (ValueError, KeyboardInterrupt):
        print("\nExiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis might be an API or configuration issue.")
        print("Check that your GOOGLE_API_KEY is valid.")


if __name__ == "__main__":
    main()

