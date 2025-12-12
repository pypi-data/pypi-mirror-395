#!/usr/bin/env python3
"""
Featrix Sphere Update Script

Checks for newer firmware versions on the server and installs them.
Runs standalone on compute nodes - no dependencies on common libs.

Usage:
    python3 featrix-update.py [--dry-run]
"""

import json
import os
import sys
import argparse
import subprocess
import hashlib
import tarfile
import tempfile
import shutil
import traceback
import socket
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import URLError

# Configuration
FIRMWARE_SERVER = "https://bits.featrix.com/sphere-firmware"
INDEX_URL = f"{FIRMWARE_SERVER}/index.json"
VERSION_FILE = Path("/sphere/VERSION")


def get_current_version() -> Optional[str]:
    """Get current installed version from VERSION file."""
    if VERSION_FILE.exists():
        try:
            return VERSION_FILE.read_text().strip()
        except Exception as e:
            print(f"⚠️  Error reading VERSION file: {e}")
            return None
    return None


def get_current_version_hash() -> Optional[str]:
    """Get current version hash - not available on nodes (no git)."""
    # Nodes don't have git, so we can't get version hash
    return None


def get_node_name() -> str:
    """Get node name from hostname, similar to featrix_watchdog.py."""
    try:
        hostname = socket.gethostname()
        hostname_lower = hostname.lower()
        # Map hostname to node name (e.g., "taco", "churro", "burrito")
        if 'taco' in hostname_lower:
            return 'taco'
        elif 'churro' in hostname_lower:
            return 'churro'
        elif 'burrito' in hostname_lower:
            return 'burrito'
        else:
            return hostname.split('.')[0]  # Use first part of hostname
    except Exception:
        return 'unknown'


def announce_to_sphere_api(version: str, version_hash: Optional[str] = None, status: str = "available") -> bool:
    """Announce node existence to sphere-api /compute-nodes/announce endpoint."""
    try:
        import urllib.request
        import urllib.parse
        
        node_name = get_node_name()
        
        # Get version hash if not provided
        if not version_hash:
            # Try to read from common locations
            for hash_path in [
                Path("/tmp/SPHERE_GIT_HASH"),
                Path("/sphere/VERSION_HASH"),
                Path("/sphere/app/VERSION_HASH"),
            ]:
                if hash_path.exists():
                    try:
                        version_hash = hash_path.read_text().strip()[:8]
                        break
                    except Exception:
                        pass
        
        payload = {
            "node_name": node_name,
            "status": status,
            "node_timestamp_now": datetime.now().isoformat(),
            "version": version,
            "version_hash": version_hash or "unknown"
        }
        
        # Try to detect external IP and port
        try:
            # Try to get external IP
            external_ip = None
            try:
                response = urlopen("https://api.ipify.org", timeout=5)
                external_ip = response.read().decode('utf-8').strip()
            except Exception:
                pass
            
            if external_ip:
                payload["external_ip"] = external_ip
            
            # Default port is 8000
            payload["port"] = 8000
        except Exception:
            pass  # IP/port detection is optional
        
        # Post to sphere-api
        api_url = "https://sphere-api.featrix.com/compute-nodes/announce"
        data = json.dumps(payload).encode('utf-8')
        
        # Create custom User-Agent with version and hostname
        user_agent = f"Featrix Firmware v{version} ({node_name})"
        req = Request(api_url, data=data, headers={
            'Content-Type': 'application/json',
            'User-Agent': user_agent
        })
        
        try:
            response = urlopen(req, timeout=10)
            if response.getcode() == 200:
                print(f"✅ Announced node '{node_name}' to sphere-api (status: {status}, version: {version})")
                return True
            else:
                print(f"⚠️  sphere-api announcement returned {response.getcode()}")
                return False
        except URLError as e:
            print(f"⚠️  Failed to announce to sphere-api: {e}")
            return False
    except Exception as e:
        print(f"⚠️  Error announcing to sphere-api: {e}")
        return False


def fetch_index() -> Optional[Dict[str, Any]]:
    """Fetch index.json from firmware server."""
    try:
        print(f"📡 Fetching firmware index from {INDEX_URL}...")
        req = Request(INDEX_URL)
        req.add_header('User-Agent', 'Featrix-Update-Script/1.0')
        
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"✅ Fetched index with {data.get('total_files', 0)} files")
            return data
    except URLError as e:
        print(f"❌ Failed to fetch index: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse index.json: {e}")
        return None
    except Exception as e:
        print(f"❌ Error fetching index: {e}")
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
        print("⚠️  No files with version information found")
        return None
    
    # Sort by version (newest first)
    versioned_files.sort(
        key=lambda x: tuple(int(p) for p in x['version'].split('.')[:3]),
        reverse=True
    )
    
    return versioned_files[0]


