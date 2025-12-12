#!/bin/bash
#
# Quick Test Script for Churro Deployment
#
# Run this script on churro to verify the deployment is working
#

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SECTION]${NC} $1"
}

echo -e "${BLUE}===========================================${NC}"
echo -e "${BLUE}🧪 Churro Deployment Quick Test${NC}"
echo -e "${BLUE}===========================================${NC}"
echo

# Test 1: Check directories exist
print_section "1. Checking directory structure..."
if [ -d "/sphere/app" ]; then
    print_status "✅ /sphere/app exists"
    ls -la /sphere/app | head -5
else
    print_error "❌ /sphere/app missing"
    exit 1
fi

if [ -d "/sphere/.venv" ]; then
    print_status "✅ /sphere/.venv exists"
else
    print_error "❌ /sphere/.venv missing"
    exit 1
fi

if [ -d "/var/log/featrix" ]; then
    print_status "✅ /var/log/featrix exists"
    ls -la /var/log/featrix/
else
    print_error "❌ /var/log/featrix missing"
    exit 1
fi

# Test 2: Check virtual environment
print_section "2. Testing virtual environment..."
if [ -f "/sphere/.venv/bin/activate" ]; then
    print_status "✅ Virtual environment activate script exists"
    
    # Test activation and imports
    source /sphere/.venv/bin/activate
    
    print_status "Testing Python imports..."
    python -c "
import sys
sys.path.insert(0, '/sphere/app')

try:
    import fastapi
    print('✅ FastAPI OK')
except Exception as e:
    print(f'❌ FastAPI failed: {e}')
    sys.exit(1)

try:
    import uvicorn
    print('✅ Uvicorn OK')
except Exception as e:
    print(f'❌ Uvicorn failed: {e}')
    sys.exit(1)

try:
    import api
    print('✅ API module OK')
except Exception as e:
    print(f'❌ API module failed: {e}')
    sys.exit(1)
"
    deactivate
else
    print_error "❌ Virtual environment activation script missing"
    exit 1
fi

# Test 3: Check supervisor status
print_section "3. Checking supervisor services..."
supervisor_status=$(supervisorctl status)
echo "$supervisor_status"

# Count running services
running_count=$(echo "$supervisor_status" | grep "RUNNING" | wc -l)
total_count=$(echo "$supervisor_status" | wc -l)

print_status "Services running: $running_count/$total_count"

if [ "$running_count" -eq 0 ]; then
    print_error "❌ No services are running"
    print_status "Attempting to start services..."
    supervisorctl start all
    sleep 5
    supervisorctl status
else
    print_status "✅ Some services are running"
fi

# Test 4: Check if API server is responding
print_section "4. Testing API server..."
if curl -f -s http://localhost:8000/docs > /dev/null 2>&1; then
    print_status "✅ API server is responding"
    
    # Test the health endpoint
    if curl -f -s http://localhost:8000/session/test > /dev/null 2>&1; then
        print_status "✅ Health endpoint working"
    else
        print_warning "⚠️  Health endpoint not responding"
    fi
else
    print_error "❌ API server not responding"
    print_status "Recent API server logs:"
    supervisorctl tail -20 api_server
fi

# Test 5: Check port 8000
print_section "5. Checking port 8000..."
if netstat -ln | grep ":8000" > /dev/null; then
    print_status "✅ Port 8000 is listening"
    netstat -ln | grep ":8000"
else
    print_error "❌ Port 8000 not listening"
fi

# Test 6: Test new single predictor endpoint structure
print_section "6. Testing single predictor endpoint structure..."
api_response=$(curl -s -w "%{http_code}" -X POST http://localhost:8000/session/test_session_id/train_predictor \
    -H "Content-Type: application/json" \
    -d '{"target_column": "test", "target_column_type": "set", "epochs": 1}' \
    -o /dev/null 2>/dev/null || echo "000")

if [ "$api_response" = "404" ]; then
    print_status "✅ Single predictor endpoint exists (404 = session not found, which is expected)"
elif [ "$api_response" = "422" ]; then
    print_status "✅ Single predictor endpoint exists (422 = validation error, which is expected)"  
elif [ "$api_response" = "000" ]; then
    print_error "❌ Could not connect to API server"
else
    print_status "🤔 Single predictor endpoint response: $api_response"
fi

print_section "Test Summary"
echo
echo -e "${GREEN}🎉 Deployment test completed!${NC}"
echo
echo -e "${BLUE}📋 Next steps:${NC}"
echo "   1. Upload test data via sphere-api.featrix.com"
echo "   2. Train an embedding space"
echo "   3. Test single predictor training"
echo
echo -e "${BLUE}🔧 Management commands:${NC}"
echo "   • Status: supervisorctl status"
echo "   • Logs: supervisorctl tail -f api_server"
echo "   • Restart: supervisorctl restart all"
echo 