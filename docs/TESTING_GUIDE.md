# Testing Guide

Complete testing guide for HomeStock covering both frontend and backend.

## 🧪 Testing Overview

### Backend Testing

#### API Endpoints
```bash
cd backend
./test_api.sh
```

#### Download Functionality
```bash
cd backend
./test_download.sh
```

#### Unit Tests
```bash
cd backend
make test
```

### Frontend Testing

#### Manual Testing
1. Start the app: `npm start`
2. Test each page:
   - Dashboard - Check status display
   - Downloads - Test download flow
   - Parser - Test parsing
   - Settings - Test configuration
   - Logs - Check log display

#### Integration Testing
1. Start backend: `cd backend && make dev`
2. Start frontend: `npm run dev:react`
3. Launch Electron: `npx electron . --dev`
4. Test complete workflows

## 📥 Download Testing

### Testing All File Types

HomeStock downloads **6 file types** for each date:

1. **fo_bhavcopy** - F&O Bhavcopy (Derivatives Market Data)
2. **cm_bhavcopy** - CM Bhavcopy (Cash Market Equity Data)
3. **fo_udiff** - F&O Open Interest (Combined OI)
4. **fo_participant_oi** - F&O Participant OI (same as fo_udiff)
5. **cm_delivery** - CM Delivery Data (Market Turnover)
6. **cm_udiff** - CM Bhavcopy (same as cm_bhavcopy)

### Test Procedure

#### Step 1: Setup
```bash
# Create test directory
mkdir -p /tmp/homestock_test

# Configure settings
curl -X POST http://localhost:5001/settings/save \
  -H "Content-Type: application/json" \
  -d '{
    "raw_path": "/tmp/homestock_test",
    "processed_path": "/tmp/homestock_processed",
    "output_path": "/tmp/homestock_output",
    "scheduler": "daily"
  }'
```

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
1. Open app → Downloads page
2. Select date range
3. Click "Download Missing Files"
4. Monitor progress

#### Step 3: Verify Files

```bash
# List downloaded files
ls -lh /tmp/homestock_test/

# Expected files (if download successful):
# - fo_bhavcopy_2024-11-29.zip
# - cm_bhavcopy_2024-11-29.zip
# - fo_udiff_2024-11-29.zip
# - fo_participant_oi_2024-11-29.zip
# - cm_delivery_2024-11-29.DAT
# - cm_udiff_2024-11-29.zip
```

### Expected Behavior

#### Success Case
- Files download successfully
- Status shows "completed"
- Files appear in raw_path directory
- All 6 file types downloaded

#### Missing Files (Normal)
- Non-trading days (weekends/holidays) → Files marked as "missing"
- Files not yet published → Marked as "missing"
- This is expected behavior, not an error

#### Error Case
- Network errors → Retry available
- Invalid paths → Error message
- Rate limiting → Automatic delays

## 🔍 Verification Checklist

### Backend Verification
- [ ] Health endpoint responds
- [ ] Settings can be saved/retrieved
- [ ] Download endpoint accepts requests
- [ ] All 6 file types are attempted
- [ ] Download status tracking works
- [ ] Rate limiting is enforced
- [ ] Error handling works

### Frontend Verification
- [ ] App loads and displays UI
- [ ] Navigation works
- [ ] Settings page saves configuration
- [ ] Downloads page initiates downloads
- [ ] Progress is displayed
- [ ] Errors are shown to user
- [ ] All pages are accessible

### Integration Verification
- [ ] Frontend can trigger backend downloads
- [ ] Download progress updates in real-time
- [ ] Files appear in configured directory
- [ ] All file types are attempted
- [ ] Error handling works end-to-end

## 📊 Test Results

### Current Status

**Backend API**: ✅ Working
- All endpoints responding correctly
- Error handling functional
- Rate limiting active

**Download System**: ⚠️ Functional but may show "missing"
- All 6 file types are attempted
- URLs are generated correctly
- Downloads may fail if:
  - Date is non-trading day
  - Files not yet published
  - NSE requires authentication

**Frontend**: ✅ Working
- UI loads correctly
- All pages accessible
- API integration functional

## 🐛 Known Issues

1. **NSE File Availability**
   - Files may not be available for future dates
   - Files may require authentication/cookies
   - Files may take time to be published

2. **Date Handling**
   - System uses current date
   - May need to use past trading days for testing
   - Weekends/holidays will show as "missing"

## 📚 Related Documentation

- [Frontend & Backend Integration Guide](FRONTEND_BACKEND_GUIDE.md)
- [Development Guide](DEVELOPMENT.md)
- [NSE Files Guide](NSE_FILES_README.md)
- [API Test Results](API_TEST_RESULTS.md)

