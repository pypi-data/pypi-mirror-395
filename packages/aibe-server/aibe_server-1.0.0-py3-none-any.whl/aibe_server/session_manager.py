"""
SessionManager - Centralized session management utility
Eliminates duplicate session validation and management logic
Direct port from SessionManager.cjs with exact functional parity
Enhanced with per-session StoryAssembler integration
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import uuid

from .story_assembler import StoryAssembler, create_mongodb_story_assembler


class SessionManager:
    """
    Session management for browser tab isolation using sessionStorage tabIds
    Exact port of Node.js SessionManager.cjs functionality
    """
    
    def __init__(self):
        # Single unified session store with active flag
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """
        Validate and retrieve session data
        
        Args:
            session_id: The session ID to validate
            
        Returns:
            Dict with keys: session, sessionInfo, error (error is None if valid)
        """
        session = self.sessions.get(session_id)
        
        if not session:
            return {
                "session": None,
                "sessionInfo": None,
                "error": {
                    "message": f"Session {session_id} not found",
                    "availableSessions": list(self.sessions.keys())
                }
            }
        
        return {
            "session": session,
            "sessionInfo": session,  # Now the same object
            "error": None
        }
    
    def validate_session_with_response(self, session_id: str, response_handler) -> Optional[Dict[str, Any]]:
        """
        Validate session and return 404 response if invalid
        
        Args:
            session_id: The session ID to validate
            response_handler: Function to call with error response
            
        Returns:
            Dict with {session, sessionInfo} if valid, None if response sent
        """
        result = self.validate_session(session_id)
        
        if result["error"]:
            response_handler(404, {
                "error": result["error"]["message"],
                "availableSessions": result["error"]["availableSessions"]
            })
            return None
        
        return result
    
    def get_or_create_session(self, tab_id: str) -> Dict[str, Any]:
        """
        Get or create session from unified sessions store
        
        Args:
            tab_id: The tab ID to use as session identifier
            
        Returns:
            The session object
        """
        if tab_id not in self.sessions:
            # Create per-session StoryAssembler for database persistence
            story_assembler = create_mongodb_story_assembler()
            
            self.sessions[tab_id] = {
                "sessionId": tab_id,
                "actorCommands": [],
                "created": datetime.now().isoformat(),
                "lastActivity": datetime.now().isoformat(),
                "unprocessedEvents": [],
                "processedEvents": [],
                "retrievedActorCommands": [],
                "story_assembler": story_assembler,
                "active": True
            }
        
        return self.sessions[tab_id]
    
    def register_session(self, session_id: str, session_info: Dict[str, Any]) -> None:
        """
        Register a new session in the unified sessions store
        
        Args:
            session_id: The session ID
            session_info: Session information object
        """
        if session_id not in self.sessions:
            story_assembler = create_mongodb_story_assembler()
            self.sessions[session_id] = {
                "sessionId": session_id,
                "actorCommands": [],
                "created": datetime.now().isoformat(),
                "unprocessedEvents": [],
                "processedEvents": [],
                "retrievedActorCommands": [],
                "story_assembler": story_assembler,
                "active": True,
                **session_info,
                "lastActivity": datetime.now().isoformat()
            }
        else:
            # Update existing session
            self.sessions[session_id].update({
                **session_info,
                "lastActivity": datetime.now().isoformat(),
                "active": True
            })
    
    def update_session_activity(self, session_id: str) -> None:
        """
        Update the last activity timestamp for a session
        
        Args:
            session_id: The session ID to update
        """
        session = self.sessions.get(session_id)
        if session:
            session["lastActivity"] = datetime.now().isoformat()
    
    def get_session_registry(self) -> List[Dict[str, Any]]:
        """
        Get all active sessions for discovery
        
        Returns:
            Array of session information objects
        """
        sessions = []
        for session_id, session in self.sessions.items():
            if session.get("active", True):  # Only return active sessions
                sessions.append({
                    "sessionId": session_id,
                    **{k: v for k, v in session.items() if k != "story_assembler"}  # Exclude non-serializable objects
                })
        return sessions
    
    def cleanup_expired_sessions(self, max_age_ms: int = 60 * 1000) -> int:
        """
        Clean up expired sessions
        
        Args:
            max_age_ms: Maximum age in milliseconds before cleanup (default: 24 hours)
            
        Returns:
            Number of sessions cleaned up
        """
        now = datetime.now()
        max_age_delta = timedelta(milliseconds=max_age_ms)
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.get("active", True):  # Only check active sessions
                last_activity = datetime.fromisoformat(session["lastActivity"])
                if now - last_activity > max_age_delta:
                    expired_sessions.append(session_id)
        
        # Remove expired sessions and close their StoryAssemblers
        for session_id in expired_sessions:
            session = self.sessions.get(session_id)
            if session and "story_assembler" in session:
                # Schedule async close_session in background
                asyncio.create_task(session["story_assembler"].close_session(session_id))
            
            self.sessions.pop(session_id, None)
        
        return len(expired_sessions)
    
    def close_session(self, session_id: str) -> bool:
        """
        Explicitly close a session and finalize its Story
        
        Args:
            session_id: Session to close
            
        Returns:
            True if session was closed, False if not found
        """
        session = self.sessions.get(session_id)
        if session and "story_assembler" in session:
            # Schedule async close_session in background
            asyncio.create_task(session["story_assembler"].close_session(session_id))
        
        # Mark as inactive instead of removing to preserve data
        if session:
            session["active"] = False
            
        return session is not None
    
    def get_session_registry(self) -> List[Dict[str, Any]]:
        """
        Get all active sessions for discovery

        Returns:
            Array of session information objects
        """
        sessions = []
        for session_id, session in self.sessions.items():
            if session.get("active", True):  # Only return active sessions
                sessions.append({
                    "sessionId": session_id,
                    **{k: v for k, v in session.items() if k != "story_assembler"}  # Exclude non-serializable objects
                })
        return sessions
    
    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data without validation (for middleware use)
        
        Args:
            session_id: The session ID
            
        Returns:
            Session data or None if not found
        """
        return self.sessions.get(session_id)
    
    def has_session(self, session_id: str) -> bool:
        """
        Check if a session exists
        
        Args:
            session_id: The session ID to check
            
        Returns:
            True if session exists
        """
        return session_id in self.sessions
    
    def get_all_session_ids(self) -> List[str]:
        """
        Get all session IDs
        
        Returns:
            Array of session IDs
        """
        return list(self.sessions.keys())
        
