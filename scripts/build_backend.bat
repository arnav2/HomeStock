@echo off
REM Build script for bundling Python backend with PyInstaller (Windows)

echo 🔨 Building Python backend...

cd /d "%~dp0\..\backend"

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup script first.
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade PyInstaller
pip install -q --upgrade pyinstaller

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Build with PyInstaller
echo 📦 Building executable...
pyinstaller build_backend.spec --clean --noconfirm

REM Check if build succeeded
if exist "dist\homestock-backend.exe" (
    echo ✅ Backend built successfully: dist\homestock-backend.exe
) else (
    echo ❌ Build failed - executable not found
    exit /b 1
)

deactivate

echo ✅ Backend build complete!

