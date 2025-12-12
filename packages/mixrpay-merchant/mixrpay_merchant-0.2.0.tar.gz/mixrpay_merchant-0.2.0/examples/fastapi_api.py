"""
Example: FastAPI with MixrPay Payments

This example shows how to add payment requirements to a FastAPI app.
Supports multiple payment methods:
- Session Authorizations (AI agents with session keys)
- Widget payments (human users)
- x402 Protocol (external agents)

Run with:
    MIXRPAY_SECRET_KEY=sk_... MIXRPAY_MERCHANT_ADDRESS=0x... uvicorn fastapi_api:app --reload
"""

import os
from fastapi import FastAPI, Depends, Request
from mixrpay_merchant import mixrpay, x402, MixrPayPaymentResult, X402PaymentResult

app = FastAPI(
    title="MixrPay API Example",
    description="FastAPI with unified MixrPay payments",
)


# =============================================================================
# Unified MixrPay Endpoint (Recommended)
# =============================================================================

@app.post("/api/query")
async def query(
    request: Request,
    payment: MixrPayPaymentResult = Depends(mixrpay(price_usd=0.05))
):
    """
    Simple endpoint with fixed $0.05 price per request.
    Accepts session, widget, or x402 payments.
    
    Test with session key:
        curl -X POST http://localhost:8000/api/query \
            -H "Content-Type: application/json" \
            -H "X-Mixr-Session: sess_xxx" \
            -d '{"prompt": "Hello!"}'
    
    Test with x402:
        curl -X POST http://localhost:8000/api/query \
            -H "Content-Type: application/json" \
            -d '{"prompt": "Hello!"}'
        # Returns 402 with payment requirements
    """
    print(f"✅ Payment received via {payment.method}: ${payment.amount_usd} from {payment.payer}")
    if payment.tx_hash:
        print(f"   Transaction: {payment.tx_hash}")
    if payment.session_id:
        print(f"   Session: {payment.session_id}")
    
    body = await request.json()
    result = f"You said: \"{body.get('prompt', 'nothing')}\""
    
    return {
        "result": result,
        "payment": {
            "method": payment.method,
            "payer": payment.payer,
            "amount_usd": payment.amount_usd,
            "tx_hash": payment.tx_hash,
            "session_id": payment.session_id,
        }
    }


# =============================================================================
# x402-only Endpoint (for backwards compatibility)
# =============================================================================

@app.post("/api/query-x402")
async def query_x402(
    request: Request,
    payment: X402PaymentResult = Depends(x402(price=0.05))
):
    """
    x402-only endpoint for backwards compatibility.
    Only accepts x402 protocol payments.
    """
    print(f"✅ x402 Payment received: ${payment.amount} from {payment.payer}")
    print(f"   Transaction: {payment.tx_hash}")
    
    body = await request.json()
    result = f"You said: \"{body.get('prompt', 'nothing')}\""
    
    return {
        "result": result,
        "payment": {
            "payer": payment.payer,
            "amount": payment.amount,
            "tx_hash": payment.tx_hash,
        }
    }


# =============================================================================
# Dynamic Pricing Endpoint
# =============================================================================

async def get_model_price(request: Request) -> float:
    """Calculate price based on the model selected."""
    try:
        body = await request.json()
        model = body.get("model", "default")
    except:
        model = "default"
    
    prices = {
        "gpt-4": 0.10,
        "gpt-3.5-turbo": 0.02,
        "default": 0.05,
    }
    return prices.get(model, prices["default"])


@app.post("/api/generate")
async def generate(
    request: Request,
    payment: MixrPayPaymentResult = Depends(mixrpay(get_price=get_model_price, feature="generate"))
):
    """
    Endpoint with dynamic pricing based on the model selected.
    Accepts session, widget, or x402 payments.
    
    GPT-4 requests cost $0.10, GPT-3.5 costs $0.02, default is $0.05.
    """
    body = await request.json()
    model = body.get("model", "default")
    
    print(f"✅ {model} generation via {payment.method}: ${payment.amount_usd} from {payment.payer}")
    
    return {
        "result": f"Generated with {model}",
        "model": model,
        "charged": payment.amount_usd,
        "method": payment.method,
    }


# =============================================================================
# Premium User Skip Example
# =============================================================================

def is_premium_user(request: Request) -> bool:
    """Check if user has premium access."""
    return request.headers.get("x-premium-token") == "valid"


@app.post("/api/premium")
async def premium_endpoint(
    request: Request,
    payment: MixrPayPaymentResult = Depends(mixrpay(price_usd=0.05, skip=is_premium_user))
):
    """
    Endpoint that skips payment for premium users.
    Accepts session, widget, or x402 payments for non-premium users.
    
    Send X-Premium-Token: valid to skip payment.
    """
    if payment.payer == "skipped":
        print("👑 Premium user - no payment required")
        return {"result": "Premium access granted", "premium": True}
    else:
        print(f"✅ Standard user paid via {payment.method}: ${payment.amount_usd}")
        return {
            "result": "Access granted", 
            "premium": False, 
            "paid": payment.amount_usd,
            "method": payment.method,
        }


# =============================================================================
# Payment Callback Example
# =============================================================================

async def log_payment(payment: MixrPayPaymentResult):
    """Log payment to console (in production, save to database)."""
    print("📝 Logging payment:", {
        "method": payment.method,
        "payer": payment.payer,
        "amount_usd": payment.amount_usd,
        "tx_hash": payment.tx_hash,
        "session_id": payment.session_id,
        "settled_at": payment.settled_at,
    })
    
    # In production, save to database:
    # await db.payments.create(
    #     method=payment.method,
    #     payer=payment.payer, 
    #     amount_usd=payment.amount_usd, 
    #     session_id=payment.session_id,
    #     ...
    # )


@app.post("/api/logged")
async def logged_endpoint(
    payment: MixrPayPaymentResult = Depends(mixrpay(price_usd=0.05, on_payment=log_payment))
):
    """Endpoint that logs all payments to console."""
    return {"result": "Success - payment logged", "method": payment.method}


# =============================================================================
# Health Check (Free)
# =============================================================================

@app.get("/health")
async def health():
    """Free health check endpoint."""
    from datetime import datetime
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# =============================================================================
# Startup
# =============================================================================

@app.on_event("startup")
async def startup():
    merchant_address = os.environ.get("MIXRPAY_MERCHANT_ADDRESS", "NOT SET")
    secret_key = "SET" if os.environ.get("MIXRPAY_SECRET_KEY") else "NOT SET"
    print(f"""
🚀 MixrPay API Server running

Endpoints (unified - accepts session/widget/x402):
  POST /api/query     - Fixed price: $0.05
  POST /api/generate  - Dynamic pricing by model
  POST /api/premium   - Free for premium users  
  POST /api/logged    - With payment callback
  POST /api/query-x402 - x402 only (backwards compat)
  GET  /health        - Free health check

Config:
  MIXRPAY_SECRET_KEY: {secret_key}
  MIXRPAY_MERCHANT_ADDRESS: {merchant_address}

Test with Python Agent SDK:
    from mixrpay import AgentWallet
    wallet = AgentWallet(session_key="sk_...")
    response = await wallet.call_merchant_api(
        url="http://localhost:8000/api/query",
        merchant_public_key="pk_...",
        price_usd=0.05,
        json={{"prompt": "Hi!"}},
    )
    """)

