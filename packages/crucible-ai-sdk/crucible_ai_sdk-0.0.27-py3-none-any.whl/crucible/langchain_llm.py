import os
from typing import Dict, Any, List, Union, Optional, Callable

try:
    from langchain_openai import ChatOpenAI as ChatOpenAIBase
except ImportError:
    # Try fallback to langchain_community for older versions
    try:
        from langchain_community.chat_models.openai import ChatOpenAI as ChatOpenAIBase
    except ImportError:
        # langchain_openai or langchain_community is required
        ChatOpenAIBase = None

from pydantic import BaseModel, Field

from .client import CrucibleOpenAI, CrucibleCompletionsWrapper
from .async_client import CrucibleAsyncOpenAI, CrucibleAsyncCompletionsWrapper


class LangChainMetadataCompletionsWrapper:
    """Wrapper that injects metadata from LangChain instance into Crucible completions."""
    
    def __init__(self, crucible_completions_wrapper: CrucibleCompletionsWrapper, langchain_instance):
        self.crucible_wrapper = crucible_completions_wrapper
        self.langchain_instance = langchain_instance
        # Store reference to original wrapper for direct access
        self._original_wrapper = crucible_completions_wrapper
    
    def __call__(self, *args, **kwargs):
        """Make wrapper callable if needed."""
        return self.create(*args, **kwargs)
    
    def create(self, *args, **kwargs):
        """Create completion with automatic metadata injection."""
        # Get metadata from LangChain instance
        metadata = {}
        
        # Get stored metadata
        if hasattr(self.langchain_instance, "_crucible_metadata"):
            metadata.update(self.langchain_instance._crucible_metadata)
        
        # Get current metadata (set by invoke/ainvoke)
        if hasattr(self.langchain_instance, "_current_metadata"):
            metadata.update(self.langchain_instance._current_metadata)
        
        # Merge with any metadata passed directly
        if "crucible_metadata" in kwargs:
            metadata.update(kwargs.pop("crucible_metadata", {}))
        
        # Add metadata to kwargs
        kwargs["crucible_metadata"] = metadata
        
        # Call the Crucible wrapper
        return self.crucible_wrapper.create(*args, **kwargs)
    
    def __getattr__(self, name):
        """Delegate other attributes to the Crucible wrapper."""
        attr = getattr(self.crucible_wrapper, name)
        # If it's a method, wrap it to inject metadata
        if callable(attr) and name != 'create':
            def wrapper(*args, **kwargs):
                # Inject metadata for any method calls
                metadata = {}
                if hasattr(self.langchain_instance, "_crucible_metadata"):
                    metadata.update(self.langchain_instance._crucible_metadata)
                if hasattr(self.langchain_instance, "_current_metadata"):
                    metadata.update(self.langchain_instance._current_metadata)
                if "crucible_metadata" in kwargs:
                    metadata.update(kwargs.pop("crucible_metadata", {}))
                kwargs["crucible_metadata"] = metadata
                return attr(*args, **kwargs)
            return wrapper
        return attr


class LangChainMetadataAsyncCompletionsWrapper:
    """Wrapper that injects metadata from LangChain instance into Crucible async completions."""
    
    def __init__(self, crucible_async_completions_wrapper: CrucibleAsyncCompletionsWrapper, langchain_instance):
        self.crucible_wrapper = crucible_async_completions_wrapper
        self.langchain_instance = langchain_instance
    
    async def create(self, *args, **kwargs):
        """Create completion with automatic metadata injection."""
        # Get metadata from LangChain instance
        metadata = {}
        
        # Get stored metadata
        if hasattr(self.langchain_instance, "_crucible_metadata"):
            metadata.update(self.langchain_instance._crucible_metadata)
        
        # Get current metadata (set by invoke/ainvoke)
        if hasattr(self.langchain_instance, "_current_metadata"):
            metadata.update(self.langchain_instance._current_metadata)
        
        # Merge with any metadata passed directly
        if "crucible_metadata" in kwargs:
            metadata.update(kwargs.pop("crucible_metadata", {}))
        
        # Add metadata to kwargs
        kwargs["crucible_metadata"] = metadata
        
        # Call the Crucible wrapper
        return await self.crucible_wrapper.create(*args, **kwargs)
    
    def __getattr__(self, name):
        """Delegate other attributes to the Crucible wrapper."""
        return getattr(self.crucible_wrapper, name)

