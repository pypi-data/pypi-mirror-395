"""FastAPI middleware for Orvion payment protection"""

import logging
from typing import TYPE_CHECKING, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from orvion.client import OrvionClient

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger("orvion")


async def _scan_and_register_routes(app: ASGIApp, client: OrvionClient) -> int:
    """
    Scan FastAPI routes and register all @require_payment decorated endpoints.

    This function peels down the middleware chain to find the FastAPI app,
    then iterates through all routes looking for endpoints marked with
    the @require_payment decorator (_orvion_protected attribute).

    Args:
        app: The ASGI application (may be wrapped in middleware)
        client: OrvionClient instance to use for registration

    Returns:
        Count of routes successfully registered
    """
    try:
        from fastapi import FastAPI
        from fastapi.routing import APIRoute
    except ImportError:
        logger.warning("FastAPI not installed, cannot scan routes")
        return 0

    # Peel down middleware chain to get the underlying FastAPI app
    inner_app = app
    max_depth = 20  # Prevent infinite loops
    depth = 0
    
    while depth < max_depth:
        if isinstance(inner_app, FastAPI):
            break
        if hasattr(inner_app, "app"):
            inner_app = inner_app.app
            depth += 1
        else:
            break

    if not isinstance(inner_app, FastAPI):
        logger.warning(f"Could not find FastAPI app for route scanning (reached {type(inner_app).__name__})")
        return 0

    registered = 0
    for route in inner_app.routes:
        if not isinstance(route, APIRoute):
            continue

        endpoint = route.endpoint
        if not hasattr(endpoint, "_orvion_protected"):
            continue

        config = getattr(endpoint, "_orvion_config", {})
        methods = route.methods or {"GET"}

        # Validate amount is provided
        route_amount = config.get("amount")
        if not route_amount:
            logger.warning(
                f"Route {route.path} has @require_payment but no amount specified. Skipping registration."
            )
            continue

        for method in methods:
            try:
                route_config = await client.register_route(
                    path=route.path,
                    method=method,
                    amount=route_amount,
                    currency=config.get("currency") or "USD",
                    allow_anonymous=config.get("allow_anonymous", True),
                    name=config.get("name"),
                    description=config.get("description"),
                )
                logger.info(
                    f"Registered protected route: {method} {route.path}",
                    route_id=route_config.id,
                    route_pattern=route_config.route_pattern,
                )
                registered += 1
            except Exception as e:
                logger.error(
                    f"Failed to register route {method} {route.path}: {type(e).__name__}: {str(e)}",
                    exc_info=True,
                )

    return registered


class OrvionMiddleware(BaseHTTPMiddleware):
    """
    FastAPI/Starlette middleware that initializes the Orvion client.

    This middleware:
    1. Creates a shared OrvionClient instance
    2. Attaches it to request.state.orvion_client
    3. Scans and registers @require_payment decorated routes on first request
    4. Pre-fetches route configurations for caching

    Usage:
        app.add_middleware(
            OrvionMiddleware,
            api_key=os.environ["ORVION_API_KEY"],
        )

    For true startup registration (before any requests), use sync_routes() in lifespan:

        from orvion.fastapi import sync_routes

        @asynccontextmanager
        async def lifespan(app):
            client = OrvionClient(api_key=API_KEY)
            await sync_routes(app, client)
            yield
            await client.close()

        app = FastAPI(lifespan=lifespan)
        app.add_middleware(OrvionMiddleware, api_key=API_KEY, register_on_first_request=False)
    """

    def __init__(
        self,
        app: ASGIApp,
        api_key: str,
        base_url: Optional[str] = None,
        cache_ttl_seconds: float = 60.0,
        transaction_header: str = "X-Transaction-Id",
        customer_header: str = "X-Customer-Id",
        register_on_first_request: bool = True,
    ):
        """
        Initialize the Orvion middleware.

        Args:
            app: The ASGI application
            api_key: Orvion API key
            base_url: Custom API base URL
            cache_ttl_seconds: Route cache TTL (default 60s)
            transaction_header: Header name for transaction ID
            customer_header: Header name for customer ID
            register_on_first_request: Auto-register decorated routes on first request (default True).
                                       Set to False if using sync_routes() in lifespan.
        """
        super().__init__(app)
        self._original_app = app  # Store reference to original app for route scanning
        self.client = OrvionClient(
            api_key=api_key,
            base_url=base_url,
            cache_ttl_seconds=cache_ttl_seconds,
        )
        self.transaction_header = transaction_header
        self.customer_header = customer_header
        self._register_on_first_request = register_on_first_request
        self._routes_registered = False

    async def dispatch(self, request: Request, call_next):
        """Process request and attach Orvion client to state."""
        # Register routes on first request (app is fully loaded at this point)
        if self._register_on_first_request and not self._routes_registered:
            try:
                # Use request.app which is the FastAPI instance
                fastapi_app = request.app
                count = await _scan_and_register_routes(fastapi_app, self.client)
                logger.info(f"Orvion: Registered {count} protected routes on startup")
            except Exception as e:
                logger.error(f"Failed to register routes on startup: {str(e)}", exc_info=True)
            finally:
                self._routes_registered = True

        # Attach client and config to request state
        request.state.orvion_client = self.client
        request.state.orvion_transaction_header = self.transaction_header
        request.state.orvion_customer_header = self.customer_header

        # Pre-fetch routes if cache is empty or expired (non-blocking)
        if self.client._cache.is_expired():
            try:
                await self.client.get_routes()
            except Exception as e:
                logger.warning(f"Failed to pre-fetch routes: {e}")

        response = await call_next(request)
        return response
