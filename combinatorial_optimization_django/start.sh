#!/bin/bash

echo "========================================"
echo "Combinatorial Optimization Framework"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Start server
echo "Starting development server..."
echo ""
echo "Application will be available at: http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
