# HomeStock Project Structure

## Complete File Tree

```
HomeStock/
├── electron/                          # Electron Frontend
│   ├── main.js                       # Main process (spawns Python backend)
│   ├── preload.js                    # Preload script (IPC bridge)
│   └── renderer/                     # Renderer process (UI)
│       ├── index.html                # Main HTML UI
│       ├── styles.css                # Application styles
│       └── app.js                    # Frontend JavaScript logic
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── api/                      # API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── download.py          # POST /download/
│   │   │   ├── parse.py             # POST /parse/
│   │   │   ├── settings.py          # GET/POST /settings/*
│   │   │   ├── logs.py              # GET /logs
│   │   │   └── run_full.py          # POST /run-full/
│   │   └── services/                 # Business Logic
│   │       ├── __init__.py
│   │       ├── download_service.py   # NSE file downloading
│   │       ├── parse_service.py     # File parsing & normalization
│   │       ├── scheduler_service.py # Cron scheduling
│   │       └── utils.py             # Utility functions
│   ├── requirements.txt              # Python dependencies
│   ├── start_server.py               # Server startup script
│   ├── settings.json                 # User settings (generated)
│   └── logs/                         # Application logs
│       └── app.log
│
├── assets/                           # Application assets
│   ├── icon.png                     # Main icon (512x512)
│   ├── icon.icns                    # Mac icon
│   ├── icon.ico                     # Windows icon
│   └── README.md                    # Icon creation guide
│
├── scripts/                          # Setup scripts
│   ├── setup.sh                     # Mac/Linux setup
│   └── setup.bat                    # Windows setup
│
├── package.json                      # Node.js/Electron config
├── electron-builder.yml              # Build configuration
├── .gitignore                        # Git ignore rules
├── README.md                          # Main documentation
├── QUICKSTART.md                     # Quick start guide
└── PROJECT_STRUCTURE.md              # This file
```

## Key Components

### Frontend (Electron)
- **main.js**: Manages Electron window, spawns Python backend, handles IPC
- **preload.js**: Secure bridge between main and renderer processes
- **renderer/**: UI layer - HTML/CSS/JS for all pages

### Backend (FastAPI)
- **main.py**: FastAPI application with CORS middleware
- **api/**: REST endpoints for all operations
- **services/**: Core business logic (download, parse, schedule)

### Integration
- Electron spawns Python backend as child process
- Frontend communicates via HTTP (localhost:5001)
- Settings stored in JSON file
- Logs written to file and console

## API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/download/` | Download NSE files |
| POST | `/parse/` | Parse raw files |
| GET | `/settings/get` | Get settings |
| POST | `/settings/save` | Save settings |
| POST | `/settings/test-path` | Test folder path |
| GET | `/logs` | Get logs |
| POST | `/run-full/` | Run full automation |

## Data Flow

1. **User Action** → Frontend (app.js)
2. **HTTP Request** → Backend API (FastAPI)
3. **Service Layer** → Business logic execution
4. **File Operations** → Download/Parse files
5. **Response** → Frontend displays results

## Settings Storage

Settings are stored in `backend/settings.json`:
```json
{
  "raw_path": "/path/to/raw",
  "processed_path": "/path/to/processed",
  "output_path": "/path/to/output",
  "scheduler": "daily-7am",
  "custom_cron": ""
}
```

## Logs

Logs are written to:
- `backend/logs/app.log` (file)
- Console/stdout (when running)

## Build Output

After building:
- Mac: `dist/HomeStock-1.0.0.dmg`
- Windows: `dist/HomeStock Setup 1.0.0.exe`

