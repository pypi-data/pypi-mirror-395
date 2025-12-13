"""
Error handling utility (Phase 2A/2B).

Generated - do not edit directly.
"""

from typing import Optional, Any, TypedDict, List, Dict


class ParsedFinaticError(TypedDict, total=False):
    type: Optional[str]
    code: Optional[str]
    message: str
    trace_id: Optional[str]
    details: Any
    fields: Optional[List[Dict[str, Optional[str]]]]


class FinaticError(Exception):
    """Base error class for Finatic SDK."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None,
        finatic: Optional[ParsedFinaticError] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        self.original_error = original_error
        self.finatic = finatic


class ApiError(FinaticError):
    """Error for API call failures."""
    
    def __init__(
        self,
        message: str,
        status_code: int,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None,
        finatic: Optional[ParsedFinaticError] = None,
    ):
        super().__init__(message, status_code, request_id, original_error, finatic)


class ValidationError(FinaticError):
    """Error for validation failures."""
    
    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None,
        finatic: Optional[ParsedFinaticError] = None,
    ):
        super().__init__(message, 422, request_id, original_error, finatic)


def _extract_finatic_error(error: Exception | Any) -> Optional[ParsedFinaticError]:
    data = getattr(error, 'response', None)
    if data and hasattr(data, 'json'):
        try:
            data = data.json()
        except Exception:
            pass
    elif hasattr(error, 'data'):
        data = getattr(error, 'data')

    if not data:
        return None

    err = data.get('error', data) if isinstance(data, dict) else None
    meta = data.get('meta', {}) if isinstance(data, dict) else {}
    message = (err or {}).get('message') if isinstance(err, dict) else None
    if not message:
        message = data.get('message') if isinstance(data, dict) else str(error)
    trace_id = None
    if isinstance(err, dict):
        trace_id = err.get('trace_id')
    if not trace_id and isinstance(meta, dict):
        trace_id = meta.get('trace_id')

    fields = None
    if isinstance(err, dict) and isinstance(err.get('fields'), list):
        fields = []
        for f in err['fields']:
            fields.append({
                'path': str(f.get('path', '')) if isinstance(f, dict) else '',
                'message': str(f.get('message', '')) if isinstance(f, dict) else '',
                'code': f.get('code') if isinstance(f, dict) else None,
            })

    return {
        'type': (err or {}).get('type') if isinstance(err, dict) else None,
        'code': (err or {}).get('code') if isinstance(err, dict) else None,
        'message': message or 'Unknown error',
        'trace_id': trace_id,
        'details': (err or {}).get('details') if isinstance(err, dict) else None,
        'fields': fields,
    }


def handle_error(error: Exception, request_id: Optional[str] = None) -> Exception:
    """Handle and transform errors from API calls.
    
    Args:
        error: Original exception
        request_id: Request ID for tracking
    
    Returns:
        Transformed error (FinaticError or subclass)
    """
    status_code = getattr(error, 'status_code', None) or getattr(error, 'status', None)
    finatic = _extract_finatic_error(error)
    message = (finatic or {}).get('message') or str(error) or 'Unknown error'
    trace_id = (finatic or {}).get('trace_id') or request_id

    if status_code == 422:
        return ValidationError(message, trace_id, error, finatic)
    elif status_code and status_code >= 400:
        return ApiError(message, status_code, trace_id, error, finatic)
    
    return FinaticError(message, status_code, trace_id, error, finatic)
