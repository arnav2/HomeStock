# HomeStock Backend API Test Results

## Test Date
$(date)

## Backend Status
✅ **Backend is running on http://localhost:5001**

## Test Results Summary

All 10 endpoints tested successfully! ✅

### 1. Health Check ✅
- **Endpoint**: `GET /health`
- **Status**: Working
- **Response**: `{"status":"ok"}`
- **Purpose**: Basic connectivity check

### 2. Settings Get ✅
- **Endpoint**: `GET /settings/get`
- **Status**: Working
- **Response**: Returns current settings or empty object
- **Purpose**: Retrieve application settings

### 3. Settings Save ✅
- **Endpoint**: `POST /settings/save`
- **Status**: Working
- **Request Body**:
  ```json
  {
    "raw_path": "/tmp/homestock_raw",
    "processed_path": "/tmp/homestock_processed",
    "output_path": "/tmp/homestock_output",
    "scheduler": "daily",
    "custom_cron": ""  // optional
  }
  ```
- **Purpose**: Save application settings

### 4. Settings Verification ✅
- **Endpoint**: `GET /settings/get` (after save)
- **Status**: Working
- **Verification**: Settings persist correctly

### 5. Path Test - Valid ✅
- **Endpoint**: `POST /settings/test-path`
- **Status**: Working
- **Request**: `{"path": "/tmp"}`
- **Response**: `{"accessible": true, "error": null}`
- **Purpose**: Validate directory accessibility

### 6. Path Test - Invalid ✅
- **Endpoint**: `POST /settings/test-path`
- **Status**: Working
- **Request**: `{"path": "/nonexistent/path/12345"}`
- **Response**: `{"accessible": false, "error": null}`
- **Purpose**: Handle invalid paths gracefully

### 7. Logs ✅
- **Endpoint**: `GET /logs`
- **Status**: Working
- **Response**: Returns array of log entries (last 200 lines)
- **Current Log Count**: 335 entries
- **Purpose**: Retrieve application logs

### 8. Download Status ✅
- **Endpoint**: `GET /download/status`
- **Status**: Working
- **Response**: Returns list of active/completed downloads
- **Current Downloads**: 0 active
- **Purpose**: Track download progress

### 9. Parse ✅
- **Endpoint**: `POST /parse/`
- **Status**: Working
- **Request Body**:
  ```json
  {
    "raw_path": "/path/to/raw/files",
    "output_path": "/path/to/output"
  }
  ```
- **Purpose**: Parse raw NSE files to normalized CSV
- **Note**: Handles invalid paths gracefully

### 10. Pipeline Verify ✅
- **Endpoint**: `POST /pipeline/verify-only`
- **Status**: Working
- **Query Parameters**: `start_date`, `end_date`, `raw_path`
- **Response**: Returns verification results with file counts
- **Purpose**: Verify downloaded files before processing

## Additional Endpoints Available

### API Documentation
- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc
- **OpenAPI JSON**: http://localhost:5001/openapi.json

### Other Endpoints (Not Tested)
- `POST /download/` - Download NSE files for date range
- `POST /download/single` - Download single file
- `POST /download/retry` - Retry failed download
- `GET /download/{download_id}` - Get specific download status
- `POST /run-full/` - Run full automation pipeline
- `POST /pipeline/run` - Run pipeline with all phases
- `POST /pipeline/confirm` - Continue pipeline after user confirmation

## CURL Examples

### Health Check
```bash
curl http://localhost:5001/health
```

### Get Settings
```bash
curl http://localhost:5001/settings/get
```

### Save Settings
```bash
curl -X POST http://localhost:5001/settings/save \
  -H "Content-Type: application/json" \
  -d '{
    "raw_path": "/tmp/raw",
    "processed_path": "/tmp/processed",
    "output_path": "/tmp/output",
    "scheduler": "daily"
  }'
```

### Test Path
```bash
curl -X POST http://localhost:5001/settings/test-path \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp"}'
```

### Get Logs
```bash
curl http://localhost:5001/logs
```

### Download Status
```bash
curl http://localhost:5001/download/status
```

## Running Tests

A test script is available at `backend/test_api.sh`:

```bash
cd backend
chmod +x test_api.sh
./test_api.sh
```

## Frontend Connection

The backend is ready for frontend connection:
- **CORS**: Enabled for all origins
- **Port**: 5001
- **Host**: 127.0.0.1 (localhost)

The Electron frontend should connect to `http://localhost:5001` for all API calls.

## Notes

- All endpoints return JSON responses
- Error handling is implemented for invalid inputs
- Settings persist to `settings.json` file
- Logs are stored in `backend/logs/app.log`
- Rate limiting is implemented for NSE downloads (5 requests per 60 seconds)