# Try to import BaseTool for type hints
try:
    from langchain_core.tools import BaseTool
except ImportError:
    BaseTool = object  # Fallback if not available

# Handle both old and new LangChain import paths
try:
    from langchain_core.runnables import RunnableLambda, Runnable
except ImportError:
    try:
        from langchain.schema.runnable import RunnableLambda, Runnable
    except ImportError:
        # Fallback: RunnableLambda might not be needed if bind_metadata isn't used
        RunnableLambda = None
        try:
            from langchain_core.runnables.base import Runnable
        except ImportError:
            Runnable = object  # Fallback to object if Runnable not available


if ChatOpenAIBase is None:
    # Create a placeholder class that raises a helpful error
    class ChatOpenAI:
        """
        LangChain ChatOpenAI wrapper for Crucible.
        
        This class requires langchain-community to be installed.
        Install it with: pip install langchain-community
        """
        def __init__(self, **kwargs):
            raise ImportError(
                "langchain_community is required to use ChatOpenAI. "
                "Please install it with: pip install langchain-community"
            )
else:
    class ChatOpenAI(ChatOpenAIBase):
        """
        LangChain ChatOpenAI wrapper for Crucible.
        
        Provides seamless integration with LangChain while automatically
        logging requests and responses to Crucible warehouse.
        """
        
        crucible_kwargs: Dict[str, Any] = Field(
            default_factory=lambda: {"verify_ssl": False}
        )

        def __init__(self, **kwargs):
            """Initialize the ChatOpenAI with Crucible client."""
            # Extract Crucible configuration before calling super()
            crucible_kwargs = kwargs.pop('crucible_kwargs', {})
            
            # Call parent constructor
            super().__init__(**kwargs)
            
            # Initialize metadata storage (always initialize, even if Crucible not configured)
            self._crucible_metadata = crucible_kwargs.get('crucible_metadata', {}) if crucible_kwargs else {}
            
            # Create Crucible client if configuration provided
            self._crucible_client = None
            if crucible_kwargs:
                crucible_api_key = crucible_kwargs.get('api_key') or os.getenv('CRUCIBLE_API_KEY')
                crucible_domain = crucible_kwargs.get('domain') or os.getenv('CRUCIBLE_DOMAIN', 'warehouse.usecrucible.ai')
                
                if crucible_api_key:
                    # Create Crucible sync client
                    immediate_flush = crucible_kwargs.get('immediate_flush', False)
                    self._crucible_client = CrucibleOpenAI(
                        api_key=crucible_api_key,
                        domain=crucible_domain,
                        immediate_flush=immediate_flush
                    )
                    
                    # Replace the sync client with Crucible's wrapped client
                    # Monkey-patch the CrucibleCompletionsWrapper to inject metadata
                    crucible_completions = self._crucible_client.chat.completions
                    
                    # Store reference to LangChain instance in the Crucible wrapper
                    crucible_completions._langchain_instance = self
                    
                    # Monkey-patch the create method to inject metadata
                    original_create = crucible_completions.create
                    def create_with_metadata(*args, **kwargs):
                        # Get metadata from LangChain instance
                        metadata = {}
                        langchain_instance = getattr(crucible_completions, '_langchain_instance', None)
                        if langchain_instance:
                            if hasattr(langchain_instance, "_crucible_metadata"):
                                metadata.update(langchain_instance._crucible_metadata)
                            if hasattr(langchain_instance, "_current_metadata"):
                                metadata.update(langchain_instance._current_metadata)
                        # Merge with any metadata passed directly
                        if "crucible_metadata" in kwargs:
                            metadata.update(kwargs.pop("crucible_metadata", {}))
                        kwargs["crucible_metadata"] = metadata
                        return original_create(*args, **kwargs)
                    
                    crucible_completions.create = create_with_metadata
                    self.client = crucible_completions
                    
                    # Set up async client - simple monkey-patch like sync
                    self._crucible_async_client = CrucibleAsyncOpenAI(
                        api_key=crucible_api_key,
                        domain=crucible_domain
                    )
                    crucible_async_completions = self._crucible_async_client.chat.completions
                    crucible_async_completions._langchain_instance = self
                    
                    # Simple monkey-patch for async (same as sync)
                    original_async_create = crucible_async_completions.create
                    async def create_with_metadata_async(*args, **kwargs):
                        metadata = {}
                        langchain_instance = getattr(crucible_async_completions, '_langchain_instance', None)
                        if langchain_instance:
                            if hasattr(langchain_instance, "_crucible_metadata"):
                                metadata.update(langchain_instance._crucible_metadata)
                            if hasattr(langchain_instance, "_current_metadata"):
                                metadata.update(langchain_instance._current_metadata)
                        if "crucible_metadata" in kwargs:
                            metadata.update(kwargs.pop("crucible_metadata", {}))
                        kwargs["crucible_metadata"] = metadata
                        return await original_async_create(*args, **kwargs)
                    
                    crucible_async_completions.create = create_with_metadata_async
                    self.async_client = crucible_async_completions

    def bind_metadata(self, **kwargs):
        """Bind metadata to the LLM for use in chains."""
        # Store metadata for use in chains
        if not hasattr(self, "_crucible_metadata"):
            self._crucible_metadata = {}
        
        self._crucible_metadata.update(kwargs)
        
        # Return a wrapper that injects metadata
        def metadata_injector(input_data):
            return self.invoke(input_data, crucible_metadata=self._crucible_metadata)
        
        if RunnableLambda is not None:
            return RunnableLambda(metadata_injector)
        else:
            # Fallback: return a simple callable if RunnableLambda is not available
            return metadata_injector

    def with_metadata(self, **kwargs) -> "ChatOpenAI":
        """
        Add metadata to be sent with Crucible requests.
        
        Args:
            **kwargs: Metadata key-value pairs
            
        Returns:
            ChatOpenAI instance with metadata
        """
        # Store metadata for use in invoke/ainvoke methods
        if not hasattr(self, "_crucible_metadata"):
            self._crucible_metadata = {}
        
        self._crucible_metadata.update(kwargs)
        
        return self

    def bind_tools(
        self,
        tools: List[Union[BaseTool, Callable, dict]],
        tool_choice: Optional[Union[str, dict]] = None,
        **kwargs
    ) -> "ChatOpenAI":
        """
        Bind tools to the model for function calling.
        
        This method enables the model to use tools/functions during generation,
        which is required for LangGraph agents and other tool-using workflows.
        
        Args:
            tools: List of tools to bind. Can be LangChain BaseTool instances,
                   callables, or dictionaries in OpenAI tool format.
            tool_choice: Optional tool choice parameter. Can be:
                        - "required": Model must call a tool
                        - "auto": Model decides whether to call tools
                        - dict: Specific tool choice configuration
            **kwargs: Additional arguments passed to parent bind_tools if available
            
        Returns:
            A new ChatOpenAI instance with tools bound, preserving Crucible integration
        """
        # Try to use parent's bind_tools if available (for newer LangChain versions)
        parent_class = self.__class__.__bases__[0]  # Get ChatOpenAIBase
        if hasattr(parent_class, 'bind_tools'):
            try:
                # Call parent's bind_tools
                bound_model = super().bind_tools(tools, tool_choice=tool_choice, **kwargs)
                
                # Create a new Crucible wrapper instance with the bound model's state
                # but preserve Crucible-specific attributes
                import copy
                new_instance = copy.copy(self)
                
                # Copy all attributes from bound_model (this updates the instance with bound state)
                for attr, value in bound_model.__dict__.items():
                    # Skip Crucible-specific attributes that we want to preserve
                    if attr not in ['_crucible_client', '_crucible_metadata']:
                        setattr(new_instance, attr, value)
                
                # Ensure Crucible client is still used
                if hasattr(self, "_crucible_client") and self._crucible_client:
                    new_instance._crucible_client = self._crucible_client
                    new_instance.client = self._crucible_client.chat.completions
                
                # Preserve metadata
                if hasattr(self, "_crucible_metadata"):
                    if not hasattr(new_instance, "_crucible_metadata"):
                        new_instance._crucible_metadata = {}
                    new_instance._crucible_metadata.update(self._crucible_metadata)
                
                return new_instance
            except (NotImplementedError, AttributeError, TypeError):
                # Parent doesn't have bind_tools or it's not implemented, fall through to manual implementation
                pass
        
        # Manual implementation: convert tools to OpenAI format and store them
        try:
            from langchain_core.utils.function_calling import convert_to_openai_tool
        except ImportError:
            # Fallback: manual conversion
            def convert_to_openai_tool(tool):
                """Convert tool to OpenAI format."""
                if isinstance(tool, dict):
                    # Already in OpenAI format
                    if "type" in tool and tool["type"] == "function":
                        return tool
                    # Try to convert from other formats
                    return {
                        "type": "function",
                        "function": tool
                    }
                elif hasattr(tool, 'name') and hasattr(tool, 'description'):
                    # LangChain BaseTool
                    return {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.args_schema.model_json_schema() if hasattr(tool, 'args_schema') and tool.args_schema else {}
                        }
                    }
                elif callable(tool):
                    # Callable - try to extract info from docstring
                    import inspect
                    sig = inspect.signature(tool)
                    doc = inspect.getdoc(tool) or ""
                    return {
                        "type": "function",
                        "function": {
                            "name": tool.__name__,
                            "description": doc.split('\n')[0] if doc else "",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    param.name: {"type": "string"}  # Default to string
                                    for param in sig.parameters.values()
                                    if param.name != 'self'
                                }
                            }
                        }
                    }
                else:
                    raise ValueError(f"Unable to convert tool {tool} to OpenAI format")
        
        # Convert all tools to OpenAI format
        openai_tools = []
        for tool in tools:
            try:
                if isinstance(tool, dict) and "type" in tool:
                    # Already in OpenAI format
                    openai_tools.append(tool)
                else:
                    # Convert using utility
                    converted = convert_to_openai_tool(tool)
                    openai_tools.append(converted)
            except Exception as e:
                # If conversion fails, try direct conversion
                try:
                    converted = convert_to_openai_tool(tool)
                    openai_tools.append(converted)
                except Exception:
                    raise ValueError(f"Failed to convert tool {tool} to OpenAI format: {e}")
        
        # Create a copy of the current instance
        import copy
        new_instance = copy.copy(self)
        
        # Store bound tools and tool_choice using object.__setattr__ to bypass Pydantic validation
        object.__setattr__(new_instance, '_bound_tools', openai_tools)
        object.__setattr__(new_instance, '_tool_choice', tool_choice)
        
        # Override invoke, ainvoke, _generate, and _agenerate to include tools
        # Use object.__setattr__ to bypass Pydantic's field validation
        original_invoke = new_instance.invoke
        original_ainvoke = new_instance.ainvoke
        original_generate = new_instance._generate
        # Capture _agenerate if it exists (for async support)
        original_agenerate = getattr(new_instance, '_agenerate', None)
        
        def invoke_with_tools(input, config=None, **invoke_kwargs):
            """Invoke with bound tools."""
            # Add tools to kwargs if not already present
            if "tools" not in invoke_kwargs:
                invoke_kwargs["tools"] = new_instance._bound_tools
            if "tool_choice" not in invoke_kwargs and new_instance._tool_choice is not None:
                invoke_kwargs["tool_choice"] = new_instance._tool_choice
            
            # Preserve metadata from stored metadata
            if hasattr(new_instance, "_crucible_metadata") and new_instance._crucible_metadata:
                invoke_kwargs.setdefault("crucible_metadata", {})
                invoke_kwargs["crucible_metadata"].update(new_instance._crucible_metadata)
            
            return original_invoke(input, config=config, **invoke_kwargs)
        
        async def ainvoke_with_tools(input, config=None, **invoke_kwargs):
            """Async invoke with bound tools."""
            # Add tools to kwargs if not already present
            if "tools" not in invoke_kwargs:
                invoke_kwargs["tools"] = new_instance._bound_tools
            if "tool_choice" not in invoke_kwargs and new_instance._tool_choice is not None:
                invoke_kwargs["tool_choice"] = new_instance._tool_choice
            
            # Preserve metadata from stored metadata
            if hasattr(new_instance, "_crucible_metadata") and new_instance._crucible_metadata:
                invoke_kwargs.setdefault("crucible_metadata", {})
                invoke_kwargs["crucible_metadata"].update(new_instance._crucible_metadata)
            
            return await original_ainvoke(input, config=config, **invoke_kwargs)
        
        def generate_with_tools(messages, stop=None, run_manager=None, **generate_kwargs):
            """Generate with bound tools."""
            # Add tools to kwargs if not already present
            if "tools" not in generate_kwargs:
                generate_kwargs["tools"] = new_instance._bound_tools
            if "tool_choice" not in generate_kwargs and new_instance._tool_choice is not None:
                generate_kwargs["tool_choice"] = new_instance._tool_choice
            
            # Preserve metadata from stored metadata
            if hasattr(new_instance, "_crucible_metadata") and new_instance._crucible_metadata:
                generate_kwargs.setdefault("crucible_metadata", {})
                generate_kwargs["crucible_metadata"].update(new_instance._crucible_metadata)
            
            return original_generate(messages, stop=stop, run_manager=run_manager, **generate_kwargs)
        
        async def agenerate_with_tools(messages, stop=None, run_manager=None, **generate_kwargs):
            """Async generate with bound tools."""
            
            # Add tools to kwargs if not already present
            if "tools" not in generate_kwargs:
                generate_kwargs["tools"] = new_instance._bound_tools
                
            if "tool_choice" not in generate_kwargs and new_instance._tool_choice is not None:
                generate_kwargs["tool_choice"] = new_instance._tool_choice
            
            # Preserve metadata from stored metadata
            if hasattr(new_instance, "_crucible_metadata") and new_instance._crucible_metadata:
                generate_kwargs.setdefault("crucible_metadata", {})
                generate_kwargs["crucible_metadata"].update(new_instance._crucible_metadata)
                
            if original_agenerate:
                result = await original_agenerate(messages, stop=stop, run_manager=run_manager, **generate_kwargs)
                
                return result
            else:
                # Fallback: if _agenerate doesn't exist, use sync version in executor
                
                import asyncio
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    lambda: original_generate(messages, stop=stop, run_manager=run_manager, **generate_kwargs)
                )
        
        # Replace methods using object.__setattr__ to bypass Pydantic validation
        object.__setattr__(new_instance, 'invoke', invoke_with_tools)
        object.__setattr__(new_instance, 'ainvoke', ainvoke_with_tools)
        object.__setattr__(new_instance, '_generate', generate_with_tools)
        if original_agenerate:
            object.__setattr__(new_instance, '_agenerate', agenerate_with_tools)
        
        return new_instance

    def with_structured_output(self, schema, **kwargs):
        """
        Return a Runnable that uses structured output.
        
        This method uses OpenAI's function calling API to get structured output,
        ensuring Crucible integration is maintained.
        
        Args:
            schema: The schema to use for structured output (Pydantic model or dict)
            **kwargs: Additional arguments (include_raw, etc.)
            
        Returns:
            A Runnable with structured output support
        """
        # Convert schema to OpenAI tool format
        try:
            from langchain_core.utils.function_calling import convert_to_openai_tool
        except ImportError:
            # Fallback: create tool format manually
            def convert_to_openai_tool(pydantic_model):
                """Convert Pydantic model to OpenAI tool format."""
                schema_dict = pydantic_model.model_json_schema()
                return {
                    "type": "function",
                    "function": {
                        "name": schema_dict.get("title", "extract_data"),
                        "description": schema_dict.get("description", ""),
                        "parameters": schema_dict
                    }
                }
        
        # Convert schema to OpenAI tool format
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            tool = convert_to_openai_tool(schema)
        else:
            tool = schema
        
        # Store reference to self for metadata injection
        original_self = self
        
        def extract_structured_output(response):
            """Extract structured output from the response."""
            # Handle AIMessage with tool calls (LangChain format)
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_call = response.tool_calls[0]
                if isinstance(tool_call, dict):
                    args = tool_call.get('args', {})
                else:
                    # Extract args from ToolCall object
                    args = getattr(tool_call, 'args', {})
                    if not args and hasattr(tool_call, 'get'):
                        args = tool_call.get('args', {})
                    # Try to parse from string if needed
                    if not args and hasattr(tool_call, 'args_str'):
                        import json
                        try:
                            args = json.loads(getattr(tool_call, 'args_str', '{}'))
                        except:
                            pass
                
                if isinstance(schema, type) and issubclass(schema, BaseModel):
                    try:
                        return schema(**args)
                    except Exception as e:
                        # If schema validation fails, try to extract from raw response
                        pass
                return args
            
            # Handle content that might be JSON
            if hasattr(response, 'content') and response.content:
                import json
                try:
                    data = json.loads(response.content)
                    if isinstance(schema, type) and issubclass(schema, BaseModel):
                        return schema(**data)
                    return data
                except:
                    pass
            
            # If no tool calls, return the response as-is
            return response
        
        # Create a wrapper Runnable that processes the output
        def structured_invoke(input_data, config=None, **invoke_kwargs):
            # Inject Crucible metadata if present
            if hasattr(original_self, "_crucible_metadata"):
                invoke_kwargs.setdefault("crucible_metadata", {})
                invoke_kwargs["crucible_metadata"].update(original_self._crucible_metadata)
            
            # Prepare messages for OpenAI API
            if isinstance(input_data, list):
                messages = input_data
            elif hasattr(input_data, 'messages'):
                messages = input_data.messages
            elif hasattr(input_data, 'to_messages'):
                messages = input_data.to_messages()
            else:
                # Convert to message format
                from langchain_core.messages import HumanMessage
                messages = [HumanMessage(content=str(input_data))]
            
            # Extract tool name safely
            if isinstance(tool, dict) and "function" in tool:
                tool_name = tool["function"].get("name", "extract_data")
            else:
                tool_name = "extract_data"
            
            # Call the LLM with tools
            response = original_self.invoke(
                messages,
                config=config,
                tools=[tool],
                tool_choice={"type": "function", "function": {"name": tool_name}},
                **invoke_kwargs
            )
            
            # Extract structured output
            return extract_structured_output(response)
        
        async def structured_ainvoke(input_data, config=None, **invoke_kwargs):
            # Inject Crucible metadata if present
            if hasattr(original_self, "_crucible_metadata"):
                invoke_kwargs.setdefault("crucible_metadata", {})
                invoke_kwargs["crucible_metadata"].update(original_self._crucible_metadata)
            
            # Prepare messages for OpenAI API
            if isinstance(input_data, list):
                messages = input_data
            elif hasattr(input_data, 'messages'):
                messages = input_data.messages
            elif hasattr(input_data, 'to_messages'):
                messages = input_data.to_messages()
            else:
                # Convert to message format
                from langchain_core.messages import HumanMessage
                messages = [HumanMessage(content=str(input_data))]
            
            # Extract tool name safely
            if isinstance(tool, dict) and "function" in tool:
                tool_name = tool["function"].get("name", "extract_data")
            else:
                tool_name = "extract_data"
            
            # Call the LLM with tools
            response = await original_self.ainvoke(
                messages,
                config=config,
                tools=[tool],
                tool_choice={"type": "function", "function": {"name": tool_name}},
                **invoke_kwargs
            )
            
            # Extract structured output
            return extract_structured_output(response)
        
        # Return a Runnable wrapper that inherits from Runnable
        # This ensures compatibility with LangChain's pipe operator (|)
        class StructuredOutputRunnable(Runnable):
            def invoke(self, input_data, config=None, **kwargs):
                return structured_invoke(input_data, config, **kwargs)
            
            async def ainvoke(self, input_data, config=None, **kwargs):
                return await structured_ainvoke(input_data, config, **kwargs)
        
        return StructuredOutputRunnable()

    def invoke(self, input, config=None, **kwargs):
        """
        Invoke the model with input and optional metadata.
        
        Args:
            input: Input to the model
            config: Optional configuration
            **kwargs: Additional arguments
            
        Returns:
            Model response
        """
        # Extract metadata if provided
        crucible_metadata = kwargs.pop("crucible_metadata", {})
        
        # Merge with stored metadata
        if hasattr(self, "_crucible_metadata"):
            crucible_metadata.update(self._crucible_metadata)
        
        # Store metadata for _generate method
        if crucible_metadata:
            self._current_metadata = crucible_metadata
        
        # Remove any Crucible-specific kwargs that shouldn't be passed to OpenAI
        kwargs.pop("_crucible_client", None)
        
        return super().invoke(input, config=config, **kwargs)

    async def ainvoke(self, input, config=None, **kwargs):
        """
        Async invoke the model with input and optional metadata.
        
        Args:
            input: Input to the model
            config: Optional configuration
            **kwargs: Additional arguments
            
        Returns:
            Model response
        """
        # Extract metadata if provided
        crucible_metadata = kwargs.pop("crucible_metadata", {})
        
        # Merge with stored metadata
        if hasattr(self, "_crucible_metadata"):
            crucible_metadata.update(self._crucible_metadata)
        
        # Store metadata for _agenerate method
        if crucible_metadata:
            self._current_metadata = crucible_metadata
                
        # Remove any Crucible-specific kwargs that shouldn't be passed to OpenAI
        kwargs.pop("_crucible_client", None)
        
        result = await super().ainvoke(input, config=config, **kwargs)
        return result

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        """Override _generate to inject Crucible metadata."""
        # Get current metadata from invoke method
        crucible_metadata = getattr(self, "_current_metadata", {})
        
        # Merge with stored metadata if present
        if hasattr(self, "_crucible_metadata"):
            crucible_metadata.update(self._crucible_metadata)
        
        # Ensure client is wrapped (in case parent class overwrote it)
        if hasattr(self, "_crucible_client") and self._crucible_client:
            if not isinstance(self.client, LangChainMetadataCompletionsWrapper):
                crucible_completions = self._crucible_client.chat.completions
                self.client = LangChainMetadataCompletionsWrapper(crucible_completions, self)
        
        # Add metadata to kwargs if present
        if crucible_metadata:
            kwargs["crucible_metadata"] = crucible_metadata
        
        # Clear current metadata after use
        if hasattr(self, "_current_metadata"):
            delattr(self, "_current_metadata")
        
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
    
    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        """Override _agenerate to inject Crucible metadata for async generation."""
        # Get current metadata from ainvoke method
        crucible_metadata = getattr(self, "_current_metadata", {})
        
        # Merge with stored metadata if present
        if hasattr(self, "_crucible_metadata"):
            crucible_metadata.update(self._crucible_metadata)
        
        # Add metadata to kwargs if present
        if crucible_metadata:
            kwargs["crucible_metadata"] = crucible_metadata
        
        # Clear current metadata after use
        if hasattr(self, "_current_metadata"):
            delattr(self, "_current_metadata")
        
        # Call parent's _agenerate if it exists, otherwise fall back to sync version
        if hasattr(super(), "_agenerate"):
            return await super()._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)
        else:
            # Fallback: run sync _generate in executor
            import asyncio
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                lambda: super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
            )

    def close(self) -> None:
        """Close the Crucible client and flush logs."""
        if hasattr(self, "_crucible_client"):
            self._crucible_client.close()

    def flush_logs(self) -> None:
        """Force flush of pending logs."""
        if hasattr(self, "_crucible_client"):
            self._crucible_client.flush_logs()

    def get_logging_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        if hasattr(self, "_crucible_client"):
            return self._crucible_client.get_logging_stats()
        return {}

    def is_healthy(self) -> bool:
        """Check if client is healthy."""
        if hasattr(self, "_crucible_client"):
            return self._crucible_client.is_healthy()
        return True

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
        except:
            pass
