#!/usr/bin/bash
#
# Churro Copy & Deploy Script - Fully Automated
#
# This script handles complete deployment to churro server with zero manual intervention
#
# Usage: ./node-install.sh [--restart-only] [--force] [--quiet]
#
# Options:
#   --restart-only    Only restart services, don't redeploy files
#   --force          Force deployment even if git-pull.log hasn't changed
#   --quiet          Print nothing if no changes are detected
#

set -e  # Exit on any error (but we'll handle errors explicitly in critical sections)

# Configuration
TARGET_DIR="/sphere/app"
VENV_DIR="/sphere/.venv"
DATA_DIR="/sphere/data"
LOG_DIR="/var/log/featrix"
SUPERVISOR_CONFIG="/etc/supervisor/conf.d/featrix-sphere.conf"

# Source directory (where the package files are) - set at script start
SOURCE_DIR=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Parse arguments
RESTART_ONLY=false
FORCE_DEPLOY=false
QUIET_MODE=false

for arg in "$@"; do
    case $arg in
        --restart-only)
            RESTART_ONLY=true
            ;;
        --force)
            FORCE_DEPLOY=true
            ;;
        --quiet)
            QUIET_MODE=true
            ;;
        *)
            # Unknown argument
            ;;
    esac
done

# Function to check if git commit hash or version has changed
check_git_changes() {
    local HASH_TRACKER="/tmp/churro-copy-last-commit"
    local VERSION_TRACKER="/tmp/churro-copy-last-version"
    local HASH_TEMP="/tmp/churro-copy-current-commit.tmp"
    local VERSION_TEMP="/tmp/churro-copy-current-version.tmp"
    
    # Get current git commit hash
    local current_hash=""
    if [ -d ".git" ]; then
        current_hash=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    else
        current_hash="no-git-repo"
    fi
    
    # Get current version from VERSION file
    # PRIORITY: If deploying from package (no git), check package VERSION first
    # Otherwise check deployed version first
    local current_version="unknown"
    local version_file=""
    if [ "$current_hash" = "no-git-repo" ]; then
        # Package deployment: prioritize package's VERSION file
        for vf in "./VERSION" "VERSION" "/sphere/VERSION" "/sphere/app/VERSION"; do
            if [ -f "$vf" ]; then
                version_file="$vf"
                current_version=$(cat "$vf" 2>/dev/null | head -1 | tr -d '\n\r ' || echo "unknown")
                break
            fi
        done
    else
        # Git deployment: prioritize deployed version, then package
    for vf in "/sphere/VERSION" "/sphere/app/VERSION" "./VERSION" "VERSION"; do
        if [ -f "$vf" ]; then
            version_file="$vf"
            current_version=$(cat "$vf" 2>/dev/null | head -1 | tr -d '\n\r ' || echo "unknown")
            break
        fi
    done
    fi
    
    # Get previous commit hash (if tracking file exists)
    local previous_hash=""
    if [ -f "$HASH_TRACKER" ]; then
        previous_hash=$(cat "$HASH_TRACKER" 2>/dev/null || echo "")
    fi
    
    # Get previous version (if tracking file exists)
    local previous_version=""
    if [ -f "$VERSION_TRACKER" ]; then
        previous_version=$(cat "$VERSION_TRACKER" 2>/dev/null || echo "")
    fi
    
    print_status "Git commit check: current=$current_hash, previous=$previous_hash"
    print_status "Version check: current=$current_version, previous=$previous_version"
    
    # Skip git check if no git repo (tarball deployment)
    if [ "$current_hash" = "no-git-repo" ]; then
        print_status "No git repository detected (tarball deployment) - proceeding with deployment"
        # Still save version for tracking
        echo "$current_version" > "$VERSION_TEMP"
        return 0
    fi
    
    # Check if either hash OR version has changed
    local hash_changed=false
    local version_changed=false
    
    if [ "$current_hash" != "$previous_hash" ] && [ -n "$current_hash" ] && [ "$current_hash" != "unknown" ] && [ -n "$previous_hash" ]; then
        hash_changed=true
    fi
    
    if [ "$current_version" != "$previous_version" ] && [ "$current_version" != "unknown" ] && [ -n "$previous_version" ]; then
        version_changed=true
    fi
    
    # If both hash and version are the same, no new changes - exit early (unless forced)
    if [ "$hash_changed" = false ] && [ "$version_changed" = false ] && [ -n "$current_hash" ] && [ "$current_hash" != "unknown" ] && [ "$FORCE_DEPLOY" = false ]; then
        if [ "$QUIET_MODE" = false ]; then
            add_prefix "${YELLOW}⏭️  No new changes detected (commit: ${current_hash:0:8}, version: $current_version)${NC}"
            add_prefix "${YELLOW}   Skipping deployment. Run with --force to override.${NC}"
        fi
        exit 0
    fi
    
    # Save current version to temp file
    echo "$current_version" > "$VERSION_TEMP"
    
    # If forced, show override message
    if [ "$current_hash" = "$previous_hash" ] && [ "$FORCE_DEPLOY" = true ]; then
        print_warning "Force flag detected - proceeding despite no commit change"
        add_prefix "${GREEN}🚀 FORCED DEPLOYMENT STARTED${NC}"
    fi
    
    # Save current hash to temp file (will be moved to permanent location after success)
    echo "$current_hash" > "$HASH_TEMP"
    
    # Show what changed
    if [ "$hash_changed" = true ]; then
        print_status "New git commit detected: ${current_hash:0:8} (was: ${previous_hash:0:8})"
        
        # Show what changed if possible
        if [ -n "$previous_hash" ] && [ "$previous_hash" != "" ] && [ -d ".git" ]; then
            add_prefix "${BLUE}📝 Recent commits:${NC}"
            git log --oneline -3 2>/dev/null | while read line; do add_prefix "${BLUE}   $line${NC}"; done || true
        fi
    fi
    
    if [ "$version_changed" = true ]; then
        print_status "New version detected: $current_version (was: $previous_version)"
        add_prefix "${GREEN}📦 Version upgrade: $previous_version → $current_version${NC}"
    fi
    
    # Log deployment start timestamp
    if [ "$hash_changed" = true ] || [ "$version_changed" = true ] || [ "$FORCE_DEPLOY" = true ]; then
        add_prefix "${GREEN}🚀 DEPLOYMENT STARTED${NC}"
    fi
    
    return 0
}

# Function to update commit hash and version tracker after successful deployment
update_commit_tracker() {
    local HASH_TEMP="/tmp/churro-copy-current-commit.tmp"
    local HASH_TRACKER="/tmp/churro-copy-last-commit"
    local VERSION_TEMP="/tmp/churro-copy-current-version.tmp"
    local VERSION_TRACKER="/tmp/churro-copy-last-version"
    
    if [ -f "$HASH_TEMP" ]; then
        mv "$HASH_TEMP" "$HASH_TRACKER"
        local saved_hash=$(cat "$HASH_TRACKER" 2>/dev/null || echo "unknown")
        print_status "Updated git commit tracker: ${saved_hash:0:8}"
    fi
    
    # Read version from deployed location (most accurate after deployment)
    local deployed_version="unknown"
    if [ -f "/sphere/VERSION" ]; then
        deployed_version=$(cat "/sphere/VERSION" 2>/dev/null | head -1 | tr -d '\n\r ' || echo "unknown")
    elif [ -f "$VERSION_TEMP" ]; then
        deployed_version=$(cat "$VERSION_TEMP" 2>/dev/null | head -1 | tr -d '\n\r ' || echo "unknown")
    fi
    
    # Update tracker with deployed version
    if [ "$deployed_version" != "unknown" ]; then
        echo "$deployed_version" > "$VERSION_TRACKER"
        print_status "Updated version tracker: $deployed_version"
    elif [ -f "$VERSION_TEMP" ]; then
        mv "$VERSION_TEMP" "$VERSION_TRACKER"
        local saved_version=$(cat "$VERSION_TRACKER" 2>/dev/null || echo "unknown")
        print_status "Updated version tracker: $saved_version"
    fi
}

# Function to add hostname and date prefix to any output
add_prefix() {
    local hostname=$(hostname)
    local date_str=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$hostname] [$date_str] $1"
}

print_status() {
    if [ "$QUIET_MODE" = false ]; then
        add_prefix "${GREEN}[INFO]${NC} $1"
    fi
}

print_error() {
    add_prefix "${RED}[ERROR]${NC} $1"
}

print_warning() {
    if [ "$QUIET_MODE" = false ]; then
        add_prefix "${YELLOW}[WARN]${NC} $1"
    fi
}

print_section() {
    if [ "$QUIET_MODE" = false ]; then
        add_prefix "${PURPLE}[SECTION]${NC} $1"
    fi
}

# Helper function to safely copy file (skip if source and dest are the same)
safe_copy() {
    local src="$1"
    local dest="$2"
    
    # Check if source and destination are the same file
    if [ -e "$src" ] && [ -e "$dest" ]; then
        if [ "$src" -ef "$dest" ]; then
            # Same file, skip copy
            return 0
        fi
    fi
    
    # Not the same file, proceed with copy
    cp "$src" "$dest"
}

if [ "$QUIET_MODE" = false ]; then
    add_prefix "${BLUE}================================================================${NC}"
    add_prefix "${BLUE}🚀 FeatrixSphere Firmware Automated Deployment Script${NC}"
    add_prefix "${BLUE}================================================================${NC}"
    add_prefix ""
fi

# Check if running on Ubuntu OS FIRST
if command -v lsb_release >/dev/null 2>&1; then
    OS_ID=$(lsb_release -si 2>/dev/null || echo "")
    if [[ "${OS_ID}" != "Ubuntu" ]]; then
        print_error "This script must be run on Ubuntu!"
        print_error "Detected OS: ${OS_ID}"
        print_error "Expected OS: Ubuntu"
    print_error "Are you trying to run this on your local development machine?"
    add_prefix ""
    print_warning "To deploy to churro:"
    print_warning "1. SSH to churro: ssh mitch@churro"
    print_warning "2. Run on churro: sudo ./churro-copy.sh"
    exit 1
    fi
else
    # Fallback to uname if lsb_release not available
    OS_INFO=$(uname -a)
    if [[ ! "${OS_INFO}" =~ [Uu]buntu ]]; then
        print_error "This script must be run on Ubuntu!"
        print_error "OS info: ${OS_INFO}"
        print_error "Expected OS: Ubuntu"
        print_error "Are you trying to run this on your local development machine?"
        add_prefix ""
        print_warning "To deploy to churro:"
        print_warning "1. SSH to churro: ssh mitch@churro"
        print_warning "2. Run on churro: sudo ./churro-copy.sh"
        exit 1
    fi
fi

# Check if running as root (only after confirming we're on churro)
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root (use sudo)"
    print_error "You're on the right server, but need root privileges"
    print_warning "Run: sudo ./churro-copy.sh"
    exit 1
fi

print_status "✅ Running on correct server: ${CURRENT_HOSTNAME}"

# Function to install packages if needed
install_packages() {
    print_section "Installing required packages..."
    
        # Check if packages are already installed
    if command -v python3 >/dev/null && command -v pip3 >/dev/null && command -v supervisorctl >/dev/null && command -v redis-server >/dev/null && command -v dot >/dev/null; then
        print_status "Core packages already installed"
    else
        print_status "Installing missing packages..."
        apt-get update -q
        apt-get install -y python3 python3-pip python3-venv supervisor curl build-essential python3-dev net-tools redis-server graphviz
    fi
    
    # Start and enable Redis
    print_status "Setting up Redis..."
    systemctl enable redis-server
    systemctl start redis-server
    
    # Test Redis connection
    if redis-cli ping | grep -q PONG; then
        print_status "✅ Redis is running"
    else
        print_error "❌ Redis failed to start"
        exit 1
    fi
    
    # Install textual for training dashboard
    print_status "Installing textual for training dashboard..."
    pip3 install textual --break-system-packages >/dev/null 2>&1 || print_warning "Failed to install textual"
}

# Function to create directories
setup_directories() {
    print_section "Setting up directories..."
    
    # Create all necessary directories
    print_status "Creating main directories..."
    mkdir -p "$TARGET_DIR"
    mkdir -p "$VENV_DIR"
    mkdir -p "$DATA_DIR" 
    mkdir -p "$LOG_DIR"
    
    # Create queue directories that workers need - CRITICAL!
    print_status "Creating queue directories..."
    mkdir -p "$TARGET_DIR/featrix_queue"
    mkdir -p "$TARGET_DIR/featrix_queue/create_structured_data"
    mkdir -p "$TARGET_DIR/featrix_queue/train_es"
    mkdir -p "$TARGET_DIR/featrix_queue/train_knn"
    mkdir -p "$TARGET_DIR/featrix_queue/run_clustering"
    mkdir -p "$TARGET_DIR/featrix_queue/train_single_predictor"
    
    # Create other required directories
    print_status "Creating application directories..."
    mkdir -p "$TARGET_DIR/featrix_sessions"
    mkdir -p "$TARGET_DIR/featrix_sessions_private"
    mkdir -p "$TARGET_DIR/featrix_output"
    mkdir -p "$TARGET_DIR/featrix_data"
    
    # Create symlink for /featrix-output -> /sphere/app/featrix_output
    print_status "Creating /featrix-output symlink to $TARGET_DIR/featrix_output..."
    if [ -L "/featrix-output" ]; then
        # Check if it points to the correct location
        existing_target=$(readlink -f "/featrix-output" 2>/dev/null || echo "")
        if [ "$existing_target" != "$TARGET_DIR/featrix_output" ]; then
            print_status "Removing existing symlink at /featrix-output (points to: $existing_target, should be: $TARGET_DIR/featrix_output)"
            rm -f "/featrix-output"
            ln -sf "$TARGET_DIR/featrix_output" "/featrix-output"
            print_status "✅ Created symlink: /featrix-output -> $TARGET_DIR/featrix_output"
        else
            print_status "✅ Symlink /featrix-output already exists and points to correct location"
        fi
    elif [ -e "/featrix-output" ]; then
        # If it exists but is not a symlink, remove it and create symlink
        print_warning "⚠️  /featrix-output exists but is not a symlink. Removing and creating symlink."
        rm -rf "/featrix-output"
        ln -sf "$TARGET_DIR/featrix_output" "/featrix-output"
        print_status "✅ Created symlink: /featrix-output -> $TARGET_DIR/featrix_output"
    else
        # Create symlink if it doesn't exist
        ln -sf "$TARGET_DIR/featrix_output" "/featrix-output"
        if [ -L "/featrix-output" ]; then
            print_status "✅ Created symlink: /featrix-output -> $TARGET_DIR/featrix_output"
        else
            print_error "❌ Failed to create symlink /featrix-output"
        fi
    fi
    
    # Create cache directories for system components
    print_status "Creating cache directories..."
    # Create traceback cache (files are installed directly to /sphere/app, not /sphere/app/src)
    mkdir -p "$TARGET_DIR/.traceback_cache"
    
    # Create flags directory for deployment triggers
    print_status "Creating flags directory..."
    mkdir -p /sphere/flags
    
    # Set permissions on everything
    print_status "Setting permissions..."
    chown -R root:root /sphere
    chmod -R 755 /sphere
    chmod -R 755 "$LOG_DIR"
    
    # Verify critical directories exist
    print_status "Verifying queue directories..."
    for queue in create_structured_data train_es train_knn run_clustering train_single_predictor; do
        if [ -d "$TARGET_DIR/featrix_queue/$queue" ]; then
            print_status "✅ Queue directory: $queue"
        else
            print_error "❌ Failed to create queue directory: $queue"
            exit 1
        fi
    done
    
    print_status "All directories created and verified"
}

