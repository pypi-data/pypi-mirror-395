"""
Crucible Google GenAI wrapper for synchronous operations.
"""

import time
import uuid
from typing import Union, Optional, Dict, Any, Iterator
from collections.abc import Iterator as ABCIterator
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
from .types import LogRequest
from .errors import handle_logging_error, LoggingError


def get_genai_response_json(response: Any) -> Dict[str, Any]:
    """
    Convert GenAI GenerateContentResponse to JSON-serializable dictionary.
    
    Args:
        response: GenerateContentResponse object or dict
        
    Returns:
        JSON-serializable dictionary
    """
    try:
        # If it's already a dict, return it
        if isinstance(response, dict):
            return response
        
        # Try to use the response's built-in to_dict or model_dump method
        if hasattr(response, "to_dict"):
            try:
                return response.to_dict()
            except:
                pass
        
        if hasattr(response, "model_dump"):
            try:
                return response.model_dump()
            except:
                pass
        
        # Convert GenAI response to dict manually
        result = {
            "candidates": [],
            "usage_metadata": {},
        }
        
        # Extract ID if available
        if hasattr(response, "id"):
            result["id"] = response.id
        
        # Extract candidates
        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                candidate_dict = {}
                
                # Extract content
                if hasattr(candidate, "content"):
                    content = candidate.content
                    if hasattr(content, "parts"):
                        parts = []
                        for part in content.parts:
                            part_dict = {}
                            if hasattr(part, "text"):
                                part_dict["text"] = str(part.text) if part.text else None
                            if hasattr(part, "function_call") and part.function_call:
                                # Serialize function_call safely
                                func_call = part.function_call
                                part_dict["function_call"] = {
                                    "name": getattr(func_call, "name", None),
                                    "args": getattr(func_call, "args", None),
                                }
                            if part_dict.get("text") or part_dict.get("function_call"):
                                parts.append(part_dict)
                        if parts:
                            candidate_dict["content"] = {"parts": parts}
                
                # Extract finish reason (convert enum to string if needed)
                if hasattr(candidate, "finish_reason"):
                    finish_reason = candidate.finish_reason
                    if finish_reason is not None:
                        candidate_dict["finish_reason"] = str(finish_reason) if not isinstance(finish_reason, str) else finish_reason
                
                # Extract index
                if hasattr(candidate, "index"):
                    candidate_dict["index"] = candidate.index
                
                if candidate_dict:
                    result["candidates"].append(candidate_dict)
        
        # Extract usage metadata
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            usage = response.usage_metadata
            result["usage_metadata"] = {
                "prompt_token_count": getattr(usage, "prompt_token_count", None),
                "candidates_token_count": getattr(usage, "candidates_token_count", None),
                "total_token_count": getattr(usage, "total_token_count", None),
            }
        
        # Extract prompt feedback if available
        if hasattr(response, "prompt_feedback") and response.prompt_feedback:
            pf = response.prompt_feedback
            result["prompt_feedback"] = {
                "block_reason": str(getattr(pf, "block_reason", None)) if getattr(pf, "block_reason", None) else None,
                "safety_ratings": None,  # Skip complex nested objects for now
            }
        
        return result
        
    except Exception as e:
        # Fallback: try to extract text content at minimum
        try:
            text = None
            if hasattr(response, "text"):
                text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                first_candidate = response.candidates[0]
                if hasattr(first_candidate, "content"):
                    content = first_candidate.content
                    if hasattr(content, "parts") and content.parts:
                        text = content.parts[0].text if hasattr(content.parts[0], "text") else None
            
            return {
                "candidates": [{"content": {"parts": [{"text": str(text) if text else None}]}}] if text else [],
                "usage_metadata": {},
                "error": f"Partial serialization: {str(e)}"
            }
        except:
            # Last resort: return minimal structure
            return {
                "candidates": [],
                "usage_metadata": {},
                "error": f"Failed to serialize response: {str(e)}"
            }


