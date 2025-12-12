#!/usr/bin/env python3
"""
Featrix Training Watchdog
Monitors training jobs for stuck conditions:
- GPU RAM full (>95%)
- CPU/GPU utilization low (<10%)
- No epoch progress for extended period

If all conditions are met, restarts worker-train_es via supervisorctl.
"""

import argparse
import json
import logging
import os
import re
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Add src to path for imports
src_path = Path(__file__).parent
if str(src_path.resolve()) not in sys.path:
    sys.path.insert(0, str(src_path.resolve()))

try:
    from config import config
    from lib.job_manager import JobStatus
    from lib.job_manager import load_job
    from slack import send_slack_message
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

# Try to import requests for pinging sphere-api
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.warning("requests not available - cannot ping sphere-api")


class TrainingWatchdog:
    def __init__(self, check_interval: int = 60, stuck_threshold: int = 300):
        """
        Initialize the training watchdog.
        
        Args:
            check_interval: How often to check for stuck jobs (seconds)
            stuck_threshold: How long without epoch progress before considering stuck (seconds)
        """
        self.check_interval = check_interval
        self.stuck_threshold = stuck_threshold
        self.last_epoch_check: Dict[str, Tuple[int, float]] = {}  # job_id -> (epoch, timestamp)
        self.last_restart_time: Dict[str, float] = {}  # job_id -> timestamp of last restart
        self.last_announce_time = 0.0  # Last time we pinged sphere-api
        self.announce_interval = 30  # Ping sphere-api every 30 seconds
        self.last_slack_notification: Dict[str, float] = {}  # issue_type -> timestamp of last Slack notification
        self.slack_notification_interval = 900  # 15 minutes in seconds
        
        # Get node name from hostname
        try:
            hostname = socket.gethostname()
            hostname_lower = hostname.lower()
            # Map hostname to node name (e.g., "taco", "churro", "burrito")
            # Hostname mappings for nodes with IP-based hostnames
            if 'taco' in hostname_lower:
                self.node_name = 'taco'
            elif 'churro' in hostname_lower:
                self.node_name = 'churro'
            elif 'burrito' in hostname_lower:
                self.node_name = 'burrito'
            else:
                self.node_name = hostname.split('.')[0]  # Use first part of hostname
        except Exception:
            self.node_name = 'unknown'
        
        logger.info(f"Training watchdog initialized")
        logger.info(f"  Check interval: {check_interval}s")
        logger.info(f"  Stuck threshold: {stuck_threshold}s")
        logger.info(f"  Node name: {self.node_name}")

    def get_gpu_stats(self) -> Optional[Dict]:
        """Get GPU memory and utilization stats using nvidia-smi."""
        try:
            cmd = [
                'nvidia-smi',
                '--query-gpu=utilization.gpu,memory.used,memory.total',
                '--format=csv,noheader,nounits'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                logger.debug("nvidia-smi command failed - GPU stats not available")
                return None
            
            lines = result.stdout.strip().split('\n')
            if not lines or not lines[0]:
                return None
            
            # Get first GPU stats (or average if multiple)
            parts = [p.strip() for p in lines[0].split(',')]
            if len(parts) >= 3:
                gpu_util = float(parts[0]) if parts[0] != '[Not Supported]' else 0.0
                mem_used = float(parts[1])
                mem_total = float(parts[2])
                mem_percent = (mem_used / mem_total * 100) if mem_total > 0 else 0
                
                return {
                    'gpu_utilization': gpu_util,
                    'memory_used_mb': mem_used,
                    'memory_total_mb': mem_total,
                    'memory_percent': mem_percent
                }
        except FileNotFoundError:
            logger.debug("nvidia-smi not found - GPU monitoring disabled")
            return None
        except Exception as e:
            logger.debug(f"Error getting GPU stats: {e}")
            return None
        
        return None

    def get_cpu_stats(self) -> Optional[Dict]:
        """Get CPU utilization stats using psutil."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            return {
                'cpu_percent': cpu_percent
            }
        except ImportError:
            logger.debug("psutil not available - CPU monitoring disabled")
            return None
        except Exception as e:
            logger.debug(f"Error getting CPU stats: {e}")
            return None

    def get_latest_epoch(self, job_output_dir: Path) -> Optional[int]:
        """Get the latest epoch number from checkpoint files."""
        try:
            checkpoint_files = list(job_output_dir.glob("training_state_e-*.pth"))
            if not checkpoint_files:
                return None
            
            latest_epoch = -1
            for checkpoint_file in checkpoint_files:
                # Extract epoch from filename like "training_state_e-42.pth"
                match = re.search(r'training_state_e-(\d+)\.pth', checkpoint_file.name)
                if match:
                    epoch = int(match.group(1))
                    if epoch > latest_epoch:
                        latest_epoch = epoch
            
            return latest_epoch if latest_epoch >= 0 else None
        except Exception as e:
            logger.debug(f"Error getting latest epoch from {job_output_dir}: {e}")
            return None

    def get_worker_train_es_pids(self) -> list:
        """Get PIDs of worker-train_es processes."""
        pids = []
        try:
            result = subprocess.run(
                ['supervisorctl', 'status', 'worker-train_es'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Parse PID from output like "worker-train_es RUNNING pid 12345, uptime 1:23:45"
                for line in result.stdout.split('\n'):
                    if 'pid' in line.lower():
                        import re
                        match = re.search(r'pid\s+(\d+)', line)
                        if match:
                            pids.append(int(match.group(1)))
        except Exception as e:
            logger.debug(f"Error getting worker-train_es PIDs: {e}")
        return pids

    def find_orphaned_multiprocess_workers(self) -> list:
        """
        Find orphaned multiprocessing processes that don't belong to current worker-train_es.
        Detects both pt_data_worker processes and multiprocessing spawn/resource_tracker processes.
        
        Returns:
            List of (pid, ppid, reason) tuples for orphaned workers
        """
        orphaned = []
        try:
            import psutil
            
            # Get current worker-train_es PIDs and their process groups
            worker_pids = self.get_worker_train_es_pids()
            worker_pgids = set()
            worker_children = set()
            
            for worker_pid in worker_pids:
                try:
                    worker_proc = psutil.Process(worker_pid)
                    # pgid is a property, not a method
                    try:
                        pgid = worker_proc.pgid
                        worker_pgids.add(pgid)
                    except AttributeError:
                        # Fallback: try to get pgid from process info
                        try:
                            proc_info = worker_proc.as_dict(['pgid'])
                            if 'pgid' in proc_info:
                                worker_pgids.add(proc_info['pgid'])
                        except (AttributeError, KeyError):
                            logger.debug(f"Could not get pgid for process {worker_pid}")
                    # Get all descendants
                    for child in worker_proc.children(recursive=True):
                        worker_children.add(child.pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Find all orphaned multiprocessing processes
            # Use safer pattern: iterate without pre-fetching pgid, get it per-process
            # This avoids exceptions from transient/unreadable processes during iteration
            attrs = ['pid', 'ppid', 'name', 'cmdline']
            proc_iter = psutil.process_iter(attrs)
            
            for proc in proc_iter:
                try:
                    proc_info = proc.info
                    cmdline = ' '.join(proc_info.get('cmdline', [])).lower()
                    
                    # Check if it's a multiprocessing-related process
                    is_pt_worker = 'pt_data_worker' in cmdline or proc_info.get('name', '').lower() == 'pt_data_worker'
                    is_multiprocessing_spawn = 'multiprocessing.spawn' in cmdline and 'spawn_main' in cmdline
                    is_multiprocessing_tracker = 'multiprocessing.resource_tracker' in cmdline and 'main' in cmdline
                    
                    if is_pt_worker or is_multiprocessing_spawn or is_multiprocessing_tracker:
                        pid = proc_info['pid']
                        ppid = proc_info['ppid']
                        
                        # Get pgid per-process with exception handling (safer than pre-fetching)
                        # This avoids exceptions from transient/unreadable processes during iteration
                        pgid = None
                        try:
                            pgid = proc.pgid  # pgid is a property, not a method
                        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                            # pgid not available for this process or on this platform
                            pass
                        
                        # Check if it belongs to current worker
                        if pid in worker_children:
                            continue  # Legitimate child process
                        
                        # Check pgid if we successfully got it
                        if pgid is not None and pgid in worker_pgids:
                            continue  # Same process group as worker
                        
                        # Check parent
                        try:
                            parent = psutil.Process(ppid)
                            parent_cmdline = ' '.join(parent.cmdline() if parent.cmdline() else [])
                            
                            # If parent is not a current worker, it's orphaned
                            if ppid not in worker_pids and 'watch-queue' not in parent_cmdline.lower():
                                process_type = "multiprocessing spawn" if is_multiprocessing_spawn else ("multiprocessing tracker" if is_multiprocessing_tracker else "pt_data_worker")
                                orphaned.append((pid, ppid, f"Orphaned {process_type} - parent {ppid} is not worker-train_es"))
                            elif ppid not in worker_pids:
                                # Parent might be a dead Python process
                                process_type = "multiprocessing spawn" if is_multiprocessing_spawn else ("multiprocessing tracker" if is_multiprocessing_tracker else "pt_data_worker")
                                orphaned.append((pid, ppid, f"Orphaned {process_type} from dead parent {ppid}"))
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            # Parent is gone - definitely orphaned
                            process_type = "multiprocessing spawn" if is_multiprocessing_spawn else ("multiprocessing tracker" if is_multiprocessing_tracker else "pt_data_worker")
                            orphaned.append((pid, ppid, f"Orphaned {process_type} - parent process no longer exists"))
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except ImportError:
            logger.warning("psutil not available - cannot find orphaned workers")
        except Exception as e:
            # Don't log pgid-related errors as errors - they're expected on some platforms
            error_msg = str(e).lower()
            if 'pgid' in error_msg and ('invalid attr' in error_msg or 'invalid attribute' in error_msg):
                logger.debug(f"pgid not available on this platform: {e}")
            else:
                logger.error(f"Error finding orphaned workers: {e}")
        
        return orphaned

    def kill_orphaned_workers(self, orphaned: list) -> int:
        """Kill orphaned multiprocess workers."""
        killed_count = 0
        for pid, ppid, reason in orphaned:
            try:
                import psutil
                proc = psutil.Process(pid)
                logger.warning(f"🔪 Killing orphaned process PID {pid} ({reason})")
                proc.kill()
                killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Already gone or can't access
                pass
            except Exception as e:
                logger.debug(f"Error killing PID {pid}: {e}")
        
        return killed_count

    def send_slack_notification(self, issue_type: str, message: str) -> bool:
        """
        Send Slack notification with rate limiting (max once per 15 minutes per issue type).
        
        Args:
            issue_type: Type of issue (e.g., "orphaned_workers", "gpu_ram_full", "worker_restart")
            message: Message to send to Slack
            
        Returns:
            bool: True if message was sent, False if throttled
        """
        current_time = time.time()
        
        # Check if we've sent this type of notification recently
        if issue_type in self.last_slack_notification:
            time_since_last = current_time - self.last_slack_notification[issue_type]
            if time_since_last < self.slack_notification_interval:
                logger.debug(f"⏸️  Slack notification throttled for {issue_type} (last sent {int(time_since_last)}s ago)")
                return False
        
        # Send notification
        try:
            slack_msg = f"🐕 Watchdog Alert ({self.node_name}): {message}"
            success = send_slack_message(slack_msg, throttle=True, skip_hostname_prefix=True)
            if success:
                self.last_slack_notification[issue_type] = current_time
                logger.info(f"📢 Sent Slack notification for {issue_type}")
                return True
            else:
                logger.debug(f"⚠️  Failed to send Slack notification for {issue_type}")
                return False
        except Exception as e:
            logger.warning(f"⚠️  Error sending Slack notification: {e}")
            return False

    def restart_worker_train_es(self, reason_key: str, reason: str) -> bool:
        """Restart worker-train_es via supervisorctl."""
        return self.restart_training_workers(reason_key, reason, workers=['worker-train_es'])
    
    def restart_training_workers(self, reason_key: str, reason: str, workers: list = None) -> bool:
        """Restart training workers via supervisorctl. Defaults to both train_es and train_single_predictor."""
        if workers is None:
            workers = ['worker-train_es', 'worker-train_single_predictor']
        
        current_time = time.time()
        
        # Prevent restart spam - only restart once per 5 minutes
        if reason_key in self.last_restart_time:
            time_since_restart = current_time - self.last_restart_time[reason_key]
            if time_since_restart < 300:  # 5 minutes
                logger.warning(f"⏸️  Skipping restart - last restart was {int(time_since_restart)}s ago")
                return False
        
        all_succeeded = True
        for worker in workers:
            try:
                logger.warning(f"🔄 Restarting {worker}")
                logger.warning(f"   Reason: {reason}")
                
                result = subprocess.run(
                    ['supervisorctl', 'restart', worker],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    logger.info(f"✅ Successfully restarted {worker}")
                else:
                    logger.error(f"❌ Failed to restart {worker}: {result.stderr}")
                    all_succeeded = False
            except Exception as e:
                logger.error(f"❌ Error restarting {worker}: {e}")
                all_succeeded = False
        
        if all_succeeded:
            self.last_restart_time[reason_key] = current_time
            
            # Send Slack notification about worker restart
            workers_str = ', '.join(workers)
            self.send_slack_notification(
                "worker_restart",
                f"Restarted {workers_str}. Reason: {reason}"
            )
            
            return True
        else:
            # Send Slack notification about failed restart
            workers_str = ', '.join(workers)
            self.send_slack_notification(
                "worker_restart_failed",
                f"Failed to restart some workers ({workers_str}). Reason: {reason}"
            )
            return False

    def cleanup_old_orphaned_processes(self, max_age_seconds: int = 3600) -> int:
        """
        Proactively find and kill very old orphaned multiprocessing processes.
        This runs regardless of GPU RAM usage to prevent accumulation of orphaned processes.
        
        Args:
            max_age_seconds: Maximum age in seconds before considering a process old (default: 1 hour)
            
        Returns:
            Number of processes killed
        """
        try:
            import psutil
            orphaned = self.find_orphaned_multiprocess_workers()
            
            if not orphaned:
                return 0
            
            # Filter to only very old processes
            old_orphaned = []
            current_time = time.time()
            
            for pid, ppid, reason in orphaned:
                try:
                    proc = psutil.Process(pid)
                    # Get process creation time
                    create_time = proc.create_time()
                    age_seconds = current_time - create_time
                    
                    if age_seconds > max_age_seconds:
                        old_orphaned.append((pid, ppid, reason, age_seconds))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if old_orphaned:
                logger.warning(f"🔍 Found {len(old_orphaned)} very old orphaned process(es) (> {max_age_seconds}s old)")
                killed_count = 0
                for pid, ppid, reason, age_seconds in old_orphaned:
                    try:
                        proc = psutil.Process(pid)
                        age_hours = age_seconds / 3600
                        logger.warning(f"🔪 Killing very old orphaned process PID {pid} (age: {age_hours:.1f} hours, {reason})")
                        proc.kill()
                        killed_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    except Exception as e:
                        logger.debug(f"Error killing old orphaned PID {pid}: {e}")
                
                if killed_count > 0:
                    logger.info(f"✅ Killed {killed_count} very old orphaned process(es)")
                    # Send Slack notification if we killed a significant number
                    if killed_count >= 5:
                        self.send_slack_notification(
                            "orphaned_workers_cleanup",
                            f"Cleaned up {killed_count} very old orphaned multiprocessing processes (> {max_age_seconds}s old)"
                        )
                
                return killed_count
            
            return 0
        except Exception as e:
            logger.debug(f"Error in cleanup_old_orphaned_processes: {e}")
            return 0

    def check_and_restart_if_needed(self):
        """Main check loop - monitors GPU RAM and kills orphaned multiprocess workers."""
        # First, proactively clean up very old orphaned processes (regardless of GPU RAM)
        self.cleanup_old_orphaned_processes(max_age_seconds=3600)  # 1 hour
        
        # Get GPU stats
        gpu_stats = self.get_gpu_stats()
        
        if not gpu_stats:
            logger.debug("GPU stats not available - skipping GPU check")
            return
        
        gpu_ram_percent = gpu_stats.get('memory_percent', 0)
        gpu_util = gpu_stats.get('gpu_utilization', 0)
        
        logger.debug(f"GPU RAM: {gpu_ram_percent:.1f}%, GPU Util: {gpu_util:.1f}%")
        
        # Check if GPU RAM is full (>95%)
        if gpu_ram_percent > 95.0:
            logger.warning(f"⚠️  GPU RAM is {gpu_ram_percent:.1f}% full - checking for orphaned workers...")
            
            # Find orphaned multiprocess workers
            orphaned = self.find_orphaned_multiprocess_workers()
            
            if orphaned:
                logger.warning(f"🔍 Found {len(orphaned)} orphaned multiprocessing process(es)")
                
                # Send Slack notification about orphaned workers
                self.send_slack_notification(
                    "orphaned_workers",
                    f"Found {len(orphaned)} orphaned multiprocessing process(es). GPU RAM: {gpu_ram_percent:.1f}%"
                )
                
                killed_count = self.kill_orphaned_workers(orphaned)
                
                if killed_count > 0:
                    logger.info(f"✅ Killed {killed_count} orphaned worker(s)")
                    
                    # Wait a moment and check GPU RAM again
                    time.sleep(5)
                    gpu_stats_after = self.get_gpu_stats()
                    if gpu_stats_after:
                        new_ram_percent = gpu_stats_after.get('memory_percent', 0)
                        logger.info(f"📊 GPU RAM after cleanup: {new_ram_percent:.1f}% (was {gpu_ram_percent:.1f}%)")
                        
                        # If still >95% and GPU utilization is low, restart all training workers
                        if new_ram_percent > 95.0 and gpu_util < 10.0:
                            logger.warning(f"🔄 GPU RAM still {new_ram_percent:.1f}% full with low utilization - restarting training workers")
                            self.restart_training_workers("gpu_ram_full", f"GPU RAM {new_ram_percent:.1f}% full, GPU util {gpu_util:.1f}%")
                else:
                    logger.warning("⚠️  No orphaned workers killed - GPU RAM may be held by active processes")
            else:
                logger.debug("✅ No orphaned workers found")
                
                # If GPU RAM is full and utilization is low, restart all training workers
                if gpu_util < 10.0:
                    logger.warning(f"🔄 GPU RAM {gpu_ram_percent:.1f}% full with low utilization ({gpu_util:.1f}%) - restarting training workers")
                    
                    # Send Slack notification about GPU RAM issue
                    self.send_slack_notification(
                        "gpu_ram_full",
                        f"GPU RAM {gpu_ram_percent:.1f}% full with low utilization ({gpu_util:.1f}%) - restarting training workers"
                    )
                    
                    self.restart_training_workers("gpu_ram_full_low_util", f"GPU RAM {gpu_ram_percent:.1f}% full, GPU util {gpu_util:.1f}%")
        else:
            logger.debug(f"GPU RAM at {gpu_ram_percent:.1f}% - no action needed")

    def get_current_training_job_info(self) -> Optional[Dict]:
        """Get info about the current training job (if any) by checking worker output directories."""
        try:
            # Find most recent train_es job output directory
            output_base = Path(config.output_dir)
            train_es_dir = output_base / "train_es"
            
            if not train_es_dir.exists():
                return None
            
            # Find most recently modified job directory
            job_dirs = sorted(
                [d for d in train_es_dir.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            if not job_dirs:
                return None
            
            job_output_dir = job_dirs[0]
            job_id = job_output_dir.name
            
            # Get latest epoch
            latest_epoch = self.get_latest_epoch(job_output_dir)
            if latest_epoch is None:
                latest_epoch = 0
            
            # Calculate runtime from directory creation time
            runtime_seconds = int(time.time() - job_output_dir.stat().st_ctime)
            
            # Extract job name, rows, cols, and validation losses
            job_name = None
            num_rows = None
            num_columns = None
            initial_val_loss = None
            current_val_loss = None
            
            # Try to get session_id from job_id (format: {session_id}/{job_type}/{job_id}/)
            session_id = None
            if '/' in job_id:
                parts = job_id.split('/')
                if len(parts) >= 1:
                    session_id = parts[0]
            
            # Try to load session metadata
            if session_id:
                try:
                    session_file = Path("/sphere/app/featrix_sessions") / f"{session_id}.session"
                    if session_file.exists():
                        with open(session_file, 'r') as f:
                            session_data = json.load(f)
                            job_name = session_data.get('name')
                            if 'column_spec' in session_data:
                                num_columns = len(session_data['column_spec'])
                except Exception as e:
                    logger.debug(f"Error loading session metadata: {e}")
            
            # Try to get data info from structured data output
            if session_id:
                try:
                    session_dir = output_base.parent / "featrix_sessions" / session_id
                    create_sd_dir = session_dir / "create_structured_data"
                    if create_sd_dir.exists():
                        sd_jobs = sorted(create_sd_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
                        for sd_job in sd_jobs[:1]:
                            schema_file = sd_job / "schema_metadata.json"
                            if schema_file.exists():
                                with open(schema_file, 'r') as f:
                                    schema = json.load(f)
                                    if num_rows is None:
                                        num_rows = schema.get('total_rows')
                                    if num_columns is None:
                                        num_columns = schema.get('total_columns')
                except Exception as e:
                    logger.debug(f"Error loading schema metadata: {e}")
            
            # Try to get ES name from embedded_space.json
            es_file = job_output_dir / "embedded_space.json"
            if es_file.exists() and job_name is None:
                try:
                    with open(es_file, 'r') as f:
                        es_data = json.load(f)
                        job_name = es_data.get('name')
                except Exception as e:
                    logger.debug(f"Error loading embedded_space.json: {e}")
            
            # Extract validation losses from log file
            log_file = job_output_dir / "logs" / "stdout.log"
            if log_file.exists():
                try:
                    # Patterns to match validation loss
                    epoch_val_pattern = re.compile(r'\[epoch=(\d+)\].*?VAL LOSS:\s+([\d.]+)')
                    train_epoch_pattern = re.compile(r'Epoch (\d+)/\d+.*?validation_loss=([\d.]+)')
                    
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            # Try epoch pattern first
                            match = epoch_val_pattern.search(line)
                            if not match:
                                match = train_epoch_pattern.search(line)
                            
                            if match:
                                epoch = int(match.group(1))
                                val_loss = float(match.group(2))
                                if initial_val_loss is None:
                                    initial_val_loss = val_loss
                                if epoch >= latest_epoch:
                                    current_val_loss = val_loss
                except Exception as e:
                    logger.debug(f"Error extracting losses from log: {e}")
            
            result = {
                "job_id": job_id,
                "epochs": latest_epoch,
                "runtime_seconds": runtime_seconds
            }
            
            # Add optional fields if available
            if job_name:
                result["job_name"] = job_name
            if num_rows is not None:
                result["num_rows"] = num_rows
            if num_columns is not None:
                result["num_columns"] = num_columns
            if initial_val_loss is not None:
                result["initial_val_loss"] = initial_val_loss
            if current_val_loss is not None:
                result["current_val_loss"] = current_val_loss
            
            return result
        except Exception as e:
            logger.debug(f"Error getting training job info: {e}")
            return None

    def ping_sphere_api(self, training_info: Optional[Dict] = None):
        """Ping sphere-api /compute-nodes/announce endpoint with training info."""
        if not HAS_REQUESTS:
            return
        
        current_time = time.time()
        if current_time - self.last_announce_time < self.announce_interval:
            return  # Don't ping too frequently
        
        try:
            # Get version info if available
            version = "unknown"
            version_hash = "unknown"
            try:
                # Try importing from src/version module
                import sys
                from pathlib import Path
                src_path = Path(__file__).parent
                if str(src_path.resolve()) not in sys.path:
                    sys.path.insert(0, str(src_path.resolve()))
                
                from version import get_version
                version_info = get_version()
                version = version_info.semantic_version
                version_hash = version_info.git_hash[:8] if version_info.git_hash else "unknown"
            except (ImportError, AttributeError, Exception) as e:
                logger.debug(f"Could not get version info: {e}")
                # Fallback: try reading from files
                try:
                    version_file = Path("/sphere/VERSION")
                    if version_file.exists():
                        version = version_file.read_text().strip()
                    
                    # Try multiple locations for hash file (in order of preference)
                    hash_file = None
                    for hash_path in [
                        Path("/tmp/SPHERE_GIT_HASH"),
                        Path("/sphere/VERSION_HASH"),
                        Path("/sphere/app/VERSION_HASH"),
                    ]:
                        if hash_path.exists():
                            hash_file = hash_path
                            break
                    
                    if hash_file:
                        version_hash = hash_file.read_text().strip()[:8]
                except Exception:
                    pass
            
            payload = {
                "node_name": self.node_name,
                "status": "available",
                "node_timestamp_now": datetime.now().isoformat(),
                "version": version,
                "version_hash": version_hash
            }
            
            # Add training info if available
            if training_info:
                payload["training_job"] = training_info
            
            # Ping sphere-api
            try:
                # Create custom User-Agent with version and hostname
                user_agent = f"Featrix Firmware v{version} ({self.node_name})"
                response = requests.post(
                    "https://sphere-api.featrix.com/compute-nodes/announce",
                    json=payload,
                    timeout=5,
                    headers={'User-Agent': user_agent}
                )
                if response.status_code == 200:
                    self.last_announce_time = current_time
                    logger.info(f"✅ Pinged sphere-api successfully (node: {self.node_name}, status: {payload.get('status')})")
                else:
                    logger.warning(f"⚠️  sphere-api ping returned {response.status_code}: {response.text[:200]}")
            except Exception as e:
                logger.warning(f"⚠️  Failed to ping sphere-api: {e}", exc_info=True)
                
                # Log for retry
                try:
                    from lib.api_event_retry import get_retry_manager, EventType
                    retry_manager = get_retry_manager()
                    retry_manager.log_failed_event(
                        event_type=EventType.COMPUTE_NODE_ANNOUNCE,
                        url="https://sphere-api.featrix.com/compute-nodes/announce",
                        method="POST",
                        payload=payload,
                        timeout=5,
                        error=str(e),
                        metadata={"node_name": self.node_name}
                    )
                except Exception as retry_err:
                    logger.debug(f"Failed to log compute node announce for retry: {retry_err}")
        except Exception as e:
            logger.debug(f"Error pinging sphere-api: {e}")

    def check_celery_workers(self) -> bool:
        """Check if Celery workers are running, restart if down (unless /DISABLE exists or upgrade in progress)."""
        # Check for /DISABLE flag - skip worker monitoring if it exists
        disable_flag = Path("/sphere/DISABLE")
        if disable_flag.exists():
            logger.debug("✅ /DISABLE flag exists - skipping Celery worker check")
            return True
        
        # Check if upgrade is in progress - don't restart workers during upgrade
        upgrade_lock = Path("/tmp/auto-upgrade.lock")
        upgrade_flag = Path("/tmp/UPGRADE_SPHERE")
        if upgrade_lock.exists() or upgrade_flag.exists():
            logger.info("⚠️  Upgrade in progress - skipping Celery worker auto-restart")
            if upgrade_lock.exists():
                logger.info(f"   Upgrade lock file exists: {upgrade_lock}")
            if upgrade_flag.exists():
                logger.info(f"   Upgrade flag file exists: {upgrade_flag}")
            return True
        
        try:
            import subprocess
            # Check supervisor status for Celery workers
            result = subprocess.run(
                ['supervisorctl', 'status', 'celery-cpu_worker', 'celery-gpu_training'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logger.warning(f"⚠️  Could not check worker status: {result.stderr}")
                return True
            
            output = result.stdout
            cpu_worker_down = 'STOPPED' in output or 'FATAL' in output or ('celery-cpu_worker' in output and 'RUNNING' not in output.split('celery-cpu_worker')[1].split('\n')[0])
            gpu_worker_down = 'STOPPED' in output or 'FATAL' in output or ('celery-gpu_training' in output and 'RUNNING' not in output.split('celery-gpu_training')[1].split('\n')[0])
            
            if cpu_worker_down or gpu_worker_down:
                workers_down = []
                if cpu_worker_down:
                    workers_down.append('celery-cpu_worker')
                if gpu_worker_down:
                    workers_down.append('celery-gpu_training')
                
                logger.error(f"❌ CRITICAL: Celery workers are DOWN: {workers_down}")
                logger.error(f"   Auto-restarting workers (create /sphere/DISABLE to prevent this)...")
                
                # Restart the down workers
                for worker in workers_down:
                    try:
                        restart_result = subprocess.run(
                            ['supervisorctl', 'start', worker],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if restart_result.returncode == 0:
                            logger.info(f"✅ Auto-restarted {worker}")
                        else:
                            logger.error(f"❌ Failed to auto-restart {worker}: {restart_result.stderr}")
                    except Exception as e:
                        logger.error(f"❌ Error auto-restarting {worker}: {e}")
                
                # Send Slack notification
                self.send_slack_notification(
                    "celery_workers_auto_restart",
                    f"Celery workers were DOWN and auto-restarted by watchdog: {', '.join(workers_down)}"
                )
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"⚠️  Could not check Celery worker status: {e}")
            return True  # Non-critical, continue
    
    def run(self):
        """Main watchdog loop - monitors training jobs, GPU, orphaned workers, AND Celery worker availability."""
        logger.info("🐕 Featrix Training Watchdog started")
        logger.info("   Monitoring:")
        logger.info("     - Stuck training jobs")
        logger.info("     - GPU RAM and orphaned workers")
        logger.info("     - Celery worker availability")
        logger.info(f"   Check interval: {self.check_interval}s")
        logger.info(f"   Stuck threshold: {self.stuck_threshold}s")
        logger.info(f"   Worker auto-restart: enabled (create /sphere/DISABLE to disable)")
        logger.info("")
        
        try:
            while True:
                try:
                    # Check if Celery workers are running, restart if down
                    self.check_celery_workers()
                    
                    # Check for stuck training jobs and GPU issues
                    self.check_and_restart_if_needed()
                    
                    # Get current training job info and ping sphere-api
                    training_info = self.get_current_training_job_info()
                    self.ping_sphere_api(training_info)
                except Exception as e:
                    logger.error(f"Error in watchdog check: {e}", exc_info=True)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("Watchdog stopped by user")
        except Exception as e:
            logger.error(f"Fatal error in watchdog: {e}", exc_info=True)
            sys.exit(1)


def main():
    import socket
    hostname = socket.gethostname()
    logger.info("=" * 80)
    logger.info(f"🚀 FEATRIX WATCHDOG STARTING - {datetime.now().isoformat()}")
    logger.info("=" * 80)
    logger.info(f"Hostname: {hostname}")
    
    # Install Featrix exception hook for better error tracking
    try:
        from lib.featrix_debug import install_featrix_excepthook
        install_featrix_excepthook()
    except Exception:
        pass  # Don't fail if debug module not available
    
    parser = argparse.ArgumentParser(description='Featrix Training Watchdog')
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    parser.add_argument(
        '--stuck-threshold',
        type=int,
        default=300,
        help='Seconds without epoch progress before considering stuck (default: 300)'
    )
    
    args = parser.parse_args()
    
    logger.info(f"Check interval: {args.interval} seconds")
    logger.info(f"Stuck threshold: {args.stuck_threshold} seconds")
    logger.info("=" * 80)
    
    watchdog = TrainingWatchdog(
        check_interval=args.interval,
        stuck_threshold=args.stuck_threshold
    )
    watchdog.run()


if __name__ == '__main__':
    main()

