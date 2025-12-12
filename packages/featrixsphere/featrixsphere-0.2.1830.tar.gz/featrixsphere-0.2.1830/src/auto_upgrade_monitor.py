#!/sphere/.venv/bin/python3
"""
Auto Upgrade Monitor for Churro

Monitors for firmware updates from bits.featrix.com and automatically installs
when no training is running. Checks every 60 minutes or on SIGUSR1 signal.
"""

import os
import sys
import time
import signal
import hashlib
import logging
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import URLError

# Ensure we're using the venv Python if available
# Try python3 first (more common), fall back to python
VENV_PYTHON = Path("/sphere/.venv/bin/python3")
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path("/sphere/.venv/bin/python")

if VENV_PYTHON.exists() and sys.executable != str(VENV_PYTHON):
    # If venv Python exists and we're not using it, re-exec with venv Python
    # Do this before any logging setup
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

# Configure logging FIRST before any other imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Log startup IMMEDIATELY
logger.info("=" * 80)
logger.info(f"🚀 AUTO UPGRADE MONITOR STARTING - {datetime.now().isoformat()}")
logger.info("=" * 80)
logger.info("⚠️  AUTO-UPGRADES ARE DISABLED BY DEFAULT")
logger.info("   Create /DEV file to enable automatic upgrades")
logger.info("=" * 80)
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python path: {sys.path}")
logger.info("=" * 80)

# Verify we're using venv Python
if VENV_PYTHON.exists():
    if sys.executable == str(VENV_PYTHON):
        logger.info(f"✅ Using venv Python: {sys.executable}")
    else:
        logger.warning(f"⚠️  Not using venv Python! Current: {sys.executable}, Expected: {VENV_PYTHON}")

# Add /sphere/app to path for imports
sys.path.insert(0, "/sphere/app")
logger.info("Added /sphere/app to sys.path")

# Check for required dependencies BEFORE importing them
logger.info("Checking required dependencies...")
missing_deps = []

try:
    import pydantic_settings
    logger.info("✅ pydantic_settings found")
except ImportError as e:
    logger.error(f"❌ pydantic_settings NOT found: {e}")
    missing_deps.append("pydantic-settings>=2.0.0")

try:
    import redis
    logger.info("✅ redis found")
except ImportError as e:
    logger.error(f"❌ redis NOT found: {e}")
    missing_deps.append("redis>=5.0.0")

try:
    import psutil
    logger.info("✅ psutil found")
except ImportError as e:
    logger.warning(f"⚠️  psutil NOT found: {e}")
    logger.warning("   CPU/memory monitoring will be disabled")
    logger.warning("   Install with: pip3 install --break-system-packages psutil>=5.9.0")
    # Don't add to missing_deps - psutil is optional for auto-upgrade-monitor

if missing_deps:
    logger.error("=" * 80)
    logger.error("MISSING REQUIRED DEPENDENCIES - CANNOT START")
    logger.error("=" * 80)
    logger.error("Please install the following packages:")
    for dep in missing_deps:
        logger.error(f"  pip3 install --break-system-packages {dep}")
    logger.error("=" * 80)
    logger.error("Or run the deployment script to install all dependencies")
    logger.error("=" * 80)
    sys.exit(1)

logger.info("All dependencies found, importing modules...")

try:
    from lib.job_manager import JobStatus
    from lib.queue_manager import iterate_over_jobs_in_queue
    logger.info("✅ Successfully imported from featrix_queue")
except Exception as e:
    logger.error(f"❌ Failed to import from featrix_queue: {e}", exc_info=True)
    sys.exit(1)

# Configuration
FIRMWARE_SERVER = "https://bits.featrix.com/sphere-firmware"
INDEX_URL = f"{FIRMWARE_SERVER}/index.json"
INSTALL_SCRIPT = Path.home() / "featrix-install-package.sh"
VERSION_FILE = Path("/sphere/VERSION")
UPGRADE_LOCK_FILE = Path("/tmp/auto-upgrade.lock")
DEV_FLAG_FILE = Path("/DEV")  # Must exist for auto-upgrades to be enabled
CHECK_INTERVAL = 1800  # Check every 30 minutes (1800 seconds) - more frequent for faster upgrades

# Training job types to check (these are the job_type values in Redis)
TRAINING_JOB_TYPES = [
    "train_es",
    "train_knn",
    "run_clustering",
    "train_single_predictor",
    "create_structured_data"
]

# Global flag for SIGUSR1 signal
check_requested = False


def signal_handler(signum, frame):
    """Handle SIGUSR1 signal to trigger immediate check."""
    global check_requested
    logger.info(f"📡 Received SIGUSR1 signal - will check for updates immediately")
    check_requested = True


