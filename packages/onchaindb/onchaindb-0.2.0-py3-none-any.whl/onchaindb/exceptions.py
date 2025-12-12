"""
OnChainDB SDK Exceptions

Custom exception classes for the OnChainDB Python SDK.
"""


class OnChainDBException(Exception):
    """Base exception for OnChainDB SDK."""
    pass


class QueryException(OnChainDBException):
    """Exception raised for query-related errors."""
    pass


class StoreException(OnChainDBException):
    """Exception raised for store-related errors."""
    pass


class TaskTimeoutException(OnChainDBException):
    """Exception raised when a task times out."""
    pass


class HttpException(OnChainDBException):
    """Exception raised for HTTP-related errors."""

    def __init__(self, message: str, status_code: int | None = None, response_data: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class PaymentRequiredException(OnChainDBException):
    """Exception raised when payment is required (402 response)."""

    def __init__(
        self,
        message: str,
        amount_utia: int,
        pay_to: str,
        quote_id: str | None = None,
        expires_at: int | None = None,
        resource: str | None = None,
        description: str | None = None,
    ):
        super().__init__(message)
        self.amount_utia = amount_utia
        self.pay_to = pay_to
        self.quote_id = quote_id
        self.expires_at = expires_at
        self.resource = resource
        self.description = description
