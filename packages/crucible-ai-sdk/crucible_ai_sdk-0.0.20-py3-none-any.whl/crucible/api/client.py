"""
Simple HTTP client for Crucible API.
"""

import httpx
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from ..config import CrucibleConfig
from ..types import LogResponse, UpdateTagsResponse
from ..errors import APIError, NetworkError, TimeoutError


@dataclass
class CircuitBreaker:
    """Simple circuit breaker for API calls."""
    
    failure_threshold: int = 5
    timeout: float = 60.0
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise APIError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"


class CrucibleAPIClient:
    """
    Simple HTTP client for Crucible API.
    
    Provides efficient communication with retry logic, circuit breaker,
    and connection pooling.
    """
    
    def __init__(self, config: CrucibleConfig):
        self.config = config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.max_retries,
            timeout=config.timeout
        )
        
        # Create HTTP client with optimizations
        self.client = httpx.Client(
            timeout=config.timeout,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            ),
            headers={
                "User-Agent": f"crucible-python-sdk/{config.sdk_version}",
                "Content-Type": "application/json",
            }
        )
        
        # Set up authentication
        if config.api_key:
            self.client.headers["Authorization"] = f"Bearer {config.api_key}"
    
    def log_batch(self, batch_data: Dict[str, Any]) -> LogResponse:
        """
        Log a batch of requests.
        
        Args:
            batch_data: Batch data to send
            
        Returns:
            LogResponse from API
        """
        def _make_request():
            response = self.client.post(
                self.config.base_url,
                json=batch_data
            )
            
            # Handle Flask's 202 Accepted response (async processing)
            if response.status_code == 202:
                flask_response = response.json()
                return LogResponse(
                    flask_response.get("task_id", "unknown"),
                    "queued",
                    flask_response.get("message", "Log queued successfully"),
                    flask_response.get("status_url")
                )
            elif response.status_code == 200:
                return LogResponse.from_dict(response.json())
            else:
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response=response.text
                )
        
        try:
            return self.circuit_breaker.call(_make_request)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise APIError(f"API request failed: {e}")
    
    def log_single(self, request_data: Dict[str, Any]) -> LogResponse:
        """
        Log a single request.
        
        Args:
            request_data: Request data to send
            
        Returns:
            LogResponse from API
        """
        def _make_request():
            # Compress single request data for consistency
            import json
            import gzip
            import base64
            
            json_bytes = json.dumps(request_data).encode('utf-8')
            compressed = gzip.compress(json_bytes)
            compressed_b64 = base64.b64encode(compressed).decode('ascii')
            
            compressed_data = {
                "compressed": True,
                "data": compressed_b64,
                "original_size": len(json_bytes),
                "compressed_size": len(compressed),
            }
            
            response = self.client.post(
                self.config.base_url,
                json=compressed_data
            )
            
            # Handle Flask's 202 Accepted response (async processing)
            if response.status_code == 202:
                flask_response = response.json()
                return LogResponse(
                    flask_response.get("task_id", "unknown"),
                    "queued",
                    flask_response.get("message", "Log queued successfully"),
                    flask_response.get("status_url")
                )
            elif response.status_code == 200:
                return LogResponse.from_dict(response.json())
            else:
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response=response.text
                )
        
        try:
            return self.circuit_breaker.call(_make_request)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise APIError(f"API request failed: {e}")
    
    def update_tags(self, filters: List[Dict[str, Any]], tags: Dict[str, Any]) -> UpdateTagsResponse:
        """
        Update tags for matching logs.
        
        Args:
            filters: Filters to match logs
            tags: Tags to update
            
        Returns:
            UpdateTagsResponse from API
        """
        def _make_request():
            response = self.client.post(
                f"{self.config.base_url}/update-tags",
                json={"filters": filters, "tags": tags}
            )
            
            if response.status_code == 200:
                return UpdateTagsResponse.from_dict(response.json())
            else:
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response=response.text
                )
        
        try:
            return self.circuit_breaker.call(_make_request)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise APIError(f"API request failed: {e}")
    
    def health_check(self) -> bool:
        """
        Check API health.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.config.base_url}/health", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
