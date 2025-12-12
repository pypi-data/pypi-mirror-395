"""
MixrPay Charges Module

Create and manage charges using session signers.
Session signers allow you to charge user wallets without
requiring approval for each transaction.
"""

import os
import hmac
import hashlib
import httpx
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


# =============================================================================
# Types
# =============================================================================

@dataclass
class SessionLimits:
    """Spending limits for a session."""
    max_total_usd: Optional[float] = None
    max_per_tx_usd: Optional[float] = None
    expires_at: Optional[str] = None


@dataclass
class SessionGrant:
    """Represents a session grant from a user."""
    session_id: str
    user_wallet: str
    merchant_wallet: str
    limits: SessionLimits
    granted_at: str


@dataclass
class Charge:
    """Represents a charge."""
    id: str
    status: str  # 'pending', 'submitted', 'confirmed', 'failed'
    amount_usd: float
    amount_usdc: str
    tx_hash: Optional[str] = None
    explorer_url: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    reference: Optional[str] = None
    created_at: Optional[str] = None
    confirmed_at: Optional[str] = None
    session_name: Optional[str] = None
    user_wallet: Optional[str] = None
    error: Optional[str] = None


@dataclass
class CreateChargeResult:
    """Result of creating a charge."""
    success: bool
    charge: Optional[Charge] = None
    idempotent_replay: bool = False
    error: Optional[str] = None
    details: Optional[str] = None


# =============================================================================
# Client
# =============================================================================

class ChargesClient:
    """
    Client for creating and managing charges.
    
    Example:
        >>> from mixrpay_merchant.charges import ChargesClient
        >>> 
        >>> charges = ChargesClient(api_key="sk_live_xxx")
        >>> 
        >>> result = charges.create(
        ...     session_id="sk_xxx",
        ...     amount_usd=0.05,
        ...     reference="image_gen_123",
        ...     metadata={"feature": "image_generation"}
        ... )
        >>> 
        >>> if result.success:
        ...     print(f"Charged {result.charge.amount_usdc}")
        ...     print(f"TX: {result.charge.explorer_url}")
    """
    
    def __init__(
        self, 
        api_key: str, 
        base_url: str = os.environ.get("MIXRPAY_BASE_URL", "https://mixrpay.com")
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )
    
    def create(
        self,
        session_id: str,
        amount_usd: float,
        reference: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> CreateChargeResult:
        """
        Create a new charge.
        
        Args:
            session_id: Session key ID granted by the user
            amount_usd: Amount to charge in USD (e.g., 0.05 for 5 cents)
            reference: Unique reference for idempotency (e.g., "order_123")
            metadata: Optional metadata
        
        Returns:
            CreateChargeResult with success status and charge details
        
        Example:
            >>> result = charges.create(
            ...     session_id="sk_xxx",
            ...     amount_usd=0.05,
            ...     reference="image_gen_123"
            ... )
        """
        response = self._client.post(
            f"{self.base_url}/api/v1/charges",
            json={
                "session_id": session_id,
                "amount_usd": amount_usd,
                "reference": reference,
                "metadata": metadata or {},
            }
        )
        
        data = response.json()
        
        if response.status_code >= 400:
            return CreateChargeResult(
                success=False,
                error=data.get("error"),
                details=data.get("details"),
            )
        
        charge = None
        if data.get("charge_id"):
            charge = Charge(
                id=data["charge_id"],
                status=data.get("status", "unknown"),
                amount_usd=data.get("amount_usd", amount_usd),
                amount_usdc=data.get("amount_usdc", ""),
                tx_hash=data.get("tx_hash"),
                explorer_url=data.get("explorer_url"),
                reference=reference,
                created_at=datetime.utcnow().isoformat(),
            )
        
        return CreateChargeResult(
            success=data.get("success", False),
            charge=charge,
            idempotent_replay=data.get("idempotent_replay", False),
            error=data.get("error"),
        )
    
    def get(self, charge_id: str) -> Optional[Charge]:
        """
        Get a charge by ID.
        
        Args:
            charge_id: The charge ID
        
        Returns:
            Charge object or None if not found
        
        Example:
            >>> charge = charges.get("chg_xxx")
            >>> print(charge.status)  # 'confirmed'
        """
        response = self._client.get(
            f"{self.base_url}/api/v1/charges",
            params={"id": charge_id}
        )
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        data = response.json()
        
        return Charge(
            id=data["id"],
            status=data["status"],
            amount_usd=data["amount_usd"],
            amount_usdc=data["amount_usdc"],
            tx_hash=data.get("tx_hash"),
            explorer_url=data.get("explorer_url"),
            from_address=data.get("from_address"),
            to_address=data.get("to_address"),
            reference=data.get("reference"),
            created_at=data.get("created_at"),
            confirmed_at=data.get("confirmed_at"),
            session_name=data.get("session_name"),
            user_wallet=data.get("user_wallet"),
        )
    
    def get_by_tx_hash(self, tx_hash: str) -> Optional[Charge]:
        """
        Get a charge by transaction hash.
        
        Args:
            tx_hash: The blockchain transaction hash
        
        Returns:
            Charge object or None if not found
        """
        response = self._client.get(
            f"{self.base_url}/api/v1/charges",
            params={"tx_hash": tx_hash}
        )
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        data = response.json()
        
        return Charge(
            id=data["id"],
            status=data["status"],
            amount_usd=data["amount_usd"],
            amount_usdc=data["amount_usdc"],
            tx_hash=data.get("tx_hash"),
            explorer_url=data.get("explorer_url"),
            from_address=data.get("from_address"),
            to_address=data.get("to_address"),
            reference=data.get("reference"),
            created_at=data.get("created_at"),
            confirmed_at=data.get("confirmed_at"),
            session_name=data.get("session_name"),
            user_wallet=data.get("user_wallet"),
        )
    
    def close(self):
        """Close the HTTP client."""
        self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# =============================================================================
# Webhook Verification
# =============================================================================

def verify_session_webhook(
    payload: str,
    signature: str,
    secret: str
) -> bool:
    """
    Verify a session.granted webhook signature.
    
    Args:
        payload: Raw JSON payload string
        signature: Value of X-MixrPay-Signature header
        secret: Your webhook secret
    
    Returns:
        True if signature is valid
    
    Example:
        >>> payload = request.get_data(as_text=True)
        >>> signature = request.headers.get('X-MixrPay-Signature')
        >>> 
        >>> if verify_session_webhook(payload, signature, webhook_secret):
        ...     data = json.loads(payload)
        ...     grant = parse_session_grant(data)
        ...     print(f"User {grant.user_wallet} granted access")
    """
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)


def parse_session_grant(payload: dict[str, Any]) -> SessionGrant:
    """
    Parse a session.granted webhook payload.
    
    Args:
        payload: Parsed JSON payload
    
    Returns:
        SessionGrant object
    
    Raises:
        ValueError: If event type is not session.granted
    """
    if payload.get("event") != "session.granted":
        raise ValueError(f"Unexpected event type: {payload.get('event')}")
    
    limits_data = payload.get("limits", {})
    limits = SessionLimits(
        max_total_usd=limits_data.get("max_total_usd"),
        max_per_tx_usd=limits_data.get("max_per_tx_usd"),
        expires_at=limits_data.get("expires_at"),
    )
    
    return SessionGrant(
        session_id=payload["session_id"],
        user_wallet=payload["user_wallet"],
        merchant_wallet=payload["merchant_wallet"],
        limits=limits,
        granted_at=payload["granted_at"],
    )

