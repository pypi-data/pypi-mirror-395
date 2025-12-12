#!/bin/bash
#
# Featrix Sphere Churro Server Startup Script
# 
# This script starts the FastAPI backend server and all worker processes
# on the churro server (75.150.77.37:8000)
#

set -e  # Exit on any error

# Configuration
APP_DIR="/sphere/app"
VENV_PATH="/sphere/.venv"
LOG_DIR="/var/log/featrix"
API_HOST="0.0.0.0"
API_PORT="8000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 Featrix Sphere Churro Server Startup${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a process is running
check_process() {
    if pgrep -f "$1" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to stop existing processes
stop_existing_processes() {
    print_status "Stopping existing processes..."
    
    # Stop supervisor processes
    if command -v supervisorctl > /dev/null; then
        print_status "Stopping supervisor processes..."
        supervisorctl stop all || print_warning "Some supervisor processes may not have been running"
    fi
    
    # Kill any remaining processes
    pkill -f "uvicorn.*api:create_app" || true
    # File-based queue workers removed - now using Celery workers
    # pkill -f "python.*cli.py.*watch-queue" || true
    
    sleep 2
    print_status "Existing processes stopped"
}

# Function to create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    
    # Create log directory
    sudo mkdir -p "$LOG_DIR"
    sudo chown root:root "$LOG_DIR"
    
    # Ensure app directory exists
    if [ ! -d "$APP_DIR" ]; then
        print_error "App directory $APP_DIR does not exist!"
        exit 1
    fi
    
    print_status "Directories ready"
}

# Function to activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    
    if [ ! -f "$VENV_PATH/bin/activate" ]; then
        print_error "Virtual environment not found at $VENV_PATH"
        print_error "Please create it first: python -m venv $VENV_PATH"
        exit 1
    fi
    
    source "$VENV_PATH/bin/activate"
    print_status "Virtual environment activated"
}

# Function to start with supervisor
start_with_supervisor() {
    print_status "Starting services with supervisor..."
    
    # Copy supervisor config
    # Find supervisord-watchers.conf in multiple locations
    CONFIG_FILE=""
    if [ -f "$APP_DIR/supervisord-watchers.conf" ]; then
        CONFIG_FILE="$APP_DIR/supervisord-watchers.conf"
    elif [ -f "$APP_DIR/src/supervisord-watchers.conf" ]; then
        CONFIG_FILE="$APP_DIR/src/supervisord-watchers.conf"
    elif [ -f "src/supervisord-watchers.conf" ]; then
        CONFIG_FILE="src/supervisord-watchers.conf"
    elif [ -f "supervisord-watchers.conf" ]; then
        CONFIG_FILE="supervisord-watchers.conf"
    fi
    
    if [ -n "$CONFIG_FILE" ] && [ -f "$CONFIG_FILE" ]; then
        echo "📋 Copying supervisor config from: $CONFIG_FILE"
        sudo cp "$CONFIG_FILE" /etc/supervisor/conf.d/
        print_status "Supervisor config updated"
    fi
    
    # Reload supervisor
    sudo supervisorctl reread
    sudo supervisorctl update
    
    # Start all services
    print_status "Starting all supervisor services..."
    sudo supervisorctl start all
    
    # Show status
    print_status "Service status:"
    sudo supervisorctl status
}

# Function to start manually (fallback)
start_manual() {
    print_status "Starting services manually..."
    
    cd "$APP_DIR"
    
    # Start API server in background
    print_status "Starting FastAPI server on $API_HOST:$API_PORT..."
    nohup uvicorn --factory api:create_app --host="$API_HOST" --port="$API_PORT" > "$LOG_DIR/api_server.log" 2>&1 &
    API_PID=$!
    echo $API_PID > "$LOG_DIR/api_server.pid"
    
    # Workers are now handled by Celery via supervisor
    # File-based queue workers (cli.py watch-queue) have been removed
    print_status "Workers are managed by Celery via supervisor (no manual workers needed)"
    
    print_status "All services started manually"
    print_status "Logs are in: $LOG_DIR"
    print_status "API server PID: $API_PID"
}

# Function to show status
show_status() {
    print_status "Checking service status..."
    
    echo ""
    echo -e "${BLUE}=== Service Status ===${NC}"
    
    # Check API server
    if check_process "uvicorn.*api:create_app"; then
        echo -e "${GREEN}✅ API Server: Running${NC}"
    else
        echo -e "${RED}❌ API Server: Not running${NC}"
    fi
    
    # Workers are now handled by Celery via supervisor
    # Check Celery workers instead
    if check_process "celery.*worker"; then
        echo -e "${GREEN}✅ Celery Workers: Running${NC}"
    else
        echo -e "${RED}❌ Celery Workers: Not running${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}=== Network Status ===${NC}"
    if netstat -ln | grep ":8000" > /dev/null; then
        echo -e "${GREEN}✅ Port 8000: Listening${NC}"
    else
        echo -e "${RED}❌ Port 8000: Not listening${NC}"
    fi
}

# Main function
main() {
    case "${1:-start}" in
        "start")
            print_status "Starting Featrix Sphere services..."
            stop_existing_processes
            setup_directories
            activate_venv
            
            # Try supervisor first, fall back to manual
            if command -v supervisorctl > /dev/null; then
                start_with_supervisor
            else
                print_warning "Supervisor not available, starting manually"
                start_manual
            fi
            
            sleep 3
            show_status
            print_status "Startup complete! API available at http://75.150.77.37:8000"
            ;;
            
        "stop")
            print_status "Stopping all services..."
            stop_existing_processes
            print_status "All services stopped"
            ;;
            
        "restart")
            print_status "Restarting services..."
            "$0" stop
            sleep 2
            "$0" start
            ;;
            
        "status")
            show_status
            ;;
            
        "logs")
            print_status "Showing recent logs..."
            if [ -d "$LOG_DIR" ]; then
                tail -f "$LOG_DIR"/*.log
            else
                print_error "Log directory not found: $LOG_DIR"
            fi
            ;;
            
        *)
            echo "Usage: $0 {start|stop|restart|status|logs}"
            echo ""
            echo "Commands:"
            echo "  start   - Start all services (API server + workers)"
            echo "  stop    - Stop all services"
            echo "  restart - Restart all services" 
            echo "  status  - Show service status"
            echo "  logs    - Tail all log files"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 