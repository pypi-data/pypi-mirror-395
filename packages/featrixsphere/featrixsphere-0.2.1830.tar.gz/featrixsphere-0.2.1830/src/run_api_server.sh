#!/bin/bash
#
# Simple FastAPI Server Startup Script
# 
# This script just starts the FastAPI backend server on churro
# Referenced in supervisord-watchers.conf
#

set -e

# Configuration
APP_DIR="/sphere/app"
VENV_PATH="/sphere/.venv" 
API_HOST="0.0.0.0"
API_PORT="8000"

echo "=================================================================================="
echo "🚀 API SERVER STARTING - $(date -Iseconds)"
echo "=================================================================================="
echo "🚀 Starting Featrix Sphere FastAPI Server..."

# Change to app directory
cd "$APP_DIR"

# Activate virtual environment if it exists
if [ -f "$VENV_PATH/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
else
    echo "Warning: Virtual environment not found at $VENV_PATH"
fi

# Check if port 8000 is already in use and clear it if needed
check_port() {
    local port_in_use=false
    local pid=""
    
    # Try multiple methods to check if port is in use
    if command -v lsof >/dev/null 2>&1; then
        # Use lsof to check if port is in use
        pid=$(lsof -ti:$API_PORT 2>/dev/null || true)
        if [ -n "$pid" ]; then
            port_in_use=true
        fi
    elif command -v netstat >/dev/null 2>&1; then
        # Fallback to netstat
        if netstat -tuln 2>/dev/null | grep -q ":$API_PORT "; then
            port_in_use=true
            # Try to get PID from netstat (may not work on all systems)
            pid=$(netstat -tulnp 2>/dev/null | grep ":$API_PORT " | awk '{print $7}' | cut -d'/' -f1 | head -1 || true)
        fi
    elif command -v ss >/dev/null 2>&1; then
        # Fallback to ss
        if ss -tuln 2>/dev/null | grep -q ":$API_PORT "; then
            port_in_use=true
        fi
    fi
    
    if [ "$port_in_use" = true ]; then
        echo "⚠️  Port $API_PORT is already in use"
        
        # First, try to kill any uvicorn processes matching our pattern
        echo "   Checking for existing uvicorn processes..."
        if pkill -f "uvicorn.*api:create_app" 2>/dev/null; then
            echo "   ✅ Killed existing uvicorn processes"
            sleep 2
        fi
        
        # If we have a specific PID, check if it's still running
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "   Found process on port $API_PORT (PID: $pid)"
            # Check if it's a uvicorn/python process
            if ps -p "$pid" -o comm= 2>/dev/null | grep -qE "uvicorn|python"; then
                echo "   Killing uvicorn/python process $pid..."
                kill -TERM "$pid" 2>/dev/null || true
                sleep 2
                # Force kill if still running
                if kill -0 "$pid" 2>/dev/null; then
                    echo "   Process still running - force killing..."
                    kill -KILL "$pid" 2>/dev/null || true
                    sleep 1
                fi
                echo "   ✅ Cleared port $API_PORT"
            else
                echo "   ⚠️  Port is in use by non-uvicorn process (PID: $pid) - may need manual intervention"
                echo "   Attempting to start anyway - uvicorn will report the error if port is still in use"
            fi
        else
            # Port might be in TIME_WAIT state - wait a moment
            echo "   Port may be in TIME_WAIT state - waiting 2 seconds..."
            sleep 2
        fi
    fi
}

# Check and clear port before starting
check_port

# Start the FastAPI server
echo "Starting FastAPI server on $API_HOST:$API_PORT..."
echo "App directory: $APP_DIR"
echo "Python path: $(which python)"

# Use uvicorn with the factory pattern as defined in supervisord config
# Suppress uvicorn access logs - we have custom logging middleware in api.py
# No --reload flag in production - code changes require proper deployment/restart
exec uvicorn --factory api:create_app --host="$API_HOST" --port="$API_PORT" \
    --no-access-log --log-level info 