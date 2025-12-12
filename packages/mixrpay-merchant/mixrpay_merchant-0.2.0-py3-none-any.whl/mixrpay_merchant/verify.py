"""
MixrPay Merchant SDK - Payment Verification
"""

import base64
import json
import time
from datetime import datetime
from typing import Optional

import httpx
from eth_account.messages import encode_typed_data
from eth_account import Account

from .types import X402PaymentResult, VerifyOptions


# USDC contracts by chain ID
USDC_CONTRACTS = {
    8453: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",   # Base Mainnet
    84532: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # Base Sepolia
}

# EIP-712 types for TransferWithAuthorization
TRANSFER_TYPES = {
    "TransferWithAuthorization": [
        {"name": "from", "type": "address"},
        {"name": "to", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "validAfter", "type": "uint256"},
        {"name": "validBefore", "type": "uint256"},
        {"name": "nonce", "type": "bytes32"},
    ]
}


def get_usdc_domain(chain_id: int) -> dict:
    """Get EIP-712 domain for USDC on the specified chain."""
    contract = USDC_CONTRACTS.get(chain_id)
    if not contract:
        raise ValueError(f"Unsupported chain ID: {chain_id}")
    
    return {
        "name": "USD Coin",
        "version": "2",
        "chainId": chain_id,
        "verifyingContract": contract,
    }


def minor_to_usd(minor: int) -> float:
    """Convert USDC minor units to USD dollars."""
    return minor / 1_000_000


def usd_to_minor(usd: float) -> int:
    """Convert USD dollars to USDC minor units."""
    return int(round(usd * 1_000_000))


async def verify_x402_payment(
    payment_header: str,
    options: VerifyOptions,
) -> X402PaymentResult:
    """
    Verify an X-PAYMENT header and optionally settle the payment.
    
    Args:
        payment_header: The X-PAYMENT header value (base64 encoded JSON)
        options: Verification options
        
    Returns:
        X402PaymentResult with verification result
        
    Example:
        result = await verify_x402_payment(
            payment_header,
            VerifyOptions(
                expected_amount=50000,  # 0.05 USDC
                expected_recipient="0x...",
            )
        )
        
        if result.valid:
            print(f"Payment from {result.payer}: ${result.amount}")
    """
    try:
        # 1. Decode the X-PAYMENT header
        try:
            json_str = base64.b64decode(payment_header).decode("utf-8")
            decoded = json.loads(json_str)
        except Exception as e:
            return X402PaymentResult(valid=False, error=f"Invalid payment header encoding: {e}")
        
        # 2. Validate payload structure
        payload = decoded.get("payload", {})
        authorization = payload.get("authorization")
        signature = payload.get("signature")
        
        if not authorization or not signature:
            return X402PaymentResult(valid=False, error="Missing authorization or signature")
        
        # 3. Build EIP-712 message for verification
        chain_id = options.chain_id
        domain = get_usdc_domain(chain_id)
        
        message = {
            "from": authorization["from"],
            "to": authorization["to"],
            "value": int(authorization["value"]),
            "validAfter": int(authorization["validAfter"]),
            "validBefore": int(authorization["validBefore"]),
            "nonce": authorization["nonce"],
        }
        
        # 4. Recover signer address
        try:
            typed_data = {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chainId", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"},
                    ],
                    **TRANSFER_TYPES
                },
                "primaryType": "TransferWithAuthorization",
                "domain": domain,
                "message": message,
            }
            
            signable = encode_typed_data(full_message=typed_data)
            signer_address = Account.recover_message(signable, signature=signature)
        except Exception as e:
            return X402PaymentResult(valid=False, error=f"Failed to recover signer: {e}")
        
        # 5. Verify signer matches 'from' address
        if signer_address.lower() != authorization["from"].lower():
            return X402PaymentResult(
                valid=False, 
                error=f"Signature mismatch: expected {authorization['from']}, got {signer_address}"
            )
        
        # 6. Verify payment amount
        payment_amount = int(authorization["value"])
        if payment_amount < options.expected_amount:
            return X402PaymentResult(
                valid=False,
                error=f"Insufficient payment: expected {options.expected_amount}, got {payment_amount}"
            )
        
        # 7. Verify recipient
        if authorization["to"].lower() != options.expected_recipient.lower():
            return X402PaymentResult(
                valid=False,
                error=f"Wrong recipient: expected {options.expected_recipient}, got {authorization['to']}"
            )
        
        # 8. Check expiration
        now = int(time.time())
        valid_before = int(authorization["validBefore"])
        if valid_before < now:
            return X402PaymentResult(valid=False, error="Payment authorization has expired")
        
        # 9. Check validAfter
        valid_after = int(authorization["validAfter"])
        if valid_after > now:
            return X402PaymentResult(valid=False, error="Payment authorization is not yet valid")
        
        # 10. Submit to facilitator for settlement (unless skipped)
        tx_hash: Optional[str] = None
        settled_at: Optional[datetime] = None
        
        if not options.skip_settlement:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{options.facilitator}/settle",
                        json={
                            "authorization": authorization,
                            "signature": signature,
                            "chainId": chain_id,
                        },
                        timeout=30.0,
                    )
                
                if response.status_code != 200:
                    error_body = response.text
                    try:
                        error_json = response.json()
                        error_body = error_json.get("message", error_json.get("error", error_body))
                    except Exception:
                        pass
                    return X402PaymentResult(valid=False, error=f"Settlement failed: {error_body}")
                
                settlement = response.json()
                tx_hash = settlement.get("txHash") or settlement.get("tx_hash")
                settled_at = datetime.now()
                
            except Exception as e:
                return X402PaymentResult(valid=False, error=f"Settlement request failed: {e}")
        
        # Success!
        return X402PaymentResult(
            valid=True,
            payer=authorization["from"],
            amount=minor_to_usd(payment_amount),
            amount_minor=payment_amount,
            tx_hash=tx_hash,
            settled_at=settled_at or datetime.now(),
            nonce=authorization["nonce"],
        )
        
    except Exception as e:
        return X402PaymentResult(valid=False, error=f"Verification error: {e}")


