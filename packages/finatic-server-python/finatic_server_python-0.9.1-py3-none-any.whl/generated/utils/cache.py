"""
Response caching utility with cachetools (Phase 2B).

Generated - do not edit directly.
"""

from cachetools import TTLCache
from typing import Optional, Any, Dict
from ..config import SdkConfig

_cache_instance: Optional[TTLCache] = None


def get_cache(config: Optional[SdkConfig] = None) -> Optional[TTLCache]:
    """Get or create cache instance.
    
    Args:
        config: SDK configuration (optional)
    
    Returns:
        Cache instance or None if caching disabled
    """
    global _cache_instance
    
    if config and not config.cache_enabled:
        return None
    
    if _cache_instance is not None:
        return _cache_instance
    
    ttl = (config.cache_ttl if config else 300)
    max_size = (config.cache_max_size if config else 1000)
    
    _cache_instance = TTLCache(maxsize=max_size, ttl=ttl)
    
    return _cache_instance


def generate_cache_key(
    method: str,
    path: str,
    params: Dict[str, Any],
    config: Optional[SdkConfig] = None
) -> str:
    """Generate cache key from method and parameters.
    
    Args:
        method: HTTP method
        path: API path
        params: Request parameters
        config: SDK configuration (optional)
    
    Returns:
        Cache key string
    """
    include = (config.cache_key_include if config else ['method', 'path', 'query', 'body'])
    parts = []
    
    if 'method' in include:
        parts.append(f'method:{method}')
    if 'path' in include:
        parts.append(f'path:{path}')
    if 'query' in include:
        query = params.get('query', params)
        query_str = '&'.join(f'{k}={repr(query[k])}' for k in sorted(query.keys()))
        parts.append(f'query:{query_str}')
    if 'body' in include:
        import json
        body = params.get('body', {})
        parts.append(f'body:{json.dumps(body, sort_keys=True)}')
    
    return f'finatic:{"|".join(parts)}'
