"""
HITL Task Models

Standard Pydantic models for HITL task requests and responses.
These models ensure consistent data structure across all HITL tasks.

Models:
- PrepareApprovalRequest: Input for prepare-approval endpoint
- PrepareApprovalResponse: Output from prepare-approval endpoint
- ProcessApprovalRequest: Input for process-approval endpoint
- ProcessApprovalResponse: Output from process-approval endpoint
- SessionData: Session storage data model
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class PrepareApprovalRequest(BaseModel):
    """
    Request model for prepare-approval endpoint.
    
    This is sent by MOGU workflow engine when execution reaches a HITL task.
    
    Attributes:
        flow_run_id: Unique identifier for the workflow execution
        task_run_id: Unique identifier for the task execution
        node_id: Node identifier in the workflow graph
        input_data: Data from previous workflow tasks
        parameters: Task configuration parameters
    
    Example:
        {
            "flow_run_id": "abc-123",
            "task_run_id": "def-456",
            "node_id": "review_data",
            "input_data": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "parameters": {
                "title": "Review User Data",
                "timeout_seconds": 3600
            }
        }
    """
    flow_run_id: str = Field(..., description="Workflow execution ID")
    task_run_id: str = Field(..., description="Task execution ID")
    node_id: str = Field(..., description="Node ID in workflow")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data from previous tasks")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task configuration parameters")


class PrepareApprovalResponse(BaseModel):
    """
    Response model for prepare-approval endpoint.
    
    Returns UI configuration and approval data to MOGU workflow engine.
    
    Attributes:
        approval_data: Data to display in the UI
        ui_type: Type of UI to display (iframe/react/webcomponent)
        ui_config: UI configuration (url, dimensions, etc.)
        metadata: Additional metadata (session_id, timestamps)
    
    Example:
        {
            "approval_data": {
                "approval_type": "hitl_review",
                "title": "Review User Data",
                "data": {"name": "John Doe", "email": "john@example.com"}
            },
            "ui_type": "iframe",
            "ui_config": {
                "url": "/ui/",
                "width": "100%",
                "height": "600px"
            },
            "metadata": {
                "session_id": "abc-123_review_data",
                "created_at": "2025-12-06T10:00:00Z"
            }
        }
    """
    approval_data: Dict[str, Any] = Field(..., description="Data to display in UI")
    ui_type: str = Field(default="iframe", description="UI type (iframe/react/webcomponent)")
    ui_config: Dict[str, Any] = Field(default_factory=dict, description="UI configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ProcessApprovalRequest(BaseModel):
    """
    Request model for process-approval endpoint.
    
    This is sent by MOGU workflow engine after user approves/rejects.
    
    Attributes:
        flow_run_id: Unique identifier for the workflow execution
        task_run_id: Unique identifier for the task execution
        node_id: Node identifier in the workflow graph
        approval_response: User's decision and modified data
    
    Example:
        {
            "flow_run_id": "abc-123",
            "task_run_id": "def-456",
            "node_id": "review_data",
            "approval_response": {
                "decision": "approved",
                "name": "John Doe",
                "email": "john.updated@example.com",
                "comments": "Updated email address"
            }
        }
    """
    flow_run_id: str = Field(..., description="Workflow execution ID")
    task_run_id: str = Field(..., description="Task execution ID")
    node_id: str = Field(..., description="Node ID in workflow")
    approval_response: Dict[str, Any] = Field(default_factory=dict, description="User's decision and data")


class ProcessApprovalResponse(BaseModel):
    """
    Response model for process-approval endpoint.
    
    Returns processed outputs for downstream workflow tasks.
    
    Attributes:
        outputs: Output data available to downstream tasks
    
    Example:
        {
            "outputs": {
                "status": "approved",
                "user_input": {
                    "name": "John Doe",
                    "email": "john.updated@example.com"
                },
                "comments": "Updated email address",
                "processed_at": "2025-12-06T10:05:00Z",
                "approved_by": "user"
            }
        }
    
    Downstream tasks can access outputs via:
        {{review_data.output.status}}
        {{review_data.output.user_input.email}}
        {{review_data.output.comments}}
    """
    outputs: Dict[str, Any] = Field(..., description="Output data for downstream tasks")


class SessionData(BaseModel):
    """
    Session data model for storing approval state.
    
    Sessions persist data between prepare-approval and process-approval calls.
    
    Attributes:
        flow_run_id: Workflow execution ID
        task_run_id: Task execution ID
        node_id: Node ID in workflow
        input_data: Original input data
        created_at: ISO timestamp of session creation
        status: Session status (pending/completed/expired)
    
    Example:
        {
            "flow_run_id": "abc-123",
            "task_run_id": "def-456",
            "node_id": "review_data",
            "input_data": {"name": "John Doe"},
            "created_at": "2025-12-06T10:00:00Z",
            "status": "pending"
        }
    """
    flow_run_id: str = Field(..., description="Workflow execution ID")
    task_run_id: str = Field(..., description="Task execution ID")
    node_id: str = Field(..., description="Node ID in workflow")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data")
    created_at: str = Field(..., description="ISO timestamp of creation")
    status: str = Field(default="pending", description="Session status")
