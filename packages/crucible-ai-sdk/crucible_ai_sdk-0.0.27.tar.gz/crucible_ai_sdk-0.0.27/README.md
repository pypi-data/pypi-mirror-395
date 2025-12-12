# Crucible SDK

A high-performance Python SDK for logging and monitoring OpenAI API calls to Crucible warehouse.

## Features

- **Seamless Integration**: Drop-in replacement for OpenAI's Python client
- **Background Logging**: Non-blocking, batched logging with configurable intervals
- **Streaming Support**: Efficient handling of streaming responses with memory optimization
- **Error Resilience**: Logging failures never break your application
- **Performance Optimized**: <1ms overhead per request, <50MB memory usage
- **Async Support**: Full async/await support for high-concurrency applications
- **Rich Tagging**: Flexible metadata system for organizing and filtering logs
- **Circuit Breaker**: Automatic failure detection and recovery
- **Compression**: Optional request/response compression for network efficiency
- **LangChain Integration**: Seamless integration with LangChain workflows
- **Google GenAI Integration**: Seamless integration with Google's Generative AI (Gemini)

## Installation

```bash
pip install crucible-ai-sdk
```

## Quick Start

### Basic Usage

```python
from crucible import CrucibleOpenAI

# Initialize client (uses warehouse.usecrucible.ai by default)
client = CrucibleOpenAI(api_key="your-crucible-api-key")

# Make API calls (automatically logged)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, world!"}],
    crucible_metadata={
        "thread_id": "thread_123",
        "task_id": "task_456",
        "user_id": "user_789"
    }
)

print(response.choices[0].message.content)

# Clean up
client.close()
```

### Async Usage

```python
import asyncio
from crucible import CrucibleAsyncOpenAI

async def main():
    client = CrucibleAsyncOpenAI(api_key="your-crucible-api-key")
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, async world!"}],
        crucible_metadata={
            "thread_id": "async_thread_123",
            "task_id": "async_task_456"
        }
    )
    
    print(response.choices[0].message.content)
    await client.close()

asyncio.run(main())
```

### Streaming Support

```python
from crucible import CrucibleOpenAI

client = CrucibleOpenAI(api_key="your-crucible-api-key")

# Streaming responses are automatically logged
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count from 1 to 5"}],
    stream=True,
    crucible_metadata={
        "session_id": "session_abc",
        "experiment": "streaming_test"
    }
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Custom Domain

```python
from crucible import CrucibleOpenAI

# Use custom domain
client = CrucibleOpenAI(
    api_key="your-crucible-api-key",
    domain="custom.warehouse.com"
)

# Make API call with metadata
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello from custom domain!"}],
    crucible_metadata={
        "domain": "custom",
        "environment": "production"
    }
)
```

### Context Manager

```python
from crucible import CrucibleOpenAI

# Automatic cleanup with context manager
with CrucibleOpenAI(api_key="your-crucible-api-key") as client:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        crucible_metadata={
            "context_test": True,
            "session_id": "context_session"
        }
    )
    
    print(response.choices[0].message.content)
    # Logs are automatically flushed when exiting context
```

## Configuration

### Environment Variables

```bash
export CRUCIBLE_API_KEY="your-api-key"
export CRUCIBLE_DOMAIN="warehouse.usecrucible.ai"  # Optional, defaults to warehouse.usecrucible.ai
export OPENAI_API_KEY="your-openai-api-key"
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | str | None | Crucible API key |
| `domain` | str | "warehouse.usecrucible.ai" | Crucible warehouse domain |
| `batch_size` | int | 10 | Number of requests to batch together |
| `flush_interval` | float | 5.0 | Seconds between batch flushes |
| `max_retries` | int | 3 | Number of retry attempts |
| `timeout` | float | 30.0 | Request timeout in seconds |
| `enable_logging` | bool | True | Enable/disable logging |
| `enable_compression` | bool | True | Enable request compression |
| `max_memory_mb` | int | 50 | Maximum memory usage in MB |
| `max_queue_size` | int | 1000 | Maximum queue size for background logging |

## Metadata System

Use metadata to organize and filter your logged requests:

```python
client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    crucible_metadata={
        "thread_id": "thread_123",
        "task_id": "task_456",
        "user_id": "user_789",
        "session_id": "session_abc",
        "question_type": "geography",
        "difficulty": "easy",
        "experiment": "knowledge_test"
    }
)
```

## Error Handling

Crucible SDK is designed to be resilient. Logging failures never break your application:

```python
from crucible import CrucibleOpenAI

client = CrucibleOpenAI(api_key="your-crucible-api-key")

try:
    # This will fail, but error will be logged
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-invalid",
        messages=[{"role": "user", "content": "This will fail"}],
        crucible_metadata={
            "error_test": True,
            "task_id": "error_test_123"
        }
    )
except Exception as e:
    print(f"API call failed: {e}")
    # Error was automatically logged to Crucible warehouse
```

## Performance Monitoring

Monitor the performance of your logging system:

