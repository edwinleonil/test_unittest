#!/usr/bin/env python3
"""
Test runner script for the PyTorch ResNet50 classifier project.
This script sets up the proper paths and runs the test suite.
"""

import sys
import os
import subprocess
from pathlib import Path


def main():
    """Main test runner function."""
    print("PyTorch ResNet50 Image Classifier - Test Runner")
    print("=" * 50)

    # Get project root directory
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    tests_path = project_root / "tests"

    # Add src to Python path
    sys.path.insert(0, str(src_path))

    # Change to project directory
    os.chdir(project_root)

    # Check if pytest is available
    try:
        import pytest
        print("✓ pytest is available")
    except ImportError:
        print("✗ pytest is not installed")
        print("Install with: pip install pytest pytest-cov")
        return 1

    # Check if test directory exists
    if not tests_path.exists():
        print(f"✗ Tests directory not found: {tests_path}")
        return 1

    print(f"✓ Tests directory found: {tests_path}")

    # Run tests with coverage
    print("\nRunning tests with coverage...")
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "tests/"
    ]

    try:
        result = subprocess.run(cmd, check=False)

        if result.returncode == 0:
            print("\n✓ All tests passed!")
            print("✓ Coverage report generated in htmlcov/")
        else:
            print(f"\n✗ Tests failed with exit code: {result.returncode}")

        return result.returncode

    except Exception as e:
        print(f"\n✗ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
