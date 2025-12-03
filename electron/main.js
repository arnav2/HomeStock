const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let pythonProcess = null;
const BACKEND_PORT = 5001;
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`;

/**
 * Get the Python executable path
 * In production (packaged), use bundled executable
 * In development, use system Python
 */
function getPythonExecutable() {
  const isDev = !app.isPackaged;
  
  if (isDev) {
    // Development: use system Python
    return process.platform === 'win32' ? 'python' : 'python3';
  } else {
    // Production: use bundled executable
    const exeName = process.platform === 'win32' ? 'homestock-backend.exe' : 'homestock-backend';
    const exePath = path.join(process.resourcesPath, 'backend', 'dist', exeName);
    
    if (fs.existsSync(exePath)) {
      return exePath;
    } else {
      // Fallback: try alternative paths
      const altPath = path.join(__dirname, '..', 'backend', 'dist', exeName);
      if (fs.existsSync(altPath)) {
        return altPath;
      }
      console.error('Bundled Python executable not found, falling back to system Python');
      return process.platform === 'win32' ? 'python' : 'python3';
    }
  }
}

/**
 * Start the FastAPI backend server
 */
function startBackend() {
  const pythonExecutable = getPythonExecutable();
  const isDev = !app.isPackaged;
  
  let args = [];
  let cwd = path.join(__dirname, '..', 'backend');
  
  if (isDev) {
    // Development: run Python script
    const backendPath = path.join(__dirname, '..', 'backend', 'start_server.py');
    args = [backendPath];
  } else {
    // Production: run bundled executable directly
    args = [];
    cwd = path.dirname(pythonExecutable);
  }
  
  console.log(`Starting FastAPI backend... (${isDev ? 'dev' : 'prod'})`);
  console.log(`Executable: ${pythonExecutable}`);
  console.log(`Args: ${args.join(' ')}`);
  
  pythonProcess = spawn(pythonExecutable, args, {
    cwd: cwd,
    stdio: 'pipe',
    env: {
      ...process.env,
      // Ensure Python can find its bundled dependencies
      PYTHONUNBUFFERED: '1'
    }
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
    pythonProcess = null;
  });

  // Wait for backend to be ready
  waitForBackend();
}

/**
 * Wait for backend to be ready by pinging /health endpoint
 */
function waitForBackend() {
  const http = require('http');
  const maxAttempts = 30;
  let attempts = 0;

  const checkHealth = () => {
    const req = http.get(`${BACKEND_URL}/health`, (res) => {
      if (res.statusCode === 200) {
        console.log('Backend is ready!');
        if (mainWindow) {
          mainWindow.webContents.send('backend-ready');
        }
      } else {
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(checkHealth, 1000);
        }
      }
    });

    req.on('error', () => {
      attempts++;
      if (attempts < maxAttempts) {
        setTimeout(checkHealth, 1000);
      } else {
        console.error('Backend failed to start');
        if (mainWindow) {
          mainWindow.webContents.send('backend-error', 'Backend failed to start');
        }
      }
    });
  };

  setTimeout(checkHealth, 2000);
}

/**
 * Create the main application window
 */
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 600,
    minWidth: 800,
    minHeight: 500,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '..', 'assets', 'icon.png')
  });

  // Load React app
  const isDev = process.argv.includes('--dev') || !app.isPackaged;
  
  if (isDev) {
    // Development: load from Vite dev server
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // Production: load from built files
    mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// IPC Handlers
ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  });
  
  if (!result.canceled && result.filePaths.length > 0) {
    return result.filePaths[0];
  }
  return null;
});

ipcMain.handle('open-folder', async (event, folderPath) => {
  const { shell } = require('electron');
  if (fs.existsSync(folderPath)) {
    shell.openPath(folderPath);
    return true;
  }
  return false;
});

// App lifecycle
app.whenReady().then(() => {
  createWindow();
  startBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (pythonProcess) {
    console.log('Stopping backend...');
    pythonProcess.kill();
    pythonProcess = null;
  }
});

// Handle app quit
app.on('will-quit', (event) => {
  if (pythonProcess) {
    event.preventDefault();
    pythonProcess.kill();
    setTimeout(() => {
      app.exit(0);
    }, 1000);
  }
});

