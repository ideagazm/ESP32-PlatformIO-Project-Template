@echo off
REM Setup virtual environment for GitHub Actions on Windows
echo Setting up Python virtual environment...

REM Create virtual environment
python -m venv .venv
if %errorlevel% neq 0 exit /b %errorlevel%

REM Activate and upgrade pip
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if %errorlevel% neq 0 exit /b %errorlevel%

REM Install requirements
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

echo Virtual environment setup complete!
echo Python version:
python --version
echo PlatformIO version:
pio --version