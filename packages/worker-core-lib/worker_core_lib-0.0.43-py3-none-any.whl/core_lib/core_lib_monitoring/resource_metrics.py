"""
Resource metrics collection for workers.

Tracks CPU, memory, disk I/O, and network usage during job processing.
Uses psutil for cross-platform system monitoring.
"""
import os
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

logger = logging.getLogger(__name__)


@dataclass
class CPUMetrics:
    """CPU usage metrics."""
    peak_percent: float = 0.0
    avg_percent: float = 0.0
    cores_used: float = 0.0
    system_time_ms: int = 0
    user_time_ms: int = 0


@dataclass
class MemoryMetrics:
    """Memory usage metrics."""
    peak_mb: float = 0.0
    avg_mb: float = 0.0
    start_mb: float = 0.0
    end_mb: float = 0.0
    leak_detected: bool = False


@dataclass
class DiskMetrics:
    """Disk I/O metrics."""
    bytes_read: int = 0
    bytes_written: int = 0
    ops_read: int = 0
    ops_write: int = 0
    temp_files_created: int = 0
    temp_files_size_mb: float = 0.0


@dataclass
class NetworkMetrics:
    """Network usage metrics."""
    bytes_received: int = 0
    bytes_sent: int = 0
    api_calls_count: int = 0
    avg_latency_ms: int = 0
    
    # Internal tracking
    _latencies: List[int] = field(default_factory=list, repr=False)
    
    def add_api_call(self, latency_ms: int):
        """Record an API call with its latency."""
        self.api_calls_count += 1
        self._latencies.append(latency_ms)
        if self._latencies:
            self.avg_latency_ms = sum(self._latencies) // len(self._latencies)


@dataclass
class ResourceSnapshot:
    """Snapshot of resource usage at a point in time."""
    timestamp: datetime
    cpu_percent: float
    memory_mb: float


