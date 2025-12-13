"""
Request/Response interceptor utilities (Phase 2B).

Generated - do not edit directly.
"""

from typing import Callable, List, Optional, Any, Dict
from ..config import SdkConfig

RequestInterceptor = Callable[[Dict[str, Any]], Dict[str, Any]]
ResponseInterceptor = Callable[[Any], Any]
ErrorInterceptor = Callable[[Exception], Exception]

_interceptors: Dict[str, List[Callable]] = {
    'request': [],
    'response': [],
    'error': [],
}


def add_request_interceptor(interceptor: RequestInterceptor) -> None:
    """Add request interceptor."""
    _interceptors['request'].append(interceptor)


def add_response_interceptor(interceptor: ResponseInterceptor) -> None:
    """Add response interceptor."""
    _interceptors['response'].append(interceptor)


def add_error_interceptor(interceptor: ErrorInterceptor) -> None:
    """Add error interceptor."""
    _interceptors['error'].append(interceptor)


async def apply_request_interceptors(
    config: Dict[str, Any],
    sdk_config: Optional[SdkConfig] = None
) -> Dict[str, Any]:
    """Apply request interceptors.
    
    Args:
        config: Request configuration
        sdk_config: SDK configuration (optional)
    
    Returns:
        Modified configuration
    """
    if sdk_config and not sdk_config.request_interceptors_enabled:
        return config
    
    result = config
    for interceptor in _interceptors['request']:
        result = await interceptor(result) if hasattr(interceptor, '__call__') else interceptor(result)
    
    return result


async def apply_response_interceptors(
    response: Any,
    sdk_config: Optional[SdkConfig] = None
) -> Any:
    """Apply response interceptors.
    
    Args:
        response: API response
        sdk_config: SDK configuration (optional)
    
    Returns:
        Modified response
    """
    if sdk_config and not sdk_config.response_interceptors_enabled:
        return response
    
    result = response
    for interceptor in _interceptors['response']:
        result = await interceptor(result) if hasattr(interceptor, '__call__') else interceptor(result)
    
    return result


async def apply_error_interceptors(
    error: Exception,
    sdk_config: Optional[SdkConfig] = None
) -> Exception:
    """Apply error interceptors.
    
    Args:
        error: Exception to process
        sdk_config: SDK configuration (optional)
    
    Returns:
        Processed exception
    """
    if sdk_config and not sdk_config.response_interceptors_enabled:
        raise error
    
    result = error
    for interceptor in _interceptors['error']:
        result = await interceptor(result) if hasattr(interceptor, '__call__') else interceptor(result)
    
    return result