```python
from crucible import CrucibleOpenAI

client = CrucibleOpenAI(api_key="your-crucible-api-key")

# Make some API calls...
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    crucible_metadata={"test": "performance"}
)

# Clean up
client.close()
```

## LangChain Integration

Crucible provides seamless integration with LangChain for automatic logging of LLM interactions:

```python
from crucible.langchain_llm import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain.schema.output_parser import StrOutputParser

# Initialize Crucible ChatOpenAI
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    crucible_kwargs={
        "api_key": "your-crucible-api-key",
        "domain": "warehouse.usecrucible.ai"
    }
)

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Explain {topic} in simple terms.")
])

# Create a chain
chain = prompt | llm | StrOutputParser()

# Run with metadata
result = chain.invoke(
    {"topic": "machine learning"},
    crucible_metadata={
        "langchain_example": True,
        "topic": "machine_learning",
        "user_id": "user_123"
    }
)

print(result)

# Clean up
llm.close()
```

### LangChain Features

- **Metadata Support**: Pass `crucible_metadata` to any LangChain operation
- **Stored Metadata**: Use `with_metadata()` to store metadata for all operations
- **Streaming Support**: Full support for LangChain streaming
- **Async Support**: Compatible with LangChain's async operations
- **Context Management**: Automatic cleanup with `close()` method

```python
# Store metadata for all operations
llm = ChatOpenAI(...).with_metadata(
    session_id="session_123",
    experiment="langchain_test"
)

# Streaming with metadata
for chunk in chain.stream(
    {"topic": "AI"},
    crucible_metadata={"streaming": True}
):
    print(chunk.content, end="")
```

## Google GenAI Integration

Crucible provides seamless integration with Google's Generative AI (Gemini) for automatic logging of LLM interactions:

### Installation

```bash
pip install crucible-ai-sdk[genai]
```

### Basic Usage

```python
from crucible import CrucibleGenAI

# Initialize client
client = CrucibleGenAI(
    api_key="your-crucible-api-key",
    genai_api_key="your-google-api-key"  # or set GOOGLE_API_KEY env var
)

# Generate content with automatic logging
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing in simple terms.",
    crucible_metadata={
        "thread_id": "thread_123",
        "task_id": "task_456",
        "user_id": "user_789"
    }
)

print(response.text)

# Clean up
client.close()
```

### Async Usage

```python
import asyncio
from crucible import CrucibleAsyncGenAI

async def main():
    client = CrucibleAsyncGenAI(
        api_key="your-crucible-api-key",
        genai_api_key="your-google-api-key"
    )
    
    response = await client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello, async world!",
        crucible_metadata={
            "thread_id": "async_thread_123",
            "task_id": "async_task_456"
        }
    )
    
    print(response.text)
    await client.close()

asyncio.run(main())
```

### Streaming Support

```python
from crucible import CrucibleGenAI

client = CrucibleGenAI(
    api_key="your-crucible-api-key",
    genai_api_key="your-google-api-key"
)

# Streaming responses are automatically logged
stream = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Count from 1 to 5",
    stream=True,
    crucible_metadata={
        "session_id": "session_abc",
        "experiment": "streaming_test"
    }
)

for chunk in stream:
    if chunk.text:
        print(chunk.text, end="", flush=True)
```

### Custom Generation Config

```python
from crucible import CrucibleGenAI

client = CrucibleGenAI(
    api_key="your-crucible-api-key",
    genai_api_key="your-google-api-key"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write a short story.",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 500,
    },
    crucible_metadata={
        "task_type": "creative_writing",
        "temperature": 0.7,
        "max_tokens": 500
    }
)

print(response.text)
client.close()
```

### Context Manager

```python
from crucible import CrucibleGenAI

# Automatic cleanup with context manager
with CrucibleGenAI(
    api_key="your-crucible-api-key",
    genai_api_key="your-google-api-key"
) as client:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello!",
        crucible_metadata={
            "context_test": True,
            "session_id": "context_session"
        }
    )
    
    print(response.text)
    # Logs are automatically flushed when exiting context
```

### Alternative Syntax: GenerativeModel

You can also use the `GenerativeModel` syntax if you prefer:

```python
from crucible import CrucibleGenAI

client = CrucibleGenAI(
    api_key="your-crucible-api-key",
    genai_api_key="your-google-api-key"
)

# Create a model instance
model = client.GenerativeModel("gemini-2.5-flash")

# Generate content with automatic logging
response = model.generate_content(
    "Explain quantum computing in simple terms.",
    crucible_metadata={
        "thread_id": "thread_123",
        "task_id": "task_456"
    }
)

print(response.text)
client.close()
```

Both syntaxes (`client.models.generate_content()` and `client.GenerativeModel().generate_content()`) are fully supported and provide identical functionality.

### GenAI Features

- **Metadata Support**: Pass `crucible_metadata` to any GenAI operation
- **Streaming Support**: Full support for GenAI streaming
- **Async Support**: Compatible with GenAI's async operations
- **Context Management**: Automatic cleanup with `close()` method
- **Error Handling**: Automatic error logging without breaking your application
- **Generation Config**: Support for all GenAI generation configuration options

