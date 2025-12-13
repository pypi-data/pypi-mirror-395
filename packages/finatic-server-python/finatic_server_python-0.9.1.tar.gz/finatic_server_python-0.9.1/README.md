# Finatic Python Server SDK

Python SDK for the Finatic Server API. Connect your Python applications to multiple brokerages through a unified, standardized interface.

**Finatic is a brokerage first aggregator. We simplify, standardize and enhance broker data.**

## Installation

```bash
pip install finatic-server-python
```

Or using uv:

```bash
uv pip install finatic-server-python
```

## Quick Start (5 Minutes)

### 1. Initialize the SDK

```python
from finatic_server_python import FinaticServer

# Initialize with your API key
finatic = await FinaticServer.init(
    api_key='your-api-key',
    user_id=None,  # Optional user ID
    sdk_config={
        'base_url': 'https://api.finatic.dev',  # Optional, defaults to production
        'log_level': 'debug',  # Optional: 'debug' | 'info' | 'warn' | 'error'
        'structured_logging': True,  # Optional: Enable structured JSON logging
    }
)
```

**Note:** The `init()` method automatically starts a session, so you're ready to use the SDK immediately.

### 2. Get Portal URL for Authentication

The portal allows users to connect their broker accounts. Get the URL and redirect users to it:

```python
# Get portal URL
portal_url = await finatic.get_portal_url(
    theme='dark',  # Theme: 'light' | 'dark' | theme dict
    brokers=['alpaca', 'tradier'],  # Optional: Filter specific brokers
    email='user@example.com',  # Optional: Pre-fill email
    mode='dark'  # Mode: 'light' | 'dark'
)

print(f'Portal URL: {portal_url}')
# Redirect user to this URL for authentication
```

### 3. Check Authentication Status

```python
# Check if user is authenticated
is_authenticated = finatic.is_authed()

# Get current user ID
user_id = finatic.get_user_id()

# Get session user details
session_user = await finatic.get_session_user()
```

### 4. Fetch Data

Once users have authenticated via the portal, you can fetch broker data:

```python
# Get all orders (automatically paginates through all pages)
all_orders = await finatic.get_all_orders()

# Get orders with filters (single page)
orders = await finatic.get_orders(
    broker_id='alpaca',
    account_id='123456789',
    order_status='filled',
    limit=100,
    offset=0
)

# Get all positions
all_positions = await finatic.get_all_positions()

# Get positions with filters
positions = await finatic.get_positions(
    broker_id='alpaca',
    symbol='AAPL',
    limit=50
)

# Get all accounts
all_accounts = await finatic.get_all_accounts()

# Get balances
balances = await finatic.get_balances(
    broker_id='alpaca',
    account_id='123456789'
)
```

## Complete Example

```python
import asyncio
import os
from finatic_server_python import FinaticServer

async def main():
    # 1. Initialize SDK
    finatic = await FinaticServer.init(
        api_key=os.getenv('FINATIC_API_KEY'),
        user_id=None,  # Optional user ID
        sdk_config={
            'base_url': os.getenv('FINATIC_API_URL', 'https://api.finatic.dev'),
            'log_level': 'info',
        }
    )

    # 2. Get portal URL for user authentication
    portal_url = await finatic.get_portal_url('dark')
    print('Please visit this URL to authenticate:')
    print(portal_url)

    # Wait for user to authenticate (in a real app, you'd handle this via webhook or polling)
    # For demo purposes, we'll assume authentication is complete

    # 3. Fetch data
    orders = await finatic.get_all_orders()
    positions = await finatic.get_all_positions()
    accounts = await finatic.get_all_accounts()

    print('Orders:', orders.success.data if orders.success else None)
    print('Positions:', positions.success.data if positions.success else None)
    print('Accounts:', accounts.success.data if accounts.success else None)

if __name__ == '__main__':
    asyncio.run(main())
```

## Generate One-Time Tokens for Client SDK

If you need to generate tokens for the Client SDK:

