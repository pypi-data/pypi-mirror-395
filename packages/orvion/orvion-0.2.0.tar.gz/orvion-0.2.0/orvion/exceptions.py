"""Orvion SDK exceptions"""


class OrvionError(Exception):
    """Base exception for all Orvion errors"""

    pass


class OrvionConfigError(OrvionError):
    """Configuration error (e.g., missing API key, invalid settings)"""

    pass


class OrvionAuthError(OrvionError):
    """Authentication error (e.g., invalid API key)"""

    pass


class OrvionAPIError(OrvionError):
    """API error response from Orvion"""

    def __init__(self, message: str, status_code: int, response_body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body or {}


class OrvionTimeoutError(OrvionError):
    """Request timeout error"""

    pass


class OrvionRouteNotFoundError(OrvionError):
    """No matching protected route found for the request"""

    pass


class OrvionPaymentRequiredError(OrvionError):
    """Payment is required to access the resource"""

    def __init__(self, charge_id: str, amount: str, currency: str, x402_requirements: dict):
        super().__init__(f"Payment required: {amount} {currency}")
        self.charge_id = charge_id
        self.amount = amount
        self.currency = currency
        self.x402_requirements = x402_requirements


class OrvionPaymentVerificationError(OrvionError):
    """Payment verification failed"""

    def __init__(self, reason: str):
        super().__init__(f"Payment verification failed: {reason}")
        self.reason = reason

