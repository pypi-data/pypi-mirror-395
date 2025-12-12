"""
Background logging engine for Crucible SDK.
"""

import queue
import threading
import time
import uuid
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json
import gzip
import io

from .config import CrucibleConfig
from .types import LogRequest, BatchLogRequest, LogResponse
from .errors import LoggingError, handle_logging_error
from .api.client import CrucibleAPIClient


@dataclass
class LoggingStats:
    """Statistics for logging operations."""
    
    total_requests: int = 0
    successful_logs: int = 0
    failed_logs: int = 0
    batches_sent: int = 0
    bytes_sent: int = 0
    last_flush_time: Optional[float] = None
    
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        return self.successful_logs / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_requests": self.total_requests,
            "successful_logs": self.successful_logs,
            "failed_logs": self.failed_logs,
            "batches_sent": self.batches_sent,
            "bytes_sent": self.bytes_sent,
            "success_rate": self.success_rate(),
            "last_flush_time": self.last_flush_time,
        }


class CrucibleLogger:
    """
    Background logger for Crucible SDK.
    
    Provides efficient, non-blocking logging with batching, compression,
    and retry mechanisms.
    """
    
    def __init__(self, config: CrucibleConfig):
        self.config = config
        self.api_client = CrucibleAPIClient(config)
        
        # Queue for background processing
        self.queue = queue.Queue(maxsize=config.max_queue_size)
        
        # Background worker thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.running = False
        
        # Statistics
        self.stats = LoggingStats()
        
        # Batch management
        self.current_batch = BatchLogRequest([])
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Start worker if logging is enabled
        if config.enable_logging:
            self.start()
    
    def start(self) -> None:
        """Start the background worker thread."""
        if self.running:
            return
        
        self.running = True
        self.worker_thread.start()
    
    def stop(self) -> None:
        """Stop the background worker thread."""
        if not self.running:
            return
        
        self.running = False
        
        # Flush remaining logs
        self.flush()
        
        # Wait for worker to finish
        self.worker_thread.join(timeout=5.0)
    
    def log_request(self, request: LogRequest) -> None:
        """
        Queue a log request for background processing.
        
        Args:
            request: The log request to queue
        """
        if not self.config.enable_logging:
            return
        
        # If immediate flush is enabled, send directly without batching
        if self.config.immediate_flush:
            try:
                batch = BatchLogRequest([request])
                self._send_batch(batch)
                with self.lock:
                    self.stats.total_requests += 1
                return
            except Exception as e:
                handle_logging_error(e, "log_request_immediate")
                return
        
        try:
            self.queue.put(request, timeout=1.0)
            with self.lock:
                self.stats.total_requests += 1
        except queue.Full:
            handle_logging_error(
                LoggingError("Log queue is full, dropping request"),
                "log_request"
            )
    
    def flush(self) -> None:
        """Force flush of current batch."""
        if self.current_batch.is_empty():
            return
        
        try:
            self._send_batch(self.current_batch)
            self.current_batch = BatchLogRequest([])
        except Exception as e:
            handle_logging_error(e, "flush")
    
    def _worker(self) -> None:
        """Background worker thread."""
        while self.running:
            try:
                # Try to get a request with timeout
                request = self.queue.get(timeout=self.config.flush_interval)
                
                # Add to current batch
                self.current_batch.add_request(request)
                
                # Check if batch is full
                if self.current_batch.is_full(self.config.batch_size):
                    self._send_batch(self.current_batch)
                    self.current_batch = BatchLogRequest([])
                
                # Mark task as done
                self.queue.task_done()
                
            except queue.Empty:
                # Timeout reached, flush current batch
                if not self.current_batch.is_empty():
                    self._send_batch(self.current_batch)
                    self.current_batch = BatchLogRequest([])
            
            except Exception as e:
                handle_logging_error(e, "worker")
    
    def _send_batch(self, batch: BatchLogRequest) -> None:
        """
        Send a batch of requests to the API.
        
        Args:
            batch: The batch to send
        """
        if batch.is_empty():
            return
        
        try:
            # Prepare batch data
            batch_data = batch.to_dict()
            
            # Always compress and base64 encode data for backend compatibility
            batch_data = self._compress_data(batch_data)
            
            # Send to API
            response = self.api_client.log_batch(batch_data)
            
            # Update statistics
            with self.lock:
                self.stats.batches_sent += 1
                self.stats.last_flush_time = time.time()
                
                # Handle Flask's async response (queued status)
                if response.status in ["success", "queued"]:
                    self.stats.successful_logs += len(batch.requests)
                else:
                    self.stats.failed_logs += len(batch.requests)
                
                # Estimate bytes sent
                self.stats.bytes_sent += len(str(batch_data))
        
        except Exception as e:
            handle_logging_error(e, "send_batch")
            with self.lock:
                self.stats.failed_logs += len(batch.requests)
    
    def _compress_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compress data for efficient transmission.
        
        Args:
            data: Data to compress
            
        Returns:
            Compressed data dictionary
        """
        try:
            # Convert to JSON bytes
            json_bytes = json.dumps(data).encode('utf-8')
            
            # Compress
            compressed = gzip.compress(json_bytes)
            
            # Return as base64 encoded string
            import base64
            compressed_b64 = base64.b64encode(compressed).decode('ascii')
            
            return {
                "compressed": True,
                "data": compressed_b64,
                "original_size": len(json_bytes),
                "compressed_size": len(compressed),
            }
        
        except Exception as e:
            handle_logging_error(e, "compress_data")
            return data
    
    def get_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        with self.lock:
            return self.stats.to_dict()
    
    def reset_stats(self) -> None:
        """Reset logging statistics."""
        with self.lock:
            self.stats = LoggingStats()
    
    def is_healthy(self) -> bool:
        """Check if logger is healthy."""
        if not self.running:
            return False
        
        if not self.worker_thread.is_alive():
            return False
        
        # Check queue health
        queue_size = self.queue.qsize()
        if queue_size > self.config.max_queue_size * 0.9:
            return False
        
        return True
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