```python
# Get a one-time token (useful for passing to client-side applications)
token = await finatic.get_token()

# Or with a custom API key
token = await finatic.get_token(api_key='custom-api-key')
```

## Available Data Methods

### Orders

- `get_orders(**params)` - Get single page of orders
- `get_all_orders(**params)` - Get all orders (auto-paginated)
- `get_order_fills(order_id, **params)` - Get fills for a specific order
- `get_all_order_fills(order_id, **params)` - Get all fills (auto-paginated)
- `get_order_events(order_id, **params)` - Get events for a specific order
- `get_all_order_events(order_id, **params)` - Get all events (auto-paginated)
- `get_order_groups(**params)` - Get order groups
- `get_all_order_groups(**params)` - Get all order groups (auto-paginated)

### Positions

- `get_positions(**params)` - Get single page of positions
- `get_all_positions(**params)` - Get all positions (auto-paginated)
- `get_position_lots(**params)` - Get position lots
- `get_all_position_lots(**params)` - Get all position lots (auto-paginated)
- `get_position_lot_fills(lot_id, **params)` - Get fills for a specific lot
- `get_all_position_lot_fills(lot_id, **params)` - Get all fills (auto-paginated)

### Accounts & Balances

- `get_accounts(**params)` - Get single page of accounts
- `get_all_accounts(**params)` - Get all accounts (auto-paginated)
- `get_balances(**params)` - Get balances
- `get_all_balances(**params)` - Get all balances (auto-paginated)

### Broker Management

- `get_brokers()` - Get available brokers
- `get_broker_connections()` - Get connected broker accounts
- `disconnect_company_from_broker(connection_id)` - Disconnect a broker

### Company

- `get_company(company_id)` - Get company information

## Method Parameters

Most data methods accept optional keyword arguments:

```python
{
    'broker_id': 'alpaca',        # Filter by broker (e.g., 'alpaca', 'tradier')
    'connection_id': 'uuid',      # Filter by connection ID
    'account_id': '123456789',    # Filter by account ID
    'symbol': 'AAPL',             # Filter by symbol
    'order_status': 'filled',     # Filter by order status
    'side': 'buy',                # Filter by side ('buy' | 'sell')
    'asset_type': 'equity',       # Filter by asset type
    'limit': 100,                 # Page size (default: varies by endpoint)
    'offset': 0,                  # Pagination offset (default: 0)
    'include_metadata': True,     # Include metadata in response
    # ... other filters specific to each method
}
```

## Response Format

All data methods return a `FinaticResponse` object:

```python
{
    'success': {
        'data': [...],  # List of data items
        # ... other metadata
    },
    'error': {
        'message': 'Error message',
        'code': 'ERROR_CODE'
    },
    'warning': [...]
}
```

Access the data:

```python
result = await finatic.get_orders()
if result.success:
    orders = result.success.data
    # Use orders...
else:
    print(f'Error: {result.error.message}')
```

## Session Management

```python
# Start a new session (usually done automatically in init())
session_result = await finatic.start_session()

# Get session user
session_user = await finatic.get_session_user()

# Get session ID
session_id = finatic.get_session_id()

# Get company ID
company_id = finatic.get_company_id()
```

## Configuration Options

```python
finatic = await FinaticServer.init(
    api_key='your-api-key',
    user_id=None,
    sdk_config={
        'base_url': 'https://api.finatic.dev',  # API base URL
        'log_level': 'info',  # 'debug' | 'info' | 'warn' | 'error'
        'structured_logging': False,  # Enable structured JSON logging
        # ... other options
    }
)
```

## Development

```bash
# Install dependencies
uv pip install -e .

# Build
python -m build

# Run tests
pytest

# Lint
ruff check .

# Format
ruff format .
```

## Documentation

Full API documentation is available at [docs.finatic.com/server/python](https://docs.finatic.com/server/python).

## License

MIT

## Copyright

© Copyright 2025 Finatic. All Rights Reserved.

---

**Finatic** - Fast. Secure. Standardized.
