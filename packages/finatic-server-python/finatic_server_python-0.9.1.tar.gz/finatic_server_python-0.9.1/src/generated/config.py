"""
Finatic Server SDK Configuration

═══════════════════════════════════════════════════════════════════════════
CENTRALIZED CONFIGURATION - Adjust all SDK settings here
═══════════════════════════════════════════════════════════════════════════

This file contains all configurable options for the SDK.
Modify values here to customize SDK behavior.

Generated - do not edit directly.
For custom configuration, extend this class in src/custom/config.py
"""

import os
from typing import Optional, Dict, List, Callable, Any
from dataclasses import dataclass, field


@dataclass
class SdkConfig:
    """SDK configuration with all customizable options."""
    
    # ═══════════════════════════════════════════════════════════════════════
    # API Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    base_url: str = field(default_factory=lambda: os.getenv('FINATIC_API_URL', 'https://api.finatic.com'))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv('FINATIC_API_KEY'))
    timeout: int = field(default_factory=lambda: int(os.getenv('FINATIC_TIMEOUT', '30')))
    headers: Dict[str, str] = field(default_factory=dict)
    
    # ═══════════════════════════════════════════════════════════════════════
    # Retry Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    retry_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_RETRY_ENABLED', 'true').lower() != 'false')
    retry_count: int = field(default_factory=lambda: int(os.getenv('FINATIC_RETRY_COUNT', '3')))
    retry_delay: float = field(default_factory=lambda: float(os.getenv('FINATIC_RETRY_DELAY', '1.0')))
    retry_max_delay: float = field(default_factory=lambda: float(os.getenv('FINATIC_RETRY_MAX_DELAY', '10.0')))
    retry_multiplier: float = field(default_factory=lambda: float(os.getenv('FINATIC_RETRY_MULTIPLIER', '2.0')))
    retry_on_status: List[int] = field(default_factory=lambda: [429, 500, 502, 503, 504])
    retry_on_network_error: bool = field(default_factory=lambda: os.getenv('FINATIC_RETRY_ON_NETWORK_ERROR', 'true').lower() != 'false')
    
    # ═══════════════════════════════════════════════════════════════════════
    # Logging Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    log_level: str = field(default_factory=lambda: os.getenv('FINATIC_LOG_LEVEL', 'error'))
    structured_logging: bool = field(default_factory=lambda: os.getenv('FINATIC_STRUCTURED_LOGGING', 'false').lower() == 'true')
    log_request_body: bool = field(default_factory=lambda: os.getenv('FINATIC_LOG_REQUEST_BODY', 'false').lower() == 'true')
    log_response_body: bool = field(default_factory=lambda: os.getenv('FINATIC_LOG_RESPONSE_BODY', 'false').lower() == 'true')
    log_request_id: bool = field(default_factory=lambda: os.getenv('FINATIC_LOG_REQUEST_ID', 'true').lower() != 'false')
    
    # ═══════════════════════════════════════════════════════════════════════
    # Validation Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    validation_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_VALIDATION_ENABLED', 'true').lower() != 'false')
    validation_strict: bool = field(default_factory=lambda: os.getenv('FINATIC_VALIDATION_STRICT', 'false').lower() == 'true')
    
    # ═══════════════════════════════════════════════════════════════════════
    # Caching Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    cache_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_CACHE_ENABLED', 'false').lower() == 'true')
    cache_ttl: int = field(default_factory=lambda: int(os.getenv('FINATIC_CACHE_TTL', '300')))
    cache_max_size: int = field(default_factory=lambda: int(os.getenv('FINATIC_CACHE_MAX_SIZE', '1000')))
    cache_key_include: List[str] = field(default_factory=lambda: ['method', 'path', 'query', 'body'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # Rate Limiting Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    rate_limit_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_RATE_LIMIT_ENABLED', 'true').lower() != 'false')
    rate_limit_auto_retry: bool = field(default_factory=lambda: os.getenv('FINATIC_RATE_LIMIT_AUTO_RETRY', 'true').lower() != 'false')
    rate_limit_handler: Optional[Callable[[float], Any]] = None
    
    # ═══════════════════════════════════════════════════════════════════════
    # Interceptor Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    request_interceptors_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_REQUEST_INTERCEPTORS', 'true').lower() != 'false')
    response_interceptors_enabled: bool = field(default_factory=lambda: os.getenv('FINATIC_RESPONSE_INTERCEPTORS', 'true').lower() != 'false')
    
    # ═══════════════════════════════════════════════════════════════════════
    # Session Management Configuration
    # ═══════════════════════════════════════════════════════════════════════
    
    session_context_storage: str = field(default_factory=lambda: os.getenv('FINATIC_SESSION_STORAGE', 'memory'))
    session_context_getter: Optional[Callable[[], Dict[str, Optional[str]]]] = None
    session_context_setter: Optional[Callable[[Dict[str, Optional[str]]], None]] = None


def get_config(overrides: Optional[Dict[str, Any]] = None) -> SdkConfig:
    """Get configuration with optional overrides.
    
    Args:
        overrides: Dictionary of configuration overrides
    
    Returns:
        SdkConfig instance
    """
    config = SdkConfig()
    
    if overrides:
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)
    
    return config