### Environment Variables

```bash
export CRUCIBLE_API_KEY="your-crucible-api-key"
export GOOGLE_API_KEY="your-google-api-key"  # or GOOGLE_GENAI_API_KEY
export CRUCIBLE_DOMAIN="warehouse.usecrucible.ai"  # Optional
```

## Advanced Usage

### Manual Logging

```python
from crucible import CrucibleLogger, LogRequest, CrucibleConfig
import time

config = CrucibleConfig(api_key="your-api-key", domain="warehouse.usecrucible.ai")
logger = CrucibleLogger(config)

# Create log request manually
log_request = LogRequest(
    requested_at=int(time.time() * 1000),
    received_at=int(time.time() * 1000),
    req_payload={"model": "gpt-3.5-turbo", "messages": [...]},
    resp_payload={"choices": [...]},
    status_code=200,
    metadata={"manual": "true", "task_id": "manual_123"}
)

# Log manually
logger.log_request(log_request)

# Clean up
logger.close()
```

### Streaming Statistics

```python
from crucible import StreamingMerger

merger = StreamingMerger(max_memory_mb=100)

# Process chunks...
for chunk in stream:
    assembled = merger.merge_chunk(assembled, chunk)

# Get streaming statistics
stats = merger.get_stats()
print(f"Memory usage: {stats['current_size']} bytes")
print(f"Chunks processed: {stats['total_chunks_processed']}")
```

## Development

### Running Tests

```bash
pip install pytest
pytest tests/
```

### Running Examples

```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export CRUCIBLE_API_KEY="your-crucible-key"

# Run examples
python examples/basic_usage.py
python examples/async_usage.py
```

### Deployment to PyPI

The SDK includes a simple deployment script for publishing to PyPI.

#### Prerequisites

1. **PyPI Account**: Ensure you have a PyPI account with upload permissions
2. **API Token**: Create a PyPI API token at https://pypi.org/manage/account/token/
3. **Version Update**: Update the version in `pyproject.toml` and `crucible/__init__.py` before deploying

#### Deployment Steps

1. **Set PyPI Credentials**:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-your-api-token-here
   ```

2. **Run Deployment Script**:
   ```bash
   cd crucible-python-sdk
   ./deploy.sh
   ```

   The script will:
   - Clean previous builds
   - Build the package (source distribution and wheel)
   - Validate the package
   - Upload to PyPI

3. **Verify Deployment**:
   ```bash
   pip install crucible-ai-sdk==<version>
   ```

#### Version Bumping

Before deploying, update the version in two places:

1. **`pyproject.toml`**:
   ```toml
   version = "0.0.14"
   ```

2. **`crucible/__init__.py`**:
   ```python
   __version__ = "0.0.14"
   ```

Follow semantic versioning:
- **Patch** (0.0.13 → 0.0.14): Bug fixes and new features (bind_tools support)
- **Minor** (0.0.9 → 0.1.0): New features, backward compatible
- **Major** (0.0.9 → 1.0.0): Breaking changes

#### Manual Deployment

If you prefer to deploy manually:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build package
python3 -m build

# Check package
python3 -m twine check dist/*

# Upload to PyPI
python3 -m twine upload dist/*
```

#### Troubleshooting

- **Authentication Errors**: Ensure `TWINE_USERNAME` and `TWINE_PASSWORD` are set correctly
- **Version Already Exists**: PyPI doesn't allow overwriting versions. Bump the version number
- **Build Errors**: Ensure all dependencies are installed: `pip install build twine`

## API Reference

### CrucibleOpenAI

Main client class for synchronous operations.

#### Methods

- `chat.completions.create(**kwargs)`: Create chat completion with logging
- `close()`: Close client and flush logs
- `flush_logs()`: Force flush pending logs
- `get_logging_stats()`: Get logging statistics
- `is_healthy()`: Check if logger is healthy

### CrucibleAsyncOpenAI

Async client class for asynchronous operations.

#### Methods

- `chat.completions.create(**kwargs)`: Create async chat completion with logging
- `close()`: Close client and flush logs
- `flush_logs()`: Force flush pending logs
- `get_logging_stats()`: Get logging statistics
- `is_healthy()`: Check if logger is healthy

### CrucibleConfig

Configuration class for Crucible SDK.

#### Properties

- `api_key`: Crucible API key
- `domain`: Crucible warehouse domain (defaults to warehouse.usecrucible.ai)
- `batch_size`: Batch size for logging
- `flush_interval`: Flush interval in seconds
- `enable_logging`: Enable/disable logging
- `enable_compression`: Enable/disable compression

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- Documentation: [https://docs.crucible.ai](https://docs.crucible.ai)
- Issues: [https://github.com/crucible/crucible-python-sdk/issues](https://github.com/crucible/crucible-python-sdk/issues)
- Email: support@crucible.ai
