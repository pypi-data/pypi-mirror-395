#!/bin/bash
# Start Celery GPU training worker with concurrency from config file

set -e

echo "=================================================================================="
echo "🚀 CELERY GPU WORKER STARTING - $(date -Iseconds)"
echo "=================================================================================="

# Source virtual environment
source /sphere/.venv/bin/activate

# Read concurrency from config file (set by install script)
CONFIG_FILE="/sphere/app/.celery_gpu_concurrency"
if [ -f "$CONFIG_FILE" ]; then
    CONCURRENCY=$(cat "$CONFIG_FILE" | tr -d '[:space:]')
else
    # Fallback: detect GPU capacity
    if command -v nvidia-smi >/dev/null 2>&1; then
        GPU_COUNT=$(nvidia-smi -L | wc -l)
        if [ "$GPU_COUNT" -ge 2 ]; then
            CONCURRENCY=2
        else
            CONCURRENCY=1
        fi
    else
        CONCURRENCY=1
    fi
fi

# Start Celery worker
exec celery -A celery_app worker \
    --loglevel=info \
    --concurrency=$CONCURRENCY \
    --queues=gpu_training \
    --hostname=celery-gpu_training@$(hostname -s) \
    --prefetch-multiplier=1

