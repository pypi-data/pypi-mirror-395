"""FastAPI integration for Orvion SDK"""

from typing import TYPE_CHECKING

from orvion.fastapi.decorators import require_payment
from orvion.fastapi.middleware import OrvionMiddleware, _scan_and_register_routes
from orvion.fastapi.routers import (
    create_full_router,
    create_health_router,
    create_payment_router,
)

if TYPE_CHECKING:
    from fastapi import FastAPI
    from orvion.client import OrvionClient


async def sync_routes(app: "FastAPI", client: "OrvionClient") -> int:
    """
    Explicitly register all @require_payment decorated routes with Orvion.

    Use this in FastAPI lifespan for true startup registration (before any requests):

        from contextlib import asynccontextmanager
        from orvion import OrvionClient
        from orvion.fastapi import sync_routes, OrvionMiddleware

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            client = OrvionClient(api_key=API_KEY)
            await sync_routes(app, client)
            yield
            await client.close()

        app = FastAPI(lifespan=lifespan)
        app.add_middleware(
            OrvionMiddleware,
            api_key=API_KEY,
            register_on_first_request=False,  # Already synced in lifespan
        )

    Note: If you call sync_routes() in lifespan, set register_on_first_request=False
    on OrvionMiddleware to avoid redundant registration (though it's safe/idempotent).

    Args:
        app: The FastAPI application instance
        client: OrvionClient instance to use for registration

    Returns:
        Count of routes successfully registered
    """
    return await _scan_and_register_routes(app, client)


__all__ = [
    # Middleware & Decorators
    "OrvionMiddleware",
    "require_payment",
    "sync_routes",
    # Pre-built Routers
    "create_payment_router",
    "create_health_router",
    "create_full_router",
]
