"""
MixrPay Merchant SDK - Flask Middleware

Add payment requirements to Flask routes.

Usage with x402 (single payment method):
    from mixrpay_merchant.flask import x402
    
    @app.route("/api/query", methods=["POST"])
    @x402(price=0.05)
    def query():
        payment = request.x402_payment
        return {"result": "success", "payer": payment.payer}

Usage with mixrpay (unified - recommended):
    from mixrpay_merchant.flask import mixrpay
    
    @app.route("/api/query", methods=["POST"])
    @mixrpay(price_usd=0.05)
    def query():
        payment = request.mixr_payment
        # Accepts session, widget, or x402 payments
        return {"result": "success", "method": payment.method}
"""

import os
import time
import uuid
import base64
import json
from functools import wraps
from typing import Optional, Callable

import httpx

from .types import (
    X402PaymentResult, 
    X402PaymentRequired, 
    VerifyOptions,
    MixrPayPaymentResult,
    PaymentMethod,
)
from .verify import verify_x402_payment_sync, usd_to_minor


DEFAULT_FACILITATOR = "https://x402.org/facilitator"
DEFAULT_MIXRPAY_API_URL = "https://mixrpay.com"


def x402(
    price: float,
    *,
    recipient: Optional[str] = None,
    chain_id: int = 8453,
    facilitator: str = DEFAULT_FACILITATOR,
    description: Optional[str] = None,
    test_mode: bool = False,
    get_price: Optional[Callable[..., float]] = None,
    on_payment: Optional[Callable[[X402PaymentResult], None]] = None,
    skip: Optional[Callable[..., bool]] = None,
):
    """
    Flask decorator that requires x402 payment.
    
    Usage:
        @app.route("/api/query", methods=["POST"])
        @x402(price=0.05)
        def query():
            payment = request.x402_payment
            return jsonify({"result": "success", "payer": payment.payer})
    
    Args:
        price: Price in USD (e.g., 0.05 for 5 cents)
        recipient: Your wallet address (defaults to MIXRPAY_MERCHANT_ADDRESS env)
        chain_id: Chain ID (default: 8453 for Base)
        facilitator: Facilitator URL for settlement
        description: Description shown to payer
        test_mode: Skip on-chain settlement (for testing)
        get_price: Dynamic pricing function
        on_payment: Callback after successful payment
        skip: Function to determine if payment should be skipped
    """
    try:
        from flask import request, jsonify
    except ImportError:
        raise ImportError(
            "Flask is required for this middleware. "
            "Install with: pip install mixrpay-merchant[flask]"
        )
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if we should skip payment
            if skip is not None and skip(request):
                request.x402_payment = X402PaymentResult(valid=True, payer="skipped", amount=0)
                return func(*args, **kwargs)
            
            # Determine price
            actual_price = get_price(request) if get_price else price
            price_minor = usd_to_minor(actual_price)
            
            # Get recipient
            actual_recipient = recipient or os.environ.get("MIXRPAY_MERCHANT_ADDRESS")
            if not actual_recipient:
                return jsonify({"error": "Payment configuration error"}), 500
            
            # Check for payment header
            payment_header = request.headers.get("X-Payment")
            
            if not payment_header:
                # Return 402 with requirements
                nonce = str(uuid.uuid4()).replace("-", "")
                expires_at = int(time.time()) + 300
                
                payment_required = X402PaymentRequired(
                    recipient=actual_recipient,
                    amount=str(price_minor),
                    currency="USDC",
                    chain_id=chain_id,
                    facilitator=facilitator,
                    nonce=nonce,
                    expires_at=expires_at,
                    description=description,
                )
                
                encoded = base64.b64encode(
                    json.dumps(payment_required.to_dict()).encode()
                ).decode()
                
                response = jsonify({
                    "error": "Payment required",
                    "payment": payment_required.to_dict()
                })
                response.status_code = 402
                response.headers["X-Payment-Required"] = json.dumps(payment_required.to_dict())
                response.headers["WWW-Authenticate"] = f"X-402 {encoded}"
                return response
            
            # Verify payment
            result = verify_x402_payment_sync(
                payment_header,
                VerifyOptions(
                    expected_amount=price_minor,
                    expected_recipient=actual_recipient,
                    chain_id=chain_id,
                    facilitator=facilitator,
                    skip_settlement=test_mode,
                )
            )
            
            if not result.valid:
                return jsonify({
                    "error": "Invalid payment",
                    "reason": result.error
                }), 402
            
            # Store payment result on request
            request.x402_payment = result
            
            # Call on_payment callback
            if on_payment is not None:
                on_payment(result)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# =============================================================================