# Function to setup virtual environment
setup_virtualenv() {
    print_section "Setting up Python virtual environment..."
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_status "System Python version: $python_version"
    
    # Use system Python - bytecode compatibility is handled by rsync excludes
    PYTHON_CMD="python3"
    print_status "Using: $PYTHON_CMD ($($PYTHON_CMD --version))"
    
    # Test if venv exists and is healthy
    if [ -f "$VENV_DIR/bin/activate" ]; then
        venv_py_version=$("$VENV_DIR/bin/python" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
        print_status "Existing venv Python version: $venv_py_version"
        
        # Check for recent bad marshal data errors in logs
        if [ -f "/var/log/featrix/api_server.log" ] && tail -100 /var/log/featrix/api_server.log 2>/dev/null | grep -q "bad marshal data"; then
            print_warning "Detected 'bad marshal data' errors in recent logs - forcing venv recreation"
            rm -rf "$VENV_DIR"
        # Test if venv works by importing torch
        elif source "$VENV_DIR/bin/activate" 2>/dev/null && python -c "import torch" >/dev/null 2>&1; then
            print_status "✅ Existing venv is healthy, keeping it"
            deactivate
        else
            print_warning "Venv corrupted, removing..."
            deactivate 2>/dev/null || true
            rm -rf "$VENV_DIR"
        fi
    fi
    
    # Create fresh virtual environment if needed
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        print_status "Creating new virtual environment with $PYTHON_CMD..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        
        if [ ! -f "$VENV_DIR/bin/activate" ]; then
            print_error "Virtual environment creation failed"
            exit 1
        fi
        print_status "✅ Virtual environment created"
    fi
    
    # Activate and install packages
    source "$VENV_DIR/bin/activate"
    
    # Copy the ACTUAL requirements.txt from the repo instead of generating a fake one
    print_status "Copying requirements.txt from repository..."
    
    # Determine REPO_ROOT based on where the script is located
    # Case 1: Git repo - script at ~/sphere/src/churro-copy.sh, requirements at ~/sphere/requirements.txt
    # Case 2: Tarball - script at /tmp/.../sphere-app/churro-copy.sh, requirements at same dir
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Try current directory first (tarball case)
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        REPO_ROOT="$SCRIPT_DIR"
    # Try parent directory (git repo case)
    elif [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
        REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    else
        print_error "Cannot find requirements.txt in $SCRIPT_DIR or $SCRIPT_DIR/.."
        print_error "Contents of $SCRIPT_DIR:"
        ls -la "$SCRIPT_DIR" | head -20
        exit 1
    fi
    
    print_status "Found requirements.txt at: $REPO_ROOT/requirements.txt"
    
    if [ -f "$REPO_ROOT/requirements.txt" ]; then
        # Check if requirements.txt has changed
        REQUIREMENTS_HASH=$(md5sum "$REPO_ROOT/requirements.txt" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        LAST_REQUIREMENTS_HASH=""
        if [ -f "$TARGET_DIR/.requirements_hash" ]; then
            LAST_REQUIREMENTS_HASH=$(cat "$TARGET_DIR/.requirements_hash" 2>/dev/null || echo "")
        fi
        
        cp "$REPO_ROOT/requirements.txt" "$TARGET_DIR/requirements.txt"
        echo "$REQUIREMENTS_HASH" > "$TARGET_DIR/.requirements_hash"
        print_status "✅ Using real requirements.txt from repo ($REPO_ROOT/requirements.txt)"
        
        # Only run pip operations if requirements.txt changed or venv was just created
        if [ "$REQUIREMENTS_HASH" != "$LAST_REQUIREMENTS_HASH" ] || [ ! -f "$VENV_DIR/.pip_installed" ]; then
            print_status "📦 Requirements changed or first install - checking packages..."
            
            # Upgrade pip and build tools first (only if needed)
            print_status "Upgrading pip and build tools..."
            if ! python -m pip install --upgrade pip setuptools wheel 2>&1 | tee /tmp/pip-upgrade.log | grep -v "Requirement already satisfied" | grep -E "(ERROR|FAILED|ValueError)"; then
                print_status "✅ Pip upgrade successful"
            else
                print_error "Pip upgrade failed. See /tmp/pip-upgrade.log for details"
                cat /tmp/pip-upgrade.log
                exit 1
            fi
            
            # Install packages with multiple retry strategies
            # Only install what's actually missing
            print_status "Checking installed packages..."
            
            # Get list of currently installed packages (just names, sorted)
            pip list --format=freeze | cut -d'=' -f1 | sort > /tmp/installed_packages.txt
            
            # Get list of required packages from requirements.txt (just names, sorted)
            grep -v '^#' "$TARGET_DIR/requirements.txt" | grep -v '^$' | cut -d'>' -f1 | cut -d'<' -f1 | cut -d'=' -f1 | tr -d ' ' | sort > /tmp/required_packages.txt
            
            # Find packages that are required but not installed
            comm -13 /tmp/installed_packages.txt /tmp/required_packages.txt > /tmp/missing_packages.txt
            
            MISSING_COUNT=$(wc -l < /tmp/missing_packages.txt | tr -d ' ')
            
            if [ "$MISSING_COUNT" -eq 0 ]; then
                print_status "✅ All required packages already installed, skipping pip install"
            else
                print_status "📦 Found $MISSING_COUNT missing packages, installing..."
                
                # Install only missing packages with full version constraints from requirements.txt
                while IFS= read -r package; do
                    if [ -n "$package" ]; then
                        # Find the full requirement line for this package
                        req_line=$(grep -i "^${package}[>=<]" "$TARGET_DIR/requirements.txt" || echo "$package")
                        print_status "Installing: $req_line"
                        if ! pip install "$req_line" 2>&1 | grep -v "Requirement already satisfied"; then
                            print_warning "Failed to install $req_line"
                        fi
                    fi
                done < /tmp/missing_packages.txt
                
                print_status "✅ Package installation complete"
            fi
            
            # Cleanup temp files
            rm -f /tmp/installed_packages.txt /tmp/required_packages.txt /tmp/missing_packages.txt
            
            # Verify key packages only if we installed something
            # Explicitly ensure critical packages are installed (for auto_upgrade_monitor and other services)
            print_status "Ensuring critical packages are installed in venv..."
            CRITICAL_PACKAGES=(
                "pydantic-settings>=2.8.0"
                "redis>=5.0.0"
                "psutil>=5.9.0"
                "weightwatcher>=0.5.2"
            )
            for pkg in "${CRITICAL_PACKAGES[@]}"; do
                print_status "Checking/installing: $pkg"
                if ! pip install "$pkg" 2>&1 | grep -v "Requirement already satisfied"; then
                    print_warning "Note: $pkg may already be installed"
                fi
            done
            
            if [ "$MISSING_COUNT" -gt 0 ]; then
                print_status "Verifying key packages..."
                python -c "
import sys
success = True
packages = ['fastapi', 'uvicorn', 'pandas', 'pydantic_settings', 'jsontables', 'redis', 'celery', 'psutil', 'weightwatcher']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg} OK')
    except Exception as e:
        print(f'❌ {pkg} failed: {e}')
        success = False

if not success:
    print('❌ Some core packages failed to install')
    sys.exit(1)
else:
    print('✅ Core packages verified')
" || { print_error "Package verification failed"; exit 1; }
            fi
            
            # Mark that pip install completed successfully
            touch "$VENV_DIR/.pip_installed"
        else
            print_status "✅ Requirements.txt unchanged, skipping pip operations"
        fi
        
        # Install featrix-string-server-client from private bits server (always run with --upgrade)
        # Use --extra-index-url so dependencies come from PyPI, only our package from bits
        print_status "Installing featrix-string-server-client from private bits server..."
        pip install --upgrade --extra-index-url https://bits.featrix.com/pypi/simple --trusted-host bits.featrix.com featrix-string-server-client 2>&1 | grep -v "Requirement already satisfied" || true
        if python -c "import featrix_string_server_client" 2>/dev/null; then
            print_status "✅ featrix-string-server-client installed/upgraded"
        else
            print_warning "Note: featrix-string-server-client installation may have failed or bits server unavailable"
        fi
    else
        print_error "requirements.txt not found at: $REPO_ROOT/requirements.txt"
        ls -la "$REPO_ROOT/" | head -20
        exit 1
    fi
    
    deactivate
    print_status "Virtual environment setup completed"
}

# Function to copy application files
copy_application_files() {
    print_section "Copying application files..."
    
    # FIRST: Clean up conflicting directories BEFORE copying anything
    # This prevents utils/ directory from shadowing utils.py
    print_status "Cleaning up conflicting directories..."
    if [ -d "$TARGET_DIR/utils" ]; then
        print_status "🗑️  Removing utils/ directory (shadows utils.py)"
        rm -rf "$TARGET_DIR/utils"
    fi
    
    # Now copy Python files and shell scripts from SOURCE_DIR (not current directory, which might have changed)
    print_status "Copying Python files and shell scripts from source directory..."
    if [ -n "$SOURCE_DIR" ] && [ "$SOURCE_DIR" != "$TARGET_DIR" ]; then
        cp "$SOURCE_DIR"/*.py "$TARGET_DIR/" 2>/dev/null || true
        cp "$SOURCE_DIR"/*.sh "$TARGET_DIR/" 2>/dev/null || true
        # Also try src/ subdirectory
        if [ -d "$SOURCE_DIR/src" ]; then
            cp "$SOURCE_DIR/src"/*.py "$TARGET_DIR/" 2>/dev/null || true
            cp "$SOURCE_DIR/src"/*.sh "$TARGET_DIR/" 2>/dev/null || true
        fi
    else
        cp *.py "$TARGET_DIR/" 2>/dev/null || true
        cp *.sh "$TARGET_DIR/" 2>/dev/null || true
    fi
    
    # Explicitly copy and verify critical supervisor files (for both git repo and tarball cases)
    print_status "Ensuring critical supervisor files are copied..."
    print_status "Source directory: $SOURCE_DIR"
    print_status "Current working directory: $(pwd)"
    print_status "Target directory: $TARGET_DIR"
    
    # Copy Celery worker startup scripts
    print_status "Copying Celery worker startup scripts..."
    SCRIPT_DIR_TEMP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    for script in "start_celery_cpu_worker.sh" "start_celery_gpu_worker.sh"; do
        script_found=false
        # Try multiple source locations (same logic as critical files)
        # Try SOURCE_DIR/src/ first (most common - git repo structure in tarball)
        if [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/src/$script" ]; then
            print_status "Found $script in $SOURCE_DIR/src/ (git repo structure)"
            cp "$SOURCE_DIR/src/$script" "$TARGET_DIR/"
            chmod +x "$TARGET_DIR/$script"
            script_found=true
        # Try SOURCE_DIR (tarball case - files at root of package)
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/$script" ]; then
            print_status "Found $script in $SOURCE_DIR (tarball root structure)"
            cp "$SOURCE_DIR/$script" "$TARGET_DIR/"
            chmod +x "$TARGET_DIR/$script"
            script_found=true
        # Try SCRIPT_DIR/src/ (when running from src/ directory)
        elif [ -f "$SCRIPT_DIR_TEMP/src/$script" ]; then
            print_status "Found $script in $SCRIPT_DIR_TEMP/src/"
            cp "$SCRIPT_DIR_TEMP/src/$script" "$TARGET_DIR/"
            chmod +x "$TARGET_DIR/$script"
            script_found=true
        # Try current directory src/
        elif [ -f "src/$script" ]; then
            print_status "Found $script in current directory src/"
            cp "src/$script" "$TARGET_DIR/"
            chmod +x "$TARGET_DIR/$script"
            script_found=true
        # Try current directory
        elif [ -f "$script" ]; then
            print_status "Found $script in current directory"
            cp "$script" "$TARGET_DIR/"
            chmod +x "$TARGET_DIR/$script"
            script_found=true
        fi
        
        # Verify it was copied
        if [ "$script_found" = true ]; then
            if [ ! -f "$TARGET_DIR/$script" ]; then
                print_error "FAILED to copy $script to $TARGET_DIR/ - Celery workers will not start!"
                exit 1
            else
                print_status "✅ Successfully copied and verified $script"
            fi
        else
            print_error "CRITICAL: $script was not found and not copied - Celery workers will not start!"
            print_error "   Searched locations:"
            [ -n "$SOURCE_DIR" ] && print_error "     $SOURCE_DIR/src/$script"
            [ -n "$SOURCE_DIR" ] && print_error "     $SOURCE_DIR/$script"
            print_error "     $SCRIPT_DIR_TEMP/src/$script"
            print_error "     $(pwd)/src/$script"
            print_error "     $(pwd)/$script"
            print_error "   Debug: Listing $SOURCE_DIR/src/ contents:"
            [ -n "$SOURCE_DIR" ] && [ -d "$SOURCE_DIR/src" ] && ls -la "$SOURCE_DIR/src/" | grep -E "(start_celery|\.sh)" || print_error "     Directory $SOURCE_DIR/src/ does not exist"
            exit 1
        fi
    done
    
    for critical_file in "featrix_watchdog.py" "gc_cleanup.py" "system_monitor.py" "auto_upgrade_monitor.py" "featrix-update.py"; do
        copied=false
        # Try SOURCE_DIR first (tarball case - files at root of package)
        if [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/$critical_file" ]; then
            print_status "Found $critical_file in source directory (tarball structure)"
            print_status "Copying $critical_file from $SOURCE_DIR/ to $TARGET_DIR/..."
            cp "$SOURCE_DIR/$critical_file" "$TARGET_DIR/$critical_file"
            chmod +x "$TARGET_DIR/$critical_file"
            copied=true
        # Try SOURCE_DIR/src/ (git repo case)
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/src/$critical_file" ]; then
            print_status "Found $critical_file in source/src/ (git repo structure)"
            print_status "Copying $critical_file from $SOURCE_DIR/src/ to $TARGET_DIR/..."
            cp "$SOURCE_DIR/src/$critical_file" "$TARGET_DIR/$critical_file"
            chmod +x "$TARGET_DIR/$critical_file"
            copied=true
        # Try root of repo (for files like system_monitor.py that are at repo root)
        elif [ -n "$SOURCE_DIR" ] && [ -f "$(dirname "$SOURCE_DIR")/$critical_file" ]; then
            print_status "Found $critical_file at repo root"
            print_status "Copying $critical_file from $(dirname "$SOURCE_DIR")/ to $TARGET_DIR/..."
            cp "$(dirname "$SOURCE_DIR")/$critical_file" "$TARGET_DIR/$critical_file"
            chmod +x "$TARGET_DIR/$critical_file"
            copied=true
        # Fallback: try current directory (for backwards compatibility)
        elif [ -f "$critical_file" ]; then
            print_status "Found $critical_file in current directory (fallback)"
            print_status "Copying $critical_file to $TARGET_DIR/..."
            cp "$critical_file" "$TARGET_DIR/$critical_file"
            chmod +x "$TARGET_DIR/$critical_file"
            copied=true
        elif [ -f "src/$critical_file" ]; then
            print_status "Found $critical_file in src/ (fallback)"
            print_status "Copying $critical_file to $TARGET_DIR/..."
            cp "src/$critical_file" "$TARGET_DIR/$critical_file"
            chmod +x "$TARGET_DIR/$critical_file"
            copied=true
        else
            print_warning "Critical file $critical_file not found - checking locations..."
            [ -n "$SOURCE_DIR" ] && ls -la "$SOURCE_DIR/$critical_file" 2>/dev/null || print_warning "  Not found at: $SOURCE_DIR/$critical_file"
            [ -n "$SOURCE_DIR" ] && ls -la "$SOURCE_DIR/src/$critical_file" 2>/dev/null || print_warning "  Not found at: $SOURCE_DIR/src/$critical_file"
            [ -n "$SOURCE_DIR" ] && ls -la "$(dirname "$SOURCE_DIR")/$critical_file" 2>/dev/null || print_warning "  Not found at: $(dirname "$SOURCE_DIR")/$critical_file"
            ls -la "$critical_file" 2>/dev/null || print_warning "  Not found at: $critical_file"
            ls -la "src/$critical_file" 2>/dev/null || print_warning "  Not found at: src/$critical_file"
        fi
        
        # Verify it was copied
        if [ "$copied" = true ]; then
            if [ ! -f "$TARGET_DIR/$critical_file" ]; then
                print_error "FAILED to copy $critical_file to $TARGET_DIR/ - supervisor will fail!"
                exit 1
            else
                print_status "✅ Successfully copied and verified $critical_file"
            fi
        else
            print_error "CRITICAL: $critical_file was not found and not copied - supervisor will fail!"
            exit 1
        fi
    done
    
    # Handle two cases: git repo (src/) or tarball (flat structure)
    if [ -d "src" ]; then
        # Git repo case: Copy contents of src/ directory into /sphere/app/
        print_status "Copying contents of src/ into $TARGET_DIR/ (git repo structure)..."
        # Copy all Python files from src/ directly to /sphere/app/
        cp src/*.py "$TARGET_DIR/" 2>/dev/null || true
        # Critical files already copied above (handles both git repo and tarball cases)
        
        # Copy lib subdirectory to /sphere/app/lib/ (excluding __pycache__)
        if [ -d "src/lib" ]; then
            print_status "Copying src/lib/ to $TARGET_DIR/lib/..."
            # Use --delete and --force to ensure files are updated
            rsync -av --delete --exclude='__pycache__' --exclude='*.pyc' src/lib/ "$TARGET_DIR/lib/"
            # Explicitly copy critical lib files to ensure they're updated
            CRITICAL_LIB_FILES=("utils.py" "es_training.py")
            for lib_file in "${CRITICAL_LIB_FILES[@]}"; do
                if [ -f "src/lib/$lib_file" ]; then
                    print_status "Explicitly copying $lib_file to ensure it's updated..."
                    rsync -av "src/lib/$lib_file" "$TARGET_DIR/lib/$lib_file"
                    chmod 644 "$TARGET_DIR/lib/$lib_file" || true
                fi
            done
            
            # Verify MD5 checksums for all files if MD5SUMS file exists
            print_status "🔍 Looking for MD5SUMS file..."
            print_status "   Current directory: $(pwd)"
            print_status "   Checking: MD5SUMS, lib/MD5SUMS, src/lib/MD5SUMS"
            MD5SUMS_FILE=""
            if [ -f "MD5SUMS" ]; then
                MD5SUMS_FILE="MD5SUMS"
                print_status "   ✅ Found: MD5SUMS (root level)"
            elif [ -f "lib/MD5SUMS" ]; then
                MD5SUMS_FILE="lib/MD5SUMS"
                print_status "   ✅ Found: lib/MD5SUMS"
            elif [ -f "src/lib/MD5SUMS" ]; then
                MD5SUMS_FILE="src/lib/MD5SUMS"
                print_status "   ✅ Found: src/lib/MD5SUMS"
            else
                print_warning "   ⚠️  MD5SUMS file not found - skipping MD5 verification"
                print_warning "   This is expected for packages created before MD5SUMS was added"
            fi
            
            if [ -n "$MD5SUMS_FILE" ] && [ -f "$MD5SUMS_FILE" ]; then
                print_status "   Using MD5SUMS file: $MD5SUMS_FILE"
                    print_status "🔐 Verifying MD5 checksums for all lib files..."
                    VERIFICATION_FAILED=0
                    VERIFICATION_COUNT=0
                    VERIFICATION_PASSED=0
                    
                    # Read MD5SUMS file and verify each file
                    while IFS= read -r line || [ -n "$line" ]; do
                        # Skip empty lines
                        [ -z "$line" ] && continue
                        
                        # Parse: MD5SUM  path/to/file
                        md5_expected=$(echo "$line" | awk '{print $1}')
                        file_path=$(echo "$line" | awk '{print $2}')
                        
                        # Skip if file path is empty
                        [ -z "$file_path" ] && continue
                        
                        # Convert package path to target path
                        # MD5SUMS has paths like "./lib/utils.py" or "lib/utils.py" or "api.py"
                        # We need to convert to "$TARGET_DIR/lib/utils.py" or "$TARGET_DIR/api.py"
                        target_file="$file_path"
                        # Remove leading "./" if present
                        target_file="${target_file#./}"
                        # Remove "build/sphere-app/" prefix if present
                        target_file="${target_file#build/sphere-app/}"
                        # Remove "src/" prefix if present
                        target_file="${target_file#src/}"
                        
                        # Full target path
                        full_target="$TARGET_DIR/$target_file"
                        
                        # Skip if target file doesn't exist
                        if [ ! -f "$full_target" ]; then
                            print_warning "⚠️  File not found (skipping): $target_file"
                            continue
                        fi
                        
                        VERIFICATION_COUNT=$((VERIFICATION_COUNT + 1))
                        
                        # Calculate MD5 of target file
                        md5_actual=$(md5sum "$full_target" | cut -d' ' -f1)
                        
                        if [ "$md5_expected" = "$md5_actual" ]; then
                            VERIFICATION_PASSED=$((VERIFICATION_PASSED + 1))
                        else
                            VERIFICATION_FAILED=$((VERIFICATION_FAILED + 1))
                            print_error "❌ MD5 mismatch: $target_file"
                            print_error "   Expected: $md5_expected"
                            print_error "   Actual:   $md5_actual"
                            # Try to fix by copying from source
                            # Check multiple possible source locations
                            source_file=""
                            for possible_source in "src/$target_file" "$target_file" "lib/${target_file#lib/}"; do
                                if [ -f "$possible_source" ]; then
                                    source_file="$possible_source"
                                    break
                                fi
                            done
                            
                            if [ -n "$source_file" ] && [ -f "$source_file" ]; then
                                print_error "   Attempting to fix by copying from source: $source_file"
                                rsync -av "$source_file" "$full_target"
                                chmod 644 "$full_target" || true
                                md5_retry=$(md5sum "$full_target" | cut -d' ' -f1)
                                if [ "$md5_expected" = "$md5_retry" ]; then
                                    print_status "   ✅ Fixed - MD5 now matches"
                                    VERIFICATION_FAILED=$((VERIFICATION_FAILED - 1))
                                    VERIFICATION_PASSED=$((VERIFICATION_PASSED + 1))
                                else
                                    print_error "   ❌ Still mismatched after fix attempt"
                                    print_error "      Expected: $md5_expected"
                                    print_error "      Got:      $md5_retry"
                                fi
                            else
                                print_error "   ❌ Source file not found in any location"
                                print_error "      Tried: src/$target_file, $target_file, lib/${target_file#lib/}"
                            fi
                        fi
                    done < "$MD5SUMS_FILE"
                    
                    print_status "🔐 MD5 Verification Summary:"
                    print_status "   Total files checked: $VERIFICATION_COUNT"
                    print_status "   Passed: $VERIFICATION_PASSED"
                    if [ $VERIFICATION_FAILED -gt 0 ]; then
                        print_error "   Failed: $VERIFICATION_FAILED"
                        print_error "❌ MD5 verification failed - some files are incorrect"
                        exit 1
                    else
                        print_status "✅ All MD5 checksums verified successfully"
                        # Copy MD5SUMS file to /sphere for later reference
                        if [ -f "$MD5SUMS_FILE" ]; then
                            print_status "📋 Copying MD5SUMS to /sphere/MD5SUMS for reference..."
                            mkdir -p /sphere
                            rsync -av "$MD5SUMS_FILE" /sphere/MD5SUMS || print_warning "⚠️  Failed to copy MD5SUMS to /sphere/"
                            print_status "✅ MD5SUMS saved to /sphere/MD5SUMS"
                        fi
                    fi
            fi
            # ALWAYS verify critical files were copied and match source (even if MD5SUMS doesn't exist)
            print_status "🔍 Verifying critical lib files match source..."
            for critical_file in "utils.py" "es_training.py"; do
                if [ -f "src/lib/$critical_file" ]; then
                    if [ ! -f "$TARGET_DIR/lib/$critical_file" ]; then
                        print_error "❌ $critical_file was not copied to $TARGET_DIR/lib/"
                        print_error "   Copying now..."
                        rsync -av "src/lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                        chmod 644 "$TARGET_DIR/lib/$critical_file" || true
                    fi
                    
                    # Always verify md5sum matches source
                    SRC_MD5=$(md5sum "src/lib/$critical_file" | cut -d' ' -f1)
                    TGT_MD5=$(md5sum "$TARGET_DIR/lib/$critical_file" | cut -d' ' -f1)
                    if [ "$SRC_MD5" = "$TGT_MD5" ]; then
                        print_status "✅ $critical_file md5sum matches source ($SRC_MD5)"
                    else
                        print_error "❌ MD5 mismatch for $critical_file"
                        print_error "   Source: $SRC_MD5"
                        print_error "   Target: $TGT_MD5"
                        print_error "   Forcing copy..."
                        rsync -av "src/lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                        chmod 644 "$TARGET_DIR/lib/$critical_file" || true
                        TGT_MD5=$(md5sum "$TARGET_DIR/lib/$critical_file" | cut -d' ' -f1)
                        if [ "$SRC_MD5" = "$TGT_MD5" ]; then
                            print_status "✅ Fixed - $critical_file md5sum now matches"
                        else
                            print_error "❌ CRITICAL: Still mismatched after force copy"
                            print_error "   This indicates a serious deployment issue"
                            print_error "   Source MD5: $SRC_MD5"
                            print_error "   Target MD5: $TGT_MD5"
                            print_error "   Target file: $TARGET_DIR/lib/$critical_file"
                            ls -la "$TARGET_DIR/lib/$critical_file" || true
                            exit 1
                        fi
                    fi
                else
                    print_warning "⚠️  Source file not found: src/lib/$critical_file"
                fi
            done
        fi
        
        # Copy ONLY source code subdirectories - DO NOT copy runtime job output directories
        # Whitelist approach: only copy known source directories
        # Skip ALL job output directories (they match patterns like create_structured_data_*, train_es_*, etc.)
        for dir in src/*/; do
            dirname=$(basename "$dir")
            if [ "$dirname" != "lib" ] && [ "$dirname" != "__pycache__" ] && [ -d "$dir" ]; then
                # Skip runtime data directories and job output directories
                case "$dirname" in
                    # Known runtime data directories
                    featrix_output|featrix_sessions|featrix_sessions_private|featrix_queue|featrix_data|jobs|dev_data|build)
                        continue
                        ;;
                    # Job output directories (match patterns)
                    create_structured_data*|train_es*|train_knn*|run_clustering*|train_single_predictor*|generate_movie_frame*|cpu_data_tasks*|json_es_training*|input_data*|logs*|*_*_*)
                        # Skip directories that look like job outputs (date-hash pattern or known job types)
                        continue
                        ;;
                esac
                # Only copy if it's a known source directory (add to whitelist as needed)
                # For now, skip everything except lib (which is already copied above)
                # If you need to copy other source dirs, add them explicitly here
                print_status "Skipping src/$dirname/ (not in source code whitelist)"
            fi
        done
    elif [ -d "lib" ]; then
        # Tarball case: Files already at root level, just copy lib/ and subdirs
        # CRITICAL: Copy from SOURCE_DIR/lib/ (package) not current directory (old files)
        if [ -n "$SOURCE_DIR" ] && [ -d "$SOURCE_DIR/lib" ]; then
            print_status "Copying lib/ from $SOURCE_DIR/lib/ to $TARGET_DIR/lib/ (tarball structure)..."
            print_status "   Source: $SOURCE_DIR/lib/"
            print_status "   Target: $TARGET_DIR/lib/"
            rsync -av --delete --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' --exclude='*.pth' --exclude='*.log' --exclude='.git' "$SOURCE_DIR/lib/" "$TARGET_DIR/lib/"
            print_status "✅ lib/ directory copied (including neural/)"
        else
            print_error "❌ SOURCE_DIR/lib/ not found: $SOURCE_DIR/lib"
            print_error "   Cannot copy lib/ files - deployment will fail"
            exit 1
        fi
        
        # Verify MD5 checksums for all files if MD5SUMS file exists
        print_status "🔍 Looking for MD5SUMS file..."
        print_status "   Current directory: $(pwd)"
        print_status "   SOURCE_DIR: $SOURCE_DIR"
        print_status "   Checking: MD5SUMS, lib/MD5SUMS, SOURCE_DIR/MD5SUMS"
        MD5SUMS_FILE=""
        # Check in current directory first (if we're in the package directory)
        if [ -f "MD5SUMS" ]; then
            MD5SUMS_FILE="MD5SUMS"
            print_status "   ✅ Found: MD5SUMS (current directory)"
        # Check in SOURCE_DIR (package location)
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/MD5SUMS" ]; then
            MD5SUMS_FILE="$SOURCE_DIR/MD5SUMS"
            print_status "   ✅ Found: MD5SUMS in SOURCE_DIR ($SOURCE_DIR/MD5SUMS)"
        elif [ -f "lib/MD5SUMS" ]; then
            MD5SUMS_FILE="lib/MD5SUMS"
            print_status "   ✅ Found: lib/MD5SUMS"
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/lib/MD5SUMS" ]; then
            MD5SUMS_FILE="$SOURCE_DIR/lib/MD5SUMS"
            print_status "   ✅ Found: lib/MD5SUMS in SOURCE_DIR ($SOURCE_DIR/lib/MD5SUMS)"
        else
            print_warning "   ⚠️  MD5SUMS file not found - skipping MD5 verification"
            print_warning "   Checked: MD5SUMS, lib/MD5SUMS, $SOURCE_DIR/MD5SUMS, $SOURCE_DIR/lib/MD5SUMS"
            print_warning "   This is expected for packages created before MD5SUMS was added"
        fi
        
        if [ -n "$MD5SUMS_FILE" ] && [ -f "$MD5SUMS_FILE" ]; then
            print_status "   Using MD5SUMS file: $MD5SUMS_FILE"
            print_status "🔐 Verifying MD5 checksums for all files..."
            VERIFICATION_FAILED=0
            VERIFICATION_COUNT=0
            VERIFICATION_PASSED=0
            
            # Read MD5SUMS file and verify each file
            while IFS= read -r line || [ -n "$line" ]; do
                # Skip empty lines
                [ -z "$line" ] && continue
                
                # Parse: MD5SUM  path/to/file
                md5_expected=$(echo "$line" | awk '{print $1}')
                file_path=$(echo "$line" | awk '{print $2}')
                
                # Skip if file path is empty
                [ -z "$file_path" ] && continue
                
                # Convert package path to target path
                # MD5SUMS has paths like "./lib/utils.py" or "lib/utils.py" or "api.py"
                target_file="$file_path"
                # Remove leading "./" if present
                target_file="${target_file#./}"
                # Remove "build/sphere-app/" prefix if present
                target_file="${target_file#build/sphere-app/}"
                
                # Full target path
                full_target="$TARGET_DIR/$target_file"
                
                # Skip if target file doesn't exist (might be in a subdirectory we don't deploy)
                if [ ! -f "$full_target" ]; then
                    # Only warn for important files, skip others silently
                    if [[ "$target_file" =~ ^(lib/|api\.py|featrix_queue\.py|config\.py|version\.py) ]]; then
                        print_warning "⚠️  Important file not found (skipping): $target_file"
                    fi
                    continue
                fi
                
                VERIFICATION_COUNT=$((VERIFICATION_COUNT + 1))
                
                # Calculate MD5 of target file
                md5_actual=$(md5sum "$full_target" | cut -d' ' -f1)
                
                if [ "$md5_expected" = "$md5_actual" ]; then
                    VERIFICATION_PASSED=$((VERIFICATION_PASSED + 1))
                else
                    VERIFICATION_FAILED=$((VERIFICATION_FAILED + 1))
                    print_error "❌ MD5 mismatch: $target_file"
                    print_error "   Expected: $md5_expected"
                    print_error "   Actual:   $md5_actual"
                    # Try to fix by copying from source package
                    # Check multiple possible source locations
                    source_file=""
                    # Try SOURCE_DIR first (package location)
                    if [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/$target_file" ]; then
                        source_file="$SOURCE_DIR/$target_file"
                    # Try current directory (if we're in package dir)
                    elif [ -f "$target_file" ]; then
                        source_file="$target_file"
                    # Try without lib/ prefix
                    elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/${target_file#lib/}" ]; then
                        source_file="$SOURCE_DIR/${target_file#lib/}"
                    fi
                    
                    if [ -n "$source_file" ] && [ -f "$source_file" ]; then
                        print_error "   Attempting to fix by copying from source: $source_file"
                        print_error "   Target: $full_target"
                        rsync -av "$source_file" "$full_target"
                        chmod 644 "$full_target" || true
                        md5_retry=$(md5sum "$full_target" | cut -d' ' -f1)
                        if [ "$md5_expected" = "$md5_retry" ]; then
                            print_status "   ✅ Fixed - MD5 now matches"
                            VERIFICATION_FAILED=$((VERIFICATION_FAILED - 1))
                            VERIFICATION_PASSED=$((VERIFICATION_PASSED + 1))
                        else
                            print_error "   ❌ Still mismatched after fix attempt"
                            print_error "      Expected: $md5_expected"
                            print_error "      Got:      $md5_retry"
                            print_error "      Source file MD5: $(md5sum "$source_file" | cut -d' ' -f1)"
                        fi
                    else
                        print_error "   ❌ Source file not found in any location"
                        print_error "      Tried: $SOURCE_DIR/$target_file, $target_file, $SOURCE_DIR/${target_file#lib/}"
                    fi
                fi
            done < "$MD5SUMS_FILE"
            
            print_status "🔐 MD5 Verification Summary:"
            print_status "   Total files checked: $VERIFICATION_COUNT"
            print_status "   Passed: $VERIFICATION_PASSED"
            if [ $VERIFICATION_FAILED -gt 0 ]; then
                print_error "   Failed: $VERIFICATION_FAILED"
                print_error "❌ MD5 verification failed - some files are incorrect"
                exit 1
            else
                print_status "✅ All MD5 checksums verified successfully"
                # ALWAYS copy MD5SUMS file to /sphere for later reference (even if verification was skipped)
                if [ -f "$MD5SUMS_FILE" ]; then
                    print_status "📋 Copying MD5SUMS to /sphere/MD5SUMS for reference..."
                    mkdir -p /sphere
                    if rsync -av "$MD5SUMS_FILE" /sphere/MD5SUMS; then
                        print_status "✅ MD5SUMS saved to /sphere/MD5SUMS"
                        print_status "   You can verify files later with: md5sum -c /sphere/MD5SUMS"
                    else
                        print_error "❌ Failed to copy MD5SUMS to /sphere/"
                        print_error "   Attempted to copy: $MD5SUMS_FILE"
                    fi
                else
                    print_warning "⚠️  MD5SUMS file not available to copy: $MD5SUMS_FILE"
                fi
            fi
        fi
        
        # ALWAYS try to copy MD5SUMS to /sphere even if verification was skipped (for reference)
        # Check multiple locations for MD5SUMS file
        MD5SUMS_TO_COPY=""
        if [ -n "$MD5SUMS_FILE" ] && [ -f "$MD5SUMS_FILE" ]; then
            MD5SUMS_TO_COPY="$MD5SUMS_FILE"
        elif [ -f "MD5SUMS" ]; then
            MD5SUMS_TO_COPY="MD5SUMS"
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/MD5SUMS" ]; then
            MD5SUMS_TO_COPY="$SOURCE_DIR/MD5SUMS"
        elif [ -f "lib/MD5SUMS" ]; then
            MD5SUMS_TO_COPY="lib/MD5SUMS"
        elif [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/lib/MD5SUMS" ]; then
            MD5SUMS_TO_COPY="$SOURCE_DIR/lib/MD5SUMS"
        fi
        
        if [ -n "$MD5SUMS_TO_COPY" ] && [ -f "$MD5SUMS_TO_COPY" ]; then
            print_status "📋 Copying MD5SUMS to /sphere/MD5SUMS for reference..."
            print_status "   Source: $MD5SUMS_TO_COPY"
            mkdir -p /sphere
            if rsync -av "$MD5SUMS_TO_COPY" /sphere/MD5SUMS; then
                print_status "✅ MD5SUMS saved to /sphere/MD5SUMS"
                print_status "   You can verify files later with: md5sum -c /sphere/MD5SUMS"
            else
                print_error "❌ Failed to copy MD5SUMS to /sphere/"
                print_error "   Tried to copy: $MD5SUMS_TO_COPY"
                ls -la "$MD5SUMS_TO_COPY" || true
            fi
        else
            print_warning "⚠️  MD5SUMS file not found - cannot copy to /sphere/"
            print_warning "   Checked: MD5SUMS, lib/MD5SUMS, $SOURCE_DIR/MD5SUMS, $SOURCE_DIR/lib/MD5SUMS"
        fi
        
        # ALWAYS verify critical files were copied and match source (even if MD5SUMS doesn't exist)
        print_status "🔍 Verifying critical lib files match source..."
        for critical_file in "utils.py" "es_training.py"; do
            if [ -f "lib/$critical_file" ]; then
                if [ ! -f "$TARGET_DIR/lib/$critical_file" ]; then
                    print_error "❌ $critical_file was not copied to $TARGET_DIR/lib/"
                    print_error "   Copying now..."
                    # Use SOURCE_DIR if available, otherwise current directory
                    if [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/lib/$critical_file" ]; then
                        rsync -av "$SOURCE_DIR/lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                    else
                        rsync -av "lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                    fi
                    chmod 644 "$TARGET_DIR/lib/$critical_file" || true
                fi
                
                # Always verify md5sum matches source
                SRC_MD5=$(md5sum "lib/$critical_file" | cut -d' ' -f1)
                TGT_MD5=$(md5sum "$TARGET_DIR/lib/$critical_file" | cut -d' ' -f1)
                if [ "$SRC_MD5" = "$TGT_MD5" ]; then
                    print_status "✅ $critical_file md5sum matches source ($SRC_MD5)"
                else
                    print_error "❌ MD5 mismatch for $critical_file"
                    print_error "   Source: $SRC_MD5"
                    print_error "   Target: $TGT_MD5"
                    print_error "   Forcing copy..."
                    # Use SOURCE_DIR if available, otherwise current directory
                    if [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/lib/$critical_file" ]; then
                        rsync -av "$SOURCE_DIR/lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                    else
                        rsync -av "lib/$critical_file" "$TARGET_DIR/lib/$critical_file"
                    fi
                    chmod 644 "$TARGET_DIR/lib/$critical_file" || true
                    TGT_MD5=$(md5sum "$TARGET_DIR/lib/$critical_file" | cut -d' ' -f1)
                    if [ "$SRC_MD5" = "$TGT_MD5" ]; then
                        print_status "✅ Fixed - $critical_file md5sum now matches"
                    else
                        print_error "❌ CRITICAL: Still mismatched after force copy"
                        print_error "   This indicates a serious deployment issue"
                        print_error "   Source MD5: $SRC_MD5"
                        print_error "   Target MD5: $TGT_MD5"
                        print_error "   Target file: $TARGET_DIR/lib/$critical_file"
                        ls -la "$TARGET_DIR/lib/$critical_file" || true
                        exit 1
                    fi
                fi
            else
                print_warning "⚠️  Source file not found: lib/$critical_file"
            fi
        done
        
        # Copy ONLY source code subdirectories - DO NOT copy runtime job output directories
        # Whitelist approach: only copy known source directories
        for dir in */; do
            dirname=$(basename "$dir")
            if [ "$dirname" != "lib" ] && [ "$dirname" != "__pycache__" ] && [ -d "$dir" ]; then
                # Skip runtime data directories and job output directories
                case "$dirname" in
                    # Known runtime data directories
                    featrix_output|featrix_sessions|featrix_sessions_private|featrix_queue|featrix_data|jobs|dev_data|build)
                        continue
                        ;;
                    # Job output directories (match patterns)
                    create_structured_data*|train_es*|train_knn*|run_clustering*|train_single_predictor*|generate_movie_frame*|cpu_data_tasks*|json_es_training*|input_data*|logs*|*_*_*)
                        # Skip directories that look like job outputs (date-hash pattern or known job types)
                        continue
                        ;;
                esac
                # Only copy if it's a known source directory (add to whitelist as needed)
                print_status "Skipping $dirname/ (not in source code whitelist)"
            fi
        done
    else
        print_warning "Neither src/ nor lib/ directory found - unexpected structure"
    fi
    
    # Remove OLD /sphere/app/src if it exists (from previous broken deployments)
    if [ -d "$TARGET_DIR/src" ]; then
        print_warning "Removing old /sphere/app/src directory from broken deployment..."
        rm -rf "$TARGET_DIR/src"
    fi
    
    # Copy VERSION file to /sphere/VERSION and /sphere/app/VERSION
    # Always copy VERSION file (force update) to ensure version is updated
    # Determine REPO_ROOT based on where the script is located (same logic as setup_venv)
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Try to find REPO_ROOT (where the package files are)
    LOCAL_REPO_ROOT=""
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        LOCAL_REPO_ROOT="$SCRIPT_DIR"
    elif [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
        LOCAL_REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    elif [ -f "requirements.txt" ]; then
        LOCAL_REPO_ROOT="$(pwd)"
    fi
    
    print_status "Looking for VERSION file..."
    print_status "  SCRIPT_DIR: $SCRIPT_DIR"
    print_status "  LOCAL_REPO_ROOT: $LOCAL_REPO_ROOT"
    print_status "  Current dir: $(pwd)"
    
    VERSION_SOURCE=""
    if [ -n "$LOCAL_REPO_ROOT" ] && [ -f "$LOCAL_REPO_ROOT/VERSION" ]; then
        VERSION_SOURCE="$LOCAL_REPO_ROOT/VERSION"
        print_status "✅ Found VERSION at: $VERSION_SOURCE"
    elif [ -f "VERSION" ] && [ "$(readlink -f VERSION 2>/dev/null || echo "")" != "$(readlink -f $TARGET_DIR/VERSION 2>/dev/null || echo "")" ]; then
        VERSION_SOURCE="VERSION"
        print_status "✅ Found VERSION in current directory: $VERSION_SOURCE"
    else
        print_warning "⚠️  VERSION file not found"
        if [ -n "$LOCAL_REPO_ROOT" ]; then
            print_warning "   Checked: $LOCAL_REPO_ROOT/VERSION"
            print_warning "   Listing $LOCAL_REPO_ROOT contents:"
            ls -la "$LOCAL_REPO_ROOT" 2>/dev/null | head -10 || print_warning "   Could not list $LOCAL_REPO_ROOT"
        fi
        print_warning "   Also checked current directory: $(pwd)"
    fi
    
    if [ -n "$VERSION_SOURCE" ] && [ -f "$VERSION_SOURCE" ]; then
        print_status "Copying VERSION file from $VERSION_SOURCE..."
        package_version=$(cat "$VERSION_SOURCE" 2>/dev/null || echo "unknown")
        print_status "Package version: $package_version"
        
        # Force copy to /sphere/VERSION
        if cp -f "$VERSION_SOURCE" /sphere/VERSION; then
            print_status "✅ Copied VERSION to /sphere/VERSION: $(cat /sphere/VERSION 2>/dev/null || echo 'unknown')"
        else
            print_error "❌ Failed to copy VERSION to /sphere/VERSION"
        fi
        
        # Force copy to TARGET_DIR/VERSION
        if cp -f "$VERSION_SOURCE" "$TARGET_DIR/VERSION"; then
            print_status "✅ Copied VERSION to $TARGET_DIR/VERSION: $(cat "$TARGET_DIR/VERSION" 2>/dev/null || echo 'unknown')"
        else
            print_error "❌ Failed to copy VERSION to $TARGET_DIR/VERSION"
        fi
        
        # Also write git commit date and hash for version checking
        if [ -d ".git" ]; then
            git_date=$(git show -s --format=%ci HEAD 2>/dev/null || echo "")
            git_hash=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
            git_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
            
            if [ -n "$git_date" ]; then
                echo "$git_date" > /sphere/VERSION_DATE || { print_warning "Failed to write VERSION_DATE"; }
                echo "$git_date" > "$TARGET_DIR/VERSION_DATE" || { print_warning "Failed to write VERSION_DATE to app"; }
            fi
            
            if [ -n "$git_hash" ]; then
                echo "$git_hash" > /sphere/VERSION_HASH || { print_warning "Failed to write VERSION_HASH"; }
                echo "$git_hash" > "$TARGET_DIR/VERSION_HASH" || { print_warning "Failed to write VERSION_HASH to app"; }
            fi
            
            if [ -n "$git_branch" ]; then
                echo "$git_branch" > /sphere/VERSION_BRANCH || { print_warning "Failed to write VERSION_BRANCH"; }
                echo "$git_branch" > "$TARGET_DIR/VERSION_BRANCH" || { print_warning "Failed to write VERSION_BRANCH to app"; }
            fi
            
            print_status "Saved version info: $git_hash on $git_branch at $git_date"
        else
            # No git repo (tarball deployment) - copy VERSION_HASH, VERSION_DATE, VERSION_BRANCH from package if they exist
            # Use LOCAL_REPO_ROOT to find files from package
            if [ -n "$LOCAL_REPO_ROOT" ] && [ -f "$LOCAL_REPO_ROOT/VERSION_HASH" ]; then
                cp -f "$LOCAL_REPO_ROOT/VERSION_HASH" /sphere/VERSION_HASH || { print_warning "Failed to copy VERSION_HASH to /sphere/"; }
                cp -f "$LOCAL_REPO_ROOT/VERSION_HASH" "$TARGET_DIR/VERSION_HASH" || { print_warning "Failed to copy VERSION_HASH to app"; }
                print_status "Copied VERSION_HASH from package: $(cat "$LOCAL_REPO_ROOT/VERSION_HASH" 2>/dev/null || echo 'unknown')"
            elif [ -f "VERSION_HASH" ] && [ "$(readlink -f VERSION_HASH 2>/dev/null || echo "")" != "$(readlink -f $TARGET_DIR/VERSION_HASH 2>/dev/null || echo "")" ]; then
                cp -f VERSION_HASH /sphere/VERSION_HASH || { print_warning "Failed to copy VERSION_HASH to /sphere/"; }
                cp -f VERSION_HASH "$TARGET_DIR/VERSION_HASH" || { print_warning "Failed to copy VERSION_HASH to app"; }
                print_status "Copied VERSION_HASH from package: $(cat VERSION_HASH 2>/dev/null || echo 'unknown')"
            fi
            
            if [ -n "$LOCAL_REPO_ROOT" ] && [ -f "$LOCAL_REPO_ROOT/VERSION_DATE" ]; then
                cp -f "$LOCAL_REPO_ROOT/VERSION_DATE" /sphere/VERSION_DATE || { print_warning "Failed to copy VERSION_DATE to /sphere/"; }
                cp -f "$LOCAL_REPO_ROOT/VERSION_DATE" "$TARGET_DIR/VERSION_DATE" || { print_warning "Failed to copy VERSION_DATE to app"; }
            elif [ -f "VERSION_DATE" ] && [ "$(readlink -f VERSION_DATE 2>/dev/null || echo "")" != "$(readlink -f $TARGET_DIR/VERSION_DATE 2>/dev/null || echo "")" ]; then
                cp -f VERSION_DATE /sphere/VERSION_DATE || { print_warning "Failed to copy VERSION_DATE to /sphere/"; }
                cp -f VERSION_DATE "$TARGET_DIR/VERSION_DATE" || { print_warning "Failed to copy VERSION_DATE to app"; }
            fi
            
            if [ -n "$LOCAL_REPO_ROOT" ] && [ -f "$LOCAL_REPO_ROOT/VERSION_BRANCH" ]; then
                cp -f "$LOCAL_REPO_ROOT/VERSION_BRANCH" /sphere/VERSION_BRANCH || { print_warning "Failed to copy VERSION_BRANCH to /sphere/"; }
                cp -f "$LOCAL_REPO_ROOT/VERSION_BRANCH" "$TARGET_DIR/VERSION_BRANCH" || { print_warning "Failed to copy VERSION_BRANCH to app"; }
            elif [ -f "VERSION_BRANCH" ] && [ "$(readlink -f VERSION_BRANCH 2>/dev/null || echo "")" != "$(readlink -f $TARGET_DIR/VERSION_BRANCH 2>/dev/null || echo "")" ]; then
                cp -f VERSION_BRANCH /sphere/VERSION_BRANCH || { print_warning "Failed to copy VERSION_BRANCH to /sphere/"; }
                cp -f VERSION_BRANCH "$TARGET_DIR/VERSION_BRANCH" || { print_warning "Failed to copy VERSION_BRANCH to app"; }
            fi
        fi
    else
        print_error "❌ Cannot copy VERSION file - source not found or invalid"
        print_error "   VERSION_SOURCE: $VERSION_SOURCE"
    fi
    
    # Copy ffsh script if it exists (check multiple locations)
    print_status "Looking for ffsh script..."
    print_status "  SCRIPT_DIR: $SCRIPT_DIR"
    print_status "  LOCAL_REPO_ROOT: $LOCAL_REPO_ROOT"
    print_status "  Current dir: $(pwd)"
    
    FFSH_SOURCE=""
    # Check in order of preference:
    # 1. LOCAL_REPO_ROOT (repo root, most reliable) - but skip if it's the target dir
    # 2. Current directory (if in tarball or source repo)
    # 3. SCRIPT_DIR parent (repo root when script is in src/)
    # 4. Common source repository locations (always check these)
    # 5. Try to find git root (from current dir or script dir)
    # 6. REPO_ROOT (if set, legacy)
    
    # First, check LOCAL_REPO_ROOT if it's not the target directory
    if [ -n "$LOCAL_REPO_ROOT" ] && [ "$LOCAL_REPO_ROOT" != "$TARGET_DIR" ] && [ -f "$LOCAL_REPO_ROOT/ffsh" ]; then
        FFSH_SOURCE="$LOCAL_REPO_ROOT/ffsh"
        print_status "  ✅ Found at: $LOCAL_REPO_ROOT/ffsh"
    # Check current directory (works for tarball extractions)
    elif [ -f "ffsh" ]; then
        FFSH_SOURCE="$(cd "$(dirname "ffsh")" && pwd)/ffsh"
        print_status "  ✅ Found at: $FFSH_SOURCE (current directory)"
    # Check SCRIPT_DIR parent
    elif [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/../ffsh" ]; then
        FFSH_SOURCE="$(cd "$SCRIPT_DIR/.." && pwd)/ffsh"
        print_status "  ✅ Found at: $FFSH_SOURCE (SCRIPT_DIR parent)"
    # Always check common source repository locations (works for tarball deployments)
    elif [ -z "$FFSH_SOURCE" ]; then
        for SOURCE_REPO in "/home/mitch/sphere" "/home/ubuntu/sphere" "$HOME/sphere"; do
            if [ -f "$SOURCE_REPO/ffsh" ]; then
                FFSH_SOURCE="$SOURCE_REPO/ffsh"
                print_status "  ✅ Found at: $SOURCE_REPO/ffsh (source repository)"
                break
            fi
        done
    fi
    
    # Continue with other checks if not found yet
    if [ -z "$FFSH_SOURCE" ]; then
        # Try git root from current directory
        if command -v git >/dev/null 2>&1 && [ -d ".git" ]; then
            GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
            if [ -n "$GIT_ROOT" ] && [ -f "$GIT_ROOT/ffsh" ]; then
                FFSH_SOURCE="$GIT_ROOT/ffsh"
                print_status "  ✅ Found at: $GIT_ROOT/ffsh (git root from current dir)"
            fi
        fi
        # Also try from script directory
        if [ -z "$FFSH_SOURCE" ] && command -v git >/dev/null 2>&1 && [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/../.git" ]; then
            GIT_ROOT=$(cd "$SCRIPT_DIR/.." && git rev-parse --show-toplevel 2>/dev/null || echo "")
            if [ -n "$GIT_ROOT" ] && [ -f "$GIT_ROOT/ffsh" ]; then
                FFSH_SOURCE="$GIT_ROOT/ffsh"
                print_status "  ✅ Found at: $GIT_ROOT/ffsh (git root from script dir)"
            fi
        fi
        # Last resort: REPO_ROOT (legacy)
        if [ -z "$FFSH_SOURCE" ] && [ -n "$REPO_ROOT" ] && [ -f "$REPO_ROOT/ffsh" ]; then
            FFSH_SOURCE="$REPO_ROOT/ffsh"
            print_status "  ✅ Found at: $REPO_ROOT/ffsh"
        fi
    fi
    
    if [ -n "$FFSH_SOURCE" ]; then
        print_status "Copying ffsh script from $FFSH_SOURCE..."
        if safe_copy "$FFSH_SOURCE" "$TARGET_DIR/ffsh"; then
            chmod +x "$TARGET_DIR/ffsh" || { print_warning "Failed to make ffsh executable"; }
            print_status "✅ ffsh script copied and made executable"
        else
            print_warning "Failed to copy ffsh script from $FFSH_SOURCE"
        fi
    else
        print_warning "ffsh script not found"
    fi
    
    # Copy ffsh completion script if it exists
    FFSH_COMPLETION_SOURCE=""
    # Check multiple locations (same logic as ffsh script)
    if [ -f "ffsh-completion.bash" ]; then
        FFSH_COMPLETION_SOURCE="$(cd "$(dirname "ffsh-completion.bash")" && pwd)/ffsh-completion.bash"
        print_status "  ✅ Found at: $FFSH_COMPLETION_SOURCE (current directory)"
    elif [ -n "$LOCAL_REPO_ROOT" ] && [ "$LOCAL_REPO_ROOT" != "$TARGET_DIR" ] && [ -f "$LOCAL_REPO_ROOT/ffsh-completion.bash" ]; then
        FFSH_COMPLETION_SOURCE="$LOCAL_REPO_ROOT/ffsh-completion.bash"
        print_status "  ✅ Found at: $LOCAL_REPO_ROOT/ffsh-completion.bash"
    elif [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/../ffsh-completion.bash" ]; then
        FFSH_COMPLETION_SOURCE="$(cd "$SCRIPT_DIR/.." && pwd)/ffsh-completion.bash"
        print_status "  ✅ Found at: $FFSH_COMPLETION_SOURCE (SCRIPT_DIR parent)"
    elif [ -n "$SOURCE_DIR" ] && [ -f "$(dirname "$SOURCE_DIR")/ffsh-completion.bash" ]; then
        FFSH_COMPLETION_SOURCE="$(dirname "$SOURCE_DIR")/ffsh-completion.bash"
        print_status "  ✅ Found at: $FFSH_COMPLETION_SOURCE (source repo root)"
    elif [ -n "$REPO_ROOT" ] && [ -f "$REPO_ROOT/ffsh-completion.bash" ]; then
        FFSH_COMPLETION_SOURCE="$REPO_ROOT/ffsh-completion.bash"
        print_status "  ✅ Found at: $REPO_ROOT/ffsh-completion.bash"
    fi
    
    # Also check git root if available
    if [ -z "$FFSH_COMPLETION_SOURCE" ] && command -v git >/dev/null 2>&1; then
        if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/../.git" ]; then
            GIT_ROOT="$(cd "$SCRIPT_DIR/.." && git rev-parse --show-toplevel 2>/dev/null || echo "")"
            if [ -n "$GIT_ROOT" ] && [ -f "$GIT_ROOT/ffsh-completion.bash" ]; then
                FFSH_COMPLETION_SOURCE="$GIT_ROOT/ffsh-completion.bash"
                print_status "  ✅ Found at: $GIT_ROOT/ffsh-completion.bash (git root)"
            fi
        fi
    fi
    
    if [ -n "$FFSH_COMPLETION_SOURCE" ]; then
        print_status "Copying ffsh completion script from $FFSH_COMPLETION_SOURCE..."
        if safe_copy "$FFSH_COMPLETION_SOURCE" "$TARGET_DIR/ffsh-completion.bash"; then
            chmod +x "$TARGET_DIR/ffsh-completion.bash" || { print_warning "Failed to make ffsh-completion.bash executable"; }
            print_status "✅ ffsh completion script copied"
            
            # Install completion system-wide
            print_status "Installing ffsh bash completion system-wide..."
            
            # Method 1: Install to /etc/bash_completion.d/ (if directory exists)
            if [ -d "/etc/bash_completion.d" ]; then
                if safe_copy "$TARGET_DIR/ffsh-completion.bash" "/etc/bash_completion.d/ffsh"; then
                    print_status "✅ Installed to /etc/bash_completion.d/ffsh"
                else
                    print_warning "Failed to install to /etc/bash_completion.d/"
                fi
            fi
            
            # Method 2: Install to /etc/profile.d/ (works for all shells)
            if [ -d "/etc/profile.d" ]; then
                cat > "/etc/profile.d/ffsh-completion.sh" << 'EOF'
# ffsh bash completion
if [ -f /sphere/app/ffsh-completion.bash ]; then
    source /sphere/app/ffsh-completion.bash
fi
EOF
                chmod 644 "/etc/profile.d/ffsh-completion.sh"
                print_status "✅ Installed to /etc/profile.d/ffsh-completion.sh"
            fi
            
            # Method 3: Add to root's .bashrc if it exists
            if [ -f "/root/.bashrc" ]; then
                if ! grep -q "ffsh-completion.bash" "/root/.bashrc"; then
                    echo "" >> "/root/.bashrc"
                    echo "# ffsh bash completion" >> "/root/.bashrc"
                    echo "if [ -f /sphere/app/ffsh-completion.bash ]; then" >> "/root/.bashrc"
                    echo "    source /sphere/app/ffsh-completion.bash" >> "/root/.bashrc"
                    echo "fi" >> "/root/.bashrc"
                    print_status "✅ Added to /root/.bashrc"
                else
                    print_status "ℹ️  Already in /root/.bashrc"
                fi
            fi
        else
            print_warning "Failed to copy ffsh completion script from $FFSH_COMPLETION_SOURCE"
        fi
    else
        print_warning "ffsh-completion.bash not found (optional)"
        print_warning "  Checked:"
        [ -n "$LOCAL_REPO_ROOT" ] && [ "$LOCAL_REPO_ROOT" != "$TARGET_DIR" ] && print_warning "    - $LOCAL_REPO_ROOT/ffsh-completion.bash"
        print_warning "    - $(pwd)/ffsh-completion.bash"
        [ -n "$SCRIPT_DIR" ] && print_warning "    - $SCRIPT_DIR/../ffsh-completion.bash"
        [ -n "$SOURCE_DIR" ] && print_warning "    - $(dirname "$SOURCE_DIR")/ffsh-completion.bash"
        for SOURCE_REPO in "/home/mitch/sphere" "/home/ubuntu/sphere" "$HOME/sphere"; do
            print_warning "    - $SOURCE_REPO/ffsh-completion.bash"
        done
        [ -n "$REPO_ROOT" ] && print_warning "    - $REPO_ROOT/ffsh-completion.bash"
    fi
    
    # Copy ffsh_simple.py if it exists (needed as fallback)
    FFSH_SIMPLE_SOURCE=""
    if [ -f "ffsh_simple.py" ]; then
        FFSH_SIMPLE_SOURCE="ffsh_simple.py"
    elif [ -f "$LOCAL_REPO_ROOT/ffsh_simple.py" ]; then
        FFSH_SIMPLE_SOURCE="$LOCAL_REPO_ROOT/ffsh_simple.py"
    elif [ -f "$REPO_ROOT/ffsh_simple.py" ]; then
        FFSH_SIMPLE_SOURCE="$REPO_ROOT/ffsh_simple.py"
    fi
    
    if [ -n "$FFSH_SIMPLE_SOURCE" ]; then
        print_status "Copying ffsh_simple.py from $FFSH_SIMPLE_SOURCE..."
        safe_copy "$FFSH_SIMPLE_SOURCE" "$TARGET_DIR/ffsh_simple.py" || { print_warning "Failed to copy ffsh_simple.py"; }
        chmod +x "$TARGET_DIR/ffsh_simple.py" || { print_warning "Failed to make ffsh_simple.py executable"; }
        print_status "✅ ffsh_simple.py copied and made executable"
    else
        print_warning "ffsh_simple.py not found (checked current directory, $LOCAL_REPO_ROOT, and $REPO_ROOT)"
    fi
    
    # Compile sbit (setuid wrapper for ffsh) if sbit.c exists
    SBIT_SOURCE=""
    if [ -f "sbit.c" ]; then
        SBIT_SOURCE="sbit.c"
    elif [ -f "$LOCAL_REPO_ROOT/sbit.c" ]; then
        SBIT_SOURCE="$LOCAL_REPO_ROOT/sbit.c"
    elif [ -f "$REPO_ROOT/sbit.c" ]; then
        SBIT_SOURCE="$REPO_ROOT/sbit.c"
    elif [ -f "$TARGET_DIR/sbit.c" ]; then
        SBIT_SOURCE="$TARGET_DIR/sbit.c"
    fi
    
    if [ -n "$SBIT_SOURCE" ]; then
        print_status "Compiling sbit (setuid wrapper for ffsh) from $SBIT_SOURCE..."
        # Check for gcc
        if ! command -v gcc >/dev/null 2>&1; then
            print_error "gcc not found - cannot compile sbit. Install with: apt-get install build-essential"
            exit 1
        fi
        # Copy source to target dir first
        safe_copy "$SBIT_SOURCE" "$TARGET_DIR/sbit.c" || { print_warning "Failed to copy sbit.c"; }
        # Compile
        if gcc -o "$TARGET_DIR/sbit" "$TARGET_DIR/sbit.c"; then
            print_status "✅ sbit compiled successfully"
            # Set setuid bit (requires root)
            if [ "$(id -u)" -eq 0 ]; then
                # Already root
                chown root:root "$TARGET_DIR/sbit"
                chmod 4755 "$TARGET_DIR/sbit"
            else
                # Not root, use sudo
                sudo chown root:root "$TARGET_DIR/sbit"
                sudo chmod 4755 "$TARGET_DIR/sbit"
            fi
            # Verify setuid bit was set (look for 's' in permissions)
            if ls -la "$TARGET_DIR/sbit" | grep -q '^-rws'; then
                print_status "✅ sbit installed with setuid bit"
            else
                print_error "Failed to set setuid bit on sbit - permissions are:"
                ls -la "$TARGET_DIR/sbit"
                print_error "Expected: -rwsr-xr-x"
                print_error "Try manually: sudo chmod 4755 $TARGET_DIR/sbit"
                exit 1
            fi
        else
            print_error "Failed to compile sbit"
            exit 1
        fi
    else
        print_warning "sbit.c not found - sbit will not be available"
    fi
    
    # Create run script if it doesn't exist
    if [ ! -f "$TARGET_DIR/run_api_server.sh" ]; then
        print_status "Creating run_api_server.sh script..."
        cat > "$TARGET_DIR/run_api_server.sh" << 'EOF'
#!/bin/bash
cd /sphere/app
source /sphere/.venv/bin/activate
exec uvicorn api:app --host 0.0.0.0 --port 8000 --log-level info
EOF
        chmod +x "$TARGET_DIR/run_api_server.sh"
    fi
    
    # Copy additional scripts if they exist (handle glob expansion failure)
    set +e  # Temporarily disable exit on error for glob
    for script in *.sh; do
        # Check if glob matched actual files (not literal "*.sh")
        if [ -f "$script" ] && [ "$script" != "churro-copy.sh" ] && [ "$script" != "*.sh" ]; then
            # Use safe_copy to skip if source and destination are the same file
            safe_copy "$script" "$TARGET_DIR/$script" || { print_warning "Failed to copy script: $script"; }
            chmod +x "$TARGET_DIR/$script" || { print_warning "Failed to chmod script: $script"; }
        fi
    done
    set -e  # Re-enable exit on error
    
    # Set ownership
    chown -R root:root "$TARGET_DIR" || { print_warning "Failed to set ownership"; }
    
    print_status "Application files copied"
}

# Function to clean Python cache files
clean_python_cache() {
    print_section "Cleaning Python cache files..."
    
    # Remove __pycache__ directories from application
    print_status "Removing __pycache__ directories from $TARGET_DIR..."
    find "$TARGET_DIR" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    
    # Remove .pyc files from application
    print_status "Removing .pyc files from $TARGET_DIR..."
    find "$TARGET_DIR" -type f -name '*.pyc' -delete 2>/dev/null || true
    
    # Remove .pyo files (optimized bytecode)
    print_status "Removing .pyo files from $TARGET_DIR..."
    find "$TARGET_DIR" -type f -name '*.pyo' -delete 2>/dev/null || true
    
    # Clean venv cache too if it exists
    if [ -d "$VENV_DIR" ]; then
        print_status "Removing __pycache__ directories from venv..."
        find "$VENV_DIR" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
        print_status "Removing .pyc files from venv..."
        find "$VENV_DIR" -type f -name '*.pyc' -delete 2>/dev/null || true
    fi
    
    print_status "✅ Python cache cleaned"
}

# Function to kill ALL old Sphere-related Python processes (orphaned workers, old queue watchers, etc.)
kill_all_old_sphere_processes() {
    print_status "Killing all old Sphere-related Python processes..."
    
    # Kill old file-based queue watchers (we removed this system)
    print_status "   Killing old cli.py watch-queue processes..."
    sh -c 'timeout 2 sudo pkill -9 -f "cli.py watch-queue" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 -f "watch-queue.*--queue-name" 2>/dev/null || true' 2>/dev/null || true
    
    # Kill orphaned supervisor-managed processes (system_monitor, auto_upgrade_monitor, etc.)
    # These are processes that were started by old supervisor instances but are now orphaned
    # We kill ALL of them - supervisor will restart the ones it needs
    print_status "   Killing orphaned supervisor-managed processes..."
    sh -c 'timeout 2 sudo pkill -9 -f "system_monitor.py" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 -f "auto_upgrade_monitor.py" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 -f "gc_cleanup.py" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 -f "featrix_watchdog.py" 2>/dev/null || true' 2>/dev/null || true
    
    # Kill any other Python processes from /sphere/app that look orphaned
    # This is aggressive but necessary - supervisor will restart what it needs
    print_status "   Killing orphaned /sphere/app Python processes..."
    # Get the current script PID and supervisor PID to avoid killing ourselves
    SCRIPT_PID=$$
    SUPERVISOR_PID=$(pgrep -f "supervisord.*supervisord.conf" | head -1 || true)
    
    # Find all Python processes from /sphere/app
    ALL_SPHERE_PIDS=$(pgrep -f "/sphere/app" 2>/dev/null || true)
    if [ -n "$ALL_SPHERE_PIDS" ]; then
        for pid in $ALL_SPHERE_PIDS; do
            # Skip if it's the current script
            if [ "$pid" = "$SCRIPT_PID" ]; then
                continue
            fi
            # Skip if it's the current supervisor (if running)
            if [ -n "$SUPERVISOR_PID" ] && [ "$pid" = "$SUPERVISOR_PID" ]; then
                continue
            fi
            # Skip if it's a uvicorn process (handled separately)
            if ps -p "$pid" -o cmd= 2>/dev/null | grep -q uvicorn; then
                continue
            fi
            # Skip if it's a celery process (handled separately)
            if ps -p "$pid" -o cmd= 2>/dev/null | grep -q celery; then
                continue
            fi
            # Kill it
            sudo kill -9 "$pid" 2>/dev/null || true
        done
    fi
    
    sleep 0.5
    print_status "   ✅ Old processes cleanup complete"
}

# Function to aggressively kill all Celery worker processes
# This prevents orphaned workers from blocking supervisor-managed workers
kill_all_celery_workers() {
    print_status "Aggressively killing all Celery worker processes..."
    
    # Step 1: Stop via supervisorctl (if supervisor is running)
    supervisorctl stop featrix-cpu_worker featrix-gpu_training >/dev/null 2>&1 || true
    sleep 1
    
    # Step 2: Get all PIDs first and kill them
    CELERY_PIDS=$(pgrep -f "celery.*worker" 2>/dev/null || true)
    if [ -n "$CELERY_PIDS" ]; then
        print_status "   Found Celery worker PIDs: $CELERY_PIDS"
        echo "$CELERY_PIDS" | xargs -r sudo kill -9 2>/dev/null || true
        sleep 1
    fi
    
    # Step 3: Kill via pkill (more aggressive, catches any pattern)
    sh -c 'timeout 2 sudo pkill -9 -f "celery.*worker" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 -f "celery -A celery_app" 2>/dev/null || true' 2>/dev/null || true
    sh -c 'timeout 2 sudo pkill -9 celery 2>/dev/null || true' 2>/dev/null || true
    sleep 1
    
    # Step 4: Verify all are gone (retry up to 3 times)
    for attempt in 1 2 3; do
        REMAINING=$(pgrep -f "celery.*worker" 2>/dev/null || true)
        if [ -z "$REMAINING" ]; then
            break
        fi
        print_status "   Attempt $attempt: Still found Celery workers, killing: $REMAINING"
        echo "$REMAINING" | xargs -r sudo kill -9 2>/dev/null || true
        sleep 1
    done
    
    # Final check
    FINAL_REMAINING=$(pgrep -f "celery.*worker" 2>/dev/null || true)
    if [ -n "$FINAL_REMAINING" ]; then
        print_warning "   ⚠️  Some Celery workers may still be running: $FINAL_REMAINING"
    else
        print_status "   ✅ All Celery workers killed"
    fi
}

# Function to kill uvicorn processes cleanly (with timeout to prevent hanging)
kill_uvicorn_processes() {
    # Show what uvicorn processes are running before killing
    print_status "Checking for uvicorn processes..."
    UVICORN_PIDS=$(pgrep -f uvicorn 2>/dev/null || true)
    if [ -n "$UVICORN_PIDS" ]; then
        print_status "Found uvicorn processes:"
        ps auxw | grep -E "[u]vicorn" | while read line; do
            print_status "   $line"
        done
        
        # Kill by process name (with 2 second timeout to prevent hanging)
        # Use sh -c to suppress "Killed" messages from bash
        sh -c 'timeout 2 sudo pkill -9 uvicorn 2>/dev/null || true' 2>/dev/null || true
        sh -c 'timeout 2 sudo pkill -9 -f "uvicorn.*api:app" 2>/dev/null || true' 2>/dev/null || true
        sh -c 'timeout 2 sudo pkill -9 -f "uvicorn.*--port" 2>/dev/null || true' 2>/dev/null || true
    else
        print_status "   No uvicorn processes found - skipping kill"
    fi
    
    # Kill anything using port 8000 (fast check with timeout, non-blocking)
    # Use a subshell with timeout to prevent hanging
    (
        if command -v lsof >/dev/null 2>&1; then
            PIDS=$(timeout 1 lsof -ti :8000 2>/dev/null || true)
            if [ -n "$PIDS" ]; then
                echo "$PIDS" | xargs -r -n1 sh -c 'timeout 1 sudo kill -9 "$1" 2>/dev/null || true' _ || true
            fi
        elif command -v ss >/dev/null 2>&1; then
            PIDS=$(timeout 1 ss -tlnp 2>/dev/null | grep ":8000 " | grep -oP 'pid=\K\d+' || true)
            if [ -n "$PIDS" ]; then
                echo "$PIDS" | xargs -r -n1 sh -c 'timeout 1 sudo kill -9 "$1" 2>/dev/null || true' _ || true
            fi
        fi
    ) &
    local port_check_pid=$!
    timeout 3 wait $port_check_pid 2>/dev/null || kill $port_check_pid 2>/dev/null || true
    
    # Minimal wait - processes should die quickly with SIGKILL
    sleep 0.2
}

# Function to fix supervisor if it's broken
fix_supervisor_if_broken() {
    print_section "Checking supervisor health..."
    
    # ALWAYS kill uvicorn processes FIRST - they block supervisor startup
    print_status "Killing uvicorn processes..."
    kill_uvicorn_processes
    
    # ALWAYS kill zombie processes and clear ports
    # This prevents "port already in use" errors
    print_status "Clearing any zombie processes and ports..."
    
    # Don't stop supervisor - just check for port conflicts
    # systemctl stop supervisor 2>/dev/null || true
    # sleep 0.2
    
    # Don't kill supervisord processes - supervisor is managed by systemd
    # Only kill processes that are holding the port but aren't the systemd-managed supervisor
    # sh -c 'timeout 2 sudo pkill -9 supervisord 2>/dev/null || true' 2>/dev/null || true
    # sh -c 'timeout 2 sudo pkill -9 -f supervisord 2>/dev/null || true' 2>/dev/null || true
    # sleep 0.2
    
    # Clean up socket files
    print_status "Cleaning up supervisor sockets..."
    rm -f /var/run/supervisor.sock /var/run/supervisor/* /tmp/supervisor.sock /tmp/supervisord.sock 2>/dev/null || true
    # Also clean up any supervisor directories
    rm -rf /var/run/supervisor 2>/dev/null || true
    mkdir -p /var/run/supervisor 2>/dev/null || true
    chmod 755 /var/run/supervisor 2>/dev/null || true
    
    # Check and kill anything using supervisor's HTTP port (9001)
    SUPERVISOR_PORT="9001"
    if [ -f /etc/supervisor/supervisord.conf ]; then
        FOUND_PORT=$(grep -A 10 "\[inet_http_server\]" /etc/supervisor/supervisord.conf 2>/dev/null | grep -E "^port\s*=" | head -1 | awk -F'=' '{print $2}' | tr -d ' ' || true)
        if [ -n "$FOUND_PORT" ] && [ "$FOUND_PORT" != "" ]; then
            SUPERVISOR_PORT="$FOUND_PORT"
        fi
    fi
    
    print_status "Checking for processes using supervisor port $SUPERVISOR_PORT..."
    if command -v lsof >/dev/null 2>&1; then
        PIDS=$(lsof -ti :$SUPERVISOR_PORT 2>/dev/null || true)
        if [ -n "$PIDS" ]; then
            echo "$PIDS" | while read pid; do
                if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                    CMD=$(ps -p $pid -o comm=,args= 2>/dev/null | head -1 || echo "unknown")
                    print_status "   Port $SUPERVISOR_PORT: PID $pid - $CMD"
                    kill -9 "$pid" 2>/dev/null || true
                fi
            done
            sleep 0.5
        else
            print_status "   Port $SUPERVISOR_PORT: No processes found"
        fi
    elif command -v ss >/dev/null 2>&1; then
        PIDS=$(ss -tlnp 2>/dev/null | grep ":$SUPERVISOR_PORT " | grep -oP 'pid=\K\d+' || true)
        if [ -n "$PIDS" ]; then
            echo "$PIDS" | while read pid; do
                if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                    CMD=$(ps -p $pid -o comm=,args= 2>/dev/null | head -1 || echo "unknown")
                    print_status "   Port $SUPERVISOR_PORT: PID $pid - $CMD"
                    kill -9 "$pid" 2>/dev/null || true
                fi
            done
            sleep 0.5
        else
            print_status "   Port $SUPERVISOR_PORT: No processes found"
        fi
    fi
    
    # Check if supervisor service is running
    if ! systemctl is-active --quiet supervisor; then
        print_warning "Supervisor service is not running, attempting to fix..."
        
        # Test config before starting - show actual error (with timeout to prevent hanging)
        print_status "Testing supervisor configuration..."
        TEST_OUTPUT=$(timeout 2 supervisord -t 2>&1)
        TEST_EXIT=$?
        if [ $TEST_EXIT -ne 0 ]; then
            print_error "Supervisor configuration is broken! Error:"
            echo "$TEST_OUTPUT" | head -20
            
            # Check if our config has the %h hostname issue
            if grep -q "@%%h\|@%h" /etc/supervisor/conf.d/featrix-sphere.conf 2>/dev/null; then
                print_status "Fixing hostname placeholder in supervisor config..."
                # Replace both %%h (escaped) and %h (unescaped) with churro
                sed -i 's/@%%h/@churro/g; s/@%h/@churro/g' /etc/supervisor/conf.d/featrix-sphere.conf
                
                # Test again
                TEST_OUTPUT=$(supervisord -t 2>&1)
                TEST_EXIT=$?
                if [ $TEST_EXIT -ne 0 ]; then
                    print_error "Still broken after hostname fix. Error:"
                    echo "$TEST_OUTPUT" | head -20
                    print_error "Config file location: /etc/supervisor/conf.d/featrix-sphere.conf"
                    print_error "Showing relevant lines with hostname:"
                    grep -n "hostname\|%%h\|%h" /etc/supervisor/conf.d/featrix-sphere.conf || true
                    exit 1
                else
                    print_status "✅ Config fixed and validated"
                fi
            else
                print_error "Config error is not related to hostname placeholder"
                exit 1
            fi
        else
            print_status "✅ Supervisor configuration is valid"
        fi
        
        # Start supervisor
        print_status "Starting supervisor service..."
        systemctl start supervisor
        sleep 2
        
        # Verify it's working
        if ! systemctl is-active --quiet supervisor; then
            print_error "Failed to start supervisor service"
            systemctl status supervisor --no-pager | head -20
            journalctl -u supervisor -n 20 --no-pager || true
            exit 1
        fi
        
        print_status "✅ Supervisor service started"
    fi
    
    # Check if supervisorctl is responding
    if ! supervisorctl status >/dev/null 2>&1; then
        print_warning "Supervisor not responding, restarting..."
        systemctl restart supervisor
        sleep 5
        
        # Wait for supervisor to be ready
        for i in {1..10}; do
            if supervisorctl status >/dev/null 2>&1; then
                print_status "✅ Supervisor is responding"
                break
            fi
            if [ $i -eq 10 ]; then
                print_error "Supervisor still not responding after restart"
                supervisorctl status
                exit 1
            fi
            sleep 1
        done
    else
        print_status "✅ Supervisor is healthy"
    fi
}

# Function to detect GPU capacity and set Celery concurrency
detect_gpu_capacity() {
    print_status "Detecting GPU capacity for Celery worker configuration..."
    
    CONFIG_FILE="$TARGET_DIR/.celery_gpu_concurrency"
    CONCURRENCY=1  # Default
    
    if command -v nvidia-smi >/dev/null 2>&1; then
        GPU_COUNT=$(nvidia-smi -L 2>/dev/null | wc -l)
        if [ "$GPU_COUNT" -ge 2 ]; then
            CONCURRENCY=2
            print_status "   Detected $GPU_COUNT GPU(s) - setting concurrency to $CONCURRENCY"
        elif [ "$GPU_COUNT" -eq 1 ]; then
            # Check GPU memory - if >32GB, can handle 2 concurrent tasks
            GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
            if [ -n "$GPU_MEM" ] && [ "$GPU_MEM" -gt 32000 ]; then
                CONCURRENCY=2
                print_status "   Detected 1 GPU with ${GPU_MEM}MB memory - setting concurrency to $CONCURRENCY"
            else
                CONCURRENCY=1
                print_status "   Detected 1 GPU with ${GPU_MEM}MB memory - setting concurrency to $CONCURRENCY"
            fi
        else
            print_status "   No GPUs detected - setting concurrency to $CONCURRENCY"
        fi
    else
        print_status "   nvidia-smi not available - using default concurrency $CONCURRENCY"
    fi
    
    # Write config file
    echo "$CONCURRENCY" > "$CONFIG_FILE"
    print_status "   ✅ GPU concurrency config written to $CONFIG_FILE: $CONCURRENCY"
}

# Function to setup supervisor
setup_supervisor() {
    print_section "Setting up supervisor configuration..."
    
    # Kill uvicorn processes FIRST - they can block supervisor
    print_status "Killing uvicorn processes before supervisor setup..."
    kill_uvicorn_processes
    
    # Ensure supervisor config directory exists
    mkdir -p /etc/supervisor/conf.d
    
    # Ensure supervisor is installed
    if ! command -v supervisorctl >/dev/null 2>&1; then
        print_error "Supervisor is not installed! Run install_packages first."
        exit 1
    fi
    
    # Fix supervisor if it's broken BEFORE we try to stop services
    # Let's assume we don't need this # fix_supervisor_if_broken
    
    # Only try to stop services if supervisor is actually running
    # CRITICAL: Never stop string-server during upgrade
    if systemctl is-active --quiet supervisor 2>/dev/null && supervisorctl status >/dev/null 2>&1; then
        SERVICES_TO_STOP=$(get_services_except_string_server)
        if [ -n "$SERVICES_TO_STOP" ]; then
            supervisorctl stop $SERVICES_TO_STOP >/dev/null 2>&1 || true
        else
            # Fallback
            supervisorctl stop all >/dev/null 2>&1 || true
            supervisorctl start string-server >/dev/null 2>&1 || true
        fi
    fi
    
    # Clean up any old sphere-flask-app entries from existing config (shouldn't be on compute nodes)
    if [ -f "$SUPERVISOR_CONFIG" ]; then
        if grep -q "\[program:sphere-flask-app\]" "$SUPERVISOR_CONFIG" 2>/dev/null; then
            print_status "Removing old sphere-flask-app entry from existing supervisor config..."
            # Remove the entire [program:sphere-flask-app] section
            sed -i '/^\[program:sphere-flask-app\]/,/^\[/ { /^\[program:sphere-flask-app\]/d; /^\[/!d; }' "$SUPERVISOR_CONFIG" 2>/dev/null || true
            # Alternative: remove lines between [program:sphere-flask-app] and next [program: or end of file
            awk '/^\[program:sphere-flask-app\]/{flag=1; next} /^\[program:/{flag=0} !flag' "$SUPERVISOR_CONFIG" > "$SUPERVISOR_CONFIG.tmp" && mv "$SUPERVISOR_CONFIG.tmp" "$SUPERVISOR_CONFIG" 2>/dev/null || true
        fi
    fi
    
    # Find the script's directory first
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Detect GPU capacity and write config file
    detect_gpu_capacity
    
    # Copy supervisor config file
    # SCRIPT_DIR is already set above
    print_status "Script directory: $SCRIPT_DIR"
    print_status "Current directory: $(pwd)"
    print_status "Looking for supervisord-watchers.conf..."
    
    # Try multiple locations in order of preference
    CONFIG_FILE=""
    if [ -f "$SCRIPT_DIR/supervisord-watchers.conf" ]; then
        CONFIG_FILE="$SCRIPT_DIR/supervisord-watchers.conf"
        print_status "Found at: $CONFIG_FILE (script directory)"
    elif [ -f "$SCRIPT_DIR/../supervisord-watchers.conf" ]; then
        CONFIG_FILE="$SCRIPT_DIR/../supervisord-watchers.conf"
        print_status "Found at: $CONFIG_FILE (parent of script directory)"
    elif [ -f "supervisord-watchers.conf" ]; then
        CONFIG_FILE="supervisord-watchers.conf"
        print_status "Found at: $CONFIG_FILE (current directory)"
    elif [ -f "src/supervisord-watchers.conf" ]; then
        CONFIG_FILE="src/supervisord-watchers.conf"
        print_status "Found at: $CONFIG_FILE (src/ subdirectory)"
    elif [ -f "$SCRIPT_DIR/../src/supervisord-watchers.conf" ]; then
        CONFIG_FILE="$SCRIPT_DIR/../src/supervisord-watchers.conf"
        print_status "Found at: $CONFIG_FILE (src/ relative to script)"
    else
        print_error "supervisord-watchers.conf not found!"
        print_error "Script directory: $SCRIPT_DIR"
        print_error "Current directory: $(pwd)"
        print_error "Searched locations:"
        print_error "  - $SCRIPT_DIR/supervisord-watchers.conf"
        print_error "  - $SCRIPT_DIR/../supervisord-watchers.conf"
        print_error "  - $(pwd)/supervisord-watchers.conf"
        print_error "  - $(pwd)/src/supervisord-watchers.conf"
        print_error "  - $SCRIPT_DIR/../src/supervisord-watchers.conf"
        exit 1
    fi
    
    print_status "Copying supervisor configuration from: $CONFIG_FILE"
    
    # Remove old/renamed supervisor config file if it exists (cleanup from rename)
    OLD_SUPERVISOR_CONFIG="/etc/supervisor/conf.d/supervisord-watchers.conf"
    if [ -f "$OLD_SUPERVISOR_CONFIG" ] && [ "$OLD_SUPERVISOR_CONFIG" != "$SUPERVISOR_CONFIG" ]; then
        print_status "Removing old supervisor config file: $OLD_SUPERVISOR_CONFIG"
        rm -f "$OLD_SUPERVISOR_CONFIG"
    fi
    
    cp "$CONFIG_FILE" "$SUPERVISOR_CONFIG"
    
    # Create log files explicitly
    touch /var/log/featrix/api_server.log
    # Old file-based worker logs - no longer needed (we use Celery now)
    # These were for: worker_create_sd, worker_train_es, worker_train_knn,
    # worker_run_clustering, worker_train_single_predictor, worker_prediction_persistence
    # and the old celery-predictions worker (consolidated into celery-cpu_worker)
    touch /var/log/featrix/celery_cpu_worker.log
    touch /var/log/featrix/celery_gpu_training.log
    touch /var/log/featrix/auto_upgrade_monitor.log
    touch /var/log/featrix/featrix_watchdog.log
    touch /var/log/featrix/gc_cleanup.log
    touch /var/log/featrix/system_monitor.log
    chmod 644 /var/log/featrix/*.log
    
    # CRITICAL: Enable supervisor for auto-start on boot (must succeed)
    print_status "Enabling supervisor service for auto-start..."
    if ! systemctl enable supervisor; then
        print_error "Failed to enable supervisor service - this is critical!"
        exit 1
    fi
    
    # Check if supervisor is already running
    if systemctl is-active --quiet supervisor && supervisorctl status >/dev/null 2>&1; then
        print_status "Supervisor is already running, reloading configuration..."
        # Just reload the config - no restart needed
        if ! supervisorctl reread 2>&1; then
            print_error "Failed to reread supervisor config"
            exit 1
        fi
        if ! supervisorctl update >/dev/null 2>&1; then
            print_error "Failed to update supervisor config"
            exit 1
        fi
        print_status "✅ Supervisor configuration reloaded"
    else
        # Supervisor not running - start it
        print_status "Starting supervisor service..."
        kill_uvicorn_processes >/dev/null 2>&1 || true
        
        # Ensure supervisor is stopped via systemctl first (in case it's in a bad state)
        systemctl stop supervisor 2>/dev/null || true
        sleep 1
        
        # Kill any remaining supervisord processes that might be holding the port
        pkill -9 supervisord 2>/dev/null || true
        sleep 1
        
        # Clean up supervisor sockets to ensure clean start
        rm -f /var/run/supervisor.sock /var/run/supervisor/* /tmp/supervisor.sock /tmp/supervisord.sock 2>/dev/null || true
        mkdir -p /var/run/supervisor 2>/dev/null || true
        chmod 755 /var/run/supervisor 2>/dev/null || true
        
        # Check and kill anything using supervisor's HTTP port (9001)
        SUPERVISOR_PORT="9001"
        if [ -f /etc/supervisor/supervisord.conf ]; then
            FOUND_PORT=$(grep -A 10 "\[inet_http_server\]" /etc/supervisor/supervisord.conf 2>/dev/null | grep -E "^port\s*=" | head -1 | awk -F'=' '{print $2}' | tr -d ' ' || true)
            if [ -n "$FOUND_PORT" ] && [ "$FOUND_PORT" != "" ]; then
                SUPERVISOR_PORT="$FOUND_PORT"
            fi
        fi
        
        # Kill processes using the supervisor port
        if command -v lsof >/dev/null 2>&1; then
            PIDS=$(lsof -ti :$SUPERVISOR_PORT 2>/dev/null || true)
            if [ -n "$PIDS" ]; then
                echo "$PIDS" | while read pid; do
                    if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                        kill -9 "$pid" 2>/dev/null || true
                    fi
                done
                sleep 0.5
            fi
        elif command -v ss >/dev/null 2>&1; then
            PIDS=$(ss -tlnp 2>/dev/null | grep ":$SUPERVISOR_PORT " | grep -oP 'pid=\K\d+' || true)
            if [ -n "$PIDS" ]; then
                echo "$PIDS" | while read pid; do
                    if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                        kill -9 "$pid" 2>/dev/null || true
                    fi
                done
                sleep 0.5
            fi
        fi
        
        # Start supervisor with timeout to prevent hanging
        if ! timeout 10 systemctl start supervisor; then
            print_error "Failed to start supervisor (timeout or error)"
            # Check if it actually started despite the timeout
            if ! systemctl is-active --quiet supervisor; then
                exit 1
            fi
        fi
        sleep 2
        
        # Wait for supervisor to be ready (with overall timeout)
        for i in {1..20}; do
            if supervisorctl status >/dev/null 2>&1; then
                break
            fi
            if [ $i -eq 20 ]; then
                print_error "Supervisor not responding after 10 seconds"
                exit 1
            fi
            sleep 0.5
        done
        
        # Update supervisor configuration
        if ! supervisorctl reread 2>&1; then
            print_error "Failed to reread supervisor config"
            exit 1
        fi
        
        if ! supervisorctl update >/dev/null 2>&1; then
            print_error "Failed to update supervisor config"
            exit 1
        fi
        print_status "✅ Supervisor started and configured"
    fi
}

# Function to test setup
test_setup() {
    print_section "Testing setup..."
    
    # Test virtual environment and imports
    source "$VENV_DIR/bin/activate"
    cd "$TARGET_DIR"
    
    python -c "
import sys
sys.path.insert(0, '/sphere/app')
sys.path.insert(0, '/sphere/app/lib')
try:
    import fastapi, uvicorn, pydantic_settings, api, jsontables
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" || { print_error "Setup test failed"; exit 1; }
    
    deactivate
    print_status "Setup test passed"
}

# Function to start services
start_services() {
    print_section "Starting services..."
    
    # CRITICAL: Ensure supervisor is enabled for auto-start on boot
    print_status "Ensuring supervisor is enabled for auto-start..."
    if ! systemctl is-enabled supervisor >/dev/null 2>&1; then
        print_status "Enabling supervisor service..."
        systemctl enable supervisor || {
            print_error "Failed to enable supervisor service"
            return 1
        }
    fi
    
    # Note: setup_supervisor() already handled supervisor restart and config update
    # We only need to ensure supervisor is responding (should already be from setup_supervisor)
    if ! supervisorctl status >/dev/null 2>&1; then
        print_warning "Supervisor not responding, restarting..."
        systemctl restart supervisor || {
            print_error "Failed to restart supervisor"
            return 1
        }
        sleep 5
        
        # Wait for supervisor to be ready (faster polling)
        for i in {1..10}; do
            if supervisorctl status >/dev/null 2>&1; then
                break
            fi
            if [ $i -eq 10 ]; then
                print_error "Supervisor not responding after restart"
                return 1
            fi
            sleep 0.5  # Reduced from 1s to 0.5s
        done
    fi
    
    # Ensure supervisor is running (not just enabled)
    if ! systemctl is-active --quiet supervisor; then
        print_status "Starting supervisor service..."
        systemctl start supervisor || {
            print_error "Failed to start supervisor service"
            return 1
        }
        sleep 3
    fi
    
    # Start all services EXCEPT string-server (never restart string-server during upgrade)
    # If string-server is already running, leave it alone
    print_status "Starting supervisor-managed services (excluding string-server)..."
    SERVICES_TO_START=$(get_services_except_string_server)
    if [ -n "$SERVICES_TO_START" ]; then
        if ! supervisorctl start $SERVICES_TO_START; then
            print_error "Failed to start services"
            supervisorctl status
            return 1
        fi
    else
        # Fallback: start all but make sure we don't restart string-server
        if ! supervisorctl start all; then
            print_error "Failed to start all services"
            supervisorctl status
            return 1
        fi
        # If string-server was stopped, start it (but don't restart if already running)
        supervisorctl start string-server 2>/dev/null || true
    fi
    
    # Restart Celery workers to pick up code changes (with aggressive cleanup)
    print_status "Restarting Celery workers to load new code..."
    
    # Use the dedicated function for cleanup
    kill_all_celery_workers || true
    
    # Also kill all old Sphere processes (including old queue watchers)
    kill_all_old_sphere_processes || true
    
    # Step 3: Start fresh workers (with retries to ensure they actually start)
    print_status "Starting Celery workers..."
    
    # Ensure workers are stopped first (in case they're in a weird state)
    supervisorctl stop featrix-cpu_worker featrix-gpu_training >/dev/null 2>&1 || true
    sleep 2
    
    # Try to start workers with retries
    MAX_RETRIES=3
    RETRY_COUNT=0
    WORKERS_STARTED=false
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if supervisorctl start featrix-cpu_worker featrix-gpu_training >/dev/null 2>&1; then
            WORKERS_STARTED=true
            break
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        print_warning "   Attempt $RETRY_COUNT failed, retrying in 2 seconds..."
        sleep 2
    done
    
    if [ "$WORKERS_STARTED" = false ]; then
        print_error "Failed to start Celery workers after $MAX_RETRIES attempts. Check logs."
        supervisorctl status featrix-cpu_worker featrix-gpu_training
        # Don't return 1 - continue with upgrade even if workers fail to start
        # They should auto-restart via supervisor autorestart=true
        print_warning "Continuing upgrade - workers should auto-restart via supervisor"
    else
        print_status "✅ Celery workers started successfully"
    fi
    
    # Wait for services to start (some services like string-server take time)
    print_status "Waiting for services to initialize..."
    sleep 5
    
    # CRITICAL: Verify all services are actually running
    # Retry checking a few times to allow services time to start
    print_status "Verifying all services are running..."
    MAX_RETRIES=3
    RETRY_DELAY=5
    
    for retry in $(seq 1 $MAX_RETRIES); do
        FAILED_SERVICES=()
        STARTING_SERVICES=()
        STATUS_OUTPUT=$(supervisorctl status 2>&1)
        
        # Check each service
        while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                SERVICE_NAME=$(echo "$line" | awk '{print $1}')
                STATUS=$(echo "$line" | awk '{print $2}')
                
                # Skip header lines
                if [[ "$SERVICE_NAME" == "supervisorctl" ]] || [[ "$SERVICE_NAME" == "unix://"* ]]; then
                    continue
                fi
                
                # Skip string-server from verification - we don't manage it during upgrade
                if [[ "$SERVICE_NAME" == "string-server" ]]; then
                    continue
                fi
                
                # STARTING is OK - service is in the process of starting
                if [[ "$STATUS" == "STARTING" ]]; then
                    STARTING_SERVICES+=("$SERVICE_NAME")
                # Only fail on actual error states
                elif [[ "$STATUS" != "RUNNING" ]]; then
                    # Error states: FATAL, STOPPED, EXITED, BACKOFF, etc.
                    FAILED_SERVICES+=("$SERVICE_NAME: $STATUS")
                fi
            fi
        done <<< "$STATUS_OUTPUT"
        
        # If we have starting services and this isn't the last retry, wait and check again
        if [ ${#STARTING_SERVICES[@]} -gt 0 ] && [ $retry -lt $MAX_RETRIES ]; then
            print_status "   ${#STARTING_SERVICES[@]} service(s) still starting, waiting ${RETRY_DELAY}s (retry $retry/$MAX_RETRIES)..."
            for service in "${STARTING_SERVICES[@]}"; do
                print_status "      - $service: STARTING"
            done
            sleep $RETRY_DELAY
            continue
        fi
        
        # If we have failed services, report them
        if [ ${#FAILED_SERVICES[@]} -gt 0 ]; then
            print_error "⚠️  Some services failed to start:"
            for service in "${FAILED_SERVICES[@]}"; do
                print_error "   - $service"
            done
            if [ ${#STARTING_SERVICES[@]} -gt 0 ]; then
                print_warning "   Services still starting (may need more time):"
                for service in "${STARTING_SERVICES[@]}"; do
                    print_warning "      - $service: STARTING"
                done
            fi
            print_error ""
            print_error "Full status:"
            supervisorctl status
            return 1
        fi
        
        # All services are either RUNNING or STARTING (and we've waited)
        if [ ${#STARTING_SERVICES[@]} -gt 0 ]; then
            print_warning "   Some services still starting (may need more time):"
            for service in "${STARTING_SERVICES[@]}"; do
                print_warning "      - $service: STARTING"
            done
            print_warning "   This is usually OK - they should finish starting soon"
        fi
        
        # Success - all services are RUNNING or we've given up waiting on STARTING
        break
    done
    
    print_status "✅ All services started successfully"
    supervisorctl status
}

# Function to get list of all services except string-server (which should never be restarted)
get_services_except_string_server() {
    # Get all service names from supervisor, excluding string-server
    supervisorctl status 2>/dev/null | awk '{print $1}' | grep -v "^string-server$" | grep -v "^supervisorctl$" | grep -v "^unix://" | grep -v "^$" | tr '\n' ' ' || echo ""
}

# Function to stop all services
stop_all_services() {
    print_section "Stopping all services..."
    
    # FIRST: Aggressively kill all Celery workers BEFORE anything else
    # This prevents orphaned workers from blocking supervisor-managed workers
    kill_all_celery_workers || true
    
    # SECOND: Kill all old orphaned processes BEFORE stopping supervisor
    # This ensures we kill processes from old supervisor instances
    kill_all_old_sphere_processes || true
    
    # Stop all supervisor services EXCEPT string-server (never restart string-server during upgrade)
    print_status "Stopping supervisor services (excluding string-server)..."
    SERVICES_TO_STOP=$(get_services_except_string_server)
    if [ -n "$SERVICES_TO_STOP" ]; then
        timeout 10 supervisorctl stop $SERVICES_TO_STOP 2>/dev/null || true
    else
        # Fallback: stop all but explicitly exclude string-server
        timeout 10 supervisorctl stop all 2>/dev/null || true
        # Make sure string-server is still running if it was running
        supervisorctl start string-server 2>/dev/null || true
    fi
    
    # Don't stop supervisor itself - just reload config later
    # print_status "Stopping supervisor..."
    # systemctl stop supervisor 2>/dev/null || true
    # sleep 2
    
    # Kill any remaining processes (with timeout to prevent hanging)
    print_status "Cleaning up any remaining processes..."
    # Call the function directly - it already has internal timeouts
    kill_uvicorn_processes || true
    
    # Kill Celery workers again after stopping supervisor (in case more were orphaned)
    kill_all_celery_workers || true
    
    # Kill old processes again after stopping supervisor (in case more were orphaned)
    kill_all_old_sphere_processes || true
    
    print_status "✅ All services stopped (supervisor still running)"
}

# Function to rotate log files
rotate_logs() {
    print_section "Rotating log files..."
    
    LOG_DIR="/var/log/featrix"
    
    if [ ! -d "$LOG_DIR" ]; then
        print_warning "Log directory $LOG_DIR does not exist, skipping rotation"
        return
    fi
    
    # Rotate all .log files in the log directory
    print_status "Rotating log files in $LOG_DIR..."
    for logfile in "$LOG_DIR"/*.log; do
        if [ -f "$logfile" ]; then
            # Get base name without extension
            basename=$(basename "$logfile" .log)
            # Create rotated filename with timestamp
            rotated="${LOG_DIR}/${basename}.log.$(date +%Y%m%d_%H%M%S)"
            print_status "   Rotating: $(basename $logfile) -> $(basename $rotated)"
            mv "$logfile" "$rotated" 2>/dev/null || true
        fi
    done
    
    print_status "✅ Log rotation complete"
}

# Function to check for tracebacks in logs
# Since logs are rotated before service startup, all .log files are fresh
check_for_tracebacks() {
    print_section "Checking for tracebacks in logs..."
    
    LOG_DIR="/var/log/featrix"
    
    if [ ! -d "$LOG_DIR" ]; then
        print_warning "Log directory $LOG_DIR does not exist"
        return 0
    fi
    
    local found_tracebacks=false
    local traceback_count=0
    local temp_output=$(mktemp)
    
    # Check all .log files (they're all fresh after rotation)
    for logfile in "$LOG_DIR"/*.log; do
        if [ ! -f "$logfile" ]; then
            continue
        fi
        
        # Look for tracebacks in this file
        local traceback_lines=$(grep -n "Traceback (most recent call last):" "$logfile" 2>/dev/null || true)
        
        if [ -n "$traceback_lines" ]; then
            found_tracebacks=true
            # Count tracebacks and collect output
            while IFS=: read -r line_num rest; do
                traceback_count=$((traceback_count + 1))
                # Extract traceback block (next 30 lines after "Traceback")
                local traceback_block=$(sed -n "${line_num},$((line_num + 30))p" "$logfile" 2>/dev/null || true)
                
                if [ -n "$traceback_block" ]; then
                    echo "❌ Found traceback in $(basename $logfile) at line $line_num:" >> "$temp_output"
                    echo "$traceback_block" | head -25 | sed 's/^/   /' >> "$temp_output"
                    echo "" >> "$temp_output"
                fi
            done <<< "$traceback_lines"
        fi
    done
    
    # Display collected tracebacks
    if [ -s "$temp_output" ]; then
        cat "$temp_output"
    fi
    rm -f "$temp_output"
    
    if [ "$found_tracebacks" = true ] && [ "$traceback_count" -gt 0 ]; then
        print_error "❌ Found $traceback_count traceback(s) in log file(s)"
        print_error "   This indicates errors occurred after service startup"
        print_error "   Check /var/log/featrix/*.log for full details"
        return 1
    else
        print_status "✅ No tracebacks found in logs"
        return 0
    fi
}

# Function to show final status
show_final_status() {
    print_section "Deployment Summary"
    
    # CRITICAL: Verify supervisor is enabled and running
    if ! systemctl is-enabled supervisor >/dev/null 2>&1; then
        print_error "⚠️  CRITICAL: Supervisor is not enabled for auto-start!"
        print_error "   Services will not start on boot!"
        systemctl enable supervisor || {
            print_error "   Failed to enable supervisor - manual intervention required"
        }
    fi
    
    if ! systemctl is-active --quiet supervisor; then
        print_error "⚠️  CRITICAL: Supervisor service is not running!"
        print_error "   Attempting to start..."
        systemctl start supervisor || {
            print_error "   Failed to start supervisor - manual intervention required"
            return 1
        }
        sleep 3
    fi
    
    # CRITICAL: Verify all services are actually running
    print_status "Verifying all services are running..."
    FAILED_SERVICES=()
    STATUS_OUTPUT=$(supervisorctl status 2>&1)
    
    if [ $? -ne 0 ]; then
        print_error "⚠️  CRITICAL: Cannot query supervisor status!"
        return 1
    fi
    
    # Check each service
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            SERVICE_NAME=$(echo "$line" | awk '{print $1}')
            STATUS=$(echo "$line" | awk '{print $2}')
            
            # Skip header lines
            if [[ "$SERVICE_NAME" == "supervisorctl" ]] || [[ "$SERVICE_NAME" == "unix://"* ]]; then
                continue
            fi
            
            # Skip string-server from verification - we don't manage it during upgrade
            if [[ "$SERVICE_NAME" == "string-server" ]]; then
                continue
            fi
            
            if [[ "$STATUS" != "RUNNING" ]]; then
                FAILED_SERVICES+=("$SERVICE_NAME: $STATUS")
            fi
        fi
    done <<< "$STATUS_OUTPUT"
    
    if [ ${#FAILED_SERVICES[@]} -gt 0 ]; then
        print_error "⚠️  CRITICAL: Some services are not running:"
        for service in "${FAILED_SERVICES[@]}"; do
            print_error "   - $service"
        done
        print_error ""
        print_error "Full status:"
        supervisorctl status
        print_error ""
        print_error "Attempting to start failed services (excluding string-server)..."
        SERVICES_TO_START=$(get_services_except_string_server)
        if [ -n "$SERVICES_TO_START" ]; then
            supervisorctl start $SERVICES_TO_START || true
        else
            supervisorctl start all || true
        fi
        sleep 2
        supervisorctl status
        return 1
    fi
    
    add_prefix ""
    add_prefix "${GREEN}🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
    add_prefix ""
    add_prefix "${BLUE}📋 System Status:${NC}"
    supervisorctl status | while read line; do add_prefix "${BLUE}   $line${NC}"; done
    add_prefix ""
    add_prefix "${BLUE}🌐 API: http://localhost:8000${NC}"
    add_prefix "${BLUE}🔧 Management:${NC}"
    add_prefix "   • Status: supervisorctl status"
    add_prefix "   • Logs: supervisorctl tail -f api_server"
    add_prefix "   • Restart: supervisorctl restart all"
    add_prefix "   • All logs: multitail /var/log/featrix/*.log"
    add_prefix ""
    add_prefix "${BLUE}🔄 This script is IDEMPOTENT:${NC}"
    add_prefix "   • Safe to run multiple times"
    add_prefix "   • Use: sudo ./churro-copy.sh"
    add_prefix "   • Quick restart: sudo ./churro-copy.sh --restart-only"
    add_prefix ""
}

# Function to send Slack notification about deployment
send_slack_notification() {
    local deployment_type="$1"  # "full" or "restart"
    
    # Check if /etc/.hook exists
    if [ ! -f "/etc/.hook" ]; then
        return 0  # Silent skip if no hook file
    fi
    
    # Read webhook URL from /etc/.hook
    SLACK_WEBHOOK_URL=$(cat /etc/.hook 2>/dev/null | head -1)
    if [ -z "$SLACK_WEBHOOK_URL" ]; then
        return 0  # Silent skip if empty
    fi
    
    # Get hostname
    local hostname=$(hostname)
    
    # Get version info - read from /sphere/VERSION after deployment
    local version="unknown"
    local git_hash="unknown"
    local git_branch="unknown"
    
    if [ -f "/sphere/VERSION" ]; then
        version=$(cat /sphere/VERSION 2>/dev/null || echo "unknown")
    fi
    
    # Git info from temp files (captured at script start before any cd)
    if [ -f "/tmp/SPHERE_GIT_HASH" ]; then
        git_hash=$(cat /tmp/SPHERE_GIT_HASH 2>/dev/null || echo "unknown")
    fi
    if [ -f "/tmp/SPHERE_GIT_BRANCH" ]; then
        git_branch=$(cat /tmp/SPHERE_GIT_BRANCH 2>/dev/null || echo "unknown")
    fi
    
    # Build Slack message
    local emoji="🚀"
    local action="deployed"
    if [ "$deployment_type" = "restart" ]; then
        emoji="🔄"
        action="restarted"
    fi
    
    local message="${emoji} *Featrix Sphere ${action} on ${hostname}*\n"
    message+="• Version: \`${version}\`\n"
    message+="• Git: \`${git_hash}\` (${git_branch})\n"
    message+="• Time: $(date '+%Y-%m-%d %H:%M:%S %Z')\n"
    message+="• Type: ${deployment_type} deployment"
    
    # Send Slack notification using Python with requests
    print_status "Sending Slack notification..."
    SLACK_EMOJI="$emoji" SLACK_ACTION="$action" python3 << 'EOF'
import requests
import json
from pathlib import Path

try:
    # Read webhook
    webhook = Path("/etc/.hook").read_text().strip() if Path("/etc/.hook").exists() else None
    if not webhook:
        print("[INFO] No /etc/.hook found, skipping Slack notification")
        exit(0)
    
    # Get version and git info
    version = Path("/sphere/VERSION").read_text().strip() if Path("/sphere/VERSION").exists() else "unknown"
    git_hash = Path("/tmp/SPHERE_GIT_HASH").read_text().strip() if Path("/tmp/SPHERE_GIT_HASH").exists() else "unknown"
    git_branch = Path("/tmp/SPHERE_GIT_BRANCH").read_text().strip() if Path("/tmp/SPHERE_GIT_BRANCH").exists() else "unknown"
    
    import socket
    from datetime import datetime
    import os
    hostname = socket.gethostname()
    
    # Build message
    emoji = os.environ.get("SLACK_EMOJI", "🚀")
    action = os.environ.get("SLACK_ACTION", "deployed")
    msg = f"{'─'*50}\n"
    msg += f"{emoji} *Featrix Sphere {action} on `{hostname}`*\n"
    msg += f"```\n"
    msg += f"Version    : {version}\n"
    msg += f"Git Commit : {git_hash[:8]}\n"
    msg += f"Branch     : {git_branch}\n"
    msg += f"Time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
    msg += f"```\n"
    
    # Get health check
    try:
        health = requests.get("http://localhost:8000/health", timeout=10).json()
        
        # Build health table
        msg += "\n*📊 System Health*\n"
        msg += f"```\n"
        
        # GPU
        if health.get("gpu", {}).get("available"):
            gpu = health["gpu"]
            msg += f"GPU Memory     : {gpu['total_free_gb']:.1f} GB free / {gpu.get('total_memory_gb', 0):.1f} GB total\n"
            msg += f"GPU Count      : {gpu['gpu_count']}\n"
        else:
            msg += f"GPU            : Not available\n"
        
        # Training capacity
        if "ready_for_training" in health:
            status = "✅ Ready" if health["ready_for_training"] else "⏸️ Busy"
            msg += f"Training       : {status}\n"
        
        # Celery
        if health.get("celery"):
            c = health["celery"]
            msg += f"Workers        : {c['total_workers']} total, {c['busy_workers']} busy\n"
        
        # Jobs
        if health.get("jobs"):
            j = health["jobs"]
            tr = j.get("training_jobs", {})
            pr = j.get("prediction_jobs", {})
            msg += f"Training Jobs  : {tr.get('running',0)} running, {tr.get('queued',0)} queued\n"
            msg += f"Prediction Jobs: {pr.get('running',0)} running, {pr.get('queued',0)} queued\n"
        
        # Disk
        if health.get("system", {}).get("disk", {}).get("sphere"):
            d = health["system"]["disk"]["sphere"]
            status = "✅" if d["usage_pct"] < 80 else "⚠️"
            msg += f"Disk /sphere   : {d['free_gb']:.0f} GB free ({100-d['usage_pct']:.0f}% available) {status}\n"
        
        # Uptime
        if health.get("uptime"):
            u = health["uptime"]["api_seconds"]
            if u < 60:
                msg += f"API Uptime     : {int(u)}s\n"
            elif u < 3600:
                msg += f"API Uptime     : {int(u//60)}m\n"
            else:
                h = int(u // 3600)
                m = int((u % 3600) // 60)
                msg += f"API Uptime     : {h}h {m}m\n"
        
        msg += f"```\n"
            
    except Exception as e:
        msg += f"\n⚠️ _Health check unavailable: {e}_\n"
    
    msg += f"{'─'*50}\n"
    
    # Send to Slack
    response = requests.post(webhook, json={"text": msg}, timeout=10)
    if response.text == "ok":
        print("[INFO] ✅ Slack notification sent successfully")
    else:
        print(f"[WARN] Slack response: {response.text}")
        
except Exception as e:
    print(f"[ERROR] Slack notification failed: {e}")
EOF
}

# Function to display version info
show_version_info() {
    local context="${1:-Deployment}"
    print_section "$context Version Info"
    
    # Always show current time prominently
    add_prefix "🕐 Current Time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    add_prefix ""
    
    # Try multiple locations to find version info
    # PRIORITY: Check deployed version first, then git repo
    local version_found=false
    
    # First try: /sphere/VERSION and /sphere/app (deployed version - most important)
    if [ -f "/sphere/VERSION" ] && [ -f "/sphere/app/version.py" ]; then
        add_prefix "📦 Sphere Version (from deployed /sphere/app):"
        cd /sphere/app
        python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from version import get_version
    v = get_version()
    print(f'   Version: {v}')
    print(f'   Git Hash: {v.git_hash[:8] if v.git_hash else \"unknown\"}')
    print(f'   Git Branch: {v.git_branch or \"unknown\"}')
    print(f'   Is Dirty: {v.is_dirty}')
    print(f'   Git Date: {v.git_date or \"unknown\"}')
except Exception as e:
    # Fallback to just reading VERSION file
    try:
        with open('/sphere/VERSION', 'r') as f:
            version = f.read().strip()
        print(f'   Version: {version}')
        print(f'   Git Hash: unknown (from VERSION file)')
    except:
        print(f'   Error getting version: {e}')
" 2>/dev/null | while read line; do add_prefix "$line"; done && version_found=true
    fi
    
    # Second try: current working directory (where script was invoked)
    if [ "$version_found" = false ] && [ -f "src/version.py" ] && [ -d ".git" ]; then
        add_prefix "📦 Sphere Version (from current directory):"
        python3 -c "
import sys
sys.path.append('src')
try:
    from version import get_version
    v = get_version()
    print(f'   Version: {v}')
    print(f'   Git Hash: {v.git_hash[:8] if v.git_hash else \"unknown\"}')
    print(f'   Git Branch: {v.git_branch or \"unknown\"}')
    print(f'   Is Dirty: {v.is_dirty}')
    print(f'   Git Date: {v.git_date or \"unknown\"}')
except Exception as e:
    print(f'   Error getting version: {e}')
" 2>/dev/null | while read line; do add_prefix "$line"; done && version_found=true
    fi
    
    # Third try: /home/mitch/sphere (git repo - least important for deployed version)
    if [ "$version_found" = false ] && [ -f "/home/mitch/sphere/src/version.py" ] && [ -d "/home/mitch/sphere/.git" ]; then
        add_prefix "📦 Sphere Version (from /home/mitch/sphere git repo):"
        cd /home/mitch/sphere
        python3 -c "
import sys
sys.path.append('src')
try:
    from version import get_version
    v = get_version()
    print(f'   Version: {v}')
    print(f'   Git Hash: {v.git_hash[:8] if v.git_hash else \"unknown\"}')
    print(f'   Git Branch: {v.git_branch or \"unknown\"}')
    print(f'   Is Dirty: {v.is_dirty}')
    print(f'   Git Date: {v.git_date or \"unknown\"}')
except Exception as e:
    print(f'   Error getting version: {e}')
" 2>/dev/null | while read line; do add_prefix "$line"; done && version_found=true
    fi
    
    # Third try: VERSION file only (fallback)
    if [ "$version_found" = false ]; then
        add_prefix "📦 Basic Version Info:"
        
        # Try to find VERSION file
        local version_file=""
        for loc in "VERSION" "/home/mitch/sphere/VERSION" "src/../VERSION"; do
            if [ -f "$loc" ]; then
                version_file="$loc"
                break
            fi
        done
        
        if [ -n "$version_file" ]; then
            add_prefix "   Version: $(cat "$version_file" 2>/dev/null || echo 'unknown')"
        else
            add_prefix "   Version: unknown (no VERSION file found)"
        fi
        
        # Try basic git info from any available location
        local git_found=false
        for git_dir in ".git" "/home/mitch/sphere/.git"; do
            if [ -d "$git_dir" ]; then
                local repo_dir=$(dirname "$git_dir")
                cd "$repo_dir"
                add_prefix "   Git Hash: $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
                add_prefix "   Git Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
                add_prefix "   Git Date: $(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M:%S' 2>/dev/null || echo 'unknown')"
                git_found=true
                break
            fi
        done
        
        if [ "$git_found" = false ]; then
            add_prefix "   Git Info: not available (no git repo found)"
        fi
    fi
    add_prefix ""
}

# Main execution flow
main() {
    # CRITICAL: Capture source directory IMMEDIATELY before any operations
    # This is where the package files are (extracted tarball or git repo)
    SOURCE_DIR="$(pwd)"
    print_status "Source directory (package location): $SOURCE_DIR"
    print_status "Target directory (deployment location): $TARGET_DIR"
    
    # Clean __pycache__ from the source repo BEFORE copying anything
    print_status "Cleaning bytecode from source repository..."
    find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name '*.pyc' -delete 2>/dev/null || true
    find . -type f -name '*.pyo' -delete 2>/dev/null || true
    
    # Capture git info early (before any directory changes)
    if [ -d ".git" ]; then
        git rev-parse --short HEAD > /tmp/SPHERE_GIT_HASH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_HASH
        git rev-parse --abbrev-ref HEAD > /tmp/SPHERE_GIT_BRANCH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_BRANCH
    else
        # No git repo - try to read hash from package VERSION_HASH file
        if [ -f "VERSION_HASH" ]; then
            cp VERSION_HASH /tmp/SPHERE_GIT_HASH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_HASH
        elif [ -f "/sphere/VERSION_HASH" ]; then
            cp /sphere/VERSION_HASH /tmp/SPHERE_GIT_HASH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_HASH
    else
        echo "unknown" > /tmp/SPHERE_GIT_HASH
        fi
        
        # Try to read branch from package VERSION_BRANCH file
        if [ -f "VERSION_BRANCH" ]; then
            cp VERSION_BRANCH /tmp/SPHERE_GIT_BRANCH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_BRANCH
        elif [ -f "/sphere/VERSION_BRANCH" ]; then
            cp /sphere/VERSION_BRANCH /tmp/SPHERE_GIT_BRANCH 2>/dev/null || echo "unknown" > /tmp/SPHERE_GIT_BRANCH
        else
        echo "unknown" > /tmp/SPHERE_GIT_BRANCH
        fi
    fi
    
    # Show version info before deployment
    show_version_info "Pre-Deployment"
    
    # Create upgrade flag to distinguish from crashes
    echo "Planned deployment started at $(date)" > /tmp/UPGRADE_SPHERE
    echo "Deployment triggered by: $0" >> /tmp/UPGRADE_SPHERE
    echo "Args: $@" >> /tmp/UPGRADE_SPHERE
    echo "Restart only: $RESTART_ONLY" >> /tmp/UPGRADE_SPHERE
    
    # Check for git changes first (unless in restart-only mode)
    if [ "$RESTART_ONLY" = false ]; then
        check_git_changes
    fi
    
    if [ "$RESTART_ONLY" = true ]; then
        add_prefix "${GREEN}🔄 RESTART-ONLY MODE STARTED${NC}"
        print_section "Restart-only mode..."
        # Even in restart mode, ensure critical directories exist
        setup_directories
        clean_python_cache
        
        # CRITICAL: Set up trap to ensure services restart even if restart fails
        # This prevents the box from being left in a broken state with all services stopped
        SERVICES_STOPPED=false
        trap 'if [ "$SERVICES_STOPPED" = true ]; then print_error "⚠️  Restart failed - attempting to restart services..."; start_services || true; fi' EXIT ERR
        
        stop_all_services || { print_warning "Some services may not have stopped cleanly"; }
        SERVICES_STOPPED=true  # Mark that services are stopped - trap will restart them on failure
        rotate_logs
        setup_supervisor
        start_services
        SERVICES_STOPPED=false  # Services are back up - clear the flag
        
        # Wait for services to initialize, then check for tracebacks
        sleep 5
        
        # Check for tracebacks in logs (all logs are fresh after rotation)
        if ! check_for_tracebacks; then
            print_warning "⚠️  Tracebacks detected in logs - services may have errors"
            print_warning "   Check /var/log/featrix/*.log for details"
        fi
        
        show_final_status
        send_slack_notification "restart"
        show_version_info "Post-Restart"
        
        # Clear the trap - restart succeeded, services are running
        trap - EXIT ERR
        SERVICES_STOPPED=false
        
        add_prefix "${GREEN}✅ RESTART-ONLY COMPLETED${NC}"
        return
    fi
    
    # Full deployment
    print_section "Starting full deployment process..."
    
    install_packages || { print_error "Package installation failed"; exit 1; }
    setup_directories || { print_error "Directory setup failed"; exit 1; }
    copy_application_files || { print_error "File copying failed"; exit 1; }
    clean_python_cache || { print_error "Cache cleanup failed"; exit 1; }
    setup_virtualenv || { print_error "Virtual environment setup failed"; exit 1; }
    clean_python_cache || { print_error "Cache cleanup failed"; exit 1; }
    test_setup || { print_error "Setup test failed"; exit 1; }
    
    # CRITICAL: Set up trap to ensure services restart even if upgrade fails
    # This prevents the box from being left in a broken state with all services stopped
    SERVICES_STOPPED=false
    trap 'if [ "$SERVICES_STOPPED" = true ]; then print_error "⚠️  Upgrade failed - attempting to restart services..."; start_services || true; fi' EXIT ERR
    
    # Stop services, rotate logs, then restart
    stop_all_services || { print_warning "Some services may not have stopped cleanly"; }
    SERVICES_STOPPED=true  # Mark that services are stopped - trap will restart them on failure
    rotate_logs
    setup_supervisor || { print_error "Supervisor setup failed"; exit 1; }
    start_services || { print_error "Service startup failed"; exit 1; }
    SERVICES_STOPPED=false  # Services are back up - clear the flag
    
    # Wait for services to initialize, then check for tracebacks
    print_status "Waiting 30 seconds for services to initialize..."
    sleep 30
    
    # Check for tracebacks in logs (all logs are fresh after rotation)
    if ! check_for_tracebacks; then
        print_warning "⚠️  Tracebacks detected in logs - services may have errors"
        print_warning "   Check /var/log/featrix/*.log for details"
    fi
    
    show_final_status || { print_error "Final status check failed"; exit 1; }
    
    # Clear the trap - deployment succeeded, services are running
    trap - EXIT ERR
    SERVICES_STOPPED=false
    
    # Update commit hash tracker after successful deployment
    update_commit_tracker
    
    # Send Slack notification
    send_slack_notification "full"
    
    # Show version info after deployment
    show_version_info "Post-Deployment"
    
    # Log final completion timestamp
    add_prefix "${GREEN}✅ FULL DEPLOYMENT COMPLETED${NC}"
}

main "$@"


