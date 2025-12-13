"""OSE Cloud SDK Exceptions"""


class OSEError(Exception):
    """Base exception for OSE SDK"""
    pass


class APIError(OSEError):
    """API request error"""

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(OSEError):
    """Authentication error"""
    pass


class NotFoundError(APIError):
    """Resource not found error"""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)
