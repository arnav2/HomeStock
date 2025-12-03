#!/bin/bash

# Test script for downloading NSE files
# Tests all file types mentioned in documentation

BACKEND_URL="http://localhost:5001"
TEST_DIR="/tmp/homestock_test_download"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo "NSE Download Test Script"
echo "=========================================="
echo ""

# Get a recent trading day
echo -e "${YELLOW}Finding recent trading day...${NC}"
TEST_DATE=$(python3 -c "
from datetime import datetime, timedelta
today = datetime.now()
for i in range(7):
    test_date = today - timedelta(days=i)
    if test_date.weekday() < 5:
        print(test_date.strftime('%Y-%m-%d'))
        break
")

if [ -z "$TEST_DATE" ]; then
    echo -e "${RED}❌ Could not find a trading day${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Testing with date: $TEST_DATE${NC}"
echo ""

# Create test directory
mkdir -p "$TEST_DIR"
echo -e "${YELLOW}Test directory: $TEST_DIR${NC}"
echo ""

# Test download endpoint
echo -e "${YELLOW}[1/6] Testing Download Endpoint...${NC}"
DOWNLOAD_RESPONSE=$(curl -s -X POST "$BACKEND_URL/download/" \
    -H "Content-Type: application/json" \
    -d "{
        \"start_date\": \"$TEST_DATE\",
        \"end_date\": \"$TEST_DATE\",
        \"urls\": {},
        \"raw_path\": \"$TEST_DIR\"
    }")

echo "$DOWNLOAD_RESPONSE" | jq .

DOWNLOADED_COUNT=$(echo "$DOWNLOAD_RESPONSE" | jq -r '.downloaded | length')
MISSING_COUNT=$(echo "$DOWNLOAD_RESPONSE" | jq -r '.missing | length')

echo ""
echo -e "Downloaded: ${GREEN}$DOWNLOADED_COUNT${NC} files"
echo -e "Missing: ${YELLOW}$MISSING_COUNT${NC} files"
echo ""

# Check what files were actually downloaded
echo -e "${YELLOW}[2/6] Checking Downloaded Files...${NC}"
if [ -d "$TEST_DIR" ]; then
    FILE_COUNT=$(ls -1 "$TEST_DIR" 2>/dev/null | wc -l | tr -d ' ')
    echo -e "Files in directory: ${GREEN}$FILE_COUNT${NC}"
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo ""
        echo "Downloaded files:"
        ls -lh "$TEST_DIR" | tail -n +2 | awk '{print "  - " $9 " (" $5 ")"}'
    fi
else
    echo -e "${RED}❌ Test directory not found${NC}"
fi
echo ""

# Test individual file types
echo -e "${YELLOW}[3/6] Testing Individual File Types...${NC}"
FILE_TYPES=("fo_bhavcopy" "cm_bhavcopy" "fo_udiff" "cm_delivery" "cm_udiff" "fo_participant_oi")

for file_type in "${FILE_TYPES[@]}"; do
    echo -n "  Testing $file_type... "
    RESPONSE=$(curl -s -X POST "$BACKEND_URL/download/single" \
        -H "Content-Type: application/json" \
        -d "{
            \"file_type\": \"$file_type\",
            \"date_str\": \"$TEST_DATE\",
            \"url\": null,
            \"raw_path\": \"$TEST_DIR\",
            \"custom_urls\": null
        }")
    
    SUCCESS=$(echo "$RESPONSE" | jq -r '.success')
    if [ "$SUCCESS" = "true" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        ERROR=$(echo "$RESPONSE" | jq -r '.error // "File not available"')
        echo -e "${YELLOW}⚠️  ($ERROR)${NC}"
    fi
done
echo ""

# Check download status
echo -e "${YELLOW}[4/6] Checking Download Status...${NC}"
STATUS=$(curl -s "$BACKEND_URL/download/status")
DOWNLOAD_COUNT=$(echo "$STATUS" | jq -r '.downloads | length')
echo -e "Active downloads: ${GREEN}$DOWNLOAD_COUNT${NC}"
echo ""

# Verify expected file types
echo -e "${YELLOW}[5/6] Expected File Types (from documentation)...${NC}"
echo "  1. fo_bhavcopy - F&O Bhavcopy (Derivatives)"
echo "  2. cm_bhavcopy - CM Bhavcopy (Equities)"
echo "  3. fo_udiff - F&O Open Interest"
echo "  4. fo_participant_oi - F&O Participant OI"
echo "  5. cm_delivery - CM Delivery Data"
echo "  6. cm_udiff - CM Bhavcopy (same as cm_bhavcopy)"
echo ""

# Summary
echo -e "${YELLOW}[6/6] Test Summary${NC}"
echo "=========================================="
echo "Test Date: $TEST_DATE"
echo "Test Directory: $TEST_DIR"
echo "Downloaded Files: $DOWNLOADED_COUNT"
echo "Missing Files: $MISSING_COUNT"
echo ""
echo "Note: Files may show as 'missing' if:"
echo "  - Date is a non-trading day (weekend/holiday)"
echo "  - Files are not yet published by NSE"
echo "  - NSE website requires authentication"
echo ""
echo "To verify downloads manually:"
echo "  ls -lh $TEST_DIR"
echo ""

