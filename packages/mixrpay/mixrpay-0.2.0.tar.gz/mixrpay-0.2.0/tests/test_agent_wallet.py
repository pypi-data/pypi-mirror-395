"""
Tests for MixrPay Agent SDK.
"""

import json
import base64
import pytest
from unittest.mock import Mock, patch, MagicMock
import httpx

from mixrpay import (
    AgentWallet,
    MixrPayError,
    InsufficientBalanceError,
    SessionKeyExpiredError,
    SpendingLimitExceededError,
    PaymentFailedError,
    InvalidSessionKeyError,
)
from mixrpay.session_key import SessionKey, build_transfer_authorization_typed_data
from mixrpay.x402 import parse_402_response, build_x_payment_header, PaymentRequirements


# =============================================================================
# Test Fixtures
# =============================================================================

# Valid test session key (32 random bytes as hex = 64 chars)
VALID_SESSION_KEY = "sk_test_" + "a" * 64
VALID_LIVE_KEY = "sk_live_" + "b" * 64

# Mock 402 response data
MOCK_PAYMENT_REQUIREMENTS = {
    "recipient": "0x1234567890123456789012345678901234567890",
    "amount": "100000",  # $0.10 USDC
    "currency": "USDC",
    "chainId": 84532,  # Base Sepolia
    "nonce": "c" * 64,
    "expiresAt": 9999999999,
    "description": "API query",
}


@pytest.fixture
def session_key():
    """Create a test session key."""
    return SessionKey.from_string(VALID_SESSION_KEY)


@pytest.fixture
def wallet():
    """Create a test wallet."""
    return AgentWallet(
        session_key=VALID_SESSION_KEY,
        max_payment_usd=10.0,
    )


# =============================================================================
# Session Key Tests
# =============================================================================

class TestSessionKey:
    """Tests for SessionKey parsing and signing."""
    
    def test_parse_valid_test_key(self):
        """Test parsing a valid test session key."""
        key = SessionKey.from_string(VALID_SESSION_KEY)
        assert key.is_test is True
        assert len(key.private_key) == 32
        assert key.address.startswith("0x")
    
    def test_parse_valid_live_key(self):
        """Test parsing a valid live session key."""
        key = SessionKey.from_string(VALID_LIVE_KEY)
        assert key.is_test is False
        assert len(key.private_key) == 32
    
    def test_invalid_prefix(self):
        """Test that invalid prefix raises error."""
        with pytest.raises(InvalidSessionKeyError):
            SessionKey.from_string("sk_invalid_" + "a" * 64)
    
    def test_invalid_length(self):
        """Test that invalid length raises error."""
        with pytest.raises(InvalidSessionKeyError):
            SessionKey.from_string("sk_test_" + "a" * 32)  # Too short
    
    def test_invalid_hex(self):
        """Test that invalid hex raises error."""
        with pytest.raises(InvalidSessionKeyError):
            SessionKey.from_string("sk_test_" + "g" * 64)  # Invalid hex char
    
    def test_sign_typed_data(self, session_key):
        """Test signing EIP-712 typed data."""
        typed_data = build_transfer_authorization_typed_data(
            from_address="0x1111111111111111111111111111111111111111",
            to_address="0x2222222222222222222222222222222222222222",
            value=100000,
            valid_after=0,
            valid_before=9999999999,
            nonce=bytes.fromhex("c" * 64),
            chain_id=84532,
        )
        
        signature = session_key.sign_typed_data(typed_data)
        
        assert signature is not None
        assert len(signature) > 0
        # Signature should be hex
        assert all(c in "0123456789abcdef" for c in signature.lower())


# =============================================================================
# x402 Protocol Tests
# =============================================================================

