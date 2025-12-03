# Packaging Guide for HomeStock

This guide explains how to package HomeStock as a standalone application for Mac and Windows distribution.

## Overview

HomeStock uses a hybrid architecture:
- **Frontend**: Electron (Node.js/HTML/CSS/JS)
- **Backend**: Python FastAPI (bundled as standalone executable)

The packaging process:
1. Bundles Python backend with PyInstaller into a standalone executable
2. Packages Electron app with electron-builder
3. Includes the Python executable in the final distribution

## Prerequisites

### For Building (Developers)

- **Python 3.10+** (3.11 or 3.12 recommended)
- **Node.js 20+** (LTS version recommended)
- **npm** or **yarn**

### Platform-Specific Requirements

#### Mac
- Xcode Command Line Tools: `xcode-select --install`
- For code signing (optional but recommended):
  - Apple Developer account
  - Code signing certificate

#### Windows
- Visual Studio Build Tools or Visual Studio Community
- Windows SDK

## Building the Application

### Step 1: Initial Setup

First, set up the development environment:

```bash
# Install Python dependencies
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
deactivate
cd ..

# Install Node dependencies
npm install
```

### Step 2: Build Python Backend

The Python backend must be built before packaging the Electron app:

**Mac/Linux:**
```bash
./scripts/build_backend.sh
```

**Windows:**
```bash
scripts\build_backend.bat
```

**Or use the Node.js script (cross-platform):**
```bash
npm run build:backend
```

This creates:
- `backend/dist/homestock-backend` (Mac/Linux)
- `backend/dist/homestock-backend.exe` (Windows)

### Step 3: Build Electron App

**For Mac (.dmg):**
```bash
npm run build:mac
```

**For Windows (.exe installer):**
```bash
npm run build:win
```

**For both platforms:**
```bash
npm run build
```

The packaged applications will be in the `dist/` folder:
- Mac: `dist/HomeStock-1.0.0.dmg`
- Windows: `dist/HomeStock Setup 1.0.0.exe`

## Distribution Files

### Mac Distribution

The Mac build creates a `.dmg` file that:
- Can be mounted and dragged to Applications folder
- Includes proper app bundle structure
- Works on macOS 10.13+ (High Sierra or later)

**File structure:**
```
HomeStock.app/
├── Contents/
│   ├── MacOS/
│   │   └── HomeStock (Electron executable)
│   ├── Resources/
│   │   ├── electron/ (frontend files)
│   │   └── backend/
│   │       └── dist/
│   │           └── homestock-backend (Python executable)
│   └── Info.plist
```

### Windows Distribution

The Windows build creates an NSIS installer that:
- Allows custom installation directory
- Creates desktop and Start Menu shortcuts
- Includes all dependencies

**File structure (after installation):**
```
HomeStock/
├── HomeStock.exe (Electron executable)
├── resources/
│   ├── electron/ (frontend files)
│   └── backend/
│       └── dist/
│           └── homestock-backend.exe (Python executable)
└── ... (other Electron files)
```

## How It Works

### Development Mode

In development (`npm start` or `npm run dev`):
- Uses system Python (`python3` or `python`)
- Runs `start_server.py` directly
- Requires Python and dependencies to be installed

### Production Mode (Packaged)

In packaged applications:
- Uses bundled `homestock-backend` executable
- No system Python required
- All Python dependencies are included
- Fully self-contained

The Electron main process (`electron/main.js`) automatically detects:
- If running in development: uses system Python
- If running packaged: uses bundled executable

## Troubleshooting

### Build Fails: "Python executable not found"

**Solution:**
1. Ensure Python backend is built first: `npm run build:backend`
2. Check that `backend/dist/homestock-backend` (or `.exe` on Windows) exists
3. Verify PyInstaller installed: `pip list | grep pyinstaller`

### Build Fails: "PyInstaller not found"

**Solution:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pyinstaller
deactivate
```

### App Won't Start: "Backend failed to start"

**Solution:**
1. Check console logs in the app (if DevTools enabled)
2. Verify the bundled executable has execute permissions (Mac/Linux)
3. On Mac, you may need to allow the app in System Preferences > Security

### Mac: "App is damaged" Error

**Solution:**
1. Remove quarantine attribute:
   ```bash
   xattr -cr /Applications/HomeStock.app
   ```
2. Or allow in System Preferences > Security & Privacy
3. For distribution, properly code sign the app (requires Apple Developer account)

### Windows: Antivirus False Positives

**Solution:**
- PyInstaller executables sometimes trigger false positives
- Submit to antivirus vendors for whitelisting
- Consider code signing (requires certificate)

## Code Signing (Optional but Recommended)

### Mac Code Signing

1. Get Apple Developer certificate
2. Update `electron-builder.yml`:
   ```yaml
   mac:
     identity: "Developer ID Application: Your Name (TEAM_ID)"
   ```
3. Build: `npm run build:mac`

### Windows Code Signing

1. Get code signing certificate
2. Update `electron-builder.yml`:
   ```yaml
   win:
     certificateFile: "path/to/certificate.pfx"
     certificatePassword: "password"
   ```
3. Build: `npm run build:win`

## File Sizes

Expected sizes:
- **Mac .dmg**: ~150-200 MB (includes Python runtime)
- **Windows installer**: ~150-200 MB (includes Python runtime)
- **Unpacked app**: ~200-300 MB

The Python runtime adds significant size but ensures the app works without system Python.

## Continuous Integration

### GitHub Actions Example

```yaml
name: Build

on: [push, pull_request]

jobs:
  build-mac:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v2
        with:
          node-version: '20'
      - run: npm install
      - run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
      - run: npm run build:mac
      - uses: actions/upload-artifact@v2
        with:
          name: mac-dist
          path: dist/*.dmg

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v2
        with:
          node-version: '20'
      - run: npm install
      - run: cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
      - run: npm run build:win
      - uses: actions/upload-artifact@v2
        with:
          name: windows-dist
          path: dist/*.exe
```

## Distribution Checklist

Before distributing:

- [ ] Test on clean system (no Python/Node installed)
- [ ] Verify all features work in packaged app
- [ ] Check file sizes are reasonable
- [ ] Test installation process
- [ ] Verify shortcuts are created (Windows)
- [ ] Test app launch and backend startup
- [ ] Check logs for errors
- [ ] Code sign (if possible)
- [ ] Create release notes
- [ ] Upload to distribution platform

## Additional Resources

- [Electron Builder Documentation](https://www.electron.build/)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Electron Packaging Guide](https://www.electronjs.org/docs/latest/tutorial/application-distribution)

