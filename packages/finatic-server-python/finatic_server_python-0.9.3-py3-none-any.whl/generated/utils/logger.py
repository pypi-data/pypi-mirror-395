"""
Structured logger utility with structlog package (Phase 2B).

Generated - do not edit directly.
"""

import structlog
import logging
import sys
from typing import Optional
from ..config import SdkConfig

_logger: Optional[structlog.BoundLogger] = None


def get_logger(config: Optional[SdkConfig] = None) -> structlog.BoundLogger:
    """Get or create a structured logger instance.
    
    Args:
        config: SDK configuration (optional)
    
    Returns:
        Structured logger instance
    """
    global _logger
    
    if _logger is not None:
        return _logger
    
    import os
    log_level = (config.log_level if config else None) or os.getenv('FINATIC_LOG_LEVEL', 'error')
    
    # Determine if we should use structured (JSON) or pretty (console) logging
    # Use pretty console renderer in development unless explicitly requested
    is_production = os.getenv('NODE_ENV', '').lower() in ('production', 'prod')
    use_structured = (
        (config.structured_logging if config else None) is True or
        (is_production and (config.structured_logging if config else None) is not False)
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if use_structured else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Set standard library logging level
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.ERROR),
    )
    
    _logger = structlog.get_logger('finatic_sdk')
    
    return _logger
