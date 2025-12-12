#!/usr/bin/env python3
"""
System Resource Monitor for Featrix Sphere
Tracks GPU, CPU, and memory usage every 15-30 seconds
Correlates resource usage with job completion events
"""

import json
import logging
import os
import sqlite3
import time
import re
import threading
import linecache
import hashlib
import socket
import traceback
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set

# Redis is REQUIRED for health data caching - crash if not available
from lib.job_manager import get_redis_client

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class TracebackMonitor:
    """Monitor log files for Python tracebacks and send to monitoring endpoint."""
    
    def __init__(self, watch_dirs: List[str], monitor_url: str = "https://monitor.featrix.com/traceback"):
        self.watch_dirs = [Path(d) for d in watch_dirs]
        self.monitor_url = monitor_url
        self.file_sizes: Dict[Path, int] = {}
        self.seen_traceback_ids: Set[str] = set()
        self.hostname = socket.gethostname()
        self.running = False
        self.thread = None
        
        for watch_dir in self.watch_dirs:
            watch_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Watching log directory: {watch_dir}")
    
    def _get_code_context(self, filename: str, lineno: int, radius: int = 3) -> List[Dict]:
        """Get code context around a line number."""
        context = []
        for offset in range(-radius, radius + 1):
            lnum = lineno + offset
            if lnum <= 0:
                continue
            line = linecache.getline(filename, lnum)
            if not line:
                continue
            context.append({
                "lineno": lnum,
                "is_error_line": (offset == 0),
                "code": line.rstrip("\n"),
            })
        return context
    
    def _enhance_traceback(self, traceback_data: Dict) -> Dict:
        """Enhance traceback with source code context for /sphere/app/* files."""
        enhanced_frames = []
        for frame in traceback_data.get("frames", []):
            filename = frame.get("filename", "")
            lineno = frame.get("lineno", 0)
            if "/sphere/app/" in filename and lineno > 0:
                if not frame.get("code_context"):
                    try:
                        code_context = self._get_code_context(filename, lineno)
                        frame["code_context"] = code_context
                    except Exception as e:
                        logger.debug(f"Could not get code context for {filename}:{lineno}: {e}")
            enhanced_frames.append(frame)
        traceback_data["frames"] = enhanced_frames
        return traceback_data
    
    def _send_traceback(self, traceback_data: Dict, log_file: Path, process_name: str = None):
        """Send traceback to monitoring endpoint AND save locally."""
        traceback_id = traceback_data.get("__id__")
        if traceback_id and traceback_id in self.seen_traceback_ids:
            return
        
        enhanced_tb = self._enhance_traceback(traceback_data.copy())
        enhanced_tb["__monitor_metadata__"] = {
            "log_file": str(log_file),
            "hostname": self.hostname,
            "process": process_name or self._extract_process_name(log_file),
            "detected_at": datetime.now(timezone.utc).isoformat(),
        }
        
        # Save locally to SQLite for monitor page display
        try:
            from lib.crash_tracker import save_crash
            save_crash(enhanced_tb)
        except Exception as e:
            logger.debug(f"Could not save crash locally: {e}")
        
        # Send to remote monitor
        try:
            data = json.dumps(enhanced_tb).encode('utf-8')
            req = urllib.request.Request(
                self.monitor_url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"✅ Sent traceback {traceback_id[:8]} to monitor")
                    if traceback_id:
                        self.seen_traceback_ids.add(traceback_id)
                else:
                    logger.warning(f"⚠️  Monitor returned status {response.status} for traceback {traceback_id[:8]}")
        except Exception as e:
            logger.error(f"❌ Error sending traceback {traceback_id[:8]}: {e}")
    
    def _extract_process_name(self, log_file: Path) -> str:
        """Extract process name from log file path."""
        try:
            if "featrix_output" in str(log_file):
                parts = log_file.parts
                for i, part in enumerate(parts):
                    if part == "featrix_output" and i + 1 < len(parts):
                        return parts[i + 1]
            elif log_file.name.endswith(".log"):
                return log_file.stem
        except Exception:
            pass
        return "unknown"
    
    def _parse_traceback_from_text(self, text: str) -> List[Dict]:
        """Parse JSON tracebacks from log text."""
        tracebacks = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if '"__comment__": "FEATRIX TRACEBACK"' in line or '{"__comment__"' in line:
                try:
                    traceback_data = json.loads(line.strip())
                    if traceback_data.get("__comment__") == "FEATRIX TRACEBACK":
                        tracebacks.append(traceback_data)
                        continue
                except json.JSONDecodeError:
                    pass
                
                json_lines = [line]
                brace_count = line.count('{') - line.count('}')
                for j in range(i + 1, min(i + 200, len(lines))):
                    next_line = lines[j]
                    json_lines.append(next_line)
                    brace_count += next_line.count('{') - next_line.count('}')
                    if brace_count == 0:
                        json_text = '\n'.join(json_lines)
                        try:
                            traceback_data = json.loads(json_text)
                            if traceback_data.get("__comment__") == "FEATRIX TRACEBACK":
                                tracebacks.append(traceback_data)
                                break
                        except json.JSONDecodeError:
                            pass
        return tracebacks
    
    def _process_log_file(self, log_file: Path):
        """Process a log file for new tracebacks."""
        try:
            current_size = log_file.stat().st_size
            if log_file in self.file_sizes and current_size < self.file_sizes[log_file]:
                read_size = min(128 * 1024, current_size)
                offset = max(0, current_size - read_size)
            elif log_file not in self.file_sizes:
                read_size = min(128 * 1024, current_size)
                offset = max(0, current_size - read_size)
            else:
                old_size = self.file_sizes[log_file]
                read_size = current_size - old_size
                offset = old_size
            
            if read_size <= 0:
                self.file_sizes[log_file] = current_size
                return
            
            with open(log_file, 'rb') as f:
                f.seek(offset)
                content = f.read(read_size).decode('utf-8', errors='ignore')
            
            tracebacks = self._parse_traceback_from_text(content)
            for traceback_data in tracebacks:
                logger.info(f"🔍 Found traceback in {log_file}: {traceback_data.get('exception_type')} - {traceback_data.get('exception_message', '')[:50]}")
                self._send_traceback(traceback_data, log_file)
            
            self.file_sizes[log_file] = current_size
        except FileNotFoundError:
            if log_file in self.file_sizes:
                del self.file_sizes[log_file]
        except Exception as e:
            logger.error(f"Error processing log file {log_file}: {e}")
    
    def _scan_log_files(self):
        """Scan watch directories for .log files."""
        log_files = []
        for watch_dir in self.watch_dirs:
            if not watch_dir.exists():
                continue
            for log_file in watch_dir.rglob("*.log"):
                if log_file.is_file():
                    log_files.append(log_file)
        return log_files
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        logger.info("🔍 Starting traceback monitor...")
        while self.running:
            try:
                log_files = self._scan_log_files()
                for log_file in log_files:
                    self._process_log_file(log_file)
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error in traceback monitor loop: {e}")
                time.sleep(10)
    
    def start(self):
        """Start the traceback monitor in a background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("✅ Traceback monitor started")
    
    def stop(self):
        """Stop the traceback monitor."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("🛑 Traceback monitor stopped")


