"""
Mogu SDK - Official Python SDK for Mogu Workflow Management Platform

Example usage:
    >>> import asyncio
    >>> from mogu_sdk import MoguClient
    >>> 
    >>> async def main():
    >>>     client = MoguClient(
    >>>         base_url="https://api.mogu.example.com",
    >>>         token="your-oauth-token"
    >>>     )
    >>>     
    >>>     # Create or update wiki page
    >>>     result = await client.wiki.create_or_update_page(
    >>>         workspace_id="ws-123",
    >>>         path="docs/guide.md",
    >>>         content="# Guide\\n\\nContent here",
    >>>         commit_message="Update guide"
    >>>     )
    >>>     print(f"Committed: {result.commit_id}")
    >>> 
    >>> asyncio.run(main())
"""

from mogu_sdk.client import MoguClient
from mogu_sdk.exceptions import (
    MoguAPIError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from mogu_sdk.models import (
    WikiFile,
    WikiContent,
    WikiUpdateResponse,
    WikiSearchMatch,
    WikiSearchResult,
    WikiSearchResponse,
)
from mogu_sdk.settings import MoguSettings

__version__ = "0.1.0"
__all__ = [
    "MoguClient",
    "MoguSettings",
    # Exceptions
    "MoguAPIError",
    "AuthenticationError",
    "NotFoundError",
    "PermissionDeniedError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    # Models
    "WikiFile",
    "WikiContent",
    "WikiUpdateResponse",
    "WikiSearchMatch",
    "WikiSearchResult",
    "WikiSearchResponse",
]
