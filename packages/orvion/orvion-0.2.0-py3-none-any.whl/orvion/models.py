"""Orvion SDK data models"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RouteConfig:
    """Configuration for a protected route"""

    id: str
    route_pattern: str
    method: str
    amount: str
    currency: str
    allow_anonymous: bool
    description: Optional[str] = None
    status: str = "active"  # "active" = requires payment, "paused" = free access


@dataclass
class Charge:
    """A payment charge"""

    id: str
    amount: str
    currency: str
    status: str
    customer_ref: Optional[str] = None
    resource_ref: Optional[str] = None
    x402_requirements: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Hosted checkout fields
    return_url: Optional[str] = None
    checkout_url: Optional[str] = None
    # Payment details (populated after confirmation)
    tx_hash: Optional[str] = None
    confirmed_at: Optional[str] = None


@dataclass
class VerifyResult:
    """Result of payment verification"""

    verified: bool
    transaction_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    customer_ref: Optional[str] = None
    resource_ref: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class PaymentInfo:
    """Payment information attached to request.state"""

    transaction_id: str
    amount: str
    currency: str
    customer_ref: Optional[str] = None
    resource_ref: Optional[str] = None
    route_id: Optional[str] = None
    verified_at: Optional[str] = None

    @classmethod
    def from_verify_result(cls, result: VerifyResult, route_id: Optional[str] = None) -> "PaymentInfo":
        """Create PaymentInfo from a VerifyResult"""
        return cls(
            transaction_id=result.transaction_id or "",
            amount=result.amount or "0",
            currency=result.currency or "USD",
            customer_ref=result.customer_ref,
            resource_ref=result.resource_ref,
            route_id=route_id,
        )


# =============================================================================
# New Models for SDK Enhancement
# =============================================================================


@dataclass
class ConfirmResult:
    """Result of payment confirmation (wallet payment)"""

    success: bool
    transaction_id: str
    status: str  # "succeeded", "pending", "failed"
    tx_hash: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    confirmed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ChargeState:
    """
    UI state for a charge - used by payment widgets to display current status.
    
    This is the response from /v1/demo/charges/{id}/ui-state endpoint.
    """

    transaction_id: str
    status: str  # "pending", "awaiting_payment", "confirming", "succeeded", "failed", "cancelled"
    amount: str
    currency: str
    # Payment details
    recipient_address: Optional[str] = None
    token_address: Optional[str] = None
    network: Optional[str] = None
    # UI hints
    display_amount: Optional[str] = None
    qr_code_data: Optional[str] = None
    # Timestamps
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    # Error info
    error_message: Optional[str] = None


@dataclass
class HealthInfo:
    """
    Health check response - API key validation and organization info.
    
    This is the response from /v1/health endpoint.
    """

    status: str  # "healthy", "degraded", "unhealthy"
    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    environment: Optional[str] = None  # "development", "production"
    api_key_valid: bool = False
    # Optional details
    version: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class WalletPaymentInfo:
    """
    Information needed for wallet-based payment.
    
    Extracted from x402_requirements for easier use.
    """

    recipient_address: str
    amount: str
    token_address: str
    network: str  # "solana-devnet", "solana-mainnet", etc.
    decimals: int = 6
    # Memo/reference for the transaction
    memo: Optional[str] = None
    
    @classmethod
    def from_x402_requirements(cls, requirements: Dict[str, Any]) -> Optional["WalletPaymentInfo"]:
        """
        Extract wallet payment info from x402_requirements.
        
        Returns None if requirements don't contain wallet payment info.
        """
        if not requirements:
            return None
        
        # Handle different formats
        solana = requirements.get("solana", {})
        if not solana:
            return None
        
        return cls(
            recipient_address=solana.get("recipient", ""),
            amount=solana.get("amount", ""),
            token_address=solana.get("token", ""),
            network=solana.get("network", "solana-devnet"),
            decimals=solana.get("decimals", 6),
            memo=solana.get("memo"),
        )


@dataclass
class PaymentMethodInfo:
    """
    Available payment methods for a charge.
    
    Parsed from x402_requirements to show users their options.
    """

    methods: List[str]  # ["solana", "stripe", etc.]
    solana: Optional[WalletPaymentInfo] = None
    # Future: stripe, ethereum, etc.
    
    @classmethod
    def from_x402_requirements(cls, requirements: Dict[str, Any]) -> "PaymentMethodInfo":
        """Parse payment methods from x402_requirements."""
        methods = []
        solana_info = None
        
        if requirements.get("solana"):
            methods.append("solana")
            solana_info = WalletPaymentInfo.from_x402_requirements(requirements)
        
        # Future: parse other payment methods
        
        return cls(methods=methods, solana=solana_info)

