"""Main Mogu SDK client"""

from typing import Any, Dict, Optional

from mogu_sdk.auth import BaseClient
from mogu_sdk.resources.cost import CostClient
from mogu_sdk.resources.wiki import WikiClient
from mogu_sdk.settings import MoguSettings


class MoguClient:
    """
    Main client for Mogu Workflow Management Platform.

    This client provides access to all Mogu API resources through
    resource-specific clients.

    Example:
        >>> import asyncio
        >>> from mogu_sdk import MoguClient
        >>>
        >>> async def main():
        >>>     client = MoguClient(
        >>>         base_url="https://api.mogu.example.com",
        >>>         token="your-oauth-token"
        >>>     )
        >>>
        >>>     # Access wiki client
        >>>     result = await client.wiki.create_or_update_page(
        >>>         workspace_id="ws-123",
        >>>         path="docs/guide.md",
        >>>         content="# Guide",
        >>>         commit_message="Update guide"
        >>>     )
        >>>     print(f"Committed: {result.commit_id}")
        >>>
        >>>     await client.close()
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        verify_ssl: Optional[bool] = None,
        headers: Optional[Dict[str, str]] = None,
        workspace_id: Optional[str] = None,
    ) -> None:
        """
        Initialize Mogu client.

        All parameters are optional and will fall back to environment variables
        or default values if not provided. Environment variables use the MOGU_ prefix:
        - MOGU_BASE_URL
        - MOGU_TOKEN
        - MOGU_WORKSPACE_ID
        - MOGU_TIMEOUT
        - MOGU_MAX_RETRIES
        - MOGU_VERIFY_SSL

        Args:
            base_url: Base URL of the Mogu API (default: from MOGU_BASE_URL env var or "http://localhost:8000")
            token: OAuth bearer token (default: from MOGU_TOKEN env var)
            timeout: Request timeout in seconds (default: from MOGU_TIMEOUT env var or 30.0)
            max_retries: Number of retry attempts for failed requests (default: from MOGU_MAX_RETRIES env var or 3)
            verify_ssl: Whether to verify SSL certificates (default: from MOGU_VERIFY_SSL env var or True)
            headers: Additional headers to include in all requests
            workspace_id: Default workspace ID for operations (default: from MOGU_WORKSPACE_ID env var)

        Raises:
            ValueError: If token is not provided and MOGU_TOKEN env var is not set

        Example:
            >>> # Using environment variables
            >>> client = MoguClient()  # Reads from MOGU_BASE_URL, MOGU_TOKEN, etc.
            >>>
            >>> # Override specific values
            >>> client = MoguClient(base_url="https://api.mogu.io", token="my-token")
            >>>
            >>> # Using .env file
            >>> # Create a .env file with:
            >>> # MOGU_BASE_URL=http://localhost:8000
            >>> # MOGU_TOKEN=your-token
            >>> # MOGU_WORKSPACE_ID=your-workspace-id
            >>> client = MoguClient()
        """
        # Load settings from environment variables
        settings = MoguSettings()
        
        # Use provided values or fall back to settings
        self._base_url = base_url or settings.base_url
        self._token = token or settings.oauth_token
        self._timeout = timeout if timeout is not None else settings.timeout
        self._max_retries = max_retries if max_retries is not None else settings.max_retries
        self._verify_ssl = verify_ssl if verify_ssl is not None else settings.verify_ssl
        self._workspace_id = workspace_id or settings.workspace_id
        
        self._http_client = BaseClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout,
            max_retries=self._max_retries,
            verify_ssl=self._verify_ssl,
            headers=headers,
        )

        # Initialize resource clients
        self._cost = CostClient(self._http_client)
        self._wiki = WikiClient(self._http_client)

    @property
    def cost(self) -> CostClient:
        """
        Access cost monitoring operations.

        Returns:
            CostClient instance for cost monitoring operations
        """
        return self._cost

    @property
    def wiki(self) -> WikiClient:
        """
        Access wiki operations.

        Returns:
            WikiClient instance for wiki operations
        """
        return self._wiki

    @property
    def workspace_id(self) -> Optional[str]:
        """
        Get the default workspace ID.

        Returns:
            Default workspace ID if configured, None otherwise
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, value: Optional[str]) -> None:
        """
        Set the default workspace ID.

        Args:
            value: Workspace ID to use as default
        """
        self._workspace_id = value

    async def __aenter__(self) -> "MoguClient":
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        await self.close()

    async def close(self) -> None:
        """
        Close the HTTP client and clean up resources.

        This should be called when you're done using the client,
        or use the client as an async context manager.
        """
        await self._http_client.close()
