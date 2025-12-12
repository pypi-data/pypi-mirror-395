"""
MixrPay Merchant SDK - FastAPI Middleware

Add payment requirements to FastAPI routes.

Usage with x402 (single payment method):
    from mixrpay_merchant import x402
    from fastapi import Depends
    
    @app.post("/api/query")
    async def query(payment = Depends(x402(price=0.05))):
        return {"result": "success", "payer": payment.payer}

Usage with mixrpay (unified - recommended):
    from mixrpay_merchant import mixrpay
    from fastapi import Depends
    
    @app.post("/api/query")
    async def query(payment = Depends(mixrpay(price_usd=0.05))):
        # Accepts session, widget, or x402 payments
        return {"result": "success", "payer": payment.payer, "method": payment.method}
"""

import os
import time
import uuid
import base64
import json
import asyncio
from functools import wraps
from typing import Optional, Callable, Union, Awaitable

import httpx

from .types import (
    X402PaymentResult, 
    X402PaymentRequired, 
    VerifyOptions,
    MixrPayPaymentResult,
    MixrPayOptions,
    PaymentMethod,
)
from .verify import verify_x402_payment, usd_to_minor


DEFAULT_FACILITATOR = "https://x402.org/facilitator"
DEFAULT_MIXRPAY_API_URL = "https://mixrpay.com"


def x402(
    price: Optional[float] = None,
    *,
    get_price: Optional[Callable[..., Union[float, Awaitable[float]]]] = None,
    recipient: Optional[str] = None,
    chain_id: int = 8453,
    facilitator: str = DEFAULT_FACILITATOR,
    description: Optional[str] = None,
    test_mode: bool = False,
    on_payment: Optional[Callable[[X402PaymentResult], Union[None, Awaitable[None]]]] = None,
    skip: Optional[Callable[..., Union[bool, Awaitable[bool]]]] = None,
):
    """
    FastAPI dependency that requires x402 payment.
    
    Usage:
        @app.post("/api/query")
        async def query(payment = Depends(x402(price=0.05))):
            # payment contains verified payment details
            return {"result": "success", "payer": payment.payer}
    
    Args:
        price: Fixed price in USD (e.g., 0.05 for 5 cents)
        get_price: Dynamic pricing function that receives the request
        recipient: Your wallet address (defaults to MIXRPAY_MERCHANT_ADDRESS env)
        chain_id: Chain ID (default: 8453 for Base)
        facilitator: Facilitator URL for settlement
        description: Description shown to payer
        test_mode: Skip on-chain settlement (for testing)
        on_payment: Callback after successful payment
        skip: Function to determine if payment should be skipped
    
    Returns:
        FastAPI dependency that returns X402PaymentResult
    """
    # Import here to avoid requiring fastapi for all users
    try:
        from fastapi import Request, HTTPException
    except ImportError:
        raise ImportError(
            "FastAPI is required for this middleware. "
            "Install with: pip install mixrpay-merchant[fastapi]"
        )
    
    async def dependency(request: Request) -> X402PaymentResult:
        # Check if we should skip payment
        if skip is not None:
            should_skip = skip(request)
            if asyncio.iscoroutine(should_skip):
                should_skip = await should_skip
            if should_skip:
                return X402PaymentResult(valid=True, payer="skipped", amount=0)
        
        # Determine price
        actual_price: float
        if get_price is not None:
            result = get_price(request)
            if asyncio.iscoroutine(result):
                actual_price = await result
            else:
                actual_price = result
        elif price is not None:
            actual_price = price
        else:
            raise ValueError("x402: price or get_price must be provided")
        
        price_minor = usd_to_minor(actual_price)
        
        # Get recipient
        actual_recipient = recipient or os.environ.get("MIXRPAY_MERCHANT_ADDRESS")
        if not actual_recipient:
            raise HTTPException(
                status_code=500,
                detail="Payment configuration error: no recipient address"
            )
        
        # Check for payment header
        payment_header = request.headers.get("x-payment")
        
        if not payment_header:
            # Return 402 with requirements
            nonce = str(uuid.uuid4()).replace("-", "")
            expires_at = int(time.time()) + 300  # 5 minutes
            
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
            
            # Encode for WWW-Authenticate header
            encoded = base64.b64encode(
                json.dumps(payment_required.to_dict()).encode()
            ).decode()
            
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "Payment required",
                    "payment": payment_required.to_dict()
                },
                headers={
                    "X-Payment-Required": json.dumps(payment_required.to_dict()),
                    "WWW-Authenticate": f"X-402 {encoded}",
                }
            )
        
        # Verify payment
        result = await verify_x402_payment(
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
            raise HTTPException(
                status_code=402,
                detail={"error": "Invalid payment", "reason": result.error}
            )
        
        # Call on_payment callback
        if on_payment is not None:
            callback_result = on_payment(result)
            if asyncio.iscoroutine(callback_result):
                await callback_result
        
        return result
    
    return dependency


def x402_decorator(
    price: float,
    **kwargs
):
    """
    Decorator version for simpler cases.
    Stores payment result in request.state.x402_payment
    
    Usage:
        @app.post("/api/query")
        @x402_decorator(price=0.05)
        async def query(request: Request):
            payment = request.state.x402_payment
            return {"result": "success"}
    """
    try:
        from fastapi import Request
    except ImportError:
        raise ImportError("FastAPI is required. Install with: pip install mixrpay-merchant[fastapi]")
    
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kw):
            dep = x402(price=price, **kwargs)
            payment = await dep(request)
            request.state.x402_payment = payment
            return await func(request, *args, **kw)
        return wrapper
    return decorator


