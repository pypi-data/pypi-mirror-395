"""
Session key handling for MixrPay SDK.

Session keys are derived private keys with on-chain spending limits that enable
AI agents to sign USDC transferWithAuthorization transactions autonomously.
"""

import re
import time
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any
from eth_account import Account
from eth_account.messages import encode_defunct

from .exceptions import InvalidSessionKeyError


# USDC Contract Addresses
USDC_ADDRESSES = {
    8453: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",      # Base Mainnet
    84532: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",     # Base Sepolia
}

# USDC EIP-712 Domain
USDC_EIP712_DOMAIN = {
    "name": "USD Coin",
    "version": "2",
}


@dataclass
class SessionKey:
    """
    Represents a session key for signing x402 payments.
    
    The session key format is: sk_live_{64_hex_chars} or sk_test_{64_hex_chars}
    """
    private_key: bytes
    address: str
    is_test: bool
    
    @classmethod
    def from_string(cls, session_key: str) -> "SessionKey":
        """
        Parse a session key string into a SessionKey object.
        
        Args:
            session_key: Session key in format sk_live_... or sk_test_...
            
        Returns:
            SessionKey object
            
        Raises:
            InvalidSessionKeyError: If the session key format is invalid
        """
        # Validate format
        pattern = r"^sk_(live|test)_([a-fA-F0-9]{64})$"
        match = re.match(pattern, session_key)
        
        if not match:
            raise InvalidSessionKeyError(
                "Session key must be in format sk_live_{64_hex} or sk_test_{64_hex}"
            )
        
        env = match.group(1)
        hex_key = match.group(2)
        
        try:
            private_key = bytes.fromhex(hex_key)
            account = Account.from_key(private_key)
            
            return cls(
                private_key=private_key,
                address=account.address,
                is_test=(env == "test"),
            )
        except Exception as e:
            raise InvalidSessionKeyError(f"Failed to decode session key: {e}")
    
    def sign_typed_data(self, typed_data: dict) -> str:
        """
        Sign EIP-712 typed data with this session key.
        
        Args:
            typed_data: EIP-712 typed data structure
            
        Returns:
            Hex-encoded signature
        """
        account = Account.from_key(self.private_key)
        signed = account.sign_typed_data(
            typed_data["domain"],
            typed_data["types"],
            typed_data["message"],
        )
        return signed.signature.hex()

    def sign_message(self, message: str) -> str:
        """
        Sign a plain message (EIP-191 personal sign).
        
        Args:
            message: Message to sign
            
        Returns:
            Hex-encoded signature (with 0x prefix)
        """
        account = Account.from_key(self.private_key)
        msg = encode_defunct(text=message)
        signed = account.sign_message(msg)
        return "0x" + signed.signature.hex()


# =============================================================================
# Session Auth (Signature-Based Authentication)
# =============================================================================

@dataclass
class SessionAuthPayload:
    """
    Payload for X-Session-Auth header.
    This is sent to the server to prove ownership of a session key
    WITHOUT transmitting the private key.
    """
    address: str
    """The session key's public address (0x...)"""
    
    timestamp: int
    """Unix timestamp in milliseconds when the signature was created"""
    
    signature: str
    """The signature of the auth message"""
    
    def to_header(self) -> str:
        """Convert to JSON string for X-Session-Auth header."""
        return json.dumps({
            "address": self.address,
            "timestamp": self.timestamp,
            "signature": self.signature,
        })


def build_session_auth_message(timestamp: int, address: str) -> str:
    """
    Build the message that should be signed for session authentication.
    Format: "MixrPay:{timestamp}:{address}"
    
    This must match the server-side buildAuthMessage function.
    """
    return f"MixrPay:{timestamp}:{address.lower()}"


def create_session_auth_payload(session_key: SessionKey) -> SessionAuthPayload:
    """
    Create a signed session auth payload for API authentication.
    
    This creates a signature proving ownership of the session key
    without transmitting the private key over the network.
    
    Args:
        session_key: The session key to authenticate with
        
    Returns:
        SessionAuthPayload to be sent as X-Session-Auth header
    
    Example:
        >>> payload = create_session_auth_payload(session_key)
        >>> headers = {"X-Session-Auth": payload.to_header()}
        >>> response = requests.get(url, headers=headers)
    """
    timestamp = int(time.time() * 1000)  # Milliseconds
    message = build_session_auth_message(timestamp, session_key.address)
    signature = session_key.sign_message(message)
    
    return SessionAuthPayload(
        address=session_key.address,
        timestamp=timestamp,
        signature=signature,
    )


# =============================================================================
# Transfer Authorization
# =============================================================================

def build_transfer_authorization_typed_data(
    from_address: str,
    to_address: str,
    value: int,
    valid_after: int,
    valid_before: int,
    nonce: bytes,
    chain_id: int,
) -> dict:
    """
    Build EIP-712 typed data for USDC transferWithAuthorization (EIP-3009).
    
    This creates the typed data structure that must be signed by the session key
    to authorize a USDC transfer.
    
    Args:
        from_address: Address sending USDC (the wallet address)
        to_address: Address receiving USDC (the merchant/facilitator)
        value: Amount in USDC minor units (6 decimals)
        valid_after: Unix timestamp after which the authorization is valid
        valid_before: Unix timestamp before which the authorization is valid
        nonce: Unique 32-byte nonce for this authorization
        chain_id: Chain ID (8453 for Base, 84532 for Base Sepolia)
        
    Returns:
        EIP-712 typed data dictionary
    """
    usdc_address = USDC_ADDRESSES.get(chain_id)
    if not usdc_address:
        raise ValueError(f"USDC not supported on chain {chain_id}")
    
    return {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ],
        },
        "primaryType": "TransferWithAuthorization",
        "domain": {
            **USDC_EIP712_DOMAIN,
            "chainId": chain_id,
            "verifyingContract": usdc_address,
        },
        "message": {
            "from": from_address,
            "to": to_address,
            "value": value,
            "validAfter": valid_after,
            "validBefore": valid_before,
            "nonce": nonce.hex() if isinstance(nonce, bytes) else nonce,
        },
    }

