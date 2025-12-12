"""
Utility functions for C1G projects.
"""

import asyncio
import json
from typing import Any

import httpx
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id.

    Args:
        password: Plain text password to hash.

    Returns:
        Argon2 hash string.

    Example:
        >>> from c1gpy.utils import hash_password
        >>> hashed = hash_password("my_secure_password")
    """
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its Argon2 hash.

    Args:
        password: Plain text password to verify.
        hashed: Argon2 hash to compare against.

    Returns:
        True if password matches, False otherwise.

    Example:
        >>> from c1gpy.utils import hash_password, verify_password
        >>> hashed = hash_password("my_secure_password")
        >>> verify_password("my_secure_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    try:
        _hasher.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False


class HTTPClientError(Exception):
    """Raised when HTTP request fails after all retries."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class JSONDecodeError(Exception):
    """Raised when response cannot be decoded as JSON dict."""

    pass


class AsyncHTTPClient:
    """
    HTTP client with retry, rate limiting, and exponential backoff support.

    Args:
        base_url: Optional base URL for all requests.
        retries: Number of retry attempts (default: 0, no retries).
        backoff_factor: Multiplier for exponential backoff (default: 1.0).
        rate_limit_delay: Minimum delay between requests in seconds (default: 0).
        timeout: Request timeout in seconds (default: 30).
        http2: Use HTTP/2 protocol (default: True).

    Example:
        >>> from c1gpy.utils import AsyncHTTPClient
        >>> client = AsyncHTTPClient(retries=3, backoff_factor=2.0)
        >>> data = await client.get("https://api.example.com/data")
        >>> client.close()
    """

    def __init__(
        self,
        base_url: str | None = None,
        retries: int = 0,
        backoff_factor: float = 1.0,
        rate_limit_delay: float = 0,
        timeout: float = 30,
        http2: bool = True,
    ) -> None:
        self._base_url = base_url
        self._retries = retries
        self._backoff_factor = backoff_factor
        self._rate_limit_delay = rate_limit_delay
        self._timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=timeout, http2=http2
        )
        self._last_request_time: float = 0

    async def _wait_for_rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        if self._rate_limit_delay > 0:
            now = asyncio.get_event_loop().time()
            elapsed = now - self._last_request_time
            if elapsed < self._rate_limit_delay:
                await asyncio.sleep(self._rate_limit_delay - elapsed)
            self._last_request_time = asyncio.get_event_loop().time()

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute HTTP request with retry and exponential backoff.

        Returns:
            Parsed JSON response as dict.

        Raises:
            HTTPClientError: If request fails after all retries.
            JSONDecodeError: If response is not valid JSON dict.
        """
        last_error: Exception | None = None
        last_status_code: int | None = None

        for attempt in range(self._retries + 1):
            await self._wait_for_rate_limit()

            try:
                response = await self._client.request(method, url, **kwargs)

                if response.is_success:
                    try:
                        data = response.json()
                        if not isinstance(data, dict):
                            raise JSONDecodeError(
                                f"Expected JSON dict, got {type(data).__name__}"
                            )
                        return data
                    except json.JSONDecodeError as e:
                        raise JSONDecodeError(f"Invalid JSON response: {e}") from e

                last_status_code = response.status_code
                last_error = HTTPClientError(
                    f"HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code,
                )

                # Don't retry on 4xx client errors (except 429 rate limit)
                if 400 <= response.status_code < 500 and response.status_code != 429:
                    raise last_error

            except httpx.RequestError as e:
                last_error = HTTPClientError(f"Request failed: {e}")

            # Exponential backoff before retry
            if attempt < self._retries:
                delay = self._backoff_factor * (2**attempt)
                await asyncio.sleep(delay)

        raise last_error or HTTPClientError(
            "Request failed", status_code=last_status_code
        )

    async def get(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """GET request returning JSON dict."""
        return await self._request_with_retry("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """POST request returning JSON dict."""
        return await self._request_with_retry("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """PUT request returning JSON dict."""
        return await self._request_with_retry("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH request returning JSON dict."""
        return await self._request_with_retry("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """DELETE request returning JSON dict."""
        return await self._request_with_retry("DELETE", url, **kwargs)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHTTPClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
