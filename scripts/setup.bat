@echo off
REM HomeStock Setup Script for Windows

echo 🚀 Setting up HomeStock...

REM Check Python version
echo 📦 Checking Python...
python --version || (echo ❌ Python 3.10+ required && exit /b 1)

REM Check Node version
echo 📦 Checking Node.js...
node --version || (echo ❌ Node.js 20+ required && exit /b 1)

REM Setup Python backend
echo 🐍 Setting up Python backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

REM Setup Node frontend
echo 📱 Setting up Node.js frontend...
call npm install

echo ✅ Setup complete!
echo.
echo To run the app:
echo   npm start
echo.
echo To build for distribution:
echo   npm run build:win

pause

