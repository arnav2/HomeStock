# Frontend & Backend Integration Guide

Complete guide covering both frontend and backend development, testing, and integration.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Backend API](#backend-api)
3. [Frontend Components](#frontend-components)
4. [Integration Testing](#integration-testing)
5. [Download Testing](#download-testing)
6. [Troubleshooting](#troubleshooting)

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────┐
│              Electron Desktop Application            │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         React Frontend (Renderer)             │  │
│  │  • Dashboard • Downloads • Parser              │  │
│  │  • Settings • Logs                              │  │
│  │                                                 │  │
│  │  HTTP Requests →                                │  │
│  └──────────────────────────────────────────────┘  │
│                      ↕                              │
│  ┌──────────────────────────────────────────────┐  │
│  │         Python FastAPI Backend                │  │
│  │  • Download Service                            │  │
│  │  • Parse Service                               │  │
│  │  • Pipeline Service                            │  │
│  │  • Database Service                            │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Communication Flow

1. **User Action** → React Component
2. **API Call** → `services/api.js` → HTTP Request
3. **Backend Processing** → FastAPI Endpoint → Service Layer
4. **Response** → JSON → React Component → UI Update

## 🔌 Backend API

### Base URL
- **Development**: `http://localhost:5001`
- **Production**: Same (backend runs locally)

### Key Endpoints

#### Download Endpoints

**Download Files for Date Range**
```http
POST /download/
Content-Type: application/json

{
  "start_date": "2024-11-29",
  "end_date": "2024-11-29",
  "urls": {},
  "raw_path": "/path/to/raw/files"
}
```

**Response:**
```json
{
  "success": true,
  "downloaded": ["fo_bhavcopy_2024-11-29.zip", ...],
  "missing": [],
  "error": null
}
```

**Download Single File**
```http
POST /download/single
Content-Type: application/json

{
  "file_type": "fo_bhavcopy",
  "date_str": "2024-11-29",
  "url": null,
  "raw_path": "/path/to/raw",
  "custom_urls": null
}
```

**Get Download Status**
```http
GET /download/status
```

**Retry Failed Download**
```http
POST /download/retry
Content-Type: application/json

{
  "download_id": 123
}
```

#### Other Endpoints

- `GET /health` - Health check
- `GET /settings/get` - Get settings
- `POST /settings/save` - Save settings
- `POST /parse/` - Parse files
- `POST /pipeline/run` - Run pipeline
- `GET /logs` - Get logs

See [API Test Results](API_TEST_RESULTS.md) for complete API documentation.

## 🎨 Frontend Components

### API Service Layer

All API calls are centralized in `electron/renderer/services/api.js`:

```javascript
// Example: Download files
const downloadFiles = async (startDate, endDate, rawPath) => {
  const response = await fetch('http://localhost:5001/download/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      start_date: startDate,
      end_date: endDate,
      urls: {},
      raw_path: rawPath
    })
  });
  return await response.json();
};
```

### Page Components

#### Dashboard (`pages/Dashboard.jsx`)
- Displays overview statistics
- Quick actions (Run Full Automation)
- Status cards

#### Downloads (`pages/Downloads.jsx`)
- Date range selection
- Download progress tracking
- File list display
- Retry failed downloads

#### Parser (`pages/Parser.jsx`)
- Path selection
- Parse progress
- Results display

#### Settings (`pages/Settings.jsx`)
- Folder path configuration
- Scheduler settings
- Path validation

#### Logs (`pages/Logs.jsx`)
- Real-time log display
- Log filtering
- Auto-refresh

## 🧪 Integration Testing

### Testing Download Flow

#### 1. Test Backend API Directly

```bash
# Set test date (use a known trading day)
TEST_DATE="2024-11-29"

# Test download endpoint
curl -X POST http://localhost:5001/download/ \
  -H "Content-Type: application/json" \
  -d "{
    \"start_date\": \"$TEST_DATE\",
    \"end_date\": \"$TEST_DATE\",
    \"urls\": {},
    \"raw_path\": \"/tmp/homestock_test\"
  }"
```

#### 2. Test via Frontend

1. Start the app: `npm start`
2. Go to **Downloads** page
3. Select date range
4. Click **Download Missing Files**
5. Monitor progress in UI

#### 3. Verify Downloads

```bash
# Check downloaded files
ls -lh /tmp/homestock_test/

# Should see files like:
# - fo_bhavcopy_2024-11-29.zip
# - cm_bhavcopy_2024-11-29.zip
# - combineoi_29112024.zip
# - MTO_29112024.DAT
```

### Testing All File Types

The application downloads **6 file types** for each date:

1. **fo_bhavcopy** - F&O Bhavcopy (Derivatives)
2. **cm_bhavcopy** - CM Bhavcopy (Equities)
3. **fo_udiff** - F&O Open Interest
4. **fo_participant_oi** - F&O Participant OI (same as fo_udiff)
5. **cm_delivery** - CM Delivery Data
6. **cm_udiff** - CM Bhavcopy (same as cm_bhavcopy)

## 📥 Download Testing Guide

### Prerequisites

1. **Backend Running**: `cd backend && make dev`
2. **Frontend Running**: `npm start` (or Electron window open)
3. **Test Directory**: Create a test directory for downloads

### Test Procedure

#### Step 1: Configure Settings

Via API:
```bash
curl -X POST http://localhost:5001/settings/save \
  -H "Content-Type: application/json" \
  -d '{
    "raw_path": "/tmp/homestock_test",
    "processed_path": "/tmp/homestock_processed",
    "output_path": "/tmp/homestock_output",
    "scheduler": "daily"
  }'
```

Via Frontend:
1. Open app → Settings page
2. Set folder paths
3. Click Save Settings

#### Step 2: Test Download

**Via API:**
```bash
TEST_DATE="2024-11-29"  # Use a known trading day

curl -X POST http://localhost:5001/download/ \
  -H "Content-Type: application/json" \
  -d "{
    \"start_date\": \"$TEST_DATE\",
    \"end_date\": \"$TEST_DATE\",
    \"urls\": {},
    \"raw_path\": \"/tmp/homestock_test\"
  }" | jq .
```

**Via Frontend:**
1. Go to Downloads page
2. Select date: `2024-11-29`
3. Click "Download Missing Files"
4. Watch progress

#### Step 3: Verify Files

```bash
# List downloaded files
ls -lh /tmp/homestock_test/

# Expected files:
# fo_bhavcopy_2024-11-29.zip
# cm_bhavcopy_2024-11-29.zip  
# fo_udiff_2024-11-29.zip
# fo_participant_oi_2024-11-29.zip
# cm_delivery_2024-11-29.DAT
# cm_udiff_2024-11-29.zip
```

#### Step 4: Check Download Status

```bash
curl http://localhost:5001/download/status | jq .
```

### Expected Behavior

1. **Success Case**:
   - Files download successfully
   - Status shows "completed"
   - Files appear in raw_path directory

2. **Missing Files** (Non-trading day):
   - Returns "missing" list
   - No error, just indicates files not available
   - This is normal for weekends/holidays

3. **Error Case**:
   - Network errors → Retry option available
   - Invalid paths → Error message displayed
   - Rate limiting → Automatic delays

## 🐛 Troubleshooting

### Downloads Not Working

**Check 1: Backend is Running**
```bash
curl http://localhost:5001/health
# Should return: {"status":"ok"}
```

**Check 2: Network Connectivity**
```bash
curl -I https://www.nseindia.com
# Should return HTTP response
```

**Check 3: Rate Limiting**
- Backend implements rate limiting (5 requests per 60 seconds)
- Downloads will automatically wait if rate limit exceeded

**Check 4: File Availability**
- NSE files are only available for trading days
- Weekends and holidays will return "missing"
- Files may take time to be published (check NSE website)

**Check 5: Logs**
```bash
# Backend logs
tail -f backend/logs/app.log

# Or via API
curl http://localhost:5001/logs | jq '.logs[-10:]'
```

### Frontend Not Connecting to Backend

**Check 1: CORS Configuration**
- Backend has CORS enabled for all origins
- Check `backend/app/main.py` for CORS settings

**Check 2: Backend URL**
- Frontend uses: `http://localhost:5001`
- Verify backend is running on this port

**Check 3: Network Errors**
- Open Electron DevTools (F12)
- Check Network tab for failed requests
- Check Console for errors

## 📊 Testing Checklist

### Backend Tests
- [ ] Health endpoint responds
- [ ] Settings can be saved and retrieved
- [ ] Download endpoint accepts requests
- [ ] Files are downloaded to correct location
- [ ] Download status tracking works
- [ ] Rate limiting is enforced

### Frontend Tests
- [ ] App loads and displays UI
- [ ] Navigation between pages works
- [ ] Settings page saves configuration
- [ ] Downloads page initiates downloads
- [ ] Progress is displayed
- [ ] Errors are shown to user

### Integration Tests
- [ ] Frontend can trigger backend downloads
- [ ] Download progress updates in real-time
- [ ] Files appear in configured directory
- [ ] All 6 file types are downloaded
- [ ] Error handling works end-to-end

## 📚 Related Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started
- [NSE Files Guide](NSE_FILES_README.md) - File types and formats
- [API Test Results](API_TEST_RESULTS.md) - Complete API reference
- [Pipeline Documentation](PIPELINE_DOCUMENTATION.md) - Full workflow
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Frontend details
- [Development Guide](DEVELOPMENT.md) - Development workflow

