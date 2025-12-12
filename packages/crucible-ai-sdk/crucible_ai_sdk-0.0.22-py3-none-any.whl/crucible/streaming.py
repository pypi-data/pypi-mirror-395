"""
Streaming chunk merger for Crucible SDK.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json
import sys

from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
from openai.types.chat.chat_completion_message_tool_call import Function as ToolCallFunction

from .errors import SerializationError


@dataclass
class MemoryStats:
    """Memory usage statistics for streaming."""
    
    current_size: int = 0
    max_size: int = 0
    chunk_count: int = 0
    total_chunks_processed: int = 0
    
    def update_size(self, size: int) -> None:
        """Update current size and track maximum."""
        self.current_size = size
        self.max_size = max(self.max_size, size)
    
    def increment_chunks(self) -> None:
        """Increment chunk count."""
        self.chunk_count += 1
        self.total_chunks_processed += 1
    
    def reset(self) -> None:
        """Reset statistics."""
        self.current_size = 0
        self.chunk_count = 0


class StreamingMerger:
    """
    Memory-efficient streaming chunk merger.
    
    Merges OpenAI streaming chunks into complete ChatCompletion objects
    while monitoring memory usage and providing compression when needed.
    """
    
    def __init__(self, max_memory_mb: int = 50):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.stats = MemoryStats()
        self.compression_threshold = 0.8  # Compress when 80% of limit reached
    
    def merge_chunk(self, base: Optional[ChatCompletion], chunk: ChatCompletionChunk) -> ChatCompletion:
        """
        Merge a streaming chunk into the base completion.
        
        Args:
            base: Existing completion object (None for first chunk)
            chunk: New chunk to merge
            
        Returns:
            Updated completion object
        """
        if base is None:
            base = self._create_base_completion(chunk)
        
        # Update statistics
        self.stats.increment_chunks()
        
        # Merge choices
        for choice in chunk.choices:
            base_choice = self._find_choice_by_index(base.choices, choice.index)
            
            if base_choice:
                self._merge_choice(base_choice, choice)
            else:
                base.choices.append(self._create_new_choice(choice))
        
        # Check memory usage
        self._check_memory_usage(base)
        
        return base
    
    def _create_base_completion(self, chunk: ChatCompletionChunk) -> ChatCompletion:
        """Create base completion from first chunk."""
        return ChatCompletion(
            id=chunk.id,
            choices=[],
            created=chunk.created,
            model=chunk.model,
            object="chat.completion",
            system_fingerprint=chunk.system_fingerprint,
        )
    
    def _find_choice_by_index(self, choices: List[Choice], index: int) -> Optional[Choice]:
        """Find choice by index."""
        for choice in choices:
            if choice.index == index:
                return choice
        return None
    
    def _merge_choice(self, base_choice: Choice, chunk_choice) -> None:
        """Merge chunk choice into base choice."""
        # Update finish reason
        if chunk_choice.finish_reason:
            base_choice.finish_reason = chunk_choice.finish_reason
        
        # Merge content
        if chunk_choice.delta and chunk_choice.delta.content:
            if base_choice.message.content is None:
                base_choice.message.content = ""
            base_choice.message.content += chunk_choice.delta.content
        
        # Merge function calls
        if chunk_choice.delta and chunk_choice.delta.function_call:
            self._merge_function_call(base_choice, chunk_choice.delta.function_call)
        
        # Merge tool calls
        if chunk_choice.delta and chunk_choice.delta.tool_calls:
            self._merge_tool_calls(base_choice, chunk_choice.delta.tool_calls)
        
        # Update logprobs
        if chunk_choice.logprobs:
            base_choice.logprobs = chunk_choice.logprobs
    
    def _merge_function_call(self, base_choice: Choice, delta_function_call) -> None:
        """Merge function call delta."""
        if base_choice.message.function_call is None:
            base_choice.message.function_call = type('FunctionCall', (), {
                'name': '',
                'arguments': ''
            })()
        
        if delta_function_call.name:
            base_choice.message.function_call.name += delta_function_call.name
        
        if delta_function_call.arguments:
            base_choice.message.function_call.arguments += delta_function_call.arguments
    
    def _merge_tool_calls(self, base_choice: Choice, delta_tool_calls: List[ChoiceDeltaToolCall]) -> None:
        """Merge tool call deltas."""
        if base_choice.message.tool_calls is None:
            base_choice.message.tool_calls = []
        
        for delta_tool_call in delta_tool_calls:
            if delta_tool_call.function.name:
                # New tool call
                tool_call = ChatCompletionMessageToolCall(
                    id=delta_tool_call.id,
                    type="function",
                    function=ToolCallFunction(
                        name=delta_tool_call.function.name,
                        arguments=delta_tool_call.function.arguments or ""
                    )
                )
                base_choice.message.tool_calls.append(tool_call)
            else:
                # Continue existing tool call
                if base_choice.message.tool_calls:
                    last_tool_call = base_choice.message.tool_calls[-1]
                    if delta_tool_call.function.arguments:
                        last_tool_call.function.arguments += delta_tool_call.function.arguments
    
    def _create_new_choice(self, chunk_choice) -> Choice:
        """Create new choice from chunk choice."""
        message = ChatCompletionMessage(
            role="assistant",
            content=chunk_choice.delta.content or "",
            function_call=chunk_choice.delta.function_call,
            tool_calls=chunk_choice.delta.tool_calls,
        )
        
        return Choice(
            index=chunk_choice.index,
            message=message,
            finish_reason=chunk_choice.finish_reason or "length",
            logprobs=chunk_choice.logprobs,
        )
    
    def _check_memory_usage(self, completion: ChatCompletion) -> None:
        """Check memory usage and compress if needed."""
        try:
            # Estimate memory usage by serializing
            size = len(json.dumps(completion.dict()))
            self.stats.update_size(size)
            
            # Compress if approaching limit
            if size > self.max_memory_bytes * self.compression_threshold:
                self._compress_completion(completion)
                
        except Exception as e:
            # If we can't estimate size, just continue
            pass
    
    def _compress_completion(self, completion: ChatCompletion) -> None:
        """Compress completion to reduce memory usage."""
        try:
            # For now, just truncate very long content
            for choice in completion.choices:
                if choice.message.content and len(choice.message.content) > 10000:
                    choice.message.content = choice.message.content[:10000] + "...[truncated]"
                    
        except Exception as e:
            raise SerializationError(f"Failed to compress completion: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get streaming statistics."""
        return {
            "current_size": self.stats.current_size,
            "max_size": self.stats.max_size,
            "chunk_count": self.stats.chunk_count,
            "total_chunks_processed": self.stats.total_chunks_processed,
            "memory_limit_mb": self.max_memory_bytes // (1024 * 1024),
            "compression_threshold": self.compression_threshold,
        }
    
    def reset_stats(self) -> None:
        """Reset streaming statistics."""
        self.stats.reset()


