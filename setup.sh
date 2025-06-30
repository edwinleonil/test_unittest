#!/bin/bash

echo "PyTorch ResNet50 Image Classifier - Setup Script"
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

echo
echo "Setting up virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment"
    exit 1
fi

echo
echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo
echo "Running demo script..."
python demo.py

echo
echo "Setup complete! To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python main.py"
echo "  3. Run tests: pytest"