class TestX402Protocol:
    """Tests for x402 protocol handling."""
    
    def test_parse_402_from_header(self):
        """Test parsing 402 response from X-Payment-Required header."""
        response = Mock(spec=httpx.Response)
        response.headers = {
            "X-Payment-Required": json.dumps(MOCK_PAYMENT_REQUIREMENTS)
        }
        
        requirements = parse_402_response(response)
        
        assert requirements.recipient == MOCK_PAYMENT_REQUIREMENTS["recipient"]
        assert requirements.amount == 100000
        assert requirements.currency == "USDC"
        assert requirements.chain_id == 84532
    
    def test_parse_402_from_www_authenticate(self):
        """Test parsing 402 response from WWW-Authenticate header."""
        encoded = base64.b64encode(json.dumps(MOCK_PAYMENT_REQUIREMENTS).encode()).decode()
        
        response = Mock(spec=httpx.Response)
        response.headers = {
            "WWW-Authenticate": f"X-402 {encoded}"
        }
        
        requirements = parse_402_response(response)
        
        assert requirements.recipient == MOCK_PAYMENT_REQUIREMENTS["recipient"]
        assert requirements.amount == 100000
    
    def test_parse_402_from_body(self):
        """Test parsing 402 response from body."""
        response = Mock(spec=httpx.Response)
        response.headers = {}
        response.json.return_value = MOCK_PAYMENT_REQUIREMENTS
        
        requirements = parse_402_response(response)
        
        assert requirements.recipient == MOCK_PAYMENT_REQUIREMENTS["recipient"]
    
    def test_build_x_payment_header(self, session_key):
        """Test building X-PAYMENT header."""
        requirements = PaymentRequirements(
            recipient="0x1234567890123456789012345678901234567890",
            amount=100000,
            currency="USDC",
            chain_id=84532,
            facilitator_url="https://x402.org/facilitator",
            nonce="c" * 64,
            expires_at=9999999999,
            description="Test payment",
        )
        
        header = build_x_payment_header(
            requirements=requirements,
            session_key=session_key,
            wallet_address=session_key.address,
        )
        
        # Should be base64 encoded
        decoded = json.loads(base64.b64decode(header))
        
        assert decoded["x402Version"] == 1
        assert decoded["scheme"] == "exact"
        assert "payload" in decoded
        assert "signature" in decoded["payload"]
        assert "authorization" in decoded["payload"]


# =============================================================================
# AgentWallet Tests
# =============================================================================

