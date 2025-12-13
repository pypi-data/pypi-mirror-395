"""Mock utilities for testing Orvion integrations"""

import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

from orvion.models import Charge, PaymentInfo, RouteConfig, VerifyResult


def fake_payment(
    amount: str = "0.10",
    currency: str = "USD",
    transaction_id: Optional[str] = None,
    customer_ref: Optional[str] = None,
    resource_ref: Optional[str] = None,
    route_id: Optional[str] = None,
) -> PaymentInfo:
    """
    Create a fake PaymentInfo object for testing.

    Usage:
        request.state.payment = fake_payment(amount="5.00", currency="USD")
    """
    return PaymentInfo(
        transaction_id=transaction_id or f"test_tx_{uuid.uuid4().hex[:8]}",
        amount=amount,
        currency=currency,
        customer_ref=customer_ref or "test_customer",
        resource_ref=resource_ref or f"protected_route:{uuid.uuid4()}",
        route_id=route_id or str(uuid.uuid4()),
        verified_at=datetime.utcnow().isoformat(),
    )


class MockOrvion:
    """
    Mock Orvion client for testing.

    Usage:
        mock = MockOrvion(always_approve=True)
        with mock:
            # Your test code here
            response = client.get("/api/premium/data")
    """

    def __init__(
        self,
        always_approve: bool = True,
        routes: Optional[List[RouteConfig]] = None,
        default_amount: str = "0.10",
        default_currency: str = "USD",
    ):
        """
        Initialize mock.

        Args:
            always_approve: If True, all payments are auto-approved
            routes: List of mock route configurations
            default_amount: Default amount for charges
            default_currency: Default currency for charges
        """
        self.always_approve = always_approve
        self.routes = routes or []
        self.default_amount = default_amount
        self.default_currency = default_currency
        self.charges: Dict[str, Charge] = {}
        self._patches: List[Any] = []

    def add_route(
        self,
        pattern: str,
        method: str = "*",
        amount: Optional[str] = None,
        currency: Optional[str] = None,
        allow_anonymous: bool = True,
    ) -> RouteConfig:
        """Add a mock route configuration."""
        route = RouteConfig(
            id=str(uuid.uuid4()),
            route_pattern=pattern,
            method=method,
            amount=amount or self.default_amount,
            currency=currency or self.default_currency,
            allow_anonymous=allow_anonymous,
        )
        self.routes.append(route)
        return route

    async def mock_create_charge(
        self,
        amount: str,
        currency: str,
        customer_ref: Optional[str] = None,
        resource_ref: Optional[str] = None,
        **kwargs,
    ) -> Charge:
        """Mock create_charge implementation."""
        charge = Charge(
            id=f"test_charge_{uuid.uuid4().hex[:8]}",
            amount=amount,
            currency=currency,
            status="pending" if not self.always_approve else "completed",
            customer_ref=customer_ref,
            resource_ref=resource_ref,
            x402_requirements={
                "test": True,
                "amount": amount,
                "currency": currency,
            },
        )
        self.charges[charge.id] = charge
        return charge

    async def mock_verify_charge(
        self,
        transaction_id: str,
        customer_ref: Optional[str] = None,
        resource_ref: Optional[str] = None,
    ) -> VerifyResult:
        """Mock verify_charge implementation."""
        if self.always_approve:
            return VerifyResult(
                verified=True,
                transaction_id=transaction_id,
                amount=self.default_amount,
                currency=self.default_currency,
                customer_ref=customer_ref,
                resource_ref=resource_ref,
            )
        else:
            return VerifyResult(
                verified=False,
                transaction_id=transaction_id,
                reason="Payment not completed",
            )

    async def mock_get_routes(self, force_refresh: bool = False) -> List[RouteConfig]:
        """Mock get_routes implementation."""
        return self.routes

    async def mock_match_route(self, path: str, method: str) -> Optional[RouteConfig]:
        """Mock match_route implementation."""
        from orvion.matcher import match_route

        return match_route(path, method, self.routes)

    def __enter__(self) -> "MockOrvion":
        """Start mocking."""
        self._patches = [
            patch("orvion.client.OrvionClient.create_charge", self.mock_create_charge),
            patch("orvion.client.OrvionClient.verify_charge", self.mock_verify_charge),
            patch("orvion.client.OrvionClient.get_routes", self.mock_get_routes),
            patch("orvion.client.OrvionClient.match_route", self.mock_match_route),
        ]
        for p in self._patches:
            p.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop mocking."""
        for p in self._patches:
            p.stop()
        self._patches = []


@contextmanager
def mock_orvion(
    always_approve: bool = True,
    routes: Optional[List[RouteConfig]] = None,
):
    """
    Context manager for mocking Orvion calls.

    Usage:
        with mock_orvion(always_approve=True) as mock:
            mock.add_route("/api/premium/*", amount="0.10")
            response = test_client.get("/api/premium/data")
    """
    mock = MockOrvion(always_approve=always_approve, routes=routes)
    with mock:
        yield mock

