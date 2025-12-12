# mixrpay-merchant

Accept payments from AI agents and web apps with one middleware. Supports session-based payments (Agent SDK, Widget) and x402 protocol.

## Installation

```bash
# For FastAPI
pip install mixrpay-merchant[fastapi]

# For Flask
pip install mixrpay-merchant[flask]

# For both
pip install mixrpay-merchant[all]
```

## Quick Start

### 1. Set Environment Variables

```bash
export MIXRPAY_PUBLIC_KEY=pk_live_...
export MIXRPAY_SECRET_KEY=sk_live_...

# Optional: for x402 protocol support
export MIXRPAY_MERCHANT_ADDRESS=0xYourWalletAddress
```

### 2. Add to Your Routes

#### FastAPI

```python
from fastapi import FastAPI, Depends
from mixrpay_merchant import mixrpay, MixrPayment

app = FastAPI()

# Accepts payments from Widget, Agent SDK, and x402 agents
@app.post("/api/generate")
async def generate(payment: MixrPayment = Depends(mixrpay(price_usd=0.05))):
    # Payment verified!
    print(f"Payment: ${payment.amount_usd} via {payment.method} from {payment.payer}")
    
    return {"result": "success", "payer": payment.payer}


# Dynamic pricing
@app.post("/api/ai")
async def ai_query(
    payment: MixrPayment = Depends(mixrpay(
        get_price=lambda req: 0.10 if req.query_params.get("premium") else 0.05
    ))
):
    return {"result": "success"}
```

#### Flask

```python
from flask import Flask, jsonify, request
from mixrpay_merchant.flask import mixrpay

app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
@mixrpay(price_usd=0.05)
def generate():
    # Access payment result via request.mixr_payment
    payment = request.mixr_payment
    
    print(f"Paid by {payment.payer}: ${payment.amount_usd} via {payment.method}")
    
    return jsonify({"result": "success", "payer": payment.payer})
```

## Accepted Payment Methods

The middleware automatically handles **three payment methods**:

| Header | Source | Description |
|--------|--------|-------------|
| `X-Mixr-Session` | Agent SDK | Session-based payment (recommended for MixrPay clients) |
| `X-Mixr-Payment` | Widget | Widget payment proof JWT |
| `X-PAYMENT` | x402 | External agent payment via x402 protocol |

```python
@app.post("/api/generate")
async def generate(payment: MixrPayment = Depends(mixrpay(price_usd=0.05))):
    match payment.method:
        case "session":
            print("Payment from Agent SDK")
        case "widget":
            print("Payment from Widget user")
        case "x402":
            print("Payment from external x402 agent")
    
    return {"result": "success"}
```

## How It Works

### Session-Based Flow (Agent SDK / Widget)

```
Agent/User                    Your API                    MixrPay
    │                            │                           │
    │  1. Request with           │                           │
    │     X-Mixr-Session header  │                           │
    ├───────────────────────────▶│                           │
    │                            │  2. Validate session      │
    │                            ├──────────────────────────▶│
    │                            │◀──────────────────────────┤
    │  3. Response               │                           │
    │◀───────────────────────────┤                           │
```

### x402 Flow (External Agents)

```
Agent                        Your API                    Facilitator
    │                            │                           │
    │  1. Request (no payment)   │                           │
    ├───────────────────────────▶│                           │
    │◀── 402 Payment Required ───┤                           │
    │                            │                           │
    │  2. Request with           │                           │
    │     X-PAYMENT header       │                           │
    ├───────────────────────────▶│                           │
    │                            │  3. Verify & settle       │
    │                            ├──────────────────────────▶│
    │                            │◀──────────────────────────┤
    │  4. Response               │                           │
    │◀───────────────────────────┤                           │
```

## Configuration Options

### mixrpay() Parameters

```python
mixrpay(
    # Price in USD (e.g., 0.05 for 5 cents)
    price_usd=0.05,
    
    # Your keys (defaults to env vars)
    public_key="pk_live_...",
    secret_key="sk_live_...",
    
    # Wallet address for x402 (defaults to MIXRPAY_MERCHANT_ADDRESS env)
    merchant_address="0x...",
    
    # x402 facilitator URL
    facilitator="https://x402.org/facilitator",
    
    # Description shown to payer
    description="API query fee",
    
    # Test mode - accepts test payments
    test_mode=False,
    
    # Dynamic pricing function
    get_price=lambda req: calculate_price(req),
    
    # Callback after successful payment
    on_payment=lambda payment: log_payment(payment),
    
    # Skip payment for certain requests
    skip=lambda req: req.headers.get("X-Premium-Token") == "valid",
)
```

