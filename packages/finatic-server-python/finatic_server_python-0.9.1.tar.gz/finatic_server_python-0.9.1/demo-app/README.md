# Finatic Python Server SDK Demo App

This demo application showcases the Finatic Python Server SDK with both CLI and API server capabilities.

## Features

- **CLI Demo**: Interactive command-line demo (existing)
- **API Server**: FastAPI server that provides endpoints matching the Client SDK interface

## Setup

1. **Install dependencies with uv** (recommended):

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -e .
   ```

2. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your FINATIC_API_KEY
   ```

## Running the API Server

The API server runs on port **8002** and provides endpoints that match the Client SDK interface.

### Development Mode

**Option 1: Using the convenience script (recommended)**:

```bash
uv run python run_api.py
```

**Option 2: Direct uvicorn**:

```bash
uv run uvicorn api_server:app --host 0.0.0.0 --port 8002 --reload
```

**Option 3: Direct Python**:

```bash
uv run python api_server.py
```

### Production Mode

```bash
uv run uvicorn api_server:app --host 0.0.0.0 --port 8002
```

The server will be available at `http://localhost:8002` and includes:

- CORS support for `http://localhost:3000` (Client SDK demo app)
- Health check endpoint at `/api/health`
- All Client SDK method endpoints under `/api/`

## API Endpoints

### Session Management

- `POST /api/session/start` - Start new session
- `POST /api/session/authenticate` - Authenticate with user ID
- `GET /api/session/user` - Get session user info
- `GET /api/session/user-id` - Get current user ID
- `GET /api/session/is-authed` - Check authentication status

### Broker Data

- `GET /api/broker/list` - Get available brokers
- `GET /api/broker/connections` - Get broker connections
- `GET /api/broker/accounts` - Get accounts (paginated)
- `GET /api/broker/accounts/all` - Get all accounts
- `POST /api/broker/disconnect` - Disconnect company

### Trading Data

- `GET /api/trading/orders` - Get orders (paginated)
- `GET /api/trading/orders/all` - Get all orders
- `GET /api/trading/positions` - Get positions (paginated)
- `GET /api/trading/positions/all` - Get all positions
- `GET /api/trading/balances` - Get balances (paginated)
- `GET /api/trading/balances/all` - Get all balances

### Trading Context

- `POST /api/trading/context/broker` - Set trading broker
- `POST /api/trading/context/account` - Set trading account
- `GET /api/trading/context` - Get trading context

### Order Management

- `POST /api/trading/order` - Place new order
- `POST /api/trading/order/cancel` - Cancel order
- `POST /api/trading/order/modify` - Modify order

## Integration with Client SDK Demo

This API server is designed to work with the Client SDK demo app's SDK switcher. When you select "Python Server SDK" in the demo app settings, it will connect to this server on port 3001.

## CLI Demo

The original CLI demo is still available:

```bash
uv run python test_trading.py
```
