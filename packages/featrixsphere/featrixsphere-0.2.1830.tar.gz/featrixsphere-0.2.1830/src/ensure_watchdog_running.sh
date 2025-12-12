#!/bin/bash
#
# Ensure featrix-watchdog is configured and running in supervisor
#

set -e

SUPERVISOR_CONFIG="/etc/supervisor/conf.d/featrix-sphere.conf"
WATCHDOG_CONFIG="[program:featrix-watchdog]
command=/usr/bin/python3 /sphere/app/src/featrix_watchdog.py --interval 60 --stuck-threshold 300
directory=/sphere/app
user=root
autostart=true
autorestart=true
startretries=3
redirect_stderr=true
stdout_logfile=/var/log/featrix/featrix_watchdog.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
stderr_logfile=/var/log/featrix/featrix_watchdog_error.log
stderr_logfile_maxbytes=10MB
stderr_logfile_backups=3
environment=PYTHONPATH=\"/sphere/app:/sphere/app/src\",PYTHONUNBUFFERED=1
priority=998"

echo "🔍 Checking if featrix-watchdog is configured..."

# Check if watchdog is in the config
if grep -q "^\[program:featrix-watchdog\]" "$SUPERVISOR_CONFIG" 2>/dev/null; then
    echo "✅ featrix-watchdog is already in supervisor config"
else
    echo "⚠️  featrix-watchdog NOT found in supervisor config"
    echo "📝 Adding featrix-watchdog to supervisor config..."
    
    # Backup the config
    cp "$SUPERVISOR_CONFIG" "${SUPERVISOR_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Append watchdog config to the file
    echo "" >> "$SUPERVISOR_CONFIG"
    echo "$WATCHDOG_CONFIG" >> "$SUPERVISOR_CONFIG"
    
    echo "✅ Added featrix-watchdog to supervisor config"
fi

# Check if supervisor can see it
echo ""
echo "🔍 Checking supervisor status..."
if supervisorctl status featrix-watchdog >/dev/null 2>&1; then
    echo "✅ featrix-watchdog is registered in supervisor"
    STATUS=$(supervisorctl status featrix-watchdog | awk '{print $2}')
    if [ "$STATUS" = "RUNNING" ]; then
        echo "✅ featrix-watchdog is RUNNING"
    else
        echo "⚠️  featrix-watchdog status: $STATUS"
        echo "🔄 Reloading supervisor and starting watchdog..."
        supervisorctl reread
        supervisorctl update
        supervisorctl start featrix-watchdog
        sleep 2
        supervisorctl status featrix-watchdog
    fi
else
    echo "⚠️  featrix-watchdog not found in supervisor"
    echo "🔄 Reloading supervisor configuration..."
    supervisorctl reread
    supervisorctl update
    sleep 2
    
    if supervisorctl status featrix-watchdog >/dev/null 2>&1; then
        echo "✅ featrix-watchdog is now registered"
        supervisorctl start featrix-watchdog
        sleep 2
        supervisorctl status featrix-watchdog
    else
        echo "❌ Failed to register featrix-watchdog"
        echo "📋 Current supervisor programs:"
        supervisorctl status
        exit 1
    fi
fi

echo ""
echo "✅ Done! featrix-watchdog should now be running."
echo "📊 Check status with: supervisorctl status featrix-watchdog"
echo "📋 View logs with: tail -f /var/log/featrix/featrix_watchdog.log"

