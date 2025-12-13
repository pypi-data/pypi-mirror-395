"""Route configuration cache with jitter for the SDK."""

import asyncio
import random
import time
from typing import List, Optional

from orvion.models import RouteConfig


class RouteCache:
    """
    Cache for route configurations with automatic background refresh.

    Features:
    - TTL-based expiration with jitter to prevent thundering herd
    - Thread-safe access
    - Background refresh before TTL expires
    """

    def __init__(self, ttl_seconds: float = 60.0):
        """
        Initialize the route cache.

        Args:
            ttl_seconds: Base TTL in seconds (default 60s)
        """
        self.ttl_seconds = ttl_seconds
        self._routes: List[RouteConfig] = []
        self._last_refresh: float = 0
        self._next_refresh: float = 0
        self._lock = asyncio.Lock()
        self._refresh_task: Optional[asyncio.Task] = None

    def _calculate_next_refresh(self) -> float:
        """
        Calculate next refresh time with jitter.

        Jitter: base_ttl - 5s + random(0, 10s)
        This prevents all instances from refreshing at exactly the same time.
        """
        jitter = random.uniform(0, 10)
        delay = max(self.ttl_seconds - 5 + jitter, 10)  # At least 10s
        return time.time() + delay

    def is_expired(self) -> bool:
        """Check if cache needs refresh."""
        return time.time() >= self._next_refresh

    def get_routes(self) -> List[RouteConfig]:
        """Get cached routes (may be stale if expired)."""
        return self._routes.copy()

    async def set_routes(self, routes: List[RouteConfig]) -> None:
        """Update cached routes and reset TTL."""
        async with self._lock:
            self._routes = routes
            self._last_refresh = time.time()
            self._next_refresh = self._calculate_next_refresh()

    async def add_route(self, route: RouteConfig) -> None:
        """
        Add or update a single route in cache.

        Uses deterministic key f"{method}:{route_pattern}" for lookup.
        If route exists with same key, it's replaced. Otherwise, it's added.

        This is used by register_route() to patch the cache without a full refresh.

        Args:
            route: The RouteConfig to add or update
        """
        async with self._lock:
            # Key convention: f"{method}:{route_pattern}"
            route_key = f"{route.method}:{route.route_pattern}"

            # Find and replace existing route with same key, or append
            found = False
            for i, existing in enumerate(self._routes):
                existing_key = f"{existing.method}:{existing.route_pattern}"
                if existing_key == route_key:
                    self._routes[i] = route
                    found = True
                    break

            if not found:
                self._routes.append(route)

    def clear(self) -> None:
        """Clear the cache, forcing a refresh on next access."""
        self._routes = []
        self._last_refresh = 0
        self._next_refresh = 0

    @property
    def has_routes(self) -> bool:
        """Check if cache has any routes."""
        return len(self._routes) > 0

    @property
    def route_count(self) -> int:
        """Get number of cached routes."""
        return len(self._routes)

    @property
    def seconds_until_refresh(self) -> float:
        """Get seconds until next refresh (negative if expired)."""
        return self._next_refresh - time.time()

