"""
Pre-built FastAPI routers for Orvion payment integration.

These routers provide out-of-the-box endpoints for common payment operations,
eliminating the need for boilerplate proxy code in your application.

Usage:
    from orvion import OrvionClient
    from orvion.fastapi import create_payment_router

    client = OrvionClient(api_key="...")
    router = create_payment_router(client)
    app.include_router(router, prefix="/api/payments")

This will add:
    POST /api/payments/confirm     - Confirm wallet payment
    POST /api/payments/cancel      - Cancel pending charge
    GET  /api/payments/state/{id}  - Get charge state for UI
    GET  /api/payments/charge/{id} - Get full charge details
"""

import logging
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("orvion")


def create_payment_router(
    client: "OrvionClient",
    prefix: str = "",
    tags: Optional[list] = None,
):
    """
    Create a FastAPI router with pre-built payment endpoints.

    This router handles common payment operations so you don't need
    to write proxy endpoints in your application.

    Args:
        client: OrvionClient instance to use for API calls
        prefix: Optional prefix for all routes (default: "")
        tags: Optional list of OpenAPI tags (default: ["payments"])

    Returns:
        FastAPI APIRouter with payment endpoints

    Endpoints created:
        POST /confirm           - Confirm a wallet payment with tx_hash
        POST /cancel/{id}       - Cancel a pending charge
        GET  /state/{id}        - Get charge state for payment widget
        GET  /charge/{id}       - Get full charge details

    Example:
        from orvion import OrvionClient
        from orvion.fastapi import create_payment_router

        client = OrvionClient(api_key=os.environ["ORVION_API_KEY"])
        
        # Add router with custom prefix
        app.include_router(
            create_payment_router(client),
            prefix="/api/payments",
        )
        
        # Now available:
        # POST /api/payments/confirm
        # POST /api/payments/cancel/{transaction_id}
        # GET  /api/payments/state/{transaction_id}
        # GET  /api/payments/charge/{transaction_id}
    """
    try:
        from fastapi import APIRouter
    except ImportError:
        raise ImportError(
            "FastAPI is required for create_payment_router. "
            "Install it with: pip install fastapi"
        )

    from orvion.client import OrvionClient

    router = APIRouter(
        prefix=prefix,
        tags=tags or ["payments"],
    )

    @router.post("/confirm")
    async def confirm_payment(request: Request):
        """
        Confirm a wallet payment with blockchain transaction hash.

        Called after user signs and submits a transaction from their wallet.

        Request body:
            {
                "transaction_id": "charge_xxx",
                "tx_hash": "blockchain_tx_signature"
            }

        Returns:
            Success: {"success": true, "status": "succeeded", ...}
            Failure: {"success": false, "error": "...", ...}
        """
        try:
            body = await request.json()
        except Exception:
            return JSONResponse(
                status_code=400,
                content={"error": "invalid_json", "detail": "Request body must be valid JSON"},
            )

        transaction_id = body.get("transaction_id")
        tx_hash = body.get("tx_hash")

        if not transaction_id:
            return JSONResponse(
                status_code=400,
                content={"error": "missing_transaction_id", "detail": "transaction_id is required"},
            )

        if not tx_hash:
            return JSONResponse(
                status_code=400,
                content={"error": "missing_tx_hash", "detail": "tx_hash is required"},
            )

        try:
            result = await client.confirm_payment(
                transaction_id=transaction_id,
                tx_hash=tx_hash,
            )

            return JSONResponse(
                status_code=200 if result.success else 400,
                content={
                    "success": result.success,
                    "transaction_id": result.transaction_id,
                    "status": result.status,
                    "tx_hash": result.tx_hash,
                    "amount": result.amount,
                    "currency": result.currency,
                    "confirmed_at": result.confirmed_at,
                    "error": result.error,
                },
            )
        except Exception as e:
            logger.error(f"Failed to confirm payment: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "confirmation_failed", "detail": str(e)},
            )

    @router.post("/cancel/{transaction_id}")
    async def cancel_charge(transaction_id: str):
        """
        Cancel a pending charge.

        Use when:
        - User closes payment modal without paying
        - User explicitly cancels payment
        - Payment timeout occurs

        Returns:
            Success: {"cancelled": true}
            Failure: {"cancelled": false, "error": "..."}
        """
        try:
            success = await client.cancel_charge(transaction_id)

            if success:
                return JSONResponse(
                    status_code=200,
                    content={"cancelled": True, "transaction_id": transaction_id},
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "cancelled": False,
                        "transaction_id": transaction_id,
                        "error": "Could not cancel charge",
                    },
                )
        except Exception as e:
            logger.error(f"Failed to cancel charge {transaction_id}: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "cancel_failed", "detail": str(e)},
            )

    @router.get("/state/{transaction_id}")
    async def get_charge_state(transaction_id: str):
        """
        Get charge state for payment widget UI.

        Returns optimized data for displaying payment status,
        including recipient address, amount, and current status.

        Returns:
            ChargeState with UI-ready status information
        """
        try:
            state = await client.get_charge_state(transaction_id)

            return JSONResponse(
                status_code=200,
                content={
                    "transaction_id": state.transaction_id,
                    "status": state.status,
                    "amount": state.amount,
                    "currency": state.currency,
                    "recipient_address": state.recipient_address,
                    "token_address": state.token_address,
                    "network": state.network,
                    "display_amount": state.display_amount,
                    "qr_code_data": state.qr_code_data,
                    "created_at": state.created_at,
                    "expires_at": state.expires_at,
                    "error_message": state.error_message,
                },
            )
        except Exception as e:
            logger.error(f"Failed to get charge state for {transaction_id}: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "state_fetch_failed", "detail": str(e)},
            )

    @router.get("/charge/{transaction_id}")
    async def get_charge(transaction_id: str):
        """
        Get full charge details by ID.

        Returns complete charge information including x402_requirements.

        Returns:
            Full Charge object with all details
        """
        try:
            charge = await client.get_charge(transaction_id)

            return JSONResponse(
                status_code=200,
                content={
                    "id": charge.id,
                    "amount": charge.amount,
                    "currency": charge.currency,
                    "status": charge.status,
                    "customer_ref": charge.customer_ref,
                    "resource_ref": charge.resource_ref,
                    "x402_requirements": charge.x402_requirements,
                    "description": charge.description,
                    "created_at": charge.created_at,
                    "updated_at": charge.updated_at,
                    "return_url": charge.return_url,
                    "checkout_url": charge.checkout_url,
                    "tx_hash": charge.tx_hash,
                    "confirmed_at": charge.confirmed_at,
                },
            )
        except Exception as e:
            logger.error(f"Failed to get charge {transaction_id}: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "charge_fetch_failed", "detail": str(e)},
            )

    return router


