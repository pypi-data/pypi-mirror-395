"""
MOGU SDK - Human-In-The-Loop (HITL) Module

This module provides reusable components for building custom HITL tasks.
HITL tasks allow human review and approval within automated workflows.

Components:
- SessionManager: Session storage and retrieval
- HITLModels: Standard request/response models
- HITLUtils: Utilities for processing approval data
- BaseHITLApp: Base FastAPI application with common endpoints

Quick Start:
    from mogu_sdk.hitl import BaseHITLApp, SessionManager
    
    session_manager = SessionManager()
    app = BaseHITLApp(
        title="My HITL Task",
        session_manager=session_manager
    )
    
    @app.prepare_approval_handler
    def prepare(request):
        # Custom preparation logic
        return {
            "approval_data": {...},
            "ui_config": {...}
        }
    
    @app.process_approval_handler
    def process(request):
        # Custom processing logic
        return {"outputs": {...}}

For complete examples, see:
    - sample-hitl-task package
    - Documentation at https://docs.mogu.com/hitl
"""

from .base import BaseHITLApp
from .models import (
    PrepareApprovalRequest,
    PrepareApprovalResponse,
    ProcessApprovalRequest,
    ProcessApprovalResponse,
    SessionData,
)
from .session_manager import SessionManager, RedisSessionManager
from .utils import (
    extract_field,
    filter_fields,
    is_approved,
    build_outputs,
    validate_approval_response,
    merge_input_with_parameters,
)

__all__ = [
    "BaseHITLApp",
    "SessionManager",
    "RedisSessionManager",
    "PrepareApprovalRequest",
    "PrepareApprovalResponse",
    "ProcessApprovalRequest",
    "ProcessApprovalResponse",
    "SessionData",
    "extract_field",
    "filter_fields",
    "is_approved",
    "build_outputs",
    "validate_approval_response",
    "merge_input_with_parameters",
]
