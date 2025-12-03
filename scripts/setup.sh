#!/bin/bash

# HomeStock Setup Script
echo "🚀 Setting up HomeStock..."

# Check Python version
echo "📦 Checking Python..."
python3 --version || { echo "❌ Python 3.10+ required"; exit 1; }

# Check Node version
echo "📦 Checking Node.js..."
node --version || { echo "❌ Node.js 20+ required"; exit 1; }

# Setup Python backend
echo "🐍 Setting up Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

# Setup Node frontend
echo "📱 Setting up Node.js frontend..."
npm install

echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  npm start"
echo ""
echo "To build for distribution:"
echo "  npm run build:mac    # For Mac"
echo "  npm run build:win    # For Windows"

