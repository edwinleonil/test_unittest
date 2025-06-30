@echo off
echo PyTorch ResNet50 Image Classifier - Setup Script
echo ================================================

echo.
echo Setting up virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo.
echo Running demo script...
python demo.py

echo.
echo Setup complete! To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run the application: python main.py
echo   3. Run tests: pytest

pause
