"""
Generated utility functions (Phase 2B).

This file is regenerated on each run - do not edit directly.
"""

from .request_id import generate_request_id
from .retry import retry_api_call
from .logger import get_logger
from .error_handling import handle_error, FinaticError, ApiError, ValidationError
from .validation import validate_params
from .cache import get_cache, generate_cache_key
from .interceptors import (
    add_request_interceptor,
    add_response_interceptor,
    add_error_interceptor,
    apply_request_interceptors,
    apply_response_interceptors,
    apply_error_interceptors,
)
from .url_utils import append_theme_to_url, append_broker_filter_to_url
from .enum_coercion import coerce_enum_value
from .pagination import PaginatedData, PaginationMeta

__all__ = [
    'generate_request_id',
    'retry_api_call',
    'get_logger',
    'handle_error',
    'FinaticError',
    'ApiError',
    'ValidationError',
    'validate_params',
    'get_cache',
    'generate_cache_key',
    'add_request_interceptor',
    'add_response_interceptor',
    'add_error_interceptor',
    'apply_request_interceptors',
    'apply_response_interceptors',
    'apply_error_interceptors',
    'append_theme_to_url',
    'append_broker_filter_to_url',
    'coerce_enum_value',
    'PaginatedData',
    'PaginationMeta',
    'unwrap_response',
]
