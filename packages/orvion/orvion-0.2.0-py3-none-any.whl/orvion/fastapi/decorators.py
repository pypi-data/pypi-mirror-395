"""FastAPI decorators for payment protection"""

import logging
from functools import wraps
from typing import Any, Callable, Optional

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from orvion.client import OrvionClient
from orvion.exceptions import OrvionAPIError
from orvion.models import PaymentInfo

logger = logging.getLogger("orvion")


def _is_browser_request(request: Request) -> bool:
    """Check if request is from a browser (vs API client)."""
    accept = request.headers.get("accept", "")
    return "text/html" in accept.lower()


def _error_response(request: Request, status_code: int, error: str, detail: str) -> Any:
    """Return HTML error page for browser requests, JSON for API requests."""
    if _is_browser_request(request):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Error {status_code}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
        h1 {{ color: #dc2626; }}
        .error {{ background: #fef2f2; border: 1px solid #fecaca; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .detail {{ color: #7f1d1d; font-family: monospace; white-space: pre-wrap; }}
        code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>Error {status_code}: {error}</h1>
    <div class="error">
        <div class="detail">{detail}</div>
    </div>
    <p><a href="/">← Back to home</a></p>
</body>
</html>"""
        return HTMLResponse(status_code=status_code, content=html)
    else:
        return JSONResponse(status_code=status_code, content={"error": error, "detail": detail})


def require_payment(
    amount: Optional[str] = None,
    currency: str = "USD",
    allow_anonymous: Optional[bool] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    customer_resolver: Optional[Callable[[Request], str]] = None,
    transaction_header: Optional[str] = None,
    customer_header: Optional[str] = None,
    hosted_checkout: bool = False,
    return_url: Optional[str] = None,
):
    """
    Decorator to require payment for a FastAPI endpoint.

    IMPORTANT: Place @require_payment UNDER @app.get/@app.post:

        @app.get("/api/premium")
        @require_payment(amount="0.01", currency="USDC")
        async def premium(request: Request):
            return {"data": "premium"}

    Routes are registered on app startup via OrvionMiddleware.
    If a route is not found at runtime, the request will fail with 500.

    This decorator supports two modes:
    1. **402 mode (default)**: Returns 402 Payment Required with x402 requirements
    2. **Hosted checkout mode**: Redirects buyer to Orvion checkout page

    For 402 mode, the decorator:
    1. Looks up the route configuration (registered on startup)
    2. If no transaction header: creates a charge and returns 402
    3. If transaction header present: verifies payment and allows access
    4. Attaches payment info to request.state.payment

    For hosted checkout mode (hosted_checkout=True):
    1. If no charge_id query param: creates charge with return_url, redirects to checkout_url
    2. If charge_id present: verifies payment and redirects to frontend page with success params
    3. Convention: If API is at /api/foo, frontend page is assumed to be at /foo
       - return_url is auto-derived as /foo (for checkout redirect back)
       - After verification, user is redirected to /foo?charge_id=xxx&status=succeeded

    Args:
        amount: Price amount (required for startup registration)
        currency: Currency code (default USD)
        allow_anonymous: Allow requests without customer ID (default True)
        name: User-friendly name for the route
        description: Description shown in 402 response
        customer_resolver: Custom function to extract customer ID from request
        transaction_header: Override transaction header name
        customer_header: Override customer header name
        hosted_checkout: Use hosted checkout redirect flow (default False for backwards compat)
        return_url: URL to redirect buyer after payment. If not provided, auto-derived using
                    convention: /api/foo → /foo. This ensures users land on frontend pages,
                    not API endpoints returning JSON.

    Usage (402 mode - default):
        @app.get("/api/premium/data")
        @require_payment(amount="0.10", currency="USDC")
        async def premium_data(request: Request):
            return {"data": "premium"}

    Usage (hosted checkout mode):
        @app.get("/api/premium/hosted")
        @require_payment(amount="0.10", currency="USDC", hosted_checkout=True)
        async def premium_hosted(request: Request):
            return {"data": "premium"}

    MVP note: Caching can be skipped - it's okay to call /v1/charges/verify on every request.
    Add in-memory cache later for optimization.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            # Get client from middleware
            client: Optional[OrvionClient] = getattr(request.state, "orvion_client", None)
            if client is None:
                logger.error("OrvionMiddleware not configured")
                return _error_response(
                    request,
                    status_code=500,
                    error="Internal server error",
                    detail="Payment middleware not configured. Ensure OrvionMiddleware is added to your FastAPI app.",
                )

            # Get header names
            tx_header = transaction_header or getattr(request.state, "orvion_transaction_header", "X-Transaction-Id")
            cust_header = customer_header or getattr(request.state, "orvion_customer_header", "X-Customer-Id")

            # Derive route pattern from FastAPI route template (not the concrete URL path)
            # This stores stable patterns like /api/articles/{slug} instead of /api/articles/123
            route_obj = request.scope.get("route")
            if route_obj is not None:
                route_pattern = getattr(route_obj, "path", request.url.path)
            else:
                route_pattern = request.url.path
            method = request.method.upper()

            # Step 1: Route lookup from cache - MUST exist (registered on startup)
            try:
                route = await client.match_route(route_pattern, method)
            except Exception as e:
                logger.error(f"Failed to match route {method} {route_pattern}: {e}", exc_info=True)
                return _error_response(
                    request,
                    status_code=500,
                    error="Internal server error",
                    detail=f"Failed to lookup route configuration: {str(e)}",
                )

            # Step 2: Fail loudly if route not found - should have been registered on startup
            if route is None:
                logger.error(
                    f"Route {method} {route_pattern} not registered. "
                    "Did OrvionMiddleware scan run? Check decorator order: @app.get must come before @require_payment"
                )
                detail = (
                    f"Protected route {method} {route_pattern} not found in Orvion.\n\n"
                    "This usually means:\n"
                    "1. The route hasn't been registered yet (first request triggers registration)\n"
                    "2. OrvionMiddleware is not configured properly\n"
                    "3. Decorator order is wrong: @app.get/@app.post must come BEFORE @require_payment\n"
                    "4. The route was registered but with a different pattern\n\n"
                    "Check server logs for route registration messages."
                )
                return _error_response(
                    request,
                    status_code=500,
                    error="Route not registered",
                    detail=detail,
                )

            # Step 2.5: Check route status - if paused, allow free access without payment
            route_status = getattr(route, "status", "active")
            if route_status == "paused":
                # Route is paused - allow free access without payment check
                logger.debug(f"Route {method} {route_pattern} is paused - allowing free access")
                # Attach empty payment info to indicate no payment was required
                request.state.payment = None
                # Continue to the actual endpoint handler
                return await func(request, *args, **kwargs)

            # Step 3: Resolve configuration from route (dashboard is source of truth)
            resolved_amount = route.amount
            resolved_currency = route.currency
            resolved_allow_anonymous = route.allow_anonymous

            # Step 4: Build customer identifier
            customer_ref: Optional[str] = None

            # Try custom resolver first
            if customer_resolver is not None:
                try:
                    customer_ref = customer_resolver(request)
                except Exception as e:
                    logger.error(f"customer_resolver failed: {e}")
                    return JSONResponse(
                        status_code=500,
                        content={"error": "Internal server error", "detail": "Failed to resolve customer"},
                    )

            # Fall back to header
            if customer_ref is None:
                customer_ref = request.headers.get(cust_header)

            # Handle missing customer
            if customer_ref is None:
                if not resolved_allow_anonymous:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Bad Request",
                            "detail": f"Customer identification required. Provide {cust_header} header.",
                        },
                    )
                customer_ref = "anonymous"

            # Resource ref for security
            resource_ref = f"protected_route:{route.id}"

            # =========================================================================
            # Hosted Checkout Mode
            # =========================================================================
            if hosted_checkout:
                # Check for charge_id in query params (return from checkout)
                charge_id = request.query_params.get("charge_id")

                if charge_id:
                    # Buyer returned from checkout - verify payment
                    try:
                        result = await client.verify_charge(
                            transaction_id=charge_id,
                            customer_ref=customer_ref if customer_ref != "anonymous" else None,
                            resource_ref=resource_ref,
                        )

                        if result.verified:
                            # Payment verified - redirect to frontend page with success indicator
                            # This gives users a proper UI experience instead of raw JSON
                            from urllib.parse import urlparse, urlunparse, urlencode
                            
                            request_url = str(request.url).split("?")[0]
                            parsed = urlparse(request_url)
                            path = parsed.path
                            
                            # Derive frontend path (strip /api prefix)
                            if path.startswith("/api/"):
                                frontend_path = path[4:]
                            elif path.startswith("/api"):
                                frontend_path = path[3:] or "/"
                            else:
                                frontend_path = path
                            
                            # Build redirect URL with success params
                            success_params = urlencode({
                                "charge_id": charge_id,
                                "status": "succeeded",
                            })
                            
                            redirect_url = urlunparse((
                                parsed.scheme,
                                parsed.netloc,
                                frontend_path,
                                "",
                                success_params,
                                ""
                            ))
                            
                            logger.info(f"Payment verified for {charge_id}, redirecting to: {redirect_url}")
                            return RedirectResponse(url=redirect_url, status_code=302)
                        else:
                            # Not verified - redirect to checkout again
                            logger.warning(f"Charge {charge_id} not verified: {result.reason}")
                            # Fall through to create new charge
                    except Exception as e:
                        logger.error(f"Failed to verify charge {charge_id}: {e}")
                        # Fall through to create new charge

                # No charge_id or verification failed - create charge and redirect
                try:
                    # Derive return_url from request if not provided
                    resolved_return_url = return_url
                    if not resolved_return_url:
                        # Build return_url from request, using convention to derive frontend page
                        # If API is at /api/foo, frontend is likely at /foo
                        request_url = str(request.url).split("?")[0]
                        
                        # Parse the URL to modify the path
                        from urllib.parse import urlparse, urlunparse
                        parsed = urlparse(request_url)
                        path = parsed.path
                        
                        # Strip /api prefix for frontend URL (convention-based)
                        if path.startswith("/api/"):
                            frontend_path = path[4:]  # Remove "/api" prefix
                        elif path.startswith("/api"):
                            frontend_path = path[3:] or "/"  # Handle /api without trailing slash
                        else:
                            frontend_path = path  # No /api prefix, use as-is
                        
                        # Rebuild URL with frontend path
                        resolved_return_url = urlunparse((
                            parsed.scheme,
                            parsed.netloc,
                            frontend_path,
                            parsed.params,
                            "",  # No query string
                            parsed.fragment
                        ))
                        
                        logger.debug(f"Derived return_url: {resolved_return_url} from API path: {path}")

                    charge = await client.create_charge(
                        amount=resolved_amount,
                        currency=resolved_currency,
                        customer_ref=customer_ref,
                        resource_ref=resource_ref,
                        description=route.description,
                        metadata={"path": str(request.url.path), "method": request.method},
                        return_url=resolved_return_url,
                    )

                    if not charge.checkout_url:
                        logger.error("No checkout_url in charge response")
                        return _error_response(
                            request,
                            status_code=500,
                            error="Internal server error",
                            detail="Hosted checkout not available. The charge was created but no checkout_url was returned.",
                        )

                    # Redirect to hosted checkout
                    return RedirectResponse(url=charge.checkout_url, status_code=302)

                except OrvionAPIError as e:
                    # Surface API errors with helpful messages
                    error_code = None
                    error_detail = None
                    if e.response_body:
                        error_code = e.response_body.get("error")
                        error_detail = e.response_body.get("detail", str(e))
                    
                    logger.error(f"Orvion API error creating charge: {error_code} - {error_detail}")
                    
                    # Handle specific error cases
                    if error_code == "invalid_return_url":
                        detail = error_detail or (
                            "return_url not in allowed domains.\n\n"
                            "To fix this:\n"
                            "1. Go to your Orvion dashboard → Settings → Domains\n"
                            "2. Add your domain (e.g., http://localhost:5002 or https://yourapp.com)\n"
                            f"3. The current return_url was: {resolved_return_url}"
                        )
                        return _error_response(
                            request,
                            status_code=400,
                            error="invalid_return_url",
                            detail=detail,
                        )
                    
                    # Return a user-friendly error for other API errors
                    return _error_response(
                        request,
                        status_code=500,
                        error="Payment service error",
                        detail=f"{error_detail or str(e)}\n\nError code: {error_code or 'unknown'}",
                    )
                except Exception as e:
                    logger.error(f"Failed to create charge for hosted checkout: {e}", exc_info=True)
                    return _error_response(
                        request,
                        status_code=500,
                        error="Internal server error",
                        detail=f"Failed to create payment charge: {str(e)}",
                    )

            # =========================================================================
            # 402 Mode (Default)
            # =========================================================================
            # Step 5: Check for transaction header
            transaction_id = request.headers.get(tx_header)

            if transaction_id is None:
                # No payment - create charge and return 402
                try:
                    charge = await client.create_charge(
                        amount=resolved_amount,
                        currency=resolved_currency,
                        customer_ref=customer_ref,
                        resource_ref=resource_ref,
                        description=route.description,
                        metadata={"path": str(request.url.path), "method": request.method},
                    )

                    response = JSONResponse(
                        status_code=402,
                        content={
                            "error": "Payment Required",
                            "charge_id": charge.id,
                            "amount": charge.amount,
                            "currency": charge.currency,
                            "x402": charge.x402_requirements,
                            "x402_requirements": charge.x402_requirements,
                            "description": route.description,
                        },
                    )
                    response.headers["X-Payment-Required"] = "true"
                    return response
                except Exception as e:
                    logger.error(f"Failed to create charge: {e}")
                    return JSONResponse(
                        status_code=500,
                        content={"error": "Internal server error", "detail": "Failed to create payment charge"},
                    )

            # Step 6: Verify payment
            try:
                result = await client.verify_charge(
                    transaction_id=transaction_id,
                    customer_ref=customer_ref if customer_ref != "anonymous" else None,
                    resource_ref=resource_ref,
                )

                # Security check: resource_ref must match
                if not result.verified:
                    return JSONResponse(
                        status_code=402,
                        content={
                            "error": "Payment verification failed",
                            "reason": result.reason or "Verification failed",
                        },
                    )

                if result.resource_ref != resource_ref:
                    logger.warning(
                        f"resource_ref mismatch: expected {resource_ref}, got {result.resource_ref}"
                    )
                    return JSONResponse(
                        status_code=402,
                        content={
                            "error": "Payment verification failed",
                            "reason": "resource_ref_mismatch",
                        },
                    )

                # Attach payment info to request
                request.state.payment = PaymentInfo.from_verify_result(result, route_id=route.id)

                # Call the actual endpoint
                return await func(request, *args, **kwargs)

            except Exception as e:
                logger.error(f"Failed to verify payment: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": "Internal server error", "detail": "Failed to verify payment"},
                )

        # Mark wrapper for startup route scanning by middleware
        wrapper._orvion_protected = True
        wrapper._orvion_config = {
            "amount": amount,
            "currency": currency,
            "allow_anonymous": allow_anonymous if allow_anonymous is not None else True,
            "name": name,
            "description": description,
            "hosted_checkout": hosted_checkout,
            "return_url": return_url,
        }

        return wrapper

    return decorator