class SystemMonitor:
    def __init__(self, db_path="/sphere/app/system_monitor.db", poll_interval=20, enable_traceback_monitor=True):
        self.db_path = Path(db_path)
        self.poll_interval = poll_interval  # seconds
        self.last_job_scan = 0  # timestamp of last job directory scan
        self.known_jobs = set()  # job IDs we've already recorded completion for
        self.last_health_collection = 0  # timestamp of last health data collection
        self.health_collection_interval = 30  # collect health data every 30 seconds
        
        # RAM monitoring state (for high memory alerts)
        self.ram_alert_count = 0  # Number of RAM alerts sent (max 3)
        self.last_ram_alert_time = 0  # Timestamp of last RAM alert
        self.ram_alert_interval = 3600  # 1 hour in seconds
        self.ram_alert_threshold_gb = 100  # Alert if RAM usage > 100 GB
        self.max_ram_alerts = 3  # Maximum number of alerts to send
        
        # Backplane monitoring state
        self.last_backplane_check = 0  # timestamp of last backplane check
        self.backplane_check_interval = 120  # 2 minutes in seconds
        self.backplane_rsync_running = False  # Track if rsync is currently running
        self.backplane_status = {
            'last_run': None,
            'last_success': None,
            'last_error': None,
            'status': 'never_run',
            'running': False
        }
        
        # API retry processing state
        self.last_retry_process = 0  # timestamp of last retry processing
        self.retry_process_interval = 60  # 1 minute in seconds
        
        # Initialize database
        self.init_database()
        
        # Load existing jobs on startup
        self.scan_existing_jobs()
        
        # Initialize traceback monitor
        self.traceback_monitor = None
        if enable_traceback_monitor:
            try:
                watch_dirs = ["/var/log/featrix", "/sphere/app/featrix_output"]
                self.traceback_monitor = TracebackMonitor(watch_dirs=watch_dirs)
                self.traceback_monitor.start()
            except Exception as e:
                logger.warning(f"Could not start traceback monitor: {e}")
        
        logger.info(f"System monitor initialized with {self.poll_interval}s polling interval")
        logger.info(f"Database: {self.db_path}")

    def init_database(self):
        """Initialize SQLite database for monitoring data."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            
            # System metrics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cpu_percent REAL,
                    memory_percent REAL,
                    memory_used_gb REAL,
                    memory_total_gb REAL,
                    gpu_count INTEGER,
                    gpu_utilization TEXT,  -- JSON array of GPU utilization %
                    gpu_memory_used TEXT,  -- JSON array of GPU memory used MB
                    gpu_memory_total TEXT, -- JSON array of GPU memory total MB
                    gpu_memory_percent TEXT, -- JSON array of GPU memory %
                    gpu_temperature TEXT,  -- JSON array of GPU temperatures
                    load_average_1m REAL,
                    load_average_5m REAL,
                    load_average_15m REAL,
                    disk_usage_percent REAL
                )
            """)
            
            # Job completion events table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    job_type TEXT,
                    session_id TEXT,
                    event_type TEXT NOT NULL,  -- 'started', 'completed', 'failed'
                    timestamp TEXT NOT NULL,
                    runtime_seconds REAL,
                    log_file_size INTEGER,
                    working_directory TEXT,
                    cpu_time_user REAL,
                    cpu_time_system REAL,
                    peak_memory_mb REAL,
                    exit_code INTEGER
                )
            """)
            
            # Job resource correlation table (links jobs to system metrics during their runtime)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_resource_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    avg_cpu_percent REAL,
                    max_cpu_percent REAL,
                    avg_memory_percent REAL,
                    max_memory_percent REAL,
                    avg_gpu_utilization TEXT,  -- JSON average across all GPUs
                    max_gpu_utilization TEXT,  -- JSON max across all GPUs
                    avg_gpu_memory_percent TEXT,
                    max_gpu_memory_percent TEXT,
                    runtime_seconds REAL
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_job_events_job_id ON job_events(job_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_job_events_timestamp ON job_events(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_job_resource_job_id ON job_resource_usage(job_id)")
            
            conn.commit()
        
        logger.info("Database initialized successfully")

    def get_cpu_stats(self) -> Dict:
        """Get CPU usage statistics."""
        try:
            import psutil
            
            # CPU percentage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Load averages
            load_avg = os.getloadavg()
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'load_average_1m': load_avg[0],
                'load_average_5m': load_avg[1],
                'load_average_15m': load_avg[2]
            }
        except ImportError:
            logger.warning("psutil not available - CPU/memory stats disabled")
            return {}
        except Exception as e:
            logger.error(f"Error getting CPU stats: {e}")
            return {}

    def check_ram_usage(self, memory_used_gb: float):
        """Check RAM usage and send Slack alerts if over threshold.
        
        Alerts are sent:
        - Once per hour (self.ram_alert_interval)
        - Maximum 3 times total (self.max_ram_alerts)
        - Only if memory_used_gb > self.ram_alert_threshold_gb (100 GB)
        """
        if memory_used_gb is None:
            return
        
        current_time = time.time()
        
        # Check if we're over threshold
        if memory_used_gb <= self.ram_alert_threshold_gb:
            # Memory is below threshold - reset alert count if it was high before
            if self.ram_alert_count > 0:
                logger.debug(f"RAM usage dropped below threshold ({memory_used_gb:.1f} GB < {self.ram_alert_threshold_gb} GB) - resetting alert count")
                self.ram_alert_count = 0
            return
        
        # We're over threshold - check if we should send an alert
        if self.ram_alert_count >= self.max_ram_alerts:
            # Already sent max alerts - don't send more
            return
        
        # Check if enough time has passed since last alert
        time_since_last = current_time - self.last_ram_alert_time
        if time_since_last < self.ram_alert_interval:
            # Not enough time has passed - skip this check
            return
        
        # Send alert
        try:
            from slack import send_slack_message
            import socket
            hostname = socket.gethostname()
            
            alert_number = self.ram_alert_count + 1
            slack_msg = (
                f"⚠️  **High RAM Usage Alert** ({alert_number}/{self.max_ram_alerts})\n"
                f"Host: {hostname}\n"
                f"Memory Used: {memory_used_gb:.1f} GB\n"
                f"Threshold: {self.ram_alert_threshold_gb} GB\n"
                f"\n"
                f"System is using over {self.ram_alert_threshold_gb} GB of RAM.\n"
                f"This alert will be sent up to {self.max_ram_alerts} times (once per hour).\n"
                f"\n"
                f"**Possible causes:**\n"
                f"- String cache growing unbounded\n"
                f"- SQLite cache size too large\n"
                f"- Memory leak in training process\n"
                f"- Large dataset loaded in memory"
            )
            
            send_slack_message(slack_msg, throttle=False, skip_hostname_prefix=True)
            logger.warning(f"🚨 High RAM usage alert sent: {memory_used_gb:.1f} GB (alert {alert_number}/{self.max_ram_alerts})")
            
            # Update state
            self.ram_alert_count += 1
            self.last_ram_alert_time = current_time
            
        except Exception as e:
            logger.error(f"Failed to send RAM usage alert: {e}")

    def get_gpu_stats(self) -> Dict:
        """Get GPU usage statistics using nvidia-smi."""
        try:
            import subprocess
            import json
            
            # Query GPU stats using nvidia-smi
            cmd = [
                'nvidia-smi', 
                '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu',
                '--format=csv,noheader,nounits'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                logger.warning("nvidia-smi command failed - GPU stats disabled")
                return {}
            
            lines = result.stdout.strip().split('\n')
            gpu_count = len(lines)
            
            gpu_utilization = []
            gpu_memory_used = []
            gpu_memory_total = []
            gpu_memory_percent = []
            gpu_temperature = []
            
            for line in lines:
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 4:
                        util = float(parts[0]) if parts[0] != '[Not Supported]' else 0.0
                        mem_used = float(parts[1])
                        mem_total = float(parts[2])
                        temp = float(parts[3]) if parts[3] != '[Not Supported]' else 0.0
                        
                        gpu_utilization.append(util)
                        gpu_memory_used.append(mem_used)
                        gpu_memory_total.append(mem_total)
                        gpu_memory_percent.append((mem_used / mem_total * 100) if mem_total > 0 else 0)
                        gpu_temperature.append(temp)
            
            return {
                'gpu_count': gpu_count,
                'gpu_utilization': json.dumps(gpu_utilization),
                'gpu_memory_used': json.dumps(gpu_memory_used),
                'gpu_memory_total': json.dumps(gpu_memory_total),
                'gpu_memory_percent': json.dumps(gpu_memory_percent),
                'gpu_temperature': json.dumps(gpu_temperature)
            }
            
        except subprocess.TimeoutExpired:
            logger.warning("nvidia-smi timeout - GPU stats disabled")
            return {}
        except FileNotFoundError:
            logger.warning("nvidia-smi not found - GPU stats disabled")
            return {}
        except Exception as e:
            logger.error(f"Error getting GPU stats: {e}")
            return {}

    def get_disk_stats(self) -> Dict:
        """Get disk usage statistics."""
        try:
            import shutil
            
            # Check disk usage for /sphere/app
            total, used, free = shutil.disk_usage('/sphere/app')
            
            usage_percent = (used / total) * 100
            
            return {
                'disk_usage_percent': usage_percent
            }
        except Exception as e:
            logger.error(f"Error getting disk stats: {e}")
            return {}

    def collect_system_metrics(self):
        """Collect all system metrics and store in database."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Collect all metrics
        metrics = {
            'timestamp': timestamp,
            'cpu_percent': None,
            'memory_percent': None,
            'memory_used_gb': None,
            'memory_total_gb': None,
            'gpu_count': 0,
            'gpu_utilization': None,
            'gpu_memory_used': None,
            'gpu_memory_total': None,
            'gpu_memory_percent': None,
            'gpu_temperature': None,
            'load_average_1m': None,
            'load_average_5m': None,
            'load_average_15m': None,
            'disk_usage_percent': None
        }
        
        # Update with actual stats
        metrics.update(self.get_cpu_stats())
        metrics.update(self.get_gpu_stats())
        metrics.update(self.get_disk_stats())
        
        # Store in database
        try:
            with sqlite3.connect(self.db_path) as conn:
                columns = ', '.join(metrics.keys())
                placeholders = ', '.join(['?' for _ in metrics])
                
                conn.execute(
                    f"INSERT INTO system_metrics ({columns}) VALUES ({placeholders})",
                    list(metrics.values())
                )
                conn.commit()
                
            # Log summary (only every 5th reading to avoid spam)
            if int(time.time()) % (self.poll_interval * 5) < self.poll_interval:
                cpu_info = f"CPU: {metrics['cpu_percent']:.1f}%" if metrics['cpu_percent'] else "CPU: N/A"
                mem_info = f"RAM: {metrics['memory_percent']:.1f}%" if metrics['memory_percent'] else "RAM: N/A"
                
                gpu_info = "GPU: N/A"
                if metrics['gpu_utilization']:
                    gpu_utils = json.loads(metrics['gpu_utilization'])
                    gpu_mems = json.loads(metrics['gpu_memory_percent'])
                    if gpu_utils:
                        gpu_info = f"GPU: {gpu_utils[0]:.1f}% util, {gpu_mems[0]:.1f}% mem"
                
                logger.info(f"📊 {cpu_info} | {mem_info} | {gpu_info}")
                
        except Exception as e:
            logger.error(f"Error storing system metrics: {e}")

    def collect_health_data(self):
        """Collect health data (GPU, Celery workers, etc.) and cache in Redis for /health endpoint."""
        try:
            redis_client = get_redis_client()
        except Exception as e:
            logger.error(f"❌ CRITICAL: Failed to get Redis client for health cache: {e}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            return
        
        current_time = time.time()
        logger.debug(f"🔄 Collecting health data for Redis cache...")
        
        # Collect GPU info using nvidia-smi (NO torch import - don't waste GPU memory!)
        gpu_info = {"error": "GPU info not available"}
        try:
            import subprocess
            # Query GPU memory and utilization
            gpu_cmd = [
                'nvidia-smi',
                '--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu',
                '--format=csv,noheader,nounits'
            ]
            result = subprocess.run(gpu_cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                gpus = []
                total_free_gb = 0
                total_used_gb = 0
                total_capacity_gb = 0
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 6:
                            gpu_id = int(parts[0])
                            name = parts[1]
                            mem_total = float(parts[2]) / 1024  # MB to GB
                            mem_used = float(parts[3]) / 1024
                            mem_free = float(parts[4]) / 1024
                            utilization = float(parts[5]) if parts[5] != '[Not Supported]' else 0.0
                            
                            total_free_gb += mem_free
                            total_used_gb += mem_used
                            total_capacity_gb += mem_total
                            
                            gpus.append({
                                "gpu_id": gpu_id,
                                "name": name,
                                "memory_free_gb": round(mem_free, 2),
                                "memory_used_gb": round(mem_used, 2),
                                "memory_total_gb": round(mem_total, 2),
                                "utilization_pct": round((mem_used / mem_total) * 100, 1) if mem_total > 0 else 0,
                                "memory_percent": round((mem_used / mem_total) * 100, 1) if mem_total > 0 else 0,
                            })
                
                overall_gpu_mem_percent = (total_used_gb / total_capacity_gb * 100) if total_capacity_gb > 0 else 0
                gpu_info = {
                    "available": True,
                    "gpu_count": len(gpus),
                    "total_free_gb": round(total_free_gb, 2),
                    "total_used_gb": round(total_used_gb, 2),
                    "total_capacity_gb": round(total_capacity_gb, 2),
                    "memory_percent": round(overall_gpu_mem_percent, 1),
                    "gpus": gpus,
                }
            else:
                gpu_info = {"available": False, "reason": "nvidia-smi command failed"}
        except FileNotFoundError:
            gpu_info = {"available": False, "reason": "nvidia-smi not found"}
        except Exception as e:
            gpu_info = {"error": str(e)}
        
        # Collect Celery worker info with proper timeout and error handling
        # Since workers are on the same physical box, we can check processes and use longer timeout
        celery_info = {"available": False, "error": "Not initialized"}
        job_queues = {"training_jobs": {"running": 0, "queued": 0}, "prediction_jobs": {"running": 0, "queued": 0}}
        
        # First, check if Celery worker processes are actually running (since they're local)
        worker_processes_running = 0
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('celery' in str(arg).lower() and 'worker' in str(arg).lower() for arg in cmdline):
                        worker_processes_running += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        
        try:
            from celery_app import app as celery_app
            
            # Use longer timeout (10 seconds) since workers are on same box
            inspect = celery_app.control.inspect(timeout=10.0)
            
            # First check if workers are available
            try:
                stats = inspect.stats()
                if not stats:
                    # No workers responding via Celery inspect, but check if processes are running
                    if worker_processes_running > 0:
                        celery_info = {
                            "available": False,
                            "error": f"Worker processes running ({worker_processes_running}) but not responding to Celery inspect",
                            "worker_processes_detected": worker_processes_running,
                            "total_workers": 0,
                            "busy_workers": 0,
                            "idle_workers": 0,
                            "active_tasks": 0,
                            "queued_tasks": 0
                        }
                    else:
                        celery_info = {
                            "available": False,
                            "error": "No Celery workers responding and no worker processes detected",
                            "worker_processes_detected": 0,
                            "total_workers": 0,
                            "busy_workers": 0,
                            "idle_workers": 0,
                            "active_tasks": 0,
                            "queued_tasks": 0
                        }
                else:
                    # Workers are available, now get active and reserved tasks
                    total_workers = len(stats.keys())
                    busy_workers = 0
                    total_active = 0
                    total_reserved = 0
                    training_jobs_running = 0
                    prediction_jobs_running = 0
                    training_jobs_queued = 0
                    prediction_jobs_queued = 0
                    
                    # Get active tasks
                    active_tasks = {}
                    try:
                        active_result = inspect.active()
                        if active_result is not None:
                            active_tasks = active_result
                    except Exception as e:
                        # If active() fails, continue with empty dict
                        active_tasks = {}
                    
                    # Get reserved tasks
                    reserved_tasks = {}
                    try:
                        reserved_result = inspect.reserved()
                        if reserved_result is not None:
                            reserved_tasks = reserved_result
                    except Exception as e:
                        # If reserved() fails, continue with empty dict
                        reserved_tasks = {}
                    
                    # Process active tasks
                    if active_tasks:
                        for worker, tasks in active_tasks.items():
                            if tasks and isinstance(tasks, list):
                                busy_workers += 1
                                total_active += len(tasks)
                                for task in tasks:
                                    task_name = task.get("name", "") if isinstance(task, dict) else ""
                                    if "train" in task_name.lower() or "embedding" in task_name.lower() or "train_es" in task_name.lower():
                                        training_jobs_running += 1
                                    elif "predict" in task_name.lower() or "predict_batch" in task_name.lower():
                                        prediction_jobs_running += 1
                    
                    # Process reserved tasks
                    if reserved_tasks:
                        for worker, tasks in reserved_tasks.items():
                            if tasks and isinstance(tasks, list):
                                total_reserved += len(tasks)
                                for task in tasks:
                                    task_name = task.get("name", "") if isinstance(task, dict) else ""
                                    if "train" in task_name.lower() or "embedding" in task_name.lower() or "train_es" in task_name.lower():
                                        training_jobs_queued += 1
                                    elif "predict" in task_name.lower() or "predict_batch" in task_name.lower():
                                        prediction_jobs_queued += 1
                    
                    celery_info = {
                        "available": True,
                        "total_workers": total_workers,
                        "busy_workers": busy_workers,
                        "idle_workers": total_workers - busy_workers,
                        "active_tasks": total_active,
                        "queued_tasks": total_reserved,
                        "worker_processes_detected": worker_processes_running,
                    }
                    
                    job_queues = {
                        "training_jobs": {"running": training_jobs_running, "queued": training_jobs_queued},
                        "prediction_jobs": {"running": prediction_jobs_running, "queued": prediction_jobs_queued},
                    }
                    
                    # Also get Redis queue lengths as additional info (since workers are local)
                    try:
                        redis_client = get_redis_client()
                        if redis_client:
                            queues_to_check = {
                                "gpu_training": "training_jobs",
                                "predictions": "prediction_jobs",
                                "celery": "general"
                            }
                            for queue_name, job_type in queues_to_check.items():
                                try:
                                    queue_len = redis_client.llen(queue_name)
                                    if job_type == "training_jobs":
                                        job_queues["training_jobs"]["redis_queued"] = queue_len
                                    elif job_type == "prediction_jobs":
                                        job_queues["prediction_jobs"]["redis_queued"] = queue_len
                                except Exception:
                                    pass
                    except Exception:
                        pass
            except Exception as e:
                # Stats check failed - workers might not be available
                error_msg = str(e)[:200]
                celery_info = {
                    "available": False,
                    "error": f"Celery workers not responding: {type(e).__name__}: {error_msg}",
                    "worker_processes_detected": worker_processes_running,
                    "total_workers": 0,
                    "busy_workers": 0,
                    "idle_workers": 0,
                    "active_tasks": 0,
                    "queued_tasks": 0
                }
        except ImportError:
            celery_info = {"available": False, "error": "Celery app not available"}
        except Exception as e:
            celery_info = {
                "available": False,
                "error": f"Celery inspection error: {type(e).__name__}: {str(e)[:100]}",
                "total_workers": 0,
                "busy_workers": 0,
                "idle_workers": 0,
                "active_tasks": 0,
                "queued_tasks": 0
            }
        
        # Get version info
        version = "unknown"
        version_timestamp = None
        try:
            version_file = Path("/sphere/app/VERSION")
            if version_file.exists():
                version = version_file.read_text().strip()
                version_timestamp = version_file.stat().st_mtime
        except Exception:
            pass
        
        # Get git info
        git_info = {"commit": "unknown", "branch": "unknown"}
        try:
            from version import get_version
            v = get_version()
            if v.git_hash:
                git_info["commit"] = v.git_hash[:8] if len(v.git_hash) > 8 else v.git_hash
            if v.git_branch:
                git_info["branch"] = v.git_branch
        except Exception:
            pass
        
        # Get uptime
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            uptime_seconds = time.time() - process.create_time()
        except Exception:
            uptime_seconds = 0
        
        # Get system info
        system_info = {}
        try:
            import psutil
            root_disk = psutil.disk_usage("/")
            sphere_disk = None
            sphere_path = "/sphere"
            try:
                if Path(sphere_path).exists():
                    sphere_disk = psutil.disk_usage(sphere_path)
            except Exception:
                pass
            
            # Get swap memory stats
            swap = psutil.swap_memory()
            swap_total_gb = round(swap.total / (1024**3), 2)
            swap_used_gb = round(swap.used / (1024**3), 2)
            swap_free_gb = round(swap.free / (1024**3), 2)
            swap_percent = swap.percent
            
            system_info = {
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "memory_free_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "swap": {
                    "total_gb": swap_total_gb,
                    "used_gb": swap_used_gb,
                    "free_gb": swap_free_gb,
                    "percent": swap_percent,
                },
                "disk": {
                    "root": {
                        "total_gb": round(root_disk.total / (1024**3), 2),
                        "used_gb": round(root_disk.used / (1024**3), 2),
                        "free_gb": round(root_disk.free / (1024**3), 2),
                        "usage_pct": root_disk.percent,
                    }
                },
            }
            
            if sphere_disk:
                system_info["disk"]["sphere"] = {
                    "path": sphere_path,
                    "total_gb": round(sphere_disk.total / (1024**3), 2),
                    "used_gb": round(sphere_disk.used / (1024**3), 2),
                    "free_gb": round(sphere_disk.free / (1024**3), 2),
                    "usage_pct": sphere_disk.percent,
                }
        except Exception as e:
            system_info = {"error": str(e)}
        
        # Collect supervisor process info
        supervisor_processes = {"error": "supervisorctl not available"}
        try:
            import subprocess
            import psutil
            import shutil
            
            # Find supervisorctl
            supervisorctl_path = shutil.which('supervisorctl')
            if not supervisorctl_path:
                for path in ['/usr/bin/supervisorctl', '/usr/local/bin/supervisorctl']:
                    if os.path.exists(path) and os.access(path, os.X_OK):
                        supervisorctl_path = path
                        break
            
            if supervisorctl_path:
                # Query GPU stats ONCE for all processes
                gpu_stats_map = {}
                gpu_processes_list = []
                gpu_mem_total = None
                try:
                    # Get total GPU memory
                    mem_cmd = ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits']
                    mem_result = subprocess.run(mem_cmd, capture_output=True, text=True, timeout=3)
                    if mem_result.returncode == 0 and mem_result.stdout.strip():
                        gpu_mem_total = float(mem_result.stdout.strip().split(',')[0].strip())
                    
                    # Query GPU processes - use --query-processes which ALWAYS works
                    # --query-compute-apps often returns NOTHING on some GPUs!
                    gpu_cmd = ['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits']
                    gpu_result = subprocess.run(gpu_cmd, capture_output=True, text=True, timeout=5)
                    
                    # CRITICAL FIX: Fallback to --query-processes if compute-apps returns nothing
                    # This is why GPU stats were ALWAYS empty - compute-apps returns nothing!
                    if not (gpu_result.returncode == 0 and gpu_result.stdout.strip()):
                        gpu_cmd = ['nvidia-smi', '--query-processes=pid,used_memory', '--format=csv,noheader,nounits']
                        gpu_result = subprocess.run(gpu_cmd, capture_output=True, text=True, timeout=5)
                    
                    if gpu_result.returncode == 0 and gpu_result.stdout.strip():
                        for line in gpu_result.stdout.strip().split('\n'):
                            if line.strip():
                                parts = [p.strip() for p in line.split(',')]
                                if len(parts) >= 2:
                                    try:
                                        gpu_pid = int(parts[0]) if parts[0].isdigit() else None
                                        if gpu_pid:
                                            # Get process name from psutil instead of nvidia-smi
                                            process_name = "unknown"
                                            job_id = None
                                            try:
                                                proc = psutil.Process(gpu_pid)
                                                process_name = proc.name()
                                                
                                                # Extract job-id from command line arguments
                                                # Look for --job-id argument in cmdline
                                                try:
                                                    cmdline = proc.cmdline()
                                                    for i, arg in enumerate(cmdline):
                                                        if arg == '--job-id' and i + 1 < len(cmdline):
                                                            job_id = cmdline[i + 1]
                                                            break
                                                except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
                                                    pass
                                                
                                                # Fallback: try environment variable
                                                if not job_id:
                                                    try:
                                                        env = proc.environ()
                                                        job_id = env.get('FEATRIX_JOB_ID')
                                                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                                                        pass
                                                
                                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                                pass
                                            
                                            # Skip Xorg - we don't want to show it in GPU processes
                                            if process_name.lower() in ['xorg', 'x']:
                                                continue
                                            
                                            # GPU utilization not available in --query-processes, set to 0
                                            gpu_percent = 0.0
                                            
                                            # Get memory usage from nvidia-smi
                                            mem_used_mb = 0.0
                                            gpu_vram_percent = 0.0
                                            gpu_vram_gb = 0.0
                                            if len(parts) >= 2:
                                                mem_used = float(parts[1]) if parts[1] != '[Not Supported]' else 0.0
                                                mem_used_mb = mem_used
                                                gpu_vram_gb = round(mem_used / 1024, 2)  # Convert MB to GB
                                                if mem_used > 0 and gpu_mem_total and gpu_mem_total > 0:
                                                    gpu_vram_percent = round((mem_used / gpu_mem_total) * 100, 1)
                                            
                                            gpu_stats_map[gpu_pid] = (gpu_percent, gpu_vram_percent, gpu_vram_gb)
                                            gpu_processes_list.append({
                                                "pid": gpu_pid,
                                                "name": process_name,
                                                "job_id": job_id,  # Add job_id for identification
                                                "gpu_percent": gpu_percent,
                                                "gpu_vram_percent": gpu_vram_percent,
                                                "memory_used_mb": round(mem_used_mb, 1)
                                            })
                                    except (ValueError, IndexError):
                                        continue
                except Exception:
                    pass  # GPU query is optional
                
                # Run supervisorctl status
                result = subprocess.run([supervisorctl_path, 'status'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout:
                    processes = []
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                name = parts[0]
                                state = parts[1]
                                pid = None
                                uptime = None
                                # Parse PID and uptime if available
                                if len(parts) >= 4 and parts[2] == 'pid':
                                    try:
                                        pid = int(parts[3].rstrip(','))
                                    except (ValueError, IndexError):
                                        pass
                                if len(parts) >= 6 and parts[4] == 'uptime':
                                    uptime = ' '.join(parts[5:])
                                
                                # Get CPU/memory for this process if we have PID
                                cpu_percent = None
                                memory_mb = None
                                memory_percent = None
                                memory_res_gb = None  # Resident Set Size (actual RAM used)
                                memory_vss_gb = None  # Virtual Set Size (total virtual memory)
                                if pid:
                                    try:
                                        proc = psutil.Process(pid)
                                        # CRITICAL: Use non-blocking cpu_percent() without interval
                                        # The interval parameter blocks for that duration, causing slow collection
                                        # Without interval, it uses cached value from previous call (non-blocking)
                                        cpu_percent = round(proc.cpu_percent(), 1)
                                        mem_info = proc.memory_info()
                                        memory_mb = round(mem_info.rss / (1024 * 1024), 1)
                                        memory_percent = round(proc.memory_percent(), 1)
                                        memory_res_gb = round(mem_info.rss / (1024 ** 3), 2)  # RES in GB
                                        memory_vss_gb = round(mem_info.vms / (1024 ** 3), 2)  # VSS in GB
                                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                                        pass
                                
                                # Collect child worker info (for celery, etc.)
                                children = []
                                gpu_percent = None
                                gpu_vram_percent = None
                                gpu_vram_gb = None
                                if pid:
                                    # Check direct PID match first
                                    if pid in gpu_stats_map:
                                        gpu_percent, gpu_vram_percent, gpu_vram_gb = gpu_stats_map[pid]
                                    
                                    # Get ALL child processes with their stats (for expandable worker lists)
                                    try:
                                        proc = psutil.Process(pid)
                                        for child in proc.children(recursive=True):
                                            child_cpu = None
                                            child_mem_mb = None
                                            child_mem_pct = None
                                            child_mem_res_gb = None
                                            child_mem_vss_gb = None
                                            child_gpu = None
                                            child_vram_pct = None
                                            child_vram_gb = None
                                            
                                            try:
                                                # Use non-blocking cpu_percent() for children too
                                                child_cpu = round(child.cpu_percent(), 1)
                                                child_mem_info = child.memory_info()
                                                child_mem_mb = round(child_mem_info.rss / (1024 * 1024), 1)
                                                child_mem_pct = round(child.memory_percent(), 1)
                                                child_mem_res_gb = round(child_mem_info.rss / (1024 ** 3), 2)
                                                child_mem_vss_gb = round(child_mem_info.vms / (1024 ** 3), 2)
                                                
                                                # Check GPU stats for this child
                                                if child.pid in gpu_stats_map:
                                                    child_gpu, child_vram_pct, child_vram_gb = gpu_stats_map[child.pid]
                                                    # If parent has no GPU but child does, use child's GPU stats for parent
                                                    if gpu_percent is None and child_gpu is not None:
                                                        gpu_percent, gpu_vram_percent, gpu_vram_gb = child_gpu, child_vram_pct, child_vram_gb
                                                
                                                # Get child process name/cmdline
                                                child_name = child.name()
                                                child_cmdline = ' '.join(child.cmdline()[:3]) if child.cmdline() else child_name
                                                
                                                children.append({
                                                    "pid": child.pid,
                                                    "name": child_name,
                                                    "cmdline": child_cmdline[:100],  # Truncate long commands
                                                    "cpu_percent": child_cpu,
                                                    "memory_mb": child_mem_mb,
                                                    "memory_percent": child_mem_pct,
                                                    "memory_res_gb": child_mem_res_gb,  # RES in GB
                                                    "memory_vss_gb": child_mem_vss_gb,  # VSS in GB
                                                    "gpu_percent": child_gpu,
                                                    "gpu_vram_percent": child_vram_pct,
                                                    "gpu_vram_gb": child_vram_gb,  # VRAM in GB
                                                })
                                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                                pass
                                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                                        pass
                                
                                processes.append({
                                    "name": name,
                                    "state": state,
                                    "pid": pid,
                                    "uptime": uptime,
                                    "cpu_percent": cpu_percent,
                                    "memory_mb": memory_mb,
                                    "memory_percent": memory_percent,
                                    "memory_res_gb": memory_res_gb,  # RES in GB (actual RAM)
                                    "memory_vss_gb": memory_vss_gb,  # VSS in GB (virtual memory)
                                    "gpu_percent": gpu_percent,
                                    "gpu_vram_percent": gpu_vram_percent,
                                    "gpu_vram_gb": gpu_vram_gb,  # VRAM in GB
                                    "children": children,  # Add child worker list for expandable UI
                                    "child_count": len(children),
                                })
                    
                    # GPU processes are now shown as children of their parent supervisor processes
                    # No need for separate gpu_processes list - already in children[]
                    supervisor_processes = {
                        "available": True,
                        "processes": processes,
                        "total_processes": len(processes),
                        "running_processes": len([p for p in processes if p['state'] == 'RUNNING']),
                    }
                else:
                    supervisor_processes = {"available": False, "error": "supervisorctl returned no data"}
            else:
                supervisor_processes = {"available": False, "error": "supervisorctl not found"}
        except Exception as e:
            supervisor_processes = {"error": str(e)}
            logger.error(f"❌ Failed to collect supervisor data: {e}")
        
        # Build health data
        health_data = {
            "timestamp": current_time,
            "gpu": gpu_info,
            "celery": celery_info,
            "jobs": job_queues,
            "version": version,
            "version_timestamp": version_timestamp,
            "git": git_info,
            "uptime_seconds": uptime_seconds,
            "system": system_info,
            "supervisor": supervisor_processes,
            "backplane": self.backplane_status.copy(),  # Include backplane rsync status
        }
        
        # Store in Redis with 90 second TTL (will be refreshed every 30 seconds)
        try:
            redis_key = "health:cache"
            health_json = json.dumps(health_data)
            redis_client.setex(redis_key, 90, health_json)
            logger.info(f"✅ Saved health data to Redis ({len(health_json)} bytes, TTL=90s)")
        except Exception as e:
            logger.error(f"❌ CRITICAL: Could not save health data to Redis: {e}")
            logger.error(f"   Redis key: {redis_key}")
            logger.error(f"   Data size: {len(json.dumps(health_data)) if health_data else 0} bytes")
            logger.error(f"   Traceback: {traceback.format_exc()}")

    def scan_existing_jobs(self):
        """Scan existing job directories to build initial known_jobs set."""
        try:
            output_dir = Path("/sphere/app/featrix_output")
            if not output_dir.exists():
                return
            
            for job_dir in output_dir.iterdir():
                if job_dir.is_dir():
                    job_name = job_dir.name
                    self.known_jobs.add(job_name)
                    
            logger.info(f"Loaded {len(self.known_jobs)} existing jobs")
            
        except Exception as e:
            logger.error(f"Error scanning existing jobs: {e}")

    def scan_for_job_events(self):
        """Scan for new job completions and record events."""
        try:
            output_dir = Path("/sphere/app/featrix_output")
            if not output_dir.exists():
                return
            
            current_jobs = set()
            new_completions = []
            
            for job_dir in output_dir.iterdir():
                if not job_dir.is_dir():
                    continue
                    
                job_name = job_dir.name
                current_jobs.add(job_name)
                
                # Skip if we've already processed this job
                if job_name in self.known_jobs:
                    continue
                
                # Parse job info
                job_parts = job_name.split('_')
                if len(job_parts) >= 3:
                    job_type = '_'.join(job_parts[:-2])
                    timestamp_str = job_parts[-2]
                    job_id = job_parts[-1]
                else:
                    job_type = "unknown"
                    job_id = job_name
                
                # Check if job has completed (has stdout.log)
                logs_dir = job_dir / "logs"
                stdout_log = logs_dir / "stdout.log"
                
                if stdout_log.exists():
                    # Job has produced output - record completion
                    try:
                        stat_info = stdout_log.stat()
                        log_size = stat_info.st_size
                        completion_time = datetime.fromtimestamp(stat_info.st_mtime, timezone.utc).isoformat()
                        
                        # Try to determine session ID from job directory structure
                        session_id = self.extract_session_id(job_dir)
                        
                        # Calculate runtime (rough estimate from directory creation to log modification)
                        job_creation_time = job_dir.stat().st_ctime
                        log_modification_time = stat_info.st_mtime
                        runtime_seconds = log_modification_time - job_creation_time
                        
                        new_completions.append({
                            'job_id': job_name,
                            'job_type': job_type,
                            'session_id': session_id,
                            'event_type': 'completed',
                            'timestamp': completion_time,
                            'runtime_seconds': runtime_seconds,
                            'log_file_size': log_size,
                            'working_directory': str(job_dir),
                            'cpu_time_user': None,  # Could parse from logs if needed
                            'cpu_time_system': None,
                            'peak_memory_mb': None,
                            'exit_code': None
                        })
                        
                    except Exception as e:
                        logger.error(f"Error processing job {job_name}: {e}")
            
            # Record new completions
            if new_completions:
                with sqlite3.connect(self.db_path) as conn:
                    for completion in new_completions:
                        conn.execute("""
                            INSERT INTO job_events 
                            (job_id, job_type, session_id, event_type, timestamp, 
                             runtime_seconds, log_file_size, working_directory, 
                             cpu_time_user, cpu_time_system, peak_memory_mb, exit_code)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            completion['job_id'],
                            completion['job_type'], 
                            completion['session_id'],
                            completion['event_type'],
                            completion['timestamp'],
                            completion['runtime_seconds'],
                            completion['log_file_size'],
                            completion['working_directory'],
                            completion['cpu_time_user'],
                            completion['cpu_time_system'],
                            completion['peak_memory_mb'],
                            completion['exit_code']
                        ))
                    conn.commit()
                
                logger.info(f"📝 Recorded {len(new_completions)} new job completions")
                for completion in new_completions:
                    logger.info(f"   ✅ {completion['job_type']} {completion['job_id'][:8]} ({completion['runtime_seconds']:.1f}s)")
            
            # Update known jobs
            self.known_jobs = current_jobs
            
        except Exception as e:
            logger.error(f"Error scanning for job events: {e}")

    def extract_session_id(self, job_dir: Path) -> Optional[str]:
        """Try to extract session ID from job directory or associated files."""
        try:
            # Look for session information in job directory
            # This is a best-effort attempt - might need refinement
            
            job_name = job_dir.name
            job_parts = job_name.split('_')
            
            if len(job_parts) >= 3:
                timestamp_str = job_parts[-2]
                job_id = job_parts[-1]
                
                # Session ID often follows pattern: YYYYMMDD-HHMMSS_jobid
                potential_session_id = f"{timestamp_str}_{job_id}"
                return potential_session_id
            
            return None
            
        except Exception:
            return None

    def calculate_job_resource_usage(self):
        """Calculate resource usage statistics for completed jobs."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Find jobs that have completed but don't have resource usage calculated
                cursor = conn.execute("""
                    SELECT DISTINCT je.job_id, je.timestamp as completed_at
                    FROM job_events je
                    LEFT JOIN job_resource_usage jru ON je.job_id = jru.job_id
                    WHERE je.event_type = 'completed' 
                    AND jru.job_id IS NULL
                    AND je.timestamp > datetime('now', '-24 hours')
                """)
                
                uncalculated_jobs = cursor.fetchall()
                
                for job_id, completed_at in uncalculated_jobs:
                    # Calculate resource usage for this job
                    # Look for metrics during job runtime (rough estimate)
                    completed_dt = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                    
                    # Estimate start time (this is rough - could be improved)
                    start_time = completed_dt.replace(microsecond=0) - timedelta(hours=2)  # Assume max 2 hour jobs
                    
                    # Query metrics during this timeframe
                    metrics_cursor = conn.execute("""
                        SELECT cpu_percent, memory_percent, gpu_utilization, gpu_memory_percent
                        FROM system_metrics
                        WHERE timestamp BETWEEN ? AND ?
                        AND cpu_percent IS NOT NULL
                    """, (start_time.isoformat(), completed_at))
                    
                    metrics_data = metrics_cursor.fetchall()
                    
                    if metrics_data:
                        # Calculate averages and maximums
                        cpu_values = [m[0] for m in metrics_data if m[0] is not None]
                        memory_values = [m[1] for m in metrics_data if m[1] is not None]
                        
                        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else None
                        max_cpu = max(cpu_values) if cpu_values else None
                        avg_memory = sum(memory_values) / len(memory_values) if memory_values else None
                        max_memory = max(memory_values) if memory_values else None
                        
                        # GPU calculations (more complex due to JSON arrays)
                        gpu_utils = []
                        gpu_mems = []
                        
                        for m in metrics_data:
                            if m[2]:  # gpu_utilization
                                try:
                                    utils = json.loads(m[2])
                                    if utils:
                                        gpu_utils.extend(utils)
                                except:
                                    pass
                                    
                            if m[3]:  # gpu_memory_percent
                                try:
                                    mems = json.loads(m[3])
                                    if mems:
                                        gpu_mems.extend(mems)
                                except:
                                    pass
                        
                        avg_gpu_util = sum(gpu_utils) / len(gpu_utils) if gpu_utils else None
                        max_gpu_util = max(gpu_utils) if gpu_utils else None
                        avg_gpu_mem = sum(gpu_mems) / len(gpu_mems) if gpu_mems else None
                        max_gpu_mem = max(gpu_mems) if gpu_mems else None
                        
                        # Store resource usage summary
                        conn.execute("""
                            INSERT INTO job_resource_usage 
                            (job_id, started_at, completed_at, avg_cpu_percent, max_cpu_percent,
                             avg_memory_percent, max_memory_percent, avg_gpu_utilization, 
                             max_gpu_utilization, avg_gpu_memory_percent, max_gpu_memory_percent)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            job_id, start_time.isoformat(), completed_at,
                            avg_cpu, max_cpu, avg_memory, max_memory,
                            json.dumps([avg_gpu_util]) if avg_gpu_util else None,
                            json.dumps([max_gpu_util]) if max_gpu_util else None,
                            json.dumps([avg_gpu_mem]) if avg_gpu_mem else None,
                            json.dumps([max_gpu_mem]) if max_gpu_mem else None
                        ))
                
                conn.commit()
                
                if uncalculated_jobs:
                    logger.info(f"📈 Calculated resource usage for {len(uncalculated_jobs)} jobs")
                    
        except Exception as e:
            logger.error(f"Error calculating job resource usage: {e}")

    def cleanup_old_data(self):
        """Clean up old monitoring data to prevent database bloat."""
        try:
            cutoff_days = 7  # Keep 7 days of detailed metrics
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=cutoff_days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Keep job events and resource usage longer (30 days)
                job_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
                
                # Clean old system metrics
                cursor = conn.execute(
                    "DELETE FROM system_metrics WHERE timestamp < ?",
                    (cutoff_date.isoformat(),)
                )
                metrics_deleted = cursor.rowcount
                
                # Clean old job events  
                cursor = conn.execute(
                    "DELETE FROM job_events WHERE timestamp < ?",
                    (job_cutoff.isoformat(),)
                )
                jobs_deleted = cursor.rowcount
                
                conn.commit()
                
                if metrics_deleted > 0 or jobs_deleted > 0:
                    logger.info(f"🧹 Cleaned up {metrics_deleted} old metrics, {jobs_deleted} old job events")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")

    def check_backplane(self):
        """Check backplane mount, directory, rsync, and disk space."""
        import subprocess
        import shutil
        
        current_time = time.time()
        
        # Check if it's time to run backplane checks (every 2 minutes)
        if current_time - self.last_backplane_check < self.backplane_check_interval:
            return
        
        # CRITICAL: Don't run if previous rsync is still running
        if self.backplane_rsync_running:
            logger.debug("Backplane rsync already running, skipping this interval")
            return
        
        self.last_backplane_check = current_time
        
        backplane_path = Path("/backplane/backplane1")
        hostname = socket.gethostname()
        host_backup_path = backplane_path / "sphere" / f"host-{hostname}"
        sphere_path = Path("/sphere")
        
        try:
            # 1. Check that /backplane/backplane1/ is mounted and is an NFS filesystem
            if not backplane_path.exists():
                logger.error(f"❌ Backplane path does not exist: {backplane_path}")
                return
            
            # Check filesystem type using findmnt or mount
            try:
                result = subprocess.run(
                    ["findmnt", "-n", "-o", "FSTYPE", str(backplane_path)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    fstype = result.stdout.strip()
                    if fstype != "nfs" and fstype != "nfs4":
                        logger.error(f"❌ Backplane is not NFS filesystem (type: {fstype})")
                        return
                    logger.debug(f"✅ Backplane is NFS filesystem: {fstype}")
                else:
                    # Fallback: check /proc/mounts
                    with open("/proc/mounts", "r") as f:
                        for line in f:
                            parts = line.split()
                            if len(parts) >= 3 and parts[1] == str(backplane_path):
                                fstype = parts[2]
                                if fstype not in ["nfs", "nfs4"]:
                                    logger.error(f"❌ Backplane is not NFS filesystem (type: {fstype})")
                                    return
                                logger.debug(f"✅ Backplane is NFS filesystem: {fstype}")
                                break
                        else:
                            logger.error(f"❌ Backplane path not found in /proc/mounts")
                            return
            except Exception as e:
                logger.warning(f"⚠️  Could not verify NFS filesystem type: {e}")
            
            # 2. Ensure /backplane/backplane1/sphere/host-<hostname> exists
            host_backup_path.mkdir(parents=True, exist_ok=True)
            if not host_backup_path.exists():
                logger.error(f"❌ Could not create host backup directory: {host_backup_path}")
                return
            logger.debug(f"✅ Host backup directory exists: {host_backup_path}")
            
            # 3. rsync -a --ignore-existing /sphere to /backplane/backplane1/sphere/host-<hostname>/
            try:
                logger.info(f"🔄 Starting rsync backup to {host_backup_path}...")
                rsync_cmd = [
                    "rsync",
                    "-a",  # archive mode
                    "--ignore-existing",  # skip files that already exist
                    f"{sphere_path}/",
                    f"{host_backup_path}/"
                ]
                result = subprocess.run(
                    rsync_cmd,
                    capture_output=True,
                    text=True,
                    timeout=1800  # 30 minute timeout
                )
                if result.returncode == 0:
                    logger.info(f"✅ Rsync backup completed successfully")
                else:
                    logger.error(f"❌ Rsync backup failed with exit code {result.returncode}")
                    logger.error(f"   stderr: {result.stderr[:500]}")
            except subprocess.TimeoutExpired:
                logger.error(f"❌ Rsync backup timed out after 30 minutes")
            except Exception as e:
                logger.error(f"❌ Rsync backup error: {e}")
            
            # 4. Make sure /backplane is not running low on space
            try:
                stat = shutil.disk_usage(backplane_path)
                total_gb = stat.total / (1024 ** 3)
                free_gb = stat.free / (1024 ** 3)
                used_gb = stat.used / (1024 ** 3)
                free_percent = (stat.free / stat.total) * 100
                
                logger.debug(f"📊 Backplane disk usage: {used_gb:.1f}GB / {total_gb:.1f}GB used, {free_gb:.1f}GB free ({free_percent:.1f}%)")
                
                if free_percent < 10:
                    logger.error(f"❌ Backplane disk space critical: {free_percent:.1f}% free ({free_gb:.1f}GB remaining)")
                elif free_percent < 20:
                    logger.warning(f"⚠️  Backplane disk space low: {free_percent:.1f}% free ({free_gb:.1f}GB remaining)")
                else:
                    logger.debug(f"✅ Backplane disk space OK: {free_percent:.1f}% free")
            except Exception as e:
                logger.error(f"❌ Could not check backplane disk space: {e}")
            
            # 5. Check /sphere disk space and delete MARKED_FOR_DELETE sessions if < 25% free
            try:
                sphere_stat = shutil.disk_usage(sphere_path)
                sphere_total_gb = sphere_stat.total / (1024 ** 3)
                sphere_free_gb = sphere_stat.free / (1024 ** 3)
                sphere_used_gb = sphere_stat.used / (1024 ** 3)
                sphere_free_percent = (sphere_stat.free / sphere_stat.total) * 100
                
                logger.debug(f"📊 /sphere disk usage: {sphere_used_gb:.1f}GB / {sphere_total_gb:.1f}GB used, {sphere_free_gb:.1f}GB free ({sphere_free_percent:.1f}%)")
                
                if sphere_free_percent < 25.0:
                    logger.warning(f"⚠️  /sphere disk space low: {sphere_free_percent:.1f}% free ({sphere_free_gb:.1f}GB remaining)")
                    logger.info(f"🗑️  Starting cleanup of MARKED_FOR_DELETE sessions...")
                    
                    # Find and delete sessions with MARKED_FOR_DELETE marker
                    session_dir = Path("/sphere/app/featrix_sessions")
                    job_output_dir = Path("/sphere/app/featrix_output")
                    marker_file = "MARKED_FOR_DELETE"
                    
                    if session_dir.exists():
                        deleted_count = 0
                        for session_file in session_dir.glob("*.session"):
                            session_id = session_file.stem
                            marker_path = session_file.parent / marker_file
                            
                            # Check if marker exists
                            if marker_path.exists():
                                logger.info(f"🗑️  Found MARKED_FOR_DELETE session: {session_id}")
                                
                                try:
                                    # Try to delete associated job directories
                                    try:
                                        with open(session_file, 'r') as f:
                                            session_data = json.load(f)
                                        
                                        job_plan = session_data.get("job_plan", [])
                                        for job in job_plan:
                                            job_id = job.get("job_id")
                                            if job_id:
                                                job_dir = job_output_dir / job_id
                                                if job_dir.exists():
                                                    logger.info(f"   Deleting associated job directory: {job_id}")
                                                    try:
                                                        shutil.rmtree(job_dir)
                                                    except Exception as e:
                                                        logger.warning(f"   Failed to delete job directory {job_id}: {e}")
                                    except Exception as e:
                                        logger.debug(f"   Could not read session file to find associated jobs: {e}")
                                    
                                    # Delete session file
                                    logger.info(f"   Deleting session: {session_id}")
                                    session_file.unlink()
                                    
                                    # Delete marker file
                                    if marker_path.exists():
                                        try:
                                            marker_path.unlink()
                                        except Exception:
                                            pass
                                    
                                    deleted_count += 1
                                    logger.info(f"✅ Deleted session {session_id}")
                                    
                                    # Recheck disk space after deletion
                                    sphere_stat = shutil.disk_usage(sphere_path)
                                    sphere_free_percent = (sphere_stat.free / sphere_stat.total) * 100
                                    
                                    # Stop if we've freed enough space (above 25%)
                                    if sphere_free_percent >= 25.0:
                                        logger.info(f"✅ Disk space now at {sphere_free_percent:.1f}% - stopping cleanup")
                                        break
                                        
                                except Exception as e:
                                    logger.error(f"❌ Failed to delete session {session_id}: {e}")
                        
                        if deleted_count > 0:
                            logger.info(f"✅ Cleanup complete: deleted {deleted_count} MARKED_FOR_DELETE session(s)")
                        else:
                            logger.info(f"ℹ️  No MARKED_FOR_DELETE sessions found to delete")
                    else:
                        logger.warning(f"⚠️  Session directory does not exist: {session_dir}")
                else:
                    logger.debug(f"✅ /sphere disk space OK: {sphere_free_percent:.1f}% free")
            except Exception as e:
                logger.error(f"❌ Could not check /sphere disk space or delete sessions: {e}")
        except Exception as e:
            logger.error(f"❌ Backplane check error: {e}", exc_info=True)
    
    def process_api_retries(self):
        """Process pending API events in the retry queue."""
        current_time = time.time()
        
        # Check if it's time to process retries (every minute)
        if current_time - self.last_retry_process < self.retry_process_interval:
            return
        
        self.last_retry_process = current_time
        
        try:
            from lib.api_event_retry import get_retry_manager
            retry_manager = get_retry_manager()
            
            # Process up to 50 events per cycle
            stats = retry_manager.process_retry_queue(max_events=50)
            
            if stats["processed"] > 0:
                logger.info(f"📤 API retry queue: {stats['processed']} processed, {stats['succeeded']} succeeded, {stats['retried']} retried, {stats['failed']} failed")
            
            # Cleanup old events (once per hour)
            if current_time % 3600 < self.retry_process_interval:
                retry_manager.cleanup_old_events()
                
        except ImportError:
            # API retry module not available - skip
            pass
        except Exception as e:
            logger.warning(f"⚠️  Error processing API retries: {e}")
            import traceback
            logger.debug(f"   Traceback: {traceback.format_exc()}")
                
    def run(self):
        """Main monitoring loop."""
        import socket
        hostname = socket.gethostname()
        logger.info("=" * 80)
        logger.info(f"🚀 SYSTEM MONITOR STARTING - {datetime.now(timezone.utc).isoformat()}")
        logger.info("=" * 80)
        logger.info(f"Hostname: {hostname}")
        logger.info(f"Polling interval: {self.poll_interval} seconds")
        logger.info(f"Database: {self.db_path}")
        logger.info(f"Traceback monitor: {'enabled' if self.traceback_monitor else 'disabled'}")
        logger.info("=" * 80)
        
        cleanup_counter = 0
        
        try:
            while True:
                start_time = time.time()
                
                # Collect system metrics
                self.collect_system_metrics()
                
                # Collect and cache health data for /health endpoint (every 30 seconds)
                current_time = time.time()
                if current_time - self.last_health_collection >= self.health_collection_interval:
                    self.collect_health_data()
                    self.last_health_collection = current_time
                
                # Scan for job events (every cycle)
                self.scan_for_job_events()
                
                # Calculate job resource usage (every 5 cycles)
                if cleanup_counter % 5 == 0:
                    self.calculate_job_resource_usage()
                
                # Check backplane (every 15 minutes)
                self.check_backplane()
                
                # Process API retry queue (every minute)
                self.process_api_retries()
                
                # Cleanup old data (every 100 cycles - roughly every 30 minutes)
                if cleanup_counter % 100 == 0:
                    self.cleanup_old_data()
                
                cleanup_counter += 1
                
                # Sleep for remaining time in polling interval
                elapsed = time.time() - start_time
                sleep_time = max(0, self.poll_interval - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    logger.warning(f"Monitoring cycle took {elapsed:.1f}s (longer than {self.poll_interval}s interval)")
                    
        except KeyboardInterrupt:
            logger.info("🛑 Monitor stopped by user")
        except Exception as e:
            logger.error(f"💥 Monitor crashed: {e}")
            raise
        finally:
            if self.traceback_monitor:
                self.traceback_monitor.stop()

def main():
    """Main entry point."""
    # Install Featrix exception hook for better error tracking
    try:
        from lib.featrix_debug import install_featrix_excepthook
        install_featrix_excepthook()
    except Exception:
        pass  # Don't fail if debug module not available
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Featrix System Resource Monitor")
    parser.add_argument('--interval', type=int, default=20, 
                       help='Polling interval in seconds (default: 20)')
    parser.add_argument('--db-path', default='/sphere/app/system_monitor.db',
                       help='Database path (default: /sphere/app/system_monitor.db)')
    parser.add_argument('--query', action='store_true',
                       help='Query recent data instead of running monitor')
    parser.add_argument('--no-traceback-monitor', action='store_true',
                       help='Disable traceback monitoring')
    
    args = parser.parse_args()
    
    if args.query:
        # Quick query mode for testing
        monitor = SystemMonitor(db_path=args.db_path, poll_interval=args.interval)
        
        with sqlite3.connect(args.db_path) as conn:
            # Show recent metrics
            cursor = conn.execute("""
                SELECT timestamp, cpu_percent, memory_percent, gpu_utilization
                FROM system_metrics 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            
            print("Recent system metrics:")
            for row in cursor.fetchall():
                timestamp, cpu, memory, gpu = row
                gpu_info = ""
                if gpu:
                    try:
                        gpu_data = json.loads(gpu)
                        if gpu_data:
                            gpu_info = f"GPU: {gpu_data[0]:.1f}%"
                    except:
                        gpu_info = "GPU: N/A"
                
                print(f"  {timestamp}: CPU {cpu:.1f}%, RAM {memory:.1f}%, {gpu_info}")
            
            # Show recent job completions
            cursor = conn.execute("""
                SELECT job_id, job_type, timestamp, runtime_seconds
                FROM job_events
                WHERE event_type = 'completed'
                ORDER BY timestamp DESC
                LIMIT 5
            """)
            
            print("\nRecent job completions:")
            for row in cursor.fetchall():
                job_id, job_type, timestamp, runtime = row
                print(f"  {timestamp}: {job_type} {job_id[:16]} ({runtime:.1f}s)")
    else:
        # Normal monitoring mode
        monitor = SystemMonitor(
            db_path=args.db_path, 
            poll_interval=args.interval,
            enable_traceback_monitor=not args.no_traceback_monitor
        )
        monitor.run()

if __name__ == "__main__":
    # Handle missing dependencies gracefully
    try:
        from datetime import timedelta
    except ImportError:
        print("Missing required dependencies. Install with: pip install psutil")
        exit(1)
        
    main() 