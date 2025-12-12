"""
Custom exceptions for Notify Africa SDK
"""

class NotifyAfricaException(Exception):
    """Base exception for Notify Africa SDK"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(NotifyAfricaException):
    """Raised when authentication fails"""
    pass


class ValidationError(NotifyAfricaException):
    """Raised when request validation fails"""
    pass


class InsufficientCreditsError(NotifyAfricaException):
    """Raised when user has insufficient SMS credits"""
    pass


class NetworkError(NotifyAfricaException):
    """Raised when network request fails"""
    pass


class SenderIDNotFoundError(NotifyAfricaException):
    """Raised when sender ID is not found or inactive"""
    pass