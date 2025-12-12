"""VCL SDK Exceptions"""


class VCLError(Exception):
    """Base exception for VCL SDK errors"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(VCLError):
    """Raised when authentication fails"""

    pass


class ReceiptNotFoundError(VCLError):
    """Raised when a receipt is not found"""

    pass


class RateLimitError(VCLError):
    """Raised when rate limit is exceeded"""

    pass


class ServerError(VCLError):
    """Raised when the server returns an error"""

    pass


class ValidationError(VCLError):
    """Raised when request validation fails"""

    pass
