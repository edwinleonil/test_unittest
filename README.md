# PyTorch ResNet50 Image Classifier

[![CI/CD Pipeline](https://github.com/yourusername/test_unittest/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/test_unittest/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A desktop application for image classification using a pre-trained PyTorch ResNet50 model with a user-friendly Tkinter GUI. This project demonstrates best practices in machine learning application development, including comprehensive testing and CI/CD integration.

## Features

- **Pre-trained ResNet50 Model**: Utilizes PyTorch's pre-trained ResNet50 for accurate image classification
- **User-Friendly GUI**: Clean and intuitive Tkinter interface for easy image selection and classification
- **Real-time Processing**: Asynchronous image processing with visual feedback
- **Robust Error Handling**: Comprehensive error handling for various edge cases
- **Comprehensive Testing**: Full unit test coverage with pytest
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## Screenshots

*GUI screenshots would go here in a real project*

## Installation

### Prerequisites

- Python 3.9 or higher
- Git

### Clone the Repository

```bash
git clone https://github.com/yourusername/test_unittest.git
cd test_unittest
```

### Set Up Virtual Environment

#### Using venv (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Using conda

```bash
conda create -n resnet50-classifier python=3.10
conda activate resnet50-classifier
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Select Image**: Click "Select Image" to choose an image file (supports .jpg, .png, .bmp, .gif, .tiff)
2. **Preview**: The selected image will be displayed in the preview panel
3. **Classify**: Click "Classify Image" to run the ResNet50 model on your image
4. **View Results**: The top 5 predictions with confidence scores will be displayed

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)

## Development

### Project Structure

```
test_unittest/
├── src/                    # Source code
│   ├── __init__.py
│   ├── model.py           # ResNet50 classifier implementation
│   └── gui.py             # Tkinter GUI implementation
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_model.py      # Model tests
│   └── test_gui.py        # GUI tests
├── data/                  # Sample images (not included)
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions workflow
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup
├── pytest.ini          # Pytest configuration
└── README.md           # This file
```

### Running Tests

#### All Tests

```bash
pytest
```

#### Specific Test Files

```bash
# Test only the model
pytest tests/test_model.py

# Test only the GUI
pytest tests/test_gui.py
```

#### With Coverage Report

```bash
pytest --cov=src --cov-report=html
```

### Code Quality

#### Linting

```bash
flake8 .
```

#### Code Formatting

```bash
# Check formatting
black --check .

# Auto-format code
black .
```

### Adding New Tests

1. Create test files in the `tests/` directory following the `test_*.py` naming convention
2. Use pytest fixtures for setup and teardown
3. Mock external dependencies (e.g., model loading) for faster tests
4. Follow the existing test structure and patterns

## Technical Details

### Model Architecture

- **Base Model**: ResNet50 pre-trained on ImageNet
- **Input Size**: 224×224×3 RGB images
- **Preprocessing**: Resize, center crop, normalization using ImageNet statistics
- **Output**: Top-k class predictions with confidence scores

### GUI Architecture

- **Framework**: Tkinter (included with Python)
- **Threading**: Asynchronous processing to prevent UI freezing
- **Error Handling**: User-friendly error messages and logging
- **Image Display**: Automatic resizing while maintaining aspect ratio

### Testing Strategy

- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: End-to-end workflow testing
- **Error Handling Tests**: Edge cases and error conditions
- **GUI Tests**: UI component and interaction testing

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Triggers

- Push to `main` or `develop` branches
- Pull requests targeting `main` branch

### Pipeline Steps

1. **Environment Setup**: Python 3.9, 3.10, 3.11 matrix
2. **Dependency Installation**: Cache pip packages for faster builds
3. **Code Linting**: flake8 for syntax and style checking
4. **Code Formatting**: black for consistent formatting
5. **Unit Testing**: pytest with coverage reporting
6. **Build Validation**: Application import and basic functionality tests

### Status Badges

The README includes badges showing:
- Build status
- Python version compatibility
- License information

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Check code quality (`flake8 .` and `black --check .`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage above 80%
- Keep functions focused and single-purpose

## Troubleshooting

### Common Issues

#### Model Loading Errors

```
Error: Failed to load model
```

**Solution**: Ensure you have a stable internet connection for downloading pre-trained weights on first run.

#### GUI Display Issues

```
Error: Display not found
```

**Solution**: If running in a headless environment, you'll need to set up a virtual display or run tests in non-GUI mode.

#### Import Errors

```
ModuleNotFoundError: No module named 'torch'
```

**Solution**: Make sure you've activated your virtual environment and installed dependencies:

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Performance Optimization

- First model load may take time due to downloading pre-trained weights
- Subsequent runs will be faster as weights are cached
- For faster inference, consider running on GPU (requires CUDA-compatible PyTorch)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyTorch team for the excellent deep learning framework
- torchvision for pre-trained models and transforms
- The Python community for amazing libraries and tools

## Roadmap

- [ ] Add support for batch image processing
- [ ] Implement custom model training capabilities
- [ ] Add more pre-trained model options (VGG, EfficientNet, etc.)
- [ ] Create web interface alternative
- [ ] Add model performance benchmarking
- [ ] Implement result export functionality

## Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/test_unittest](https://github.com/yourusername/test_unittest)
