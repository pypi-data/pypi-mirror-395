"""
Generated wrapper functions for brokers operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/brokers.py instead.
"""

from __future__ import annotations

from typing import Optional, Any, Dict, List
from dataclasses import dataclass
from ..api.brokers_api import BrokersApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..types import FinaticResponse
from ..models.account_status import AccountStatus
from ..models.broker_data_account_type_enum import BrokerDataAccountTypeEnum
from ..models.broker_data_asset_type_enum import BrokerDataAssetTypeEnum
from ..models.broker_data_order_side_enum import BrokerDataOrderSideEnum
from ..models.broker_data_position_status_enum import BrokerDataPositionStatusEnum
from ..models.broker_info import BrokerInfo
from ..models.disconnect_action_result import DisconnectActionResult
from ..models.fdx_broker_account import FDXBrokerAccount
from ..models.fdx_broker_balance import FDXBrokerBalance
from ..models.fdx_broker_order import FDXBrokerOrder
from ..models.fdx_broker_order_event import FDXBrokerOrderEvent
from ..models.fdx_broker_order_fill import FDXBrokerOrderFill
from ..models.fdx_broker_order_group import FDXBrokerOrderGroup
from ..models.fdx_broker_position import FDXBrokerPosition
from ..models.fdx_broker_position_lot import FDXBrokerPositionLot
from ..models.fdx_broker_position_lot_fill import FDXBrokerPositionLotFill
from ..models.user_broker_connection_with_permissions import UserBrokerConnectionWithPermissions
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
from ..utils.pagination import PaginatedData, PaginationMeta


# Phase 2C: Input type definitions (output types use FinaticResponse[DataType] pattern - no models needed)
@dataclass
class GetBrokersParams:
    """Input parameters for get_brokers_api_v1_brokers__get."""
    pass

@dataclass
class GetBrokerConnectionsParams:
    """Input parameters for list_broker_connections_api_v1_brokers_connections_get."""
    pass

@dataclass
class DisconnectCompanyFromBrokerParams:
    """Input parameters for disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete."""
  # Connection ID
    connection_id: str