def get_chat_completion_json(completion: ChatCompletion) -> Dict[str, Any]:
    """
    Convert ChatCompletion to JSON-serializable dictionary.
    
    Args:
        completion: ChatCompletion object
        
    Returns:
        JSON-serializable dictionary
    """
    try:
        # Use OpenAI's built-in serialization
        return completion.dict()
    except Exception:
        # Fallback manual serialization
        try:
            return {
                "id": completion.id,
                "object": completion.object,
                "created": completion.created,
                "model": completion.model,
                "choices": [
                    {
                        "index": choice.index,
                        "message": {
                            "role": choice.message.role,
                            "content": choice.message.content,
                            "function_call": choice.message.function_call,
                            "tool_calls": choice.message.tool_calls,
                        },
                        "finish_reason": choice.finish_reason,
                        "logprobs": choice.logprobs,
                    }
                    for choice in completion.choices
                ],
                "usage": completion.usage,
                "system_fingerprint": completion.system_fingerprint,
            }
        except Exception as e:
            raise SerializationError(f"Failed to serialize ChatCompletion: {e}")


def estimate_memory_usage(obj: Any) -> int:
    """
    Estimate memory usage of an object.
    
    Args:
        obj: Object to estimate
        
    Returns:
        Estimated size in bytes
    """
    try:
        return sys.getsizeof(obj)
    except Exception:
        return 0
