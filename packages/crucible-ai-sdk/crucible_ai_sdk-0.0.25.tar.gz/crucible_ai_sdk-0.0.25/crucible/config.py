"""
Configuration management for Crucible SDK.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json


@dataclass
class CrucibleConfig:
    """
    Configuration for Crucible SDK.
    
    Provides hierarchical configuration with environment variables as defaults
    and explicit parameters taking precedence.
    """
    
    # API Configuration
    api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("CRUCIBLE_API_KEY")
    )
    domain: Optional[str] = field(
        default_factory=lambda: os.getenv("CRUCIBLE_DOMAIN", "warehouse.usecrucible.ai")
    )
    
    # Performance Configuration
    batch_size: int = 10
    flush_interval: float = 5.0
    max_retries: int = 3
    timeout: float = 30.0
    
    # Feature Flags
    enable_logging: bool = True
    enable_compression: bool = True
    enable_caching: bool = False
    immediate_flush: bool = False  # If True, flush immediately after each request
    
    # Memory Management
    max_memory_mb: int = 50
    max_queue_size: int = 1000
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "json"
    
    # SDK Information
    sdk_version: str = "0.1.0"
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Handle None values - use defaults from environment or hardcoded defaults
        if self.domain is None:
            self.domain = os.getenv("CRUCIBLE_DOMAIN", "warehouse.usecrucible.ai")
        
        if self.api_key is None:
            self.api_key = os.getenv("CRUCIBLE_API_KEY")
        
        self.validate()
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.enable_logging and not self.api_key:
            raise ValueError("API key required when logging is enabled")
        
        if self.domain and not self._validate_domain(self.domain):
            raise ValueError(f"Invalid domain format: {self.domain}")
        
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        
        if self.flush_interval <= 0:
            raise ValueError("flush_interval must be positive")
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.max_memory_mb <= 0:
            raise ValueError("max_memory_mb must be positive")
        
        if self.max_queue_size <= 0:
            raise ValueError("max_queue_size must be positive")
    
    def _validate_domain(self, domain: str) -> bool:
        """Validate domain format."""
        import re
        # Allow localhost with or without port
        if domain.startswith("localhost"):
            return True
        # Standard domain pattern
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(pattern, domain))
    
    @property
    def base_url(self) -> str:
        """Get the base URL for the API."""
        # Ensure domain is set
        if self.domain is None:
            self.domain = os.getenv("CRUCIBLE_DOMAIN", "warehouse.usecrucible.ai")
        
        protocol = "http" if self.domain.startswith("localhost") else "https"
        if self.domain.startswith("localhost"):
            # For localhost, use port 5001 if no port specified
            if ":" not in self.domain:
                return f"{protocol}://{self.domain}:5001/llm-logs"
            else:
                return f"{protocol}://{self.domain}/llm-logs"
        else:
            return f"{protocol}://{self.domain}/llm-logs"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "api_key": self.api_key,
            "domain": self.domain,
            "base_url": self.base_url,
            "batch_size": self.batch_size,
            "flush_interval": self.flush_interval,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "enable_logging": self.enable_logging,
            "enable_compression": self.enable_compression,
            "enable_caching": self.enable_caching,
            "max_memory_mb": self.max_memory_mb,
            "max_queue_size": self.max_queue_size,
            "log_level": self.log_level,
            "log_format": self.log_format,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CrucibleConfig":
        """Create configuration from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_file(cls, filepath: str) -> "CrucibleConfig":
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def save_to_file(self, filepath: str) -> None:
        """Save configuration to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def update(self, **kwargs) -> "CrucibleConfig":
        """Create new configuration with updated values."""
        current_data = self.to_dict()
        current_data.update(kwargs)
        return self.from_dict(current_data)
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"CrucibleConfig(api_key={'***' if self.api_key else None}, domain={self.domain})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"CrucibleConfig({', '.join(f'{k}={v}' for k, v in self.to_dict().items())})"