# Unified MixrPay Middleware
# =============================================================================

def mixrpay(
    price_usd: float,
    *,
    feature: Optional[str] = None,
    description: Optional[str] = None,
    skip: Optional[Callable[..., bool]] = None,
    test_mode: bool = False,
    on_payment: Optional[Callable[[MixrPayPaymentResult], None]] = None,
    # x402-specific options
    recipient: Optional[str] = None,
    chain_id: int = 8453,
    facilitator: str = DEFAULT_FACILITATOR,
    mixrpay_api_url: Optional[str] = None,
    get_price: Optional[Callable[..., float]] = None,
):
    """
    Unified Flask decorator that accepts payments from multiple sources:
    - Session Authorizations (X-Mixr-Session header)
    - Widget payments (X-Mixr-Payment header)
    - x402 Protocol (X-PAYMENT header)
    
    This is the recommended middleware for new integrations.
    
    Usage:
        @app.route("/api/query", methods=["POST"])
        @mixrpay(price_usd=0.05)
        def query():
            payment = request.mixr_payment
            print(f"Paid ${payment.amount_usd} via {payment.method}")
            return jsonify({"result": "success", "payer": payment.payer})
    
    Args:
        price_usd: Price in USD (e.g., 0.05 for 5 cents)
        feature: Feature slug for tracking/analytics
        description: Description shown to payer
        skip: Function to determine if payment should be skipped
        test_mode: Skip on-chain settlement (for testing)
        on_payment: Callback after successful payment
        recipient: Your wallet address for x402 payments
        chain_id: Chain ID (default: 8453 for Base)
        facilitator: Facilitator URL for x402 settlement
        mixrpay_api_url: MixrPay API URL for session/widget verification
        get_price: Dynamic pricing function
    """
    try:
        from flask import request, jsonify
    except ImportError:
        raise ImportError(
            "Flask is required for this middleware. "
            "Install with: pip install mixrpay-merchant[flask]"
        )
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if we should skip payment
            if skip is not None and skip(request):
                request.mixr_payment = MixrPayPaymentResult(
                    valid=True, 
                    method="session", 
                    payer="skipped", 
                    amount_usd=0
                )
                return func(*args, **kwargs)
            
            # Determine price
            actual_price = get_price(request) if get_price else price_usd
            
            # Check headers in priority order
            session_header = request.headers.get("X-Mixr-Session")
            widget_header = request.headers.get("X-Mixr-Payment")
            x402_header = request.headers.get("X-Payment")
            
            payment_result: MixrPayPaymentResult
            
            # 1. Session Authorization (highest priority - agent SDK)
            if session_header:
                payment_result = _verify_session_payment_sync(
                    session_id=session_header,
                    price_usd=actual_price,
                    feature=feature or request.headers.get("X-Mixr-Feature"),
                    idempotency_key=request.headers.get("X-Idempotency-Key"),
                    mixrpay_api_url=mixrpay_api_url,
                )
            # 2. Widget Payment (human users)
            elif widget_header:
                payment_result = _verify_widget_payment_sync(
                    payment_jwt=widget_header,
                    price_usd=actual_price,
                    feature=feature or request.headers.get("X-Mixr-Feature"),
                    mixrpay_api_url=mixrpay_api_url,
                )
            # 3. x402 Protocol (external agents)
            elif x402_header:
                payment_result = _verify_x402_payment_sync_unified(
                    payment_header=x402_header,
                    price_usd=actual_price,
                    recipient=recipient,
                    chain_id=chain_id,
                    facilitator=facilitator,
                    test_mode=test_mode,
                )
            # No payment header - return 402
            else:
                return _return_payment_required_flask(
                    price_usd=actual_price,
                    recipient=recipient,
                    chain_id=chain_id,
                    facilitator=facilitator,
                    description=description,
                )
            
            if not payment_result.valid:
                return jsonify({
                    "error": "Invalid payment",
                    "reason": payment_result.error,
                    "method": payment_result.method,
                }), 402
            
            # Store payment result on request
            request.mixr_payment = payment_result
            
            # Call on_payment callback
            if on_payment is not None:
                on_payment(payment_result)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def _verify_session_payment_sync(
    session_id: str,
    price_usd: float,
    feature: Optional[str],
    idempotency_key: Optional[str],
    mixrpay_api_url: Optional[str],
) -> MixrPayPaymentResult:
    """Verify a session authorization payment (sync version for Flask)."""
    base_url = mixrpay_api_url or os.environ.get("MIXRPAY_API_URL") or DEFAULT_MIXRPAY_API_URL
    secret_key = os.environ.get("MIXRPAY_SECRET_KEY")
    
    if not secret_key:
        return MixrPayPaymentResult(
            valid=False,
            method="session",
            error="MIXRPAY_SECRET_KEY not configured",
            session_id=session_id,
        )
    
    try:
        response = httpx.post(
            f"{base_url}/api/v2/charge",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {secret_key}",
            },
            json={
                "session_id": session_id,
                "price_usd": price_usd,
                "feature": feature,
                "idempotency_key": idempotency_key,
            },
            timeout=30.0,
        )
        
        data = response.json()
        
        if not response.is_success:
            return MixrPayPaymentResult(
                valid=False,
                method="session",
                error=data.get("error") or f"Charge failed: {response.status_code}",
                session_id=session_id,
                remaining_session_balance_usd=data.get("session_remaining_usd"),
            )
        
        from datetime import datetime
        return MixrPayPaymentResult(
            valid=True,
            method="session",
            payer=data.get("payer") or data.get("wallet_address"),
            amount_usd=data.get("merchant_amount_usd") or price_usd,
            tx_hash=data.get("tx_hash"),
            charge_id=data.get("charge_id"),
            session_id=session_id,
            feature=feature,
            settled_at=datetime.now(),
            remaining_session_balance_usd=data.get("session_remaining_usd"),
        )
    except Exception as e:
        return MixrPayPaymentResult(
            valid=False,
            method="session",
            error=f"Session verification failed: {str(e)}",
            session_id=session_id,
        )


