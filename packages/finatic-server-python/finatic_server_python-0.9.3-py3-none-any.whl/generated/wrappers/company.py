"""
Generated wrapper functions for company operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/company.py instead.
"""

from __future__ import annotations

from typing import Optional, Any, Dict, List
from dataclasses import dataclass
from ..api.company_api import CompanyApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..types import FinaticResponse
from ..models.company_response import CompanyResponse
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
class GetCompanyParams:
    """Input parameters for get_company_api_v1_company__company_id__get."""
  # Company ID
    company_id: str


class CompanyWrapper:
    """Company wrapper functions.
    
    Provides simplified method names and response unwrapping.
    """
    
    def __init__(self, api: CompanyApi, config: Optional[Configuration] = None, sdk_config: Optional[SdkConfig] = None):
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

    async def get_company(self, **kwargs) -> FinaticResponse[CompanyResponse]:
        """Get Company
        
        Get public company details by ID (no user check, no sensitive data).

        Args:
            company_id (str): Company ID
        Returns:
        - Dict[str, Any]: FinaticResponse[CompanyResponse] format
                     success: {data: CompanyResponse, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/company/{company_id}
        @methodId get_company_api_v1_company__company_id__get
        @category company
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_company(
            company_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        """
        # Convert kwargs to params object
        params = GetCompanyParams(**kwargs) if kwargs else GetCompanyParams()
        # Phase 2C: Extract individual params from input params object
        company_id = params.company_id

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
            cache_key = generate_cache_key('GET', '/api/v1/company/{company_id}', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Company',
            request_id=request_id,
            method='GET',
            path='/api/v1/company/{company_id}',
            params=params_dict,
            action='get_company'
        )

        try:
            async def api_call():
                response = await self.api.get_company_api_v1_company_company_id_get(company_id=company_id)

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
                cache_key = generate_cache_key('GET', '/api/v1/company/{company_id}', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Company completed',
                request_id=request_id,
                action='get_company'
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
                    self.get_company,
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
            
            self.logger.error('Get Company failed',
                error=str(e),
                request_id=request_id,
                action='get_company',
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
