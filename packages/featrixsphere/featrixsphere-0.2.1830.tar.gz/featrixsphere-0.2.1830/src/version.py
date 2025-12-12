#!/usr/bin/env python3
"""
Version tracking for Featrix Sphere.

Provides version information including semantic version and git commit hash.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Cache version info to avoid repeated git calls
_version_cache = None

class VersionInfo:
    """Container for version information."""
    
    def __init__(self, semantic_version: str, git_hash: Optional[str] = None, 
                 git_branch: Optional[str] = None, is_dirty: bool = False, 
                 git_date: Optional[str] = None):
        self.semantic_version = semantic_version
        self.git_hash = git_hash
        self.git_branch = git_branch
        self.is_dirty = is_dirty
        self.git_date = git_date
    
    def __str__(self):
        """Full version string for logging."""
        parts = [f"v{self.semantic_version}"]
        
        if self.git_hash:
            hash_part = self.git_hash[:8]  # Short hash
            if self.is_dirty:
                hash_part += "-dirty"
            parts.append(f"({hash_part})")
        
        if self.git_branch and self.git_branch != "main":
            parts.append(f"[{self.git_branch}]")
        
        return " ".join(parts)
    
    def short(self):
        """Short version for display."""
        return f"v{self.semantic_version}"
    
    def dict(self):
        """Dictionary representation."""
        return {
            "semantic_version": self.semantic_version,
            "git_hash": self.git_hash,
            "git_branch": self.git_branch,
            "is_dirty": self.is_dirty,
            "git_date": self.git_date,
            "full_version": str(self)
        }


def _run_git_command(cmd: list) -> Optional[str]:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent.parent  # Repository root
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def _get_semantic_version() -> str:
    """Read semantic version from VERSION file."""
    # Try multiple possible locations for VERSION file in order of preference
    possible_version_paths = [
        # Production deployment path (where deployment scripts copy VERSION)
        Path("/sphere/VERSION"),
        # Development/repository path 
        Path(__file__).parent.parent / "VERSION",
        # Alternative production paths
        Path("/sphere/app/VERSION"),
        # Current working directory (fallback)
        Path("VERSION"),
    ]
    
    logger.info(f"🔍 VERSION DEBUG: __file__ = {__file__}")
    logger.info(f"🔍 VERSION DEBUG: Current working directory = {os.getcwd()}")
    
    for version_file in possible_version_paths:
        try:
            logger.info(f"🔍 VERSION DEBUG: Checking VERSION file at: {version_file}")
            
            if version_file.exists():
                version = version_file.read_text().strip()
                logger.info(f"🔍 VERSION DEBUG: Found VERSION file with content: '{version}'")
                
                if version and version != "unknown":
                    logger.info(f"✅ VERSION DEBUG: Using version from {version_file}: {version}")
                    return version
                else:
                    logger.warning(f"⚠️ VERSION DEBUG: VERSION file at {version_file} exists but is empty or invalid")
            else:
                logger.info(f"🔍 VERSION DEBUG: VERSION file does not exist at {version_file}")
                
        except Exception as e:
            logger.warning(f"⚠️ VERSION DEBUG: Failed to read VERSION file at {version_file}: {e}")
    
    # VERSION file not found anywhere - this is a deployment issue, don't hide it
    logger.error(f"❌ VERSION FAILURE: No VERSION file found in any expected location!")
    logger.error(f"   Searched paths: {[str(p) for p in possible_version_paths]}")
    logger.error(f"   This indicates a deployment configuration problem.")
    
    # Fail explicitly instead of hiding the problem with a fallback
    raise FileNotFoundError(
        f"VERSION file not found in any expected location. "
        f"Searched: {[str(p) for p in possible_version_paths]}. "
        f"This indicates a deployment issue - VERSION file should be available."
    )


def _get_git_info() -> tuple[Optional[str], Optional[str], bool, Optional[str]]:
    """Get git commit hash, branch, dirty status, and commit date."""
    git_hash = None
    git_branch = None
    git_date = None
    is_dirty = False
    
    # Try git commands first (if in a git repo)
    git_hash = _run_git_command(["git", "rev-parse", "HEAD"])
    git_branch = _run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    
    # If git commands failed (no git repo), try reading from deployment files
    if not git_hash:
        # Try multiple possible locations for VERSION_HASH file
        possible_hash_paths = [
            Path("/sphere/VERSION_HASH"),
            Path("/sphere/app/VERSION_HASH"),
            Path(__file__).parent.parent / "VERSION_HASH",
            Path("VERSION_HASH"),
        ]
        
        for hash_file in possible_hash_paths:
            if hash_file.exists():
                try:
                    git_hash = hash_file.read_text().strip()
                    if git_hash and git_hash != "unknown":
                        logger.info(f"✅ Using git hash from deployment file: {hash_file}")
                        break
                except Exception as e:
                    logger.warning(f"Failed to read VERSION_HASH from {hash_file}: {e}")
    
    if not git_branch:
        # Try multiple possible locations for VERSION_BRANCH file
        possible_branch_paths = [
            Path("/sphere/VERSION_BRANCH"),
            Path("/sphere/app/VERSION_BRANCH"),
            Path(__file__).parent.parent / "VERSION_BRANCH",
            Path("VERSION_BRANCH"),
        ]
        
        for branch_file in possible_branch_paths:
            if branch_file.exists():
                try:
                    git_branch = branch_file.read_text().strip()
                    if git_branch and git_branch != "unknown":
                        logger.info(f"✅ Using git branch from deployment file: {branch_file}")
                        break
                except Exception as e:
                    logger.warning(f"Failed to read VERSION_BRANCH from {branch_file}: {e}")
    
    # Get git commit date - try deployment file first, then git command
    # Try reading from /sphere/VERSION_DATE (written during deployment)
    version_date_paths = [
        Path("/sphere/VERSION_DATE"),
        Path("/sphere/app/VERSION_DATE"),
        Path(__file__).parent.parent / "VERSION_DATE",
        Path("VERSION_DATE"),
    ]
    
    for version_date_path in version_date_paths:
        if version_date_path.exists():
            try:
                git_date = version_date_path.read_text().strip()
                if git_date and git_date != "unknown":
                    logger.info(f"✅ Using git date from deployment file: {version_date_path}")
                    break
            except Exception as e:
                logger.warning(f"Failed to read VERSION_DATE from {version_date_path}: {e}")
    
    # Fall back to git command if available and date not found
    if not git_date and git_hash:
        git_date = _run_git_command(["git", "show", "-s", "--format=%ci", git_hash])
    
    # Check if working directory is dirty (only if we have a git repo)
    if git_hash and _run_git_command(["git", "rev-parse", "--git-dir"]):
        dirty_check = _run_git_command(["git", "status", "--porcelain"])
        if dirty_check:
            is_dirty = bool(dirty_check.strip())
    
    return git_hash, git_branch, is_dirty, git_date


def get_version() -> VersionInfo:
    """Get comprehensive version information."""
    global _version_cache
    
    if _version_cache is None:
        try:
            semantic_version = _get_semantic_version()
        except FileNotFoundError as e:
            logger.error(f"❌ VERSION FAILURE: {e}")
            # Make the version failure very visible instead of hiding it
            semantic_version = "VERSION_NOT_FOUND"
        
        git_hash, git_branch, is_dirty, git_date = _get_git_info()
        
        _version_cache = VersionInfo(
            semantic_version=semantic_version,
            git_hash=git_hash,
            git_branch=git_branch,
            is_dirty=is_dirty,
            git_date=git_date
        )
    
    return _version_cache


def print_version_banner(service_name: str = "Featrix Sphere"):
    """Print a version banner for service startup."""
    version = get_version()
    
    print("=" * 60)
    print(f"🚀 {service_name} Starting Up")
    
    # Make version issues very visible
    if version.semantic_version in ["VERSION_NOT_FOUND", "VERSION_FILE_NOT_FOUND"]:
        print(f"❌ Version: {version} ❌")
        print("⚠️  WARNING: VERSION FILE NOT FOUND!")
        print("⚠️  This indicates a deployment configuration problem!")
        print("⚠️  Expected VERSION file in production deployment!")
    else:
        print(f"📦 Version: {version}")
    
    # Show git commit date instead of current time
    if version.git_date:
        # Parse and format git date nicely
        try:
            from datetime import datetime
            # Git date format: "2025-01-04 15:30:22 -0500"
            dt = datetime.fromisoformat(version.git_date.rsplit(' ', 1)[0])
            formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            print(f"🕐 Version Date: {formatted_date}")
        except Exception:
            print(f"🕐 Version Date: {version.git_date}")
    else:
        print(f"🕐 Version Date: unknown")
    
    print(f"🔧 Working Directory: {os.getcwd()}")
    print(f"🐍 Python: {os.sys.version.split()[0]}")
    print("=" * 60)
    
    # Also log it
    date_str = version.git_date or "unknown"
    logger.info(f"{service_name} version: {version} (date: {date_str})")


def bump_version(component: str = "patch", quiet: bool = False) -> str:
    """
    Bump the version in VERSION file.
    
    Args:
        component: 'major', 'minor', or 'patch'
        quiet: If True, don't print output
    
    Returns:
        New version string
    """
    current = _get_semantic_version()
    
    try:
        major, minor, patch = map(int, current.split('.'))
        
        if component == "major":
            major += 1
            minor = 0
            patch = 0
        elif component == "minor":
            minor += 1
            patch = 0
        elif component == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid component: {component}")
        
        new_version = f"{major}.{minor}.{patch}"
        
        # Write to VERSION file
        version_file = Path(__file__).parent.parent / "VERSION"
        version_file.write_text(new_version + "\n")
        
        # Clear cache so next call gets new version
        global _version_cache
        _version_cache = None
        
        if not quiet:
            print(f"Version bumped: {current} → {new_version}")
        return new_version
        
    except Exception as e:
        raise ValueError(f"Failed to bump version from '{current}': {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Parse arguments
        args = sys.argv[1:]
        quiet = "--quiet" in args
        
        # Remove --quiet from args
        args = [arg for arg in args if arg != "--quiet"]
        
        if len(args) > 0:
            component = args[0]
            if component in ["major", "minor", "patch"]:
                bump_version(component, quiet=quiet)
            else:
                print(f"Usage: python version.py [major|minor|patch] [--quiet]")
                sys.exit(1)
        else:
            print(f"Usage: python version.py [major|minor|patch] [--quiet]")
            sys.exit(1)
    else:
        # Print version
        print_version_banner() 