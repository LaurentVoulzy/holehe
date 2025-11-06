#!/bin/bash

# Marketing Research AI - Startup Script
# For MachinePoem.agency

echo "🎯 Starting Marketing Research AI..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed" ]; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
    touch venv/installed
    echo "✅ Requirements installed"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "❗ Please edit .env and add your API keys before continuing"
    echo "   Required: ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Start the app
echo ""
echo "🚀 Launching Streamlit app..."
echo ""
streamlit run app.py
