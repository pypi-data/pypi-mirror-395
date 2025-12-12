"""
MixrPay SDK - Custom Exceptions

These exceptions provide clear, actionable messages for common x402 payment failures.
Each exception includes:
- A clear description of what went wrong
- Relevant data for programmatic handling
- Suggestions for how to fix the issue

Example:
    >>> from mixrpay import AgentWallet, InsufficientBalanceError
    >>> 
    >>> try:
    ...     wallet.fetch("https://api.example.com/query")
    ... except InsufficientBalanceError as e:
    ...     print(f"Need ${e.required}, have ${e.available}")
    ...     print(f"Top up at: {e.top_up_url}")
"""


class MixrPayError(Exception):
    """
    Base exception for all MixrPay SDK errors.
    
    All SDK exceptions extend this class, making it easy to catch all
    MixrPay-related errors in a single except block.
    
    Attributes:
        code: Error code for programmatic handling
        message: Human-readable error message
    
    Example:
        >>> try:
        ...     wallet.fetch(...)
        ... except MixrPayError as e:
        ...     print(f"MixrPay error [{e.code}]: {e.message}")
    """
    
    code: str = "MIXRPAY_ERROR"
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        if code:
            self.code = code
        super().__init__(message)


class InsufficientBalanceError(MixrPayError):
    """
    Wallet doesn't have enough USDC for the payment.
    
    This error indicates the smart wallet needs to be topped up with more USDC.
    
    Resolution:
        1. Direct the user to top up their wallet
        2. Use a smaller transaction (if possible)
        3. Wait for pending deposits to confirm
    
    Attributes:
        required: Amount required for the payment in USD
        available: Current available balance in USD
        shortage: How much more is needed (required - available)
        top_up_url: URL where the user can top up their wallet
    
    Example:
        >>> except InsufficientBalanceError as e:
        ...     print(f"Need ${e.required:.2f}, have ${e.available:.2f}")
        ...     print(f"Short by ${e.shortage:.2f}")
        ...     print(f"Top up at: {e.top_up_url}")
    """
    
    code = "INSUFFICIENT_BALANCE"
    
    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        self.shortage = required - available
        self.top_up_url = "/wallet"  # Relative to your MixrPay server
        
        super().__init__(
            f"Insufficient balance: need ${required:.2f}, have ${available:.2f} "
            f"(short ${self.shortage:.2f}). Top up your wallet to continue."
        )


class SessionKeyExpiredError(MixrPayError):
    """
    Session key has expired.
    
    Session keys have an expiration date set by the wallet owner. Once expired,
    the key can no longer authorize payments.
    
    Resolution:
        1. Request a new session key from the wallet owner
        2. Create a new session key (if you have wallet access)
    
    Attributes:
        expired_at: When the session key expired
    
    Example:
        >>> except SessionKeyExpiredError as e:
        ...     print(f"Session key expired at {e.expired_at}")
        ...     # Request new key from wallet owner
    """
    
    code = "SESSION_KEY_EXPIRED"
    
    def __init__(self, expired_at: str):
        self.expired_at = expired_at
        super().__init__(
            f"Session key expired at {expired_at}. Request a new session key "
            f"from the wallet owner or create one at your MixrPay server /wallet/sessions"
        )


class SpendingLimitExceededError(MixrPayError):
    """
    Payment would exceed session key spending limits.
    
    Session keys can have three types of limits:
    - per_tx: Maximum per single transaction
    - daily: Maximum total per 24-hour period
    - total: Maximum lifetime spend
    - client_max: Client-side limit set in AgentWallet config
    
    Resolution:
        - per_tx: Use a smaller transaction or request higher limit
        - daily: Wait until tomorrow or request higher limit
        - total: Request a new session key with higher limit
        - client_max: Increase max_payment_usd in config
    
    Attributes:
        limit_type: Type of limit that was exceeded
        limit: The limit amount in USD
        attempted: The amount that was attempted in USD
        excess: How much over the limit (attempted - limit)
    
    Example:
        >>> except SpendingLimitExceededError as e:
        ...     if e.limit_type == "daily":
        ...         print("Daily limit reached. Try again tomorrow.")
        ...     elif e.limit_type == "per_tx":
        ...         print(f"Max per transaction is ${e.limit}")
    """
    
    code = "SPENDING_LIMIT_EXCEEDED"
    
    def __init__(self, limit_type: str, limit: float, attempted: float):
        self.limit_type = limit_type  # "per_tx", "daily", "total", "client_max"
        self.limit = limit
        self.attempted = attempted
        self.excess = attempted - limit
        
        limit_names = {
            "per_tx": "Per-transaction",
            "daily": "Daily",
            "total": "Total",
            "client_max": "Client-side",
        }
        limit_name = limit_names.get(limit_type, limit_type)
        
        suggestions = {
            "daily": "Wait until tomorrow or request a higher limit.",
            "client_max": "Increase max_payment_usd in your AgentWallet configuration.",
        }
        suggestion = suggestions.get(limit_type, "Request a new session key with a higher limit.")
        
        super().__init__(
            f"{limit_name} spending limit exceeded: limit is ${limit:.2f}, "
            f"attempted ${attempted:.2f}. {suggestion}"
        )