### MixrPayment

```python
@dataclass
class MixrPayment:
    valid: bool              # Whether payment is valid
    method: str              # 'session' | 'widget' | 'x402'
    payer: str               # Payer's wallet address
    amount_usd: float        # Amount paid in USD
    session_id: str | None   # Session ID (for session-based)
    charge_id: str | None    # Charge record ID
    tx_hash: str | None      # Transaction hash (for x402)
    timestamp: datetime      # When payment was made
    error: str | None        # Error message if invalid
```

## Advanced Usage

### Dynamic Pricing (FastAPI)

```python
from fastapi import Request

async def calculate_price(request: Request) -> float:
    body = await request.json()
    model = body.get("model", "basic")
    tokens = body.get("tokens", 1000)
    
    rates = {"gpt-4": 0.03, "gpt-3.5": 0.002, "basic": 0.01}
    return rates.get(model, 0.01) * (tokens / 1000)

@app.post("/api/ai")
async def ai_query(
    payment: MixrPayment = Depends(mixrpay(get_price=calculate_price))
):
    return {"result": "success"}
```

### Skip Payment for Certain Requests

```python
async def is_premium_user(request: Request) -> bool:
    token = request.headers.get("Authorization")
    if not token:
        return False
    user = await get_user(token)
    return user and user.is_premium

@app.post("/api/query")
async def query(
    payment: MixrPayment = Depends(mixrpay(price_usd=0.05, skip=is_premium_user))
):
    return {"result": "success"}
```

### Payment Callbacks

```python
async def log_payment(payment: MixrPayment):
    # Log to analytics
    await analytics.track("payment_received", {
        "payer": payment.payer,
        "amount": payment.amount_usd,
        "method": payment.method,
    })
    
    # Store in database
    await db.payments.create(
        payer=payment.payer,
        amount=payment.amount_usd,
        charge_id=payment.charge_id,
    )

@app.post("/api/query")
async def query(
    payment: MixrPayment = Depends(mixrpay(price_usd=0.05, on_payment=log_payment))
):
    return {"result": "success"}
```

### Manual Verification

```python
from mixrpay_merchant import verify_mixr_payment, VerifyOptions

result = await verify_mixr_payment(
    headers=request.headers,
    options=VerifyOptions(
        public_key=os.environ["MIXRPAY_PUBLIC_KEY"],
        secret_key=os.environ["MIXRPAY_SECRET_KEY"],
        expected_amount=0.05,
    )
)

if result.valid:
    print(f"Valid payment from {result.payer} via {result.method}")
```

## Testing

Enable test mode to accept test payments during development:

```python
import os

@app.post("/api/query")
async def query(
    payment: MixrPayment = Depends(mixrpay(
        price_usd=0.05,
        test_mode=os.environ.get("ENV") != "production"
    ))
):
    return {"result": "success"}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MIXRPAY_PUBLIC_KEY` | Your merchant public key (pk_...) | Yes |
| `MIXRPAY_SECRET_KEY` | Your merchant secret key | Yes |
| `MIXRPAY_MERCHANT_ADDRESS` | Wallet address for x402 payments | For x402 |

## Supported Chains

| Chain | Chain ID | USDC Contract |
|-------|----------|---------------|
| Base Mainnet | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

## Error Handling

The middleware returns appropriate HTTP status codes:

- `402 Payment Required` - No payment or invalid payment
- `403 Forbidden` - Session limit exceeded or revoked
- `500 Internal Server Error` - Configuration issues

Error responses include details:

```json
{
  "error": "payment_required",
  "message": "No valid payment provided",
  "payment_info": {
    "price_usd": 0.05,
    "recipient": "0x...",
    "accepted_methods": ["X-Mixr-Session", "X-Mixr-Payment", "X-PAYMENT"]
  }
}
```

## Migration from x402-Only

If you were using the old x402-only middleware:

```python
# Before (x402 only)
from mixrpay_merchant import x402

@app.post("/api/query")
async def query(payment = Depends(x402(price=0.05))):
    ...

# After (unified - backwards compatible)
from mixrpay_merchant import mixrpay

@app.post("/api/query")
async def query(payment = Depends(mixrpay(price_usd=0.05))):
    ...
```

The new `mixrpay` middleware is backwards compatible—it still accepts x402 payments via `X-PAYMENT` header, but now also accepts session-based payments.

## License

MIT
