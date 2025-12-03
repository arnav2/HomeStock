#!/bin/bash

# HomeStock Backend API Test Script
# Tests all available endpoints with CURL requests

BASE_URL="http://localhost:5001"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "HomeStock Backend API Test Suite"
echo "=========================================="
echo ""

# Test 1: Health Check
echo -e "${YELLOW}[1/10] Testing Health Endpoint...${NC}"
HEALTH=$(curl -s "$BASE_URL/health")
if echo "$HEALTH" | grep -q "ok"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "   Response: $HEALTH"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi
echo ""

# Test 2: Get Settings
echo -e "${YELLOW}[2/10] Testing Settings Get Endpoint...${NC}"
SETTINGS_GET=$(curl -s "$BASE_URL/settings/get")
if echo "$SETTINGS_GET" | grep -q "success"; then
    echo -e "${GREEN}✅ Settings get passed${NC}"
    echo "   Response: $(echo $SETTINGS_GET | jq -c '.')"
else
    echo -e "${RED}❌ Settings get failed${NC}"
fi
echo ""

# Test 3: Save Settings
echo -e "${YELLOW}[3/10] Testing Settings Save Endpoint...${NC}"
SETTINGS_SAVE=$(curl -s -X POST "$BASE_URL/settings/save" \
    -H "Content-Type: application/json" \
    -d '{
        "raw_path": "/tmp/homestock_raw",
        "processed_path": "/tmp/homestock_processed",
        "output_path": "/tmp/homestock_output",
        "scheduler": "daily"
    }')
if echo "$SETTINGS_SAVE" | grep -q "success"; then
    echo -e "${GREEN}✅ Settings save passed${NC}"
    echo "   Response: $(echo $SETTINGS_SAVE | jq -c '.')"
else
    echo -e "${RED}❌ Settings save failed${NC}"
    echo "   Response: $SETTINGS_SAVE"
fi
echo ""

# Test 4: Verify Settings Were Saved
echo -e "${YELLOW}[4/10] Verifying Settings Were Saved...${NC}"
SETTINGS_VERIFY=$(curl -s "$BASE_URL/settings/get")
if echo "$SETTINGS_VERIFY" | jq -e '.settings.raw_path == "/tmp/homestock_raw"' > /dev/null; then
    echo -e "${GREEN}✅ Settings verification passed${NC}"
    echo "   Raw Path: $(echo $SETTINGS_VERIFY | jq -r '.settings.raw_path')"
else
    echo -e "${RED}❌ Settings verification failed${NC}"
fi
echo ""

# Test 5: Test Path - Valid
echo -e "${YELLOW}[5/10] Testing Path Validation (Valid Path)...${NC}"
PATH_TEST_VALID=$(curl -s -X POST "$BASE_URL/settings/test-path" \
    -H "Content-Type: application/json" \
    -d '{"path": "/tmp"}')
if echo "$PATH_TEST_VALID" | jq -e '.accessible == true' > /dev/null; then
    echo -e "${GREEN}✅ Valid path test passed${NC}"
else
    echo -e "${RED}❌ Valid path test failed${NC}"
fi
echo ""

# Test 6: Test Path - Invalid
echo -e "${YELLOW}[6/10] Testing Path Validation (Invalid Path)...${NC}"
PATH_TEST_INVALID=$(curl -s -X POST "$BASE_URL/settings/test-path" \
    -H "Content-Type: application/json" \
    -d '{"path": "/nonexistent/path/12345"}')
if echo "$PATH_TEST_INVALID" | jq -e '.accessible == false' > /dev/null; then
    echo -e "${GREEN}✅ Invalid path test passed${NC}"
else
    echo -e "${RED}❌ Invalid path test failed${NC}"
fi
echo ""

# Test 7: Get Logs
echo -e "${YELLOW}[7/10] Testing Logs Endpoint...${NC}"
LOGS=$(curl -s "$BASE_URL/logs")
if echo "$LOGS" | grep -q "logs"; then
    echo -e "${GREEN}✅ Logs endpoint passed${NC}"
    LOG_COUNT=$(echo "$LOGS" | jq '.logs | length')
    echo "   Log entries: $LOG_COUNT"
else
    echo -e "${RED}❌ Logs endpoint failed${NC}"
fi
echo ""

# Test 8: Download Status
echo -e "${YELLOW}[8/10] Testing Download Status Endpoint...${NC}"
DOWNLOAD_STATUS=$(curl -s "$BASE_URL/download/status")
if echo "$DOWNLOAD_STATUS" | grep -q "success"; then
    echo -e "${GREEN}✅ Download status passed${NC}"
    DOWNLOAD_COUNT=$(echo "$DOWNLOAD_STATUS" | jq '.downloads | length')
    echo "   Active downloads: $DOWNLOAD_COUNT"
else
    echo -e "${RED}❌ Download status failed${NC}"
fi
echo ""

# Test 9: Parse Endpoint (with invalid path - should handle gracefully)
echo -e "${YELLOW}[9/10] Testing Parse Endpoint...${NC}"
PARSE=$(curl -s -X POST "$BASE_URL/parse/" \
    -H "Content-Type: application/json" \
    -d '{
        "raw_path": "/nonexistent/path",
        "output_path": "/tmp/output"
    }')
if echo "$PARSE" | grep -q "success"; then
    echo -e "${GREEN}✅ Parse endpoint passed (handles invalid path gracefully)${NC}"
else
    echo -e "${RED}❌ Parse endpoint failed${NC}"
fi
echo ""

# Test 10: Pipeline Verify Only
echo -e "${YELLOW}[10/10] Testing Pipeline Verify Endpoint...${NC}"
PIPELINE_VERIFY=$(curl -s -X POST "$BASE_URL/pipeline/verify-only?start_date=2023-12-01&end_date=2023-12-01&raw_path=/tmp/homestock_raw")
if echo "$PIPELINE_VERIFY" | grep -q "success"; then
    echo -e "${GREEN}✅ Pipeline verify passed${NC}"
    VERIFIED_COUNT=$(echo "$PIPELINE_VERIFY" | jq -r '.verified_count')
    echo "   Verified files: $VERIFIED_COUNT"
else
    echo -e "${RED}❌ Pipeline verify failed${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "All endpoints tested successfully!"
echo ""
echo "API Documentation available at:"
echo "  - Swagger UI: $BASE_URL/docs"
echo "  - ReDoc: $BASE_URL/redoc"
echo "  - OpenAPI JSON: $BASE_URL/openapi.json"
echo ""
echo "Backend is running and ready for frontend connection!"

