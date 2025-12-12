"""Pydantic models for Mogu SDK"""

from typing import List, Optional
from pydantic import BaseModel, Field


class WikiFile(BaseModel):
    """Represents a wiki file or folder"""

    path: str = Field(..., description="Full path to the file/folder")
    name: str = Field(..., description="File/folder name")
    is_folder: bool = Field(..., description="Whether this is a folder")


class WikiContent(BaseModel):
    """Represents wiki file content"""

    path: str = Field(..., description="Path to the file")
    content: str = Field(..., description="File content")


class WikiUpdateResponse(BaseModel):
    """Response from wiki create/update/delete operations"""

    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="Success/error message")
    commit_id: Optional[str] = Field(None, description="Git commit ID")


class WikiSearchMatch(BaseModel):
    """A single search match within a file"""

    line_number: int = Field(..., description="Line number of the match")
    line_content: str = Field(..., description="Content of the matched line")
    char_offset: int = Field(..., description="Character offset within the line")
    length: int = Field(..., description="Length of the match")
    context_before: Optional[List[str]] = Field(
        None, description="Lines before the match for context"
    )
    context_after: Optional[List[str]] = Field(
        None, description="Lines after the match for context"
    )
    text_snippet: Optional[str] = Field(
        None,
        description="Character-based text snippet around the match (if snippet_chars > 0)"
    )
    snippet_match_start: Optional[int] = Field(
        None,
        description="Start position of match within the snippet (if text_snippet is provided)"
    )
    snippet_match_end: Optional[int] = Field(
        None,
        description="End position of match within the snippet (if text_snippet is provided)"
    )


class WikiSearchResult(BaseModel):
    """A wiki search result for a single file"""

    path: str = Field(..., description="Path to the file")
    name: str = Field(..., description="File name")
    matches: List[WikiSearchMatch] = Field(..., description="List of matches in the file")
    score: float = Field(..., description="Relevance score")


class WikiSearchResponse(BaseModel):
    """Response from wiki search operation"""

    results: List[WikiSearchResult] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total number of results")
    query: str = Field(..., description="The search query used")


# Internal request models (used by SDK, not exposed to users)


class CreateWikiFileRequest(BaseModel):
    """Request to create a new wiki file"""

    path: str = Field(..., description="File path relative to repository root")
    content: str = Field(default="", description="Initial file content")
    commit_message: str = Field(
        default="Create new wiki file",
        min_length=1,
        max_length=500,
        description="Commit message",
    )


class UpdateWikiFileRequest(BaseModel):
    """Request to update an existing wiki file"""

    path: str = Field(..., description="File path relative to repository root")
    content: str = Field(..., description="Updated file content")
    commit_message: str = Field(
        default="Update wiki file",
        min_length=1,
        max_length=500,
        description="Commit message",
    )


# ============================================================================
# Cost Monitoring Models
# ============================================================================


class ConsumptionFinalizeRequest(BaseModel):
    """Request to finalize consumption to database"""

    workspace_id: str = Field(..., description="Workspace identifier")
    flow_run_id: str = Field(..., description="Prefect flow run ID")
    workflow_id: Optional[str] = Field(None, description="Workflow ID")
    started_at: Optional[str] = Field(None, description="Flow start time (ISO format)")
    completed_at: Optional[str] = Field(None, description="Flow completion time (ISO format)")


class ConsumptionFinalizeResponse(BaseModel):
    """Response from consumption finalize operation"""

    record_id: str = Field(..., description="Database record ID")
    flow_run_id: str = Field(..., description="Prefect flow run ID")
    total_cost: float = Field(..., description="Total cost in USD")
    message: str = Field(..., description="Status message")
