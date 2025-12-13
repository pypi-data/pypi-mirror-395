"""
Generated wrapper functions for session operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/session.py instead.
"""

from __future__ import annotations

from typing import Optional, Any, Dict, List
from dataclasses import dataclass
from ..api.session_api import SessionApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..types import FinaticResponse
from ..models.portal_url_response import PortalUrlResponse
from ..models.session_response_data import SessionResponseData
from ..models.session_start_request import SessionStartRequest
from ..models.session_user_response import SessionUserResponse
from ..models.token_response_data import TokenResponseData
from ..utils.request_id import generate_request_id
from ..utils.retry import retry_api_call
from ..utils.logger import get_logger
from ..utils.error_handling import handle_error
from ..utils.cache import get_cache, generate_cache_key
from ..utils.interceptors import (
    apply_request_interceptors,
    apply_response_interceptors,
    apply_error_interceptors,
)
from ..utils.enum_coercion import coerce_enum_value
from ..utils.plain_object import convert_to_plain_object


# Phase 2C: Input type definitions (output types use FinaticResponse[DataType] pattern - no models needed)
@dataclass
class InitSessionParams:
    """Input parameters for init_session_api_v1_session_init_post."""
  # Company API key
    x_api_key: str

@dataclass
class StartSessionParams:
    """Input parameters for start_session_api_v1_session_start_post."""
  # One-time use token obtained from init_session endpoint to authenticate and start the session
    one_time_token: str
  # Session start request containing optional user ID to associate with the session
    session_start_request: SessionStartRequest

@dataclass
class GetPortalUrlParams:
    """Input parameters for get_portal_url_api_v1_session_portal_get."""
    pass

@dataclass
class GetSessionUserParams:
    """Input parameters for get_session_user_api_v1_session__session_id__user_get."""
  # Session ID
    session_id: str


