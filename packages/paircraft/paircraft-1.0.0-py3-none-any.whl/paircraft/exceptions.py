"""
Custom exceptions for the Paircraft API SDK.
"""


class APIError(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, code: str = None, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response = response or {}
    
    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class AuthenticationError(APIError):
    """Raised when authentication fails (401)."""
    pass


class ForbiddenError(APIError):
    """Raised when access is forbidden (403)."""
    pass


class NotFoundError(APIError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(APIError):
    """Raised when request validation fails (400)."""
    
    def __init__(self, message: str, errors: list = None, **kwargs):
        super().__init__(message, **kwargs)
        self.errors = errors or []


class RateLimitError(APIError):
    """Raised when rate limit is exceeded (429)."""
    
    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised when the server returns an error (5xx)."""
    pass


class NetworkError(APIError):
    """Raised when a network error occurs."""
    pass


def raise_for_error(response: dict, status_code: int):
    """Raise appropriate exception based on response."""
    
    message = response.get("error", "Unknown error")
    code = response.get("code", "UNKNOWN")
    
    kwargs = {
        "message": message,
        "code": code,
        "status_code": status_code,
        "response": response,
    }
    
    if status_code == 401:
        raise AuthenticationError(**kwargs)
    elif status_code == 403:
        raise ForbiddenError(**kwargs)
    elif status_code == 404:
        raise NotFoundError(**kwargs)
    elif status_code == 400:
        raise ValidationError(errors=response.get("errors"), **kwargs)
    elif status_code == 429:
        raise RateLimitError(retry_after=response.get("retry_after"), **kwargs)
    elif status_code >= 500:
        raise ServerError(**kwargs)
    else:
        raise APIError(**kwargs)
