# Development Guide

Complete guide for developing HomeStock, covering both frontend and backend.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [API Integration](#api-integration)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Mobile (React Native)](#mobile-react-native)

## 🏗️ Architecture Overview

HomeStock uses a hybrid architecture:

```
┌─────────────────────────────────────────┐
│         Electron Desktop App            │
│  ┌───────────────────────────────────┐  │
│  │   React Frontend (Vite + Tailwind) │  │
│  │   - Dashboard                      │  │
│  │   - Downloads                      │  │
│  │   - Parser                         │  │
│  │   - Settings                       │  │
│  │   - Logs                           │  │
│  └───────────────────────────────────┘  │
│              ↕ IPC / HTTP                │
│  ┌───────────────────────────────────┐  │
│  │   Python FastAPI Backend           │  │
│  │   - Download Service               │  │
│  │   - Parse Service                  │  │
│  │   - Pipeline Service               │  │
│  │   - Database Service                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Communication Flow

1. **Electron Main Process** (`electron/main.js`)
   - Manages application window
   - Spawns Python backend process
   - Handles IPC communication

2. **React Renderer** (`electron/renderer/`)
   - UI components and pages
   - Makes HTTP requests to backend API
   - Uses `services/api.js` for API calls

3. **FastAPI Backend** (`backend/app/`)
   - RESTful API endpoints
   - Business logic in services
   - Database operations

## 🔧 Backend Development

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/                 # API endpoints
│   │   ├── download.py     # Download endpoints
│   │   ├── parse.py        # Parse endpoints
│   │   ├── settings.py     # Settings endpoints
│   │   ├── logs.py         # Logs endpoints
│   │   ├── pipeline.py     # Pipeline endpoints
│   │   └── run_full.py     # Full automation endpoint
│   └── services/           # Business logic
│       ├── download_service.py
│       ├── parse_service.py
│       ├── pipeline_service.py
│       ├── excel_service.py
│       ├── verification_service.py
│       ├── database.py
│       └── rate_limiter.py
├── tests/                  # Test files
├── Makefile               # Development commands
├── pyproject.toml         # Dependencies (uv)
└── requirements.txt       # Dependencies (pip)
```

### Development Commands

```bash
cd backend

# Install dependencies
make install-dev

# Run development server (with auto-reload)
make dev

# Code quality
make lint          # Check code
make lint-fix      # Auto-fix issues
make format        # Format code
make type-check    # Type checking with pyright

# Testing
make test          # Run all tests
make test-verbose  # Verbose output
make test-coverage # With coverage report

# Cleanup
make clean         # Remove build artifacts
```

### Key Backend Services

#### Download Service (`app/services/download_service.py`)

- Downloads NSE files from URLs
- Implements rate limiting (5 requests per 60 seconds)
- Tracks download progress
- Handles retries and errors

#### Parse Service (`app/services/parse_service.py`)

- Extracts ZIP files
- Parses CSV files
- Normalizes data formats
- Generates output CSVs

#### Pipeline Service (`app/services/pipeline_service.py`)

- Orchestrates full workflow:
  1. Download files
  2. Verify downloads
  3. User confirmation
  4. Excel processing
  5. Output generation

#### Database Service (`app/services/database.py`)

- SQLite database for tracking downloads
- Stores download history
- Tracks file status

### Backend API Endpoints

See [API Test Results](API_TEST_RESULTS.md) for complete API documentation.

**Key Endpoints:**

- `GET /health` - Health check
- `POST /download/` - Download files for date range
- `POST /download/single` - Download single file
- `POST /parse/` - Parse raw files
- `GET /settings/get` - Get settings
- `POST /settings/save` - Save settings
- `POST /pipeline/run` - Run pipeline
- `GET /logs` - Get logs

## 🎨 Frontend Development

### Project Structure

```
electron/
├── main.js                 # Electron main process
├── preload.js             # Preload script (IPC bridge)
└── renderer/              # React application
    ├── main.jsx           # React entry point
    ├── App.jsx            # Main app component
    ├── index.html         # HTML template
    ├── index.css          # Global styles
    ├── components/        # Reusable components
    │   ├── Sidebar.jsx
    │   ├── Button.jsx
    │   ├── FormInput.jsx
    │   ├── StatusCard.jsx
    │   └── StatusMessage.jsx
    ├── pages/             # Page components
    │   ├── Dashboard.jsx
    │   ├── Downloads.jsx
    │   ├── Parser.jsx
    │   ├── Settings.jsx
    │   └── Logs.jsx
    └── services/          # API service layer
        └── api.js
```

### Development Commands

```bash
# From project root

# Start full app (backend + frontend)
npm start

# Dev mode (with auto-reload)
npm run dev

# Frontend only (Vite dev server)
npm run dev:react

# Build React app
npm run build:react
```

### Frontend Architecture

#### React Router

- Uses `HashRouter` for Electron compatibility
- Routes defined in `App.jsx`
- Navigation handled by `Sidebar` component

#### API Integration

- All API calls through `services/api.js`
- Centralized error handling
- Automatic retry logic

#### State Management

- React hooks (`useState`, `useEffect`)
- Component-level state
- No global state management library

#### Styling

- TailwindCSS utility classes
- Responsive design
- Consistent component styling

### Key Frontend Components

#### Pages

- **Dashboard**: Overview and quick actions
- **Downloads**: File download interface
- **Parser**: File parsing interface
- **Settings**: Configuration management
- **Logs**: Application logs viewer

#### Components

- **Sidebar**: Navigation with active route highlighting
- **Button**: Reusable button with variants
- **FormInput**: Form input with label
- **StatusCard**: Statistics display
- **StatusMessage**: Status notifications

## 🔌 API Integration

### Frontend to Backend Communication

The frontend communicates with the backend via HTTP requests:

```javascript
// Example from services/api.js
const response = await fetch('http://localhost:5001/download/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    start_date: '2024-12-01',
    end_date: '2024-12-01',
    urls: {},
    raw_path: '/path/to/raw'
  })
});
```

### Backend API Base URL

- **Development**: `http://localhost:5001`
- **Production**: Same (backend runs locally)

### Error Handling

Frontend handles errors gracefully:

- Network errors → User-friendly messages
- API errors → Display error details
- Timeout errors → Retry mechanism

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run all tests
make test

# Run specific test file
uv run pytest tests/test_download.py

# Run with coverage
make test-coverage

# Run API tests
./test_api.sh
```

### Frontend Testing

Currently, frontend testing is manual:

1. Start the app: `npm start`
2. Test each page and feature
3. Check browser console for errors

### Integration Testing

Test the full flow:

1. Start backend: `cd backend && make dev`
2. Start frontend: `npm run dev:react`
3. Launch Electron: `npx electron . --dev`
4. Test download → parse → pipeline flow

## 🐛 Debugging

### Backend Debugging

```bash
# Check backend logs
tail -f backend/logs/app.log

# Run backend with verbose logging
cd backend
uv run python start_server.py

# Test API endpoints directly
curl http://localhost:5001/health
```

### Frontend Debugging

1. **Electron DevTools**: Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
2. **Console Logs**: Check browser console
3. **Network Tab**: Monitor API requests
4. **React DevTools**: Install React DevTools extension

### Common Issues

#### Backend won't start

- Check Python version: `python3 --version`
- Check port 5001: `lsof -ti:5001`
- Check logs: `backend/logs/app.log`

#### Frontend won't load

- Check Vite is running: `lsof -ti:5173`
- Check PostCSS config: `postcss.config.js` should use `module.exports`
- Check console for errors

#### API calls failing

- Verify backend is running: `curl http://localhost:5001/health`
- Check CORS settings in `backend/app/main.py`
- Check network tab in DevTools

## 📱 Mobile (React Native)

There is an experimental **React Native / Expo** client in the `mobile/` directory:

- Uses Expo + React Native
- Talks to the same FastAPI backend over HTTP
- Lets you monitor the backend from iPad / Android (backend still runs on desktop/server)

### Running the Mobile App

```bash
cd mobile
npm install
npm start   # starts Expo dev server
```

Then use **Expo Go** on your iOS/Android device (or simulators) to open the app.

Configure the backend URL inside the app to point to the machine running the backend,
for example:

- `http://192.168.1.10:5001` (replace with your desktop/server LAN IP)

## Additional Resources

- [Backend API Documentation](API_TEST_RESULTS.md)
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md)
- [Project Structure](PROJECT_STRUCTURE.md)
- [NSE Files Guide](NSE_FILES_README.md)
- [Pipeline Documentation](PIPELINE_DOCUMENTATION.md)
