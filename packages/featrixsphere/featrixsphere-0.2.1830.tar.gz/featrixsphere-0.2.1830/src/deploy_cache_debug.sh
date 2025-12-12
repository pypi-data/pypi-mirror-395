#!/bin/bash
# Deploy StringCache debugging updates to remote server
set -e

echo "🚀 Deploying StringCache debugging updates..."

# Files to copy
FILES=(
    "src/featrix_queue.py"
    "src/lib/featrix/neural/string_cache.py"
    "src/lib/featrix/neural/string_codec.py"
    "src/lib/featrix/neural/input_data_set.py"
    "src/lib/structureddata.py"
    "src/lib/weightwatcher_tracking.py"
)

# Check if files exist locally
echo "📋 Checking local files..."
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ File not found: $file"
        exit 1
    fi
    echo "✅ $file"
done

echo ""
echo "🔄 Copying files to remote server..."
echo "   Use this script to copy the updated debugging files:"
echo ""

for file in "${FILES[@]}"; do
    echo "scp $file username@remote-server:/sphere/$file"
done

echo ""
echo "📝 After copying, restart the queue workers to apply changes:"
echo "   sudo supervisorctl restart sphere-workers:*"
echo ""
echo "🔍 Then monitor the logs for the new debug output:"
echo "   tail -f /var/log/sphere/*.log | grep 'CACHE DEBUG\\|STRINGCODEC\\|STRINGCACHE\\|STRUCTUREDDATA'" 