def install_package(package_file: Path, force: bool = False) -> bool:
    """
    Install a sphere-app package tarball.
    Self-contained - extracts package and runs node-install.sh from extracted directory.
    """
    
    print(f"\n🚀 Installing {package_file.name}...")
    
    # Create temp directory for extraction
    temp_dir = Path(tempfile.mkdtemp())
    try:
        print(f"   Extracting to temporary directory: {temp_dir}")
        
        # Extract tarball
        with tarfile.open(package_file, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        # Find the sphere-app directory in the extracted content
        extracted_dir = None
        if (temp_dir / "sphere-app").exists():
            extracted_dir = temp_dir / "sphere-app"
        elif temp_dir.exists():
            # Check if node-install.sh is directly in temp_dir
            if (temp_dir / "node-install.sh").exists() or (temp_dir / "src" / "node-install.sh").exists():
                extracted_dir = temp_dir
            else:
                # Look for any subdirectory with node-install.sh
                for item in temp_dir.iterdir():
                    if item.is_dir():
                        if (item / "node-install.sh").exists() or (item / "src" / "node-install.sh").exists():
                            extracted_dir = item
                            break
        
        if not extracted_dir:
            print("❌ Could not find sphere-app directory or node-install.sh in extracted package")
            return False
        
        print(f"   Package extracted successfully")
        
        # Show version info if available
        package_version = "unknown"
        package_hash = "unknown"
        if (extracted_dir / "VERSION").exists():
            package_version = (extracted_dir / "VERSION").read_text().strip()
        if (extracted_dir / "VERSION_HASH").exists():
            package_hash = (extracted_dir / "VERSION_HASH").read_text().strip()
        
        print(f"   Package version: {package_version}")
        print(f"   Package hash: {package_hash}")
        
        # Check if already deployed (unless forced)
        if not force:
            deployed_hash = None
            if Path("/sphere/app/VERSION_HASH").exists():
                deployed_hash = Path("/sphere/app/VERSION_HASH").read_text().strip()
            
            if deployed_hash and package_hash != "unknown" and package_hash == deployed_hash:
                print(f"\n⏭️  This package is already deployed (hash: {package_hash})")
                print(f"   Skipping installation. Use --force to reinstall anyway.")
                return True
        
        # Find node-install.sh
        install_script = None
        for script_path in [
            extracted_dir / "node-install.sh",
            extracted_dir / "src" / "node-install.sh",
        ]:
            if script_path.exists():
                install_script = script_path
                break
        
        if not install_script:
            print("❌ node-install.sh not found in package")
            print("   Package contents:")
            for item in extracted_dir.iterdir():
                print(f"      {item.name}")
            return False
        
        print(f"   Using install script: {install_script}")
        
        # Change to extracted directory and run install script
        original_cwd = os.getcwd()
        try:
            os.chdir(extracted_dir)
            
            # Always use --force when installing from a package because:
            # 1. We've already done version checking in featrix-update.py
            # 2. The package is a specific version we want to install
            # 3. node-install.sh checks git state from /home/mitch/sphere which may not match the package
            cmd = ["sudo", str(install_script), "--force"]
            print(f"   Using --force flag (installing from package)")
            
            # Run the install script with sudo
            result = subprocess.run(
                cmd,
                check=True,
                timeout=600  # 10 minute timeout
            )
            
            print("✅ Installation completed successfully")
            return True
            
        finally:
            os.chdir(original_cwd)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed with exit code {e.returncode}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        traceback.print_exc()
        return False
    finally:
        # Clean up temp directory
        if temp_dir.exists():
            print(f"   Cleaning up temporary files...")
            shutil.rmtree(temp_dir, ignore_errors=True)


def download_file(url: str, dest_path: Path, expected_hash: Optional[str] = None) -> bool:
    """Download a file and verify its hash if provided."""
    try:
        print(f"📥 Downloading {url}...")
        req = Request(url)
        req.add_header('User-Agent', 'Featrix-Update-Script/1.0')
        
        with urlopen(req, timeout=300) as response:
            data = response.read()
            
            # Verify hash if provided
            if expected_hash:
                calculated_hash = hashlib.sha256(data).hexdigest()
                if calculated_hash != expected_hash:
                    print(f"❌ Hash mismatch! Expected {expected_hash[:16]}..., got {calculated_hash[:16]}...")
                    return False
                print(f"✅ Hash verified: {expected_hash[:16]}...")
            
            # Write to destination
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, 'wb') as f:
                f.write(data)
            
            file_size_mb = len(data) / (1024 * 1024)
            print(f"✅ Downloaded {file_size_mb:.2f} MB to {dest_path}")
            return True
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False


