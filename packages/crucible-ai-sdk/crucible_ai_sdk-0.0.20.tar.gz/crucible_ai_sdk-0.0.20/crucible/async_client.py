"""
Crucible OpenAI wrapper for asynchronous operations.
"""

import time
import asyncio
from typing import Union, Optional, Dict, Any
from openai import AsyncOpenAI as OriginalAsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai._streaming import AsyncStream
from openai._types import NotGiven, NOT_GIVEN
from openai._base_client import DEFAULT_MAX_RETRIES

from .config import CrucibleConfig
from .logger import CrucibleLogger
from .streaming import StreamingMerger, get_chat_completion_json
from .types import LogRequest
from .errors import handle_logging_error, LoggingError


class CrucibleAsyncCompletionsWrapper:
    """Wrapper for OpenAI async completions with Crucible logging."""
    
    def __init__(self, original_completions, crucible_logger: CrucibleLogger):
        self.original_completions = original_completions
        self.crucible_logger = crucible_logger
        self.streaming_merger = StreamingMerger()
    
    async def create(self, *args, **kwargs) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
        """Create completion with Crucible logging."""
        # Extract Crucible metadata
        metadata = kwargs.pop("crucible_metadata", {})
        
        # Record request start time
        requested_at = int(time.time() * 1000)
        
        # Prepare request data for logging
        request_data = {
            "model": kwargs.get("model"),
            "messages": kwargs.get("messages", []),
            "temperature": kwargs.get("temperature"),
            "max_tokens": kwargs.get("max_tokens"),
            "stream": kwargs.get("stream", False),
            "functions": kwargs.get("functions"),
            "function_call": kwargs.get("function_call"),
            "tools": kwargs.get("tools"),
            "tool_choice": kwargs.get("tool_choice"),
            "response_format": kwargs.get("response_format"),
            "stop": kwargs.get("stop"),
            "presence_penalty": kwargs.get("presence_penalty"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "logit_bias": kwargs.get("logit_bias"),
            "user": kwargs.get("user"),
            "n": kwargs.get("n"),
            "seed": kwargs.get("seed"),
        }
        
        # Remove None values
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        try:
            # Make the actual OpenAI API call
            completion = await self.original_completions.create(*args, **kwargs)
            
            # Handle streaming vs non-streaming
            if isinstance(completion, AsyncStream):
                return self._handle_streaming(completion, request_data, requested_at, metadata)
            else:
                return self._handle_non_streaming(completion, request_data, requested_at, metadata)
                
        except Exception as e:
            # Log error
            self._log_error(e, request_data, requested_at, metadata)
            raise e
    
    async def _handle_streaming(self, stream: AsyncStream[ChatCompletionChunk], request_data: Dict[str, Any], 
                              requested_at: int, metadata: Dict[str, Any]) -> AsyncStream[ChatCompletionChunk]:
        """Handle streaming completion."""
        assembled_completion = None
        
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
                self.assembled_completion = None
                
            def __aiter__(self):
                return self
                
            async def __anext__(self):
                try:
                    chunk = await self.original_stream.__anext__()
                    self.assembled_completion = self.merger.merge_chunk(self.assembled_completion, chunk)
                    return chunk
                except StopAsyncIteration:
                    # Log the complete response after streaming finishes
                    if self.assembled_completion:
                        self.log_success(self.assembled_completion, self.request_data, self.requested_at, self.metadata)
                    raise
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
    
    async def _handle_non_streaming(self, completion: ChatCompletion, request_data: Dict[str, Any], 
                                  requested_at: int, metadata: Dict[str, Any]) -> ChatCompletion:
        """Handle non-streaming completion."""
        self._log_success(completion, request_data, requested_at, metadata)
        return completion
    
    def _log_success(self, completion: ChatCompletion, request_data: Dict[str, Any], 
                    requested_at: int, metadata: Dict[str, Any]) -> None:
        """Log successful completion."""
        try:
            received_at = int(time.time() * 1000)
            
            # Convert completion to JSON
            response_data = get_chat_completion_json(completion)
            
            # Create log request
            log_request = LogRequest.from_openai_call(
                request_data=request_data,
                response_data=response_data,
                requested_at=requested_at,
                received_at=received_at,
                status_code=200,
                metadata=metadata,
            )
            
            # Queue for background logging
            self.crucible_logger.log_request(log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_success")
    
    def _log_error(self, error: Exception, request_data: Dict[str, Any], 
                  requested_at: int, metadata: Dict[str, Any]) -> None:
        """Log error completion."""
        try:
            received_at = int(time.time() * 1000)
            
            # Extract error information
            error_message = str(error)
            status_code = getattr(error, 'status_code', None)
            
            # Create log request
            log_request = LogRequest.from_openai_call(
                request_data=request_data,
                response_data=None,
                requested_at=requested_at,
                received_at=received_at,
                status_code=status_code,
                error_message=error_message,
                metadata=metadata,
            )
            
            # Queue for background logging
            self.crucible_logger.log_request(log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_error")


class CrucibleAsyncChatWrapper:
    """Wrapper for OpenAI async chat with Crucible logging."""
    
    def __init__(self, original_chat, crucible_logger: CrucibleLogger):
        self.original_chat = original_chat
        self.crucible_logger = crucible_logger
        self.completions = CrucibleAsyncCompletionsWrapper(original_chat.completions, crucible_logger)


class CrucibleAsyncOpenAI:
    """
    Crucible wrapper for OpenAI async client.
    
    Provides seamless integration with OpenAI's async API while automatically
    logging requests and responses to Crucible warehouse.
    """
    
    def __init__(self, api_key: Optional[str] = None, domain: Optional[str] = None, **openai_kwargs):
        """
        Initialize Crucible async OpenAI client.
        
        Args:
            api_key: Crucible API key (defaults to CRUCIBLE_API_KEY env var)
            domain: Crucible domain (defaults to warehouse.usecrucible.ai)
            **openai_kwargs: Arguments passed to OpenAI async client
        """
        # Initialize Crucible configuration
        self.crucible_config = CrucibleConfig(api_key=api_key, domain=domain)
        
        # Initialize OpenAI async client
        self.openai_client = OriginalAsyncOpenAI(**openai_kwargs)
        
        # Initialize Crucible logger
        self.crucible_logger = CrucibleLogger(self.crucible_config)
        
        # Wrap chat completions
        self.chat = CrucibleAsyncChatWrapper(self.openai_client.chat, self.crucible_logger)
    
    def __getattr__(self, name):
        """Delegate unknown attributes to OpenAI client."""
        return getattr(self.openai_client, name)
    
    async def close(self) -> None:
        """Close the client and flush logs."""
        self.crucible_logger.stop()
        await self.openai_client.close()
    
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
