# HomeStock - NSE Automation Desktop App

A lightweight Electron desktop application with Python FastAPI backend for automating NSE (National Stock Exchange) data downloads, parsing, and processing.

## 🚀 Quick Start

```bash
# 1. Install dependencies
cd backend && make install-dev && cd ..
npm install

# 2. Start the application
npm start
```

The app will automatically:
- Start the FastAPI backend on `http://localhost:5001`
- Start the Vite dev server on `http://localhost:5173`
- Launch the Electron desktop window

## ✨ Features

- **Download NSE Files**: Automatically download Capital Market (CM) and Derivatives (F&O) data files
- **Parse & Normalize**: Process raw files and generate normalized CSV outputs
- **Configurable Paths**: Set custom input/output folders
- **Date Range Selection**: Download files for specific date ranges
- **Scheduler**: Run automation on schedule (daily or custom cron)
- **Dashboard**: View download status and file counts
- **Cross-Platform**: Works on Mac and Windows

## 📋 Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Node.js 20+** (Node 20 LTS or higher)
- **npm** or **yarn**
- **uv** (Python package manager) - Install from https://github.com/astral-sh/uv

## 🛠️ Installation

### Option 1: Using Make (Recommended)

```bash
# Install backend dependencies
cd backend
make install-dev

# Install frontend dependencies (from project root)
cd ..
npm install
```

### Option 2: Manual Installation

#### Backend Setup

```bash
cd backend

# Using uv (recommended)
uv sync --extra dev --extra build

# Or using pip
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup

```bash
# From project root
npm install
```

## 🏃 Running the Application

### Development Mode

```bash
npm start
```

This will:
1. Start the Vite dev server (React frontend)
2. Start the FastAPI backend
3. Launch the Electron desktop window

### Backend Only (for testing)

```bash
cd backend
make dev
# Or: uv run python start_server.py
```

### Frontend Only (if backend is already running)

```bash
npm run dev:react
```

## 📚 Documentation

All documentation is available in the [`docs/`](docs/) folder:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started quickly
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started quickly
- **[Packaging Guide](docs/PACKAGING.md)** - Build for distribution
- **[Pipeline Documentation](docs/PIPELINE_DOCUMENTATION.md)** - Understanding the data pipeline
- **[NSE Files Guide](docs/NSE_FILES_README.md)** - What files are downloaded from NSE
- **[API Test Results](docs/API_TEST_RESULTS.md)** - Backend API testing
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Codebase organization
- **[Frontend Architecture](docs/FRONTEND_ARCHITECTURE.md)** - Frontend architecture

## 🏗️ Architecture

- **Frontend**: Electron + React + Vite + TailwindCSS
- **Backend**: Python FastAPI + Uvicorn
- **Package Manager**: uv (Python), npm (Node.js)
- **Integration**: Electron spawns Python backend as child process

## 📁 Project Structure

```
HomeStock/
├── docs/                    # All documentation
├── electron/                # Electron frontend
│   ├── main.js             # Main process
│   ├── preload.js          # Preload script
│   └── renderer/           # React app
│       ├── App.jsx         # Main React component
│       ├── pages/          # Page components
│       └── components/     # Reusable components
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py        # FastAPI app entry
│   │   ├── api/           # API endpoints
│   │   └── services/      # Business logic
│   ├── Makefile           # Backend commands
│   ├── pyproject.toml     # Python dependencies (uv)
│   └── requirements.txt   # Python dependencies (pip)
├── scripts/                # Build and setup scripts
└── package.json           # Node.js dependencies
```

## 🔧 Development Commands

### Backend (using Make)

```bash
cd backend

make help          # Show all available commands
make install-dev   # Install dependencies
make dev           # Run dev server with auto-reload
make lint          # Run linter
make lint-fix      # Fix linting issues
make format        # Format code
make test          # Run tests
make clean         # Clean build artifacts
```

### Frontend

```bash
npm start          # Start full app (backend + frontend)
npm run dev        # Start with dev mode
npm run dev:react  # Start only Vite dev server
npm run build:react # Build React app
```

## 🌐 API Endpoints

The backend API runs on `http://localhost:5001`. Key endpoints:

- `GET /health` - Health check
- `GET /settings/get` - Get settings
- `POST /settings/save` - Save settings
- `POST /download/` - Download NSE files
- `POST /parse/` - Parse files
- `GET /logs` - Get logs
- `POST /pipeline/run` - Run full pipeline

**API Documentation**: 
- Swagger UI: http://localhost:5001/docs
- ReDoc: http://localhost:5001/redoc

## 📦 Building for Distribution

```bash
# Mac
npm run build:mac

# Windows
npm run build:win

# Both platforms
npm run build
```

See [Packaging Guide](docs/PACKAGING.md) for detailed instructions.

## 🐛 Troubleshooting

### Backend won't start

1. Check Python version: `python3 --version` (should be 3.10+)
2. Install dependencies: `cd backend && make install-dev`
3. Check port 5001 is not in use: `lsof -ti:5001`
4. Check logs: `backend/logs/app.log`

### Electron app won't launch

1. Check Node version: `node --version` (should be 20+)
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Check if Vite is running: `lsof -ti:5173`
4. Check PostCSS config: Ensure `postcss.config.js` uses `module.exports`

### UI not visible

1. Ensure Vite is running on port 5173
2. Check Electron window (may be minimized)
3. Check browser console in Electron DevTools (press F12)

### Files not downloading

1. Check internet connection
2. Verify NSE URLs are accessible
3. Check folder permissions
4. Review logs in the **Logs** page

## 🧪 Testing

### Backend Tests

```bash
cd backend
make test
# Or: uv run pytest
```

### API Testing

```bash
cd backend
./test_api.sh
```

## 📝 License

MIT License

## 🤝 Support

For issues and questions:
- Check logs in the **Logs** page of the app
- Review `backend/logs/app.log`
- See documentation in `docs/` folder
