"""
Actor command models for the Browser-AI Interface Server
Pydantic models for command validation
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class ActorCommand(BaseModel):
    """Actor command data structure"""
    type: str = Field(..., description="Command type (e.g., 'mouse', 'keyboard', 'load')")
    target: Optional[Dict[str, Any]] = Field(None, description="Command target information")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional command data")
    id: Optional[str] = Field(None, description="Unique command ID (auto-generated)")
    timestamp: Optional[str] = Field(None, description="ISO timestamp (auto-generated)")
    queuedAt: Optional[str] = Field(None, description="Queue timestamp (auto-generated)")
    status: str = Field(default="queued", description="Command status")
    
    model_config = ConfigDict(extra="allow")  # Allow additional fields for flexibility


class CommandsListRequest(BaseModel):
    """Request for sending multiple commands"""
    commands: List[ActorCommand]


class CommandResponse(BaseModel):
    """Response for command operations"""
    success: bool
    commandsQueued: int
    sessionId: str
    message: Optional[str] = None


class CommandsListResponse(BaseModel):
    """Response containing list of commands"""
    commands: List[ActorCommand]
    total: int
    sessionId: str