class CrucibleGenAIModelWrapper:
    """Wrapper for GenAI GenerativeModel with Crucible logging."""
    
    def __init__(self, model, crucible_logger: CrucibleLogger):
        self.model = model
        self.crucible_logger = crucible_logger
        self.streaming_merger = StreamingMerger()
    
    def generate_content(self, *args, **kwargs) -> Union[GenerateContentResponse, Iterator[GenerateContentResponse]]:
        """Generate content with Crucible logging."""
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
            
            # Make the actual GenAI API call
            response = self.model.generate_content(*args, **filtered_kwargs)
            
            # Handle streaming vs non-streaming
            if kwargs.get("stream", False) or isinstance(response, Iterator):
                return self._handle_streaming(response, request_data, requested_at, metadata)
            else:
                return self._handle_non_streaming(response, request_data, requested_at, metadata)
                
        except Exception as e:
            # Log error
            self._log_error(e, request_data, requested_at, metadata)
            raise e
    
    def _handle_streaming(self, stream: Iterator[GenerateContentResponse], request_data: Dict[str, Any], 
                         requested_at: int, metadata: Dict[str, Any]) -> Iterator[GenerateContentResponse]:
        """Handle streaming completion."""
        assembled_response = None
        
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
                self.assembled_response = None
                self.chunks = []
                
            def __iter__(self):
                return self
                
            def __next__(self):
                try:
                    chunk = next(self.original_stream)
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
                except StopIteration:
                    # Log the complete response after streaming finishes
                    if self.assembled_response:
                        self.log_success(self.assembled_response, self.request_data, self.requested_at, self.metadata)
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
    
    def _handle_non_streaming(self, response: GenerateContentResponse, request_data: Dict[str, Any], 
                             requested_at: int, metadata: Dict[str, Any]) -> GenerateContentResponse:
        """Handle non-streaming completion."""
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


