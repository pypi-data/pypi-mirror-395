"""
Crucible OpenAI wrapper for synchronous operations.
"""

import time
from typing import Union, Optional, Dict, Any
from openai import OpenAI as OriginalOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai._streaming import Stream
from openai._types import NotGiven, NOT_GIVEN
from openai._base_client import DEFAULT_MAX_RETRIES

from .config import CrucibleConfig
from .logger import CrucibleLogger
from .streaming import StreamingMerger, get_chat_completion_json
from .types import LogRequest
from .errors import handle_logging_error, LoggingError


class RawResponseWrapper:
    """Wrapper that provides raw response access."""
    
    def __init__(self, completions_wrapper):
        self.completions_wrapper = completions_wrapper
    
    def create(self, *args, **kwargs):
        """Create completion and return response with parse() method."""
        response = self.completions_wrapper.create(*args, **kwargs)
        
        # Create a wrapper object that has parse() method
        class ResponseWithParse:
            def __init__(self, data):
                self.data = data
            
            def parse(self):
                return self.data
        
        return ResponseWithParse(response)


class CrucibleCompletionsWrapper:
    """Wrapper for OpenAI completions with Crucible logging."""
    
    def __init__(self, original_completions, crucible_logger: CrucibleLogger):
        self.original_completions = original_completions
        self.crucible_logger = crucible_logger
        self.streaming_merger = StreamingMerger()
        self._raw_response_wrapper = RawResponseWrapper(self)
    
    def create(self, *args, **kwargs) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
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
            # Filter out Crucible-specific kwargs
            filtered_kwargs = {k: v for k, v in kwargs.items() 
                             if not k.startswith('_crucible') and k != 'crucible_metadata'}
            
            # Make the actual OpenAI API call
            completion = self.original_completions.create(*args, **filtered_kwargs)
            
            # Handle streaming vs non-streaming
            if isinstance(completion, Stream):
                return self._handle_streaming(completion, request_data, requested_at, metadata)
            else:
                return self._handle_non_streaming(completion, request_data, requested_at, metadata)
                
        except Exception as e:
            # Log error
            self._log_error(e, request_data, requested_at, metadata)
            raise e
    
    @property
    def with_raw_response(self):
        """Return a wrapper that provides raw response access."""
        return self._raw_response_wrapper
    
    def _handle_streaming(self, stream: Stream[ChatCompletionChunk], request_data: Dict[str, Any], 
                         requested_at: int, metadata: Dict[str, Any]) -> Stream[ChatCompletionChunk]:
        """Handle streaming completion."""
        assembled_completion = None
        
        # Create a wrapper class that logs after completion
        class LoggingStreamWrapper:
            def __init__(self, original_stream, merger, log_success, log_error, request_data, requested_at, metadata):
                self.original_stream = original_stream
                self.merger = merger
                self.log_success = log_success
                self.log_error = log_error
                self.request_data = request_data
                self.requested_at = requested_at
                self.metadata = metadata
                self.assembled_completion = None
                
            def __iter__(self):
                return self
                
            def __next__(self):
                try:
                    chunk = next(self.original_stream)
                    self.assembled_completion = self.merger.merge_chunk(self.assembled_completion, chunk)
                    return chunk
                except StopIteration:
                    # Log the complete response after streaming finishes
                    if self.assembled_completion:
                        self.log_success(self.assembled_completion, self.request_data, self.requested_at, self.metadata)
                    raise
                except Exception as e:
                    # Log error if streaming fails
                    self.log_error(e, self.request_data, self.requested_at, self.metadata)
                    raise
        
        return LoggingStreamWrapper(
            stream, 
            self.streaming_merger, 
            self._log_success, 
            self._log_error, 
            request_data, 
            requested_at, 
            metadata
        )
    
    def _handle_non_streaming(self, completion: ChatCompletion, request_data: Dict[str, Any], 
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
            
            # Base64 encode the log request for backend compatibility
            import json
            import base64
            
            # Convert to JSON and base64 encode
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
            
            # Base64 encode the log request for backend compatibility
            import json
            import base64
            
            # Convert to JSON and base64 encode
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


class CrucibleChatWrapper:
    """Wrapper for OpenAI chat with Crucible logging."""
    
    def __init__(self, original_chat, crucible_logger: CrucibleLogger):
        self.original_chat = original_chat
        self.crucible_logger = crucible_logger
        self.completions = CrucibleCompletionsWrapper(original_chat.completions, crucible_logger)


class CrucibleOpenAI:
    """
    Crucible wrapper for OpenAI client.
    
    Provides seamless integration with OpenAI's API while automatically
    logging requests and responses to Crucible warehouse.
    """
    
    def __init__(self, api_key: Optional[str] = None, domain: Optional[str] = None, 
                 immediate_flush: bool = False, **openai_kwargs):
        """
        Initialize Crucible OpenAI client.
        
        Args:
            api_key: Crucible API key (defaults to CRUCIBL_API_KEY env var)
            domain: Crucible domain (defaults to warehouse.usecrucible.ai)
            immediate_flush: If True, flush logs immediately after each request
            **openai_kwargs: Arguments passed to OpenAI client
        """
        # Initialize Crucible configuration
        self.crucible_config = CrucibleConfig(api_key=api_key, domain=domain, immediate_flush=immediate_flush)
        
        # Initialize OpenAI client
        self.openai_client = OriginalOpenAI(**openai_kwargs)
        
        # Initialize Crucible logger
        self.crucible_logger = CrucibleLogger(self.crucible_config)
        
        # Wrap chat completions
        self.chat = CrucibleChatWrapper(self.openai_client.chat, self.crucible_logger)
    
    def __getattr__(self, name):
        """Delegate unknown attributes to OpenAI client."""
        return getattr(self.openai_client, name)
    
    def close(self) -> None:
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
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.close()
        except Exception:
            pass
