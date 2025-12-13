"""
Main client class for Finatic Server SDK (Python).

This file is regenerated on each run - do not edit directly.
For custom logic, extend this class or use custom wrappers.
"""

from __future__ import annotations

from typing import Optional, Dict, Any, List, Union
from .configuration import Configuration
from .api_client import ApiClient
from .config import SdkConfig, get_config
from .types import FinaticResponse
from .utils.url_utils import append_theme_to_url, append_broker_filter_to_url
from .utils.logger import get_logger
from .models.session_response_data import SessionResponseData
from .models.session_user_response import SessionUserResponse

from .api.brokers_api import BrokersApi
from .api.company_api import CompanyApi
from .api.session_api import SessionApi

from .wrappers.brokers import BrokersWrapper
from .wrappers.company import CompanyWrapper
from .wrappers.session import SessionWrapper

from .wrappers.company import GetCompanyParams
from .wrappers.brokers import DisconnectCompanyFromBrokerParams, GetAccountsParams, GetBalancesParams, GetBrokerConnectionsParams, GetBrokersParams, GetOrderEventsParams, GetOrderFillsParams, GetOrderGroupsParams, GetOrdersParams, GetPositionLotFillsParams, GetPositionLotsParams, GetPositionsParams

from .wrappers.brokers import GetOrdersParams
from .models.fdx_broker_order import FDXBrokerOrder
from .wrappers.brokers import GetPositionsParams
from .models.fdx_broker_position import FDXBrokerPosition
from .wrappers.brokers import GetBalancesParams
from .models.fdx_broker_balance import FDXBrokerBalance
from .wrappers.brokers import GetAccountsParams
from .models.fdx_broker_account import FDXBrokerAccount
from .wrappers.brokers import GetOrderFillsParams
from .models.fdx_broker_order_fill import FDXBrokerOrderFill
from .wrappers.brokers import GetOrderEventsParams
from .models.fdx_broker_order_event import FDXBrokerOrderEvent
from .wrappers.brokers import GetOrderGroupsParams
from .models.fdx_broker_order_group import FDXBrokerOrderGroup
from .wrappers.brokers import GetPositionLotsParams
from .models.fdx_broker_position_lot import FDXBrokerPositionLot
from .wrappers.brokers import GetPositionLotFillsParams
from .models.fdx_broker_position_lot_fill import FDXBrokerPositionLotFill


