"""Orvion API client"""

import asyncio
from typing import Any, Dict, List, Optional

import httpx

from orvion.cache import RouteCache
from orvion.exceptions import (
    OrvionAPIError,
    OrvionAuthError,
    OrvionConfigError,
    OrvionTimeoutError,
)
from orvion.matcher import match_route
from orvion.models import (
    Charge,
    ChargeState,
    ConfirmResult,
    HealthInfo,
    RouteConfig,
    VerifyResult,
)
from orvion.telemetry import TelemetryConfig, TelemetryManager


class OrvionClient:
    """
    Orvion API client for x402 payment operations.

    Features:
    - Create and verify charges
    - Fetch and cache route configurations
    - Local route matching for performance
    """

    DEFAULT_BASE_URL = "https://api.orvion.sh"
    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        cache_ttl_seconds: float = 60.0,
        telemetry: Optional[TelemetryConfig] = None,
    ):
        """
        Initialize the Orvion client.

        Args:
            api_key: Your Orvion API key
            base_url: API base URL (default: https://api.orvion.sh)
            timeout: Request timeout in seconds (default: 30)
            cache_ttl_seconds: Route cache TTL in seconds (default: 60)
            telemetry: Optional telemetry configuration
        """
        if not api_key:
            raise OrvionConfigError("API key is required")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._cache = RouteCache(ttl_seconds=cache_ttl_seconds)
        self._http_client: Optional[httpx.AsyncClient] = None
        self._refresh_lock = asyncio.Lock()
        # Initialize telemetry with API key and base URL for backend forwarding
        self._telemetry: Optional[TelemetryManager] = (
            TelemetryManager(
                config=telemetry,
                api_key=self.api_key,  # For attribution
                base_url=self.base_url,  # Telemetry goes to same backend
            )
            if telemetry
            else None
        )

        if self._telemetry:
            self._telemetry.record_init(
                base_url=self.base_url,
                cache_ttl=cache_ttl_seconds,
            )

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._http_client

    async def close(self) -> None:
        """Close the HTTP client and shutdown telemetry."""
        # Shutdown telemetry first (flushes remaining events)
        if self._telemetry:
            await self._telemetry.shutdown()

        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

    async def __aenter__(self) -> "OrvionClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Make an API request."""
        client = await self._get_client()

        try:
            # Use custom timeout if provided, otherwise use client default
            request_timeout = timeout if timeout is not None else self.timeout
            response = await client.request(method, path, json=json, params=params, timeout=request_timeout)
        except httpx.TimeoutException as e:
            raise OrvionTimeoutError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise OrvionAPIError(f"Request failed: {e}", status_code=0)

        if response.status_code == 401:
            raise OrvionAuthError("Invalid API key")

        if response.status_code >= 400:
            try:
                body = response.json()
            except Exception:
                body = {"detail": response.text}

            raise OrvionAPIError(
                message=body.get("detail", f"API error: {response.status_code}"),
                status_code=response.status_code,
                response_body=body,
            )

        if response.status_code == 204:
            return {}

        return response.json()

    # =========================================================================
    # Charge Operations
    # =========================================================================

    async def create_charge(
        self,
        amount: str,
        currency: str,
        customer_ref: Optional[str] = None,
        resource_ref: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        return_url: Optional[str] = None,
    ) -> Charge:
        """
        Create a new payment charge.

        Args:
            amount: Price amount as string (e.g., "0.10")
            currency: Currency code (e.g., "USD")
            customer_ref: Customer identifier
            resource_ref: Resource identifier (e.g., "protected_route:uuid")
            description: Charge description
            metadata: Additional metadata
            idempotency_key: Idempotency key for retries
            return_url: URL to redirect buyer after successful payment on hosted checkout.
                        If provided, response will include checkout_url.

        Returns:
            The created Charge (includes checkout_url if return_url was provided)
        """
        async def _create() -> Charge:
            payload: Dict[str, Any] = {
                "amount": amount,
                "currency": currency,
            }

            if customer_ref:
                payload["customer_ref"] = customer_ref
            if resource_ref:
                payload["resource_ref"] = resource_ref
            if description:
                payload["description"] = description
            if metadata:
                payload["metadata"] = metadata
            if return_url:
                payload["return_url"] = return_url

            headers = {}
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key

            data = await self._request("POST", "/v1/charges", json=payload)

            return Charge(
                id=data["id"],
                amount=data["amount"],
                currency=data["currency"],
                status=data.get("status", "pending"),
                customer_ref=data.get("customer_ref"),
                resource_ref=data.get("resource_ref"),
                x402_requirements=data.get("x402_requirements", {}),
                description=data.get("description"),
                created_at=data.get("created_at"),
                return_url=data.get("return_url"),
                checkout_url=data.get("checkout_url"),
            )

        if self._telemetry:
            async with self._telemetry.record_operation(
                "create_charge",
                {
                    "currency": currency,
                    "has_customer_ref": 1 if customer_ref else 0,
                    "has_resource_ref": 1 if resource_ref else 0,
                    "has_return_url": 1 if return_url else 0,
                },
            ):
                return await _create()

        return await _create()

    async def verify_charge(
        self,
        transaction_id: str,
        customer_ref: Optional[str] = None,
        resource_ref: Optional[str] = None,
    ) -> VerifyResult:
        """
        Verify a payment transaction.

        Args:
            transaction_id: The transaction ID from the payment header
            customer_ref: Expected customer reference (optional validation)
            resource_ref: Expected resource reference (REQUIRED for security)

        Returns:
            VerifyResult with verification status
        """
        async def _verify() -> VerifyResult:
            payload: Dict[str, Any] = {
                "transaction_id": transaction_id,
            }

            if customer_ref:
                payload["customer_ref"] = customer_ref
            if resource_ref:
                payload["resource_ref"] = resource_ref

            try:
                data = await self._request("POST", "/v1/charges/verify", json=payload)

                return VerifyResult(
                    verified=data.get("verified", False),
                    transaction_id=data.get("transaction_id"),
                    amount=data.get("amount"),
                    currency=data.get("currency"),
                    customer_ref=data.get("customer_ref"),
                    resource_ref=data.get("resource_ref"),
                )
            except OrvionAPIError as e:
                if e.status_code == 404:
                    return VerifyResult(verified=False, reason="Transaction not found")
                elif e.status_code == 409:
                    return VerifyResult(verified=False, reason="Transaction not completed")
                raise

        if self._telemetry:
            async with self._telemetry.record_operation(
                "verify_charge",
                {
                    "has_customer_ref": 1 if customer_ref else 0,
                    "has_resource_ref": 1 if resource_ref else 0,
                },
            ):
                return await _verify()

        return await _verify()

    async def get_charge(self, charge_id: str) -> Charge:
        """
        Get a charge by its ID.

        Args:
            charge_id: The charge/transaction ID

        Returns:
            The Charge object with current status
        """
        data = await self._request("GET", f"/v1/charges/{charge_id}")

        return Charge(
            id=data["id"],
            amount=data["amount"],
            currency=data["currency"],
            status=data.get("status", "pending"),
            customer_ref=data.get("customer_ref"),
            resource_ref=data.get("resource_ref"),
            x402_requirements=data.get("x402_requirements", {}),
            description=data.get("description"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            return_url=data.get("return_url"),
            checkout_url=data.get("checkout_url"),
            tx_hash=data.get("tx_hash"),
            confirmed_at=data.get("confirmed_at"),
        )

    async def confirm_payment(
        self,
        transaction_id: str,
        tx_hash: str,
        timeout: Optional[float] = 60.0,
    ) -> ConfirmResult:
        """
        Confirm a wallet payment with blockchain transaction hash.

        This is called after the user signs and submits a transaction
        from their wallet (e.g., Phantom on Solana).

        Args:
            transaction_id: The charge/transaction ID from create_charge
            tx_hash: The blockchain transaction hash/signature
            timeout: Request timeout in seconds (default: 60s, longer than default
                     due to on-chain verification which may require RPC retries)

        Returns:
            ConfirmResult with confirmation status
        """
        payload = {
            "transaction_id": transaction_id,
            "tx_hash": tx_hash,
        }

        try:
            data = await self._request("POST", "/v1/facilitator/confirm", json=payload, timeout=timeout)

            return ConfirmResult(
                success=data.get("status") == "succeeded",
                transaction_id=data.get("transaction_id", transaction_id),
                status=data.get("status", "pending"),
                tx_hash=data.get("tx_hash", tx_hash),
                amount=data.get("amount"),
                currency=data.get("currency"),
                confirmed_at=data.get("confirmed_at"),
            )
        except OrvionAPIError as e:
            return ConfirmResult(
                success=False,
                transaction_id=transaction_id,
                status="failed",
                error=str(e),
            )

    async def cancel_charge(self, transaction_id: str) -> bool:
        """
        Cancel a pending charge.

        Use this when:
        - User closes the payment modal without paying
        - User explicitly cancels the payment
        - Payment timeout occurs

        Args:
            transaction_id: The charge/transaction ID to cancel

        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            await self._request(
                "POST",
                f"/v1/billing/transactions/{transaction_id}/cancel",
            )
            return True
        except OrvionAPIError:
            return False

    async def get_charge_state(self, transaction_id: str) -> ChargeState:
        """
        Get the UI state for a charge.

        This endpoint is optimized for payment widgets and returns
        all the information needed to display the payment status.

        Args:
            transaction_id: The charge/transaction ID

        Returns:
            ChargeState with UI-ready status information
        """
        data = await self._request(
            "GET",
            f"/v1/demo/charges/{transaction_id}/ui-state",
        )

        return ChargeState(
            transaction_id=data.get("transaction_id", transaction_id),
            status=data.get("status", "pending"),
            amount=data.get("amount", "0"),
            currency=data.get("currency", "USD"),
            recipient_address=data.get("recipient_address"),
            token_address=data.get("token_address"),
            network=data.get("network"),
            display_amount=data.get("display_amount"),
            qr_code_data=data.get("qr_code_data"),
            created_at=data.get("created_at"),
            expires_at=data.get("expires_at"),
            error_message=data.get("error_message"),
        )

    # =========================================================================
    # Health & Organization
    # =========================================================================

    async def health_check(self) -> HealthInfo:
        """
        Check API health and validate API key.

        This endpoint validates your API key and returns organization info.
        Use this on startup to verify configuration.

        Returns:
            HealthInfo with status and organization details
        """
        try:
            data = await self._request("GET", "/v1/health")

            return HealthInfo(
                status=data.get("status", "healthy"),
                organization_id=data.get("organization_id"),
                organization_name=data.get("organization_name"),
                environment=data.get("environment"),
                api_key_valid=True,
                version=data.get("version"),
                timestamp=data.get("timestamp"),
            )
        except OrvionAuthError:
            return HealthInfo(
                status="unhealthy",
                api_key_valid=False,
            )
        except OrvionAPIError as e:
            return HealthInfo(
                status="unhealthy",
                api_key_valid=False,
            )

    # =========================================================================
    # Route Configuration
    # =========================================================================

    async def get_routes(self, force_refresh: bool = False) -> List[RouteConfig]:
        """
        Get protected route configurations.

        Uses local cache with automatic refresh. Call force_refresh=True
        to bypass cache.

        Args:
            force_refresh: Force fetch from API, ignoring cache

        Returns:
            List of RouteConfig objects
        """
        if not force_refresh and self._cache.has_routes and not self._cache.is_expired():
            return self._cache.get_routes()

        async with self._refresh_lock:
            # Double-check after acquiring lock
            if not force_refresh and self._cache.has_routes and not self._cache.is_expired():
                return self._cache.get_routes()

            data = await self._request("GET", "/v1/protected-routes/routes")

            routes = [
                RouteConfig(
                    id=r["id"],
                    route_pattern=r["route_pattern"],
                    method=r["method"],
                    amount=r["amount"],
                    currency=r["currency"],
                    allow_anonymous=r.get("allow_anonymous", True),
                    description=r.get("description"),
                    status=r.get("status", "active"),  # Default to active for legacy routes
                )
                for r in data
            ]

            await self._cache.set_routes(routes)
            return routes

    async def register_route(
        self,
        path: str,
        method: str,
        amount: str,
        currency: str = "USD",
        allow_anonymous: bool = True,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> RouteConfig:
        """
        Register a protected route. If route exists, returns existing config.

        This method is used by the @require_payment() decorator to auto-register
        routes on first access. Decorator arguments (amount, currency, etc.) are
        only used if the route is created for the first time. Afterwards, dashboard
        edits override them (dashboard is source of truth).

        Args:
            path: Route pattern (e.g., /api/premium or /api/articles/{slug})
            method: HTTP method (GET, POST, etc.) - will be uppercased
            amount: Price amount as string (e.g., "0.10")
            currency: Currency code (default: USD)
            allow_anonymous: Allow requests without customer ID (default: True)
            name: User-friendly name for the route
            description: Description shown in 402 response

        Returns:
            RouteConfig with the route configuration (new or existing)
        """
        method = method.upper()  # Normalize method

        payload: Dict[str, Any] = {
            "route_pattern": path,
            "method": method,
            "amount": amount,
            "currency": currency,
            "allow_anonymous": allow_anonymous,
        }

        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        data = await self._request("POST", "/v1/protected-routes/routes/register", json=payload)

        route = RouteConfig(
            id=data["id"],
            route_pattern=data["route_pattern"],
            method=data["method"],
            amount=data["amount"],
            currency=data["currency"],
            allow_anonymous=data.get("allow_anonymous", True),
            description=data.get("description"),
        )

        # Update cache with new/existing route
        await self._cache.add_route(route)

        return route

    async def match_route(self, path: str, method: str) -> Optional[RouteConfig]:
        """
        Match a request to a protected route using local cache.

        Args:
            path: Request path (e.g., /api/premium/data)
            method: HTTP method (e.g., GET)

        Returns:
            Matching RouteConfig or None
        """
        routes = await self.get_routes()
        return match_route(path, method.upper(), routes)

    def clear_cache(self) -> None:
        """Clear the route cache, forcing refresh on next access."""
        self._cache.clear()

