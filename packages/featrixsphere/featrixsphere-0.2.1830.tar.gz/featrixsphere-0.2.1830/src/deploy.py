#!/usr/bin/env python3
"""
Simple deployment script for Featrix Sphere.
Does ONE thing: deploys code reliably.
"""
import os
import sys
import time
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


def run(cmd, check=True):
    """Run command and return output."""
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"✗ Command failed: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


def main():
    print("=" * 60)
    print("🚀 Featrix Sphere Deployment")
    print("=" * 60)
    
    # 1. Clean source repo of all bytecode
    print("\n[1/8] Cleaning source repository...")
    for pattern in ["**/__pycache__", "**/*.pyc", "**/*.pyo"]:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    
    # 2. Get version and git info
    print("\n[2/8] Getting version info...")
    version = Path("VERSION").read_text().strip()
    git_hash = run("git rev-parse --short HEAD", check=False) or "unknown"
    git_branch = run("git rev-parse --abbrev-ref HEAD", check=False) or "unknown"
    git_date = run("git show -s --format=%ci HEAD", check=False) or "unknown"
    print(f"   Version: {version}")
    print(f"   Git: {git_hash} ({git_branch})")
    
    # 3. Nuke corrupted venv
    print("\n[3/8] Removing old venv...")
    for venv_path in ["/sphere/.venv", "/shared1/sphere-data/.venv"]:
        if Path(venv_path).exists():
            run(f"rm -rf {venv_path}")
    
    # 4. Copy files
    print("\n[4/8] Copying application files...")
    run("mkdir -p /sphere/app")
    run("rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' src/ /sphere/app/")
    # Explicitly ensure critical supervisor files are copied and executable
    if Path("src/gc_cleanup.py").exists():
        print("   Ensuring gc_cleanup.py is executable...")
        run("cp src/gc_cleanup.py /sphere/app/gc_cleanup.py")
        run("chmod +x /sphere/app/gc_cleanup.py")
    if Path("src/featrix_watchdog.py").exists():
        print("   Ensuring featrix_watchdog.py is executable...")
        run("cp src/featrix_watchdog.py /sphere/app/featrix_watchdog.py")
        run("chmod +x /sphere/app/featrix_watchdog.py")
    
    # 5. Write version files
    print("\n[5/8] Writing version files...")
    Path("/sphere/VERSION").write_text(version)
    Path("/sphere/VERSION_DATE").write_text(git_date)
    
    # 6. Create fresh venv and install packages
    print("\n[6/8] Creating fresh venv and installing packages...")
    run("python3 -m venv /sphere/.venv")
    pip = "/sphere/.venv/bin/pip"
    run(f"{pip} install --upgrade pip setuptools wheel")
    
    # Install core packages
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.5.0",
        "pydantic-settings>=2.0.0",
        "pandas>=2.1.4",
        "torch>=2.1.0",
        "redis>=4.5.0",
        "celery>=5.3.0",
        "requests>=2.31.0",
        "jsontables",
    ]
    run(f"{pip} install {' '.join(packages)}")
    
    # 7. Restart services
    print("\n[7/8] Restarting services...")
    run("supervisorctl restart all", check=False)
    time.sleep(5)
    
    # 8. Send Slack notification
    print("\n[8/8] Sending Slack notification...")
    webhook = Path("/etc/.hook").read_text().strip() if Path("/etc/.hook").exists() else None
    
    if webhook:
        # Wait for API and get health
        health = None
        for i in range(5):
            try:
                result = run(f"curl -s http://localhost:8000/health --max-time 10", check=False)
                if result and len(result) > 100:
                    health = json.loads(result)
                    break
            except:
                pass
            time.sleep(3)
        
        # Format message
        msg = f"🚀 *Featrix Sphere deployed on {run('hostname')}*\n"
        msg += f"• Version: `{version}`\n"
        msg += f"• Git: `{git_hash}` ({git_branch})\n"
        msg += f"• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n"
        
        if health:
            msg += "*Health Check:*\n"
            if health.get("gpu", {}).get("available"):
                gpu = health["gpu"]
                msg += f"🎮 GPU: {gpu['gpu_count']} GPU(s), {gpu['total_free_gb']:.1f} GB free\n"
            if health.get("ready_for_training"):
                msg += f"✅ Ready for Training: Yes\n"
            if health.get("celery"):
                c = health["celery"]
                msg += f"👷 Celery: {c['total_workers']} workers\n"
        else:
            msg += "⚠️ Health check unavailable\n"
        
        # Send to Slack
        payload = json.dumps({"text": msg})
        run(f"curl -s -X POST '{webhook}' -H 'Content-Type: application/json' -d '{payload}'", check=False)
    
    print("\n" + "=" * 60)
    print("✅ Deployment complete!")
    print("=" * 60)
    
    # Show service status
    run("supervisorctl status", check=False)


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("ERROR: Must run as root (use sudo)")
        sys.exit(1)
    main()