def is_training_running():
    """Check if any training jobs are currently running."""
    try:
        from lib.job_manager import get_redis_client, load_job
        client = get_redis_client()
        
        # Scan Redis for all job keys
        cursor = 0
        running_count = 0
        while True:
            cursor, keys = client.scan(cursor, match="job:*", count=100)
            for key in keys:
                try:
                    job_id = key.replace("job:", "")
                    job_data = load_job(job_id)
                    if not job_data:
                        continue
                    
                    job_type = job_data.get("type") or job_data.get("job_type", "unknown")
                    status = job_data.get("status")
                    
                    # Only check training job types
                    if job_type not in TRAINING_JOB_TYPES:
                        continue
                    
                    # Check if job is running
                    if status == JobStatus.RUNNING:
                        running_count += 1
                        logger.info(f"⏸️  Found running training job: {job_id} ({job_type})")
                except Exception as e:
                    logger.debug(f"Error checking job {key}: {e}")
                    continue
            
            if cursor == 0:
                break
        
        if running_count > 0:
            logger.info(f"⏸️  Total running training jobs: {running_count}")
            return True
        
        return False
        
    except Exception as e:
        logger.warning(f"⚠️  Could not check for running training jobs: {e}")
        # If we can't check, assume training might be running to be safe
        return False


def get_current_version() -> Optional[str]:
    """Get current installed version from VERSION file."""
    if VERSION_FILE.exists():
        try:
            return VERSION_FILE.read_text().strip()
        except Exception as e:
            logger.warning(f"⚠️  Error reading VERSION file: {e}")
            return None
    return None


def compare_versions(current: str, available: str) -> int:
    """
    Compare version strings (semantic versioning).
    Returns: -1 if current < available, 0 if equal, 1 if current > available
    """
    def version_tuple(v: str) -> tuple:
        """Convert version string to tuple for comparison."""
        parts = v.split('.')
        try:
            return tuple(int(p) for p in parts[:3])  # Major.minor.patch
        except ValueError:
            return (0, 0, 0)
    
    current_tuple = version_tuple(current)
    available_tuple = version_tuple(available)
    
    if current_tuple < available_tuple:
        return -1
    elif current_tuple > available_tuple:
        return 1
    else:
        return 0


