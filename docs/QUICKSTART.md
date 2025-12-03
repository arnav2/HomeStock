# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

**Using Make (Recommended):**

```bash
# Backend dependencies
cd backend
make install-dev

# Frontend dependencies (from project root)
cd ..
npm install
```

**Using uv (Python) + npm:**

```bash
# Backend dependencies
cd backend
uv sync --extra dev --extra build

# Frontend dependencies (from project root)
cd ..
npm install
```

**Using pip (Alternative):**

```bash
# Backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend dependencies (from project root)
cd ..
npm install
```

### 2. Run the App

```bash
# From project root
npm start
```

This will:

- ✅ Start the FastAPI backend on `http://localhost:5001`
- ✅ Start the Vite dev server on `http://localhost:5173`
- ✅ Launch the Electron desktop window

### 3. Configure Settings

1. Open the app (Electron window should appear)
2. Go to **Settings** page
3. Set your folder paths:
   - **Raw File Folder**: Where downloaded files are stored
   - **Processed Folder**: Intermediate processing folder
   - **Output Folder**: Final normalized CSV output location
4. Click **Save Settings**

## 🎯 Next Steps

### Download NSE Files

1. Go to **Downloads** page
2. Select date range (e.g., last 7 days)
3. Click **Download Missing Files**
4. Wait for downloads to complete

### Parse Files

1. Go to **Parser** page
2. Verify paths are correct
3. Click **Parse Raw Files → Normalized CSV**

### Run Full Automation

1. Go to **Dashboard**
2. Click **Run Full Automation Now**
3. This will download and parse files automatically

## 🔧 Development Commands

### Backend Commands (using Make)

```bash
cd backend

make help          # Show all commands
make dev           # Run dev server with auto-reload
make lint          # Check code quality
make lint-fix      # Auto-fix linting issues
make format        # Format code
make test          # Run tests
make clean         # Clean build artifacts
```

### Frontend Commands

```bash
npm start          # Start full app
npm run dev        # Dev mode
npm run dev:react  # Vite dev server only
```

## 📚 Documentation

- **[Main README](../README.md)** - Project overview
- **[NSE Files Guide](NSE_FILES_README.md)** - What files are downloaded
- **[Pipeline Documentation](PIPELINE_DOCUMENTATION.md)** - How the pipeline works
- **[Packaging Guide](PACKAGING.md)** - Build for distribution
- **[All Documentation](README.md)** - Complete documentation index

## 🐛 Troubleshooting

### Backend won't start

```bash
cd backend
make dev
# Check logs: tail -f logs/app.log
```

### Electron window not visible

- Check if Vite is running: `lsof -ti:5173`
- Check if backend is running: `lsof -ti:5001`
- Look for Electron icon in dock/taskbar

### Dependencies issues

```bash
# Backend
cd backend
make clean
make install-dev

# Frontend
rm -rf node_modules
npm install
```

## ✅ Verification

Test that everything is working:

```bash
# Backend health check
curl http://localhost:5001/health

# Should return: {"status":"ok"}
```

If you see the Electron window and can navigate between pages, you're all set! 🎉

## 💻 Running on macOS

### Requirements

- macOS 12+ (Intel or Apple Silicon)
- Python 3.10+ installed and on `PATH`
- Node.js 20+ and npm installed

### Commands (macOS)

```bash
# 1) Install backend deps
cd backend
make install-dev

# 2) Install frontend deps
cd ..
npm install

# 3) Run the app (backend + frontend + Electron)
npm start
```

You can also run just the backend:

```bash
cd backend
make dev
```

## 🪟 Running on Windows

### Requirements

- Windows 10/11 (64‑bit)
- Python 3.10+ installed, added to `PATH`
- Node.js 20+ and npm installed
- Git Bash / PowerShell for running commands

### Commands (Windows)

```powershell
# 1) Install backend deps
cd backend
make install-dev   # If Make is available

# Or without Make:
uv sync --extra dev --extra build

# 2) Install frontend deps (from project root)
cd ..
npm install

# 3) Run the app
npm start
```

On Windows, Electron will open a normal desktop window; the backend still runs on `http://localhost:5001` and the UI works the same as on macOS.

## 📱 Mobile / Tablet Support (iPad, Android)

HomeStock is currently built as a **desktop application**:

- **Supported**:
  - macOS (Intel + Apple Silicon)
  - Windows 10/11
- **Not natively supported**:
  - iPadOS (iPad)
  - Android phones/tablets

Electron apps do not run directly on iOS/iPadOS or Android. To support those platforms in the future, the app would need to be:

- Exposed as a web app served from the backend, **or**
- Ported to a mobile framework (e.g. React Native / Flutter) that talks to the same FastAPI backend.

Right now, the recommended way to use HomeStock on mobile is to run it on a desktop machine and access the results (e.g. processed files) via shared storage or synced folders.
