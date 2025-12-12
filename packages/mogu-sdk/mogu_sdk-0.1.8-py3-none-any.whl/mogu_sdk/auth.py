"""Base HTTP client for Mogu API with authentication and error handling"""

import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx
from dotenv import load_dotenv

from mogu_sdk.exceptions import (
    AuthenticationError,
    MoguAPIError,
    NetworkError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)

# Load environment variables
load_dotenv()


class BaseClient:
    """Base HTTP client with authentication and error handling"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        verify_ssl: bool = True,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize the base client.

        Args:
            base_url: Base URL of the Mogu API (default: from MOGU_BASE_URL env var)
            token: OAuth bearer token (default: from MOGU_TOKEN env var)
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts for failed requests
            verify_ssl: Whether to verify SSL certificates
            headers: Additional headers to include in all requests
        """
        self.base_url = base_url or os.getenv("MOGU_BASE_URL", "http://localhost:8000")
        self.token = token or os.getenv("MOGU_TOKEN")

        if not self.token:
            raise ValueError(
                "Authentication token is required. "
                "Provide it via 'token' parameter or MOGU_TOKEN environment variable."
            )

        # Ensure base_url doesn't end with slash
        self.base_url = self.base_url.rstrip("/")

        # Initialize HTTP client
        default_headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "mogu-sdk/0.1.0",
        }

        if headers:
            default_headers.update(headers)

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=default_headers,
            timeout=timeout,
            verify=verify_ssl,
        )

        self.max_retries = max_retries

    async def __aenter__(self) -> "BaseClient":
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client"""
        await self._client.aclose()

    def _build_url(self, path: str) -> str:
        """Build full URL from path"""
        # Remove leading slash if present
        path = path.lstrip("/")
        return urljoin(f"{self.base_url}/", path)

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses"""
        status_code = response.status_code

        try:
            error_data = response.json()
            message = error_data.get("detail", response.text)
        except Exception:
            message = response.text or f"HTTP {status_code} error"

        if status_code == 401:
            raise AuthenticationError(message, response=error_data)
        elif status_code == 403:
            raise PermissionDeniedError(message, response=error_data)
        elif status_code == 404:
            raise NotFoundError(message, response=error_data)
        elif status_code == 422:
            raise ValidationError(message, response=error_data)
        elif status_code == 429:
            raise RateLimitError(message, response=error_data)
        elif 500 <= status_code < 600:
            raise ServerError(message, status_code=status_code, response=error_data)
        else:
            raise MoguAPIError(message, status_code=status_code, response=error_data)

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make HTTP request with error handling and retries.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            **kwargs: Additional arguments to pass to httpx

        Returns:
            HTTP response

        Raises:
            MoguAPIError: On API errors
            NetworkError: On network errors
            TimeoutError: On timeout
        """
        url = self._build_url(path)
        attempt = 0

        while attempt <= self.max_retries:
            try:
                response = await self._client.request(method, url, **kwargs)

                # Raise for HTTP errors
                if response.status_code >= 400:
                    self._handle_error(response)

                return response

            except (httpx.TimeoutException, httpx.ConnectTimeout, httpx.ReadTimeout):
                attempt += 1
                if attempt > self.max_retries:
                    raise TimeoutError(
                        f"Request to {url} timed out after {self.max_retries} retries"
                    )

            except (httpx.NetworkError, httpx.ConnectError):
                attempt += 1
                if attempt > self.max_retries:
                    raise NetworkError(
                        f"Network error connecting to {url} after {self.max_retries} retries"
                    )

            except (AuthenticationError, PermissionDeniedError, NotFoundError, ValidationError):
                # Don't retry these errors
                raise

        # Should not reach here
        raise MoguAPIError("Unexpected error during request")

    async def get(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make GET request"""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make POST request"""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make PUT request"""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make DELETE request"""
        return await self._request("DELETE", path, **kwargs)