def verify_x402_payment_sync(
    payment_header: str,
    options: VerifyOptions,
) -> X402PaymentResult:
    """
    Synchronous version of verify_x402_payment.
    Uses httpx in sync mode for settlement.
    """
    try:
        # 1. Decode the X-PAYMENT header
        try:
            json_str = base64.b64decode(payment_header).decode("utf-8")
            decoded = json.loads(json_str)
        except Exception as e:
            return X402PaymentResult(valid=False, error=f"Invalid payment header encoding: {e}")
        
        # 2. Validate payload structure
        payload = decoded.get("payload", {})
        authorization = payload.get("authorization")
        signature = payload.get("signature")
        
        if not authorization or not signature:
            return X402PaymentResult(valid=False, error="Missing authorization or signature")
        
        # 3. Build EIP-712 message for verification
        chain_id = options.chain_id
        domain = get_usdc_domain(chain_id)
        
        message = {
            "from": authorization["from"],
            "to": authorization["to"],
            "value": int(authorization["value"]),
            "validAfter": int(authorization["validAfter"]),
            "validBefore": int(authorization["validBefore"]),
            "nonce": authorization["nonce"],
        }
        
        # 4. Recover signer address
        try:
            typed_data = {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chainId", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"},
                    ],
                    **TRANSFER_TYPES
                },
                "primaryType": "TransferWithAuthorization",
                "domain": domain,
                "message": message,
            }
            
            signable = encode_typed_data(full_message=typed_data)
            signer_address = Account.recover_message(signable, signature=signature)
        except Exception as e:
            return X402PaymentResult(valid=False, error=f"Failed to recover signer: {e}")
        
        # 5. Verify signer matches 'from' address
        if signer_address.lower() != authorization["from"].lower():
            return X402PaymentResult(
                valid=False,
                error=f"Signature mismatch"
            )
        
        # 6. Verify payment amount
        payment_amount = int(authorization["value"])
        if payment_amount < options.expected_amount:
            return X402PaymentResult(
                valid=False,
                error=f"Insufficient payment"
            )
        
        # 7. Verify recipient
        if authorization["to"].lower() != options.expected_recipient.lower():
            return X402PaymentResult(valid=False, error=f"Wrong recipient")
        
        # 8. Check expiration
        now = int(time.time())
        if int(authorization["validBefore"]) < now:
            return X402PaymentResult(valid=False, error="Authorization expired")
        
        # 9. Submit to facilitator for settlement (unless skipped)
        tx_hash: Optional[str] = None
        settled_at: Optional[datetime] = None
        
        if not options.skip_settlement:
            try:
                response = httpx.post(
                    f"{options.facilitator}/settle",
                    json={
                        "authorization": authorization,
                        "signature": signature,
                        "chainId": chain_id,
                    },
                    timeout=30.0,
                )
                
                if response.status_code != 200:
                    return X402PaymentResult(valid=False, error="Settlement failed")
                
                settlement = response.json()
                tx_hash = settlement.get("txHash") or settlement.get("tx_hash")
                settled_at = datetime.now()
                
            except Exception as e:
                return X402PaymentResult(valid=False, error=f"Settlement request failed: {e}")
        
        return X402PaymentResult(
            valid=True,
            payer=authorization["from"],
            amount=minor_to_usd(payment_amount),
            amount_minor=payment_amount,
            tx_hash=tx_hash,
            settled_at=settled_at or datetime.now(),
            nonce=authorization["nonce"],
        )
        
    except Exception as e:
        return X402PaymentResult(valid=False, error=f"Verification error: {e}")


async def parse_x402_payment(
    payment_header: str,
    chain_id: int = 8453,
) -> X402PaymentResult:
    """
    Parse and validate an X-PAYMENT header without settlement.
    Useful for checking if a payment is structurally valid.
    """
    try:
        json_str = base64.b64decode(payment_header).decode("utf-8")
        decoded = json.loads(json_str)
        
        payload = decoded.get("payload", {})
        authorization = payload.get("authorization")
        signature = payload.get("signature")
        
        if not authorization:
            return X402PaymentResult(valid=False, error="Missing authorization")
        
        # Verify signature
        domain = get_usdc_domain(chain_id)
        message = {
            "from": authorization["from"],
            "to": authorization["to"],
            "value": int(authorization["value"]),
            "validAfter": int(authorization["validAfter"]),
            "validBefore": int(authorization["validBefore"]),
            "nonce": authorization["nonce"],
        }
        
        typed_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                **TRANSFER_TYPES
            },
            "primaryType": "TransferWithAuthorization",
            "domain": domain,
            "message": message,
        }
        
        signable = encode_typed_data(full_message=typed_data)
        signer_address = Account.recover_message(signable, signature=signature)
        
        if signer_address.lower() != authorization["from"].lower():
            return X402PaymentResult(valid=False, error="Signature mismatch")
        
        payment_amount = int(authorization["value"])
        
        return X402PaymentResult(
            valid=True,
            payer=authorization["from"],
            amount=minor_to_usd(payment_amount),
            amount_minor=payment_amount,
        )
        
    except Exception as e:
        return X402PaymentResult(valid=False, error=f"Parse error: {e}")

