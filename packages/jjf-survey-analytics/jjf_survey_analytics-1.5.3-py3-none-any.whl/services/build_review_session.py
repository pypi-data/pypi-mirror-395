#!/usr/bin/env python3
"""
BuildReviewSession - Session management for build-review workflow.

Manages sessions for the card-based qualitative editor, tracking:
- Session initialization and lifecycle
- Cache status for all dimensions
- Session metadata and timestamps
- Automatic session cleanup after timeout

Usage:
    from src.services.build_review_session import BuildReviewSessionManager

    # Get singleton instance
    manager = get_session_manager()

    # Create new session
    session_id, session_data = manager.create_session(
        org_name="Example Org",
        cache_status={...}
    )

    # Get session
    session = manager.get_session(session_id)

    # Sessions auto-expire after 30 minutes of inactivity
"""

import threading
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple


class BuildReviewSessionManager:
    """
    Thread-safe manager for build-review sessions.

    Handles session lifecycle, expiration, and metadata tracking.
    Sessions are stored in-memory and expire after 30 minutes of inactivity.
    """

    # Session expiration time (30 minutes)
    SESSION_TIMEOUT_MINUTES = 30

    def __init__(self):
        """Initialize session manager with empty session store."""
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def create_session(
        self,
        org_name: str,
        cache_status: Dict[str, Dict[str, Any]],
        force_refresh: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Create new build-review session.

        Args:
            org_name: Organization name
            cache_status: Dictionary mapping dimensions to cache metadata
            force_refresh: Whether user requested force refresh

        Returns:
            Tuple of (session_id, session_data):
                - session_id: UUID string
                - session_data: Complete session object

        Example cache_status:
            {
                "Program Technology": {
                    "status": "pending",
                    "cached": True,
                    "version": 1,
                    "has_user_edits": False
                },
                ...
            }
        """
        with self._lock:
            # Generate unique session ID
            session_id = str(uuid.uuid4())

            # Create session object
            now = datetime.utcnow()
            session_data = {
                "session_id": session_id,
                "org_name": org_name,
                "status": "started",
                "force_refresh": force_refresh,
                "dimensions": cache_status,
                "created_at": now.isoformat(),
                "last_activity": now.isoformat(),
                "expires_at": (now + timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)).isoformat()
            }

            # Store session
            self._sessions[session_id] = session_data

            # Clean up old sessions
            self._cleanup_expired_sessions()

            return (session_id, session_data)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session by ID.

        Args:
            session_id: Session UUID

        Returns:
            Session data dictionary or None if not found/expired
        """
        with self._lock:
            # Clean up expired sessions first
            self._cleanup_expired_sessions()

            session = self._sessions.get(session_id)
            if not session:
                return None

            # Update last activity timestamp
            now = datetime.utcnow()
            session["last_activity"] = now.isoformat()
            session["expires_at"] = (now + timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)).isoformat()

            return session.copy()

    def update_dimension_status(
        self,
        session_id: str,
        dimension: str,
        status: str,
        **kwargs
    ) -> bool:
        """
        Update dimension status within a session.

        Args:
            session_id: Session UUID
            dimension: Dimension name
            status: New status (pending, loading, completed, error)
            **kwargs: Additional metadata to update (progress, error_message, etc.)

        Returns:
            True if updated successfully, False if session not found
        """
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return False

            if dimension not in session["dimensions"]:
                session["dimensions"][dimension] = {}

            session["dimensions"][dimension]["status"] = status
            session["dimensions"][dimension].update(kwargs)

            # Update last activity
            now = datetime.utcnow()
            session["last_activity"] = now.isoformat()
            session["expires_at"] = (now + timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)).isoformat()

            return True

    def delete_session(self, session_id: str) -> bool:
        """
        Delete session by ID.

        Args:
            session_id: Session UUID

        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def cleanup_all_sessions(self) -> int:
        """
        Remove all sessions (for testing/debugging).

        Returns:
            Number of sessions deleted
        """
        with self._lock:
            count = len(self._sessions)
            self._sessions.clear()
            return count

    def _cleanup_expired_sessions(self) -> int:
        """
        Remove sessions that have expired.

        Returns:
            Number of sessions cleaned up
        """
        now = datetime.utcnow()
        expired_ids = []

        for session_id, session in self._sessions.items():
            expires_at = datetime.fromisoformat(session["expires_at"])
            if now > expires_at:
                expired_ids.append(session_id)

        for session_id in expired_ids:
            del self._sessions[session_id]

        if expired_ids:
            print(f"[BuildReviewSession] Cleaned up {len(expired_ids)} expired sessions")

        return len(expired_ids)

    def get_active_sessions_count(self) -> int:
        """
        Get count of active (non-expired) sessions.

        Returns:
            Number of active sessions
        """
        with self._lock:
            self._cleanup_expired_sessions()
            return len(self._sessions)


# Singleton instance
_session_manager_instance: Optional[BuildReviewSessionManager] = None


def get_session_manager() -> BuildReviewSessionManager:
    """
    Get singleton instance of BuildReviewSessionManager.

    Returns:
        BuildReviewSessionManager instance
    """
    global _session_manager_instance

    if _session_manager_instance is None:
        _session_manager_instance = BuildReviewSessionManager()

    return _session_manager_instance
