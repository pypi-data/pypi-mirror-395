#!/usr/bin/env python3
"""
Build-time version stamping script.

This script generates a comprehensive version.json file with all version info
baked in at build/deployment time, so we don't need git commands at runtime.

Run this before deployment to stamp version info into the codebase.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def run_git_command(cmd: list) -> Optional[str]:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent  # Repository root
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Warning: Git command failed: {e}")
    return None


def get_semantic_version() -> str:
    """Read semantic version from VERSION file."""
    try:
        version_file = Path(__file__).parent.parent / "VERSION"
        if version_file.exists():
            version = version_file.read_text().strip()
            if version:
                return version
    except Exception as e:
        print(f"Warning: Failed to read VERSION file: {e}")
    
    return "unknown"


def build_version_info():
    """Build comprehensive version information."""
    print("🔨 Building version information...")
    
    # Get semantic version
    semantic_version = get_semantic_version()
    print(f"📦 Semantic version: {semantic_version}")
    
    # Get git info
    git_hash = run_git_command(["git", "rev-parse", "HEAD"])
    git_hash_short = git_hash[:8] if git_hash else "unknown"
    git_branch = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    
    # Check if working directory is dirty
    is_dirty = False
    dirty_check = run_git_command(["git", "status", "--porcelain"])
    if dirty_check:
        is_dirty = bool(dirty_check.strip())
    
    # Get last commit info
    commit_message = run_git_command(["git", "log", "-1", "--pretty=%s"])
    commit_author = run_git_command(["git", "log", "-1", "--pretty=%an"])
    commit_date = run_git_command(["git", "log", "-1", "--pretty=%ci"])
    
    # Build timestamp (when this version was built)
    build_timestamp = datetime.now(timezone.utc)
    build_timestamp_str = build_timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    build_timestamp_iso = build_timestamp.isoformat()
    
    # Create version info dict
    version_info = {
        "semantic_version": semantic_version,
        "git": {
            "hash": git_hash,
            "hash_short": git_hash_short,
            "branch": git_branch or "unknown",
            "is_dirty": is_dirty,
            "last_commit": {
                "message": commit_message or "unknown",
                "author": commit_author or "unknown", 
                "date": commit_date or "unknown"
            }
        },
        "build": {
            "timestamp": build_timestamp_str,
            "timestamp_iso": build_timestamp_iso,
            "builder": "build_version.py"
        }
    }
    
    # Create full version string
    version_parts = [f"v{semantic_version}"]
    if git_hash_short != "unknown":
        hash_part = git_hash_short
        if is_dirty:
            hash_part += "-dirty"
        version_parts.append(f"({hash_part})")
    
    if git_branch and git_branch not in ["main", "master", "unknown"]:
        version_parts.append(f"[{git_branch}]")
    
    version_parts.append(f"built {build_timestamp_str}")
    
    version_info["full_version"] = " ".join(version_parts)
    
    print(f"🔍 Git hash: {git_hash_short}")
    print(f"🌿 Git branch: {git_branch}")
    print(f"💾 Is dirty: {is_dirty}")
    print(f"⏰ Build time: {build_timestamp_str}")
    print(f"📋 Full version: {version_info['full_version']}")
    
    return version_info


def write_version_file(version_info: dict):
    """Write version info to JSON file."""
    version_file = Path(__file__).parent.parent / "version.json"
    
    try:
        with open(version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
        
        print(f"✅ Version file written: {version_file}")
        print(f"   File size: {version_file.stat().st_size} bytes")
        
    except Exception as e:
        print(f"❌ Failed to write version file: {e}")
        sys.exit(1)


def main():
    """Main build function."""
    print("=" * 60)
    print("🏗️  Featrix Sphere Version Builder")
    print("=" * 60)
    
    version_info = build_version_info()
    write_version_file(version_info)
    
    print("=" * 60)
    print("🎉 Version build complete!")
    print(f"📦 Built version: {version_info['full_version']}")
    print("=" * 60)


if __name__ == "__main__":
    main() 