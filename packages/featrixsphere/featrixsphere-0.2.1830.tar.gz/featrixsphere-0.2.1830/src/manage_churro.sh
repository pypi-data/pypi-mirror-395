#!/bin/bash
#
# Churro Server Management Script
#
# Simple script for common churro server management tasks
#
# Usage: ./manage_churro.sh {status|logs|restart|stop|start|test}
#

CHURRO_HOST="root@75.150.77.37"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SECTION]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

case "${1:-status}" in
    "status")
        print_section "Checking churro server status..."
        ssh "$CHURRO_HOST" "supervisorctl status"
        echo
        print_status "API server port check:"
        ssh "$CHURRO_HOST" "netstat -ln | grep :8000 || echo 'Port 8000 not listening'"
        ;;
        
    "logs")
        service="${2:-api_server}"
        print_section "Showing logs for $service..."
        ssh "$CHURRO_HOST" "supervisorctl tail -f $service"
        ;;
        
    "restart")
        service="${2:-all}"
        print_section "Restarting $service..."
        ssh "$CHURRO_HOST" "supervisorctl restart $service"
        sleep 2
        ssh "$CHURRO_HOST" "supervisorctl status"
        ;;
        
    "stop")
        service="${2:-all}"
        print_section "Stopping $service..."
        ssh "$CHURRO_HOST" "supervisorctl stop $service"
        ssh "$CHURRO_HOST" "supervisorctl status"
        ;;
        
    "start")
        service="${2:-all}"
        print_section "Starting $service..."
        ssh "$CHURRO_HOST" "supervisorctl start $service"
        sleep 2
        ssh "$CHURRO_HOST" "supervisorctl status"
        ;;
        
    "test")
        print_section "Testing API endpoint..."
        echo "Testing: http://75.150.77.37:8000/docs"
        curl -f -s "http://75.150.77.37:8000/docs" > /dev/null && \
            print_status "✅ API server responding" || \
            print_error "❌ API server not responding"
        
        echo
        echo "Testing: https://sphere-api.featrix.com/compute/session/test"
        curl -f -s "https://sphere-api.featrix.com/compute/session/test" > /dev/null && \
            print_status "✅ Proxy connection working" || \
            print_error "❌ Proxy connection failed"
        ;;
        
    "deploy")
        print_section "Quick deployment (restart only)..."
        cd "$(dirname "$0")"
        if [ -f "churro-copy.sh" ]; then
            print_status "Copying files to churro and restarting services..."
            scp churro-copy.sh "$CHURRO_HOST:/tmp/"
            scp *.py "$CHURRO_HOST:/tmp/"
            if [ -d "lib" ]; then
                scp -r lib "$CHURRO_HOST:/tmp/"
            fi
            ssh "$CHURRO_HOST" "cd /tmp && chmod +x churro-copy.sh && sudo ./churro-copy.sh --restart-only"
        else
            print_error "churro-copy.sh not found"
            exit 1
        fi
        ;;
        
    *)
        echo "Churro Server Management"
        echo "Usage: $0 {status|logs|restart|stop|start|test|deploy} [service]"
        echo
        echo "Commands:"
        echo "  status      - Show service status"
        echo "  logs [svc]  - Show logs (default: api_server)"
        echo "  restart [svc] - Restart service (default: all)"
        echo "  stop [svc]  - Stop service (default: all)"
        echo "  start [svc] - Start service (default: all)"
        echo "  test        - Test API endpoints"
        echo "  deploy      - Copy files and restart services"
        echo
        echo "Services:"
        echo "  all, api_server, worker-train_es, worker-train_single_predictor,"
        echo "  worker-create_sd, worker-train_knn, worker-run_clustering"
        echo
        echo "Examples:"
        echo "  $0 status"
        echo "  $0 logs api_server"
        echo "  $0 restart worker-train_single_predictor"
        echo "  $0 test"
        echo "  $0 deploy"
        exit 1
        ;;
esac 