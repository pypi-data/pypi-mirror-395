"""
x402 Protocol handling for MixrPay SDK.

The x402 protocol enables HTTP-native payments. When a server returns a 402 Payment
Required response, the client can automatically fulfill the payment and retry the request.

Flow:
1. Client makes HTTP request
2. Server returns 402 with payment requirements in headers/body
3. Client signs a USDC transferWithAuthorization
4. Client retries request with X-PAYMENT header
5. Server/facilitator processes payment and returns response
"""

import json
import base64
import time
import secrets
from dataclasses import dataclass
from typing import Optional, Any
import httpx

from .session_key import SessionKey, build_transfer_authorization_typed_data
from .exceptions import X402ProtocolError


@dataclass
class PaymentRequirements:
    """Parsed payment requirements from a 402 response."""
    
    recipient: str              # Address to pay
    amount: int                 # Amount in USDC minor units (6 decimals)
    currency: str               # Currency code (e.g., "USDC")
    chain_id: int               # Chain ID (e.g., 8453 for Base)
    facilitator_url: str        # Where to submit payment
    nonce: str                  # Unique nonce for this payment
    expires_at: int             # Unix timestamp when payment expires
    description: Optional[str]  # Optional description of what's being paid for
    
    @property
    def amount_usd(self) -> float:
        """Amount in USD (USDC has 6 decimals)."""
        return self.amount / 1_000_000
    
    def is_expired(self) -> bool:
        """Check if the payment requirements have expired."""
        return time.time() > self.expires_at


def parse_402_response(response: httpx.Response) -> PaymentRequirements:
    """
    Parse payment requirements from a 402 response.
    
    The 402 response can include payment requirements in:
    1. X-Payment-Required header (JSON)
    2. WWW-Authenticate header (per x402 spec)
    3. Response body (JSON)
    
    Args:
        response: The HTTP response with status 402
        
    Returns:
        PaymentRequirements parsed from the response
        
    Raises:
        X402ProtocolError: If payment requirements cannot be parsed
    """
    payment_data = None
    
    # Try X-Payment-Required header first
    if "X-Payment-Required" in response.headers:
        try:
            payment_data = json.loads(response.headers["X-Payment-Required"])
        except json.JSONDecodeError:
            pass
    
    # Try WWW-Authenticate header (x402 standard)
    if payment_data is None and "WWW-Authenticate" in response.headers:
        auth_header = response.headers["WWW-Authenticate"]
        if auth_header.startswith("X-402 "):
            try:
                # Format: X-402 base64_encoded_json
                encoded = auth_header[6:]  # Remove "X-402 " prefix
                payment_data = json.loads(base64.b64decode(encoded))
            except (json.JSONDecodeError, ValueError):
                pass
    
    # Try response body
    if payment_data is None:
        try:
            payment_data = response.json()
        except (json.JSONDecodeError, ValueError):
            pass
    
    if payment_data is None:
        raise X402ProtocolError("Could not parse payment requirements from 402 response")
    
    # Extract and validate required fields
    try:
        return PaymentRequirements(
            recipient=payment_data["recipient"],
            amount=int(payment_data["amount"]),
            currency=payment_data.get("currency", "USDC"),
            chain_id=int(payment_data.get("chainId", payment_data.get("chain_id", 8453))),
            facilitator_url=payment_data.get(
                "facilitatorUrl", 
                payment_data.get("facilitator_url", "https://x402.org/facilitator")
            ),
            nonce=payment_data.get("nonce", secrets.token_hex(32)),
            expires_at=int(payment_data.get("expiresAt", payment_data.get("expires_at", time.time() + 300))),
            description=payment_data.get("description"),
        )
    except KeyError as e:
        raise X402ProtocolError(f"Missing required field in payment requirements: {e}")


def build_x_payment_header(
    requirements: PaymentRequirements,
    session_key: SessionKey,
    wallet_address: str,
) -> str:
    """
    Build the X-PAYMENT header value for a payment request.
    
    This creates an EIP-3009 transferWithAuthorization, signs it with the session key,
    and encodes it for the X-PAYMENT header.
    
    Args:
        requirements: Payment requirements from the 402 response
        session_key: Session key to sign the payment
        wallet_address: The smart wallet address that holds USDC
        
    Returns:
        Base64-encoded JSON string for the X-PAYMENT header
    """
    # Generate nonce as bytes
    nonce = bytes.fromhex(requirements.nonce) if len(requirements.nonce) == 64 else secrets.token_bytes(32)
    
    # Current time for validity window
    now = int(time.time())
    valid_after = now - 60  # Valid from 1 minute ago (clock skew tolerance)
    valid_before = requirements.expires_at
    
    # Build EIP-712 typed data for transferWithAuthorization
    typed_data = build_transfer_authorization_typed_data(
        from_address=wallet_address,
        to_address=requirements.recipient,
        value=requirements.amount,
        valid_after=valid_after,
        valid_before=valid_before,
        nonce=nonce,
        chain_id=requirements.chain_id,
    )
    
    # Sign with session key
    signature = session_key.sign_typed_data(typed_data)
    
    # Build payment payload
    payment_payload = {
        "x402Version": 1,
        "scheme": "exact",
        "network": "base" if requirements.chain_id == 8453 else "base-sepolia",
        "payload": {
            "signature": f"0x{signature}" if not signature.startswith("0x") else signature,
            "authorization": {
                "from": wallet_address,
                "to": requirements.recipient,
                "value": str(requirements.amount),
                "validAfter": str(valid_after),
                "validBefore": str(valid_before),
                "nonce": f"0x{nonce.hex()}",
            },
        },
    }
    
    # Base64 encode
    return base64.b64encode(json.dumps(payment_payload).encode()).decode()


def validate_payment_amount(
    amount_usd: float,
    max_payment_usd: Optional[float] = None,
) -> None:
    """
    Validate that a payment amount is within acceptable limits.
    
    Args:
        amount_usd: Payment amount in USD
        max_payment_usd: Optional client-side maximum per payment
        
    Raises:
        X402ProtocolError: If the amount exceeds limits
    """
    if amount_usd <= 0:
        raise X402ProtocolError(f"Invalid payment amount: ${amount_usd:.2f}")
    
    if max_payment_usd is not None and amount_usd > max_payment_usd:
        raise X402ProtocolError(
            f"Payment amount ${amount_usd:.2f} exceeds client limit ${max_payment_usd:.2f}"
        )

