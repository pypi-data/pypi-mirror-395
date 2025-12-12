#!/bin/bash
#
# Restart Celery worker and clear GPU memory
# Use this if the worker is holding onto GPU memory
#

echo "🔄 Restarting Celery worker and clearing GPU memory..."

# Kill any existing Celery workers
echo "🛑 Stopping existing Celery workers..."
pkill -f "celery.*worker" || echo "No Celery workers were running"

# Wait a moment for processes to exit
sleep 2

# Clear GPU memory if NVIDIA GPU is available
if command -v nvidia-smi > /dev/null 2>&1; then
    echo "📊 GPU memory before cleanup:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "   GPU Memory: " $1 " MB / " $2 " MB (" int($1/$2*100) "% used)"}'
    
    # Force GPU memory cleanup by killing any Python processes that might be holding GPU memory
    echo "🧹 Cleaning up GPU memory..."
    
    # Find and kill any Python processes using GPU memory (be careful!)
    # This is aggressive - only use if you know no other important processes are running
    # nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits | xargs -r kill -9
    
    # Instead, just try to clear the CUDA cache programmatically
    python3 -c "
try:
    import torch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        print('✅ PyTorch CUDA cache cleared')
    else:
        print('ℹ️  CUDA not available')
except ImportError:
    print('ℹ️  PyTorch not available')

import gc
gc.collect()
print('✅ Python garbage collection completed')
"
    
    echo "📊 GPU memory after cleanup:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "   GPU Memory: " $1 " MB / " $2 " MB (" int($1/$2*100) "% used)"}'
fi

# Restart the Celery worker
echo "🚀 Starting fresh Celery worker..."
exec ./start_celery_worker.sh 