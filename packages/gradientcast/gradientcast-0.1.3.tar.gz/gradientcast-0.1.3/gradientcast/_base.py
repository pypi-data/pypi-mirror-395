"""Base client with HTTP handling, retry logic, and authentication."""

import json
import random
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._exceptions import (
    APIError,
    AuthenticationError,
    GradientCastError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)


class BaseClient(ABC):
    """Abstract base client with shared HTTP and retry functionality.

    This class handles:
    - HTTP session management with connection pooling
    - Bearer token authentication
    - Exponential backoff with jitter for retries
    - Azure ML double-encoded JSON response handling
    - Context manager support

    Subclasses must implement:
    - endpoint_name: Property returning the endpoint identifier
    - _get_endpoint_urls: Method returning (production_url, development_url)
    """

    # Retry configuration
    DEFAULT_TIMEOUT = 180
    DEFAULT_MAX_RETRIES = 3
    INITIAL_RETRY_DELAY_MS = 1000
    MAX_RETRY_DELAY_MS = 30000
    RETRY_EXPONENTIAL_BASE = 2.0
    RETRY_JITTER_FACTOR = 0.2
    RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)

    def __init__(
        self,
        api_key: str,
        environment: str = "production",
        endpoint_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES
    ) -> None:
        """Initialize the client.

        Args:
            api_key: Your GradientCast API key for this endpoint.
            environment: Either "production" (default) or "development".
            endpoint_url: Optional custom endpoint URL override.
            timeout: Request timeout in seconds (default 180).
            max_retries: Maximum retry attempts for transient failures (default 3).

        Raises:
            ValueError: If api_key is empty or environment is invalid.
        """
        if not api_key:
            raise ValueError("api_key is required")

        if environment not in ("production", "development"):
            raise ValueError(
                f"Invalid environment '{environment}'. "
                "Must be 'production' or 'development'."
            )

        self.api_key = api_key
        self.environment = environment
        self.timeout = timeout
        self.max_retries = max_retries

        # Set endpoint URL
        if endpoint_url:
            self.endpoint_url = endpoint_url
        else:
            prod_url, dev_url = self._get_endpoint_urls()
            self.endpoint_url = prod_url if environment == "production" else dev_url

        self._session: Optional[requests.Session] = None

    @property
    @abstractmethod
    def endpoint_name(self) -> str:
        """Return the endpoint name for logging/debugging."""
        pass

    @abstractmethod
    def _get_endpoint_urls(self) -> Tuple[str, str]:
        """Return (production_url, development_url) for this endpoint."""
        pass

    def _get_session(self) -> requests.Session:
        """Get or create the HTTP session with connection pooling."""
        if self._session is None:
            self._session = requests.Session()

            # Configure connection pooling
            adapter = HTTPAdapter(
                pool_connections=10,
                pool_maxsize=10,
                max_retries=Retry(total=0)  # We handle retries ourselves
            )
            self._session.mount("https://", adapter)
            self._session.mount("http://", adapter)

        return self._session

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "azureml-model-deployment": "blue"
        }

    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse API response, handling Azure ML's double-encoded JSON.

        Azure ML endpoints sometimes return JSON as a double-encoded string.
        This method handles both normal and double-encoded responses.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed response dictionary.

        Raises:
            APIError: If response cannot be parsed as JSON.
        """
        try:
            data = response.json()

            # Handle double-encoded JSON (Azure ML quirk)
            if isinstance(data, str):
                data = json.loads(data)

            return data
        except (json.JSONDecodeError, ValueError) as e:
            raise APIError(
                f"Failed to parse API response: {e}",
                status_code=response.status_code
            )

    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate retry delay with exponential backoff and jitter.

        Args:
            attempt: The current attempt number (0-indexed).

        Returns:
            Delay in seconds before the next retry.
        """
        delay_ms = min(
            self.INITIAL_RETRY_DELAY_MS * (self.RETRY_EXPONENTIAL_BASE ** attempt),
            self.MAX_RETRY_DELAY_MS
        )

        # Add jitter
        jitter = delay_ms * self.RETRY_JITTER_FACTOR
        delay_ms += random.uniform(-jitter, jitter)

        return delay_ms / 1000.0

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if a request should be retried.

        Args:
            exception: The exception that occurred.
            attempt: The current attempt number (0-indexed).

        Returns:
            True if the request should be retried.
        """
        if attempt >= self.max_retries:
            return False

        # Retry on rate limits
        if isinstance(exception, RateLimitError):
            return True

        # Retry on transient API errors
        if isinstance(exception, APIError) and exception.status_code in self.RETRYABLE_STATUS_CODES:
            return True

        # Retry on connection errors
        if isinstance(exception, (requests.ConnectionError, requests.Timeout)):
            return True

        return False

    def _handle_error_response(
        self,
        response: requests.Response,
        parsed_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Convert HTTP error response to appropriate exception.

        Args:
            response: The HTTP response object.
            parsed_data: Parsed response data, if available.

        Raises:
            AuthenticationError: For 401/403 responses.
            RateLimitError: For 429 responses.
            ValidationError: For 400 responses with validation errors.
            APIError: For other error responses.
        """
        status_code = response.status_code

        # Try to get error message from response
        error_message = "Unknown error"
        error_type = None

        if parsed_data:
            error_message = parsed_data.get("error", parsed_data.get("message", error_message))
            error_type = parsed_data.get("error_type", parsed_data.get("error"))

            # Handle nested error structure
            if isinstance(error_message, dict):
                error_message = error_message.get("message", str(error_message))

        # Map status codes to exceptions
        if status_code in (401, 403):
            raise AuthenticationError(
                f"Authentication failed: {error_message}",
                response=parsed_data
            )

        if status_code == 429:
            retry_after = None
            if "Retry-After" in response.headers:
                try:
                    retry_after = int(response.headers["Retry-After"])
                except ValueError:
                    pass

            raise RateLimitError(
                f"Rate limit exceeded: {error_message}",
                response=parsed_data,
                retry_after=retry_after
            )

        if status_code == 400:
            raise ValidationError(
                f"Validation error: {error_message}",
                response=parsed_data
            )

        raise APIError(
            error_message,
            status_code=status_code,
            error_type=error_type,
            response=parsed_data
        )

    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request with retry logic.

        Args:
            payload: Request payload dictionary.

        Returns:
            Parsed response dictionary.

        Raises:
            AuthenticationError: If authentication fails.
            RateLimitError: If rate limit is exceeded after retries.
            ValidationError: If input validation fails.
            TimeoutError: If request times out after retries.
            APIError: For other API errors after retries.
        """
        session = self._get_session()
        headers = self._get_headers()
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = session.post(
                    self.endpoint_url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )

                # Parse response
                try:
                    parsed_data = self._parse_response(response)
                except APIError:
                    parsed_data = None

                # Check for HTTP errors
                if not response.ok:
                    self._handle_error_response(response, parsed_data)

                # Check for error in response body (some APIs return 200 with error)
                if parsed_data and "error" in parsed_data:
                    error_msg = parsed_data.get("error", "Unknown error")
                    if isinstance(error_msg, str) and error_msg:
                        # Check if it's a validation error
                        error_type = parsed_data.get("error", "")
                        if error_type == "ValidationError" or "validation" in error_msg.lower():
                            raise ValidationError(error_msg, response=parsed_data)
                        raise APIError(
                            error_msg,
                            status_code=response.status_code,
                            error_type=error_type,
                            response=parsed_data
                        )

                return parsed_data

            except requests.Timeout as e:
                last_exception = TimeoutError(
                    f"Request timed out after {self.timeout}s"
                )

                if not self._should_retry(e, attempt):
                    raise last_exception

            except requests.ConnectionError as e:
                last_exception = APIError(
                    f"Connection error: {e}",
                    status_code=None
                )

                if not self._should_retry(e, attempt):
                    raise last_exception

            except (RateLimitError, APIError) as e:
                last_exception = e

                if not self._should_retry(e, attempt):
                    raise

                # Use retry-after header for rate limits if available
                if isinstance(e, RateLimitError) and e.retry_after:
                    delay = e.retry_after
                else:
                    delay = self._calculate_retry_delay(attempt)

            except (AuthenticationError, ValidationError):
                # Don't retry auth or validation errors
                raise

            except GradientCastError:
                raise

            except Exception as e:
                raise APIError(f"Unexpected error: {e}")

            # Wait before retry
            delay = self._calculate_retry_delay(attempt)
            time.sleep(delay)

        # Should not reach here, but just in case
        if last_exception:
            raise last_exception

        raise APIError("Request failed after all retries")

    def close(self) -> None:
        """Close the HTTP session and release resources."""
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self) -> "BaseClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - close the session."""
        self.close()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"environment='{self.environment}', "
            f"endpoint='{self.endpoint_url}')"
        )
