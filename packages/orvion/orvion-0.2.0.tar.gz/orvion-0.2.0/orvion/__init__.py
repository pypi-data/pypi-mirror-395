"""Orvion SDK for x402 payment-protected APIs"""

from orvion.client import OrvionClient
from orvion.exceptions import (
    OrvionError,
    OrvionAPIError,
    OrvionAuthError,
    OrvionConfigError,
    OrvionTimeoutError,
)
from orvion.models import (
    Charge,
    ChargeState,
    ConfirmResult,
    HealthInfo,
    PaymentInfo,
    PaymentMethodInfo,
    RouteConfig,
    VerifyResult,
    WalletPaymentInfo,
)
from orvion.telemetry import TelemetryConfig, TelemetryManager, get_telemetry, init_telemetry

__version__ = "0.2.0"

__all__ = [
    # Client
    "OrvionClient",
    # Exceptions
    "OrvionError",
    "OrvionAPIError",
    "OrvionAuthError",
    "OrvionConfigError",
    "OrvionTimeoutError",
    # Core Models
    "Charge",
    "PaymentInfo",
    "RouteConfig",
    "VerifyResult",
    # New Models (v0.2.0)
    "ConfirmResult",
    "ChargeState",
    "HealthInfo",
    "WalletPaymentInfo",
    "PaymentMethodInfo",
    # Telemetry
    "TelemetryConfig",
    "TelemetryManager",
    "init_telemetry",
    "get_telemetry",
]

