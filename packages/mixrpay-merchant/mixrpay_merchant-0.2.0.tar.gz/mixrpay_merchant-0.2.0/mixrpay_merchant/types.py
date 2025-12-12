"""
MixrPay Merchant SDK - Type definitions
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable, Awaitable, Union
from datetime import datetime


@dataclass
class X402PaymentResult:
    """Result of x402 payment verification."""
    
    valid: bool
    """Whether the payment is valid."""
    
    error: Optional[str] = None
    """Error message if invalid."""
    
    payer: Optional[str] = None
    """Address that paid (if valid)."""
    
    amount: Optional[float] = None
    """Amount in USDC (major units, e.g., 0.05)."""
    
    amount_minor: Optional[int] = None
    """Amount in USDC minor units (e.g., 50000)."""
    
    tx_hash: Optional[str] = None
    """Settlement transaction hash."""
    
    settled_at: Optional[datetime] = None
    """When the payment was settled."""
    
    nonce: Optional[str] = None
    """The nonce used for this payment."""


@dataclass
class X402PaymentRequired:
    """Payment requirements returned in 402 response."""
    
    recipient: str
    """Recipient wallet address."""
    
    amount: str
    """Amount in USDC minor units (6 decimals) as string."""
    
    currency: str = "USDC"
    """Currency code."""
    
    chain_id: int = 8453
    """Chain ID (8453 for Base)."""
    
    facilitator: str = "https://x402.org/facilitator"
    """Facilitator URL."""
    
    nonce: str = ""
    """Unique nonce for this payment request."""
    
    expires_at: int = 0
    """Unix timestamp when payment requirements expire."""
    
    description: Optional[str] = None
    """Description of the payment."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        result = {
            "recipient": self.recipient,
            "amount": self.amount,
            "currency": self.currency,
            "chainId": self.chain_id,
            "facilitator": self.facilitator,
            "nonce": self.nonce,
            "expiresAt": self.expires_at,
        }
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class X402Options:
    """Configuration options for x402 middleware."""
    
    price: Optional[float] = None
    """Fixed price in USD (e.g., 0.05 for 5 cents)."""
    
    recipient: Optional[str] = None
    """Your wallet address (defaults to MIXRPAY_MERCHANT_ADDRESS env var)."""
    
    chain_id: int = 8453
    """Chain ID (default: 8453 for Base)."""
    
    facilitator: str = "https://x402.org/facilitator"
    """Facilitator URL for payment settlement."""
    
    description: Optional[str] = None
    """Description shown to payer."""
    
    test_mode: bool = False
    """Test mode - skips on-chain settlement."""
    
    get_price: Optional[Callable[..., Union[float, Awaitable[float]]]] = None
    """Dynamic pricing function."""
    
    on_payment: Optional[Callable[[X402PaymentResult], Union[None, Awaitable[None]]]] = None
    """Callback after successful payment."""
    
    skip: Optional[Callable[..., Union[bool, Awaitable[bool]]]] = None
    """Function to determine if payment should be skipped."""


@dataclass 
class VerifyOptions:
    """Options for payment verification."""
    
    expected_amount: int
    """Expected amount in USDC minor units."""
    
    expected_recipient: str
    """Expected recipient address."""
    
    chain_id: int = 8453
    """Chain ID (default: 8453 for Base)."""
    
    facilitator: str = "https://x402.org/facilitator"
    """Facilitator URL."""
    
    skip_settlement: bool = False
    """Skip on-chain settlement (for testing)."""


# =============================================================================
# Unified MixrPay Payment Types (Session + Widget + x402)
# =============================================================================

from typing import Literal

PaymentMethod = Literal["session", "widget", "x402"]
"""Payment method used for the transaction."""


@dataclass
class MixrPayPaymentResult:
    """
    Unified payment result from any payment method.
    
    This result type is returned by the `mixrpay()` middleware and
    contains information about the payment regardless of the method used.
    """
    
    valid: bool
    """Whether the payment is valid."""
    
    method: PaymentMethod
    """Payment method used: 'session', 'widget', or 'x402'."""
    
    error: Optional[str] = None
    """Error message if invalid."""
    
    payer: Optional[str] = None
    """Address that paid."""
    
    amount_usd: Optional[float] = None
    """Amount in USD."""
    
    tx_hash: Optional[str] = None
    """Settlement transaction hash (if applicable)."""
    
    charge_id: Optional[str] = None
    """Charge ID (for session/widget payments)."""
    
    session_id: Optional[str] = None
    """Session ID (if session payment)."""
    
    feature: Optional[str] = None
    """Feature slug (if provided)."""
    
    settled_at: Optional[datetime] = None
    """When the payment was settled."""
    
    receipt: Optional[str] = None
    """JWT payment receipt (for x402 with receipt mode)."""
    
    x402_result: Optional[X402PaymentResult] = None
    """Raw x402 payment result (if x402 method)."""
    
    remaining_session_balance_usd: Optional[float] = None
    """Remaining session balance after charge (for session payments)."""


@dataclass
class MixrPayOptions:
    """
    Configuration options for the unified mixrpay() middleware.
    
    Accepts payments from Session Authorizations, Widget, and x402 Protocol.
    """
    
    price_usd: Optional[float] = None
    """Price in USD (e.g., 0.05 for 5 cents)."""
    
    get_price: Optional[Callable[..., Union[float, Awaitable[float]]]] = None
    """Custom function to determine price dynamically."""
    
    feature: Optional[str] = None
    """Feature slug for tracking/analytics (used for session and widget payments)."""
    
    description: Optional[str] = None
    """Description of what the payment is for."""
    
    skip: Optional[Callable[..., Union[bool, Awaitable[bool]]]] = None
    """Function to determine if payment should be skipped (return True to skip)."""
    
    test_mode: bool = False
    """Allow test payments (for development)."""
    
    on_payment: Optional[Callable[["MixrPayPaymentResult"], Union[None, Awaitable[None]]]] = None
    """Called after successful payment verification."""
    
    # x402-specific options
    recipient: Optional[str] = None
    """Your merchant wallet address to receive x402 payments."""
    
    chain_id: int = 8453
    """Chain ID for x402 (default: 8453 for Base)."""
    
    facilitator: str = "https://x402.org/facilitator"
    """Facilitator URL for x402 payment settlement."""
    
    # API configuration
    mixrpay_api_url: Optional[str] = None
    """MixrPay API URL (defaults to MIXRPAY_API_URL env or https://mixrpay.com)."""

