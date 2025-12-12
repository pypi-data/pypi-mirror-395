"""
Error handling for Crucible SDK.
"""

from typing import Optional, Any


class CrucibleError(Exception):
    """Base exception for Crucible errors."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class ConfigurationError(CrucibleError):
    """Configuration validation error."""
    pass


class LoggingError(CrucibleError):
    """Error during logging (non-fatal)."""
    pass


class APIError(CrucibleError):
    """API communication error."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        super().__init__(message, {"status_code": status_code, "response": response})
        self.status_code = status_code
        self.response = response


class NetworkError(CrucibleError):
    """Network communication error."""
    pass


class SerializationError(CrucibleError):
    """Data serialization error."""
    pass


class ValidationError(CrucibleError):
    """Data validation error."""
    pass


class TimeoutError(CrucibleError):
    """Operation timeout error."""
    pass


class CircuitBreakerError(CrucibleError):
    """Circuit breaker is open."""
    pass


def handle_logging_error(error: Exception, context: Optional[str] = None) -> None:
    """
    Safely handle logging errors without breaking the application.
    
    Args:
        error: The exception that occurred
        context: Optional context about where the error occurred
    """
    error_msg = f"Logging error{f' in {context}' if context else ''}: {error}"
    print(f"CRUCIBLE WARNING: {error_msg}")
    
    # In production, you might want to use proper logging
    # logger.warning(error_msg, exc_info=True)


def handle_api_error(error: Exception, operation: str) -> None:
    """
    Handle API errors with proper context.
    
    Args:
        error: The exception that occurred
        operation: The operation that failed
    """
    error_msg = f"API error during {operation}: {error}"
    print(f"CRUCIBLE ERROR: {error_msg}")
    
    # In production, you might want to use proper logging
    # logger.error(error_msg, exc_info=True)
