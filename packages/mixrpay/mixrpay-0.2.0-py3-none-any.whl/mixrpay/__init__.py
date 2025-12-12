"""
MixrPay Agent SDK - Enable AI agents to make x402 payments with session keys.

Quick Start:
    >>> from mixrpay import AgentWallet
    >>> 
    >>> # 1. Initialize with your session key
    >>> wallet = AgentWallet(
    ...     session_key="sk_live_...",  # Get from wallet owner
    ... )
    >>> 
    >>> # 2. Make requests - payments are automatic!
    >>> response = wallet.fetch(
    ...     "https://api.example.com/ai/query",
    ...     method="POST",
    ...     json={"prompt": "Hello world"}
    ... )
    >>> 
    >>> # 3. Use the response
    >>> print(response.json())

How It Works:
    1. Your agent makes a request to a paid API
    2. The server returns ``402 Payment Required`` with pricing info
    3. The SDK automatically signs a USDC payment authorization
    4. The request is retried with the payment, and you get the response

Features:
    - 🔐 **Secure** - Session keys have built-in spending limits
    - 🤖 **Agent-Ready** - Works with LangChain, CrewAI, and any framework
    - ⚡ **Automatic** - No manual payment handling needed
    - 📊 **Tracking** - Built-in spending statistics and payment history
    - 🔄 **Async Support** - Full async/await support for high-performance apps

Error Handling:
    >>> from mixrpay import (
    ...     AgentWallet,
    ...     InsufficientBalanceError,
    ...     SpendingLimitExceededError,
    ...     SessionKeyExpiredError,
    ... )
    >>> 
    >>> try:
    ...     response = wallet.fetch("...")
    ... except InsufficientBalanceError as e:
    ...     print(f"Need ${e.required}, have ${e.available}")
    ...     print(f"Top up at: {e.top_up_url}")
    ... except SpendingLimitExceededError as e:
    ...     print(f"Exceeded {e.limit_type} limit of ${e.limit}")
    ... except SessionKeyExpiredError as e:
    ...     print(f"Key expired at {e.expired_at}")

Debugging:
    Enable debug logging to see what's happening:
    
    >>> wallet = AgentWallet(
    ...     session_key="...",
    ...     log_level="debug",  # 'debug' | 'info' | 'warning' | 'error' | 'none'
    ... )
    >>> 
    >>> # Or toggle at runtime:
    >>> wallet.set_debug(True)

Networks:
    - **Base Mainnet** (chain ID: 8453) - Use ``sk_live_...`` keys
    - **Base Sepolia** (chain ID: 84532) - Use ``sk_test_...`` keys

Getting Session Keys:
    Session keys are granted by wallet owners. They can be created at:
    - Your MixrPay server's /wallet/sessions page
    - Via the MixrPay widget
    - Programmatically through the MixrPay API
"""

# Version
__version__ = "0.2.0"

# Main classes
from .agent_wallet import (
    AgentWallet,
    AsyncAgentWallet,
    PaymentEvent,
    SpendingStats,
    SessionKeyInfo,
    SessionKeyLimits,
    SessionKeyUsage,
    DiagnosticsResult,
    Network,
    # Session Authorization types
    SessionAuthorization,
    ChargeResult,
    CreateSessionOptions,
    CallMerchantApiOptions,
    ChargeSessionOptions,
    # Constants
    SDK_VERSION,
    DEFAULT_BASE_URL,
    DEFAULT_FACILITATOR_URL,
    DEFAULT_TIMEOUT,
)

# Exceptions
from .exceptions import (
    MixrPayError,
    InsufficientBalanceError,
    SessionKeyExpiredError,
    SpendingLimitExceededError,
    PaymentFailedError,
    InvalidSessionKeyError,
    X402ProtocolError,
    # Utilities
    is_mixrpay_error,
    get_error_message,
)

# x402 types (for advanced usage)
from .x402 import PaymentRequirements

# All public exports
__all__ = [
    # Version
    "__version__",
    # Main classes
    "AgentWallet",
    "AsyncAgentWallet",
    # Data types
    "PaymentEvent",
    "SpendingStats",
    "SessionKeyInfo",
    "SessionKeyLimits",
    "SessionKeyUsage",
    "DiagnosticsResult",
    "PaymentRequirements",
    "Network",
    # Session Authorization types
    "SessionAuthorization",
    "ChargeResult",
    "CreateSessionOptions",
    "CallMerchantApiOptions",
    "ChargeSessionOptions",
    # Constants
    "SDK_VERSION",
    "DEFAULT_BASE_URL",
    "DEFAULT_FACILITATOR_URL",
    "DEFAULT_TIMEOUT",
    # Exceptions
    "MixrPayError",
    "InsufficientBalanceError",
    "SessionKeyExpiredError",
    "SpendingLimitExceededError",
    "PaymentFailedError",
    "InvalidSessionKeyError",
    "X402ProtocolError",
    # Utilities
    "is_mixrpay_error",
    "get_error_message",
]
