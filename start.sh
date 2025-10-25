#!/bin/bash
# PlantAI Backend Startup Script

echo "🌱 Starting PlantAI Backend..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Dependencies not installed. Installing now..."
    pip install -r requirements.txt
fi

echo "✅ Virtual environment activated"
echo "✅ Dependencies verified"
echo ""
echo "🚀 Starting Flask server on http://localhost:5001"
echo "📁 Upload directory: $(pwd)/uploads"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Start the Flask app
python app.py