def create_health_router(
    client: "OrvionClient",
    prefix: str = "",
    tags: Optional[list] = None,
):
    """
    Create a FastAPI router with health check endpoint.

    Args:
        client: OrvionClient instance
        prefix: Optional route prefix
        tags: Optional OpenAPI tags

    Returns:
        FastAPI APIRouter with health endpoint

    Endpoints:
        GET /health - Check API health and validate API key
    """
    try:
        from fastapi import APIRouter
    except ImportError:
        raise ImportError(
            "FastAPI is required for create_health_router. "
            "Install it with: pip install fastapi"
        )

    router = APIRouter(
        prefix=prefix,
        tags=tags or ["health"],
    )

    @router.get("/health")
    async def health_check():
        """
        Check Orvion API health and validate API key.

        Returns organization info if API key is valid.
        """
        try:
            info = await client.health_check()

            return JSONResponse(
                status_code=200 if info.api_key_valid else 401,
                content={
                    "status": info.status,
                    "organization_id": info.organization_id,
                    "organization_name": info.organization_name,
                    "environment": info.environment,
                    "api_key_valid": info.api_key_valid,
                    "version": info.version,
                    "timestamp": info.timestamp,
                },
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "error": str(e)},
            )

    return router


def create_full_router(
    client: "OrvionClient",
    prefix: str = "",
    include_health: bool = True,
):
    """
    Create a combined router with all Orvion endpoints.

    This is a convenience function that combines:
    - Payment endpoints (confirm, cancel, state, charge)
    - Health endpoint (if include_health=True)

    Args:
        client: OrvionClient instance
        prefix: Route prefix for all endpoints
        include_health: Include health check endpoint (default: True)

    Returns:
        FastAPI APIRouter with all endpoints

    Example:
        from orvion.fastapi import create_full_router

        app.include_router(
            create_full_router(client),
            prefix="/api/orvion",
        )

        # Endpoints:
        # POST /api/orvion/confirm
        # POST /api/orvion/cancel/{id}
        # GET  /api/orvion/state/{id}
        # GET  /api/orvion/charge/{id}
        # GET  /api/orvion/health
    """
    try:
        from fastapi import APIRouter
    except ImportError:
        raise ImportError(
            "FastAPI is required for create_full_router. "
            "Install it with: pip install fastapi"
        )

    main_router = APIRouter(prefix=prefix)

    # Add payment router
    payment_router = create_payment_router(client, tags=["orvion-payments"])
    main_router.include_router(payment_router)

    # Add health router
    if include_health:
        health_router = create_health_router(client, tags=["orvion-health"])
        main_router.include_router(health_router)

    return main_router