class TestAgentWallet:
    """Tests for AgentWallet class."""
    
    def test_init_with_valid_key(self):
        """Test initializing wallet with valid session key."""
        wallet = AgentWallet(session_key=VALID_SESSION_KEY)
        assert wallet.is_testnet is True
        assert wallet.wallet_address.startswith("0x")
    
    def test_init_with_invalid_key(self):
        """Test that invalid session key raises error."""
        with pytest.raises(InvalidSessionKeyError):
            AgentWallet(session_key="invalid_key")
    
    def test_context_manager(self):
        """Test using wallet as context manager."""
        with AgentWallet(session_key=VALID_SESSION_KEY) as wallet:
            assert wallet is not None
        # Client should be closed after exiting context
    
    def test_max_payment_limit(self, wallet):
        """Test client-side payment limit."""
        assert wallet._max_payment_usd == 10.0
    
    @patch.object(httpx.Client, "request")
    def test_fetch_success_no_payment(self, mock_request, wallet):
        """Test fetch when no payment is required."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_request.return_value = mock_response
        
        response = wallet.fetch("https://api.example.com/free")
        
        assert response.status_code == 200
        assert len(wallet.get_payment_history()) == 0
    
    @patch.object(httpx.Client, "request")
    def test_fetch_with_402_payment(self, mock_request, wallet):
        """Test fetch handling 402 and retrying with payment."""
        # First request returns 402
        mock_402_response = Mock(spec=httpx.Response)
        mock_402_response.status_code = 402
        mock_402_response.headers = {
            "X-Payment-Required": json.dumps(MOCK_PAYMENT_REQUIREMENTS)
        }
        
        # Second request (with payment) succeeds
        mock_success_response = Mock(spec=httpx.Response)
        mock_success_response.status_code = 200
        mock_success_response.headers = {"X-Payment-TxHash": "0xabc123"}
        mock_success_response.json.return_value = {"result": "paid"}
        
        mock_request.side_effect = [mock_402_response, mock_success_response]
        
        response = wallet.fetch("https://api.example.com/paid")
        
        assert response.status_code == 200
        assert mock_request.call_count == 2
        
        # Check payment was tracked
        history = wallet.get_payment_history()
        assert len(history) == 1
        assert history[0].amount_usd == 0.10  # $0.10
        assert history[0].tx_hash == "0xabc123"
    
    @patch.object(httpx.Client, "request")
    def test_fetch_payment_callback(self, mock_request, wallet):
        """Test that payment callback is called."""
        callback_called = []
        
        wallet_with_callback = AgentWallet(
            session_key=VALID_SESSION_KEY,
            on_payment=lambda p: callback_called.append(p),
        )
        
        mock_402_response = Mock(spec=httpx.Response)
        mock_402_response.status_code = 402
        mock_402_response.headers = {
            "X-Payment-Required": json.dumps(MOCK_PAYMENT_REQUIREMENTS)
        }
        
        mock_success_response = Mock(spec=httpx.Response)
        mock_success_response.status_code = 200
        mock_success_response.headers = {}
        
        mock_request.side_effect = [mock_402_response, mock_success_response]
        
        wallet_with_callback.fetch("https://api.example.com/paid")
        
        assert len(callback_called) == 1
        assert callback_called[0].amount_usd == 0.10
    
    def test_get_spending_stats(self, wallet):
        """Test getting spending stats."""
        stats = wallet.get_spending_stats()
        
        assert stats.total_spent_usd == 0.0
        assert stats.tx_count == 0
    
    def test_shorthand_methods(self, wallet):
        """Test GET/POST/PUT/DELETE shorthand methods exist."""
        assert hasattr(wallet, "get")
        assert hasattr(wallet, "post")
        assert hasattr(wallet, "put")
        assert hasattr(wallet, "delete")


# =============================================================================
# Exception Tests
# =============================================================================

class TestExceptions:
    """Tests for custom exceptions."""
    
    def test_insufficient_balance_error(self):
        """Test InsufficientBalanceError."""
        error = InsufficientBalanceError(required=10.0, available=5.0)
        assert error.required == 10.0
        assert error.available == 5.0
        assert "10.00" in str(error)
        assert "5.00" in str(error)
    
    def test_session_key_expired_error(self):
        """Test SessionKeyExpiredError."""
        error = SessionKeyExpiredError(expired_at="2024-01-01T00:00:00Z")
        assert error.expired_at == "2024-01-01T00:00:00Z"
        assert "expired" in str(error).lower()
    
    def test_spending_limit_exceeded_error(self):
        """Test SpendingLimitExceededError."""
        error = SpendingLimitExceededError(
            limit_type="daily",
            limit=100.0,
            attempted=150.0,
        )
        assert error.limit_type == "daily"
        assert error.limit == 100.0
        assert error.attempted == 150.0
    
    def test_payment_failed_error(self):
        """Test PaymentFailedError."""
        error = PaymentFailedError(reason="Transaction reverted")
        assert error.reason == "Transaction reverted"
        
        error_with_hash = PaymentFailedError(
            reason="Failed",
            tx_hash="0xabc123"
        )
        assert "0xabc123" in str(error_with_hash)


# =============================================================================
# Integration Tests (require mocking)
# =============================================================================

class TestIntegration:
    """Integration tests with mocked external services."""
    
    @patch.object(httpx.Client, "request")
    def test_full_payment_flow(self, mock_request):
        """Test complete payment flow from 402 to success."""
        wallet = AgentWallet(
            session_key=VALID_SESSION_KEY,
            max_payment_usd=1.0,
        )
        
        # Mock 402 response
        mock_402 = Mock(spec=httpx.Response)
        mock_402.status_code = 402
        mock_402.headers = {
            "X-Payment-Required": json.dumps({
                "recipient": "0x" + "1" * 40,
                "amount": "50000",  # $0.05
                "chainId": 84532,
                "nonce": "d" * 64,
                "expiresAt": 9999999999,
            })
        }
        
        # Mock success response
        mock_success = Mock(spec=httpx.Response)
        mock_success.status_code = 200
        mock_success.headers = {"X-Payment-TxHash": "0xdef456"}
        mock_success.json.return_value = {"data": "premium content"}
        
        mock_request.side_effect = [mock_402, mock_success]
        
        # Make request
        response = wallet.fetch(
            "https://api.premium.com/content",
            method="POST",
            json={"query": "test"},
        )
        
        # Verify
        assert response.status_code == 200
        assert response.json()["data"] == "premium content"
        
        # Check second request had X-PAYMENT header
        second_call = mock_request.call_args_list[1]
        assert "X-PAYMENT" in second_call.kwargs["headers"]
        
        # Verify payment tracking
        stats = wallet.get_spending_stats()
        assert stats.total_spent_usd == 0.05
        assert stats.tx_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