# =============================================================================
# Unified MixrPay Middleware
# =============================================================================

def mixrpay(
    price_usd: Optional[float] = None,
    *,
    get_price: Optional[Callable[..., Union[float, Awaitable[float]]]] = None,
    feature: Optional[str] = None,
    description: Optional[str] = None,
    skip: Optional[Callable[..., Union[bool, Awaitable[bool]]]] = None,
    test_mode: bool = False,
    on_payment: Optional[Callable[[MixrPayPaymentResult], Union[None, Awaitable[None]]]] = None,
    # x402-specific options
    recipient: Optional[str] = None,
    chain_id: int = 8453,
    facilitator: str = DEFAULT_FACILITATOR,
    mixrpay_api_url: Optional[str] = None,
):
    """
    Unified FastAPI dependency that accepts payments from multiple sources:
    - Session Authorizations (X-Mixr-Session header)
    - Widget payments (X-Mixr-Payment header)
    - x402 Protocol (X-PAYMENT header)
    
    This is the recommended middleware for new integrations.
    
    Usage:
        @app.post("/api/query")
        async def query(payment = Depends(mixrpay(price_usd=0.05))):
            # payment contains unified payment details
            print(f"Paid ${payment.amount_usd} via {payment.method}")
            return {"result": "success", "payer": payment.payer}
    
    Args:
        price_usd: Fixed price in USD (e.g., 0.05 for 5 cents)
        get_price: Dynamic pricing function that receives the request
        feature: Feature slug for tracking/analytics
        description: Description shown to payer
        skip: Function to determine if payment should be skipped
        test_mode: Skip on-chain settlement (for testing)
        on_payment: Callback after successful payment
        recipient: Your wallet address for x402 payments
        chain_id: Chain ID (default: 8453 for Base)
        facilitator: Facilitator URL for x402 settlement
        mixrpay_api_url: MixrPay API URL for session/widget verification
    
    Returns:
        FastAPI dependency that returns MixrPayPaymentResult
    """
    try:
        from fastapi import Request, HTTPException
    except ImportError:
        raise ImportError(
            "FastAPI is required for this middleware. "
            "Install with: pip install mixrpay-merchant[fastapi]"
        )
    
    async def dependency(request: Request) -> MixrPayPaymentResult:
        # Check if we should skip payment
        if skip is not None:
            should_skip = skip(request)
            if asyncio.iscoroutine(should_skip):
                should_skip = await should_skip
            if should_skip:
                return MixrPayPaymentResult(
                    valid=True, 
                    method="session",  # Default for skipped
                    payer="skipped", 
                    amount_usd=0
                )
        
        # Determine price
        actual_price: float
        if get_price is not None:
            result = get_price(request)
            if asyncio.iscoroutine(result):
                actual_price = await result
            else:
                actual_price = result
        elif price_usd is not None:
            actual_price = price_usd
        else:
            raise ValueError("mixrpay: price_usd or get_price must be provided")
        
        # Check headers in priority order
        session_header = request.headers.get("x-mixr-session")
        widget_header = request.headers.get("x-mixr-payment")
        x402_header = request.headers.get("x-payment")
        
        payment_result: MixrPayPaymentResult
        
        # 1. Session Authorization (highest priority - agent SDK)
        if session_header:
            payment_result = await _verify_session_payment(
                session_id=session_header,
                price_usd=actual_price,
                feature=feature or request.headers.get("x-mixr-feature"),
                idempotency_key=request.headers.get("x-idempotency-key"),
                mixrpay_api_url=mixrpay_api_url,
            )
        # 2. Widget Payment (human users)
        elif widget_header:
            payment_result = await _verify_widget_payment(
                payment_jwt=widget_header,
                price_usd=actual_price,
                feature=feature or request.headers.get("x-mixr-feature"),
                mixrpay_api_url=mixrpay_api_url,
            )
        # 3. x402 Protocol (external agents)
        elif x402_header:
            payment_result = await _verify_x402_payment_unified(
                payment_header=x402_header,
                price_usd=actual_price,
                recipient=recipient,
                chain_id=chain_id,
                facilitator=facilitator,
                test_mode=test_mode,
            )
        # No payment header - return 402
        else:
            _raise_payment_required(
                price_usd=actual_price,
                recipient=recipient,
                chain_id=chain_id,
                facilitator=facilitator,
                description=description,
            )
        
        if not payment_result.valid:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "Invalid payment",
                    "reason": payment_result.error,
                    "method": payment_result.method,
                }
            )
        
        # Call on_payment callback
        if on_payment is not None:
            callback_result = on_payment(payment_result)
            if asyncio.iscoroutine(callback_result):
                await callback_result
        
        return payment_result
    
    return dependency


