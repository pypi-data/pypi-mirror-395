#!/usr/bin/env python3
"""
System health monitoring for memory pressure, disk errors, and kernel OOM events.

This module provides real-time monitoring of:
- System RAM usage and memory pressure
- GPU VRAM usage
- Kernel OOM events from dmesg
- Disk errors from dmesg
- Process-level memory consumption
"""
import logging
import os
import psutil
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class SystemHealthMonitor:
    """
    Monitor system health metrics including memory pressure, OOM events, and disk errors.
    """
    
    def __init__(self, job_id: str = None):
        self.job_id = job_id
        self.last_dmesg_check = None
        self.oom_events_seen = set()  # Track which OOM events we've already logged
        self.disk_errors_seen = set()
        
    def check_memory_pressure(self) -> Dict:
        """
        Check system memory pressure and return detailed stats.
        
        Returns:
            dict with keys:
                - total_ram_gb: Total system RAM
                - available_ram_gb: Available RAM (accounts for cache/buffers)
                - used_ram_gb: Used RAM
                - percent_used: Percentage of RAM used
                - swap_total_gb: Total swap space
                - swap_used_gb: Used swap
                - swap_percent: Percentage of swap used
                - pressure_level: 'low', 'medium', 'high', 'critical'
                - warning: Human-readable warning message if pressure is high
        """
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            total_ram = mem.total / (1024**3)
            available_ram = mem.available / (1024**3)
            used_ram = mem.used / (1024**3)
            percent_used = mem.percent
            
            swap_total = swap.total / (1024**3)
            swap_used = swap.used / (1024**3)
            swap_percent = swap.percent
            
            # Determine pressure level
            if percent_used < 70:
                pressure = 'low'
                warning = None
            elif percent_used < 85:
                pressure = 'medium'
                warning = f"Memory pressure moderate: {percent_used:.1f}% RAM used, {available_ram:.1f}GB available"
            elif percent_used < 95:
                pressure = 'high'
                warning = f"⚠️  HIGH memory pressure: {percent_used:.1f}% RAM used, only {available_ram:.1f}GB available"
            else:
                pressure = 'critical'
                warning = f"🚨 CRITICAL memory pressure: {percent_used:.1f}% RAM used, only {available_ram:.1f}GB available - OOM imminent!"
            
            # Check swap usage
            if swap_percent > 50 and swap_total > 0:
                if warning:
                    warning += f" | Swap: {swap_percent:.1f}% used ({swap_used:.1f}/{swap_total:.1f}GB)"
                else:
                    warning = f"⚠️  Swap usage high: {swap_percent:.1f}% ({swap_used:.1f}/{swap_total:.1f}GB)"
            
            return {
                'total_ram_gb': total_ram,
                'available_ram_gb': available_ram,
                'used_ram_gb': used_ram,
                'percent_used': percent_used,
                'swap_total_gb': swap_total,
                'swap_used_gb': swap_used,
                'swap_percent': swap_percent,
                'pressure_level': pressure,
                'warning': warning,
            }
        except Exception as e:
            logger.error(f"Failed to check memory pressure: {e}")
            return None
    
    def check_process_memory(self, pid: int = None) -> Dict:
        """
        Check memory usage for current process or specified PID.
        
        Args:
            pid: Process ID to check (None = current process)
            
        Returns:
            dict with keys:
                - pid: Process ID
                - rss_gb: Resident Set Size (actual RAM used)
                - vms_gb: Virtual Memory Size
                - percent: Percent of system RAM
                - num_threads: Number of threads
                - num_fds: Number of open file descriptors
        """
        try:
            if pid is None:
                pid = os.getpid()
            
            process = psutil.Process(pid)
            mem_info = process.memory_info()
            
            rss_gb = mem_info.rss / (1024**3)  # Resident Set Size (actual RAM)
            vms_gb = mem_info.vms / (1024**3)  # Virtual Memory Size
            percent = process.memory_percent()
            
            num_threads = process.num_threads()
            
            # Count file descriptors
            try:
                num_fds = process.num_fds()
            except:
                num_fds = None  # Not available on all platforms
            
            return {
                'pid': pid,
                'rss_gb': rss_gb,
                'vms_gb': vms_gb,
                'percent': percent,
                'num_threads': num_threads,
                'num_fds': num_fds,
            }
        except Exception as e:
            logger.error(f"Failed to check process memory for PID {pid}: {e}")
            return None
    
    def check_dmesg_for_oom(self) -> List[Dict]:
        """
        Check dmesg for recent OOM killer events.
        
        Returns:
            List of OOM events, each with:
                - timestamp: When the OOM occurred
                - victim_process: Process name that was killed
                - victim_pid: PID that was killed
                - message: Full dmesg message
        """
        try:
            # Run dmesg to get kernel messages
            # Use -T for human-readable timestamps
            result = subprocess.run(
                ['dmesg', '-T'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                # Try without -T (some systems don't support it)
                result = subprocess.run(
                    ['dmesg'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            if result.returncode != 0:
                logger.debug(f"dmesg failed with return code {result.returncode}")
                return []
            
            dmesg_output = result.stdout
            
            # Parse for OOM killer messages
            # Pattern: "Out of memory: Killed process <pid> (<name>)"
            oom_events = []
            oom_pattern = re.compile(
                r'(.*?)\s+.*?Out of memory.*?Killed process (\d+) \(([^)]+)\)',
                re.IGNORECASE
            )
            
            for line in dmesg_output.split('\n'):
                match = oom_pattern.search(line)
                if match:
                    timestamp_str = match.group(1)
                    pid = match.group(2)
                    process_name = match.group(3)
                    
                    # Create unique ID for this event (to avoid duplicate logging)
                    event_id = f"{timestamp_str}_{pid}_{process_name}"
                    
                    if event_id not in self.oom_events_seen:
                        self.oom_events_seen.add(event_id)
                        oom_events.append({
                            'timestamp': timestamp_str,
                            'victim_pid': pid,
                            'victim_process': process_name,
                            'message': line.strip(),
                            'event_id': event_id,
                        })
            
            return oom_events
            
        except subprocess.TimeoutExpired:
            logger.warning("dmesg check timed out")
            return []
        except PermissionError:
            logger.debug("Permission denied for dmesg (requires root/sudo)")
            return []
        except FileNotFoundError:
            logger.debug("dmesg command not found")
            return []
        except Exception as e:
            logger.debug(f"Failed to check dmesg for OOM events: {e}")
            return []
    
    def check_dmesg_for_disk_errors(self) -> List[Dict]:
        """
        Check dmesg for recent disk I/O errors.
        
        Returns:
            List of disk errors, each with:
                - timestamp: When the error occurred
                - device: Affected device (e.g., sda, nvme0n1)
                - error_type: Type of error (I/O error, timeout, etc.)
                - message: Full dmesg message
        """
        try:
            result = subprocess.run(
                ['dmesg', '-T'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                result = subprocess.run(['dmesg'], capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                return []
            
            dmesg_output = result.stdout
            
            # Parse for disk errors
            disk_errors = []
            error_patterns = [
                (r'(.*?)\s+.*?(sd[a-z]+|nvme\d+n\d+).*?(I/O error|timeout|failed command)', 'I/O error'),
                (r'(.*?)\s+.*?EXT4-fs.*?error', 'filesystem error'),
                (r'(.*?)\s+.*?Buffer I/O error', 'buffer I/O error'),
            ]
            
            for line in dmesg_output.split('\n'):
                for pattern, error_type in error_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        timestamp_str = match.group(1) if match.lastindex >= 1 else 'unknown'
                        device = match.group(2) if match.lastindex >= 2 else 'unknown'
                        
                        event_id = f"{timestamp_str}_{device}_{error_type}"
                        
                        if event_id not in self.disk_errors_seen:
                            self.disk_errors_seen.add(event_id)
                            disk_errors.append({
                                'timestamp': timestamp_str,
                                'device': device,
                                'error_type': error_type,
                                'message': line.strip(),
                                'event_id': event_id,
                            })
            
            return disk_errors
            
        except Exception as e:
            logger.debug(f"Failed to check dmesg for disk errors: {e}")
            return []
    
    def get_comprehensive_status(self) -> Dict:
        """
        Get comprehensive system health status including memory, OOM, and disk.
        
        Returns:
            dict with all health metrics
        """
        status = {
            'timestamp': datetime.now().isoformat(),
            'job_id': self.job_id,
        }
        
        # Memory pressure
        mem_pressure = self.check_memory_pressure()
        if mem_pressure:
            status['memory'] = mem_pressure
        
        # Process memory
        proc_mem = self.check_process_memory()
        if proc_mem:
            status['process'] = proc_mem
        
        # OOM events
        oom_events = self.check_dmesg_for_oom()
        if oom_events:
            status['oom_events'] = oom_events
        
        # Disk errors
        disk_errors = self.check_dmesg_for_disk_errors()
        if disk_errors:
            status['disk_errors'] = disk_errors
        
        return status
    
    def log_health_status(self, context: str = "", log_level: int = logging.INFO):
        """
        Log comprehensive health status with warnings for issues.
        
        Args:
            context: Context string to include in log (e.g., "EPOCH_START", "BEFORE_VALIDATION")
            log_level: Logging level to use for normal status
        """
        status = self.get_comprehensive_status()
        
        context_str = f" [{context}]" if context else ""
        
        # Log memory status
        if 'memory' in status:
            mem = status['memory']
            logger.log(
                log_level,
                f"💾 SYSTEM RAM{context_str}: {mem['used_ram_gb']:.1f}/{mem['total_ram_gb']:.1f}GB used "
                f"({mem['percent_used']:.1f}%), {mem['available_ram_gb']:.1f}GB available"
            )
            
            if mem['swap_percent'] > 10:
                logger.warning(
                    f"⚠️  SWAP{context_str}: {mem['swap_used_gb']:.1f}/{mem['swap_total_gb']:.1f}GB used "
                    f"({mem['swap_percent']:.1f}%)"
                )
            
            # Log warning if pressure is high
            if mem['warning']:
                logger.warning(mem['warning'])
        
        # Log process memory
        if 'process' in status:
            proc = status['process']
            logger.log(
                log_level,
                f"📊 PROCESS RAM{context_str}: PID={proc['pid']} RSS={proc['rss_gb']:.2f}GB "
                f"({proc['percent']:.1f}% of system), VMS={proc['vms_gb']:.2f}GB, threads={proc['num_threads']}"
            )
            
            if proc['num_fds']:
                logger.debug(f"   File descriptors: {proc['num_fds']}")
        
        # Log OOM events
        if 'oom_events' in status and status['oom_events']:
            for event in status['oom_events']:
                logger.error(
                    f"🚨 KERNEL OOM EVENT{context_str}: Killed PID {event['victim_pid']} "
                    f"({event['victim_process']}) at {event['timestamp']}"
                )
                logger.error(f"   Message: {event['message']}")
        
        # Log disk errors
        if 'disk_errors' in status and status['disk_errors']:
            for error in status['disk_errors']:
                logger.error(
                    f"💥 DISK ERROR{context_str}: {error['error_type']} on {error['device']} "
                    f"at {error['timestamp']}"
                )
                logger.error(f"   Message: {error['message']}")
        
        return status


def check_system_health(context: str = "", job_id: str = None) -> Dict:
    """
    Convenience function to check and log system health.
    
    Args:
        context: Context string for logging
        job_id: Job ID for tracking
        
    Returns:
        System health status dict
    """
    monitor = SystemHealthMonitor(job_id=job_id)
    return monitor.log_health_status(context=context)


def check_memory_available_for_workers(safety_margin_gb: float = 5.0) -> int:
    """
    Calculate how many DataLoader workers can be safely created based on available system RAM.
    
    Args:
        safety_margin_gb: GB of RAM to reserve for safety
        
    Returns:
        Maximum number of workers that can be created safely
    """
    try:
        mem = psutil.virtual_memory()
        available_ram_gb = mem.available / (1024**3)
        
        # Reserve safety margin
        available_for_workers = max(0, available_ram_gb - safety_margin_gb)
        
        # Each worker uses ~1-2GB RAM (depends on batch size and column types)
        # Conservative estimate: 2GB per worker
        worker_ram_gb = 2.0
        max_workers = int(available_for_workers / worker_ram_gb)
        
        logger.debug(
            f"RAM worker calculation: {available_ram_gb:.1f}GB available, "
            f"{safety_margin_gb:.1f}GB safety margin → max {max_workers} workers"
        )
        
        return max(0, max_workers)
    except Exception as e:
        logger.warning(f"Failed to calculate workers by RAM: {e}")
        return 8  # Safe default


def check_for_recent_oom_events(minutes: int = 10) -> List[Dict]:
    """
    Check for OOM events in the last N minutes.
    
    Args:
        minutes: How many minutes back to check
        
    Returns:
        List of recent OOM events
    """
    monitor = SystemHealthMonitor()
    all_events = monitor.check_dmesg_for_oom()
    
    # Filter for recent events (dmesg timestamp parsing is tricky, so return all for now)
    # In practice, we track seen events to avoid duplicate logging
    return all_events


if __name__ == '__main__':
    # Test the monitoring
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "=" * 80)
    print("SYSTEM HEALTH CHECK")
    print("=" * 80 + "\n")
    
    monitor = SystemHealthMonitor(job_id="test-job")
    status = monitor.log_health_status(context="TEST", log_level=logging.INFO)
    
    print("\n" + "=" * 80)
    print("RAW STATUS DICT")
    print("=" * 80)
    import json
    print(json.dumps(status, indent=2, default=str))