class FinaticServer:
    """Main client class for Finatic Server SDK."""

    @classmethod
    async def init(
        cls,
        api_key: str,
        user_id: Optional[str] = None,
        sdk_config: Optional[SdkConfig] = None,
    ) -> 'FinaticServer':
        """Initialize and create a FinaticServer instance with session started.
        
        This is the recommended way to initialize the SDK. It creates an instance
        and automatically starts a session using the provided API key.
        
        @methodId init_server_sdk
        @category session
        
        Args:
            api_key: Company API key (required)
            user_id: Optional user ID for direct authentication
            sdk_config: Optional SDK configuration overrides (includes base_url)
        
        Returns:
            FinaticServer instance with session already initialized
        
        @example
        ```python
        client = await FinaticServer.init(
            api_key="fntc_live_your_key",
            user_id="optional_user_id",
            sdk_config={'base_url': 'https://api.finatic.dev', 'log_level': 'debug'}
        )
        # Session is already started, ready to use
        orders = await client.get_all_orders()
        ```
        @example
        ```typescript-server
        const finatic = await FinaticServer.init('your-api-key', 'optional-user-id', {
          baseUrl: 'https://api.finatic.dev',
          logLevel: 'debug'
        });
        ```
        """
        # Create instance (base_url is extracted from sdk_config in __init__)
        instance = cls(api_key, sdk_config)
        
        # Initialize session automatically
        try:
            # Start session using the instance's start_session method
            # This will use the API key from constructor and get token internally
            # Returns FinaticResponse[SessionResponseData] format
            session_result = await instance.start_session(user_id=user_id) if user_id else await instance.start_session()
            
            # Check if session was started successfully (FinaticResponse[SessionResponseData] format)
            if session_result.get('error'):
                error_data = session_result.get('error', {})
                if isinstance(error_data, dict):
                    error_msg = error_data.get('message', 'Unknown error')
                else:
                    error_msg = str(error_data)
                raise ValueError(
                    f"Session initialization failed: {error_msg}. "
                    "Please check that the API endpoint returned a valid session response and ensure the API key is valid."
                )
            
            # Verify session was initialized correctly
            session_id = instance.get_session_id()
            if not session_id:
                raise ValueError(
                    "Session initialization failed: start_session() did not return a session_id. "
                    "Please check that the API endpoint returned a valid session response."
                )
            
            return instance
        except ValueError:
            # Re-raise ValueError as-is (already has good error message)
            raise
        except Exception as e:
            # Re-raise with more context if it's a session initialization error
            # Safely convert exception to string to avoid type formatting issues
            try:
                error_str = str(e) if e else 'Unknown error'
            except Exception:
                error_str = f'Exception of type {type(e).__name__}'
            
            if "Session not initialized" in error_str or "session_id" in error_str.lower():
                raise ValueError(
                    f"Failed to initialize Finatic session: {error_str}. "
                    "This may indicate that start_session() was called but did not successfully create a session. "
                    "Please check the API response and ensure the API key is valid."
                ) from e
            raise ValueError(
                f"Session initialization failed: {error_str}. "
                "Please check that the API endpoint returned a valid session response and ensure the API key is valid."
            ) from e

    def __init__(
        self,
        api_key: str,
        sdk_config: Optional[SdkConfig] = None,
    ):
        """Initialize the client.
        
        Note: For automatic session initialization, use FinaticServer.init() instead.
        This constructor creates an instance but does not start a session.
        
        Args:
            api_key: Company API key
            sdk_config: Optional SDK configuration overrides (includes base_url)
        """
        self.api_key = api_key
        # Extract base_url from sdk_config if provided
        base_url = None
        if sdk_config:
            if isinstance(sdk_config, dict):
                base_url = sdk_config.get('base_url')
            elif hasattr(sdk_config, 'base_url'):
                base_url = sdk_config.base_url
        
        self.config = Configuration(
            host=base_url or 'https://api.finatic.dev',
            api_key={'X-API-Key': api_key},
        )
        # Create ApiClient from Configuration for API classes
        self.api_client = ApiClient(self.config)
        # Merge sdk_config with defaults
        if sdk_config:
            default = get_config()
            # If sdk_config is a SdkConfig instance, merge its attributes
            if isinstance(sdk_config, SdkConfig):
                for key in sdk_config.__dataclass_fields__:
                    if hasattr(sdk_config, key):
                        setattr(default, key, getattr(sdk_config, key))
            # If it's a dict, merge the values
            elif isinstance(sdk_config, dict):
                for key, value in sdk_config.items():
                    if hasattr(default, key):
                        setattr(default, key, value)
            self.sdk_config = default
        else:
            self.sdk_config = get_config()
        
        self.session_id: Optional[str] = None
        self.company_id: Optional[str] = None
        self.csrf_token: Optional[str] = None
        self.user_id: Optional[str] = None
        
        # Initialize logger
        self.logger = get_logger(self.sdk_config)

        self._brokers = BrokersWrapper(BrokersApi(self.api_client), self.config, self.sdk_config)
        self._company = CompanyWrapper(CompanyApi(self.api_client), self.config, self.sdk_config)
        self._session = SessionWrapper(SessionApi(self.api_client), self.config, self.sdk_config)

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        pass

    def set_session_context(self, session_id: str, company_id: str, csrf_token: str) -> None:
        """Set session context for all wrappers.
        
        Args:
            session_id: Session ID
            company_id: Company ID
            csrf_token: CSRF token
        """
        self.session_id = session_id
        self.company_id = company_id
        self.csrf_token = csrf_token
        
        # Update all wrappers with session context
        self._brokers.set_session_context(session_id, company_id, csrf_token)
        self._company.set_session_context(session_id, company_id, csrf_token)
        self._session.set_session_context(session_id, company_id, csrf_token)

    def get_session_id(self) -> Optional[str]:
        """Get current session ID."""
        return self.session_id

    def get_company_id(self) -> Optional[str]:
        """Get current company ID."""
        return self.company_id

    def get_user_id(self) -> Optional[str]:
        """Get current user ID (set after portal authentication).
        
        @methodId get_user_id_helper
        @category session
        
        Returns:
            Current user ID or None if not authenticated
        
        @example
        ```python
        user_id = finatic.get_user_id()
        ```
        @example
        ```typescript-server
        const userId = finatic.getUserId();
        ```
        @example
        ```typescript-client
        const userId = finatic.getUserId();
        ```
        """
        return self.user_id

    def is_authed(self) -> bool:
        """Check if user is authenticated (has userId).
        
        @methodId is_authed_helper
        @category session
        
        Returns:
            True if user is authenticated, False otherwise
        
        @example
        ```python
        is_authenticated = finatic.is_authed()
        ```
        @example
        ```typescript-server
        const isAuthenticated = finatic.isAuthed();
        ```
        @example
        ```typescript-client
        const isAuthenticated = finatic.isAuthed();
        ```
        """
        return bool(self.user_id)

    async def _init_session(self, x_api_key: str) -> str:
        """Initialize a session by getting a one-time token (internal/private).
        
        Args:
            x_api_key: Company API key
        
        Returns:
            One-time token
        """
        # Call wrapper method with keyword arguments (standardized format)
        # Returns dict (FinaticResponse[TokenResponseData])
        response = await self._session.init_session(x_api_key=x_api_key)
        if response.get('error'):
            error_msg = response.get('error', {}).get('message', 'Failed to initialize session') if isinstance(response.get('error'), dict) else str(response.get('error'))
            raise Exception(error_msg)
        success_data = response.get('success', {})
        return success_data.get('data', {}).get('one_time_token', '') if isinstance(success_data, dict) else ''

    async def get_token(self, api_key: Optional[str] = None) -> str:
        """Get a one-time token from an API key.
        
        This method only retrieves the token and returns it - it does NOT start a session
        or set any session context. Useful for generating tokens to pass to clients.
        
        @methodId init_session_api_v1_session_init_post
        @category session
        
        Args:
            api_key: Company API key (uses instance API key if not provided)
        
        Returns:
            One-time token string
        
        Raises:
            Exception: If API key is missing or token generation fails
        
        @example
        ```python
        token = await finatic.get_token()
        ```
        @example
        ```typescript-server
        const token = await finatic.getToken();
        ```
        @example
        ```typescript-client
        const token = await finatic.getToken();
        ```
        """
        key_to_use = api_key or self.api_key
        if not key_to_use:
            raise Exception('API key is required. Provide it as a parameter or in the constructor.')
        return await self._init_session(key_to_use)

    async def start_session(
        self,
        **kwargs
    ) -> FinaticResponse[SessionResponseData]:
        """Start a session using the API key from constructor.
        
        Gets a one-time token using the API key from constructor, then starts the session.
        This method is exposed for advanced use cases. For most use cases, use FinaticServer.init() instead.
        
        @methodId start_session_api_v1_session_start_post
        @category session
        
        Args:
            one_time_token: Optional one-time token. If not provided, will get one using API key.
            user_id: Optional user ID for direct authentication
        
        Returns:
            Dict[str, Any]: FinaticResponse[SessionResponseData] format
                success: {data: SessionResponseData, meta: dict | None}
                error: dict | None
                warning: list[dict] | None
        
        Raises:
            Exception: If API key is missing or session start fails
        
        @example
        ```python
        result = await finatic.start_session(one_time_token='token', user_id='optional_user_id')
        ```
        @example
        ```typescript-server
        const result = await finatic.startSession({ oneTimeToken, userId });
        ```
        @example
        ```typescript-client
        const result = await finatic.startSession({ oneTimeToken, userId });
        ```
        """
        one_time_token = kwargs.get('one_time_token')
        user_id = kwargs.get('user_id')
        
        # If token provided, use it directly
        if one_time_token:
            session_start_request = {"user_id": user_id} if user_id else {}
            response = await self._session.start_session(
                one_time_token=one_time_token,
                session_start_request=session_start_request
            )
            
            # Extract session data and set context if successful
            if response.get('success') and not response.get('error'):
                session_data = response['success'].get('data', {}) if isinstance(response.get('success'), dict) else {}
                session_id = session_data.get('session_id', '') if isinstance(session_data, dict) else ''
                company_id = session_data.get('company_id', '') if isinstance(session_data, dict) else ''
                user_id = session_data.get('user_id', '') if isinstance(session_data, dict) else ''
                csrf_token = ''
                
                if session_id and company_id:
                    self.set_session_context(session_id, company_id, csrf_token)
                
                # Store user_id if present in response (for get_user_id() and is_authed())
                if user_id:
                    self.user_id = user_id
            
            return response
        
        # No token provided - get one using API key
        if not self.api_key:
            return {
                'success': {'data': None, 'meta': None},
                'error': {'message': 'API key is required. Provide it in the constructor.'},
                'warning': None
            }

        try:
            # Step 1: Get one-time token using API key from constructor
            one_time_token = await self._init_session(self.api_key)
            
            if not one_time_token or not isinstance(one_time_token, str):
                return {
                    'success': {'data': None, 'meta': None},
                    'error': {'message': 'Failed to get one-time token'},
                    'warning': None
                }

            # Step 2: Start session with the token - returns FinaticResponse[SessionResponseData]
            session_start_request = {"user_id": user_id} if user_id else {}
            response = await self._session.start_session(
                one_time_token=one_time_token,
                session_start_request=session_start_request
            )
            
            # Extract session data and set context if successful
            if response.get('success') and not response.get('error'):
                session_data = response['success'].get('data', {}) if isinstance(response.get('success'), dict) else {}
                session_id = session_data.get('session_id', '') if isinstance(session_data, dict) else ''
                company_id = session_data.get('company_id', '') if isinstance(session_data, dict) else ''
                user_id = session_data.get('user_id', '') if isinstance(session_data, dict) else ''
                csrf_token = ''
                
                if session_id and company_id:
                    self.set_session_context(session_id, company_id, csrf_token)
                
                # Store user_id if present in response (for get_user_id() and is_authed())
                if user_id:
                    self.user_id = user_id
            
            # Return the standard response format (already FinaticResponse[SessionResponseData])
            return response
        except Exception as e:
            return {
                'success': {'data': None, 'meta': None},
                'error': {'message': str(e)},
                'warning': None
            }

    async def get_portal_url(
        self,
        **kwargs
    ) -> str:
        """Get portal URL with optional theme, broker filters, email, and mode.
        
        This is where URL manipulation happens (not in session wrapper).
        Returns the URL - app can use it as needed.
        
        @methodId get_portal_url_api_v1_session_portal_get
        @category session
        
        Args:
            theme: Optional theme configuration (preset string or custom dict)
            brokers: Optional list of broker names/IDs to filter
            email: Optional email for pre-filling
            mode: Optional mode ('light' or 'dark')
        
        Returns:
            Portal URL with all parameters appended
        
        @example
        ```python
        url = await finatic.get_portal_url(theme='default', brokers=['broker-1'], email='user@example.com', mode='dark')
        ```
        @example
        ```typescript-server
        const url = await finatic.getPortalUrl({ theme: 'default', brokers: ['broker-1'], email: 'user@example.com', mode: 'dark' });
        ```
        @example
        ```typescript-client
        const url = await finatic.getPortalUrl({ theme: 'default', brokers: ['broker-1'], email: 'user@example.com', mode: 'dark' });
        ```
        """
        theme = kwargs.get('theme')
        brokers = kwargs.get('brokers')
        email = kwargs.get('email')
        mode = kwargs.get('mode')
        
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Get raw portal URL from session wrapper (using keyword arguments)
        # Returns dict (FinaticResponse[PortalUrlResponse])
        response = await self._session.get_portal_url()
        
        # Check for errors
        if response.get('error'):
            error_msg = response.get('error', {}).get('message', 'Failed to get portal URL') if isinstance(response.get('error'), dict) else str(response.get('error'))
            self.logger.error('Failed to get portal URL', extra={
                'error': error_msg,
                'code': response.get('error', {}).get('code') if isinstance(response.get('error'), dict) else None,
                'status': response.get('error', {}).get('status') if isinstance(response.get('error'), dict) else None,
            })
            raise Exception(error_msg)
        
        # Extract portal URL from standard response structure
        success_data = response.get('success', {})
        if success_data and isinstance(success_data, dict):
            data = success_data.get('data', {})
            portal_url = data.get('portal_url', '') if isinstance(data, dict) else ''
        else:
            self.logger.error('Invalid portal URL response: missing data', extra={})
            raise ValueError('Invalid portal URL response: missing portal_url')
        
        if not portal_url:
            self.logger.error('Empty portal URL from API', extra={})
            raise ValueError('Empty portal URL received from API')

        # Validate URL before manipulation
        from urllib.parse import urlparse
        try:
            parsed = urlparse(portal_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f'Invalid portal URL format: {portal_url}')
        except Exception as e:
            self.logger.error('Invalid portal URL from API', extra={'portal_url': portal_url, 'error': str(e)})
            raise ValueError(f'Invalid portal URL received from API: {portal_url}')

        # Append theme if provided
        if theme:
            portal_url = append_theme_to_url(portal_url, theme)

        # Append broker filter if provided
        if brokers:
            portal_url = append_broker_filter_to_url(portal_url, brokers)

        # Append email if provided
        if email:
            from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params['email'] = [email]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Append mode if provided (light or dark)
        if mode:
            from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params['mode'] = [mode]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Note: session_id and company_id should NOT be added to the portal URL
        # The backend includes the token in the URL, and session context is handled via headers

        self.logger.debug('Portal URL generated', extra={'portal_url': portal_url})
        return portal_url

    async def get_session_user(self) -> FinaticResponse[SessionUserResponse]:
        """Get session user information after portal authentication.
        
        @methodId get_session_user_api_v1_session__session_id__user_get
        @category session
        
        Returns:
            Dict[str, Any]: FinaticResponse[SessionUserResponse] format
                success: {data: SessionUserResponse, meta: dict | None}
                error: dict | None
                warning: list[dict] | None
        
        @example
        ```python
        user = await finatic.get_session_user()
        ```
        @example
        ```typescript-server
        const user = await finatic.getSessionUser();
        ```
        @example
        ```typescript-client
        const user = await finatic.getSessionUser();
        ```
        """
        if not self.session_id or not self.company_id:
            raise ValueError('Session not initialized. Call start_session() first.')
        
        # get_session_user uses session_id in the path and company_id from session context
        # Call wrapper method with keyword arguments (standardized format)
        # Returns FinaticResponse[SessionUserResponse] - maintain the structure
        response = await self._session.get_session_user(session_id=self.session_id)
        
        # Extract user_id from response for internal state management
        if response.get('success') and isinstance(response.get('success'), dict):
            data = response['success'].get('data', {})
            user_id = data.get('user_id', '') if isinstance(data, dict) else ''
            # Store user_id for get_user_id() method
            if user_id:
                self.user_id = user_id
        
        # Return the full FinaticResponse[SessionUserResponse] structure
        return response


    async def get_all_orders(self, **kwargs) -> FinaticResponse[list[FDXBrokerOrder]]:
        """Get all orders across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_orders method with internal pagination handling.
        
        @methodId get_all_orders_api_v1_brokers_data_orders_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllOrders({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllOrders({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_orders(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    account_id='123456789'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrdersParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrdersParams(**filtered_kwargs) if filtered_kwargs else GetOrdersParams()
        else:
            params = GetOrdersParams()
        
        all_data: list[FDXBrokerOrder] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_orders(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_positions(self, **kwargs) -> FinaticResponse[list[FDXBrokerPosition]]:
        """Get all positions across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_positions method with internal pagination handling.
        
        @methodId get_all_positions_api_v1_brokers_data_positions_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_positions(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllPositions({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllPositions({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_positions(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    account_id='123456789'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionsParams(**filtered_kwargs) if filtered_kwargs else GetPositionsParams()
        else:
            params = GetPositionsParams()
        
        all_data: list[FDXBrokerPosition] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_positions(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_balances(self, **kwargs) -> FinaticResponse[list[FDXBrokerBalance]]:
        """Get all balances across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_balances method with internal pagination handling.
        
        @methodId get_all_balances_api_v1_brokers_data_balances_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_balances(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllBalances({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllBalances({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_balances(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    account_id='123456789'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetBalancesParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetBalancesParams(**filtered_kwargs) if filtered_kwargs else GetBalancesParams()
        else:
            params = GetBalancesParams()
        
        all_data: list[FDXBrokerBalance] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_balances(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_accounts(self, **kwargs) -> FinaticResponse[list[FDXBrokerAccount]]:
        """Get all accounts across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_accounts method with internal pagination handling.
        
        @methodId get_all_accounts_api_v1_brokers_data_accounts_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_accounts(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllAccounts({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountType: 'margin' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllAccounts({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountType: 'margin' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_accounts(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    account_type='margin'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetAccountsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetAccountsParams(**filtered_kwargs) if filtered_kwargs else GetAccountsParams()
        else:
            params = GetAccountsParams()
        
        all_data: list[FDXBrokerAccount] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_accounts(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_fills(self, **kwargs) -> FinaticResponse[list[FDXBrokerOrderFill]]:
        """Get all order_fills across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_order_fills method with internal pagination handling.
        
        @methodId get_all_order_fills_api_v1_brokers_data_orders__order_id__fills_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_order_fills(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderFills({ connectionId: '00000000-0000-0000-0000-000000000000', includeMetadata: false });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderFills({ connectionId: '00000000-0000-0000-0000-000000000000', includeMetadata: false });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_order_fills(
           *            connection_id='00000000-0000-0000-0000-000000000000',
                    include_metadata=false
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderFillsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderFillsParams(**filtered_kwargs) if filtered_kwargs else GetOrderFillsParams()
        else:
            params = GetOrderFillsParams()
        
        all_data: list[FDXBrokerOrderFill] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_fills(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_events(self, **kwargs) -> FinaticResponse[list[FDXBrokerOrderEvent]]:
        """Get all order_events across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_order_events method with internal pagination handling.
        
        @methodId get_all_order_events_api_v1_brokers_data_orders__order_id__events_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_order_events(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderEvents({ connectionId: '00000000-0000-0000-0000-000000000000', includeMetadata: false });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderEvents({ connectionId: '00000000-0000-0000-0000-000000000000', includeMetadata: false });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_order_events(
           *            connection_id='00000000-0000-0000-0000-000000000000',
                    include_metadata=false
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderEventsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderEventsParams(**filtered_kwargs) if filtered_kwargs else GetOrderEventsParams()
        else:
            params = GetOrderEventsParams()
        
        all_data: list[FDXBrokerOrderEvent] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_events(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_groups(self, **kwargs) -> FinaticResponse[list[FDXBrokerOrderGroup]]:
        """Get all order_groups across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_order_groups method with internal pagination handling.
        
        @methodId get_all_order_groups_api_v1_brokers_data_orders_groups_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_order_groups(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderGroups({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', createdAfter: '2024-01-01T00:00:00Z' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllOrderGroups({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', createdAfter: '2024-01-01T00:00:00Z' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_order_groups(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    created_after='2024-01-01T00:00:00Z'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderGroupsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderGroupsParams(**filtered_kwargs) if filtered_kwargs else GetOrderGroupsParams()
        else:
            params = GetOrderGroupsParams()
        
        all_data: list[FDXBrokerOrderGroup] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_groups(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_position_lots(self, **kwargs) -> FinaticResponse[list[FDXBrokerPositionLot]]:
        """Get all position_lots across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_position_lots method with internal pagination handling.
        
        @methodId get_all_position_lots_api_v1_brokers_data_positions_lots_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_position_lots(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllPositionLots({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllPositionLots({ brokerId: 'alpaca', connectionId: '00000000-0000-0000-0000-000000000000', accountId: '123456789' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_position_lots(
           *            broker_id='alpaca',
                    connection_id='00000000-0000-0000-0000-000000000000',
                    account_id='123456789'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionLotsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionLotsParams(**filtered_kwargs) if filtered_kwargs else GetPositionLotsParams()
        else:
            params = GetPositionLotsParams()
        
        all_data: list[FDXBrokerPositionLot] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_position_lots(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_position_lot_fills(self, **kwargs) -> FinaticResponse[list[FDXBrokerPositionLotFill]]:
        """Get all position_lot_fills across all pages.
        
        Auto-generated from paginated endpoint.
        
        This method automatically paginates through all pages and returns all items in a single response.
        It uses the underlying get_position_lot_fills method with internal pagination handling.
        
        @methodId get_all_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
        @category brokers
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_position_lot_fills(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
           * @example
           * ```typescript-server
           * // Get all items with optional filters
           * const result = await finatic.getAllPositionLotFills({ connectionId: '00000000-0000-0000-0000-000000000000' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```typescript-client
           * // Get all items with optional filters
           * const result = await finatic.getAllPositionLotFills({ connectionId: '00000000-0000-0000-0000-000000000000' });
           * 
           * // Access the response data
           * if (result.success) {
           *   console.log('Total items:', result.success.data.length);
           *   if (result.warning && result.warning.length > 0) {
           *     console.warn('Warnings:', result.warning);
           *   }
           * } else if (result.error) {
           *   console.error('Error:', result.error.message);
           * }
           * ```
           * @example
           * ```python
           * # Get all items with optional filters
           * result = await finatic.get_all_position_lot_fills(
           *            connection_id='00000000-0000-0000-0000-000000000000'
           * )
           * 
           * # Access the response data
           * if result.success:
           *     print('Total items:', len(result.success['data']))
           *     if result.warning:
           *         print('Warnings:', result.warning)
           * elif result.error:
           *     print('Error:', result.error['message'])
           * ```
        """
        from dataclasses import replace, fields
        from .utils.pagination import PaginatedData
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionLotFillsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionLotFillsParams(**filtered_kwargs) if filtered_kwargs else GetPositionLotFillsParams()
        else:
            params = GetPositionLotFillsParams()
        
        all_data: list[FDXBrokerPositionLotFill] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_position_lot_fills(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            # PaginatedData is array-like (has __len__, __iter__, __getitem__), so we can use it directly
            # For get_all_* methods, we iterate over PaginatedData to extract items and build a flat list
            # get_all_* methods only work with paginated endpoints, so result is always PaginatedData
            if len(result) == 0:
                break
            # Extract items by iterating (PaginatedData.__iter__ works)
            items = list(result)
            
            all_data.extend(items)
            if len(items) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }


    async def get_company(self, **kwargs) -> FinaticResponse[CompanyResponse]:
        """Get Company
        
        Get public company details by ID (no user check, no sensitive data).
        
        Convenience method that delegates to company wrapper.
        
                @methodId get_company_api_v1_company__company_id__get
                @category company
        
        Args:
            company_id (str): Company ID
        
        Returns:
            FinaticResponse[CompanyResponse]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Minimal example with required parameters only
        const result = await finatic.getCompany({ companyId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        @example
        ```typescript-client
        // Minimal example with required parameters only
        const result = await finatic.getCompany({ companyId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetCompanyParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._company.get_company(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._company.get_company(**kwargs)
        else:
            return await self._company.get_company()

    async def get_brokers(self, **kwargs) -> FinaticResponse[list[BrokerInfo]]:
        """Get Brokers
        
        Get all available brokers.
        
        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.
        
        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_brokers_api_v1_brokers__get
                @category brokers
        
        Args:
            **kwargs: No parameters required for this method
        
        Returns:
            FinaticResponse[list[BrokerInfo]]: Standard FinaticResponse format
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_brokers()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getBrokers();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getBrokers();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBrokersParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_brokers(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_brokers(**kwargs)
        else:
            return await self._brokers.get_brokers()

    async def get_broker_connections(self, **kwargs) -> FinaticResponse[list[UserBrokerConnectionWithPermissions]]:
        """List Broker Connections
        
        List all broker connections for the current user with permissions.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for, including the current
        company's permissions (read/write) for each connection.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId list_broker_connections_api_v1_brokers_connections_get
                @category brokers
        
        Args:
            **kwargs: No parameters required for this method
        
        Returns:
            FinaticResponse[list[UserBrokerConnectionWithPermissions]]: Standard FinaticResponse format
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_broker_connections()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getBrokerConnections();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getBrokerConnections();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBrokerConnectionsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_broker_connections(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_broker_connections(**kwargs)
        else:
            return await self._brokers.get_broker_connections()

    async def disconnect_company_from_broker(self, **kwargs) -> FinaticResponse[DisconnectActionResult]:
        """Disconnect Company From Broker
        
        Remove a company's access to a broker connection.
        
        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete
                @category brokers
        
        Args:
            connection_id (str): Connection ID
        
        Returns:
            FinaticResponse[DisconnectActionResult]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Minimal example with required parameters only
        const result = await finatic.disconnectCompanyFromBroker({ connectionId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        @example
        ```typescript-client
        // Minimal example with required parameters only
        const result = await finatic.disconnectCompanyFromBroker({ connectionId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(DisconnectCompanyFromBrokerParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.disconnect_company_from_broker(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.disconnect_company_from_broker(**kwargs)
        else:
            return await self._brokers.disconnect_company_from_broker()

    async def get_orders(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrder]]:
        """Get Orders
        
        Get orders for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_orders_api_v1_brokers_data_orders_get
                @category brokers
        
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
            FinaticResponse[PaginatedData[FDXBrokerOrder]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getOrders();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getOrders();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrdersParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_orders(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_orders(**kwargs)
        else:
            return await self._brokers.get_orders()

    async def get_positions(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPosition]]:
        """Get Positions
        
        Get positions for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_positions_api_v1_brokers_data_positions_get
                @category brokers
        
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
            FinaticResponse[PaginatedData[FDXBrokerPosition]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getPositions();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getPositions();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_positions(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_positions(**kwargs)
        else:
            return await self._brokers.get_positions()

    async def get_balances(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerBalance]]:
        """Get Balances
        
        Get balances for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_balances_api_v1_brokers_data_balances_get
                @category brokers
        
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
            FinaticResponse[PaginatedData[FDXBrokerBalance]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getBalances();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getBalances();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBalancesParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_balances(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_balances(**kwargs)
        else:
            return await self._brokers.get_balances()

    async def get_accounts(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerAccount]]:
        """Get Accounts
        
        Get accounts for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_accounts_api_v1_brokers_data_accounts_get
                @category brokers
        
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
            FinaticResponse[PaginatedData[FDXBrokerAccount]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getAccounts();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getAccounts();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetAccountsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_accounts(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_accounts(**kwargs)
        else:
            return await self._brokers.get_accounts()

    async def get_order_fills(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderFill]]:
        """Get Order Fills
        
        Get order fills for a specific order.
        
        This endpoint returns all execution fills for the specified order.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_order_fills_api_v1_brokers_data_orders__order_id__fills_get
                @category brokers
        
        Args:
            order_id (str): Order ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of fills to return
            offset (int, optional): Number of fills to skip for pagination
            include_metadata (bool, optional): Include fill metadata in response (excluded by default for FDX compliance)
        
        Returns:
            FinaticResponse[PaginatedData[FDXBrokerOrderFill]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Minimal example with required parameters only
        const result = await finatic.getOrderFills({ orderId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        @example
        ```typescript-client
        // Minimal example with required parameters only
        const result = await finatic.getOrderFills({ orderId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderFillsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_fills(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_fills(**kwargs)
        else:
            return await self._brokers.get_order_fills()

    async def get_order_events(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderEvent]]:
        """Get Order Events
        
        Get order events for a specific order.
        
        This endpoint returns all lifecycle events for the specified order.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_order_events_api_v1_brokers_data_orders__order_id__events_get
                @category brokers
        
        Args:
            order_id (str): Order ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of events to return
            offset (int, optional): Number of events to skip for pagination
            include_metadata (bool, optional): Include event metadata in response (excluded by default for FDX compliance)
        
        Returns:
            FinaticResponse[PaginatedData[FDXBrokerOrderEvent]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Minimal example with required parameters only
        const result = await finatic.getOrderEvents({ orderId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        @example
        ```typescript-client
        // Minimal example with required parameters only
        const result = await finatic.getOrderEvents({ orderId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderEventsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_events(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_events(**kwargs)
        else:
            return await self._brokers.get_order_events()

    async def get_order_groups(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerOrderGroup]]:
        """Get Order Groups
        
        Get order groups.
        
        This endpoint returns order groups that contain multiple orders.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_order_groups_api_v1_brokers_data_orders_groups_get
                @category brokers
        
        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of order groups to return
            offset (int, optional): Number of order groups to skip for pagination
            created_after (str, optional): Filter order groups created after this timestamp
            created_before (str, optional): Filter order groups created before this timestamp
            include_metadata (bool, optional): Include group metadata in response (excluded by default for FDX compliance)
        
        Returns:
            FinaticResponse[PaginatedData[FDXBrokerOrderGroup]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getOrderGroups();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getOrderGroups();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderGroupsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_groups(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_groups(**kwargs)
        else:
            return await self._brokers.get_order_groups()

    async def get_position_lots(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPositionLot]]:
        """Get Position Lots
        
        Get position lots (tax lots for positions).
        
        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_position_lots_api_v1_brokers_data_positions_lots_get
                @category brokers
        
        Args:
            broker_id (str, optional): Filter by broker ID
            connection_id (str, optional): Filter by connection ID
            account_id (str, optional): Filter by broker provided account ID
            symbol (str, optional): Filter by symbol
            position_id (str, optional): Filter by position ID
            limit (int, optional): Maximum number of position lots to return
            offset (int, optional): Number of position lots to skip for pagination
        
        Returns:
            FinaticResponse[PaginatedData[FDXBrokerPositionLot]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Example with no parameters
        const result = await finatic.getPositionLots();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        @example
        ```typescript-client
        // Example with no parameters
        const result = await finatic.getPositionLots();
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionLotsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_position_lots(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_position_lots(**kwargs)
        else:
            return await self._brokers.get_position_lots()

    async def get_position_lot_fills(self, **kwargs) -> FinaticResponse[PaginatedData[FDXBrokerPositionLotFill]]:
        """Get Position Lot Fills
        
        Get position lot fills for a specific lot.
        
        This endpoint returns all fills associated with a specific position lot.
        
        Convenience method that delegates to brokers wrapper.
        
                @methodId get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
                @category brokers
        
        Args:
            lot_id (str): Position lot ID
            connection_id (str, optional): Filter by connection ID
            limit (int, optional): Maximum number of fills to return
            offset (int, optional): Number of fills to skip for pagination
        
        Returns:
            FinaticResponse[PaginatedData[FDXBrokerPositionLotFill]]: Standard FinaticResponse format
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
        @example
        ```typescript-server
        // Minimal example with required parameters only
        const result = await finatic.getPositionLotFills({ lotId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        @example
        ```typescript-client
        // Minimal example with required parameters only
        const result = await finatic.getPositionLotFills({ lotId: '00000000-0000-0000-0000-000000000000' });
        
        // Access the response data
        if (result.success) {
          console.log('Data:', result.success.data);
        } else if (result.error) {
          console.error('Error:', result.error.message);
        }
        ```
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionLotFillsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_position_lot_fills(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_position_lot_fills(**kwargs)
        else:
            return await self._brokers.get_position_lot_fills()
