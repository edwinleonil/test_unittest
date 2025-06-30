#!/usr/bin/env python3
"""
Sample script to demonstrate the PyTorch ResNet50 classifier functionality.
This script can be used for quick testing or demonstration purposes.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from model import create_classifier
    print("✓ Successfully imported model module")
except ImportError as e:
    print(f"✗ Failed to import model module: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main demonstration function."""
    print("PyTorch ResNet50 Image Classifier - Demo Script")
    print("=" * 50)

    try:
        print("Loading ResNet50 model...")
        classifier = create_classifier()
        print("✓ Model loaded successfully!")

        print(f"✓ Model is ready: {classifier.is_model_loaded()}")
        print(f"✓ Transform pipeline configured: {classifier.transform is not None}")
        print(f"✓ Class labels loaded: {len(classifier.class_labels)} classes available")

        print("\nModel Information:")
        print(f"  - Model type: ResNet50")
        print(f"  - Input size: 224x224 RGB")
        print(f"  - Pre-trained: ImageNet")
        print(f"  - Available classes (sample): {classifier.class_labels[:5]}...")

        print("\nTo run the GUI application, execute:")
        print("  python main.py")

        print("\nTo run tests, execute:")
        print("  pytest")

    except Exception as e:
        print(f"✗ Error during demonstration: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