class PaymentFailedError(MixrPayError):
    """
    Payment transaction failed.
    
    This is a general error for payment failures that don't fit other categories.
    Check the `reason` attribute for more details.
    
    Common Causes:
        - Network issues
        - Invalid payment parameters
        - Server-side errors
        - Blockchain congestion
    
    Attributes:
        reason: Detailed reason for the failure
        tx_hash: Transaction hash if the tx was submitted (for debugging)
    
    Example:
        >>> except PaymentFailedError as e:
        ...     print(f"Payment failed: {e.reason}")
        ...     if e.tx_hash:
        ...         print(f"Check transaction: https://basescan.org/tx/{e.tx_hash}")
    """
    
    code = "PAYMENT_FAILED"
    
    def __init__(self, reason: str, tx_hash: str | None = None):
        self.reason = reason
        self.tx_hash = tx_hash
        
        msg = f"Payment failed: {reason}"
        if tx_hash:
            msg += f" (tx: {tx_hash} - check on basescan.org)"
        super().__init__(msg)


class InvalidSessionKeyError(MixrPayError):
    """
    Session key format is invalid or cannot be decoded.
    
    Session keys must:
    - Start with ``sk_live_`` (mainnet) or ``sk_test_`` (testnet)
    - Be followed by exactly 64 hexadecimal characters
    - Total length: 72 characters
    
    Common Issues:
        - Incomplete copy/paste
        - Extra whitespace
        - Using API key instead of session key
        - Using public key instead of private key
    
    Attributes:
        reason: Detailed reason why the key is invalid
    
    Example:
        >>> except InvalidSessionKeyError as e:
        ...     print(f"Invalid key: {e.reason}")
        ...     print("Get a valid session key from your MixrPay server /wallet/sessions")
    """
    
    code = "INVALID_SESSION_KEY"
    
    def __init__(self, reason: str = "Invalid session key format"):
        self.reason = reason
        super().__init__(
            f"{reason}. Session keys should be in format: sk_live_<64 hex chars> "
            f"or sk_test_<64 hex chars>. Get one from your MixrPay server /wallet/sessions"
        )


class X402ProtocolError(MixrPayError):
    """
    Error in x402 protocol handling.
    
    This indicates a problem with the payment protocol, usually due to:
    - Malformed 402 response from server
    - Missing required payment fields
    - Invalid payment parameters
    - Protocol version mismatch
    
    Resolution:
        This is usually a server-side issue. Contact the API provider if
        the error persists.
    
    Attributes:
        reason: Detailed reason for the protocol error
    
    Example:
        >>> except X402ProtocolError as e:
        ...     print(f"Protocol error: {e.reason}")
        ...     # Contact API provider or check server configuration
    """
    
    code = "X402_PROTOCOL_ERROR"
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(
            f"x402 protocol error: {reason}. "
            f"This may indicate a server configuration issue. "
            f"If the problem persists, contact the API provider."
        )


# =============================================================================
# Utility Functions
# =============================================================================

def is_mixrpay_error(error: Exception) -> bool:
    """
    Check if an exception is a MixrPay SDK error.
    
    Args:
        error: The exception to check
    
    Returns:
        True if the error is a MixrPayError or subclass
    
    Example:
        >>> try:
        ...     wallet.fetch(...)
        ... except Exception as e:
        ...     if is_mixrpay_error(e):
        ...         print(f"MixrPay error: {e.code}")
        ...     else:
        ...         raise
    """
    return isinstance(error, MixrPayError)


def get_error_message(error: Exception) -> str:
    """
    Get a user-friendly error message from any exception.
    
    Args:
        error: The exception to get a message from
    
    Returns:
        A user-friendly error message
    
    Example:
        >>> except Exception as e:
        ...     message = get_error_message(e)
        ...     show_toast(message)
    """
    if isinstance(error, MixrPayError):
        return error.message
    return str(error)
