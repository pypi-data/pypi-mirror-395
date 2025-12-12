#!/bin/bash
# Start Celery CPU worker

set -e

echo "=================================================================================="
echo "🚀 CELERY CPU WORKER STARTING - $(date -Iseconds)"
echo "=================================================================================="

# Source virtual environment
source /sphere/.venv/bin/activate

# Start Celery worker
exec celery -A celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=cpu_worker,predictions \
    --hostname=celery-cpu_worker@$(hostname -s) \
    --prefetch-multiplier=1