def _verify_widget_payment_sync(
    payment_jwt: str,
    price_usd: float,
    feature: Optional[str],
    mixrpay_api_url: Optional[str],
) -> MixrPayPaymentResult:
    """Verify a widget payment JWT (sync version for Flask)."""
    base_url = mixrpay_api_url or os.environ.get("MIXRPAY_API_URL") or DEFAULT_MIXRPAY_API_URL
    secret_key = os.environ.get("MIXRPAY_SECRET_KEY")
    
    if not secret_key:
        return MixrPayPaymentResult(
            valid=False,
            method="widget",
            error="MIXRPAY_SECRET_KEY not configured",
        )
    
    try:
        response = httpx.post(
            f"{base_url}/api/widget/verify",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {secret_key}",
            },
            json={
                "paymentJwt": payment_jwt,
                "expectedAmountUsd": price_usd,
                "feature": feature,
            },
            timeout=30.0,
        )
        
        data = response.json()
        
        if not response.is_success:
            return MixrPayPaymentResult(
                valid=False,
                method="widget",
                error=data.get("message") or data.get("error") or f"Widget verification failed: {response.status_code}",
            )
        
        from datetime import datetime
        return MixrPayPaymentResult(
            valid=True,
            method="widget",
            payer=data.get("payer") or data.get("walletAddress"),
            amount_usd=data.get("amountUsd") or price_usd,
            tx_hash=data.get("txHash"),
            charge_id=data.get("chargeId"),
            feature=feature,
            settled_at=datetime.fromisoformat(data["settledAt"]) if data.get("settledAt") else datetime.now(),
        )
    except Exception as e:
        return MixrPayPaymentResult(
            valid=False,
            method="widget",
            error=f"Widget verification failed: {str(e)}",
        )


