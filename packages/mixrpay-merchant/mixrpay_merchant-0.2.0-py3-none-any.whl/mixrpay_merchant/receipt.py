"""
MixrPay Merchant SDK - Payment Receipt Verification

Verify JWT payment receipts issued by MixrPay after successful x402 payments.

Example:
    from mixrpay_merchant import verify_payment_receipt

    receipt = request.headers.get("X-Payment-Receipt")
    payment = verify_payment_receipt(receipt)

    print(f"Payment received: ${payment.amount_usd} from {payment.payer}")
    print(f"Transaction: {payment.tx_hash}")
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import httpx
import jwt
from jwt import PyJWKClient

# =============================================================================
# Constants
# =============================================================================

DEFAULT_JWKS_URL = os.environ.get("MIXRPAY_JWKS_URL", "https://mixrpay.com/.well-known/jwks")
JWKS_CACHE_TTL_SECONDS = 3600  # 1 hour

# =============================================================================
# Types
# =============================================================================


@dataclass
class PaymentReceipt:
    """Verified payment receipt from MixrPay."""

    payment_id: str
    """Unique payment ID."""

    amount: str
    """Amount in USDC minor units (6 decimals) as string."""

    amount_usd: float
    """Amount in USD."""

    payer: str
    """Payer wallet address."""

    recipient: str
    """Recipient wallet address."""

    chain_id: int
    """Blockchain chain ID."""

    tx_hash: str
    """Settlement transaction hash."""

    settled_at: str
    """When the payment was settled (ISO string)."""

    issued_at: Optional[datetime] = None
    """When the receipt was issued."""

    expires_at: Optional[datetime] = None
    """When the receipt expires."""


class ReceiptVerificationError(Exception):
    """Raised when receipt verification fails."""

    pass


class ReceiptExpiredError(ReceiptVerificationError):
    """Raised when a receipt has expired."""

    pass


class InvalidReceiptSignatureError(ReceiptVerificationError):
    """Raised when a receipt has an invalid signature."""

    pass


# =============================================================================
# JWKS Cache
# =============================================================================


class _JWKSCache:
    """Simple JWKS cache with TTL."""

    def __init__(self):
        self._cache: dict[str, tuple[PyJWKClient, float]] = {}

    def get_client(self, jwks_url: str) -> PyJWKClient:
        """Get or create a PyJWKClient for the given JWKS URL."""
        cached = self._cache.get(jwks_url)

        if cached:
            client, fetched_at = cached
            if time.time() - fetched_at < JWKS_CACHE_TTL_SECONDS:
                return client

        # Create new client
        client = PyJWKClient(jwks_url, cache_keys=True)
        self._cache[jwks_url] = (client, time.time())
        return client

    def clear(self):
        """Clear the cache."""
        self._cache.clear()


_jwks_cache = _JWKSCache()


# =============================================================================
# Receipt Verification
# =============================================================================


def verify_payment_receipt(
    receipt: str,
    jwks_url: Optional[str] = None,
    issuer: Optional[str] = None,
) -> PaymentReceipt:
    """
    Verify a JWT payment receipt from MixrPay.

    This function:
    1. Fetches the JWKS from MixrPay (cached for 1 hour)
    2. Verifies the JWT signature using RS256
    3. Validates standard JWT claims (exp, iat)
    4. Returns the typed payment receipt

    Args:
        receipt: The JWT receipt string from X-Payment-Receipt header
        jwks_url: Custom JWKS URL (default: MixrPay production JWKS)
        issuer: Expected issuer (for additional validation)

    Returns:
        PaymentReceipt: Verified payment receipt

    Raises:
        ReceiptVerificationError: If verification fails
        ReceiptExpiredError: If the receipt has expired
        InvalidReceiptSignatureError: If the signature is invalid

    Example:
        Basic usage:
            payment = verify_payment_receipt(receipt)

        With custom JWKS URL (for testing or self-hosted):
            payment = verify_payment_receipt(
                receipt,
                jwks_url="https://your-mixrpay.com/.well-known/jwks"
            )
    """
    url = jwks_url or DEFAULT_JWKS_URL

    try:
        # Get JWKS client
        jwks_client = _jwks_cache.get_client(url)

        # Get signing key from JWKS
        signing_key = jwks_client.get_signing_key_from_jwt(receipt)

        # Build verification options
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_iat": True,
            "require": ["exp", "iat", "paymentId", "amount", "payer", "recipient"],
        }

        # Decode and verify
        payload = jwt.decode(
            receipt,
            signing_key.key,
            algorithms=["RS256"],
            issuer=issuer,
            options=options,
        )

        # Build receipt object
        return PaymentReceipt(
            payment_id=payload["paymentId"],
            amount=str(payload["amount"]),
            amount_usd=float(payload["amountUsd"]),
            payer=payload["payer"],
            recipient=payload["recipient"],
            chain_id=int(payload["chainId"]),
            tx_hash=payload["txHash"],
            settled_at=payload["settledAt"],
            issued_at=datetime.fromtimestamp(payload["iat"]) if "iat" in payload else None,
            expires_at=datetime.fromtimestamp(payload["exp"]) if "exp" in payload else None,
        )

    except jwt.ExpiredSignatureError as e:
        raise ReceiptExpiredError("Payment receipt has expired") from e

    except jwt.InvalidSignatureError as e:
        raise InvalidReceiptSignatureError("Invalid receipt signature") from e

    except jwt.DecodeError as e:
        raise ReceiptVerificationError(f"Failed to decode receipt: {e}") from e

    except jwt.InvalidTokenError as e:
        raise ReceiptVerificationError(f"Invalid receipt: {e}") from e

    except Exception as e:
        raise ReceiptVerificationError(f"Receipt verification failed: {e}") from e


def parse_payment_receipt(receipt: str) -> PaymentReceipt:
    """
    Parse a JWT payment receipt without verification.

    WARNING: This does NOT verify the signature. Use only for debugging
    or when you've already verified the receipt elsewhere.

    Args:
        receipt: The JWT receipt string

    Returns:
        PaymentReceipt: Decoded payload (unverified)
    """
    # Decode without verification
    payload = jwt.decode(receipt, options={"verify_signature": False})

    return PaymentReceipt(
        payment_id=payload.get("paymentId", ""),
        amount=str(payload.get("amount", "0")),
        amount_usd=float(payload.get("amountUsd", 0)),
        payer=payload.get("payer", ""),
        recipient=payload.get("recipient", ""),
        chain_id=int(payload.get("chainId", 0)),
        tx_hash=payload.get("txHash", ""),
        settled_at=payload.get("settledAt", ""),
        issued_at=datetime.fromtimestamp(payload["iat"]) if "iat" in payload else None,
        expires_at=datetime.fromtimestamp(payload["exp"]) if "exp" in payload else None,
    )


def is_receipt_expired(receipt: str | PaymentReceipt) -> bool:
    """
    Check if a receipt is expired.

    Args:
        receipt: The JWT receipt string or parsed PaymentReceipt

    Returns:
        bool: True if expired, False otherwise
    """
    if isinstance(receipt, str):
        parsed = parse_payment_receipt(receipt)
    else:
        parsed = receipt

    if parsed.expires_at is None:
        return False

    return parsed.expires_at < datetime.now()


def clear_jwks_cache() -> None:
    """
    Clear the JWKS cache.

    Useful for testing or when keys have rotated.
    """
    _jwks_cache.clear()


def get_default_jwks_url() -> str:
    """
    Get the default JWKS URL.

    Returns:
        str: The default JWKS URL
    """
    return DEFAULT_JWKS_URL

