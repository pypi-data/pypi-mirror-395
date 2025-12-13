"""
Session models for the Browser-AI Interface Server
Pydantic models for session management
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict


class TabIdentity(BaseModel):
    """Tab identity information for session initialization"""
    tabId: Union[str, int] = Field(..., description="Browser tab ID")
    url: str = Field(..., description="Current URL")
    title: Optional[str] = Field(None, description="Page title")
    windowId: Optional[int] = Field(None, description="Window ID")
    index: Optional[int] = Field(None, description="Tab index")
    
    @field_validator('tabId')
    def convert_tab_id_to_string(cls, value):
        """Convert tabId to string to match Node.js behavior"""
        return str(value)
        
    model_config = ConfigDict(extra="allow")  # Allow additional fields for flexibility


class SessionInfo(BaseModel):
    """Session information in the registry"""
    sessionId: str
    tabId: str
    url: str
    title: Optional[str] = None
    windowId: Optional[int] = None
    index: Optional[int] = None
    lastActivity: str = Field(..., description="ISO timestamp of last activity")
    capabilities: List[str] = Field(default=["observer", "actor"], description="Session capabilities")


class SessionStatus(BaseModel):
    """Session status information"""
    sessionId: str
    exists: bool
    eventCount: int
    unprocessedEventCount: int
    processedEventCount: int
    actorCommandCount: int
    pendingCommandCount: int
    retrievedCommandCount: int
    oldestCommand: Optional[Dict[str, Any]] = None
    created: Optional[str] = None


class SessionInitResponse(BaseModel):
    """Response for session initialization"""
    success: bool
    sessionId: str
    message: str


class SessionsListResponse(BaseModel):
    """Response for session discovery"""
    sessions: List[SessionInfo]
    total: int


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    availableSessions: Optional[List[str]] = None