async def _verify_session_payment(
    session_id: str,
    price_usd: float,
    feature: Optional[str],
    idempotency_key: Optional[str],
    mixrpay_api_url: Optional[str],
) -> MixrPayPaymentResult:
    """Verify a session authorization payment by charging against the session."""
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
        async with httpx.AsyncClient() as client:
            response = await client.post(
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


async def _verify_widget_payment(
    payment_jwt: str,
    price_usd: float,
    feature: Optional[str],
    mixrpay_api_url: Optional[str],
) -> MixrPayPaymentResult:
    """Verify a widget payment JWT."""
    base_url = mixrpay_api_url or os.environ.get("MIXRPAY_API_URL") or DEFAULT_MIXRPAY_API_URL
    secret_key = os.environ.get("MIXRPAY_SECRET_KEY")
    
    if not secret_key:
        return MixrPayPaymentResult(
            valid=False,
            method="widget",
            error="MIXRPAY_SECRET_KEY not configured",
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
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


async def _verify_x402_payment_unified(
    payment_header: str,
    price_usd: float,
    recipient: Optional[str],
    chain_id: int,
    facilitator: str,
    test_mode: bool,
) -> MixrPayPaymentResult:
    """Verify an x402 payment header."""
    actual_recipient = recipient or os.environ.get("MIXRPAY_MERCHANT_ADDRESS")
    
    if not actual_recipient:
        return MixrPayPaymentResult(
            valid=False,
            method="x402",
            error="MIXRPAY_MERCHANT_ADDRESS not configured for x402 payments",
        )
    
    price_minor = usd_to_minor(price_usd)
    
    x402_result = await verify_x402_payment(
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


def _raise_payment_required(
    price_usd: float,
    recipient: Optional[str],
    chain_id: int,
    facilitator: str,
    description: Optional[str],
) -> None:
    """Raise a 402 Payment Required response."""
    from fastapi import HTTPException
    
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
    
    headers = {}
    if x402_payment_required:
        encoded = base64.b64encode(
            json.dumps(x402_payment_required.to_dict()).encode()
        ).decode()
        headers["X-Payment-Required"] = json.dumps(x402_payment_required.to_dict())
        headers["WWW-Authenticate"] = f"X-402 {encoded}"
    
    raise HTTPException(
        status_code=402,
        detail=response_body,
        headers=headers,
    )


def mixrpay_decorator(
    price_usd: float,
    **kwargs
):
    """
    Decorator version of the unified mixrpay middleware.
    Stores payment result in request.state.mixr_payment
    
    Usage:
        @app.post("/api/query")
        @mixrpay_decorator(price_usd=0.05)
        async def query(request: Request):
            payment = request.state.mixr_payment
            return {"result": "success", "method": payment.method}
    """
    try:
        from fastapi import Request
    except ImportError:
        raise ImportError("FastAPI is required. Install with: pip install mixrpay-merchant[fastapi]")
    
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kw):
            dep = mixrpay(price_usd=price_usd, **kwargs)
            payment = await dep(request)
            request.state.mixr_payment = payment
            return await func(request, *args, **kw)
        return wrapper
    return decorator

