"""
MixrPay Agent SDK - AgentWallet

Main class for AI agents to make x402 payments. Provides a simple interface
for making HTTP requests that automatically handle payments using session keys.

Quick Start:
    >>> from mixrpay import AgentWallet
    >>> 
    >>> # Initialize with your session key
    >>> wallet = AgentWallet(session_key="sk_live_...")
    >>> 
    >>> # Make requests - payments handled automatically!
    >>> response = wallet.fetch(
    ...     "https://api.example.com/ai/query",
    ...     method="POST",
    ...     json={"prompt": "Hello world"}
    ... )
    >>> print(response.json())
"""

import os
import time
import logging
from typing import Optional, Dict, Any, Callable, List, Literal
from dataclasses import dataclass, field
from enum import Enum
import httpx

from .session_key import SessionKey, create_session_auth_payload
from .x402 import (
    parse_402_response,
    build_x_payment_header,
    validate_payment_amount,
    PaymentRequirements,
)
from .exceptions import (
    MixrPayError,
    InsufficientBalanceError,
    SessionKeyExpiredError,
    SpendingLimitExceededError,
    PaymentFailedError,
    InvalidSessionKeyError,
    X402ProtocolError,
)


# =============================================================================
# Constants
# =============================================================================

SDK_VERSION = "0.1.0"
"""Current SDK version."""

DEFAULT_BASE_URL = os.environ.get("MIXRPAY_BASE_URL", "https://mixrpay.com")
"""Default MixrPay API base URL. Override with MIXRPAY_BASE_URL env var or base_url param."""

DEFAULT_FACILITATOR_URL = "https://x402.org/facilitator"
"""Default x402 facilitator URL."""

DEFAULT_TIMEOUT = 30.0
"""Default request timeout in seconds."""


class Network(Enum):
    """Supported blockchain networks."""
    BASE_MAINNET = (8453, "Base", False)
    BASE_SEPOLIA = (84532, "Base Sepolia", True)
    
    def __init__(self, chain_id: int, name: str, is_testnet: bool):
        self.chain_id = chain_id
        self.display_name = name
        self.is_testnet = is_testnet


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class PaymentEvent:
    """
    Record of a payment made by the agent.
    
    Attributes:
        amount_usd: Payment amount in USD
        recipient: Recipient wallet address
        tx_hash: Transaction hash on the blockchain (if available)
        timestamp: Unix timestamp when the payment was made
        description: Description of what was paid for
        url: URL that triggered the payment
    """
    amount_usd: float
    recipient: str
    tx_hash: Optional[str]
    timestamp: float
    description: Optional[str] = None
    url: Optional[str] = None


@dataclass
class SpendingStats:
    """
    Spending statistics for the session key.
    
    Attributes:
        total_spent_usd: Total amount spent in USD
        tx_count: Number of transactions made
        remaining_daily_usd: Remaining daily limit (None if no limit)
        remaining_total_usd: Remaining total limit (None if no limit)
        expires_at: When the session key expires (None if never)
    """
    total_spent_usd: float
    tx_count: int
    remaining_daily_usd: Optional[float]
    remaining_total_usd: Optional[float]
    expires_at: Optional[str]


@dataclass
class SessionKeyLimits:
    """Spending limits configured for a session key."""
    per_tx_usd: Optional[float] = None
    daily_usd: Optional[float] = None
    total_usd: Optional[float] = None


@dataclass
class SessionKeyUsage:
    """Current usage statistics for a session key."""
    today_usd: float = 0.0
    total_usd: float = 0.0
    tx_count: int = 0


@dataclass
class SessionKeyInfo:
    """
    Information about a session key.
    
    Attributes:
        address: The session key's address
        is_valid: Whether the key is currently valid
        limits: Spending limits
        usage: Current usage statistics
        expires_at: When the key expires (None if never)
        created_at: When the key was created
        name: Optional name given to the key
    """
    address: str
    is_valid: bool
    limits: SessionKeyLimits
    usage: SessionKeyUsage
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
    name: Optional[str] = None


@dataclass
class DiagnosticsResult:
    """
    Result of running diagnostics on the wallet.
    
    Attributes:
        healthy: Whether all checks passed
        issues: List of issues found
        checks: Individual check results
        sdk_version: SDK version
        network: Network name
        wallet_address: Wallet address
    """
    healthy: bool
    issues: List[str]
    checks: Dict[str, bool]
    sdk_version: str
    network: str
    wallet_address: str


# =============================================================================
# Session Authorization Data Classes
# =============================================================================

@dataclass
class SessionAuthorization:
    """
    Represents an active session authorization with a MixrPay merchant.
    
    A session authorization allows pre-approved spending up to a limit
    without requiring per-transaction signatures.
    
    Attributes:
        id: Unique session identifier
        merchant_id: The merchant's internal ID
        merchant_name: Display name of the merchant
        status: Current status (active, expired, revoked)
        spending_limit_usd: Maximum amount that can be spent
        amount_used_usd: Amount already spent in this session
        remaining_limit_usd: Amount remaining to spend
        expires_at: When this session authorization expires
        created_at: When this session was created
    """
    id: str
    merchant_id: str
    merchant_name: str
    status: str  # 'active', 'pending', 'expired', 'revoked'
    spending_limit_usd: float
    amount_used_usd: float
    remaining_limit_usd: float
    expires_at: str
    created_at: str


@dataclass
class ChargeResult:
    """
    Result of charging against a session authorization.
    
    Attributes:
        success: Whether the charge was successful
        charge_id: Unique identifier for this charge
        amount_usd: Amount that was charged
        tx_hash: Transaction hash (if on-chain)
        remaining_session_balance_usd: Remaining balance in the session
    """
    success: bool
    charge_id: Optional[str] = None
    amount_usd: float = 0.0
    tx_hash: Optional[str] = None
    remaining_session_balance_usd: float = 0.0


@dataclass
class CreateSessionOptions:
    """
    Options for creating a session authorization.
    
    Attributes:
        merchant_public_key: The merchant's public key (pk_...)
        spending_limit_usd: Maximum spending limit for the session
        duration_days: Number of days the session is valid
    """
    merchant_public_key: str
    spending_limit_usd: float = 25.0
    duration_days: int = 7


@dataclass
class CallMerchantApiOptions:
    """
    Options for calling a merchant's API with session-based payment.
    
    Attributes:
        url: The API endpoint URL
        merchant_public_key: The merchant's public key (pk_...)
        method: HTTP method (GET, POST, etc.)
        headers: Additional headers to include
        json: JSON body to send
        data: Form data to send
        price_usd: Expected price for this API call
        feature: Feature slug for tracking
        timeout: Request timeout in seconds
        spending_limit_usd: Spending limit if creating new session
        duration_days: Session duration if creating new session
    """
    url: str
    merchant_public_key: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    json: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    price_usd: Optional[float] = None
    feature: Optional[str] = None
    timeout: float = 30.0
    spending_limit_usd: float = 25.0
    duration_days: int = 7


