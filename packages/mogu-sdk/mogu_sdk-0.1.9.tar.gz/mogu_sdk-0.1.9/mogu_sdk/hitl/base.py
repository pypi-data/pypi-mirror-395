"""
Base HITL Application

Provides a base FastAPI application with common HITL endpoints pre-configured.
Developers can extend this to quickly build custom HITL microservices.

Features:
- Pre-configured FastAPI app with CORS
- Standard /prepare-approval and /process-approval endpoints
- Health check endpoint
- Session API endpoints (/api/session/{id})
- Static file serving for UI frontend
- Extensible via handler registration

Quick Start:
    from mogu_sdk.hitl import BaseHITLApp, SessionManager, build_outputs
    from fastapi import FastAPI
    
    # Create session manager
    session_manager = SessionManager()
    
    # Create base app
    app = BaseHITLApp(
        title="My HITL Task",
        version="1.0.0",
        session_manager=session_manager,
        ui_directory="./frontend/dist"
    )
    
    # Register custom prepare handler
    @app.prepare_approval_handler
    def prepare(request):
        session_id = f"{request.flow_run_id}_{request.node_id}"
        
        # Create session
        session_manager.create_session(
            session_id=session_id,
            flow_run_id=request.flow_run_id,
            task_run_id=request.task_run_id,
            node_id=request.node_id,
            input_data={**request.input_data, **request.parameters}
        )
        
        # Return UI configuration
        return {
            "approval_data": {
                "approval_type": "my_review",
                "title": "Review Data",
                "data": request.input_data
            },
            "ui_type": "iframe",
            "ui_config": {
                "url": "/ui/",
                "session_id": session_id,
                "width": "100%",
                "height": "600px"
            },
            "metadata": {
                "session_id": session_id
            }
        }
    
    # Register custom process handler  
    @app.process_approval_handler
    def process(request):
        # Build outputs from approval response
        outputs = build_outputs(request.approval_response)
        return {"outputs": outputs}
    
    # Get FastAPI app
    fastapi_app = app.get_app()
    
    # Run with: uvicorn main:fastapi_app --host 0.0.0.0 --port 8080

For complete examples, see the sample-hitl-task package.
"""

from datetime import datetime
from typing import Any, Callable, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .models import (
    PrepareApprovalRequest,
    PrepareApprovalResponse,
    ProcessApprovalRequest,
    ProcessApprovalResponse,
)
from .session_manager import BaseSessionManager


