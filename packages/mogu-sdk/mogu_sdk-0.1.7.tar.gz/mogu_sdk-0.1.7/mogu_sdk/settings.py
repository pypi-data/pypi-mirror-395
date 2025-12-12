"""Configuration settings for Mogu SDK"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MoguSettings(BaseSettings):
    """
    Mogu SDK configuration settings.
    
    These settings can be configured via:
    1. Environment variables (with MOGU_ prefix)
    2. .env file
    3. Direct parameter passing to MoguClient
    
    Example environment variables:
        MOGU_BASE_URL=http://localhost:8000
        MOGU_TOKEN=your-oauth-token
        MOGU_WORKSPACE_ID=your-workspace-id
    """
    
    model_config = SettingsConfigDict(
        env_prefix="MOGU__",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    base_url: str = Field(
        default="http://localhost:8000",
        description="Base URL of the Mogu API server",
    )
    
    oauth_token: Optional[str] = Field(
        default=None,
        description="OAuth bearer token for authentication",
    )
    
    workspace_id: Optional[str] = Field(
        default=None,
        description="Default workspace ID to use for operations",
    )

    workflow_id: Optional[str] = Field(
        default=None,
        description="Default workflow ID to use for operations",
    )

    workflow_run_id: Optional[str] = Field(
        default=None,
        description="Default workflow run ID to use for operations",
    )
    
    timeout: float = Field(
        default=30.0,
        description="Request timeout in seconds",
        gt=0,
    )
    
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for failed requests",
        ge=0,
    )
    
    verify_ssl: bool = Field(
        default=True,
        description="Whether to verify SSL certificates",
    )