class ResourceMetricsCollector:
    """
    Collects system resource metrics during worker job processing.
    
    Usage:
        collector = ResourceMetricsCollector()
        collector.start()
        
        # ... do work ...
        collector.network_metrics.add_api_call(latency_ms=150)
        
        metrics = collector.stop()
        
        # Access metrics
        print(f"Peak CPU: {metrics['cpu']['peakPercent']}%")
        print(f"Peak Memory: {metrics['memory']['peakMb']} MB")
    """
    
    def __init__(self, sampling_interval: float = 0.5):
        """
        Initialize resource metrics collector.
        
        Args:
            sampling_interval: How often to sample metrics (seconds)
        """
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available - resource metrics will be limited")
        
        self.sampling_interval = sampling_interval
        self.process = psutil.Process(os.getpid()) if PSUTIL_AVAILABLE else None
        
        # Metrics storage
        self.cpu_metrics = CPUMetrics()
        self.memory_metrics = MemoryMetrics()
        self.disk_metrics = DiskMetrics()
        self.network_metrics = NetworkMetrics()
        
        # Snapshots for averaging
        self.snapshots: List[ResourceSnapshot] = []
        
        # Start/end state
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.initial_disk_io = None
        self.initial_network_io = None
        
        # Sampling control
        self._sampling = False
        self._sample_thread = None
    
    def start(self):
        """Start collecting metrics."""
        if not PSUTIL_AVAILABLE:
            logger.debug("psutil not available - skipping resource collection")
            return
        
        self.start_time = time.time()
        self._sampling = True
        
        # Record initial state
        try:
            self.memory_metrics.start_mb = self.process.memory_info().rss / (1024 * 1024)
        except Exception as e:
            logger.warning(f"Failed to get initial memory: {e}")
        
        try:
            self.initial_disk_io = self.process.io_counters()
        except (AttributeError, OSError) as e:
            logger.debug(f"Disk I/O metrics not available: {e}")
            self.initial_disk_io = None
        
        try:
            self.initial_network_io = psutil.net_io_counters()
        except Exception as e:
            logger.debug(f"Network metrics not available: {e}")
            self.initial_network_io = None
        
        # Start background sampling thread
        import threading
        self._sample_thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._sample_thread.start()
        
        logger.debug("Resource metrics collection started")
    
    def stop(self) -> Dict:
        """
        Stop collecting metrics and return summary.
        
        Returns:
            Dictionary with CPU, memory, disk, and network metrics
        """
        if not PSUTIL_AVAILABLE:
            return self._empty_metrics()
        
        self._sampling = False
        self.end_time = time.time()
        
        # Wait for sampling thread to finish
        if self._sample_thread and self._sample_thread.is_alive():
            self._sample_thread.join(timeout=1.0)
        
        # Record final state
        try:
            self.memory_metrics.end_mb = self.process.memory_info().rss / (1024 * 1024)
            
            # Calculate memory leak detection (50% increase threshold)
            if self.memory_metrics.end_mb > self.memory_metrics.start_mb * 1.5:
                self.memory_metrics.leak_detected = True
                logger.warning(
                    f"Potential memory leak detected: "
                    f"{self.memory_metrics.start_mb:.1f} MB -> {self.memory_metrics.end_mb:.1f} MB"
                )
        except Exception as e:
            logger.warning(f"Failed to get final memory: {e}")
        
        # Calculate disk I/O delta
        if self.initial_disk_io:
            try:
                final_disk_io = self.process.io_counters()
                self.disk_metrics.bytes_read = final_disk_io.read_bytes - self.initial_disk_io.read_bytes
                self.disk_metrics.bytes_written = final_disk_io.write_bytes - self.initial_disk_io.write_bytes
                self.disk_metrics.ops_read = final_disk_io.read_count - self.initial_disk_io.read_count
                self.disk_metrics.ops_write = final_disk_io.write_count - self.initial_disk_io.write_count
            except Exception as e:
                logger.debug(f"Failed to calculate disk I/O delta: {e}")
        
        # Calculate network delta
        if self.initial_network_io:
            try:
                final_network_io = psutil.net_io_counters()
                self.network_metrics.bytes_received = final_network_io.bytes_recv - self.initial_network_io.bytes_recv
                self.network_metrics.bytes_sent = final_network_io.bytes_sent - self.initial_network_io.bytes_sent
            except Exception as e:
                logger.debug(f"Failed to calculate network delta: {e}")
        
        # Calculate averages from snapshots
        if self.snapshots:
            self.cpu_metrics.avg_percent = sum(s.cpu_percent for s in self.snapshots) / len(self.snapshots)
            self.memory_metrics.avg_mb = sum(s.memory_mb for s in self.snapshots) / len(self.snapshots)
        
        # Get CPU times
        try:
            cpu_times = self.process.cpu_times()
            self.cpu_metrics.system_time_ms = int(cpu_times.system * 1000)
            self.cpu_metrics.user_time_ms = int(cpu_times.user * 1000)
        except Exception as e:
            logger.debug(f"Failed to get CPU times: {e}")
        
        logger.debug(
            f"Resource metrics collected: "
            f"CPU peak={self.cpu_metrics.peak_percent:.1f}%, "
            f"Memory peak={self.memory_metrics.peak_mb:.1f}MB"
        )
        
        return self.to_dict()
    
    def _sample_loop(self):
        """Background loop to sample metrics at regular intervals."""
        while self._sampling:
            try:
                # Sample CPU
                cpu_percent = self.process.cpu_percent(interval=None)
                self.cpu_metrics.peak_percent = max(self.cpu_metrics.peak_percent, cpu_percent)
                
                # Sample memory
                memory_mb = self.process.memory_info().rss / (1024 * 1024)
                self.memory_metrics.peak_mb = max(self.memory_metrics.peak_mb, memory_mb)
                
                # Record snapshot
                snapshot = ResourceSnapshot(
                    timestamp=datetime.now(),
                    cpu_percent=cpu_percent,
                    memory_mb=memory_mb
                )
                self.snapshots.append(snapshot)
                
            except Exception as e:
                logger.debug(f"Error sampling metrics: {e}")
            
            time.sleep(self.sampling_interval)
    
    def _empty_metrics(self) -> Dict:
        """Return empty metrics structure when psutil unavailable."""
        return {
            "cpu": {
                "peakPercent": 0.0,
                "avgPercent": 0.0,
                "coresUsed": 0.0,
                "systemTimeMs": 0,
                "userTimeMs": 0,
            },
            "memory": {
                "peakMb": 0.0,
                "avgMb": 0.0,
                "startMb": 0.0,
                "endMb": 0.0,
                "leakDetected": False,
            },
            "disk": {
                "bytesRead": 0,
                "bytesWritten": 0,
                "opsRead": 0,
                "opsWrite": 0,
                "tempFilesCreated": 0,
                "tempFilesSizeMb": 0.0,
            },
            "network": {
                "bytesReceived": 0,
                "bytesSent": 0,
                "apiCallsCount": 0,
                "avgLatencyMs": 0,
            }
        }
    
    def to_dict(self) -> Dict:
        """Convert metrics to dictionary for serialization."""
        return {
            "cpu": {
                "peakPercent": round(self.cpu_metrics.peak_percent, 2),
                "avgPercent": round(self.cpu_metrics.avg_percent, 2),
                "coresUsed": round(self.cpu_metrics.cores_used, 2),
                "systemTimeMs": self.cpu_metrics.system_time_ms,
                "userTimeMs": self.cpu_metrics.user_time_ms,
            },
            "memory": {
                "peakMb": round(self.memory_metrics.peak_mb, 2),
                "avgMb": round(self.memory_metrics.avg_mb, 2),
                "startMb": round(self.memory_metrics.start_mb, 2),
                "endMb": round(self.memory_metrics.end_mb, 2),
                "leakDetected": self.memory_metrics.leak_detected,
            },
            "disk": {
                "bytesRead": self.disk_metrics.bytes_read,
                "bytesWritten": self.disk_metrics.bytes_written,
                "opsRead": self.disk_metrics.ops_read,
                "opsWrite": self.disk_metrics.ops_write,
                "tempFilesCreated": self.disk_metrics.temp_files_created,
                "tempFilesSizeMb": round(self.disk_metrics.temp_files_size_mb, 2),
            },
            "network": {
                "bytesReceived": self.network_metrics.bytes_received,
                "bytesSent": self.network_metrics.bytes_sent,
                "apiCallsCount": self.network_metrics.api_calls_count,
                "avgLatencyMs": self.network_metrics.avg_latency_ms,
            }
        }