class CrucibleGenAIModelsWrapper:
    """Wrapper for GenAI models API with Crucible logging."""
    
    def __init__(self, genai_module, crucible_logger: CrucibleLogger):
        self.genai_module = genai_module
        self.crucible_logger = crucible_logger
        self.streaming_merger = StreamingMerger()
        self._logged_requests = set()  # Track logged requests to prevent duplicates
    
    def generate_content(self, model: str, contents: Any, **kwargs) -> Union[GenerateContentResponse, Iterator[GenerateContentResponse]]:
        """
        Generate content with Crucible logging.
        
        Args:
            model: Model name (e.g., 'gemini-2.5-flash')
            contents: Content to generate from
            **kwargs: Additional arguments including crucible_metadata
        """
        # Extract Crucible metadata
        metadata = kwargs.pop("crucible_metadata", {})
        
        # Record request start time
        requested_at = int(time.time() * 1000)
        
        # Create a unique request ID to prevent double logging
        request_id = str(uuid.uuid4())
        
        # Prepare request data for logging
        # Serialize contents safely
        serialized_contents = contents
        if isinstance(contents, str):
            serialized_contents = contents
        elif isinstance(contents, (list, dict)):
            serialized_contents = contents
        else:
            # Try to convert complex objects to string
            try:
                serialized_contents = str(contents)
            except:
                serialized_contents = None
        
        request_data = {
            "model": model,
            "contents": serialized_contents,
            "generation_config": kwargs.get("generation_config"),
            "safety_settings": kwargs.get("safety_settings"),
            "tools": kwargs.get("tools"),
            "tool_config": kwargs.get("tool_config"),
            "stream": kwargs.get("stream", False),
        }
        
        # Remove None values and ensure all values are JSON-serializable
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        # Test JSON serialization of request_data
        try:
            json.dumps(request_data)
        except (TypeError, ValueError):
            # If serialization fails, simplify the request_data
            request_data = {
                "model": model,
                "contents": str(contents) if contents else None,
                "stream": kwargs.get("stream", False),
            }
            request_data = {k: v for k, v in request_data.items() if v is not None}
        
        try:
            # Filter out Crucible-specific kwargs
            filtered_kwargs = {k: v for k, v in kwargs.items() 
                             if not k.startswith('_crucible') and k != 'crucible_metadata'}
            
            # Create model and generate content
            genai_model = self.genai_module.GenerativeModel(model)
            
            # Ensure stream is passed correctly
            if kwargs.get("stream", False):
                filtered_kwargs["stream"] = True
            
            response = genai_model.generate_content(contents, **filtered_kwargs)
            
            # Handle streaming vs non-streaming
            is_streaming = kwargs.get("stream", False)
            if is_streaming:
                # When streaming=True, GenAI should return a generator/iterator
                # Try to detect if it's actually a stream
                import types
                
                # Check multiple ways to detect a stream
                is_generator = isinstance(response, types.GeneratorType)
                is_abc_iterator = isinstance(response, ABCIterator)
                has_next_method = hasattr(response, '__next__')
                
                # Check if it's NOT a GenerateContentResponse type (which might be iterable but not a stream)
                response_type_name = type(response).__name__
                is_response_type = 'GenerateContentResponse' in response_type_name
                
                # If it's a generator or ABCIterator, definitely a stream
                # If it has __next__ and is NOT a GenerateContentResponse, likely a stream
                if is_generator or is_abc_iterator or (has_next_method and not is_response_type):
                    try:
                        # Try to handle as streaming
                        return self._handle_streaming(response, request_data, requested_at, metadata, request_id)
                    except (TypeError, AttributeError) as e:
                        # If streaming handling fails, fall back to non-streaming
                        # This can happen if GenAI returns a single response even with stream=True
                        handle_logging_error(Exception(f"Streaming detection failed, treating as non-streaming: {e}"), "streaming_detection")
                        return self._handle_non_streaming(response, request_data, requested_at, metadata, request_id)
                else:
                    # Not detected as a stream, treat as non-streaming
                    # This might happen if GenAI's API changed or returns differently
                    return self._handle_non_streaming(response, request_data, requested_at, metadata, request_id)
            
            return self._handle_non_streaming(response, request_data, requested_at, metadata, request_id)
                
        except Exception as e:
            # Log error
            self._log_error(e, request_data, requested_at, metadata, request_id)
            raise e
    
    def _handle_streaming(self, stream, request_data: Dict[str, Any], 
                         requested_at: int, metadata: Dict[str, Any], request_id: str):
        """Handle streaming completion."""
        assembled_response = None
        
        class LoggingStreamWrapper:
            def __init__(self, original_stream, merger, log_success, log_error, request_data, requested_at, metadata, request_id):
                self.original_stream = original_stream
                self.merger = merger
                self.log_success = log_success
                self.log_error = log_error
                self.request_data = request_data
                self.requested_at = requested_at
                self.metadata = metadata
                self.request_id = request_id
                self.assembled_response = None
                self.chunks = []
                self._logged = False  # Prevent double logging
                self._iterator = None
                
            def __iter__(self):
                return self
                
            def __next__(self):
                try:
                    # Get iterator if we haven't already
                    if self._iterator is None:
                        # Check if original_stream is already an iterator/generator
                        if hasattr(self.original_stream, '__next__'):
                            self._iterator = self.original_stream
                        elif hasattr(self.original_stream, '__iter__'):
                            # Try to create iterator from it
                            try:
                                self._iterator = iter(self.original_stream)
                                # Verify it's actually an iterator
                                if not hasattr(self._iterator, '__next__'):
                                    raise TypeError("Response is not iterable as chunks")
                            except TypeError:
                                # Not iterable, this shouldn't happen with stream=True
                                raise TypeError(f"Stream response is not iterable: {type(self.original_stream)}")
                        else:
                            raise TypeError(f"Stream response is not iterable: {type(self.original_stream)}")
                    
                    chunk = next(self._iterator)
                    self.chunks.append(chunk)
                    
                    # Try to merge chunks for final logging
                    if self.assembled_response is None:
                        self.assembled_response = chunk
                    else:
                        # Merge candidates if available
                        if hasattr(chunk, "candidates") and chunk.candidates:
                            if not hasattr(self.assembled_response, "candidates"):
                                self.assembled_response.candidates = []
                            if hasattr(self.assembled_response, "candidates"):
                                self.assembled_response.candidates.extend(chunk.candidates)
                    
                    return chunk
                except StopIteration:
                    # Log the complete response after streaming finishes
                    if self.assembled_response and not self._logged:
                        self._logged = True
                        self.log_success(self.assembled_response, self.request_data, self.requested_at, self.metadata, self.request_id)
                    raise
                except TypeError as e:
                    # If we get TypeError, it means the stream isn't actually iterable
                    # Log the error and re-raise
                    if not self._logged:
                        self._logged = True
                        self.log_error(e, self.request_data, self.requested_at, self.metadata, self.request_id)
                    raise
                except Exception as e:
                    if not self._logged:
                        self._logged = True
                        self.log_error(e, self.request_data, self.requested_at, self.metadata, self.request_id)
                    raise
        
        return LoggingStreamWrapper(
            stream, 
            self.streaming_merger, 
            self._log_success, 
            self._log_error, 
            request_data, 
            requested_at, 
            metadata,
            request_id
        )
    
    def _handle_non_streaming(self, response: GenerateContentResponse, request_data: Dict[str, Any], 
                             requested_at: int, metadata: Dict[str, Any], request_id: str) -> GenerateContentResponse:
        """Handle non-streaming completion."""
        self._log_success(response, request_data, requested_at, metadata, request_id)
        return response
    
    def _log_success(self, response: GenerateContentResponse, request_data: Dict[str, Any], 
                    requested_at: int, metadata: Dict[str, Any], request_id: str) -> None:
        """Log successful completion."""
        # Check if we've already logged this request
        if request_id in self._logged_requests:
            return  # Already logged, skip
        
        try:
            received_at = int(time.time() * 1000)
            response_data = get_genai_response_json(response)
            
            # Ensure response_data is JSON-serializable
            try:
                # Test serialization
                json.dumps(response_data)
            except (TypeError, ValueError) as e:
                # If response_data contains non-serializable objects, extract text only
                text = None
                if isinstance(response_data, dict) and response_data.get("candidates"):
                    first_candidate = response_data["candidates"][0] if response_data["candidates"] else {}
                    if first_candidate.get("content", {}).get("parts"):
                        first_part = first_candidate["content"]["parts"][0] if first_candidate["content"]["parts"] else {}
                        text = first_part.get("text")
                
                response_data = {
                    "candidates": [{"content": {"parts": [{"text": str(text) if text else None}]}}] if text else [],
                    "usage_metadata": {},
                    "serialization_note": "Simplified due to serialization error"
                }
            
            log_request = LogRequest.from_genai_call(
                request_data=request_data,
                response_data=response_data,
                requested_at=requested_at,
                received_at=received_at,
                status_code=200,
                metadata=metadata,
            )
            
            json_data = json.dumps(log_request.to_dict())
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('ascii')
            
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
            
            # Mark as logged before queuing to prevent race conditions
            self._logged_requests.add(request_id)
            
            # Clean up old request IDs (keep only last 1000 to prevent memory issues)
            if len(self._logged_requests) > 1000:
                # Remove oldest entries (simple approach: clear and rebuild)
                self._logged_requests = set(list(self._logged_requests)[-500:])
            
            self.crucible_logger.log_request(encoded_log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_success")
            # Remove from logged set on error so it can be retried
            self._logged_requests.discard(request_id)
    
    def _log_error(self, error: Exception, request_data: Dict[str, Any], 
                  requested_at: int, metadata: Dict[str, Any], request_id: str) -> None:
        """Log error completion."""
        # Check if we've already logged this request
        if request_id in self._logged_requests:
            return  # Already logged, skip
        
        try:
            received_at = int(time.time() * 1000)
            error_message = str(error)
            status_code = getattr(error, 'status_code', None) or getattr(error, 'code', None)
            
            log_request = LogRequest.from_genai_call(
                request_data=request_data,
                response_data=None,
                requested_at=requested_at,
                received_at=received_at,
                status_code=status_code,
                error_message=error_message,
                metadata=metadata,
            )
            
            json_data = json.dumps(log_request.to_dict())
            encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('ascii')
            
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
            
            # Mark as logged
            self._logged_requests.add(request_id)
            
            self.crucible_logger.log_request(encoded_log_request)
            
        except Exception as e:
            handle_logging_error(e, "log_error")
            # Remove from logged set on error
            self._logged_requests.discard(request_id)


class CrucibleGenAI:
    """
    Crucible wrapper for Google GenAI client.
    
    Provides seamless integration with Google's Generative AI API while automatically
    logging requests and responses to Crucible warehouse.
    """
    
    def __init__(self, api_key: Optional[str] = None, domain: Optional[str] = None, 
                 genai_api_key: Optional[str] = None, **genai_kwargs):
        """
        Initialize Crucible GenAI client.
        
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
        
        # Create models wrapper
        self.models = CrucibleGenAIModelsWrapper(self.genai_module, self.crucible_logger)
    
    def GenerativeModel(self, model_name: str, **kwargs):
        """
        Create a GenerativeModel with Crucible logging.
        
        Args:
            model_name: Name of the model to use
            **kwargs: Additional arguments for GenerativeModel
            
        Returns:
            CrucibleGenAIModelWrapper instance
        """
        model = self.genai_module.GenerativeModel(model_name, **kwargs)
        return CrucibleGenAIModelWrapper(model, self.crucible_logger)
    
    def __getattr__(self, name):
        """Delegate unknown attributes to GenAI module."""
        return getattr(self.genai_module, name)
    
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