@dataclass
class ChargeSessionOptions:
    """
    Options for manually charging against a session.
    
    Attributes:
        feature: Feature slug for tracking
        idempotency_key: Unique key to prevent double-charging
        metadata: Arbitrary metadata to attach to the charge
    """
    feature: Optional[str] = None
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# =============================================================================
# Logger Setup
# =============================================================================

logger = logging.getLogger("mixrpay")


class MixrPayLogger:
    """Internal logger for MixrPay SDK."""
    
    PREFIX = "[MixrPay]"
    
    def __init__(self, level: str = "WARNING"):
        self.logger = logging.getLogger("mixrpay")
        self.set_level(level)
        
        # Add handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)
    
    def set_level(self, level: str) -> None:
        """Set the logging level."""
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "warn": logging.WARNING,
            "error": logging.ERROR,
            "none": logging.CRITICAL + 1,  # Effectively disables logging
        }
        self.logger.setLevel(level_map.get(level.lower(), logging.WARNING))
    
    def debug(self, msg: str, *args: Any) -> None:
        self.logger.debug(f"{self.PREFIX} 🔍 {msg}", *args)
    
    def info(self, msg: str, *args: Any) -> None:
        self.logger.info(f"{self.PREFIX} ℹ️  {msg}", *args)
    
    def warning(self, msg: str, *args: Any) -> None:
        self.logger.warning(f"{self.PREFIX} ⚠️  {msg}", *args)
    
    def error(self, msg: str, *args: Any) -> None:
        self.logger.error(f"{self.PREFIX} ❌ {msg}", *args)
    
    def payment(self, amount: float, recipient: str, description: Optional[str] = None) -> None:
        desc = f' for "{description}"' if description else ""
        self.logger.info(f"{self.PREFIX} 💸 Paid ${amount:.4f} to {recipient[:10]}...{desc}")


# =============================================================================
# AgentWallet Class
# =============================================================================

