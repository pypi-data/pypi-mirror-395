"""
Global configuration management for Contexere SDK
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Global configuration for Contexere SDK"""
    api_key: Optional[str] = None
    project_name: Optional[str] = None
    endpoint: str = "https://contexere-be-prod.up.railway.app"  # Production Railway backend
    enabled: bool = True
    timeout: float = 0.5  # HTTP timeout in seconds (fail fast, never block user code)


# Global configuration instance
_config = Config()


def init(
    api_key: str,
    project_name: str = "default",
    endpoint: Optional[str] = None,
    enabled: bool = True
) -> None:
    """
    Initialize Contexere SDK

    Args:
        api_key: Your Contexere API key (e.g., "ck_...")
        project_name: Logical project name for grouping traces (default: "default")
        endpoint: Backend endpoint URL (optional, defaults to production)
        enabled: Enable/disable tracing (default: True)

    Example:
        >>> import contexere as conte
        >>> conte.init(api_key="ck_12345", project_name="my-agent")
    """
    global _config

    _config.api_key = api_key
    _config.project_name = project_name
    _config.enabled = enabled

    # Allow overriding endpoint for custom deployments
    if endpoint:
        _config.endpoint = endpoint


def get_config() -> Config:
    """Get the current global configuration"""
    return _config


def is_enabled() -> bool:
    """Check if tracing is enabled and properly configured"""
    return _config.enabled and _config.api_key is not None