class BaseHITLApp:
    """
    Base HITL application with pre-configured endpoints.
    
    Provides a FastAPI application with standard HITL endpoints:
    - POST /prepare-approval
    - POST /process-approval
    - GET /health
    - GET /api/session/{id}
    - POST /api/session/{id}/update
    - Static files at /ui/ (if ui_directory provided)
    
    Developers register custom handlers for prepare and process logic.
    
    Args:
        title: Application title
        description: Application description
        version: Application version
        session_manager: Session manager instance
        ui_directory: Path to UI static files (optional)
        cors_origins: Allowed CORS origins (default: ["*"])
    
    Example:
        app = BaseHITLApp(
            title="My HITL Task",
            version="1.0.0",
            session_manager=SessionManager(),
            ui_directory="./frontend/dist"
        )
        
        @app.prepare_approval_handler
        def prepare(request):
            # Custom logic
            return {...}
        
        @app.process_approval_handler
        def process(request):
            # Custom logic
            return {...}
        
        fastapi_app = app.get_app()
    """
    
    def __init__(
        self,
        title: str = "HITL Microservice",
        description: str = "Human-In-The-Loop approval microservice",
        version: str = "1.0.0",
        session_manager: Optional[BaseSessionManager] = None,
        ui_directory: Optional[str] = None,
        cors_origins: list = None
    ):
        """Initialize base HITL application."""
        self.title = title
        self.description = description
        self.version = version
        self.session_manager = session_manager
        self.ui_directory = ui_directory
        self.cors_origins = cors_origins or ["*"]
        
        # Handler functions (to be registered by developer)
        self._prepare_handler: Optional[Callable] = None
        self._process_handler: Optional[Callable] = None
        
        # Create FastAPI app
        self.app = FastAPI(
            title=self.title,
            description=self.description,
            version=self.version,
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register standard endpoints
        self._register_endpoints()
        
        # Mount UI static files if directory provided
        if self.ui_directory and Path(self.ui_directory).exists():
            self.app.mount(
                "/ui",
                StaticFiles(directory=self.ui_directory, html=True),
                name="ui"
            )
    
    def _register_endpoints(self):
        """Register standard HITL endpoints."""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint for Kubernetes probes."""
            return {
                "status": "healthy",
                "service": self.title,
                "version": self.version
            }
        
        @self.app.post("/prepare-approval", response_model=PrepareApprovalResponse)
        async def prepare_approval(request: PrepareApprovalRequest):
            """
            Prepare data for human review.
            
            Calls registered prepare_handler function with the request.
            Handler must return dict with approval_data, ui_type, ui_config, metadata.
            """
            if not self._prepare_handler:
                raise HTTPException(
                    status_code=501,
                    detail="prepare_approval_handler not registered"
                )
            
            result = self._prepare_handler(request)
            return PrepareApprovalResponse(**result)
        
        @self.app.post("/process-approval", response_model=ProcessApprovalResponse)
        async def process_approval(request: ProcessApprovalRequest):
            """
            Process approved/rejected data.
            
            Calls registered process_handler function with the request.
            Handler must return dict with outputs field.
            """
            if not self._process_handler:
                raise HTTPException(
                    status_code=501,
                    detail="process_approval_handler not registered"
                )
            
            result = self._process_handler(request)
            return ProcessApprovalResponse(**result)
        
        if self.session_manager:
            @self.app.get("/api/session/{session_id}")
            async def get_session(session_id: str):
                """Get session data for the UI."""
                session = self.session_manager.get_session(session_id)
                if not session:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Session {session_id} not found"
                    )
                return session
            
            @self.app.get("/ui/api/session/{session_id}")
            async def get_session_legacy(session_id: str):
                """Legacy endpoint for backward compatibility."""
                return await get_session(session_id)
            
            @self.app.post("/api/session/{session_id}/update")
            async def update_session_data(session_id: str, request: Request):
                """Update session data from the UI."""
                session = self.session_manager.get_session(session_id)
                if not session:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Session {session_id} not found"
                    )
                
                body = await request.json()
                updates = body.get("data", {})
                
                success = self.session_manager.update_session(
                    session_id=session_id,
                    updates=updates
                )
                
                if not success:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to update session"
                    )
                
                return {"status": "updated"}
    
    def prepare_approval_handler(self, func: Callable):
        """
        Decorator to register prepare approval handler.
        
        Handler function receives PrepareApprovalRequest and should return dict with:
        - approval_data: Data to display in UI
        - ui_type: "iframe" | "react" | "webcomponent"
        - ui_config: UI configuration dict
        - metadata: Additional metadata dict
        
        Example:
            @app.prepare_approval_handler
            def prepare(request: PrepareApprovalRequest):
                return {
                    "approval_data": {...},
                    "ui_type": "iframe",
                    "ui_config": {"url": "/ui/"},
                    "metadata": {"session_id": "..."}
                }
        """
        self._prepare_handler = func
        return func
    
    def process_approval_handler(self, func: Callable):
        """
        Decorator to register process approval handler.
        
        Handler function receives ProcessApprovalRequest and should return dict with:
        - outputs: Output data for downstream tasks
        
        Example:
            @app.process_approval_handler
            def process(request: ProcessApprovalRequest):
                outputs = build_outputs(request.approval_response)
                return {"outputs": outputs}
        """
        self._process_handler = func
        return func
    
    def get_app(self) -> FastAPI:
        """
        Get the FastAPI application instance.
        
        Use this to run the application with uvicorn:
            app = BaseHITLApp(...)
            fastapi_app = app.get_app()
            
            # Run with:
            # uvicorn main:fastapi_app --host 0.0.0.0 --port 8080
        
        Returns:
            FastAPI application instance
        """
        return self.app
    
    def add_custom_endpoint(
        self,
        path: str,
        methods: list,
        handler: Callable,
        **kwargs
    ):
        """
        Add a custom endpoint to the application.
        
        Args:
            path: URL path for the endpoint
            methods: List of HTTP methods (["GET"], ["POST"], etc.)
            handler: Async function to handle requests
            **kwargs: Additional arguments passed to FastAPI route
        
        Example:
            async def custom_handler():
                return {"message": "Custom endpoint"}
            
            app.add_custom_endpoint(
                path="/custom",
                methods=["GET"],
                handler=custom_handler
            )
        """
        self.app.add_api_route(path, handler, methods=methods, **kwargs)
