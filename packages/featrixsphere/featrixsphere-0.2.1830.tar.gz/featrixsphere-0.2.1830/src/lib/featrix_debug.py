# featrix_debug.py

import sys
import os
import uuid
import json
import hashlib
import linecache
import datetime
import traceback
import socket
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

FEATRIX_MODULE_PREFIXES = ("featrix", "sphere")
CONTEXT_RADIUS = 3


def _is_featrix_frame(frame):
    mod = frame.f_globals.get("__name__", "")
    filename = frame.f_code.co_filename or ""
    if mod.startswith(FEATRIX_MODULE_PREFIXES):
        return True
    lowered = filename.lower()
    return "featrix" in lowered or "/sphere/" in lowered


def _file_md5(path, _cache={}):
    if not path or not os.path.isfile(path):
        return None
    if path in _cache:
        return _cache[path]
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                if not chunk:
                    break
                h.update(chunk)
        digest = h.hexdigest()
    except Exception:
        digest = None
    _cache[path] = digest
    return digest


def _safe_locals(frame):
    out = {}
    for k, v in frame.f_locals.items():
        try:
            out[k] = repr(v)
        except Exception as e:
            out[k] = f"<unreprable {type(v).__name__}: {e}>"
    return out


def _code_context(filename, lineno, radius=CONTEXT_RADIUS):
    ctx = []
    for offset in range(-radius, radius + 1):
        lnum = lineno + offset
        if lnum <= 0:
            continue
        line = linecache.getline(filename, lnum)
        if not line:
            continue
        ctx.append({
            "lineno": lnum,
            "is_error_line": (offset == 0),
            "code": line.rstrip("\n"),
        })
    return ctx


def _get_hostname():
    """Get hostname."""
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def _get_process_info():
    """Get process information."""
    try:
        return {
            "pid": os.getpid(),
            "ppid": os.getppid() if hasattr(os, 'getppid') else None,
        }
    except Exception:
        return {"pid": "unknown"}


def _get_gpu_info():
    """Get GPU information if available."""
    try:
        import torch
        if torch.cuda.is_available():
            return {
                "available": True,
                "device_count": torch.cuda.device_count(),
                "current_device": torch.cuda.current_device(),
                "device_name": torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else None,
            }
        else:
            return {"available": False}
    except ImportError:
        return {"available": False, "error": "torch not available"}
    except Exception as e:
        return {"available": False, "error": str(e)}


def _get_git_info():
    """Get git branch and SHA."""
    branch = "unknown"
    git_sha = "unknown"
    
    # Try to use version module first
    try:
        # Try importing from deployed location
        sys.path.insert(0, '/sphere/app')
        from version import get_version
        v = get_version()
        if v.git_branch:
            branch = v.git_branch
        if v.git_hash:
            git_sha = v.git_hash[:8]  # Short hash
    except Exception:
        pass
    
    # Fallback to subprocess if version module didn't work
    if branch == "unknown" or git_sha == "unknown":
        # Try common git repo locations
        for repo_path in [Path("/home/mitch/sphere"), Path("/sphere/app"), Path(".")]:
            if (repo_path / ".git").exists():
                try:
                    if branch == "unknown":
                        result = subprocess.run(
                            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            cwd=repo_path,
                            capture_output=True,
                            timeout=2,
                            stderr=subprocess.DEVNULL
                        )
                        if result.returncode == 0:
                            branch = result.stdout.decode().strip()
                    
                    if git_sha == "unknown":
                        result = subprocess.run(
                            ["git", "rev-parse", "--short", "HEAD"],
                            cwd=repo_path,
                            capture_output=True,
                            timeout=2,
                            stderr=subprocess.DEVNULL
                        )
                        if result.returncode == 0:
                            git_sha = result.stdout.decode().strip()
                    
                    if branch != "unknown" and git_sha != "unknown":
                        break
                except Exception:
                    continue
    
    return {"branch": branch, "sha": git_sha}


def featrix_excepthook(exc_type, exc, tb):
    frames = []
    cur = tb

    while cur is not None:
        frame = cur.tb_frame
        code = frame.f_code
        filename = code.co_filename
        lineno = cur.tb_lineno
        is_featrix = _is_featrix_frame(frame)

        frames.append({
            "filename": filename,
            "function": code.co_name,
            "lineno": lineno,
            "file_md5": _file_md5(filename),
            "is_featrix_frame": is_featrix,
            "code_context": _code_context(filename, lineno),
            "locals": _safe_locals(frame) if is_featrix else None,
        })

        cur = cur.tb_next

    # Get system and environment info
    hostname = _get_hostname()
    process_info = _get_process_info()
    gpu_info = _get_gpu_info()
    git_info = _get_git_info()

    payload = {
        "__comment__": "FEATRIX TRACEBACK",
        "__version__": "1.0",
        "__id__": str(uuid.uuid4()),
        "__timestamp__": datetime.datetime.utcnow().isoformat() + "Z",
        "__line_count__": len(frames),
        "__hostname__": hostname,
        "__process__": process_info,
        "__gpu_info__": gpu_info,
        "__branch__": git_info["branch"],
        "__git_sha__": git_info["sha"],

        "exception_type": exc_type.__name__,
        "exception_message": str(exc),
        "frames": frames,
    }

    # Primary: send to logging with a big, easy-to-grab extra field
    try:
        logger.error("Uncaught exception in Featrix", extra={"featrix_trace": payload})
    except Exception:
        # Last-ditch fallback so we don't lose the info completely
        try:
            sys.stderr.write(json.dumps(payload, separators=(",", ":")) + "\n")
        except Exception:
            sys.stderr.write(
                '{"__comment__":"FEATRIX TRACEBACK","error":"logging_failed"}\n'
            )

    # Also show normal traceback for humans
    traceback.print_exception(exc_type, exc, tb)


def install_featrix_excepthook():
    """Install the Featrix exception hook as the system excepthook."""
    sys.excepthook = featrix_excepthook