def _verify_x402_payment_sync_unified(
    payment_header: str,
    price_usd: float,
    recipient: Optional[str],
    chain_id: int,
    facilitator: str,
    test_mode: bool,
) -> MixrPayPaymentResult:
    """Verify an x402 payment header (sync version for Flask)."""
    actual_recipient = recipient or os.environ.get("MIXRPAY_MERCHANT_ADDRESS")
    
    if not actual_recipient:
        return MixrPayPaymentResult(
            valid=False,
            method="x402",
            error="MIXRPAY_MERCHANT_ADDRESS not configured for x402 payments",
        )
    
    price_minor = usd_to_minor(price_usd)
    
    x402_result = verify_x402_payment_sync(
        payment_header,
        VerifyOptions(
            expected_amount=price_minor,
            expected_recipient=actual_recipient,
            chain_id=chain_id,
            facilitator=facilitator,
            skip_settlement=test_mode,
        )
    )
    
    if not x402_result.valid:
        return MixrPayPaymentResult(
            valid=False,
            method="x402",
            error=x402_result.error,
            x402_result=x402_result,
        )
    
    return MixrPayPaymentResult(
        valid=True,
        method="x402",
        payer=x402_result.payer,
        amount_usd=x402_result.amount,
        tx_hash=x402_result.tx_hash,
        settled_at=x402_result.settled_at,
        x402_result=x402_result,
    )


def _return_payment_required_flask(
    price_usd: float,
    recipient: Optional[str],
    chain_id: int,
    facilitator: str,
    description: Optional[str],
):
    """Return a 402 Payment Required response for Flask."""
    from flask import jsonify
    
    price_minor = usd_to_minor(price_usd)
    actual_recipient = recipient or os.environ.get("MIXRPAY_MERCHANT_ADDRESS")
    nonce = str(uuid.uuid4()).replace("-", "")
    expires_at = int(time.time()) + 300  # 5 minutes
    
    # x402 payment requirements (for x402-enabled agents)
    x402_payment_required = None
    if actual_recipient:
        x402_payment_required = X402PaymentRequired(
            recipient=actual_recipient,
            amount=str(price_minor),
            currency="USDC",
            chain_id=chain_id,
            facilitator=facilitator,
            nonce=nonce,
            expires_at=expires_at,
            description=description,
        )
    
    response_body = {
        "error": "Payment required",
        "priceUsd": price_usd,
        "acceptedMethods": [
            {"method": "session", "header": "X-Mixr-Session", "description": "Session authorization ID"},
            {"method": "widget", "header": "X-Mixr-Payment", "description": "Widget payment JWT"},
        ],
        "description": description,
    }
    
    if x402_payment_required:
        response_body["acceptedMethods"].append(
            {"method": "x402", "header": "X-PAYMENT", "description": "x402 protocol payment"}
        )
        response_body["x402"] = x402_payment_required.to_dict()
    
    response = jsonify(response_body)
    response.status_code = 402
    
    if x402_payment_required:
        encoded = base64.b64encode(
            json.dumps(x402_payment_required.to_dict()).encode()
        ).decode()
        response.headers["X-Payment-Required"] = json.dumps(x402_payment_required.to_dict())
        response.headers["WWW-Authenticate"] = f"X-402 {encoded}"
    
    return response