def main():
    """Main entry point."""
    # Save original working directory to restore it at the end
    original_cwd = os.getcwd()
    
    try:
        parser = argparse.ArgumentParser(description='Check for and install Featrix Sphere updates')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be done without installing')
        parser.add_argument('--force', action='store_true', help='Force update even if already on latest version')
        args = parser.parse_args()
        
        print("=" * 60)
        print("🔄 Featrix Sphere Update Checker")
        print("=" * 60)
        
        # Get current version
        current_version = get_current_version()
        
        if current_version:
            print(f"📦 Current version: {current_version}")
        else:
            print("⚠️  Could not determine current version (continuing anyway)")
        
        # Fetch index
        index = fetch_index()
        if not index:
            print("❌ Failed to fetch firmware index")
            return 1
        
        # Find newest version
        newest = find_newest_version(index)
        if not newest:
            print("❌ No valid firmware files found")
            return 1
        
        newest_version = newest['version']
        newest_filename = newest['filename']
        newest_hash = newest.get('hash')
        newest_date = newest.get('date_modified')
        newest_url = f"{FIRMWARE_SERVER}/{newest_filename}"
        
        # Format date if available
        date_str = ""
        if newest_date:
            try:
                # Parse ISO format date and format nicely
                date_obj = datetime.fromisoformat(newest_date.replace('Z', '+00:00'))
                date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                # Fallback to raw date if parsing fails
                date_str = newest_date
        
        print(f"\n📊 Available versions:")
        print(f"   Newest: {newest_version} ({newest_filename})")
        if date_str:
            print(f"   Date: {date_str}")
        if newest_hash:
            print(f"   Hash: {newest_hash[:16]}...")
        
        # Compare versions
        if not current_version:
            print("\n⚠️  Cannot compare versions - current version unknown")
            should_update = True
        else:
            comparison = compare_versions(current_version, newest_version)
            if comparison < 0:
                print(f"\n✅ Update available: {current_version} → {newest_version}")
                should_update = True
            elif comparison == 0:
                print(f"\n✅ Already on latest version: {current_version}")
                if args.force:
                    print("   --force flag set, will reinstall anyway")
                    should_update = True
                else:
                    should_update = False
            else:
                print(f"\n⚠️  Current version ({current_version}) is newer than available ({newest_version})")
                if args.force:
                    print("   --force flag set, will downgrade anyway")
                    should_update = True
                else:
                    should_update = False
        
        if not should_update:
            print("No update needed.")
            return 0
        
        if args.dry_run:
            print("\n🔍 DRY RUN - Would perform the following:")
            print(f"   1. Download {newest_filename} from {newest_url}")
            if newest_hash:
                print(f"   2. Verify hash: {newest_hash[:16]}...")
            print(f"   3. Extract package and run node-install.sh")
            print("\nRun without --dry-run to perform update.")
            return 0
        
        # Download file
        download_dir = Path.home() / "featrix-updates"
        download_dir.mkdir(exist_ok=True)
        downloaded_file = download_dir / newest_filename
        
        if not download_file(newest_url, downloaded_file, newest_hash):
            print("❌ Download failed")
            return 1
        
        # Install package (self-contained - no external script needed)
        if not install_package(downloaded_file, force=args.force):
            print("❌ Installation failed")
            return 1
        
        # Announce node to sphere-api after successful installation
        print("\n📡 Announcing node to sphere-api...")
        installed_version = get_current_version() or newest_version
        installed_hash = newest_hash[:8] if newest_hash else None
        announce_to_sphere_api(installed_version, installed_hash, status="available")
        
        return 0
    
    finally:
        # Always restore original working directory
        try:
            os.chdir(original_cwd)
        except Exception:
            pass  # Ignore errors when restoring directory


if __name__ == "__main__":
    exit(main())

