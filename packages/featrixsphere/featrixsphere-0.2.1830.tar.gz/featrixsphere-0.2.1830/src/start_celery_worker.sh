#!/bin/bash
#
# Start Celery worker for prediction jobs
# This script should be run from the src/ directory
#

echo "🚀 Starting Celery worker for prediction jobs..."

# Activate virtual environment (critical for pickle compatibility!)
VENV_PATH="/sphere/.venv"
if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activating virtual environment: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment activated"
    echo "   Python: $(which python)"
    echo "   Pip packages: $(pip list | wc -l) packages installed"
else
    echo "⚠️  Virtual environment not found at $VENV_PATH"
    echo "   Using system Python: $(which python)"
    echo "   This may cause pickle import issues!"
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Please start Redis first:"
    echo "   brew services start redis  # macOS"
    echo "   sudo systemctl start redis  # Linux"
    exit 1
fi

echo "✅ Redis is running"

# Check GPU memory status
if command -v nvidia-smi > /dev/null 2>&1; then
    echo "📊 GPU memory status before starting worker:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "   GPU Memory: " $1 " MB / " $2 " MB (" int($1/$2*100) "% used)"}'
fi

# Set environment variables for better memory management
export PYTHONPATH="$(pwd):$(pwd)/lib:$PYTHONPATH"
export CUDA_VISIBLE_DEVICES=0  # Use only first GPU
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512  # Limit CUDA memory allocation

echo "🔧 Environment setup:"
echo "   PYTHONPATH: $PYTHONPATH"
echo "   Working directory: $(pwd)"
echo "   Python executable: $(which python)"

# Start Celery worker with GPU-optimized settings
echo "🚀 Starting Celery worker..."
celery -A celery_app worker \
    --loglevel=info \
    --concurrency=1 \
    --queues=predictions \
    --hostname=predictions@%h \
    --prefetch-multiplier=1

echo "🛑 Celery worker stopped"

# Show final GPU memory status
if command -v nvidia-smi > /dev/null 2>&1; then
    echo "📊 GPU memory status after worker stopped:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "   GPU Memory: " $1 " MB / " $2 " MB (" int($1/$2*100) "% used)"}'
fi 