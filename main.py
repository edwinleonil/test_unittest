"""
Main entry point for the PyTorch ResNet50 Image Classifier application.
"""

from src.gui import main
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


if __name__ == "__main__":
    main()
