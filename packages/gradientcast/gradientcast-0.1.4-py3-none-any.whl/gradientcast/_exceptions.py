"""Exception classes for the GradientCast SDK."""

from typing import Any, Dict, Optional


class GradientCastError(Exception):
    """Base exception for all GradientCast SDK errors.

    Attributes:
        message: Human-readable error description.
        response: Raw API response dict, if available.
    """

    def __init__(
        self,
        message: str,
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response = response

    def __str__(self) -> str:
        return self.message


class AuthenticationError(GradientCastError):
    """Raised when API authentication fails (HTTP 401/403).

    This typically indicates an invalid or expired API key.

    Example:
        >>> try:
        ...     fm.forecast(data, horizon_len=10, freq="H")
        ... except AuthenticationError as e:
        ...     print(f"Invalid API key: {e}")
    """
    pass


class RateLimitError(GradientCastError):
    """Raised when API rate limit is exceeded (HTTP 429).

    Attributes:
        retry_after: Suggested wait time in seconds before retrying.

    Example:
        >>> try:
        ...     fm.forecast(data, horizon_len=10, freq="H")
        ... except RateLimitError as e:
        ...     print(f"Rate limited. Retry after {e.retry_after}s")
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        response: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None
    ) -> None:
        super().__init__(message, response)
        self.retry_after = retry_after


class ValidationError(GradientCastError):
    """Raised when input validation fails.

    This can occur client-side (SDK validation) or server-side (API validation).

    Example:
        >>> try:
        ...     fm.forecast([], horizon_len=10, freq="H")  # Empty data
        ... except ValidationError as e:
        ...     print(f"Invalid input: {e}")
    """
    pass


class TimeoutError(GradientCastError):
    """Raised when a request times out.

    ML inference can take time. Consider increasing the timeout
    parameter if you're processing large datasets.

    Example:
        >>> try:
        ...     fm.forecast(large_data, horizon_len=100, freq="H")
        ... except TimeoutError as e:
        ...     print("Request timed out. Try increasing timeout.")
    """
    pass


class APIError(GradientCastError):
    """Raised for general API errors not covered by other exceptions.

    Attributes:
        status_code: HTTP status code from the API response.
        error_type: Error type string from the API, if available.

    Example:
        >>> try:
        ...     fm.forecast(data, horizon_len=10, freq="H")
        ... except APIError as e:
        ...     print(f"API error {e.status_code}: {e.message}")
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_type: Optional[str] = None,
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, response)
        self.status_code = status_code
        self.error_type = error_type

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