def fetch_index() -> Optional[Dict[str, Any]]:
    """Fetch index.json from firmware server."""
    try:
        logger.info(f"📡 Fetching firmware index from {INDEX_URL}...")
        req = Request(INDEX_URL)
        req.add_header('User-Agent', 'Featrix-Auto-Upgrade-Monitor/1.0')
        
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            logger.info(f"✅ Fetched index with {data.get('total_files', 0)} files")
            return data
    except URLError as e:
        logger.error(f"❌ Failed to fetch index: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"❌ Failed to parse index.json: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error fetching index: {e}")
        return None


def find_newest_version(index: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find the newest version from index.json."""
    files = index.get('files', [])
    if not files:
        return None
    
    # Filter to only files (not directories) with valid versions
    versioned_files = []
    for file_info in files:
        if file_info.get('is_directory'):
            continue
        version = file_info.get('version')
        if version and version != 'unknown':
            versioned_files.append(file_info)
    
    if not versioned_files:
        logger.warning("⚠️  No files with version information found")
        return None
    
    # Sort by version (newest first)
    versioned_files.sort(
        key=lambda x: tuple(int(p) for p in x['version'].split('.')[:3]),
        reverse=True
    )
    
    return versioned_files[0]


def download_file(url: str, dest_path: Path, expected_hash: Optional[str] = None) -> bool:
    """Download a file and verify its hash if provided."""
    try:
        logger.info(f"📥 Downloading {url}...")
        req = Request(url)
        req.add_header('User-Agent', 'Featrix-Auto-Upgrade-Monitor/1.0')
        
        with urlopen(req, timeout=300) as response:
            data = response.read()
            
            # Verify hash if provided
            if expected_hash:
                calculated_hash = hashlib.sha256(data).hexdigest()
                if calculated_hash != expected_hash:
                    logger.error(f"❌ Hash mismatch! Expected {expected_hash[:16]}..., got {calculated_hash[:16]}...")
                    return False
                logger.info(f"✅ Hash verified: {expected_hash[:16]}...")
            
            # Write to destination
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, 'wb') as f:
                f.write(data)
            
            file_size_mb = len(data) / (1024 * 1024)
            logger.info(f"✅ Downloaded {file_size_mb:.2f} MB to {dest_path}")
            return True
            
    except Exception as e:
        logger.error(f"❌ Download failed: {e}")
        return False


def check_for_updates() -> Optional[Dict[str, Any]]:
    """
    Check if firmware updates are available.
    Returns dict with update info if available, None otherwise.
    """
    # Get current version
    current_version = get_current_version()
    if current_version:
        logger.info(f"📦 Current version: {current_version}")
    else:
        logger.warning("⚠️  Could not determine current version")
    
    # Fetch index
    index = fetch_index()
    if not index:
        logger.error("❌ Failed to fetch firmware index")
        return None
    
    # Find newest version
    newest = find_newest_version(index)
    if not newest:
        logger.error("❌ No valid firmware files found")
        return None
    
    newest_version = newest['version']
    newest_filename = newest['filename']
    newest_hash = newest.get('hash')
    newest_url = f"{FIRMWARE_SERVER}/{newest_filename}"
    
    logger.info(f"📊 Available versions:")
    logger.info(f"   Newest: {newest_version} ({newest_filename})")
    if newest_hash:
        logger.info(f"   Hash: {newest_hash[:16]}...")
    
    # Compare versions
    if not current_version:
        logger.warning("⚠️  Cannot compare versions - current version unknown")
        return {
            'version': newest_version,
            'filename': newest_filename,
            'hash': newest_hash,
            'url': newest_url
        }
    
    comparison = compare_versions(current_version, newest_version)
    if comparison < 0:
        logger.info(f"✅ Update available: {current_version} → {newest_version}")
        return {
            'version': newest_version,
            'filename': newest_filename,
            'hash': newest_hash,
            'url': newest_url
        }
    elif comparison == 0:
        logger.info(f"✅ Already on latest version: {current_version}")
        return None
    else:
        logger.warning(f"⚠️  Current version ({current_version}) is newer than available ({newest_version})")
        return None


def perform_update(update_info: Dict[str, Any]) -> bool:
    """Download and install the firmware update."""
    newest_filename = update_info['filename']
    newest_url = update_info['url']
    newest_hash = update_info.get('hash')
    
    # Create lock file
    try:
        UPGRADE_LOCK_FILE.touch()
        logger.info(f"Created upgrade lock file: {UPGRADE_LOCK_FILE}")
    except Exception as e:
        logger.error(f"Could not create lock file: {e}")
        return False
    
    try:
        # Download file
        download_dir = Path.home() / "featrix-updates"
        download_dir.mkdir(exist_ok=True)
        downloaded_file = download_dir / newest_filename
        
        if not download_file(newest_url, downloaded_file, newest_hash):
            logger.error("❌ Download failed")
            return False
        
        # Check if install script exists
        if not INSTALL_SCRIPT.exists():
            logger.error(f"❌ Install script not found: {INSTALL_SCRIPT}")
            logger.error("   Please ensure featrix-install-package.sh is in your home directory")
            return False
        
        # Call install script
        logger.info(f"🚀 Installing {newest_filename}...")
        logger.info(f"   Using install script: {INSTALL_SCRIPT}")
        
        result = subprocess.run(
            [str(INSTALL_SCRIPT), str(downloaded_file)],
            check=True,
            timeout=600  # 10 minute timeout
        )
        logger.info("✅ Installation completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Installation failed with exit code {e.returncode}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Installation timed out after 10 minutes")
        return False
    except Exception as e:
        logger.error(f"❌ Installation error: {e}")
        return False
    finally:
        # Remove lock file
        try:
            if UPGRADE_LOCK_FILE.exists():
                UPGRADE_LOCK_FILE.unlink()
                logger.info("Removed upgrade lock file")
        except Exception as e:
            logger.warning(f"Could not remove lock file: {e}")


def main():
    """Main monitoring loop."""
    # Install Featrix exception hook for better error tracking
    try:
        from lib.featrix_debug import install_featrix_excepthook
        install_featrix_excepthook()
    except Exception:
        pass  # Don't fail if debug module not available
    
    global check_requested
    
    # Set up SIGUSR1 signal handler
    signal.signal(signal.SIGUSR1, signal_handler)
    logger.info("✅ SIGUSR1 signal handler registered (send SIGUSR1 to trigger immediate check)")
    
    logger.info("=" * 80)
    logger.info("🚀 Auto Upgrade Monitor Starting Main Loop")
    logger.info("=" * 80)
    logger.info(f"Firmware server: {FIRMWARE_SERVER}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds ({CHECK_INTERVAL // 60} minutes)")
    logger.info(f"Lock file: {UPGRADE_LOCK_FILE}")
    logger.info(f"⚠️  DEV flag: {DEV_FLAG_FILE} (MUST EXIST for auto-upgrades to be enabled)")
    if DEV_FLAG_FILE.exists():
        logger.info(f"   ✅ DEV flag exists - auto-upgrades are ENABLED")
    else:
        logger.info(f"   ❌ DEV flag does NOT exist - auto-upgrades are DISABLED")
    logger.info(f"Pause flag: /sphere/NO_UPGRADE (create this file to pause auto-upgrades even if DEV flag exists)")
    logger.info(f"Force upgrade flag: /sphere/FORCE_UPGRADE (create this file to upgrade even if training is running)")
    logger.info(f"Training job types to check: {TRAINING_JOB_TYPES}")
    logger.info("=" * 80)
    
    check_count = 0
    last_heartbeat = time.time()
    last_check_time = time.time()
    HEARTBEAT_INTERVAL = 3600  # Log heartbeat every hour
    
    while True:
        try:
            check_count += 1
            current_time = time.time()
            
            # Log heartbeat periodically
            if current_time - last_heartbeat >= HEARTBEAT_INTERVAL:
                logger.info(f"💓 HEARTBEAT - Monitor alive, {check_count} checks performed")
                last_heartbeat = current_time
            
            # Check for DEV flag file - auto-upgrades are DISABLED by default
            if not DEV_FLAG_FILE.exists():
                logger.debug("DEV flag file does not exist - auto-upgrades are disabled (create /DEV to enable)")
                time.sleep(60)  # Sleep 60 seconds when disabled
                continue
            
            # Check for NO_UPGRADE flag file (overrides DEV flag)
            no_upgrade_flag = Path("/sphere/NO_UPGRADE")
            if no_upgrade_flag.exists():
                logger.debug("NO_UPGRADE flag exists, skipping check (create this file to pause auto-upgrades)")
                time.sleep(60)  # Sleep 60 seconds when paused
                continue
            
            # Check if upgrade lock exists (another process is upgrading)
            if UPGRADE_LOCK_FILE.exists():
                logger.debug("Upgrade lock file exists, skipping check")
                time.sleep(60)  # Sleep 60 seconds when locked
                continue
            
            # Determine if we should check now
            time_since_last_check = current_time - last_check_time
            should_check = check_requested or (time_since_last_check >= CHECK_INTERVAL)
            
            if should_check:
                if check_requested:
                    logger.info("📡 SIGUSR1 triggered - checking for updates immediately")
                    check_requested = False
                else:
                    logger.info(f"⏰ Scheduled check - {int(time_since_last_check / 60)} minutes since last check")
                
                last_check_time = current_time
                
                # Check for updates
                update_info = check_for_updates()
                if update_info:
                    # Check for force upgrade flag
                    force_upgrade_flag = Path("/sphere/FORCE_UPGRADE")
                    force_upgrade = force_upgrade_flag.exists()
                    
                    if force_upgrade:
                        logger.warning("⚠️  FORCE_UPGRADE flag detected - upgrading even if training is running")
                    
                    # Check if training is running
                    training_running = is_training_running() if not force_upgrade else False
                    if training_running:
                        logger.info("⏸️  Training is running, deferring update")
                        logger.info("   (Upgrade will proceed when training completes)")
                        logger.info("   (Or create /sphere/FORCE_UPGRADE to upgrade immediately)")
                    else:
                        logger.info("✅ No training running (or force upgrade enabled), proceeding with update")
                        success = perform_update(update_info)
                        if success:
                            logger.info("✅ Upgrade completed successfully - services will restart")
                            # Remove force upgrade flag after successful upgrade
                            if force_upgrade_flag.exists():
                                try:
                                    force_upgrade_flag.unlink()
                                    logger.info("✅ Removed FORCE_UPGRADE flag after successful upgrade")
                                except Exception as e:
                                    logger.warning(f"⚠️  Could not remove FORCE_UPGRADE flag: {e}")
                        else:
                            logger.error("❌ Upgrade failed - check logs for details")
                else:
                    logger.debug(f"Check #{check_count}: No updates available")
            
            # Sleep for 60 seconds, then check again
            # This allows SIGUSR1 to interrupt the sleep
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("=" * 80)
            logger.info("🛑 Received interrupt signal, shutting down...")
            logger.info(f"Total checks performed: {check_count}")
            logger.info("=" * 80)
            break
        except Exception as e:
            logger.error(f"❌ Error in main loop (check #{check_count}): {e}", exc_info=True)
            logger.error("Will retry after sleep interval...")
            time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"💥 FATAL ERROR - Auto upgrade monitor crashed: {e}")
        logger.error("=" * 80)
        logger.error("Stack trace:", exc_info=True)
        logger.error("=" * 80)
        sys.exit(1)
    finally:
        logger.info("=" * 80)
        logger.info(f"🏁 AUTO UPGRADE MONITOR SHUTDOWN - {datetime.now().isoformat()}")
        logger.info("=" * 80)
