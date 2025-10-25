#!/bin/bash
# Railway Deployment Script for PlantAI API

echo "🚀 Deploying PlantAI API to Railway"
echo "=================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
    echo "✅ Railway CLI installed"
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project
echo "🏗️  Initializing Railway project..."
railway init

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your API is now live at the URL shown above"
echo "📡 Test with: curl -X POST -F 'image=@test.jpg' <your-url>/upload"