class SessionWrapper:
    """Session wrapper functions.
    
    Provides simplified method names and response unwrapping.
    """
    
    def __init__(self, api: SessionApi, config: Optional[Configuration] = None, sdk_config: Optional[SdkConfig] = None):
        self.api = api
        self.config = config
        self.sdk_config = sdk_config
        self.logger = get_logger(sdk_config)
        self.session_id: Optional[str] = None
        self.company_id: Optional[str] = None
        self.csrf_token: Optional[str] = None
    
    # Session context setters (called by session management)
    def set_session_context(self, session_id: str, company_id: str, csrf_token: str) -> None:
        """Set session context for API calls."""
        self.session_id = session_id
        self.company_id = company_id
        self.csrf_token = csrf_token
    
    # Utility methods (Phase 2B)
    def _generate_request_id(self) -> str:
        """Generate a unique request ID."""
        return generate_request_id()
    
    async def _retry_api_call(self, fn):
        """Retry an API call with exponential backoff."""
        return await retry_api_call(fn)
    
    def _handle_error(self, error: Exception, request_id: Optional[str] = None) -> Exception:
        """Handle and transform errors from API calls."""
        return handle_error(error, request_id)

    async def init_session(self, **kwargs) -> FinaticResponse[TokenResponseData]:
        """Init Session
        
        Initialize a new session with company API key.

        Args:
            x_api_key (str): Company API key
        Returns:
        - Dict[str, Any]: FinaticResponse[TokenResponseData] format
                     success: {data: TokenResponseData, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: POST /api/v1/session/init
        @methodId init_session_api_v1_session_init_post
        @category session
        @example
        ```python
        # Example with no parameters
        result = await finatic.init_session()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = InitSessionParams(**kwargs) if kwargs else InitSessionParams()
        # Phase 2C: Extract individual params from input params object
        x_api_key = params.x_api_key

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('POST', '/api/v1/session/init', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Init Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/init',
            params=params_dict,
            action='init_session'
        )

        try:
            async def api_call():
                response = await self.api.init_session_api_v1_session_init_post(x_api_key=x_api_key)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict (recursively convert all nested models)
                standard_response = convert_to_plain_object(response_data)
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it (recursively convert all nested models)
                standard_response = convert_to_plain_object(response)
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/init', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Init Session completed',
                request_id=request_id,
                action='init_session'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = False
            has_offset = False
            has_pagination = has_limit and has_offset
            if has_pagination and standard_response.get('success') and isinstance(standard_response['success'].get('data'), list) and standard_response['success'].get('meta', {}).get('pagination'):
                # PaginatedData is already imported at top of file
                pagination_meta_dict = standard_response['success']['meta']['pagination']
                pagination_meta = PaginationMeta(
                    has_more=pagination_meta_dict.get('has_more', False),
                    next_offset=pagination_meta_dict.get('next_offset'),
                    current_offset=pagination_meta_dict.get('current_offset', 0),
                    limit=pagination_meta_dict.get('limit', 100)
                )
                # Get params dict for current_params
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                paginated_data = PaginatedData(
                    standard_response['success']['data'],
                    pagination_meta,
                    self.init_session,
                    params_dict,
                    self
                )
                standard_response['success']['data'] = paginated_data
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Init Session failed',
                error=str(e),
                request_id=request_id,
                action='init_session',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            # FinaticResponse is a type alias (Dict[str, Any]), not a class, so construct a dict directly
            error_response = {
                'success': {'data': None},
                'error': {
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                'warning': None,
            }
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def start_session(self, **kwargs) -> FinaticResponse[SessionResponseData]:
        """Start Session
        
        Start a session with a one-time token.

        Args:
            one_time_token (str): One-time use token obtained from init_session endpoint to authenticate and start the session
            session_start_request (SessionStartRequest): Session start request containing optional user ID to associate with the session
        Returns:
        - Dict[str, Any]: FinaticResponse[SessionResponseData] format
                     success: {data: SessionResponseData, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: POST /api/v1/session/start
        @methodId start_session_api_v1_session_start_post
        @category session
        @example
        ```python
        # Example with no parameters
        result = await finatic.start_session()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = StartSessionParams(**kwargs) if kwargs else StartSessionParams()
        # Phase 2C: Extract individual params from input params object
        one_time_token = params.one_time_token
        session_start_request = params.session_start_request

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('POST', '/api/v1/session/start', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Start Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/start',
            params=params_dict,
            action='start_session'
        )

        try:
            async def api_call():
                response = await self.api.start_session_api_v1_session_start_post(session_start_request=session_start_request, one_time_token=one_time_token)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict (recursively convert all nested models)
                standard_response = convert_to_plain_object(response_data)
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it (recursively convert all nested models)
                standard_response = convert_to_plain_object(response)
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/start', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Start Session completed',
                request_id=request_id,
                action='start_session'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = False
            has_offset = False
            has_pagination = has_limit and has_offset
            if has_pagination and standard_response.get('success') and isinstance(standard_response['success'].get('data'), list) and standard_response['success'].get('meta', {}).get('pagination'):
                # PaginatedData is already imported at top of file
                pagination_meta_dict = standard_response['success']['meta']['pagination']
                pagination_meta = PaginationMeta(
                    has_more=pagination_meta_dict.get('has_more', False),
                    next_offset=pagination_meta_dict.get('next_offset'),
                    current_offset=pagination_meta_dict.get('current_offset', 0),
                    limit=pagination_meta_dict.get('limit', 100)
                )
                # Get params dict for current_params
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                paginated_data = PaginatedData(
                    standard_response['success']['data'],
                    pagination_meta,
                    self.start_session,
                    params_dict,
                    self
                )
                standard_response['success']['data'] = paginated_data
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Start Session failed',
                error=str(e),
                request_id=request_id,
                action='start_session',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            # FinaticResponse is a type alias (Dict[str, Any]), not a class, so construct a dict directly
            error_response = {
                'success': {'data': None},
                'error': {
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                'warning': None,
            }
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_portal_url(self, **kwargs) -> FinaticResponse[PortalUrlResponse]:
        """Get Portal Url
        
        Get a portal URL with token for a session.
        
        The session must be in ACTIVE or AUTHENTICATING state and the request must come from the same device
        that initiated the session. Device info is automatically validated from the request.

        Args:
        - **kwargs: No parameters required for this method
        Returns:
        - Dict[str, Any]: FinaticResponse[PortalUrlResponse] format
                     success: {data: PortalUrlResponse, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/session/portal
        @methodId get_portal_url_api_v1_session_portal_get
        @category session
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_portal_url()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = GetPortalUrlParams(**kwargs) if kwargs else GetPortalUrlParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        # No parameters to extract

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/session/portal', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Portal Url',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/portal',
            params=params_dict,
            action='get_portal_url'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_portal_url_api_v1_session_portal_get(session_id=self.session_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict (recursively convert all nested models)
                standard_response = convert_to_plain_object(response_data)
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it (recursively convert all nested models)
                standard_response = convert_to_plain_object(response)
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/session/portal', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Portal Url completed',
                request_id=request_id,
                action='get_portal_url'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = False
            has_offset = False
            has_pagination = has_limit and has_offset
            if has_pagination and standard_response.get('success') and isinstance(standard_response['success'].get('data'), list) and standard_response['success'].get('meta', {}).get('pagination'):
                # PaginatedData is already imported at top of file
                pagination_meta_dict = standard_response['success']['meta']['pagination']
                pagination_meta = PaginationMeta(
                    has_more=pagination_meta_dict.get('has_more', False),
                    next_offset=pagination_meta_dict.get('next_offset'),
                    current_offset=pagination_meta_dict.get('current_offset', 0),
                    limit=pagination_meta_dict.get('limit', 100)
                )
                # Get params dict for current_params
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                paginated_data = PaginatedData(
                    standard_response['success']['data'],
                    pagination_meta,
                    self.get_portal_url,
                    params_dict,
                    self
                )
                standard_response['success']['data'] = paginated_data
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Portal Url failed',
                error=str(e),
                request_id=request_id,
                action='get_portal_url',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            # FinaticResponse is a type alias (Dict[str, Any]), not a class, so construct a dict directly
            error_response = {
                'success': {'data': None},
                'error': {
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                'warning': None,
            }
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_session_user(self, **kwargs) -> FinaticResponse[SessionUserResponse]:
        """Get Session User
        
        Get user information and fresh tokens for a completed session.
        
        This endpoint is designed for server SDKs to retrieve user information
        and authentication tokens after successful OTP verification.
        
        
        Security:
        - Requires valid session in ACTIVE state
        - Validates device fingerprint binding
        - Generates fresh tokens (not returning stored ones)
        - Only accessible to authenticated sessions with user_id
        - Validates that header session_id matches path session_id

        Args:
            session_id (str): Session ID
        Returns:
        - Dict[str, Any]: FinaticResponse[SessionUserResponse] format
                     success: {data: SessionUserResponse, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/session/{session_id}/user
        @methodId get_session_user_api_v1_session__session_id__user_get
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_session_user(
            session_id='sess_1234567890abcdef'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        """
        # Convert kwargs to params object
        params = GetSessionUserParams(**kwargs) if kwargs else GetSessionUserParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        session_id = params.session_id

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Session User',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/{session_id}/user',
            params=params_dict,
            action='get_session_user'
        )

        try:
            async def api_call():
                # get_session_user only needs session_id (company_id comes from session)
                if not self.session_id:
                    raise ValueError("Session context incomplete. Missing sessionId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_session_user_api_v1_session_session_id_user_get(session_id=session_id, x_session_id=self.session_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict (recursively convert all nested models)
                standard_response = convert_to_plain_object(response_data)
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it (recursively convert all nested models)
                standard_response = convert_to_plain_object(response)
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Session User completed',
                request_id=request_id,
                action='get_session_user'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = False
            has_offset = False
            has_pagination = has_limit and has_offset
            if has_pagination and standard_response.get('success') and isinstance(standard_response['success'].get('data'), list) and standard_response['success'].get('meta', {}).get('pagination'):
                # PaginatedData is already imported at top of file
                pagination_meta_dict = standard_response['success']['meta']['pagination']
                pagination_meta = PaginationMeta(
                    has_more=pagination_meta_dict.get('has_more', False),
                    next_offset=pagination_meta_dict.get('next_offset'),
                    current_offset=pagination_meta_dict.get('current_offset', 0),
                    limit=pagination_meta_dict.get('limit', 100)
                )
                # Get params dict for current_params
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                paginated_data = PaginatedData(
                    standard_response['success']['data'],
                    pagination_meta,
                    self.get_session_user,
                    params_dict,
                    self
                )
                standard_response['success']['data'] = paginated_data
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Session User failed',
                error=str(e),
                request_id=request_id,
                action='get_session_user',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            # FinaticResponse is a type alias (Dict[str, Any]), not a class, so construct a dict directly
            error_response = {
                'success': {'data': None},
                'error': {
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                'warning': None,
            }
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods
