"""
Session Management for HITL Tasks

Provides session storage implementations for HITL approval workflows.
Sessions store approval data between prepare-approval and process-approval.

Implementations:
- SessionManager: In-memory session storage (development/single-instance)
- RedisSessionManager: Redis-based storage (production/distributed)

Usage:
    # In-memory (development)
    from mogu_sdk.hitl import SessionManager
    session_manager = SessionManager()
    
    # Redis (production)
    from mogu_sdk.hitl import RedisSessionManager
    session_manager = RedisSessionManager(
        host="localhost",
        port=6379,
        db=0
    )
    
    # Create session
    session = session_manager.create_session(
        session_id="flow_123_node_1",
        flow_run_id="flow_123",
        task_run_id="task_456",
        node_id="node_1",
        input_data={"name": "John"}
    )
    
    # Retrieve session
    session = session_manager.get_session("flow_123_node_1")
    
    # Update session
    session_manager.update_session(
        session_id="flow_123_node_1",
        updates={"status": "completed"}
    )
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional

from .models import SessionData


class BaseSessionManager(ABC):
    """
    Abstract base class for session managers.
    
    Subclasses must implement:
    - create_session
    - get_session
    - update_session
    - delete_session
    """
    
    @abstractmethod
    def create_session(
        self,
        session_id: str,
        flow_run_id: str,
        task_run_id: str,
        node_id: str,
        input_data: Dict[str, Any]
    ) -> SessionData:
        """Create a new session."""
        pass
    
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a session by ID."""
        pass
    
    @abstractmethod
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session with new data."""
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        pass


class SessionManager(BaseSessionManager):
    """
    In-memory session manager.
    
    Suitable for:
    - Development and testing
    - Single-instance deployments
    - Low-volume workloads
    
    Limitations:
    - Data lost on restart
    - Not suitable for distributed deployments
    - No automatic cleanup/TTL
    
    For production, use RedisSessionManager instead.
    
    Example:
        session_manager = SessionManager()
        
        session = session_manager.create_session(
            session_id="flow_123_node_1",
            flow_run_id="flow_123",
            task_run_id="task_456",
            node_id="node_1",
            input_data={"name": "John", "age": 30}
        )
    """
    
    def __init__(self):
        """Initialize empty session storage."""
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(
        self,
        session_id: str,
        flow_run_id: str,
        task_run_id: str,
        node_id: str,
        input_data: Dict[str, Any]
    ) -> SessionData:
        """
        Create a new session.
        
        Args:
            session_id: Unique session identifier
            flow_run_id: Workflow execution ID
            task_run_id: Task execution ID
            node_id: Node ID in workflow
            input_data: Data to be reviewed
        
        Returns:
            SessionData object with created session
        """
        session_data = {
            "flow_run_id": flow_run_id,
            "task_run_id": task_run_id,
            "node_id": node_id,
            "input_data": input_data,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        
        self._sessions[session_id] = session_data
        return SessionData(**session_data)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by ID.
        
        Args:
            session_id: Unique session identifier
        
        Returns:
            Session data dictionary or None if not found
        """
        return self._sessions.get(session_id)
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update session with new data.
        
        Args:
            session_id: Unique session identifier
            updates: Dictionary of fields to update
        
        Returns:
            True if session was updated, False if not found
        """
        if session_id not in self._sessions:
            return False
        
        self._sessions[session_id].update(updates)
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Unique session identifier
        
        Returns:
            True if session was deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        List all sessions.
        
        Returns:
            Dictionary of all sessions keyed by session_id
        """
        return self._sessions.copy()


class RedisSessionManager(BaseSessionManager):
    """
    Redis-based session manager.
    
    Suitable for:
    - Production deployments
    - Distributed systems
    - High-volume workloads
    
    Features:
    - Persistent storage
    - Automatic TTL/expiration
    - Distributed deployment support
    - Scalable performance
    
    Requirements:
        pip install redis
    
    Example:
        session_manager = RedisSessionManager(
            host="redis.example.com",
            port=6379,
            db=0,
            password="secret",
            ttl_seconds=3600
        )
        
        session = session_manager.create_session(
            session_id="flow_123_node_1",
            flow_run_id="flow_123",
            task_run_id="task_456",
            node_id="node_1",
            input_data={"name": "John", "age": 30}
        )
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        ttl_seconds: int = 3600,
        key_prefix: str = "hitl:session:"
    ):
        """
        Initialize Redis session manager.
        
        Args:
            host: Redis host address
            port: Redis port
            db: Redis database number
            password: Redis password (if required)
            ttl_seconds: Session TTL in seconds (default 1 hour)
            key_prefix: Prefix for Redis keys
        
        Raises:
            ImportError: If redis package is not installed
        """
        try:
            import redis
        except ImportError:
            raise ImportError(
                "Redis session manager requires redis package. "
                "Install with: pip install redis"
            )
        
        self.ttl_seconds = ttl_seconds
        self.key_prefix = key_prefix
        
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
    
    def _make_key(self, session_id: str) -> str:
        """Create Redis key from session ID."""
        return f"{self.key_prefix}{session_id}"
    
    def create_session(
        self,
        session_id: str,
        flow_run_id: str,
        task_run_id: str,
        node_id: str,
        input_data: Dict[str, Any]
    ) -> SessionData:
        """
        Create a new session in Redis.
        
        Args:
            session_id: Unique session identifier
            flow_run_id: Workflow execution ID
            task_run_id: Task execution ID
            node_id: Node ID in workflow
            input_data: Data to be reviewed
        
        Returns:
            SessionData object with created session
        """
        session_data = {
            "flow_run_id": flow_run_id,
            "task_run_id": task_run_id,
            "node_id": node_id,
            "input_data": input_data,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        
        key = self._make_key(session_id)
        self.redis_client.setex(
            key,
            self.ttl_seconds,
            json.dumps(session_data)
        )
        
        return SessionData(**session_data)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session from Redis.
        
        Args:
            session_id: Unique session identifier
        
        Returns:
            Session data dictionary or None if not found
        """
        key = self._make_key(session_id)
        data = self.redis_client.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update session in Redis.
        
        Args:
            session_id: Unique session identifier
            updates: Dictionary of fields to update
        
        Returns:
            True if session was updated, False if not found
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.update(updates)
        
        key = self._make_key(session_id)
        self.redis_client.setex(
            key,
            self.ttl_seconds,
            json.dumps(session)
        )
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session from Redis.
        
        Args:
            session_id: Unique session identifier
        
        Returns:
            True if session was deleted, False if not found
        """
        key = self._make_key(session_id)
        return bool(self.redis_client.delete(key))
