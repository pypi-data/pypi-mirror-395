"""
MixrPay Merchant SDK - Add payments to your Python API.

Unified Middleware (Recommended):
    from mixrpay_merchant import mixrpay
    from fastapi import Depends
    
    @app.post("/api/query")
    async def query(payment = Depends(mixrpay(price_usd=0.05))):
        # Accepts session, widget, or x402 payments
        print(f"Paid ${payment.amount_usd} via {payment.method}")
        return {"result": "success", "payer": payment.payer}

x402-only Middleware:
    from mixrpay_merchant import x402
    from fastapi import Depends
    
    @app.post("/api/query")
    async def query(payment = Depends(x402(price=0.05))):
        return {"result": "success", "payer": payment.payer}

Flask Usage:
    from mixrpay_merchant.flask import mixrpay  # or x402
    
    @app.route("/api/query", methods=["POST"])
    @mixrpay(price_usd=0.05)
    def query():
        payment = request.mixr_payment
        return {"result": "success", "method": payment.method}

JWT Receipt Verification:
    from mixrpay_merchant import verify_payment_receipt
    
    receipt = request.headers.get("X-Payment-Receipt")
    payment = verify_payment_receipt(receipt)
    print(f"Paid ${payment.amount_usd} from {payment.payer}")

Session-Based Charges:
    from mixrpay_merchant.charges import ChargesClient
    
    charges = ChargesClient(api_key="sk_live_xxx")
    result = charges.create(
        session_id="sk_xxx",
        amount_usd=0.05,
        reference="image_gen_123"
    )
"""

from .types import (
    X402PaymentResult,
    X402PaymentRequired,
    X402Options,
    # Unified types
    MixrPayPaymentResult,
    MixrPayOptions,
    PaymentMethod,
)
from .verify import verify_x402_payment, parse_x402_payment
from .middleware import x402, x402_decorator, mixrpay, mixrpay_decorator
from .receipt import (
    verify_payment_receipt,
    parse_payment_receipt,
    is_receipt_expired,
    clear_jwks_cache,
    get_default_jwks_url,
    PaymentReceipt,
    ReceiptVerificationError,
    ReceiptExpiredError,
    InvalidReceiptSignatureError,
)
from .charges import (
    ChargesClient,
    Charge,
    CreateChargeResult,
    SessionGrant,
    SessionLimits,
    verify_session_webhook,
    parse_session_grant,
)

__version__ = "0.2.0"
__all__ = [
    # Unified Middleware (recommended)
    "mixrpay",
    "mixrpay_decorator",
    # x402-only Middleware
    "x402",
    "x402_decorator",
    # Payment verification
    "verify_x402_payment",
    "parse_x402_payment",
    # Receipt verification
    "verify_payment_receipt",
    "parse_payment_receipt",
    "is_receipt_expired",
    "clear_jwks_cache",
    "get_default_jwks_url",
    # Charges (session-based payments)
    "ChargesClient",
    "Charge",
    "CreateChargeResult",
    "SessionGrant",
    "SessionLimits",
    "verify_session_webhook",
    "parse_session_grant",
    # Unified Types
    "MixrPayPaymentResult",
    "MixrPayOptions",
    "PaymentMethod",
    # x402 Types
    "X402PaymentResult",
    "X402PaymentRequired",
    "X402Options",
    "PaymentReceipt",
    # Exceptions
    "ReceiptVerificationError",
    "ReceiptExpiredError",
    "InvalidReceiptSignatureError",
]

