# MixrPay Agent SDK for Python

Enable AI agents to make autonomous payments. Supports both session-based payments (for MixrPay merchants) and x402 protocol (for external APIs).

[![PyPI version](https://img.shields.io/pypi/v/mixrpay)](https://pypi.org/project/mixrpay/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

```python
from mixrpay import AgentWallet

wallet = AgentWallet(session_key="sk_live_...")

# For MixrPay merchants (recommended):
response = await wallet.call_merchant_api(
    url="https://api.merchant.com/generate",
    merchant_public_key="pk_live_abc123",
    price_usd=0.05,
    json={"prompt": "Hello world"}
)

# For external x402 APIs:
response = wallet.fetch("https://external-api.com/query")
```

## 📦 Installation

```bash
pip install mixrpay
```

With LangChain integration:
```bash
pip install mixrpay[langchain]
```

With CrewAI integration:
```bash
pip install mixrpay[crewai]
```

## Two Payment Methods

The Agent SDK supports **two payment patterns** depending on what API you're calling:

### 1. Session-Based Payments (For MixrPay Merchants) ⭐ Recommended

Use `call_merchant_api()` when the API uses MixrPay:

```python
response = await wallet.call_merchant_api(
    url="https://api.merchant.com/generate",
    merchant_public_key="pk_live_abc123",  # Merchant's MixrPay public key
    price_usd=0.05,
    method="POST",
    json={"prompt": "Hello world"},
)
```

**How it works:**
1. SDK creates/reuses a session authorization with the merchant
2. SDK charges against the session
3. Request is sent with `X-Mixr-Session` header
4. No 402 round-trip needed—faster and cheaper

**When to use:** APIs built with MixrPay, or any API that accepts `X-Mixr-Session` headers.

### 2. x402 Protocol (For External APIs)

Use `fetch()` when calling APIs that implement x402 but aren't MixrPay merchants:

```python
response = wallet.fetch(
    "https://external-api.com/query",
    method="POST",
    json={"prompt": "Hello"}
)
```

**How it works:**
1. SDK makes initial request
2. API returns `402 Payment Required`
3. SDK signs payment authorization
4. SDK retries with `X-PAYMENT` header

**When to use:** External APIs that use standard x402 protocol.

## 🔑 Getting Session Keys

Session keys are created by wallet owners and grant spending permissions to agents:

1. **From a wallet owner**: They create a session key at `/wallet/sessions`
2. **Programmatically**: Via the MixrPay API

Session keys look like: `sk_live_abc123...` (mainnet) or `sk_test_abc123...` (testnet)

### Session Key Limits

Each session key has configurable spending limits:
- **Per-transaction**: Maximum amount per single request
- **Daily**: Maximum total per 24 hours
- **Total**: Maximum lifetime spend
- **Expiration**: When the key becomes invalid

## 📖 Session Management

### Automatic (Recommended)

`call_merchant_api()` handles sessions automatically:

```python
# Sessions are created and reused automatically
response = await wallet.call_merchant_api(
    url="https://api.merchant.com/generate",
    merchant_public_key="pk_live_abc123",
    price_usd=0.05,
    json={"prompt": "Hello"}
)
```

### Manual Control

For fine-grained control over sessions:

```python
# Get or create a session
session = await wallet.get_or_create_session(
    merchant_public_key="pk_live_abc123",
    spending_limit_usd=25,    # Max total spending
    duration_days=7,          # Session validity
)

print(f"Session ID: {session.id}")
print(f"Remaining: ${session.remaining_usd}")
print(f"Expires: {session.expires_at}")

# Charge manually
charge = await wallet.charge_session(
    session_id=session.id,
    amount_usd=0.05,
    feature="generate",
    idempotency_key=f"charge-{time.time()}"
)

# Then make your API call with the session
import httpx
async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://api.merchant.com/generate",
        headers={
            "X-Mixr-Session": session.id,
            "X-Mixr-Charged": "true",
        },
        json={"prompt": "Hello"}
    )
```

### List and Revoke Sessions

```python
# List all active sessions
sessions = await wallet.list_sessions()
for session in sessions:
    print(f"{session.merchant_name}: ${session.remaining_usd} remaining")

# Revoke a session (e.g., when done with a merchant)
await wallet.revoke_session(session.id)

# Get session statistics
stats = await wallet.get_session_stats()
print(f"Active sessions: {stats['active_count']}")
print(f"Total authorized: ${stats['total_authorized_usd']}")
```

## 💡 Usage Examples

### With Payment Tracking

```python
from mixrpay import AgentWallet, PaymentEvent

def on_payment(payment: PaymentEvent):
    print(f"💸 Paid ${payment.amount_usd:.4f} to {payment.recipient}")

wallet = AgentWallet(
    session_key="sk_live_...",
    on_payment=on_payment,
)

# Make requests
response = await wallet.call_merchant_api(...)

# Check spending
stats = wallet.get_spending_stats()
print(f"Total spent: ${stats.total_spent_usd:.2f}")
print(f"Transactions: {stats.tx_count}")
```

### Error Handling

```python
from mixrpay import (
    AgentWallet,
    InsufficientBalanceError,
    SpendingLimitExceededError,
    SessionKeyExpiredError,
    SessionExpiredError,
    SessionLimitExceededError,
)

wallet = AgentWallet(session_key="sk_live_...")

try:
    response = await wallet.call_merchant_api(...)
except InsufficientBalanceError as e:
    print(f"❌ Not enough funds: need ${e.required:.2f}, have ${e.available:.2f}")
    print(f"   Top up at: {e.top_up_url}")
except SessionExpiredError:
    print("❌ Session expired, creating new one...")
    # SDK will auto-create on next call_merchant_api()
except SessionLimitExceededError as e:
    print(f"❌ Session limit exceeded: {e.limit_type}")
    print(f"   Limit: ${e.limit}, Requested: ${e.requested}")
except SpendingLimitExceededError as e:
    print(f"❌ Session key limit exceeded: {e.limit_type}")
except SessionKeyExpiredError as e:
    print(f"❌ Session key expired at {e.expired_at}")
```

### With Client-Side Safety Limit

```python
wallet = AgentWallet(
    session_key="sk_live_...",
    max_payment_usd=1.0,  # Never pay more than $1 per request
)

# If an API tries to charge more than $1, the SDK will raise
# SpendingLimitExceededError with limit_type='client_max'
```

### Context Manager (Recommended)

```python
# Automatically closes the HTTP client when done
async with AsyncAgentWallet(session_key="sk_live_...") as wallet:
    response = await wallet.call_merchant_api(...)
    print(response.json())
```

### Debug Mode

```python
# Enable logging during initialization
wallet = AgentWallet(
    session_key="sk_live_...",
    log_level="debug",  # 'debug' | 'info' | 'warning' | 'error' | 'none'
)

# Or toggle at runtime
wallet.set_debug(True)
```

## 🤖 AI Framework Integrations

### LangChain

```python
from langchain.tools import BaseTool
from mixrpay import AgentWallet, SessionLimitExceededError
import os

class PaidSearchTool(BaseTool):
    name = "paid_search"
    description = "Search using a premium paid API ($0.05/query)"
    
    def __init__(self, session_key: str):
        super().__init__()
        self.wallet = AgentWallet(
            session_key=session_key,
            max_payment_usd=0.50,
        )
    
    async def _arun(self, query: str) -> str:
        try:
            response = await self.wallet.call_merchant_api(
                url="https://api.search.com/query",
                merchant_public_key="pk_live_...",
                price_usd=0.05,
                json={"query": query}
            )
            return response.json()["results"]
        except SessionLimitExceededError as e:
            return f"Error: {e.limit_type} limit exceeded"
        except Exception as e:
            return f"Error: {e}"

# Use with LangChain agent
tool = PaidSearchTool(session_key=os.environ["MIXRPAY_SESSION_KEY"])
```

### CrewAI

```python
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from mixrpay import AgentWallet, InsufficientBalanceError
import os

class PaidResearchTool(BaseTool):
    name: str = "paid_research"
    description: str = "Access premium research databases ($0.10/query)"
    
    def __init__(self, session_key: str):
        super().__init__()
        self.wallet = AgentWallet(
            session_key=session_key,
            max_payment_usd=1.00,
        )
    
    async def _run(self, query: str) -> str:
        try:
            response = await self.wallet.call_merchant_api(
                url="https://api.research.com/query",
                merchant_public_key="pk_live_...",
                price_usd=0.10,
                json={"query": query}
            )
            return response.json()["findings"]
        except InsufficientBalanceError:
            return "Error: Insufficient balance"
```

### OpenAI Functions

```python
import json
from openai import OpenAI
from mixrpay import AgentWallet

wallet = AgentWallet(session_key="sk_live_...")
client = OpenAI()

async def handle_tool_call(function_name: str, args: dict) -> str:
    if function_name == "paid_search":
        response = await wallet.call_merchant_api(
            url="https://api.search.com/query",
            merchant_public_key="pk_live_...",
            price_usd=0.05,
            json={"query": args["query"]}
        )
        return json.dumps(response.json())
```

## 📚 API Reference

### AgentWallet

```python
AgentWallet(
    # Required
    session_key: str,              # Session key (sk_live_... or sk_test_...)
    
    # Optional
    wallet_address: str = None,    # Smart wallet address (auto-detected)
    max_payment_usd: float = None, # Client-side payment limit
    on_payment: Callable = None,   # Payment callback
    facilitator_url: str = "...",  # x402 facilitator URL
    base_url: str = "...",         # MixrPay API base URL
    timeout: float = 30.0,         # Request timeout in seconds
    log_level: str = "warning",    # 'debug' | 'info' | 'warning' | 'error' | 'none'
)
```

### Methods

| Method | Description |
|--------|-------------|
| `call_merchant_api(...)` | Make request to MixrPay merchant (session-based) |
| `fetch(url, ...)` | Make request to x402 API |
| `get(url, ...)` | GET request shorthand |
| `post(url, ...)` | POST request shorthand |
| `get_or_create_session(...)` | Get or create session with merchant |
| `charge_session(...)` | Charge against a session |
| `list_sessions()` | List all active sessions |
| `revoke_session(id)` | Revoke a session |
| `get_session_stats()` | Get session statistics |
| `get_balance()` | Get USDC balance in USD |
| `get_spending_stats()` | Get spending statistics |
| `get_session_key_info()` | Get session key details and limits |
| `get_payment_history()` | Get list of payments made |
| `get_total_spent()` | Get total amount spent |
| `run_diagnostics()` | Run health checks |
| `set_debug(enable)` | Toggle debug logging |
| `close()` | Close HTTP client |

### Data Classes

```python
@dataclass
class Session:
    id: str
    merchant_public_key: str
    merchant_name: Optional[str]
    spending_limit_usd: float
    spent_usd: float
    remaining_usd: float
    status: str  # 'active' | 'expired' | 'revoked'
    expires_at: datetime
    created_at: datetime

@dataclass
class ChargeResult:
    success: bool
    charge_id: str
    amount_usd: float
    tx_hash: Optional[str]
    remaining_usd: float

@dataclass
class PaymentEvent:
    amount_usd: float
    recipient: str
    tx_hash: Optional[str]
    timestamp: float
    description: Optional[str]
    url: Optional[str]
```

### Exceptions

| Exception | When Raised |
|-----------|-------------|
| `InsufficientBalanceError` | Wallet doesn't have enough USDC |
| `SessionKeyExpiredError` | Session key has expired |
| `SpendingLimitExceededError` | Would exceed session key limits |
| `SessionExpiredError` | Session authorization has expired |
| `SessionLimitExceededError` | Would exceed session spending limit |
| `SessionNotFoundError` | Session ID is invalid |
| `SessionRevokedError` | Session was revoked |
| `PaymentFailedError` | Payment transaction failed |
| `InvalidSessionKeyError` | Invalid session key format |
| `X402ProtocolError` | x402 protocol handling error |

All exceptions inherit from `MixrPayError`:

```python
from mixrpay import MixrPayError

try:
    await wallet.call_merchant_api(...)
except MixrPayError as e:
    print(f"MixrPay error [{e.code}]: {e.message}")
```

## 🌐 Networks

| Network | Chain ID | Session Key Prefix | USDC Address |
|---------|----------|-------------------|--------------|
| Base Mainnet | 8453 | `sk_live_` | Production USDC |
| Base Sepolia | 84532 | `sk_test_` | Test USDC |

### Testing on Testnet

```python
import os

# Test environment setup
wallet = AgentWallet(
    session_key="sk_test_...",  # Use test key
    base_url="http://localhost:3000",  # Local dev server
)

# The SDK automatically detects testnet from sk_test_ prefix
print(f"Testnet: {wallet.is_testnet}")  # True
```

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MIXRPAY_SESSION_KEY` | Yes | Your session key (`sk_live_...` or `sk_test_...`) |
| `MIXRPAY_BASE_URL` | No | MixrPay server URL (default: `https://mixrpay.com`) |

## 🔒 Security Best Practices

1. **Store session keys securely** - Use environment variables, never commit to source
2. **Set appropriate limits** - Use `max_payment_usd` as a safety net
3. **Monitor spending** - Use `on_payment` callback and `get_spending_stats()`
4. **Use testnet first** - Test with `sk_test_` keys before production
5. **Use context managers** - Ensures proper resource cleanup
6. **Configure base URL** - Always set `base_url` explicitly in production

## 📋 Changelog

### v0.2.0 (Current)
- Added session-based payments (`call_merchant_api()`)
- Added session management (`get_or_create_session()`, `list_sessions()`, `revoke_session()`)
- Added session-related error types
- Improved documentation

### v0.1.0
- Initial release
- x402 payment handling via `fetch()`
- Session key validation and spending limits
- Payment callbacks and statistics
- Async support with `AsyncAgentWallet`

## 📝 License

MIT
