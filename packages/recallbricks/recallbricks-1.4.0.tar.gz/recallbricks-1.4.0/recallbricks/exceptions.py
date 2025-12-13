"""
RecallBricks SDK Exceptions
"""

class RecallBricksError(Exception):
    """Base exception for RecallBricks SDK"""
    pass

class AuthenticationError(RecallBricksError):
    """Raised when API key is invalid or missing"""
    pass

class RateLimitError(RecallBricksError):
    """Raised when rate limit is exceeded"""
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after

class APIError(RecallBricksError):
    """Raised when API returns an error"""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
