"""
Example: Flask with MixrPay Payments

This example shows how to add payment requirements to a Flask app.
Supports multiple payment methods:
- Session Authorizations (AI agents with session keys)
- Widget payments (human users)
- x402 Protocol (external agents)

Run with:
    MIXRPAY_SECRET_KEY=sk_... MIXRPAY_MERCHANT_ADDRESS=0x... flask --app flask_api run
"""

import os
from datetime import datetime
from flask import Flask, jsonify, request
from mixrpay_merchant.flask import mixrpay, x402

app = Flask(__name__)


# =============================================================================
# Unified MixrPay Endpoint (Recommended)
# =============================================================================

@app.route("/api/query", methods=["POST"])
@mixrpay(price_usd=0.05)
def query():
    """
    Simple endpoint with fixed $0.05 price per request.
    Accepts session, widget, or x402 payments.
    
    Test with session key:
        curl -X POST http://localhost:5000/api/query \
            -H "Content-Type: application/json" \
            -H "X-Mixr-Session: sess_xxx" \
            -d '{"prompt": "Hello!"}'
    
    Test with x402:
        curl -X POST http://localhost:5000/api/query \
            -H "Content-Type: application/json" \
            -d '{"prompt": "Hello!"}'
        # Returns 402 with payment requirements
    """
    payment = request.mixr_payment
    
    print(f"✅ Payment received via {payment.method}: ${payment.amount_usd} from {payment.payer}")
    if payment.tx_hash:
        print(f"   Transaction: {payment.tx_hash}")
    if payment.session_id:
        print(f"   Session: {payment.session_id}")
    
    body = request.get_json() or {}
    result = f"You said: \"{body.get('prompt', 'nothing')}\""
    
    return jsonify({
        "result": result,
        "payment": {
            "method": payment.method,
            "payer": payment.payer,
            "amount_usd": payment.amount_usd,
            "tx_hash": payment.tx_hash,
            "session_id": payment.session_id,
        }
    })


# =============================================================================
# x402-only Endpoint (for backwards compatibility)
# =============================================================================

@app.route("/api/query-x402", methods=["POST"])
@x402(price=0.05)
def query_x402():
    """
    x402-only endpoint for backwards compatibility.
    Only accepts x402 protocol payments.
    """
    payment = request.x402_payment
    
    print(f"✅ x402 Payment received: ${payment.amount} from {payment.payer}")
    print(f"   Transaction: {payment.tx_hash}")
    
    body = request.get_json() or {}
    result = f"You said: \"{body.get('prompt', 'nothing')}\""
    
    return jsonify({
        "result": result,
        "payment": {
            "payer": payment.payer,
            "amount": payment.amount,
            "tx_hash": payment.tx_hash,
        }
    })


# =============================================================================
# Dynamic Pricing Endpoint
# =============================================================================

def get_model_price(req) -> float:
    """Calculate price based on the model selected."""
    body = req.get_json() or {}
    model = body.get("model", "default")
    
    prices = {
        "gpt-4": 0.10,
        "gpt-3.5-turbo": 0.02,
        "default": 0.05,
    }
    return prices.get(model, prices["default"])


@app.route("/api/generate", methods=["POST"])
@mixrpay(price_usd=0.05, get_price=get_model_price, feature="generate")
def generate():
    """
    Endpoint with dynamic pricing based on the model selected.
    Accepts session, widget, or x402 payments.
    
    GPT-4 requests cost $0.10, GPT-3.5 costs $0.02, default is $0.05.
    """
    payment = request.mixr_payment
    body = request.get_json() or {}
    model = body.get("model", "default")
    
    print(f"✅ {model} generation via {payment.method}: ${payment.amount_usd} from {payment.payer}")
    
    return jsonify({
        "result": f"Generated with {model}",
        "model": model,
        "charged": payment.amount_usd,
        "method": payment.method,
    })


# =============================================================================
# Premium User Skip Example
# =============================================================================

def is_premium_user(req) -> bool:
    """Check if user has premium access."""
    return req.headers.get("X-Premium-Token") == "valid"


@app.route("/api/premium", methods=["POST"])
@mixrpay(price_usd=0.05, skip=is_premium_user)
def premium_endpoint():
    """
    Endpoint that skips payment for premium users.
    Accepts session, widget, or x402 payments for non-premium users.
    
    Send X-Premium-Token: valid to skip payment.
    """
    payment = request.mixr_payment
    
    if payment.payer == "skipped":
        print("👑 Premium user - no payment required")
        return jsonify({"result": "Premium access granted", "premium": True})
    else:
        print(f"✅ Standard user paid via {payment.method}: ${payment.amount_usd}")
        return jsonify({
            "result": "Access granted", 
            "premium": False, 
            "paid": payment.amount_usd,
            "method": payment.method,
        })


# =============================================================================
# Payment Callback Example
# =============================================================================

def log_payment(payment):
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
    # db.payments.create(
    #     method=payment.method,
    #     payer=payment.payer, 
    #     amount_usd=payment.amount_usd, 
    #     session_id=payment.session_id,
    #     ...
    # )


@app.route("/api/logged", methods=["POST"])
@mixrpay(price_usd=0.05, on_payment=log_payment)
def logged_endpoint():
    """Endpoint that logs all payments to console."""
    payment = request.mixr_payment
    return jsonify({"result": "Success - payment logged", "method": payment.method})


# =============================================================================
# Health Check (Free)
# =============================================================================

@app.route("/health")
def health():
    """Free health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


# =============================================================================
# Startup Message
# =============================================================================

if __name__ == "__main__":
    merchant_address = os.environ.get("MIXRPAY_MERCHANT_ADDRESS", "NOT SET")
    secret_key = "SET" if os.environ.get("MIXRPAY_SECRET_KEY") else "NOT SET"
    print(f"""
🚀 MixrPay API Server starting...

Endpoints (unified - accepts session/widget/x402):
  POST /api/query      - Fixed price: $0.05
  POST /api/generate   - Dynamic pricing by model
  POST /api/premium    - Free for premium users
  POST /api/logged     - With payment callback
  POST /api/query-x402 - x402 only (backwards compat)
  GET  /health         - Free health check

Config:
  MIXRPAY_SECRET_KEY: {secret_key}
  MIXRPAY_MERCHANT_ADDRESS: {merchant_address}

Test with Python Agent SDK:
    from mixrpay import AgentWallet
    wallet = AgentWallet(session_key="sk_...")
    response = await wallet.call_merchant_api(
        url="http://localhost:5000/api/query",
        merchant_public_key="pk_...",
        price_usd=0.05,
        json={{"prompt": "Hi!"}},
    )
    """)
    
    app.run(debug=True)