class AgentWallet:
    """
    A wallet wrapper for AI agents that handles x402 payments automatically.
    
    The AgentWallet makes it easy for AI agents to access paid APIs. When a server
    returns a 402 Payment Required response, the SDK automatically handles the payment
    using a session key and retries the request.
    
    Features:
        - 🔐 Secure: Session keys have built-in spending limits
        - 🤖 Agent-Ready: Works with LangChain, CrewAI, and any framework
        - ⚡ Automatic: No manual payment handling needed
        - 📊 Tracking: Built-in spending statistics and payment history
        - 🔄 Drop-in: Similar interface to requests/httpx
    
    Quick Start:
        >>> wallet = AgentWallet(
        ...     session_key="sk_live_...",
        ...     on_payment=lambda p: print(f"Paid ${p.amount_usd}")
        ... )
        >>> 
        >>> # Make requests - payments are automatic!
        >>> response = wallet.fetch("https://api.example.com/endpoint")
        >>> print(response.json())
    
    Session Keys:
        Session keys are granted by wallet owners and have spending limits:
        - Per-transaction limit: Maximum amount per single request
        - Daily limit: Maximum total per 24 hours
        - Total limit: Maximum lifetime spend
        - Expiration: When the key becomes invalid
        
        Keys are prefixed with ``sk_live_`` (mainnet) or ``sk_test_`` (testnet).
    
    Args:
        session_key: Session key granted by the wallet owner (sk_live_... or sk_test_...)
        wallet_address: Optional smart wallet address (auto-detected if not provided)
        max_payment_usd: Optional client-side max payment per request
        on_payment: Optional callback when a payment is made
        facilitator_url: x402 facilitator endpoint
        base_url: MixrPay API base URL
        timeout: Request timeout in seconds
        log_level: Logging level ('debug', 'info', 'warning', 'error', 'none')
    
    Raises:
        InvalidSessionKeyError: If the session key format is invalid
    
    Example:
        Basic usage::
        
            from mixrpay import AgentWallet
            
            wallet = AgentWallet(session_key="sk_live_abc123...")
            response = wallet.fetch("https://api.example.com/query")
            print(response.json())
        
        With all options::
        
            wallet = AgentWallet(
                session_key="sk_live_abc123...",
                max_payment_usd=5.0,
                on_payment=lambda p: print(f"Paid ${p.amount_usd}"),
                log_level="info",
            )
    """
    
    def __init__(
        self,
        session_key: str,
        *,
        wallet_address: Optional[str] = None,
        max_payment_usd: Optional[float] = None,
        on_payment: Optional[Callable[[PaymentEvent], None]] = None,
        facilitator_url: str = DEFAULT_FACILITATOR_URL,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        log_level: Literal["debug", "info", "warning", "error", "none"] = "warning",
    ):
        # Initialize logger first
        self._logger = MixrPayLogger(log_level)
        
        # Validate configuration
        self._validate_config(session_key, max_payment_usd)
        
        # Parse session key
        self._session_key = SessionKey.from_string(session_key)
        self._wallet_address = wallet_address
        self._max_payment_usd = max_payment_usd
        self._on_payment = on_payment
        self._facilitator_url = facilitator_url
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        
        # Payment tracking
        self._payments: List[PaymentEvent] = []
        self._total_spent_usd = 0.0
        
        # Session key info cache
        self._session_key_info: Optional[SessionKeyInfo] = None
        self._session_key_info_fetched_at: Optional[float] = None
        
        # HTTP client
        self._client = httpx.Client(timeout=timeout)
        
        self._logger.debug(
            f"AgentWallet initialized: wallet={self.wallet_address}, "
            f"testnet={self.is_testnet}, max_payment=${max_payment_usd}"
        )
    
    def _validate_config(self, session_key: str, max_payment_usd: Optional[float]) -> None:
        """Validate the configuration before initialization."""
        # Check session key presence
        if not session_key:
            raise InvalidSessionKeyError(
                "Session key is required. Get one from the wallet owner or "
                "create one at your MixrPay server /wallet/sessions"
            )
        
        # Check session key format
        key = session_key.strip()
        if not key.startswith("sk_live_") and not key.startswith("sk_test_"):
            raise InvalidSessionKeyError(
                f"Invalid session key prefix. Expected 'sk_live_' (mainnet) or "
                f"'sk_test_' (testnet), got '{key[:10]}...'"
            )
        
        # Check session key length
        expected_length = 8 + 64  # prefix + 64 hex chars
        if len(key) != expected_length:
            raise InvalidSessionKeyError(
                f"Invalid session key length. Expected {expected_length} characters, "
                f"got {len(key)}. Make sure you copied the complete key."
            )
        
        # Validate hex portion
        hex_portion = key[8:]
        if not all(c in "0123456789abcdefABCDEF" for c in hex_portion):
            raise InvalidSessionKeyError(
                "Invalid session key format. The key should contain only "
                "hexadecimal characters after the prefix."
            )
        
        # Validate max_payment_usd
        if max_payment_usd is not None:
            if max_payment_usd <= 0:
                raise MixrPayError("max_payment_usd must be a positive number")
            if max_payment_usd > 10000:
                self._logger.warning(
                    f"max_payment_usd is very high (${max_payment_usd}). "
                    "Consider using a lower limit for safety."
                )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def wallet_address(self) -> str:
        """Get the wallet address."""
        if self._wallet_address:
            return self._wallet_address
        return self._session_key.address
    
    @property
    def is_testnet(self) -> bool:
        """Check if using testnet session key."""
        return self._session_key.is_test
    
    @property
    def network(self) -> Network:
        """Get the network information."""
        return Network.BASE_SEPOLIA if self.is_testnet else Network.BASE_MAINNET
    
    # =========================================================================
    # Core Methods
    # =========================================================================
    
    def fetch(
        self,
        url: str,
        *,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        max_retries: int = 1,
    ) -> httpx.Response:
        """
        Make an HTTP request, automatically handling x402 payment if required.
        
        If server returns 402 Payment Required:
        1. Parse payment requirements from response
        2. Sign transferWithAuthorization using session key
        3. Retry request with X-PAYMENT header
        
        Args:
            url: Request URL
            method: HTTP method (GET, POST, etc.)
            headers: Optional request headers
            json: Optional JSON body (mutually exclusive with data)
            data: Optional form data body (mutually exclusive with json)
            params: Optional URL query parameters
            timeout: Optional request timeout (overrides default)
            max_retries: Maximum retries for payment (default 1)
        
        Returns:
            httpx.Response from the server
        
        Raises:
            InsufficientBalanceError: Wallet doesn't have enough USDC
            SessionKeyExpiredError: Session key has expired
            SpendingLimitExceededError: Would exceed session key limits
            PaymentFailedError: Payment transaction failed
        
        Example:
            GET request::
            
                response = wallet.fetch("https://api.example.com/data")
                data = response.json()
            
            POST request with JSON::
            
                response = wallet.fetch(
                    "https://api.example.com/generate",
                    method="POST",
                    json={"prompt": "Hello world"}
                )
        """
        self._logger.debug(f"Fetching {method} {url}")
        
        request_headers = dict(headers or {})
        request_timeout = timeout or self._timeout
        
        # Make initial request
        response = self._make_request(
            method=method,
            url=url,
            headers=request_headers,
            json=json,
            data=data,
            params=params,
            timeout=request_timeout,
        )
        
        self._logger.debug(f"Initial response: {response.status_code}")
        
        # Handle 402 Payment Required
        retries = 0
        while response.status_code == 402 and retries < max_retries:
            retries += 1
            self._logger.info(f"Payment required for {url}")
            
            # Parse payment requirements
            try:
                requirements = parse_402_response(response)
                self._logger.debug(
                    f"Payment requirements: ${requirements.amount_usd:.4f} "
                    f"to {requirements.recipient}"
                )
            except X402ProtocolError as e:
                self._logger.error(f"Failed to parse payment requirements: {e}")
                raise PaymentFailedError(
                    f"Failed to parse payment requirements: {e}. "
                    "The server may not be properly configured for x402 payments."
                )
            
            # Check if expired
            if requirements.is_expired():
                raise PaymentFailedError(
                    "Payment requirements have expired. "
                    "This usually means the request took too long. Try again."
                )
            
            # Validate amount against client-side limit
            if self._max_payment_usd is not None and requirements.amount_usd > self._max_payment_usd:
                raise SpendingLimitExceededError(
                    "client_max",
                    self._max_payment_usd,
                    requirements.amount_usd,
                )
            
            # Build X-PAYMENT header
            try:
                self._logger.debug("Signing payment authorization...")
                x_payment = build_x_payment_header(
                    requirements=requirements,
                    session_key=self._session_key,
                    wallet_address=self.wallet_address,
                )
            except Exception as e:
                self._logger.error(f"Failed to sign payment: {e}")
                raise PaymentFailedError(
                    f"Failed to sign payment: {e}. "
                    "This may indicate an issue with the session key."
                )
            
            # Retry with payment
            self._logger.debug("Retrying request with payment...")
            request_headers["X-PAYMENT"] = x_payment
            
            response = self._make_request(
                method=method,
                url=url,
                headers=request_headers,
                json=json,
                data=data,
                params=params,
                timeout=request_timeout,
            )
            
            # Track successful payment (if not still 402)
            if response.status_code != 402:
                payment = PaymentEvent(
                    amount_usd=requirements.amount_usd,
                    recipient=requirements.recipient,
                    tx_hash=response.headers.get("X-Payment-TxHash"),
                    timestamp=time.time(),
                    description=requirements.description,
                    url=url,
                )
                self._payments.append(payment)
                self._total_spent_usd += requirements.amount_usd
                
                self._logger.payment(
                    requirements.amount_usd,
                    requirements.recipient,
                    requirements.description
                )
                
                if self._on_payment:
                    self._on_payment(payment)
        
        # Check for payment-specific error responses
        if response.status_code == 402:
            self._handle_payment_error(response)
        
        return response
    
    def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        json: Optional[Dict[str, Any]],
        data: Optional[Any],
        params: Optional[Dict[str, str]],
        timeout: float,
    ) -> httpx.Response:
        """Make an HTTP request."""
        return self._client.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            data=data,
            params=params,
            timeout=timeout,
        )
    
    def _handle_payment_error(self, response: httpx.Response) -> None:
        """Handle payment-specific errors from the response."""
        try:
            error_data = response.json()
        except Exception:
            error_data = {}
        
        error_code = error_data.get("error_code", "")
        error_message = error_data.get("error", error_data.get("message", "Payment required"))
        
        self._logger.error(f"Payment failed: {error_code} - {error_message}")
        
        if error_code == "insufficient_balance":
            raise InsufficientBalanceError(
                required=error_data.get("required", 0),
                available=error_data.get("available", 0),
            )
        elif error_code == "session_key_expired":
            raise SessionKeyExpiredError(error_data.get("expired_at", "unknown"))
        elif error_code == "spending_limit_exceeded":
            raise SpendingLimitExceededError(
                limit_type=error_data.get("limit_type", "unknown"),
                limit=error_data.get("limit", 0),
                attempted=error_data.get("attempted", 0),
            )
        else:
            raise PaymentFailedError(error_message)
    
    # =========================================================================
    # HTTP Method Shortcuts
    # =========================================================================
    
    def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request. Shorthand for fetch(url, method="GET", ...)."""
        return self.fetch(url, method="GET", **kwargs)
    
    def post(self, url: str, **kwargs) -> httpx.Response:
        """Make a POST request. Shorthand for fetch(url, method="POST", ...)."""
        return self.fetch(url, method="POST", **kwargs)
    
    def put(self, url: str, **kwargs) -> httpx.Response:
        """Make a PUT request. Shorthand for fetch(url, method="PUT", ...)."""
        return self.fetch(url, method="PUT", **kwargs)
    
    def delete(self, url: str, **kwargs) -> httpx.Response:
        """Make a DELETE request. Shorthand for fetch(url, method="DELETE", ...)."""
        return self.fetch(url, method="DELETE", **kwargs)
    
    def patch(self, url: str, **kwargs) -> httpx.Response:
        """Make a PATCH request. Shorthand for fetch(url, method="PATCH", ...)."""
        return self.fetch(url, method="PATCH", **kwargs)
    
    # =========================================================================
    # Wallet Information
    # =========================================================================
    
    def get_balance(self) -> float:
        """
        Get current USDC balance of the wallet.
        
        Returns:
            USDC balance in USD
        
        Example:
            >>> balance = wallet.get_balance()
            >>> print(f"Balance: ${balance:.2f}")
        """
        self._logger.debug("Fetching wallet balance...")
        
        try:
            response = self._client.get(
                f"{self._base_url}/v1/wallet/balance",
                headers={"X-Session-Key": self._session_key.address},
            )
            if response.status_code == 200:
                data = response.json()
                balance = data.get("balance_usd", data.get("balanceUsd", 0.0))
                self._logger.debug(f"Balance: ${balance}")
                return balance
        except Exception as e:
            self._logger.warning(f"Failed to fetch balance: {e}")
        
        # Fallback: return tracked spending subtracted from assumed balance
        self._logger.debug("Using estimated balance based on tracking")
        return max(0, 100.0 - self._total_spent_usd)
    
    def get_session_key_info(self, refresh: bool = False) -> SessionKeyInfo:
        """
        Get information about the session key.
        
        Args:
            refresh: Force refresh from server (default: use cache if < 60s old)
        
        Returns:
            Session key details including limits and expiration
        
        Example:
            >>> info = wallet.get_session_key_info()
            >>> print(f"Daily limit: ${info.limits.daily_usd}")
            >>> print(f"Expires: {info.expires_at}")
        """
        # Use cache if available and fresh
        cache_age = (
            time.time() - self._session_key_info_fetched_at
            if self._session_key_info_fetched_at
            else float("inf")
        )
        
        if not refresh and self._session_key_info and cache_age < 60:
            return self._session_key_info
        
        self._logger.debug("Fetching session key info...")
        
        try:
            response = self._client.get(
                f"{self._base_url}/v1/session-key/info",
                headers={"X-Session-Key": self._session_key.address},
            )
            
            if response.status_code == 200:
                data = response.json()
                self._session_key_info = SessionKeyInfo(
                    address=self._session_key.address,
                    is_valid=data.get("is_valid", data.get("isValid", True)),
                    limits=SessionKeyLimits(
                        per_tx_usd=data.get("per_tx_limit_usd", data.get("perTxLimitUsd")),
                        daily_usd=data.get("daily_limit_usd", data.get("dailyLimitUsd")),
                        total_usd=data.get("total_limit_usd", data.get("totalLimitUsd")),
                    ),
                    usage=SessionKeyUsage(
                        today_usd=data.get("today_spent_usd", data.get("todaySpentUsd", 0)),
                        total_usd=data.get("total_spent_usd", data.get("totalSpentUsd", 0)),
                        tx_count=data.get("tx_count", data.get("txCount", 0)),
                    ),
                    expires_at=data.get("expires_at"),
                    created_at=data.get("created_at"),
                    name=data.get("name"),
                )
                self._session_key_info_fetched_at = time.time()
                return self._session_key_info
        except Exception as e:
            self._logger.warning(f"Failed to fetch session key info: {e}")
        
        # Return minimal info if fetch fails
        return SessionKeyInfo(
            address=self._session_key.address,
            is_valid=True,
            limits=SessionKeyLimits(),
            usage=SessionKeyUsage(
                today_usd=self._total_spent_usd,
                total_usd=self._total_spent_usd,
                tx_count=len(self._payments),
            ),
        )
    
    def get_spending_stats(self) -> SpendingStats:
        """
        Get spending stats for this session key.
        
        Returns:
            SpendingStats with usage and limit information
        
        Example:
            >>> stats = wallet.get_spending_stats()
            >>> print(f"Spent: ${stats.total_spent_usd:.2f}")
            >>> print(f"Remaining daily: ${stats.remaining_daily_usd or 'unlimited'}")
        """
        self._logger.debug("Fetching spending stats...")
        
        try:
            response = self._client.get(
                f"{self._base_url}/v1/session-key/stats",
                headers={"X-Session-Key": self._session_key.address},
            )
            if response.status_code == 200:
                data = response.json()
                return SpendingStats(
                    total_spent_usd=data.get("total_spent_usd", data.get("totalSpentUsd", self._total_spent_usd)),
                    tx_count=data.get("tx_count", data.get("txCount", len(self._payments))),
                    remaining_daily_usd=data.get("remaining_daily_usd", data.get("remainingDailyUsd")),
                    remaining_total_usd=data.get("remaining_total_usd", data.get("remainingTotalUsd")),
                    expires_at=data.get("expires_at"),
                )
        except Exception as e:
            self._logger.warning(f"Failed to fetch spending stats: {e}")
        
        # Fallback: return local tracking data
        return SpendingStats(
            total_spent_usd=self._total_spent_usd,
            tx_count=len(self._payments),
            remaining_daily_usd=None,
            remaining_total_usd=None,
            expires_at=None,
        )
    
    def get_payment_history(self) -> List[PaymentEvent]:
        """
        Get list of payments made in this session.
        
        Returns:
            List of PaymentEvent objects
        """
        return list(self._payments)
    
    def get_total_spent(self) -> float:
        """
        Get the total amount spent in this session.
        
        Returns:
            Total spent in USD
        """
        return self._total_spent_usd
    
    # =========================================================================
    # Diagnostics
    # =========================================================================
    
    def run_diagnostics(self) -> DiagnosticsResult:
        """
        Run diagnostics to verify the wallet is properly configured.
        
        This is useful for debugging integration issues.
        
        Returns:
            Diagnostic results with status and any issues found
        
        Example:
            >>> diagnostics = wallet.run_diagnostics()
            >>> if diagnostics.healthy:
            ...     print("✅ Wallet is ready to use")
            ... else:
            ...     print("❌ Issues found:")
            ...     for issue in diagnostics.issues:
            ...         print(f"  - {issue}")
        """
        self._logger.info("Running diagnostics...")
        
        issues: List[str] = []
        checks: Dict[str, bool] = {}
        
        # Check 1: Session key format
        checks["session_key_format"] = True  # Already validated in constructor
        
        # Check 2: Network connectivity
        try:
            response = self._client.get(f"{self._base_url}/health", timeout=5.0)
            checks["api_connectivity"] = response.status_code == 200
            if not checks["api_connectivity"]:
                issues.append(f"API server returned {response.status_code}. Check base_url configuration.")
        except Exception:
            checks["api_connectivity"] = False
            issues.append("Cannot connect to MixrPay API. Check your network connection and base_url.")
        
        # Check 3: Session key validity
        try:
            info = self.get_session_key_info(refresh=True)
            checks["session_key_valid"] = info.is_valid
            if not info.is_valid:
                issues.append("Session key is invalid or has been revoked.")
            
            # Check expiration
            if info.expires_at:
                from datetime import datetime
                try:
                    expires = datetime.fromisoformat(info.expires_at.replace("Z", "+00:00"))
                    if expires < datetime.now(expires.tzinfo):
                        checks["session_key_valid"] = False
                        issues.append(f"Session key expired on {info.expires_at}")
                except Exception:
                    pass
        except Exception:
            checks["session_key_valid"] = False
            issues.append("Could not verify session key validity.")
        
        # Check 4: Balance
        try:
            balance = self.get_balance()
            checks["has_balance"] = balance > 0
            if balance <= 0:
                issues.append("Wallet has no USDC balance. Top up at your MixrPay server /wallet")
            elif balance < 1:
                issues.append(f"Low balance: ${balance:.2f}. Consider topping up.")
        except Exception:
            checks["has_balance"] = False
            issues.append("Could not fetch wallet balance.")
        
        healthy = len(issues) == 0
        
        self._logger.info(f"Diagnostics complete: healthy={healthy}, issues={issues}")
        
        return DiagnosticsResult(
            healthy=healthy,
            issues=issues,
            checks=checks,
            sdk_version=SDK_VERSION,
            network=self.network.display_name,
            wallet_address=self.wallet_address,
        )
    
    def set_log_level(self, level: str) -> None:
        """
        Set the logging level.
        
        Args:
            level: 'debug', 'info', 'warning', 'error', or 'none'
        """
        self._logger.set_level(level)
    
    def set_debug(self, enable: bool) -> None:
        """
        Enable or disable debug logging.
        
        Args:
            enable: True to enable debug logging, False to disable
        """
        self._logger.set_level("debug" if enable else "none")

    # =========================================================================
    # Session Authorization Methods (for MixrPay Merchants)
    # =========================================================================

    def _get_session_auth_headers(self) -> Dict[str, str]:
        """
        Create the X-Session-Auth header for secure API authentication.
        Uses signature-based authentication - private key is NEVER transmitted.
        
        Returns:
            Headers dict with X-Session-Auth
        """
        payload = create_session_auth_payload(self._session_key)
        return {"X-Session-Auth": payload.to_header()}

    def get_or_create_session(
        self,
        merchant_public_key: str,
        spending_limit_usd: float = 25.0,
        duration_days: int = 7,
    ) -> "SessionAuthorization":
        """
        Get an existing session or create a new one with a MixrPay merchant.
        
        This is the recommended way to interact with MixrPay-enabled APIs.
        If an active session exists, it will be returned. Otherwise, a new
        session authorization request will be created and confirmed.
        
        Args:
            merchant_public_key: The merchant's public key (pk_...)
            spending_limit_usd: Maximum spending limit for the session
            duration_days: Number of days the session is valid
            
        Returns:
            Active SessionAuthorization
            
        Raises:
            MixrPayError: If merchant not found or session creation fails
            
        Example:
            >>> session = wallet.get_or_create_session(
            ...     merchant_public_key="pk_live_abc123...",
            ...     spending_limit_usd=25.00,
            ...     duration_days=7,
            ... )
            >>> print(f"Session active: ${session.remaining_limit_usd} remaining")
        """
        self._logger.debug(f"get_or_create_session called for merchant {merchant_public_key[:20]}...")

        # First, check for existing active session
        try:
            existing_session = self.get_session_by_merchant(merchant_public_key)
            if existing_session and existing_session.status == "active":
                self._logger.debug(f"Found existing active session: {existing_session.id}")
                return existing_session
        except Exception:
            # No existing session, continue to create one
            pass

        # Create new session authorization
        self._logger.info(f"Creating new session with merchant {merchant_public_key[:20]}...")

        auth_headers = self._get_session_auth_headers()

        # Step 1: Request session authorization
        authorize_response = self._client.post(
            f"{self._base_url}/api/v2/session/authorize",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={
                "merchant_public_key": merchant_public_key,
                "spending_limit_usd": spending_limit_usd,
                "duration_days": duration_days,
            },
        )

        if not authorize_response.is_success:
            error = authorize_response.json() if authorize_response.content else {}
            raise MixrPayError(
                error.get("message") or error.get("error") or 
                f"Failed to create session: {authorize_response.status_code}"
            )

        authorize_data = authorize_response.json()
        session_id = authorize_data.get("session_id")
        message_to_sign = authorize_data.get("message_to_sign")

        if not session_id or not message_to_sign:
            raise MixrPayError("Invalid authorize response: missing session_id or message_to_sign")

        # Step 2: Sign the authorization message
        self._logger.debug("Signing session authorization message...")
        signature = self._session_key.sign_message(message_to_sign)

        # Step 3: Confirm the session with signature
        confirm_response = self._client.post(
            f"{self._base_url}/api/v2/session/confirm",
            headers={"Content-Type": "application/json"},
            json={
                "session_id": session_id,
                "signature": signature,
                "wallet_address": self.wallet_address,
            },
        )

        if not confirm_response.is_success:
            error = confirm_response.json() if confirm_response.content else {}
            raise MixrPayError(
                error.get("message") or error.get("error") or 
                f"Failed to confirm session: {confirm_response.status_code}"
            )

        confirm_data = confirm_response.json()
        self._logger.info(f"Session created: {confirm_data.get('session', {}).get('id') or session_id}")

        return self._parse_session_response(confirm_data.get("session") or confirm_data)

    def get_session_by_merchant(self, merchant_public_key: str) -> Optional["SessionAuthorization"]:
        """
        Get session status for a specific merchant.
        
        Args:
            merchant_public_key: The merchant's public key
            
        Returns:
            SessionAuthorization or None if not found
        """
        self._logger.debug(f"get_session_by_merchant: {merchant_public_key}")

        auth_headers = self._get_session_auth_headers()
        response = self._client.get(
            f"{self._base_url}/api/v2/session/status",
            params={"merchant_public_key": merchant_public_key},
            headers=auth_headers,
        )

        if response.status_code == 404:
            return None

        if not response.is_success:
            error = response.json() if response.content else {}
            raise MixrPayError(error.get("message") or f"Failed to get session: {response.status_code}")

        data = response.json()
        if not data.get("has_session"):
            return None
        return self._parse_session_response(data.get("session")) if data.get("session") else None

    def list_sessions(self) -> List["SessionAuthorization"]:
        """
        List all session authorizations for this wallet.
        
        Returns:
            List of SessionAuthorization objects
            
        Example:
            >>> sessions = wallet.list_sessions()
            >>> for session in sessions:
            ...     print(f"{session.merchant_name}: ${session.remaining_limit_usd} remaining")
        """
        self._logger.debug("list_sessions")

        auth_headers = self._get_session_auth_headers()
        response = self._client.get(
            f"{self._base_url}/api/v2/session/list",
            headers=auth_headers,
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            raise MixrPayError(error.get("message") or f"Failed to list sessions: {response.status_code}")

        data = response.json()
        return [self._parse_session_response(s) for s in data.get("sessions", [])]

    def revoke_session(self, session_id: str) -> bool:
        """
        Revoke a session authorization.
        
        After revocation, no further charges can be made against this session.
        
        Args:
            session_id: The session ID to revoke
            
        Returns:
            True if revoked successfully
            
        Example:
            >>> revoked = wallet.revoke_session("sess_abc123")
            >>> if revoked:
            ...     print("Session revoked successfully")
        """
        self._logger.debug(f"revoke_session: {session_id}")

        auth_headers = self._get_session_auth_headers()
        response = self._client.post(
            f"{self._base_url}/api/v2/session/revoke",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={"session_id": session_id},
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            self._logger.error(f"Failed to revoke session: {error}")
            return False

        self._logger.info(f"Session {session_id} revoked")
        return True

    def charge_session(
        self,
        session_id: str,
        amount_usd: float,
        feature: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "ChargeResult":
        """
        Charge against an active session authorization.
        
        This is useful when you need to manually charge a session outside of
        the call_merchant_api() flow.
        
        Args:
            session_id: The session ID to charge
            amount_usd: Amount to charge in USD
            feature: Feature slug for tracking
            idempotency_key: Unique key to prevent double-charging
            metadata: Arbitrary metadata to attach to the charge
            
        Returns:
            ChargeResult with charge details
            
        Example:
            >>> result = wallet.charge_session(
            ...     "sess_abc123", 
            ...     0.05,
            ...     feature="ai-generation",
            ...     idempotency_key="unique-key-123",
            ... )
            >>> print(f"Charged ${result.amount_usd}, remaining: ${result.remaining_session_balance_usd}")
        """
        self._logger.debug(f"charge_session: {session_id}, ${amount_usd}")

        auth_headers = self._get_session_auth_headers()
        response = self._client.post(
            f"{self._base_url}/api/v2/charge",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={
                "session_id": session_id,
                "price_usd": amount_usd,
                "feature": feature,
                "idempotency_key": idempotency_key,
                "metadata": metadata,
            },
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            
            if response.status_code == 402:
                if error.get("error") == "session_limit_exceeded":
                    raise SpendingLimitExceededError(
                        "session",
                        error.get("session_limit_usd", error.get("sessionLimitUsd", 0)),
                        amount_usd,
                    )
                if error.get("error") == "insufficient_balance":
                    raise InsufficientBalanceError(
                        amount_usd,
                        error.get("available_usd", error.get("availableUsd", 0)),
                    )
            
            raise MixrPayError(error.get("message") or f"Charge failed: {response.status_code}")

        data = response.json()
        
        self._logger.payment(amount_usd, session_id, feature)

        return ChargeResult(
            success=True,
            charge_id=data.get("charge_id") or data.get("chargeId"),
            amount_usd=data.get("amount_usd") or data.get("amountUsd") or amount_usd,
            tx_hash=data.get("tx_hash") or data.get("txHash"),
            remaining_session_balance_usd=data.get("remaining_session_balance_usd") or data.get("remainingSessionBalanceUsd") or 0,
        )

    def call_merchant_api(
        self,
        url: str,
        merchant_public_key: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        price_usd: Optional[float] = None,
        feature: Optional[str] = None,
        timeout: float = 30.0,
        spending_limit_usd: float = 25.0,
        duration_days: int = 7,
    ) -> httpx.Response:
        """
        Call a MixrPay merchant's API with automatic session management.
        
        This is the recommended way to interact with MixrPay-enabled APIs.
        It automatically:
        1. Gets or creates a session authorization
        2. Adds the X-Mixr-Session header to the request
        3. Handles payment errors and session expiration
        
        Args:
            url: The API endpoint URL
            merchant_public_key: The merchant's public key (pk_...)
            method: HTTP method
            headers: Additional headers to include
            json: JSON body to send
            data: Form data to send
            price_usd: Expected price for this call (for validation)
            feature: Feature slug for tracking
            timeout: Request timeout in seconds
            spending_limit_usd: Spending limit if creating new session
            duration_days: Session duration if creating new session
            
        Returns:
            Response from the merchant API
            
        Example:
            >>> response = wallet.call_merchant_api(
            ...     url="https://api.merchant.com/generate",
            ...     merchant_public_key="pk_live_abc123...",
            ...     json={"prompt": "Hello world"},
            ...     price_usd=0.05,
            ... )
            >>> print(response.json())
        """
        self._logger.debug(f"call_merchant_api: {method} {url}")

        # Get or create session
        session = self.get_or_create_session(
            merchant_public_key=merchant_public_key,
            spending_limit_usd=spending_limit_usd,
            duration_days=duration_days,
        )

        # Build request headers with session token
        request_headers = headers.copy() if headers else {}
        request_headers["X-Mixr-Session"] = session.id

        if price_usd is not None:
            request_headers["X-Expected-Price-Usd"] = str(price_usd)
        if feature:
            request_headers["X-Feature"] = feature

        # Make the request
        response = self._client.request(
            method=method,
            url=url,
            headers=request_headers,
            json=json,
            data=data,
            timeout=timeout,
        )

        # If payment successful, log it
        if response.is_success and price_usd:
            self._logger.payment(price_usd, session.id, feature)

        return response

    def _parse_session_response(self, data: Dict[str, Any]) -> "SessionAuthorization":
        """Parse API response into SessionAuthorization object."""
        return SessionAuthorization(
            id=data.get("id") or data.get("session_id") or data.get("sessionId") or "",
            merchant_id=data.get("merchant_id") or data.get("merchantId") or "",
            merchant_name=data.get("merchant_name") or data.get("merchantName") or "Unknown",
            status=data.get("status") or "active",
            spending_limit_usd=float(data.get("spending_limit_usd") or data.get("spendingLimitUsd") or data.get("spending_limit") or 0),
            amount_used_usd=float(data.get("amount_used_usd") or data.get("amountUsedUsd") or data.get("amount_used") or 0),
            remaining_limit_usd=float(
                data.get("remaining_usd") or data.get("remaining_limit_usd") or data.get("remainingLimitUsd") or data.get("remaining_limit") or
                (float(data.get("spending_limit_usd") or data.get("spendingLimitUsd") or 0) - float(data.get("amount_used_usd") or data.get("amountUsedUsd") or 0))
            ),
            expires_at=data.get("expires_at") or data.get("expiresAt") or "",
            created_at=data.get("created_at") or data.get("createdAt") or "",
        )


# =============================================================================
# Async Version
# =============================================================================

class AsyncAgentWallet:
    """
    Async version of AgentWallet for use with asyncio.
    
    Usage:
        >>> async with AsyncAgentWallet(session_key="sk_live_...") as wallet:
        ...     response = await wallet.fetch("https://api.example.com/endpoint")
        ...     print(response.json())
    
    For concurrent requests:
        >>> async with AsyncAgentWallet(session_key="sk_live_...") as wallet:
        ...     tasks = [
        ...         wallet.fetch(f"https://api.example.com/query/{i}")
        ...         for i in range(10)
        ...     ]
        ...     responses = await asyncio.gather(*tasks)
    """
    
    def __init__(
        self,
        session_key: str,
        *,
        wallet_address: Optional[str] = None,
        max_payment_usd: Optional[float] = None,
        on_payment: Optional[Callable[[PaymentEvent], None]] = None,
        facilitator_url: str = DEFAULT_FACILITATOR_URL,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        log_level: Literal["debug", "info", "warning", "error", "none"] = "warning",
    ):
        self._logger = MixrPayLogger(log_level)
        
        # Validate session key format
        if not session_key:
            raise InvalidSessionKeyError("Session key is required.")
        
        key = session_key.strip()
        if not key.startswith("sk_live_") and not key.startswith("sk_test_"):
            raise InvalidSessionKeyError(
                f"Invalid session key prefix. Expected 'sk_live_' or 'sk_test_'."
            )
        
        self._session_key = SessionKey.from_string(session_key)
        self._wallet_address = wallet_address
        self._max_payment_usd = max_payment_usd
        self._on_payment = on_payment
        self._facilitator_url = facilitator_url
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        
        self._payments: List[PaymentEvent] = []
        self._total_spent_usd = 0.0
        
        self._client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
    
    @property
    def wallet_address(self) -> str:
        if self._wallet_address:
            return self._wallet_address
        return self._session_key.address
    
    @property
    def is_testnet(self) -> bool:
        return self._session_key.is_test
    
    async def fetch(
        self,
        url: str,
        *,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        max_retries: int = 1,
    ) -> httpx.Response:
        """Make an async HTTP request with automatic x402 payment handling."""
        self._logger.debug(f"Async fetching {method} {url}")
        
        request_headers = dict(headers or {})
        request_timeout = timeout or self._timeout
        
        response = await self._client.request(
            method=method,
            url=url,
            headers=request_headers,
            json=json,
            data=data,
            params=params,
            timeout=request_timeout,
        )
        
        retries = 0
        while response.status_code == 402 and retries < max_retries:
            retries += 1
            self._logger.info(f"Payment required for {url}")
            
            try:
                requirements = parse_402_response(response)
            except X402ProtocolError as e:
                raise PaymentFailedError(f"Failed to parse payment requirements: {e}")
            
            if requirements.is_expired():
                raise PaymentFailedError("Payment requirements have expired")
            
            if self._max_payment_usd is not None and requirements.amount_usd > self._max_payment_usd:
                raise SpendingLimitExceededError(
                    "client_max",
                    self._max_payment_usd,
                    requirements.amount_usd,
                )
            
            try:
                x_payment = build_x_payment_header(
                    requirements=requirements,
                    session_key=self._session_key,
                    wallet_address=self.wallet_address,
                )
            except Exception as e:
                raise PaymentFailedError(f"Failed to sign payment: {e}")
            
            request_headers["X-PAYMENT"] = x_payment
            
            response = await self._client.request(
                method=method,
                url=url,
                headers=request_headers,
                json=json,
                data=data,
                params=params,
                timeout=request_timeout,
            )
            
            if response.status_code != 402:
                payment = PaymentEvent(
                    amount_usd=requirements.amount_usd,
                    recipient=requirements.recipient,
                    tx_hash=response.headers.get("X-Payment-TxHash"),
                    timestamp=time.time(),
                    description=requirements.description,
                    url=url,
                )
                self._payments.append(payment)
                self._total_spent_usd += requirements.amount_usd
                
                self._logger.payment(
                    requirements.amount_usd,
                    requirements.recipient,
                    requirements.description
                )
                
                if self._on_payment:
                    self._on_payment(payment)
        
        return response
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make an async GET request."""
        return await self.fetch(url, method="GET", **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Make an async POST request."""
        return await self.fetch(url, method="POST", **kwargs)
    
    async def get_balance(self) -> float:
        """Get current USDC balance of the wallet."""
        try:
            response = await self._client.get(
                f"{self._base_url}/v1/wallet/balance",
                headers={"X-Session-Key": self._session_key.address},
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("balance_usd", data.get("balanceUsd", 0.0))
        except Exception:
            pass
        return max(0, 100.0 - self._total_spent_usd)
    
    def get_spending_stats(self) -> SpendingStats:
        """Get spending stats (local tracking only in async version)."""
        return SpendingStats(
            total_spent_usd=self._total_spent_usd,
            tx_count=len(self._payments),
            remaining_daily_usd=None,
            remaining_total_usd=None,
            expires_at=None,
        )
    
    def get_payment_history(self) -> List[PaymentEvent]:
        """Get list of payments made in this session."""
        return list(self._payments)
    
    def get_total_spent(self) -> float:
        """Get the total amount spent in this session."""
        return self._total_spent_usd

    # =========================================================================
    # Session Authorization Methods (for MixrPay Merchants)
    # =========================================================================

    def _get_session_auth_headers(self) -> Dict[str, str]:
        """
        Create the X-Session-Auth header for secure API authentication.
        Uses signature-based authentication - private key is NEVER transmitted.
        """
        payload = create_session_auth_payload(self._session_key)
        return {"X-Session-Auth": payload.to_header()}

    async def get_or_create_session(
        self,
        merchant_public_key: str,
        spending_limit_usd: float = 25.0,
        duration_days: int = 7,
    ) -> SessionAuthorization:
        """
        Get an existing session or create a new one with a MixrPay merchant.
        
        Args:
            merchant_public_key: The merchant's public key (pk_...)
            spending_limit_usd: Maximum spending limit for the session
            duration_days: Number of days the session is valid
            
        Returns:
            Active SessionAuthorization
        """
        self._logger.debug(f"get_or_create_session for merchant {merchant_public_key[:20]}...")

        # First, check for existing active session
        try:
            existing_session = await self.get_session_by_merchant(merchant_public_key)
            if existing_session and existing_session.status == "active":
                self._logger.debug(f"Found existing active session: {existing_session.id}")
                return existing_session
        except Exception:
            pass

        self._logger.info(f"Creating new session with merchant {merchant_public_key[:20]}...")

        auth_headers = self._get_session_auth_headers()

        # Step 1: Request session authorization
        authorize_response = await self._client.post(
            f"{self._base_url}/api/v2/session/authorize",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={
                "merchant_public_key": merchant_public_key,
                "spending_limit_usd": spending_limit_usd,
                "duration_days": duration_days,
            },
        )

        if not authorize_response.is_success:
            error = authorize_response.json() if authorize_response.content else {}
            raise MixrPayError(
                error.get("message") or error.get("error") or 
                f"Failed to create session: {authorize_response.status_code}"
            )

        authorize_data = authorize_response.json()
        session_id = authorize_data.get("session_id")
        message_to_sign = authorize_data.get("message_to_sign")

        if not session_id or not message_to_sign:
            raise MixrPayError("Invalid authorize response: missing session_id or message_to_sign")

        # Step 2: Sign the authorization message
        self._logger.debug("Signing session authorization message...")
        signature = self._session_key.sign_message(message_to_sign)

        # Step 3: Confirm the session with signature
        confirm_response = await self._client.post(
            f"{self._base_url}/api/v2/session/confirm",
            headers={"Content-Type": "application/json"},
            json={
                "session_id": session_id,
                "signature": signature,
                "wallet_address": self.wallet_address,
            },
        )

        if not confirm_response.is_success:
            error = confirm_response.json() if confirm_response.content else {}
            raise MixrPayError(
                error.get("message") or error.get("error") or 
                f"Failed to confirm session: {confirm_response.status_code}"
            )

        confirm_data = confirm_response.json()
        self._logger.info(f"Session created: {confirm_data.get('session', {}).get('id') or session_id}")

        return self._parse_session_response(confirm_data.get("session") or confirm_data)

    async def get_session_by_merchant(self, merchant_public_key: str) -> Optional[SessionAuthorization]:
        """
        Get session status for a specific merchant.
        
        Args:
            merchant_public_key: The merchant's public key
            
        Returns:
            SessionAuthorization or None if not found
        """
        self._logger.debug(f"get_session_by_merchant: {merchant_public_key}")

        auth_headers = self._get_session_auth_headers()
        response = await self._client.get(
            f"{self._base_url}/api/v2/session/status",
            params={"merchant_public_key": merchant_public_key},
            headers=auth_headers,
        )

        if response.status_code == 404:
            return None

        if not response.is_success:
            error = response.json() if response.content else {}
            raise MixrPayError(error.get("message") or f"Failed to get session: {response.status_code}")

        data = response.json()
        if not data.get("has_session"):
            return None
        return self._parse_session_response(data.get("session")) if data.get("session") else None

    async def list_sessions(self) -> List[SessionAuthorization]:
        """
        List all session authorizations for this wallet.
        
        Returns:
            List of SessionAuthorization objects
        """
        self._logger.debug("list_sessions")

        auth_headers = self._get_session_auth_headers()
        response = await self._client.get(
            f"{self._base_url}/api/v2/session/list",
            headers=auth_headers,
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            raise MixrPayError(error.get("message") or f"Failed to list sessions: {response.status_code}")

        data = response.json()
        return [self._parse_session_response(s) for s in data.get("sessions", [])]

    async def revoke_session(self, session_id: str) -> bool:
        """
        Revoke a session authorization.
        
        Args:
            session_id: The session ID to revoke
            
        Returns:
            True if revoked successfully
        """
        self._logger.debug(f"revoke_session: {session_id}")

        auth_headers = self._get_session_auth_headers()
        response = await self._client.post(
            f"{self._base_url}/api/v2/session/revoke",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={"session_id": session_id},
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            self._logger.error(f"Failed to revoke session: {error}")
            return False

        self._logger.info(f"Session {session_id} revoked")
        return True

    async def charge_session(
        self,
        session_id: str,
        amount_usd: float,
        feature: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ChargeResult:
        """
        Charge against an active session authorization.
        
        Args:
            session_id: The session ID to charge
            amount_usd: Amount to charge in USD
            feature: Feature slug for tracking
            idempotency_key: Unique key to prevent double-charging
            metadata: Arbitrary metadata to attach to the charge
            
        Returns:
            ChargeResult with charge details
        """
        self._logger.debug(f"charge_session: {session_id}, ${amount_usd}")

        auth_headers = self._get_session_auth_headers()
        response = await self._client.post(
            f"{self._base_url}/api/v2/charge",
            headers={**auth_headers, "Content-Type": "application/json"},
            json={
                "session_id": session_id,
                "price_usd": amount_usd,
                "feature": feature,
                "idempotency_key": idempotency_key,
                "metadata": metadata,
            },
        )

        if not response.is_success:
            error = response.json() if response.content else {}
            
            if response.status_code == 402:
                if error.get("error") == "session_limit_exceeded":
                    raise SpendingLimitExceededError(
                        "session",
                        error.get("session_limit_usd", error.get("sessionLimitUsd", 0)),
                        amount_usd,
                    )
                if error.get("error") == "insufficient_balance":
                    raise InsufficientBalanceError(
                        amount_usd,
                        error.get("available_usd", error.get("availableUsd", 0)),
                    )
            
            raise MixrPayError(error.get("message") or f"Charge failed: {response.status_code}")

        data = response.json()
        
        self._logger.payment(amount_usd, session_id, feature)

        return ChargeResult(
            success=True,
            charge_id=data.get("charge_id") or data.get("chargeId"),
            amount_usd=data.get("amount_usd") or data.get("amountUsd") or amount_usd,
            tx_hash=data.get("tx_hash") or data.get("txHash"),
            remaining_session_balance_usd=data.get("remaining_session_balance_usd") or data.get("remainingSessionBalanceUsd") or 0,
        )

    async def call_merchant_api(
        self,
        url: str,
        merchant_public_key: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        price_usd: Optional[float] = None,
        feature: Optional[str] = None,
        timeout: float = 30.0,
        spending_limit_usd: float = 25.0,
        duration_days: int = 7,
    ) -> httpx.Response:
        """
        Call a MixrPay merchant's API with automatic session management.
        
        Args:
            url: The API endpoint URL
            merchant_public_key: The merchant's public key (pk_...)
            method: HTTP method
            headers: Additional headers to include
            json: JSON body to send
            data: Form data to send
            price_usd: Expected price for this call (for validation)
            feature: Feature slug for tracking
            timeout: Request timeout in seconds
            spending_limit_usd: Spending limit if creating new session
            duration_days: Session duration if creating new session
            
        Returns:
            Response from the merchant API
        """
        self._logger.debug(f"call_merchant_api: {method} {url}")

        # Get or create session
        session = await self.get_or_create_session(
            merchant_public_key=merchant_public_key,
            spending_limit_usd=spending_limit_usd,
            duration_days=duration_days,
        )

        # Build request headers with session token
        request_headers = headers.copy() if headers else {}
        request_headers["X-Mixr-Session"] = session.id

        if price_usd is not None:
            request_headers["X-Expected-Price-Usd"] = str(price_usd)
        if feature:
            request_headers["X-Feature"] = feature

        # Make the request
        response = await self._client.request(
            method=method,
            url=url,
            headers=request_headers,
            json=json,
            data=data,
            timeout=timeout,
        )

        # If payment successful, log it
        if response.is_success and price_usd:
            self._logger.payment(price_usd, session.id, feature)

        return response

    def _parse_session_response(self, data: Dict[str, Any]) -> SessionAuthorization:
        """Parse API response into SessionAuthorization object."""
        return SessionAuthorization(
            id=data.get("id") or data.get("session_id") or data.get("sessionId") or "",
            merchant_id=data.get("merchant_id") or data.get("merchantId") or "",
            merchant_name=data.get("merchant_name") or data.get("merchantName") or "Unknown",
            status=data.get("status") or "active",
            spending_limit_usd=float(data.get("spending_limit_usd") or data.get("spendingLimitUsd") or data.get("spending_limit") or 0),
            amount_used_usd=float(data.get("amount_used_usd") or data.get("amountUsedUsd") or data.get("amount_used") or 0),
            remaining_limit_usd=float(
                data.get("remaining_usd") or data.get("remaining_limit_usd") or data.get("remainingLimitUsd") or data.get("remaining_limit") or
                (float(data.get("spending_limit_usd") or data.get("spendingLimitUsd") or 0) - float(data.get("amount_used_usd") or data.get("amountUsedUsd") or 0))
            ),
            expires_at=data.get("expires_at") or data.get("expiresAt") or "",
            created_at=data.get("created_at") or data.get("createdAt") or "",
        )
