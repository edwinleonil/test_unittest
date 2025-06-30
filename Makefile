# Makefile for PyTorch ResNet50 Image Classifier

.PHONY: help install test lint format clean run demo setup

# Default target
help:
	@echo "PyTorch ResNet50 Image Classifier - Available Commands"
	@echo "====================================================="
	@echo ""
	@echo "setup     - Set up virtual environment and install dependencies"
	@echo "install   - Install dependencies"
	@echo "test      - Run all tests with coverage"
	@echo "lint      - Run code linting with flake8"
	@echo "format    - Format code with black"
	@echo "clean     - Clean up generated files"
	@echo "run       - Run the main application"
	@echo "demo      - Run the demo script"
	@echo "help      - Show this help message"

# Set up virtual environment and install dependencies
setup:
	python -m venv venv
	@echo "Activate virtual environment with:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Unix/macOS: source venv/bin/activate"
	@echo "Then run: make install"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Run tests with coverage
test:
	python run_tests.py

# Run linting
lint:
	flake8 .

# Format code
format:
	black .

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf build/ 2>/dev/null || true
	rm -rf dist/ 2>/dev/null || true
	rm -rf *.egg-info/ 2>/dev/null || true

# Run the main application
run:
	python main.py

# Run the demo script
demo:
	python demo.py