@dataclass
class GetOrdersParams:
    """Input parameters for get_orders_api_v1_brokers_data_orders_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Filter by broker provided account ID or internal account UUID
    account_id: str = None
  # Filter by symbol
    symbol: str = None
  # Filter by order status (e.g., 'filled', 'pending_new', 'cancelled')
    order_status: str = None
  # Filter by order side (e.g., 'buy', 'sell')
    side: BrokerDataOrderSideEnum = None
  # Filter by asset type (e.g., 'stock', 'option', 'crypto', 'future')
    asset_type: BrokerDataAssetTypeEnum = None
  # Maximum number of orders to return
    limit: Optional[int] = None
  # Number of orders to skip for pagination
    offset: Optional[int] = None
  # Filter orders created after this timestamp
    created_after: str = None
  # Filter orders created before this timestamp
    created_before: str = None
  # Include order metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetPositionsParams:
    """Input parameters for get_positions_api_v1_brokers_data_positions_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Filter by broker provided account ID or internal account UUID
    account_id: str = None
  # Filter by symbol
    symbol: str = None
  # Filter by position side (e.g., 'long', 'short')
    side: BrokerDataOrderSideEnum = None
  # Filter by asset type (e.g., 'stock', 'option', 'crypto', 'future')
    asset_type: BrokerDataAssetTypeEnum = None
  # Filter by position status: 'open' (quantity > 0) or 'closed' (quantity = 0)
    position_status: BrokerDataPositionStatusEnum = None
  # Maximum number of positions to return
    limit: Optional[int] = None
  # Number of positions to skip for pagination
    offset: Optional[int] = None
  # Filter positions updated after this timestamp
    updated_after: str = None
  # Filter positions updated before this timestamp
    updated_before: str = None
  # Include position metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetBalancesParams:
    """Input parameters for get_balances_api_v1_brokers_data_balances_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Filter by broker provided account ID or internal account UUID
    account_id: str = None
  # Filter by end-of-day snapshot status (true/false)
    is_end_of_day_snapshot: Optional[bool] = None
  # Maximum number of balances to return
    limit: Optional[int] = None
  # Number of balances to skip for pagination
    offset: Optional[int] = None
  # Filter balances created after this timestamp
    balance_created_after: str = None
  # Filter balances created before this timestamp
    balance_created_before: str = None
  # Include balance metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetAccountsParams:
    """Input parameters for get_accounts_api_v1_brokers_data_accounts_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Filter by account type (e.g., 'margin', 'cash', 'crypto_wallet', 'live', 'sim')
    account_type: BrokerDataAccountTypeEnum = None
  # Filter by account status (e.g., 'active', 'inactive')
    status: AccountStatus = None
  # Filter by currency (e.g., 'USD', 'EUR')
    currency: str = None
  # Maximum number of accounts to return
    limit: Optional[int] = None
  # Number of accounts to skip for pagination
    offset: Optional[int] = None
  # Include connection metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetOrderFillsParams:
    """Input parameters for get_order_fills_api_v1_brokers_data_orders__order_id__fills_get."""
  # Order ID
    order_id: str
  # Filter by connection ID
    connection_id: str = None
  # Maximum number of fills to return
    limit: Optional[int] = None
  # Number of fills to skip for pagination
    offset: Optional[int] = None
  # Include fill metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetOrderEventsParams:
    """Input parameters for get_order_events_api_v1_brokers_data_orders__order_id__events_get."""
  # Order ID
    order_id: str
  # Filter by connection ID
    connection_id: str = None
  # Maximum number of events to return
    limit: Optional[int] = None
  # Number of events to skip for pagination
    offset: Optional[int] = None
  # Include event metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetOrderGroupsParams:
    """Input parameters for get_order_groups_api_v1_brokers_data_orders_groups_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Maximum number of order groups to return
    limit: Optional[int] = None
  # Number of order groups to skip for pagination
    offset: Optional[int] = None
  # Filter order groups created after this timestamp
    created_after: str = None
  # Filter order groups created before this timestamp
    created_before: str = None
  # Include group metadata in response (excluded by default for FDX compliance)
    include_metadata: Optional[bool] = None

@dataclass
class GetPositionLotsParams:
    """Input parameters for get_position_lots_api_v1_brokers_data_positions_lots_get."""
  # Filter by broker ID
    broker_id: str = None
  # Filter by connection ID
    connection_id: str = None
  # Filter by broker provided account ID
    account_id: str = None
  # Filter by symbol
    symbol: str = None
  # Filter by position ID
    position_id: str = None
  # Maximum number of position lots to return
    limit: Optional[int] = None
  # Number of position lots to skip for pagination
    offset: Optional[int] = None

@dataclass
class GetPositionLotFillsParams:
    """Input parameters for get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get."""
  # Position lot ID
    lot_id: str
  # Filter by connection ID
    connection_id: str = None
  # Maximum number of fills to return
    limit: Optional[int] = None
  # Number of fills to skip for pagination
    offset: Optional[int] = None


class BrokersWrapper:
    """Brokers wrapper functions.
    
    Provides simplified method names and response unwrapping.
    """
    
    def __init__(self, api: BrokersApi, config: Optional[Configuration] = None, sdk_config: Optional[SdkConfig] = None):
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

    async def get_brokers(self, **kwargs) -> FinaticResponse[list[BrokerInfo]]:
        """Get Brokers
        
        Get all available brokers.
        
        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.
        
        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.

        Args:
        - **kwargs: No parameters required for this method
        Returns:
        - Dict[str, Any]: FinaticResponse[list[BrokerInfo]] format
                     success: {data: list[BrokerInfo], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/
        @methodId get_brokers_api_v1_brokers__get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_brokers()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = GetBrokersParams(**kwargs) if kwargs else GetBrokersParams()
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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Brokers',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/',
            params=params_dict,
            action='get_brokers'
        )

        try:
            async def api_call():
                response = await self.api.get_brokers_api_v1_brokers_get()

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Brokers completed',
                request_id=request_id,
                action='get_brokers'
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
                    self.get_brokers,
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
            
            self.logger.error('Get Brokers failed',
                error=str(e),
                request_id=request_id,
                action='get_brokers',
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

    async def get_broker_connections(self, **kwargs) -> FinaticResponse[list[UserBrokerConnectionWithPermissions]]:
        """List Broker Connections
        
        List all broker connections for the current user with permissions.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for, including the current
        company's permissions (read/write) for each connection.

        Args:
        - **kwargs: No parameters required for this method
        Returns:
        - Dict[str, Any]: FinaticResponse[list[UserBrokerConnectionWithPermissions]] format
                     success: {data: list[UserBrokerConnectionWithPermissions], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/connections
        @methodId list_broker_connections_api_v1_brokers_connections_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_broker_connections()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = GetBrokerConnectionsParams(**kwargs) if kwargs else GetBrokerConnectionsParams()
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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('List Broker Connections',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/connections',
            params=params_dict,
            action='get_broker_connections'
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
                response = await self.api.list_broker_connections_api_v1_brokers_connections_get(_headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('List Broker Connections completed',
                request_id=request_id,
                action='get_broker_connections'
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
                    self.get_broker_connections,
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
            
            self.logger.error('List Broker Connections failed',
                error=str(e),
                request_id=request_id,
                action='get_broker_connections',
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

    async def disconnect_company_from_broker(self, **kwargs) -> FinaticResponse[DisconnectActionResult]:
        """Disconnect Company From Broker
        
        Remove a company's access to a broker connection.
        
        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.

        Args:
            connection_id (str): Connection ID
        Returns:
        - Dict[str, Any]: FinaticResponse[DisconnectActionResult] format
                     success: {data: DisconnectActionResult, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: DELETE /api/v1/brokers/disconnect-company/{connection_id}
        @methodId disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.disconnect_company_from_broker(
            connection_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        """
        # Convert kwargs to params object
        params = DisconnectCompanyFromBrokerParams(**kwargs) if kwargs else DisconnectCompanyFromBrokerParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        connection_id = params.connection_id

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
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Disconnect Company From Broker',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/disconnect-company/{connection_id}',
            params=params_dict,
            action='disconnect_company_from_broker'
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
                response = await self.api.disconnect_company_from_broker_api_v1_brokers_disconnect_company_connection_id_delete(connection_id=connection_id, _headers=headers)

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
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Disconnect Company From Broker completed',
                request_id=request_id,
                action='disconnect_company_from_broker'
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
                    self.disconnect_company_from_broker,
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
            
            self.logger.error('Disconnect Company From Broker failed',
                error=str(e),
                request_id=request_id,
                action='disconnect_company_from_broker',
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

    async def get_orders(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrder]]:
        """Get Orders
        
        Get orders for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_id (str, optional): Filter by broker provided account ID or internal account UUID
            symbol (str, optional): Filter by symbol
            order_status (str, optional): Filter by order status (e.g., 'filled', 'pending_new', 'cancelled')
            side (BrokerDataOrderSideEnum, optional): Filter by order side (e.g., 'buy', 'sell')
            asset_type (BrokerDataAssetTypeEnum, optional): Filter by asset type (e.g., 'stock', 'option', 'crypto', 'future')
            limit (int, optional): Maximum number of orders to return
            offset (int, optional): Number of orders to skip for pagination
            created_after (str, optional): Filter orders created after this timestamp
            created_before (str, optional): Filter orders created before this timestamp
            include_metadata (bool, optional): Include order metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerOrder]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders
        @methodId get_orders_api_v1_brokers_data_orders_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_orders()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_orders(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrdersParams(**kwargs) if kwargs else GetOrdersParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        order_status = getattr(params, 'order_status', None)
        side = coerce_enum_value(getattr(params, 'side', None), BrokerDataOrderSideEnum, 'side') if getattr(params, 'side', None) is not None else None
        asset_type = coerce_enum_value(getattr(params, 'asset_type', None), BrokerDataAssetTypeEnum, 'asset_type') if getattr(params, 'asset_type', None) is not None else None
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        created_after = getattr(params, 'created_after', None)
        created_before = getattr(params, 'created_before', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Orders',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders',
            params=params_dict,
            action='get_orders'
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
                response = await self.api.get_orders_api_v1_brokers_data_orders_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, order_status=order_status, side=side, asset_type=asset_type, limit=limit, offset=offset, created_after=created_after, created_before=created_before, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Orders completed',
                request_id=request_id,
                action='get_orders'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_orders,
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
            
            self.logger.error('Get Orders failed',
                error=str(e),
                request_id=request_id,
                action='get_orders',
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

    async def get_positions(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPosition]]:
        """Get Positions
        
        Get positions for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_id (str, optional): Filter by broker provided account ID or internal account UUID
            symbol (str, optional): Filter by symbol
            side (BrokerDataOrderSideEnum, optional): Filter by position side (e.g., 'long', 'short')
            asset_type (BrokerDataAssetTypeEnum, optional): Filter by asset type (e.g., 'stock', 'option', 'crypto', 'future')
            position_status (BrokerDataPositionStatusEnum, optional): Filter by position status: 'open' (quantity > 0) or 'closed' (quantity = 0)
            limit (int, optional): Maximum number of positions to return
            offset (int, optional): Number of positions to skip for pagination
            updated_after (str, optional): Filter positions updated after this timestamp
            updated_before (str, optional): Filter positions updated before this timestamp
            include_metadata (bool, optional): Include position metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerPosition]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions
        @methodId get_positions_api_v1_brokers_data_positions_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_positions()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_positions(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionsParams(**kwargs) if kwargs else GetPositionsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        side = coerce_enum_value(getattr(params, 'side', None), BrokerDataOrderSideEnum, 'side') if getattr(params, 'side', None) is not None else None
        asset_type = coerce_enum_value(getattr(params, 'asset_type', None), BrokerDataAssetTypeEnum, 'asset_type') if getattr(params, 'asset_type', None) is not None else None
        position_status = coerce_enum_value(getattr(params, 'position_status', None), BrokerDataPositionStatusEnum, 'position_status') if getattr(params, 'position_status', None) is not None else None
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        updated_after = getattr(params, 'updated_after', None)
        updated_before = getattr(params, 'updated_before', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Positions',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions',
            params=params_dict,
            action='get_positions'
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
                response = await self.api.get_positions_api_v1_brokers_data_positions_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, side=side, asset_type=asset_type, position_status=position_status, limit=limit, offset=offset, updated_after=updated_after, updated_before=updated_before, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Positions completed',
                request_id=request_id,
                action='get_positions'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_positions,
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
            
            self.logger.error('Get Positions failed',
                error=str(e),
                request_id=request_id,
                action='get_positions',
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

    async def get_balances(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerBalance]]:
        """Get Balances
        
        Get balances for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_id (str, optional): Filter by broker provided account ID or internal account UUID
            is_end_of_day_snapshot (bool, optional): Filter by end-of-day snapshot status (true/false)
            limit (int, optional): Maximum number of balances to return
            offset (int, optional): Number of balances to skip for pagination
            balance_created_after (str, optional): Filter balances created after this timestamp
            balance_created_before (str, optional): Filter balances created before this timestamp
            include_metadata (bool, optional): Include balance metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerBalance]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/balances
        @methodId get_balances_api_v1_brokers_data_balances_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_balances()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_balances(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetBalancesParams(**kwargs) if kwargs else GetBalancesParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        is_end_of_day_snapshot = getattr(params, 'is_end_of_day_snapshot', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        balance_created_after = getattr(params, 'balance_created_after', None)
        balance_created_before = getattr(params, 'balance_created_before', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Balances',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/balances',
            params=params_dict,
            action='get_balances'
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
                response = await self.api.get_balances_api_v1_brokers_data_balances_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, is_end_of_day_snapshot=is_end_of_day_snapshot, limit=limit, offset=offset, balance_created_after=balance_created_after, balance_created_before=balance_created_before, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Balances completed',
                request_id=request_id,
                action='get_balances'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_balances,
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
            
            self.logger.error('Get Balances failed',
                error=str(e),
                request_id=request_id,
                action='get_balances',
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

    async def get_accounts(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerAccount]]:
        """Get Accounts
        
        Get accounts for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_type (BrokerDataAccountTypeEnum, optional): Filter by account type (e.g., 'margin', 'cash', 'crypto_wallet', 'live', 'sim')
            status (AccountStatus, optional): Filter by account status (e.g., 'active', 'inactive')
            currency (str, optional): Filter by currency (e.g., 'USD', 'EUR')
            limit (int, optional): Maximum number of accounts to return
            offset (int, optional): Number of accounts to skip for pagination
            include_metadata (bool, optional): Include connection metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerAccount]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/accounts
        @methodId get_accounts_api_v1_brokers_data_accounts_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_accounts()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_accounts(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_type='margin'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetAccountsParams(**kwargs) if kwargs else GetAccountsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_type = coerce_enum_value(getattr(params, 'account_type', None), BrokerDataAccountTypeEnum, 'account_type') if getattr(params, 'account_type', None) is not None else None
        status = getattr(params, 'status', None)
        currency = getattr(params, 'currency', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Accounts',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/accounts',
            params=params_dict,
            action='get_accounts'
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
                response = await self.api.get_accounts_api_v1_brokers_data_accounts_get(broker_id=broker_id, connection_id=connection_id, account_type=account_type, status=status, currency=currency, limit=limit, offset=offset, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Accounts completed',
                request_id=request_id,
                action='get_accounts'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_accounts,
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
            
            self.logger.error('Get Accounts failed',
                error=str(e),
                request_id=request_id,
                action='get_accounts',
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

    async def get_order_fills(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderFill]]:
        """Get Order Fills
        
        Get order fills for a specific order.
        
        This endpoint returns all execution fills for the specified order.

        Args:
            order_id (str): Order ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of fills to return
            offset (int, optional): Number of fills to skip for pagination
            include_metadata (bool, optional): Include fill metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerOrderFill]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/fills
        @methodId get_order_fills_api_v1_brokers_data_orders__order_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_order_fills(
            order_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_fills(
            order_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderFillsParams(**kwargs) if kwargs else GetOrderFillsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/fills',
            params=params_dict,
            action='get_order_fills'
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
                response = await self.api.get_order_fills_api_v1_brokers_data_orders_order_id_fills_get(order_id=order_id, connection_id=connection_id, limit=limit, offset=offset, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Fills completed',
                request_id=request_id,
                action='get_order_fills'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_order_fills,
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
            
            self.logger.error('Get Order Fills failed',
                error=str(e),
                request_id=request_id,
                action='get_order_fills',
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

    async def get_order_events(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderEvent]]:
        """Get Order Events
        
        Get order events for a specific order.
        
        This endpoint returns all lifecycle events for the specified order.

        Args:
            order_id (str): Order ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of events to return
            offset (int, optional): Number of events to skip for pagination
            include_metadata (bool, optional): Include event metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerOrderEvent]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/events
        @methodId get_order_events_api_v1_brokers_data_orders__order_id__events_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_order_events(
            order_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_events(
            order_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderEventsParams(**kwargs) if kwargs else GetOrderEventsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Events',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/events',
            params=params_dict,
            action='get_order_events'
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
                response = await self.api.get_order_events_api_v1_brokers_data_orders_order_id_events_get(order_id=order_id, connection_id=connection_id, limit=limit, offset=offset, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Events completed',
                request_id=request_id,
                action='get_order_events'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_order_events,
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
            
            self.logger.error('Get Order Events failed',
                error=str(e),
                request_id=request_id,
                action='get_order_events',
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

    async def get_order_groups(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderGroup]]:
        """Get Order Groups
        
        Get order groups.
        
        This endpoint returns order groups that contain multiple orders.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of order groups to return
            offset (int, optional): Number of order groups to skip for pagination
            created_after (str, optional): Filter order groups created after this timestamp
            created_before (str, optional): Filter order groups created before this timestamp
            include_metadata (bool, optional): Include group metadata in response (excluded by default for FDX compliance)
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerOrderGroup]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/groups
        @methodId get_order_groups_api_v1_brokers_data_orders_groups_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_order_groups()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_groups(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderGroupsParams(**kwargs) if kwargs else GetOrderGroupsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        created_after = getattr(params, 'created_after', None)
        created_before = getattr(params, 'created_before', None)
        include_metadata = getattr(params, 'include_metadata', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Groups',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/groups',
            params=params_dict,
            action='get_order_groups'
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
                response = await self.api.get_order_groups_api_v1_brokers_data_orders_groups_get(broker_id=broker_id, connection_id=connection_id, limit=limit, offset=offset, created_after=created_after, created_before=created_before, include_metadata=include_metadata, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Groups completed',
                request_id=request_id,
                action='get_order_groups'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_order_groups,
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
            
            self.logger.error('Get Order Groups failed',
                error=str(e),
                request_id=request_id,
                action='get_order_groups',
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

    async def get_position_lots(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPositionLot]]:
        """Get Position Lots
        
        Get position lots (tax lots for positions).
        
        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.

        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_id (str, optional): Filter by broker provided account ID
            symbol (str, optional): Filter by symbol
            position_id (str, optional): Filter by position ID
            limit (int, optional): Maximum number of position lots to return
            offset (int, optional): Number of position lots to skip for pagination
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerPositionLot]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions/lots
        @methodId get_position_lots_api_v1_brokers_data_positions_lots_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_position_lots()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_position_lots(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionLotsParams(**kwargs) if kwargs else GetPositionLotsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        position_id = getattr(params, 'position_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Position Lots',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots',
            params=params_dict,
            action='get_position_lots'
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
                response = await self.api.get_position_lots_api_v1_brokers_data_positions_lots_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, position_id=position_id, limit=limit, offset=offset, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Position Lots completed',
                request_id=request_id,
                action='get_position_lots'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_position_lots,
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
            
            self.logger.error('Get Position Lots failed',
                error=str(e),
                request_id=request_id,
                action='get_position_lots',
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

    async def get_position_lot_fills(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPositionLotFill]]:
        """Get Position Lot Fills
        
        Get position lot fills for a specific lot.
        
        This endpoint returns all fills associated with a specific position lot.

        Args:
            lot_id (str): Position lot ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of fills to return
            offset (int, optional): Number of fills to skip for pagination
        Returns:
        - Dict[str, Any]: FinaticResponse[PaginatedData[FDXBrokerPositionLotFill]] format
                     success: {data: PaginatedData[T], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions/lots/{lot_id}/fills
        @methodId get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_position_lot_fills(
            lot_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_position_lot_fills(
            lot_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionLotFillsParams(**kwargs) if kwargs else GetPositionLotFillsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        lot_id = params.lot_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

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
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Position Lot Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots/{lot_id}/fills',
            params=params_dict,
            action='get_position_lot_fills'
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
                response = await self.api.get_position_lot_fills_api_v1_brokers_data_positions_lots_lot_id_fills_get(lot_id=lot_id, connection_id=connection_id, limit=limit, offset=offset, _headers=headers)

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
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Position Lot Fills completed',
                request_id=request_id,
                action='get_position_lot_fills'
            )
            
            # Phase 2: Wrap paginated responses with PaginatedData
            has_limit = True
            has_offset = True
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
                    self.get_position_lot_fills,
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
            
            self.logger.error('Get Position Lot Fills failed',
                error=str(e),
                request_id=request_id,
                action='get_position_lot_fills',
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
