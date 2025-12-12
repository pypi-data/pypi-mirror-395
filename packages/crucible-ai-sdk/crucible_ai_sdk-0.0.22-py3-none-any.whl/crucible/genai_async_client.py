"""
Crucible Google GenAI wrapper for asynchronous operations.
"""

import time
import asyncio
from typing import Union, Optional, Dict, Any, AsyncIterator
import json
import base64

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerateContentResponse
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    GenerateContentResponse = None

from .config import CrucibleConfig
from .logger import CrucibleLogger
from .streaming import StreamingMerger
from .genai_client import get_genai_response_json
from .types import LogRequest
from .errors import handle_logging_error, LoggingError


class CrucibleAsyncGenAIModelWrapper:
    """Wrapper for GenAI GenerativeModel with Crucible logging (async)."""
    
    def __init__(self, model, crucible_logger: CrucibleLogger):
        self.model = model
        self.crucible_logger = crucible_logger
        self.streaming_merger = StreamingMerger()
    
    async def generate_content(self, *args, **kwargs) -> Union[GenerateContentResponse, AsyncIterator[GenerateContentResponse]]:
        """Generate content with Crucible logging (async)."""
        # Extract Crucible metadata
        metadata = kwargs.pop("crucible_metadata", {})
        
        # Record request start time
        requested_at = int(time.time() * 1000)
        
        # Prepare request data for logging
        request_data = {
            "model": getattr(self.model, "_model_name", None) or getattr(self.model, "model_name", None),
            "contents": kwargs.get("contents") or (args[0] if args else None),
            "generation_config": kwargs.get("generation_config"),
            "safety_settings": kwargs.get("safety_settings"),
            "tools": kwargs.get("tools"),
            "tool_config": kwargs.get("tool_config"),
            "stream": kwargs.get("stream", False),
        }
        
        # Remove None values
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        try:
            # Filter out Crucible-specific kwargs
            filtered_kwargs = {k: v for k, v in kwargs.items() 
                             if not k.startswith('_crucible') and k != 'crucible_metadata'}
            
            # Check if GenAI has async support
            # Note: GenAI may not have native async, so we might need to run in executor
            if hasattr(self.model, "generate_content_async"):
                response = await self.model.generate_content_async(*args, **filtered_kwargs)
            else:
                # Run sync method in executor if async not available
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, 
                    lambda: self.model.generate_content(*args, **filtered_kwargs)
                )
            
            # Handle streaming vs non-streaming
            if kwargs.get("stream", False):
                # For async streaming, wrap the iterator
                return self._handle_streaming(response, request_data, requested_at, metadata)
            else:
                return self._handle_non_streaming(response, request_data, requested_at, metadata)
                
        except Exception as e:
            # Log error
            self._log_error(e, request_data, requested_at, metadata)
            raise e
    
    async def _handle_streaming(self, stream: AsyncIterator[GenerateContentResponse], request_data: Dict[str, Any], 
                               requested_at: int, metadata: Dict[str, Any]) -> AsyncIterator[GenerateContentResponse]:
        """Handle streaming completion (async)."""
        assembled_response = None
        
        # Create a wrapper class that logs after completion
        class LoggingAsyncStreamWrapper:
            def __init__(self, original_stream, merger, log_success, log_error, request_data, requested_at, metadata):
                self.original_stream = original_stream
                self.merger = merger
                self.log_success = log_success
                self.log_error = log_error
                self.request_data = request_data
                self.requested_at = requested_at
                self.metadata = metadata
                self.assembled_response = None
                self.chunks = []
                
            def __aiter__(self):
                return self
                
            async def __anext__(self):
                try:
                    # Handle both async iterator and sync iterator wrapped in executor
                    if hasattr(self.original_stream, "__anext__"):
                        chunk = await self.original_stream.__anext__()
                    else:
                        # Sync iterator in executor
                        loop = asyncio.get_event_loop()
                        chunk = await loop.run_in_executor(None, lambda: next(self.original_stream))
                    
                    self.chunks.append(chunk)
                    # Merge chunks for final logging
                    if self.assembled_response is None:
                        self.assembled_response = chunk
                    else:
                        # Try to merge response data
                        if hasattr(chunk, "candidates") and chunk.candidates:
                            if not hasattr(self.assembled_response, "candidates"):
                                self.assembled_response.candidates = []
                            self.assembled_response.candidates.extend(chunk.candidates)
                    return chunk
                except StopAsyncIteration:
                    # Log the complete response after streaming finishes
                    if self.assembled_response:
                        self.log_success(self.assembled_response, self.request_data, self.requested_at, self.metadata)
                    raise
                except StopIteration:
                    # Also handle StopIteration for sync iterators
                    if self.assembled_response:
                        self.log_success(self.assembled_response, self.request_data, self.requested_at, self.metadata)
                    raise StopAsyncIteration
                except Exception as e:
                    # Log error if streaming fails
                    self.log_error(e, self.request_data, self.requested_at, self.metadata)
                    raise
        
        return LoggingAsyncStreamWrapper(
            stream, 
            self.streaming_merger, 
            self._log_success, 
            self._log_error, 
            request_data, 
            requested_at, 
            metadata
        )
    
    async def _handle_non_streaming(self, response: GenerateContentResponse, request_data: Dict[str, Any], 
                                   requested_at: int, metadata: Dict[str, Any]) -> GenerateContentResponse:
        """Handle non-streaming completion (async)."""
        self._log_success(response, request_data, requested_at, metadata)
        return response
    
    def _log_success(self, response: GenerateContentResponse, request_data: Dict[str, Any], 
                    requested_at: int, metadata: Dict[str, Any]) -> None:
        """Log successful completion."""
        try:
            received_at = int(time.time() * 1000)
            
            # Convert response to JSON
            response_data = get_genai_response_json(response)
            
            # Create log request
            log_request = LogRequest.from_genai_call(
                request_data=request_data,
                response_data=response_data,
                requested_at=requested_at,
                received_at=received_at,
                status_code=200,
                metadata=metadata,
            )
            
            # Base64 encode the log request for backend compatibility
            json_data = json.dumps(log_request.to_dict())
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('ascii')
            
            # Create encoded log request
            encoded_log_request = LogRequest(
                requested_at=log_request.requested_at,
                received_at=log_request.received_at,
                req_payload={"encoded": True, "data": encoded_data},
                resp_payload=None,
                status_code=log_request.status_code,
                error_message=log_request.error_message,
                metadata=log_request.metadata,
                tags=log_request.tags,
                model=log_request.model,
                completion_id=log_request.completion_id,
                sdk_version=log_request.sdk_version,
                sdk_name=log_request.sdk_name,
            )
            
            # Queue for background logging
            self.crucible_logger.log_request(encoded_log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_success")
    
    def _log_error(self, error: Exception, request_data: Dict[str, Any], 
                  requested_at: int, metadata: Dict[str, Any]) -> None:
        """Log error completion."""
        try:
            received_at = int(time.time() * 1000)
            
            # Extract error information
            error_message = str(error)
            status_code = getattr(error, 'status_code', None) or getattr(error, 'code', None)
            
            # Create log request
            log_request = LogRequest.from_genai_call(
                request_data=request_data,
                response_data=None,
                requested_at=requested_at,
                received_at=received_at,
                status_code=status_code,
                error_message=error_message,
                metadata=metadata,
            )
            
            # Base64 encode the log request for backend compatibility
            json_data = json.dumps(log_request.to_dict())
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('ascii')
            
            # Create encoded log request
            encoded_log_request = LogRequest(
                requested_at=log_request.requested_at,
                received_at=log_request.received_at,
                req_payload={"encoded": True, "data": encoded_data},
                resp_payload=None,
                status_code=log_request.status_code,
                error_message=log_request.error_message,
                metadata=log_request.metadata,
                tags=log_request.tags,
                model=log_request.model,
                completion_id=log_request.completion_id,
                sdk_version=log_request.sdk_version,
                sdk_name=log_request.sdk_name,
            )
            
            # Queue for background logging
            self.crucible_logger.log_request(encoded_log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_error")


class CrucibleAsyncGenAI:
    """
    Crucible wrapper for Google GenAI client (async).
    
    Provides seamless integration with Google's Generative AI API while automatically
    logging requests and responses to Crucible warehouse.
    """
    
    def __init__(self, api_key: Optional[str] = None, domain: Optional[str] = None, 
                 genai_api_key: Optional[str] = None, **genai_kwargs):
        """
        Initialize Crucible async GenAI client.
        
        Args:
            api_key: Crucible API key (defaults to CRUCIBLE_API_KEY env var)
            domain: Crucible domain (defaults to warehouse.usecrucible.ai)
            genai_api_key: Google GenAI API key (defaults to GOOGLE_API_KEY env var)
            **genai_kwargs: Arguments passed to GenAI configuration
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-generativeai package is not installed. "
                "Install it with: pip install google-generativeai"
            )
        
        # Initialize Crucible configuration
        self.crucible_config = CrucibleConfig(api_key=api_key, domain=domain)
        
        # Initialize GenAI client
        # Use provided genai_api_key or get from environment
        import os
        genai_api_key = genai_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
        
        if genai_api_key:
            genai.configure(api_key=genai_api_key, **genai_kwargs)
        
        # Store GenAI module reference
        self.genai_module = genai
        
        # Initialize Crucible logger
        self.crucible_logger = CrucibleLogger(self.crucible_config)
    
    async def GenerativeModel(self, model_name: str, **kwargs):
        """
        Create a GenerativeModel with Crucible logging (async).
        
        Args:
            model_name: Name of the model to use
            **kwargs: Additional arguments for GenerativeModel
            
        Returns:
            CrucibleAsyncGenAIModelWrapper instance
        """
        # Run sync GenerativeModel creation in executor
        loop = asyncio.get_event_loop()
        model = await loop.run_in_executor(
            None,
            lambda: self.genai_module.GenerativeModel(model_name, **kwargs)
        )
        return CrucibleAsyncGenAIModelWrapper(model, self.crucible_logger)
    
    def __getattr__(self, name):
        """Delegate unknown attributes to GenAI module."""
        return getattr(self.genai_module, name)
    
    async def close(self) -> None:
        """Close the client and flush logs."""
        self.crucible_logger.stop()
    
    def flush_logs(self) -> None:
        """Force flush of pending logs."""
        self.crucible_logger.flush()
    
    def get_logging_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        return self.crucible_logger.get_stats()
    
    def is_healthy(self) -> bool:
        """Check if client is healthy."""
        return self.crucible_logger.is_healthy()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            # Note: Can't await in __del__, so we just stop the logger
            self.crucible_logger.stop()
        except Exception:
            pass

